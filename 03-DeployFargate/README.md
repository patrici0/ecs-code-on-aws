# Deploying an application with AWS Fargate

![aws fargate logo](/03-DeployFargate/images/aws_fargate_logo.png)


**Quick jump:**

* [1. Tutorial overview](/03-DeployFargate#1-tutorial-overview)
* [2. Creating the Cluster](/03-DeployFargate#2-creating-the-cluster)
* [3. Creating the ALB](/03-DeployFargate#3-creating-the-alb)
* [4. Creating the Task Definition](/03-DeployFargate#4-creating-the-task-definition)
* [5. Creating the service](/03-DeployFargate#5-creating-the-service)
* [6. Accessing the application](/03-DeployFargate#6-accessing-the-application)
* [7. Conclusion](/03-DeployFargate#7-conclusion)


## 1. Tutorial overview

This tutorial will guide you through the utilization of an AWS Fargate to deploy the containerized application created in the previous lab.

In order to run this tutorial, you must have completed the following steps:

* [Setup Environment](/01-EnvironmentSetup)
* [Creating your Docker image](/02-CreatingDockerImage)

After concluding this tutorial, you will have an application running in AWS Fargate.

## 2. Creating the Cluster

We will create a new ECS cluster for the Fargate tasks, however, please note a single ECS cluster could supports both EC2 and Fargate tasks.

Let's create a new cluster to deploy our containers. In your AWS account Management Console, navigate to the [ECS Console](https://console.aws.amazon.com/ecs/).

On the left side panel, click on **Clusters**, then back on the main screen click the **Create cluster** button, and in the following screen select the **Networking only** cluster template. Click on **Next step**:

![cluster template](/03-DeployFargate/images/cluster_template.png)

For the **Cluster name** use `containers-workshop-fargate-cluster` and click on **Create**:

![cluster configuration](/03-DeployFargate/images/cluster_configuration.png)

## 3. Creating the ALB

Now that we've created our cluster, we need an [Application Load Balancer (ALB)](https://aws.amazon.com/elasticloadbalancing/applicationloadbalancer/) to route traffic to our endpoints. Compared to a traditional load balancer, an ALB lets you direct traffic between different endpoints. In our example, we'll use the enpoint `/`.

To create the ALB:

Navigate to the [EC2 Service Console](https://console.aws.amazon.com/ec2), and select **Load Balancers** from the left-hand menu.  Click on **Create Load Balancer**. Inside the `Application Load Balancer`, click on **Create**:

![choose ALB](/03-DeployFargate/images/select_alb.png)

Name your ALB `containers-workshop-alb` and add an HTTP listener on port 80:

![name ALB](/03-DeployFargate/images/create_alb.png)

On this same screen, under **Availability Zones** select the VPC `containers-workshop-vpc` previously created and select the two public subnets:

![select subnets](/03-DeployFargate/images/select_subnets.png)


After adding the information about your Availability Zones, click on **Next: Configure Security Settings**.

At this screen you should see a message saying that your load balancer is not using any secure listener. We can just skip this screen, by clicking on **Next: Configure Security Groups**.

>NOTE: In a production environment, you should also have a secure listener on port 443.  This will require an SSL certificate, which can be obtained from [AWS Certificate Manager](https://aws.amazon.com/certificate-manager/), or from a registrar/any CA.  For the purposes of this workshop, we will only create the insecure HTTP listener. DO NOT RUN THIS IN PRODUCTION.

Let's now create a security group to be used by your ALB. In the *Step 3: Configure Security Groups* screen, let's select the option `Create a new security group`. Change the **Security group name** to `containers-workshop-alb-sg` and create a rule allowing all traffic in the port `80`:

![create alb security group](/03-DeployFargate/images/create_alb_sg.png)

Then, click on **Next: Configure Routing**.

During this initial setup, we're just adding a dummy health check on `/`.  We'll add specific health checks for our ECS service endpoint when registering it with the ALB. Let's only fill in the field **Name** with the text `dummy`:

![add routing](/03-DeployFargate/images/configure_alb_routing.png)

Click on **Next: Register Targets** and skip this next section by just clicking on **Next: Review**. If your values look correct, click **Create**:

![alb creation](/03-DeployFargate/images/alb_creation.png)

## 4. Creating the Task Definition

To create a Task Definition, at the left side of the ECS Console menu, click on **Task Definitions**. Then click on **Create new Task Definition**. And finally Select `FARGATE` as the **Launch type compatibility** and click on **Next step**:

![type compatibility](/03-DeployFargate/images/task_compatibility.png)

In the **Task Definition Name** type `containers-workshop-fargate-task-def`. For **Task Role** choose `None`.

![task configuration](/03-DeployFargate/images/task_configuration.png)

For the *Task execution IAM role* section, you'll see the **Task execution role** field. You have to choose the role `ecsTaskEcecutionRole`. If the role doesn't exist, as it may not have been created yet, it will be created for you automatically and you'll see something like this:

![task role](/03-DeployFargate/images/task_exec_role.png)

Now scroll down, and for **Task memory (GB)** select `0.5GB`. For **Task CPU (vCPU)** select `0.25 vCPU`.

Then, click on the **Add container** button:

![task size](/03-DeployFargate/images/task_size.png)

For **Container name** type in `containers-workshop-app`. For the **Image** field, use the same ECR URL we have been using in the previous modules of this workshop, which should look like this:

    XXXXXXXXXX.dkr.ecr.us-east-1.amazonaws.com/containers-workshop-app:latest

Then, under **Port mappings** type in `80` and leave `tcp` as the protocol. Finally, click on **Add** at the bottom of the screen:

![task container](/03-DeployFargate/images/fargate_container.png)

Click on **Create**.

## 5. Creating the Service

Now that we have the description of everything we need to run our application in the `Task Definition`, the next step is to run our container using AWS Fargate. Let's do it by creating a `Service`.

In ECS, a `Service` allows you to run and maintain a specified number (the "desired count") of instances of a task definition simultaneously in an Amazon ECS cluster. If any of your tasks should fail or stop for any reason, the Amazon ECS service scheduler launches another instance of your task definition to replace it and maintain the desired count of tasks in service. You can find more information about ECS Services in the [ECS documentation](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs_services.html).

Navigate back to the [Clusters screen](https://console.aws.amazon.com/ecs/) on the ECS console, and click on the cluster name `containers-workshop-fargate-cluster` previously created.

>If you don't have a cluster named **containers-workshop-fargate-cluster**, create one following the procedures in [Creating the cluster](/03-DeployFargate#2-creating-the-cluster).

In the details page for the **containers-workshop-fargate-cluster**, under the `Services` tab, click on the **Create** button:

![service creation](/03-DeployFargate/images/service_creation.png)

Select `Fargate` as the `Launch Type`, and choose the Task Definition created in the previous section, whose name should be **containers-workshop-fargate-task-def**.
For the field **Service name** type in `containers-workshop-fargate-service`.
For the purposes of this demo, we'll only start one copy of this task, so type in `1` into the **Number of tasks** field.

>In a production environment, you will always want more than one copy of each task running for reliability and availability.

  ![create service](/03-DeployFargate/images/configure_service.png)

Scroll down and click on **Next step**.

For **Cluster VPC** select your containers-workshop VPC (whose IP looks like 10.192.0...) and for **Subnets** select both private subnets.

>Pay special attention to the subnets. You'll probably see 4, two of them are public, which we are using for the load balancer, and the other two are **private**, which we are using for the containers.

Choose `DISABLED` for the **Auto-assign public IP** option.

Under the `Load balancing` section, select `Application Load Balancer` as the **Load balancer type**. Then, under **Service IAM role** you will see a field called **Load balancer name**, so you need to select containers-workshop-alb`, which is the application load balancer created previously, and probably your only choice at this point.

Let's configure the integration between the ECS Service and the Application Load Balancer, so we are able to access the application through the ALB. Under the *"Container to load balance"* section, for the **Container name : port**  select `containers-workshop-app:80`. Then, click on **Add to load balancer**:

![add to ALB](/03-DeployFargate/images/add_container_to_alb.png)

This final step allows you to configure the container with the ALB. When we created our ALB, we only added a listener for HTTP:80.  Select this from the dropdown menu as the value for **Production listener port**.
For **Target Group Name**, select `create new` and next to it enter a value that will make sense to you later, like `containers-workshop-target`.
For **Path Pattern**, the value should be `/*`. And in the field for **Evaluation order**, type in the number `1`.

Then, for **Health check path**, use the value `/`.

![configure container ALB](/03-DeployFargate/images/configure_container_alb.png)

Finally, under the last section **Service discovery (optional)** uncheck **Enable service discovery integration**.

If the values look correct, click **Next Step**.

Since we will not use Auto Scaling in this tutorial, in the `Set Auto Scaling` screen, just click on **Next Step** and after reviewing your configurations, click on **Create Service**.

## 6. Accessing the application

After finnishing the creation of your service, go back to the ECS Console. Select the cluster and click on the **Tasks** tab. You'll see a task in `PENDING` status.

![pending task](/03-DeployFargate/images/pending_task.png)

A Fargate task can take around 30 seconds to a minute before changing its status to `RUNNING`. That's because, for each new task, an ENI (Elastic Network Interface) is created in your VPC with an IP from the subnet you chose, and then, it's attached to the Fargate task.

![running task](/03-DeployFargate/images/running_task.png)

We can test our application by accessing it through the Application Load Balancer. To find the DNS record for your ALB, navigate to the EC2 Console > **Load Balancers** > **Select your Load Balancer**. Under **Description**, you can find details about your ALB, including a section for **DNS Name**. Copy that value and enter it in your browser:

![alb web test](/03-DeployFargate/images/alb_app_response.png)

You can see that the ALB routes traffic appropriately based on the path (`/`) we specified when we registered the container

## 7. Conclusion

You have successfully deployed an application with AWS Fargate and Docker containers. This is how you deploy a serverless container app on AWS!!!

<br>

[![back to menu](/images/back_to_menu.png)][back-to-menu]  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   [![continue workshop](/images/continue_workshop.png)][continue-workshop]

[back-to-menu]: https://github.com/patrici0/ECS-Code-on-AWS
[continue-workshop]: /04-ContinuousDelivery
