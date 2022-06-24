![workshop logo](https://github.com/patrici0/ecs-code-on-aws/blob/master/images/containers-on-aws-worshop-logo.jpg)

**The automated launch of the CloudFormation stack in item 3 of the 'Environment Setup' section of this workshop is currently not working as the s3 bucket where the CloudFormation template is stored is no longer public.**
**It will be updated at some point... Meanwhile, you can find the template to deploy the VPC and the Cloud9 environment under the "Resources" directory. The file name is "containers-workshop-with-cloud9.yaml".**
**All you need to do is download the file and and then create a CloudFormation Stack uploading it as a template file.** 

# Welcome to the "Serverless containers and continuous delivery workshop on AWS"

Hello and welcome to the serverless containers and continuous delivery workshop on AWS! Please, read the instructions below carefully.

## 1. It's all about containers!

We will walk you through the very basics of containers: from installing and configuring Docker, running containers locally, deploying them on AWS container services like Amazon Elastic Container Service (ECS) and AWS Fargate, through implementing a Continuous Delivery pipeline for your containerized application.

## 2. Let's use Cloud9 as our integrated development environment!

We strongly recommend you spinning up a Cloud9 environment.

For that purpose we will launch an AWS CloudFormation template on our next section [01-EnvironmentSetup](https://github.com/patrici0/ecs-code-on-aws/tree/master/01-EnvironmentSetup).

## 3. We strongly recommend you running this workshop in the following order:

* [1. Environment Setup](/01-EnvironmentSetup)
* [2. Creating Your Docker Image](/02-CreatingDockerImage)
* [3. Deploying An Application with AWS Fargate](/03-DeployFargate)
* [4. Creating a Continuous Delivery Pipeline with Code services and Amazon ECS](/04-ContinuousDelivery)

## 4. Enough jibber jabber...

You can start the workshop by clicking on the following button:

[![start workshop](/images/start_workshop.png)][start_workshop]

[start_workshop]: /01-EnvironmentSetup
