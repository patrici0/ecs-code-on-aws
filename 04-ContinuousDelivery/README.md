# Creating a Continuous Delivery Pipeline with Code services and Amazon ECS

![CI/CD](/04-ContinuousDelivery/images/ci_cd.png)


**Quick jump:**

* [1. Tutorial overview](/04-ContinuousDelivery#1-tutorial-overview)
* [2. Creating a Source stage](/04-ContinuousDelivery#2-creating-a-source-stage)
* [3. Creating a Build stage](/04-ContinuousDelivery#3-creating-a-build-stage)
* [4. Configuring a Continuous Delivery pipeline](/04-ContinuousDelivery#4-configuring-a-continuous-delivery-pipeline)
* [5. Testing our pipeline](/04-ContinuousDelivery#5-testing-our-pipeline)

## 1. Tutorial overview

So far we've been deploying our containers into ECS manually. On a production environment, changes that happens on code or on the container image itself could be built, tested, and deployed, all automatically. This process is commonly known as Continuous Delivery (CD).

To help us achieve this, we must create a Continuous Delivery pipeline that will orchestrate different stages of our software release process. For this workshop our pipeline will have three stages:

**a) Source stage**: the Git repository branch where all the changes are promoted to a production environment. We will use *AWS CodeCommit* as our Git repository;

**b) Build stage**: automatically pulls the content from the Git repository upon detecting changes, then it builds and tags the Docker image, and pushes the new version to Amazon ECR. We will use *AWS CodeBuild* for this job;

**c) Deployment stage**: automatically deploys the new version of our application that is on Amazon ECR onto Amazon ECS. Amazon ECS itself will be responsible for deploying it without any downtime;

Since we already have the Deployment stage working, and configured ECS, we just need to create the Source and the Build stages, and later, figure out how to connect all those stages together to finally form an actual Continuous Delivery pipeline.

Let's begin with the Source stage.

## 2. Creating a Source stage

At the AWS Management Console, type `Commit` in the search field and select the service **CodeCommit** from the list.

![CodeCommit](/04-ContinuousDelivery/images/codecommit.png)

If this is your first time using CodeCommit, click on **Get started**.

![Get started with CodeCommit](/04-ContinuousDelivery/images/codecommit_get_started.png)

Otherwise click **Create repository**.

![CodeCommit create repository](/04-ContinuousDelivery/images/codecommit_create_repository.png)

For **Respository name** type `containers-workshop-repository`. Leave **Description** blank and click on **Create repository**.

![CodeCommit create repository](/04-ContinuousDelivery/images/codecommit_create_repository_II.png)

Now run the following commands to clone your repository:

    cd ~/environment
    git config --global credential.helper '!aws codecommit credential-helper $@'
    git config --global credential.UseHttpPath true
    git clone https://git-codecommit.us-east-1.amazonaws.com/v1/repos/containers-workshop-repository

The output should look similar to this:

    $ Cloning into 'containers-workshop-repository'...
    $ warning: You appear to have cloned an empty repository.
    $ Admin:~/environment $

Aditionally you'll also need to type in the following commands and add your email and a username. This is just to identify who commited a new change to the repository:

    git config --global user.email "YOUREMAIL@HERE.COM"
    git config --global user.name "USERNAME"

At this point, you should have two folders: `containers-workshop-repository` and `ecs-code-on-aws`. Now we need to copy our application to the CodeCommit repository. First, go to the folder where your application resides

    cd /home/ec2-user/environment/ecs-code-on-aws/00-Application/

Copy everything to the folder that was created when you cloned the empty repository from CodeCommit

    cp -r * /home/ec2-user/environment/containers-workshop-repository/

Then, go to the folder where we will synchronize (push) our chages with the CodeCommit repository

    cd /home/ec2-user/environment/containers-workshop-repository/

Now let's push our application to the repository

    git add .
    git commit -m "My first commit"

The output should look like this:

    $ [master 4956fb4] My first commit
    $ 62 files changed, 20787 insertions(+)
    $ create mode 100644 Dockerfile
    $ create mode 100644 app/LICENSE
    $ create mode 100644 app/css/coming-soon.css
    $ create mode 100644 app/gulpfile.js
    $ create mode 100644 app/img/AWS_logo_RGB_REV.png
    $ create mode 100644 app/img/bg-mobile-fallback.png
    $ ...

Finally execute this:

    git push origin master

The output should look like this:

    $ Counting objects: 77, done.
    $ Compressing objects: 100% (73/73), done.
    $ Writing objects: 100% (77/77), 4.27 MiB | 7.42 MiB/s, done.
    $ Total 77 (delta 5), reused 0 (delta 0)
    $ To https://git-codecommit.us-east-2.amazonaws.com/v1/repos/containers-workshop-repository
    $ * [new branch]      master -> master

We can also list the files through the CodeCommit console interface:

![CodeCommit list files](/04-ContinuousDelivery/images/codecommit_list_files.png)

## 3. Creating a Build stage

Before we create our CodeBuild environment, we need to upload a YAML file with all the build commands and specifications. This file will be read by CodeBuild everytime a new build job is executed.

In your Cloud9 environment, click on the menu **File > New File**

![Cloud9 new file](/04-ContinuousDelivery/images/cloud9_new_file.png)

Paste the following code in the new file:

```
version: 0.2

phases:
  install:
    runtime-versions:
      docker: 18
  pre_build:
    commands:
      - echo Logging in to Amazon ECR...
      - aws --version
      - $(aws ecr get-login --region $AWS_DEFAULT_REGION --no-include-email)
      - COMMIT_HASH=$(echo $CODEBUILD_RESOLVED_SOURCE_VERSION | cut -c 1-7)
      - IMAGE_TAG=${COMMIT_HASH:=latest}
  build:
    commands:
      - echo Build started on `date`
      - echo Building the Docker image...          
      - docker build -t $REPOSITORY_URI:latest .
      - docker tag $REPOSITORY_URI:latest $REPOSITORY_URI:$IMAGE_TAG
  post_build:
    commands:
      - echo Build completed on `date`
      - echo Pushing the Docker images...
      - docker push $REPOSITORY_URI:latest
      - docker push $REPOSITORY_URI:$IMAGE_TAG
      - echo Writing image definitions file...
      - printf '[{"name":"containers-workshop-app","imageUri":"%s"}]' $REPOSITORY_URI:$IMAGE_TAG > imagedefinitions.json
artifacts:
    files: imagedefinitions.json
```

Save the file by using the menu **File > Save** in Cloud9. Name it `buildspec.yml` and save it under the `containers-workshop-repository` folder

![Save the buildspec.yml file](/04-ContinuousDelivery/images/buildspec_save.png)

At this point, your repository folder should contain an `app` folder, a `Dockerfile` file and a `buildspec.yml` file. Let's push it to our repository

    git add buildspec.yml
    git commit -m "Adding the build specifications file"
    git push origin master

The `buildpsec.yml` shoudld be listed now

![List buildspec](/04-ContinuousDelivery/images/buildspec_list.png)

Now we have everything we need to create our Build environment. At the AWS Management Console, click on **Services**, type in `Build` in the search field and then select **CodeBuild** from the list

![CodeBuild](/04-ContinuousDelivery/images/codebuild.png)

If this is your first time using CodeBuild, click on **Get started**

![CodeBuild get started](/04-ContinuousDelivery/images/codebuild_get_started.png)

Otherwise, click on **Create build project**

![CodeBuild create project](/04-ContinuousDelivery/images/codebuild_create_project.png)

In the following screen, change only what's defined below:

Under the **Project configuration** section

*Project name:* `containers-workshop-build`

Under the **Source** Section

*Source provider*: `AWS CodeCommit`

*Repository*: `containers-workshop-repository`

*Branch*: `master`

Under the **Environment** Section

*Operating system*: `Ubuntu`

*Runtime*: `Standard`

*Image*: `aws/codebuild/standard:2.0`

*Privileged*: Check the box for `Enable this flag if you want to build Docker images or want your builds to get elevated privileges`

*Service role*: make sure `New service role` is selected. In `Role name`, if the role name is not already filled in, type in `codebuild-containers-workshop-build-service-role`

>NOTE: take note of your role name because you will need to modify its permissions later on

Now expand *> Additional configurations* under this **Environment** section.

Scroll down to *Environment variables*: let's create two env vars:

For `Name` type in `REPOSITORY_URI`, for `Value` type in your ECR URI, which looks like this:
    
    XXXXXXXXXXX.dkr.ecr.us-east-1.amazonaws.com/containers-workshop-app

Then click on the **Add environment variable** button to populate another variable.

For `Name` type in `AWS_DEFAULT_REGION`, for `Value` type in the region code where your ECR repository resides (e.g. `us-east-1` for N. Virginia, `us-east-2` for Ohio...).

Scroll down to the bottom of the page and click on **Create build project**. Your build project will be listed after that:

![CodeBuild list project](/04-ContinuousDelivery/images/codebuild_list_project.png)

If we try and test our build now, it will fail. There are two reasons for that:

1) The service CodeBuild doesn't have permissions to read anything from our CodeCommit repository;

2) The IAM role associated with the CodeBuild environment only has permissions to input logs into CloudWatch logs (that's the default permission created by the CodeBuild service role).

Let's fix these.

First, let's change the ECR repository permisions. At the AWS Management Console, click on **Services** > in the search field type in `ecr` and select the **ECR** service from the list

![select ECR](/04-ContinuousDelivery/images/ecr_select.png)

Click on your repository (`containers-workshop-app`). Then, click on the **Permissions** menu on left side panel. And click on the **Edit** button under the Statements section on the main screen.

![ECR add permissions](/04-ContinuousDelivery/images/ecr_add_permissions.png)

Click on **Add statement**

For *Statement name* type in `Codebuild permission`

For *Effect* select `Allow`

For *Service principal - optional* type in `codebuild.amazonaws.com`

For *Actions*, at the bottom of this page, click on the empty field under it. This will show the menu and where you need to select the following actions: `ecr:GetDownloadUrlForLayer`, `ecr:PutImage`, `ecr:CompleteLayerUpload`, `ecr:BatchGetImage`, `ecr:InitiateLayerUpload`, `ecr:BatchCheckLayerAvailability`, `ecr:UploadLayerPart`

![ECR actions](/04-ContinuousDelivery/images/ecr_actions.png)

Click on **Save**

You permissions should look exactly like this:

![ECR permissions](/04-ContinuousDelivery/images/ecr_review_permissions.png)

Next step, we need to change the IAM role associated with our CodeBuild environment. So back at the AWS Management Console, go to **Services** > in the search field type `iam` and select **IAM** from the list

![Select IAM](/04-ContinuousDelivery/images/iam.png)

On the left side panel, click on **Roles**. This will list all the roles in your account.

Type the role name `codebuild` in the search field. Click on the IAM role that looks like this:

![IAM filter role](/04-ContinuousDelivery/images/iam_filter_role.png)

You should now see the contents of the **Permissions** tab, if so, click on **Attach policies**

![Find the IAM role](/04-ContinuousDelivery/images/iam_attach_policies.png)

Now in the serch field type in `registry` and select `AmazonEC2ContainerRegistryPowerUser`. Click on **Attach policy**

![Attach ECR Power User](/04-ContinuousDelivery/images/iam_registry_policy.png)

Your permissions should look like this:

![Permissions list](/04-ContinuousDelivery/images/iam_permissions_list.png)

Now let's go ahead and configure our test build.

At the AWS Management Console, click on **Services** > in the search field type `build` and select **CodeBuild** from the drop down list.

In **CodeBuild**, on the left side panel, click on **Build projects**. Select your project by clicking on the radio button and then click on **Start build**

Under the **Source** section, make sure that the `master` branch is selected

![CodeBuild list project](/04-ContinuousDelivery/images/codebuild_test_project_new.png)

Now scroll down to the bottom of the page and click on **Start build**

The build phase might take a while to finish. Once it has completed, you should be able to go into the **Phase details** tab and see all the phases as `Succeeded`.

![CodeBuild Status Succeeded](/04-ContinuousDelivery/images/codebuild_succeeded.png)

## 4. Configuring a Continuous Delivery pipeline

Now that our Source (CodeCommit), Build (CodeBuild) and Deploy (ECS) stages are configured and tested, we need a tool to orchestrate and connect all of them together. To achieve this we will use *AWS CodePipeline*.

AWS CodePipeline already understands the concepts of Stages (Source, Build, Test, Deploy, Approval, Invoke). All we need to do is to create a pipeline, and for each stage, choose the correlated service. For example, when configuring the Source stage, we will choose our CodeCommit respository. And so on...

Let's start with the Source Stage:

At the AWS Management Console, click on **Services** > in search field type `pipeline` and select **CodePipeline** from the list.

![CodePipeline](/04-ContinuousDelivery/images/codepipeline.png)

If this is your first time using CodePipeline, click on **Get started**.

![CodePipeline Get started](/04-ContinuousDelivery/images/codepipeline_get_started.png)

Otherwise click on **Create pipeline**

![CodePipeline create](/04-ContinuousDelivery/images/codepipeline_create.png)

For **Pipeline name** type in `containers-workshop-pipeline` and click on **Next**

![CodePipeline Next Step](/04-ContinuousDelivery/images/codepipeline_next.png)

We will now configure the Source stage:

For **Source provider** select **CodeCommit**

![CodePipeline Source Stage](/04-ContinuousDelivery/images/codepipeline_source.png)

For **Repository name** select the respository created for this workshop `containers-workshop-repository`

For **Branch name** select `master`

Click on **Next**

![CodePipeline Source Stage](/04-ContinuousDelivery/images/codepipeline_repository_ii.png)

We will now configure the Buid Stage:

For **Build provider** select **CodeBuild**

![CodePipeline Build Stage](/04-ContinuousDelivery/images/codepipeline_create_build.png)

For **Project name** select `containers-workshop-build` and click on **Next**

![CodePipeline Build Stage](/04-ContinuousDelivery/images/codepipeline_create_build_ii.png)

Finally, it's time to configure the last stage of our pipeline: the Deploy Stage.

For **Deployment provider** select **Amazon ECS**

![CodePipeline Deploy Stage](/04-ContinuousDelivery/images/codepipeline_deploy.png)

For **Cluster name** select `containers-workshop-fargate-cluster`

For **Service name** select `containers-workshop-fargate-service`

For **Image filename** type in `imagedefinitions.json`

Click on **Next**

And after reviewing your config, click on **Create pipeline**.

AWS CodePiepline will automatically start the pipeline execution.

![CodePipeline Running](/04-ContinuousDelivery/images/codepipeline_running.png)

The whole process should take around 10 minutes. All three stages should be completed as `Succeeded`.

>NOTE: If your pipeline fails, one of the potential reasons could be a permissions issue. Check if the IAM Role created by your CodePipeline has ECS full permissions by going to Services > IAM > Roles. Type in the search bar the name of the role and click on it. In **Permissions policies** check if the policy attached to it has "ecs:*" permissions. If not, click on **Attach policies** and search for `AmazonECS_FullAccess`. Select it and click on **Attach policy**.


![CodePipeline Finished](/04-ContinuousDelivery/images/codepipeline_succeeded.png)


If you go to the URL of your app you won't see any changes because we didn't change anything at the application level yet. So now, let's do exactly that! Let's change something in our app to see how the pipeline executes automatically upon detecting changes to our source repository.

## 5. Testing our pipeline

Go to your Cloud9 enviroment. On the left side panel, expand the directories `MyCloud9Instance > containers-workshop-repository > app`

Right click on the `index.html` > Open

![Test your pipeline](/04-ContinuousDelivery/images/cloud9_open_index.png)

A new tab will open. In line 37, before `This application is running inside a container!`, add the following text: `This is version 2!`. The line should look like this:

![Test your pipeline](/04-ContinuousDelivery/images/cloud9_edit_html.png)

Save it by using Ctrl+S or Command+S (MacOS) or by clicking on the menu **File > Save**

Now let's commit our change to the CodeCommit repository. Go to the Terminal tab and type:

    cd /home/ec2-user/environment/containers-workshop-repository/app
    git add index.html
    git commit -m "Changing the text on the landing page"
    git push


After the push, go back to CodePipeline and watch it execute your pipeline automatically. You will see it starting in a minute or so, as the Source stage changes to `In Progress`. Wait until the last stage is completed.


![CodePipeline final run](/04-ContinuousDelivery/images/codepipeline_final_test.png)


Now go to your app URL and see the new changes in action!

If the changes are reflected on your web app, it means you have completed this workshop successfully. Congratulations!

In the next step, you'll see a summary of resources created during this workshop in case you want to clean it all up.

<br>

[![back to menu](/images/back_to_menu.png)][back-to-menu]
[![continue workshop](/images/continue_workshop.png)][continue-workshop]

[back-to-menu]: https://github.com/patrici0/ecs-code-on-aws
[continue-workshop]: /05-CleanUp
