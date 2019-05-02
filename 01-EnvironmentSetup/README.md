# Environment Setup

![environment setup](/01-EnvironmentSetup/images/environment_setup.png)

This section describes the hardware and software needed for this workshop, and how to configure them. This workshop is designed for a BYOL (Brying Your Own Laptop) style hands-on-lab.


**Quick jump:**

* [1. First Notes](/01-EnvironmentSetup#1-first-notes)
* [2. The VPC Structure](/01-EnvironmentSetup#2-the-vpc-structure)
* [3. Infrastructure Setup (with Cloud9)](/01-EnvironmentSetup#3-infrastructure-setup-with-cloud9)
* [4. Understanding the Cloud9 Interface](/01-EnvironmentSetup#4-understanding-the-cloud9-interface)
* [5. Cloning the workshop repository](/01-EnvironmentSetup#5-cloning-the-workshop-repository)


## 1. First Notes

This workshop can be executed both on a Cloud9 environment or in your own computer. Cloud9 is a cloud-based integrated development environment (IDE) that lets you write, run, and debug your code with just a browser. This environment already comes with Git, Docker, AWS CLI and all the necessary tools that you'll need to run this lab.

## 2. The VPC Structure

For this workshop, we are going to use a VPC with public and private subnets. All Fargate tasks should run on private subnets. All Load Balancers should run on public subnets.

> NOTE: If you are running this workshop on a large group of people, you can optionally create just one VPC for the entire workshop, instead of one VPC per workshop participant. This is just to prevent you hitting some VPC limits for your AWS account, like number of VPCs per region and number of Elastic IPs per region.

![VPC structure](/01-EnvironmentSetup/images/containers-on-aws-workshop-vpc.png)

## 3. Infrastructure Setup (with Cloud9)

In order to deploy the infrastructure to your account, you can use one of the following links according to the region you want to use. These are the regions that currently support Fargate and Cloud9.

|Deploy | Region |
|:---:|:---:|
|[![launch stach](/01-EnvironmentSetup/images/launch_stack_button.png)][us-east-1-with-cloud9] | US East (N. Virginia)|
|[![launch stach](/01-EnvironmentSetup/images/launch_stack_button.png)][us-east-2-with-cloud9] | US East (Ohio)|
|[![launch stach](/01-EnvironmentSetup/images/launch_stack_button.png)][us-west-2-with-cloud9] | US West (Oregon)|
|[![launch stach](/01-EnvironmentSetup/images/launch_stack_button.png)][eu-west-1-with-cloud9] | EU (Ireland)|
|[![launch stach](/01-EnvironmentSetup/images/launch_stack_button.png)][ap-southeast-1-with-cloud9] | Asia Pacific (Singapore)|

In the CloudFormation screen, add your name under the resource naming. This is going to add your name in front of the names of all the resources created, so if you are running the workshop along with someone else using the same account, you will be able to know your which are your resources.

Wait till the status of the stack changes to `CREATE_COMPLETE`, click on the **Outputs** tab and take note of all the values in the **Value** colunm. As you are using a template that also provisions a Cloud9 instance, you will see the `Cloud9URL` value. You can use this URL to access your Cloud9 instance:

![CloudFormation Output](/01-EnvironmentSetup/images/cloudformation_output.png)

## 4. Understanding the Cloud9 Interface

AWS Cloud9 is a cloud-based integrated development environment (IDE) that lets you write, run, and debug your code with just a browser. During this workshop, we will be using Cloud9 to interact with the application code and Docker containers. Since Cloud9 has everything we need to run the workshop, let's take a moment now to understand where we will be running our commands and executing the steps.

This is the main interface presented by Cloud9 and the first thing you will see when clicking in the CloudFormation output URL:

![Cloud9 Main Screen](/01-EnvironmentSetup/images/cloud9_main_screen.png)

All the commands presented in the workshop, such as `docker build`, `aws ecr get-login` and so on, should be executed in the terminal window:

![Cloud9 Terminal](/01-EnvironmentSetup/images/cloud9_terminal.png)

>NOTE: You can arrange the size of the windows inside the Cloud9 interface.

On the left side panel, you will see a list of all your files:

![Cloud9 Files](/01-EnvironmentSetup/images/cloud9_files.png)

On the top window, you have a text editor, where you can make changes to the files. If you just click twice on any file on the *files** menu, you will be able to edit it:

![Cloud9 Editor](/01-EnvironmentSetup/images/cloud9_editor.png)

## 5. Cloning the workshop repository

In order to clone this repository, you can use the following command:

    $ git clone https://github.com/patrici0/ECS-Code-on-AWS.git

After cloning the repository, you will see that a new folder called `ECS-Code-on-AWS` has been created. All the content will be available inside this folder.

After provisioning the infrastructure and cloning the repository within your Cloud9 environment, you can go to the next chapter: [2. Creating your Docker image](/02-CreatingDockerImage).

<br>

[![back to menu](/images/back_to_menu.png)][back-to-menu]  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   [![continue workshop](/images/continue_workshop.png)][continue-workshop]

[back-to-menu]: https://github.com/patrici0/ECS-Code-on-AWS
[continue-workshop]: /02-CreatingDockerImage

[us-east-1-with-cloud9]: https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=containers-workshop-insfrastructure&templateURL=https://s3.amazonaws.com/ecs-code-on-aws/containers-workshop-with-cloud9.yaml
[us-east-2-with-cloud9]: https://console.aws.amazon.com/cloudformation/home?region=us-east-2#/stacks/new?stackName=containers-workshop-insfrastructure&templateURL=https://s3.amazonaws.com/ecs-code-on-aws/containers-workshop-with-cloud9.yaml
[us-west-2-with-cloud9]: https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=containers-workshop-insfrastructure&templateURL=https://s3.amazonaws.com/ecs-code-on-aws/containers-workshop-with-cloud9.yaml
[eu-west-1-with-cloud9]: https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?stackName=containers-workshop-insfrastructure&templateURL=https://s3.amazonaws.com/ecs-code-on-aws/containers-workshop-with-cloud9.yaml
[ap-southeast-1-with-cloud9]: https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-1#/stacks/new?stackName=containers-workshop-insfrastructure&templateURL=https://s3.amazonaws.com/ecs-code-on-aws/containers-workshop-with-cloud9.yaml