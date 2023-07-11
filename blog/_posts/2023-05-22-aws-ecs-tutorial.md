---
title: "AWS ECS Tutorial: Running Your Containers on Amazon"
categories:
  - Tutorials
toc: true
author: Ndafara Tsamba
editor: Bala Priya C

internal-links:
 - Containerization
 - Amazon
 - ECS
 - Containers
excerpt: |
    Learn how to run your containers on Amazon using AWS ECS. This tutorial will guide you through the process of creating an ECS cluster, deploying a containerized application, and accessing it using the public IP address.
---
<!--sgpt-->**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. This article is about running containers on Amazon using AWS ECS. Earthly is a powerful build tool that can greatly enhance the containerization process described in this article, making it easier to build and deploy containerized applications. [Check us out](/).**

Containerization is the process of bundling the components of an application (*ie* files, libraries, and application code) into a single package that can be run consistently on any infrastructure. Containerization continues to grow in popularity because it's portable, has built-in fault tolerance, and is easily scalable.

Docker is a popular containerization solution because it allows you to build, test, deploy, and run applications within containers quickly. In combination with [Amazon Elastic Container Service (Amazon ECS)](https://aws.amazon.com/ecs/), which allows you to deploy, manage, and scale containerized applications, you can efficiently coordinate and manage your containers.

You can use Amazon ECS to run cloud-native applications built using Docker and enforce DevOps and [continuous integration](/blog/continuous-integration), continuous delivery (CI/CD) pipelines. In this article, you'll learn how to run containers in the cloud using Amazon ECS.

## Running Docker Containers Using Amazon ECS

As previously stated, this tutorial will guide you through the process of running containers in the cloud using Amazon ECS, so let's get started!

### Prerequisites

Before you begin, you'll need the following:

* An [Amazon Web Services (AWS) account](https://aws.amazon.com/console/)
* A Docker image (*ie* a readily available Docker Hub image or a Dockerized app of your choosing).

The walkthrough in this article will use a NGINX image which is hosted on Docker Hub. NGINX is a popular open-source web server that is known for its high performance, scalability, and reliability. It's commonly used to serve static and dynamic content on the web, and can also be used as a reverse proxy, load balancer, and caching server.

To retrieve the latest NGINX image on Docker Hub, use the `nginx:latest` command
in the ECS console:

<div class="wide">
![NGINX on Docker Hub]({{site.images}}{{page.slug}}/uZFgVM0.png)
</div>

### Create a New ECS Service

An [ECS](/blog/how-to-setup-and-use-amazons-elastic-container-registry) Service is a way to define and run a group of related Docker containers on an Amazon Elastic Compute Cloud (EC2) or Fargate cluster.

To create an ECS Service, you need to create a cluster, specify a task definition, configure load balancing, and then deploy the service. You'll walk through each of these steps in the following sections.

Let's start by creating a new service. Log into the AWS Management Console and search for "ECS":

<div class="wide">
![Search for "ECS"]({{site.images}}{{page.slug}}/Od6HtZu.png)
</div>

Select **Elastic Container Service** and then **Get started** to deploy your containerized application:

<div class="wide">
![Select **Get started**]({{site.images}}{{page.slug}}/2uptvbc.png)
</div>

This will open the **Clusters** page, where you can create your cluster:

<div class="wide">
![**Clusters** page]({{site.images}}{{page.slug}}/apJKuv4.png)
</div>

A cluster is simply a logical grouping of services or stand-alone tasks. To create the cluster, click on **Create cluster**, which will take you to the **Cluster configuration** page:

<div class="wide">
![**Cluster configuration** page]({{site.images}}{{page.slug}}/ddBVnBn.png)
</div>

Give the cluster a name (here, it's "EcsDemoCluster"), and under the **Networking** section, select the default Virtual Private Cloud (VPC).

A VPC allows you to create a private network which comes with the benefits of customization and security. For instance, you can customize your VPC to meet your specific networking requirements like choosing your own IP address range or selecting your own routing tables and configuration subnets.

A VPC also allows you to create security groups and network access control lists (ACLs) which control traffic to and from your instances. This makes it easier for you to enforce security policies.

After selecting the VPC, you need to select the subnets where you want the tasks to run. Subnets are logical subdivisions within a VPC. They allow you to further segment the VPC into smaller networks to isolate resources and control network traffic.

One of the benefits of using subnets is that it allows for isolation, or in other words, subnets allow you to isolate different types of resources within the VPC. For example, you can place your web servers in one subnet and your database servers in another subnet to improve security. In this example, all the subnets have been selected, so you have the ability to launch the cluster in any subnet. Finally, specify the default namespace (*ie* "EcsDemoCluster"):

<div class="wide">
![Cluster configuration and networking]({{site.images}}{{page.slug}}/ZLo8vBc.png)
</div>

Now, expand the **Infrastructure** section, which can be found after the **Networking** section. The infrastructure is the actual hardware that will be used to deploy the containers:

<div class="wide">
![**Infrastructure** details]({{site.images}}{{page.slug}}/6wXjA87.png)
</div>

The cluster is automatically configured for AWS Fargate, which is serverless with two capacity providers. You can enable Amazon EC2 instances and external instances using [Amazon ECS Anywhere](https://aws.amazon.com/ecs/anywhere/), but both require manual configurations, which is outside the scope of this article. Leaving the default option is sufficient for this tutorial.

If you want to turn on container insights, you need to expand the **Monitoring** section in order to do so. AWS Container insights help you to monitor and troubleshoot your containerized applications and they're designed to provide deep visibility into the performance and health of your containers, and the underlying infrastructure that supports them.

Container insights provide a comprehensive and easy-to-use toolset for monitoring and troubleshooting containerized applications running on AWS. However, these [insights are not free](https://aws.amazon.com/cloudwatch/pricing/) and will not be used here for this reason:

<div class="wide">
![Monitoring and tags]({{site.images}}{{page.slug}}/fcrg1xI.png)
</div>

To create a tag, expand the **Tags** section. Tags are a key-value pair that helps you to organize and identify your resources. In this instance, the tags will be used to identify and organize your clusters. As you can see in the previous image, you only have one tag that identifies how the cluster was created with the key `ecs:cluster:createdFrom` and value `ecs-console-v2`.

To create the cluster, click **Create cluster** on the right. This will take about twenty minutes, and you should see a notification at the top of the screen letting you know the cluster creation is in progress:

<div class="wide">
![Cluster creation]({{site.images}}{{page.slug}}/r8LoFZT.png)
</div>

Once the cluster has been created successfully, you'll receive a confirmation message, and the cluster will now be listed in your **All Clusters** list:

<div class="wide">
![Cluster successfully created]({{site.images}}{{page.slug}}/BFktF8s.png)
</div>

### Create a Task Definition

The next step is to create a task definition, which is essentially a blueprint of how your container should launch. It contains details such as how much CPU and memory your container should have, what image it should use, and what ports need to be opened. To create a task, click **Task definitions** from the menu on the left. This will open the **Task definition configuration** page:

<div class="wide">
![**Task definition configuration** page]({{site.images}}{{page.slug}}/gqH7vXZ.png)
</div>

Then click on **Create new task definition** to configure the task definition:

<div class="wide">
![Task definition]({{site.images}}{{page.slug}}/Ynn1EXa.png)
</div>

Fill in the **Task definition family name** (here, "DemoNGINX" was used), and then fill in the container details. "NGINX" was used as the name of the container, and "nginx:latest" as the image URI.

Input "80" for the container port; then give the port a name (*ie* "nginx80-tcp") and select **Next**:

<div class="wide">
![Task definition completed]({{site.images}}{{page.slug}}/vdvd6s8.png)
</div>

This will take you to a page where you can configure the environment, storage, monitoring, and tags. The environment allows you to specify the infrastructure requirements for the task definition and storage allows you to configure the storage options for your container including setting up data volumes and Elastic File System (EFS) mounts. These storage options can help you manage persistent data and share files across multiple containers.  

Monitoring allows you to specify the logging options such as the log group to use and tags help you to organize and categorize your task definitions. This makes it easy to manage and transfer resources across your container environment:

<div class="wide">
![Task, storage, monitoring, and tags]({{site.images}}{{page.slug}}/LmEdQcq.png)
</div>

To save money, expand the **Environment** section and change the memory from 3 GB to 2 GB. If you have a task Identity and Access Management (IAM) role, you can select it under **Task role**; otherwise, select **None**. Finally, under the **Task execution role**, select **Create new role**:

<div class="wide">
![Task environment]({{site.images}}{{page.slug}}/Ov72SQi.png)
</div>

Leave everything else as is and select **Next**. This will take you to the **Review and create** page, where you can review your settings:

<div class="wide">
![Review and create]({{site.images}}{{page.slug}}/dYi2Ync.png)
</div>

If everything looks good, click on **Create** at the bottom to create the task definition. You would get a confirmation message if the DemoNGINX task definition was created successfully:

<div class="wide">
![Task definition created successfully]({{site.images}}{{page.slug}}/GuZB2u6.png)
</div>

### Deploy the Application

Now you need to create a service to run the application. Click on the **Deploy** drop-down in the upper right-hand corner and select **Create service**:

<div class="wide">
![**Create service**]({{site.images}}{{page.slug}}/cDENSvS.png)
</div>

This will open up the **Create service** page. Under **Environment**, select the cluster that you created previously (*ie* "EcsDemoCluster") and keep everything else as it is:

<div class="wide">
![Service environment settings]({{site.images}}{{page.slug}}/PdgwOPW.png)
</div>

Scroll down to **Deployment Configuration** and give your service a name. Here, "nginx-ecs-service-demo" was used:

<div class="wide">
![Give your service a name]({{site.images}}{{page.slug}}/S4M7ve4.png)
</div>

Scroll down and expand the **Networking** section and enable the **Public IP**:

<div class="wide">
![**Networking** section]({{site.images}}{{page.slug}}/GcAtRhf.png)
</div>

<div class="wide">
![Enable Public IP for service]({{site.images}}{{page.slug}}/Zxtygwr.png)
</div>

Enabling the Public IP allows the container to communicate directly with the internet without any intermediate services or gateways:

Scroll down and expand the **Load balancing** section:

<div class="wide">
![**Load balancing** section]({{site.images}}{{page.slug}}/xfxcMlt.png)
</div>

This is where you can configure a load balancer to distribute incoming traffic across the tasks running in your service.

Click on the drop-down, and you'll see two types of load balancers you can set up. The first option is an **Application Load Balancer**, which makes routing decisions based on the application layer (*ie* you can route traffic based on whether it is HTTP or HTTPS). The second option is a **Network Load Balancer**, which makes routing decisions on the transport layer (TCP or UDP). This demo application is small and, therefore, does not need a load balancer.

To create the service, click on **Create** at the bottom of your screen:

<div class="wide">
![Create the service]({{site.images}}{{page.slug}}/KkkfDFi.png)
</div>

Like before, you should see that the service creation is in progress:

<div class="wide">
![Service creation in progress]({{site.images}}{{page.slug}}/8fpyD1U.png)
</div>

After a few minutes, you'll see the "nginx-ecs-service-demo" service.

If the service deployment goes through successfully, it will notify you and run the task:

<div class="wide">
![Service deployment was successful]({{site.images}}{{page.slug}}/5G6lE2s.png)
</div>

To verify the service is running, select the **Tasks** tab:

<div class="wide">
![**Tasks** tab]({{site.images}}{{page.slug}}/fNCn2C2.png)
</div>

Check that both the **Last status** and **Desired status** are running and click on the **Task ID** to open the task. Then under **Configuration**, click on **open address** or copy the public IP address and paste it into your browser:

<div class="wide">
![Public IP]({{site.images}}{{page.slug}}/Iz5vpSp.png)
</div>

You should see your application running, and if it is i.e. showing you a *Welcome to NGINX page*, you've successfully deployed a container on Amazon ECS:

<div class="wide">
![NGINX running]({{site.images}}{{page.slug}}/UvUra77.png)
</div>

## Conclusion

In this article, you learned how to run containers using Amazon ECS. You started by creating an ECS cluster (which is a logical grouping of resources that can be managed together) to host your containers. Then you used the latest NGINX container image hosted on Docker Hub and created a task definition. After that, you created an ECS Service which enables you to specify the number of tasks and the load balancing strategy for the container. Finally, you accessed the container using the public IP address of the service which allowed you to connect to the NGINX web server and view the default welcome page.

To optimize your container environment and improve your development workflow, you may want to explore other CI/CD tools such as [Earthly](https://earthly.dev/). One of the primary benefits of Earthly is that it focuses on developer productivity—which means developers can focus on core development instead of orchestration. This, ultimately, streamlines the development process and reduces the time and effort required to build and deploy containerized applications.

{% include_html cta/bottom-cta.html %}