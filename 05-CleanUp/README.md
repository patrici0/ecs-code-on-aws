# Cleaning up AWS resources

![CleanUp](/05-CleanUp/images/clean-up.png)


**Quick jump:**

* [1. AWS IAM](/05-CleanUp#1-aws-iam)
* [2. AWS Code* tools](/05-CleanUp#2-aws-code*-tools)
* [3. Amazon ECS](/05-CleanUp#3-amazon-ecs)
* [4. Amazon EC2](/05-CleanUp#4-amazon-ec2)
* [5. Amazon S3](/05-CleanUp#5-amazon-s3)
* [6. AWS Cloudformation](05-CleanUp#6-aws-cloudformation)

## 1. AWS IAM
Clean up the following resources in order:
```
delete role AWSCodePipelineServiceRole-us-east-1-containers-workshop-pipeli
delete role codebuild-containers-workshop-build-service-role
delete role ecsTaskExecutionRole
delete role cwe-role-us-east-1-containers-workshop-pipeline
delete policy AWSCodePipelineServiceRole-us-east-1-containers-workshop-pipeline
delete policy CodeBuildBasePolicy-containers-workshop-build-us-east-1
delete policy start-pipeline-execution-us-east-1-containers-workshop-pipelinecode 
```

## 2. AWS Code* tools
Clean up the following resources in order:
```
delete CodePipeline pipeline
delete CodeBuild project
delete CodeCommit repository
```

## 3. Amazon ECS
Clean up the following resources in order:
```
stop/delete the tasks in the cluster
delete the service in the cluster
delete the cluster
deregister/delete the task definition versions
delete ECR repo
```

## 4. Amazon EC2
Clean up the following resources in order:
```
delete load balancer
delete target groups
delete security groups “contai” and “containers-workshop-alb-sg”
```

## 5. Amazon S3
Clean up the following resources in order:
```
delete bucket codepipeline-us-east-1-*
```

## 6. AWS Cloudformation
Clean up the following resources in order:
```
delete stack containers-workshop-infrastrucutre
```

<br>

[![back to menu](/images/back_to_menu.png)][back-to-menu]

[back-to-menu]: https://github.com/patrici0/ecs-code-on-aws
