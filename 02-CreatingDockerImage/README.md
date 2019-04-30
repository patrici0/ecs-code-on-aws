# Creating your Docker image

![container](/02-CreatingDockerImage/images/container.png)


## Quick jump:

* [1. Tutorial overview](/02-CreatingDockerImage#1-tutorial-overview)
* [2. Creating your first image](/02-CreatingDockerImage#2-creating-your-first-image)
* [3. Creating the image repository with ECR](/02-CreatingDockerImage#3-creating-the-image-repository-with-ecr)
* [4. Pushing our tested images to ECR](/02-CreatingDockerImage#4-pushing-our-tested-images-to-ecr)

## 1. Tutorial overview

This tutorial is going to drive you through the process of creating your first Docker image, running this image locally and pushing it to a image repository. If you are going to execute this lab in the Clou9 environment, you can jump to [2. Creating your first image](/02-CreatingDockerImage#2-creating-your-first-image).

>This Docker image will have a very simple web application that you can find in the `00-Application/app` directory.

In this tutorial, we assume that you completed the [Environment Setup tutorial](/01-EnvironmentSetup) and:

* [Have a working AWS account](<https://aws.amazon.com>)
* [Have the AWS CLI installed](<http://docs.aws.amazon.com/cli/latest/userguide/installing.html>)

All the tools you need for this workshop should come pre-installed with your Cloud9 environment.

To check if you have the AWS CLI installed and configured:

    $ aws --version

This should return something like:

    $ aws --version
    aws-cli/1.14.9 Python/2.7.13 Linux/4.9.81-35.56.amzn1.x86_64 botocore/1.8.13

To check if you have Docker installed:

    $  docker -v

This should return something like:

    Docker version 17.12.0-ce, build 3dfb8343b139d6342acfd9975d7f1068b5b1c3d3

If you have completed these steps, you are good to go!

## 2. Creating your first image

The following steps should be executed in your Cloud9 environment.

If you haven't executed the `git clone` command present in the [Setup Environment](/01-EnvironmentSetup#5-cloning-the-workshop-repository) chapter, do it now using the following command:

    $ git clone https://github.com/patrici0/ECS-Code-on-AWS.git

Now we are going to build and test our containers locally.  If you've never worked with Docker before, there are a few basic commands that we'll use in this workshop, but you can find a more thorough list in the [Docker "Getting Started" documentation](https://docs.docker.com/engine/getstarted/).

In this step, we are going to build a *Docker image* with a simple web application. The application that we will be using is available on the directory `00-Application` inside the project folder. In this case, lets's navigate to the `00-Application` directory:

    $ cd ECS-Code-on-AWS/00-Application/

Take a look at the contents of this directory. You will see that there is a directory called `app/` and also a file called `Dockerfile`. We will be using this `Dockerfile` to package our web application. In order to do that, run the following command inside the `00-Application` directory:

    $ docker build -t containers-workshop-app .

This should output steps that look something like this:

    Sending build context to Docker daemon  9.295MB
    Step 1/9 : FROM node:alpine
     ---> 5ce79d7a9aad
    Step 2/9 : COPY app/ /app
     ---> 5db182714408
    Step 3/9 : WORKDIR /app
    Removing intermediate container 0fed50590e13
     ---> 8b89b65c5c67
    Step 4/9 : RUN npm install --global gulp && npm install gulp
     ---> Running in f86ae7a1e8bb

If the container builds successfully, the output should end with something like this:

    Successfully built 0c50204fc662
    Successfully tagged containers-workshop-app:latest

To run your container:

     $  docker run -d -p 8080:80 containers-workshop-app

To check if your container is running:

     $ docker ps

This should return a list of all the currently running containers.  In this example,  it should just return a single container, the one that we've just started:

    CONTAINER ID        IMAGE                     COMMAND             CREATED                  STATUS              PORTS                          NAMES
    1255ca3087f5        containers-workshop-app   "node server.js"    Less than a second ago   Up 1 second         0.0.0.0:80->8080/tcp, 8080/tcp   nifty_snyder



To test the application, you can use the Cloud9 `Preview Running Application` feature. In Cloud9, click on the menu `Preview` > `Preview Running Application`

![Preview Running Application](/02-CreatingDockerImage/images/preview_application.png)

If everything went well, you should see your web application:

![Web Application](/02-CreatingDockerImage/images/web_application.png)



## 3. Creating the image repository with ECR

Before we can build and push our images, we need somewhere to push them to.  In this case, we're going to create just one repository in [ECR](https://aws.amazon.com/ecr/).

To create a repository, navigate to the [ECR console](https://console.aws.amazon.com/ecr). If this is the first time that you are accessing the ECR console, you will see the **Get Started** button in the top right corner. Click on it:

![get started ecr](/02-CreatingDockerImage/images/getting_started_ecr.png)


Name your first repository **containers-workshop-app**:

![create ecr repository](/02-CreatingDockerImage/images/creating_repository.png)

Once you've created the repository, you will be redirected to the ECR main screen. You will be able to see your newly created repository:

![ecr main screen](/02-CreatingDockerImage/images/ecr_main_screen.png)

Now, access your repository by clicking on its name. Then click on the button **View push commands** at the top right corner. It will display a list of commands that you will need to use to push your Docker images. The list of commands should look like this:

![push commands](/02-CreatingDockerImage/images/push_commands.png)

## 4. Pushing our tested images to ECR

Now that we've tested our images locally, we need to tag them again, and push them to ECR.  This will allow us to use them in `Task definitions` that can be deployed to an ECS cluster.

Now you'll need to use some push commands.

The first thing that we need to do, is authenticate our Docker client to the ECR. To do this, we need to get the `docker login` command with the repository information. To get this information, run the following command:

    $ aws ecr get-login --no-include-email

>NOTE: If you are running it on a linux terminal, you can just run the command like this `$(aws ecr get-login --no-include-email --region us-east-1)` which will tell your shell to execute the output of the previous command for you.

The output of this command is the `docker login` command that we wil need to run. It is going to be similar to:

    docker login -u AWS -p eyJwYXlsb2FkIjoiQXowb3lmSVNpa2dCeUF0UCt3UjRyN3JqZ2w0ZVFqbjMwQXBFY2szVkRQRUx6KzRMb3REUHhLTlowYk9ncWZYelhwclhXdW1vWm5GVzJPVi9LSDhaRlVsTUtxaGVPMWU2RzV6Njg2QlAraXVDSklPMXdZVTNpNTBLVkR2dnUyaVZ2SkRZUEdmM3BLR0IvSG9WQWFFZmJJVFRJNkZPODVOQWRvcEpHYnJhYmNGQXYvckVGQ0FLa1pkQ1k1NkNNTmcwNFlOek1lanpKLzQyUjZwMlV2ZjgxUVBaTm1ubWZYZE11VHA0MHQ2OGRJdDBuQi9acXZZVkN6MXVzSlJBVFUwK1A4UlNSOXlyL0N3T3lvQWlkUlFDdDlUc3Z1SHVwZGhOeHNkTHVNc1RRcDZvYS9obzFWVXhiN0RJYmhrcWEwdlVIREhtS2t0OTFpUnFGcFV5aVBhYk80eTVGaXlzOU15NkN5QlIzZlI4U2lOUDlmaW9tb2hvMklYYkdZeHpsYXNKK0FvTGFkU2xhYUFxRkRzeGpPaEJRL1ZlTWlNL2Z3bHhDYytuMUdrK29LT1lsZm5LTS9RdUdNcVdXTkJpN1VxUncyN3p4VjJCR3NPT05NaXVMemlQUlhyWXhucVpxTDh6b2JpN25KQy96UXFsRERqdExPTW9UMGdiSmo1bWloTXVqdm4vWWZYRDVqQnAxWTRSNW5YcCtwQ2Q4Z0NSQKSJFXlKT0hUZUJuM21VZFR0N2EzdmhxNWoyL0RtdFJxYVpPNUpSMm9GWjY5UmJYUUFUSStLMDBVZ1lMMFpZVHcycXorbGVZYlh0YzlxK2FTM3krSm53L2FNZVNiUGtoOWJuU01CZDQvSFcvemcxUElsRlhvOEZpTG1ZakppNEpRcHJIa2czemk0ektOOS9NL3pOaXVXSXp1a3Ezb05QZjMrUndZSmptdy9mbFd3OEJGLzJoejJJVXVhbENkWkYzdldRaUhRNEt3YjBYNVFidXdvZTVZOWwyNEJZcVBMdEh4V0xrUUFuS2NVUkEvVTNVSlpLaEVVZXlMV28vSFBYWmxUSK820WUVMU25hNTVUWTJqa0VCcXBhaTEyQTJyTGwwM0tjUjY1VzNyZU05RUVUMmswTmJhZVNWZmNkQ28rUE95dUxCSHJTS2RIVHozbzNuVzE2SlhtaTdOWlRSMlBjMkFCOEExQTNXN01zaGJGcjRqbUs1a1UySWI2cnRjeWcrU2g2Zm0xYWhpQlRueXJrbzlpZGhGanVWbU1GOHppL29jZ3JBTG80TjExOGlvejZwNkxSWmhdVMmdmUWI5UnFGRkXKSjJRVXdFcHBqWXhtSzRLQ0RwTWF4NVhGM1czT1c1MjM1ejV3emR1ZGxwclg5TWdGbmY2Q3ljdjA2YlFEa25LeVZVK2VOQXZqUkZlWndhZGJKeTZtMzdRYkI4MllNN25VVmREVmhtOXpKV0dEUlNQVWpGSzYrLCJkYXRha2V5IjoiQVFFQkFIaHdtMFlhSVNKZVJ0Sm01bjFHNnVxZWVrWHVvWFhQZTVVRmNlOVJxOC8xNHdBQUFINHdmQVlKS29aSWh2Y05BUWNHb0c4d2JRSUJBREJvQmdrcWhraUc5dzBCQndFd0hnWUpZSVpJQVdVREJBRXVNQkVFREtQbEE5b1VnVUpyY3JkOFFRSUJFSUE3MHJETXcwMFJUc0R4eDBCOEN2NXJTK25waW5iUEw4WG9UeUpubmxnbWhGTFkwcGo3WGg4ZEpxMHlkSXpNWGhYT2xxb2ZFUFU4UVk4UkZkRT0iLCJ2ZXJzaW9uIjoiMiIsInR5cGUiOiJEQVRBX0tFWSIsImV4cGlyYXRpb24iOjE1MjE4ODIxOTZ9 https://XXXXXXXXX.dkr.ecr.us-east-1.amazonaws.com

To login to ECR, copy this output and execute it as a linux command. The output will be the following:

    WARNING! Using --password via the CLI is insecure. Use --password-stdin.
    Login Succeeded  

If you are unable to login to ECR, check your IAM user group permissions.

Now, let's tag our image locally and then push our image to the ECR repository. Use the following commands:

    $ docker tag containers-workshop-app:latest XXXXXXXXX.dkr.ecr.us-east-1.amazonaws.com/containers-workshop-app:latest
    $ docker push XXXXXXXXX.dkr.ecr.us-east-1.amazonaws.com/containers-workshop-app:latest

>NOTE: Remember to replace the `XXXXXXXXX` with your account ID. This information will be presented to you in the ECR screen with the Docker push commands.

> Why `:latest`?  This is the actual image tag.  In most production environments, you'd tag images for different schemes:  for example, you might tag the most up-to-date image with `:latest`, and all other versions of the same container with a commit SHA from a CI job.  If you push an image without a specific tag, it will default to `:latest`, and untag the previous image with that tag.  For more information on Docker tags, see the Docker [documentation](https://docs.docker.com/engine/getstarted/step_six/).


This step will take a few minutes. When the command finishes, you should see something like this:

    The push refers to a repository [XXXXXXXXX.dkr.ecr.us-east-1.amazonaws.com/containers-workshop-app]
    9ef5219507db: Pushed
    b3d18e8f520f: Pushed
    a83b4d2ff3a0: Pushed
    2f5b0990636a: Pushed
    c9748fbf541d: Pushed
    b3968bc26fbd: Pushed
    aa4e47c45116: Pushed
    788ce2310e2f: Pushed
    latest: digest: sha256:38588bb240b57d123522ab3d23cec642907a99f1379445fbea27dafc58608 size: 1988


You can see your pushed images by viewing the repository in the AWS Console.  Alternatively, you can use the CLI:

    $ aws ecr list-images --repository-name=containers-workshop-app --region us-east-1

Whose output will look like this:

    {
        "imageIds": [
            {
                "imageTag": "latest",
                "imageDigest": "sha256:38588bb240b57d123522ab3d23107cec6438d7a99f1379445fbea27dafc58608"
            }
        ]
    }

<br>

[![back to menu](/images/back_to_menu.png)][back-to-menu]  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   [![continue workshop](/images/continue_workshop.png)][continue-workshop]

[back-to-menu]: https://github.com/patrici0/ECS-Code-on-AWS
[continue-workshop]: /03-DeployFargate
