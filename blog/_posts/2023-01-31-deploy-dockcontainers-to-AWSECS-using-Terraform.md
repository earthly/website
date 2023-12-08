---
title: "Deploying Docker Containers to AWS ECS Using Terraform"
categories:
  - Tutorials
toc: true
author: Rose Chege

internal-links:
 - ECS
 - Docker
 - AWS
 - Container
excerpt: |
    Learn how to automate the process of deploying Docker containers to AWS ECS using Terraform. This tutorial provides step-by-step instructions and code examples to help you set up the necessary infrastructure and launch your containers on AWS.
last_modified_at: 2023-07-19
---
**This article explains how to automate ECS deployment. Earthly simplifies the Docker container build process. [Check it out](https://cloud.earthly.dev/login).**

[Elastic Container Service](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html) (ECS) is a container orchestration service from AWS. It allows you to launch and manage container workloads. Recently, we published a [Deploying Docker Containers with ECS](https://earthly.dev/blog/deploy-dockercontainers-with-ecs/) guide that allows you to provision infrastructure on [ECS](/blog/how-to-setup-and-use-amazons-elastic-container-registry) . However, these steps are implemented manually.

This guide aims to help you automate the process of deploying Docker Containers to ECS using [Terraform](https://developer.hashicorp.com/terraform/intro), an infrastructure-as-code (IaC) tool.

## Prerequisites

To follow along with this guide, it's essential to have the following tools installed on your computer:

- [Docker](https://docs.docker.com/desktop/install/windows-install/) Engine
- [HashiCorp Terraform](https://developer.hashicorp.com/terraform/downloads)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [Node.js](https://nodejs.org/en/download/) runtime
- [Git](https://git-scm.com/downloads) version control system

You can get the code used in this guide from this [GitHub repository](https://github.com/Rose-stack/docker-aws-ecs-using-terraform).

## Setting Up AWS IAM Deployer User Account

To provision the infrastructure running on AWS ECS, you need an [Identity and Access Management](https://aws.amazon.com/iam/) (IAM) user account. IAM enables you to manage access to AWS resources securely. You can manage who is authenticated (signed in) and permitted (has permissions) to use resources using IAM.

On your AWS account, add an IAM by clicking the **Add user** button. Fill in the name and select the access key credential type. Check the password option if you want to create a dedicated sign in for this user.

<div class="wide">
![AWS IAM user]({{site.images}}{{page.slug}}/STi7ZSg.png)\
</div>

Click next to create user permission roles. For simplicity, give this user `AdministratorAccess` without enabling multi-factor authentication. Next, add the user to a group that has administrator access.

<div class="wide">
![AWS administrator access]({{site.images}}{{page.slug}}/ke5R8ix.png)\
</div>

This should reflect as follows:

<div class="wide">
![AWS user permissions]({{site.images}}{{page.slug}}/s1bjOVg.png)\
</div>

Proceed to the next step and create a user. This will create a user access key ID and a secret access key. Copy these credentials and configure them to your installed AWS CLI as follows.

Launch your command line and run the following command:

~~~{.bash caption=">_"}
aws configure
~~~

Provide your AWS IAM user details:

- AWS Access Key ID
- AWS Secret Access Key
- Default region name: For example, us-east-1
- Default output format: [json](/blog/convert-to-from-json)

<div class="wide">
![AWS CLI configuration]({{site.images}}{{page.slug}}/A4RgDXD.png)\
</div>

That's all you need for AWS configuration.

## Setting Up a Docker App

To demonstrate how to automate tasks using [Terraform](/blog/kubernetes-terraform), you need a demo application. Let's get a simple Node.js application running. If you have an application ready, you can skip this step and use the application alongside this guide.

Navigate to your directory of choice and run the following command to clone the demo Node.js application from GitHub.

~~~{.bash caption=">_"}
git clone https://github.com/Rose-stack/demo_node_app.git
~~~

A `demo_node_app` directory containing your application will be created. You can `cd` into this newly created folder:

~~~{.bash caption=">_"}
cd demo_node_app
~~~

Go ahead and run the following command to install the needed dependencies for this application:

~~~{.bash caption=">_"}
git clone https://github.com/Rose-stack/demo_node_app.git
~~~

To test this application, run this command:

~~~{.bash caption=">_"}
node index.js
~~~

Open `http://localhost:5000/` on your browser and check if the application is working. You should see the following basic CRUD web app:

<div class="wide">
![Node.js demo app]({{site.images}}{{page.slug}}/wshCJFG.png)\
</div>

The goal is to deploy the above application to AWS ECS.
<div class="notice--info">
Terraform will set up and automate configuration files to run the above app with Docker. Therefore, ensure Docker Engine is up and running.
</div>

## Creating Dockerfile for the App

![Creating Dockerfile for the App]({{site.images}}{{page.slug}}/yiZu7ug.png)\

Terraform checks the application's Dockerfile and instructs Docker on what needs to be done. Dockerfile contains the instructions used to create a Docker image. To create a docker image for the application, follow the steps outlined below:

First, create a `Dockerfile` file in the `demo_node_app` directory. Inside this file, add the following:

A [DockerHub](https://hub.docker.com/_/node) image to run Node.js:

~~~{.dockerfile caption="Dockerfile"}
# Pull the Node.js image
FROM node:18-alpine
~~~

Create a directory to host the application on the Docker:

~~~{.dockerfile caption="Dockerfile"}
# Create a Docker working directory
WORKDIR /app
~~~

Copy all the dependency files:

~~~{.dockerfile caption="Dockerfile"}
# Copy package.json and package-lock.json dependencies files 
COPY package*.json ./

~~~

Install the application's dependencies:

~~~{.dockerfile caption="Dockerfile"}
# Install dependencies inside Docker
RUN npm install
~~~

Copy the application files to the Docker directory:

~~~{.dockerfile caption="Dockerfile"}
# Copy the application source code
COPY . .
~~~

Add a port number to expose the Docker image:

~~~{.dockerfile caption="Dockerfile"}
# Port number to expose the Node.js app outside of Docker
EXPOSE 5000

~~~

Finally, add the command to run the application:

~~~{.dockerfile caption="Dockerfile"}
# Command to run the application
CMD ["node", "index.js"]
~~~

Note: Always ensure you have the right Dockerfile for running your application and test if your `Dockerfile` is working as expected.

Run the following command to build the image:

~~~{.bash caption=">_"}
docker build -t sample-app .
~~~

Finally, expose a container to run the image:

~~~{.bash caption=">_"}
docker run -it -p 5000:5000 sample-app
~~~

`http://localhost:5000/` should serve the same application, but this time from a Docker container.

Docker and AWS are ready. Let's now create Terraform automation procedures to get this application to the cloud using Terraform.

## Creating an Elastic Container Registry (ECR) on AWS ECS

You've verified that your application is working locally and with Docker. We'll now deploy the application to ECS. But before you can deploy your application's [container](/blog/docker-slim) to AWS ECS, you need an ECR setup.

[ECR](https://aws.amazon.com/ecr/) is an AWS service for sharing and deploying container applications. This service offers a fully managed container registry that makes the process of storing, managing, sharing, and deploying your containers easier and faster. To set up an ECR, create a `main.tf` file inside the `demo_node_app` directory.

First, you need the [Terraform AWS provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs). A provider allows Terraform to *connect to the infrastructure of your choice*.

Here you are using AWS. Therefore, inside the `main.tf` file, **add the AWS provider** as follows:

~~~{.terraform caption="main.tf"}
# main.tf
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "4.45.0"
    }
  }
}
~~~

You can always check the latest [AWS provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs). Go ahead and provide the **AWS configuration credentials** to allow Terraform to connect to AWS:

~~~{.terraform caption="main.tf"}
# main.tf
provider "aws" {
  region  = "us-east-1" #The region where the environment 
  #is going to be deployed # Use your own region here
  access_key = "enter_access_key_here" # Enter AWS IAM 
  secret_key = "enter_secret_key_here" # Enter AWS IAM 
}
~~~

Finally, create an ECR using Terraform as follows:

~~~{.terraform caption="main.tf"}
# main.tf
resource "aws_ecr_repository" "app_ecr_repo" {
  name = "app-repo"
}
~~~

This way, Terraform will communicate with AWS and create an ECR named `app-repo`. Let's test this.

Start by running the `terraform init` command. This should be the first command executed after creating a new Terraform configuration. It creates the Terraform configuration files in your working directory, `demo_node_app`.

~~~{.bash caption=">_"}
terraform init
~~~

The message **Terraform has been successfully initialized!** should be displayed on your terminal, as shown:

<div class="wide">
![Initialize terraform directory]({{site.images}}{{page.slug}}/BXlLt2i.png)\
</div>

To create an ECR, run the `plan` command; you'll be able to preview the above Terraform configuration file and the resource that will be created:

~~~{.bash caption=">_"}
terraform plan
~~~

<div class="wide">
![Terraform plan]({{site.images}}{{page.slug}}/Bt3wwzA.png)\
</div>

Terraform plan will let you see the resource that will be added, changed, or deployed to AWS. In this case, one resource, `aws_ecr_repository.app_ecr_repo`, will be added to AWS. To provision the displayed configuration infrastructure on AWS, apply the above execution plan:

~~~{.bash caption=">_"}
terraform apply
~~~

Don't forget to enter **yes** when prompted to allow Terraform to execute this command as expected.

<div class="wide">
![Terraform apply]({{site.images}}{{page.slug}}/cEGOKDb.png)\
</div>

Terraform will create the ECR. You can confirm this on your Amazon Elastic Container Registry Repositories list.

<div class="wide">
![AWS ECR]({{site.images}}{{page.slug}}/ioOVCb0.png)\
</div>

Now that you have an ECR repository ready, it's time to push your Docker image to the newly created repository. You need to run some commands that authenticate the Docker image to the registry and push the image to the repository. AWS provides these commands out of the box. To access these commands, navigate to your ECR repository and click the **View push commands** button, as shown below:

<div class="wide">
![AWS ECR]({{site.images}}{{page.slug}}/WtU0IRd.png)\
</div>

A pop-up containing the push commands for the repository will be launched. Next, execute the following command to run an authentication token that authenticates and connects the Docker client to your registry (ECR) repository.

<div class="notice--info">
Ensure you are running the following command as copied from your AWS **View push commands** section.
</div>

~~~{.bash caption=">_"}
aws ecr get-login-password --region REGION | docker login \
--username AWS --password-stdin ID.dkr.ecr.REGION.amazonaws.com 
~~~

Copy your authentication token and run command in the directory that contains the application's Dockerfile. If the authentication is successful, a **Login Succeeded** message should be logged onto your terminal.

Now, run the Docker build command to build the [container](/blog/docker-slim) from the local or working project directory:

~~~{.bash caption=">_"}
docker build -t app-repo .
~~~

After building, run the following [docker tag](https://docs.docker.com/engine/reference/commandline/tag/) command to tag the image. Doing so gives a tag to the image that you'll use to push the image to the repository.

~~~{.bash caption=">_"}
docker tag app-repo:latest ID.dkr.REGION.amazonaws.com/app-repo:latest  
~~~

Once tagged, run the [docker push](https://docs.docker.com/engine/reference/commandline/push/) command to push and publish the image to the ECR repository.  

~~~{.bash caption=">_"}
docker push ID.dkr.REGION.amazonaws.com/app-repo:latest
~~~

Finally, refresh the repository's page to verify you've successfully pushed the image to the AWS ECR repository.

<div class="wide">
![AWS ECR image]({{site.images}}{{page.slug}}/rZUhwKG.png)\
</div>

## Creating an ECS Cluster

![Creating an ECS Cluster]({{site.images}}{{page.slug}}/n5zlbCC.png)\

So far, you've created a repository and deployed the image. But whenever you want to launch, you'll need a **target**. A cluster acts as the container target. It takes a task into the cluster configuration and runs that task within the cluster.
The ECS agent communicates with the ECS cluster and receives requests to launch the container. To create a cluster where you'll run your task, add the following configurations to your `main.tf` file:

~~~{.terraform caption="main.tf"}
# main.tf
resource "aws_ecs_cluster" "my_cluster" {
  name = "app-cluster" # Name your cluster here
}
~~~

This will instruct ECS to create a new cluster named `app-cluster`. Re-run the apply command to add these changes to AWS:

~~~{.bash caption=">_"}
terraform apply
~~~

Head over to Amazon ECS Clusters, and verify that you can see these changes:

<div class="wide">
![AWS ECS cluster]({{site.images}}{{page.slug}}/Orc6r5T.png)\
</div>

## Configuring AWS ECS Task Definitions

The image is now hosted in the ECR, but to run the image, you need to launch it onto an ECS container.

To deploy the image to ECS, you first need to create a task. A task tells ECS how you want to spin up your Docker container. A task is a true blueprint for your application. It describes the container's critical specifications of how to launch your application container. These specifications include:

- Port mappings
- Application image
- CPU and RAM resources
- Container launch types such as EC2 or Fargate

An AWS ECS workload has two main launch types: [EC2](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-anywhere.html) and [Fargate](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html).

Fargate is an AWS orchestration tool. It allows you to give AWS the role of managing your container lifecycle and the hosting infrastructure. Fargate runs your container as serverless, which means you don't need to provision your container using EC2 instances. Instead of using the ECS clusters to run your container, you can use Fargate to spin up and run your container on ECS without provisioning a virtual machine on AWS.

In the next steps, you'll write the configuration that a task requires to spin up your Docker container. Terraform will automate all this for you.

You need to build a task definition to get the application ready to operate on ECS. The task specification is a text file in JSON format that lists one or more resources that make up your container. Using Task definition JSON format, provide the container specifications as follows:

~~~{.terraform caption="main.tf"}
# main.tf
resource "aws_ecs_task_definition" "app_task" {
  family                   = "app-first-task" # Name your task
  container_definitions    = <<DEFINITION
  [
    {
      "name": "app-first-task",
      "image": "${aws_ecr_repository.app_ecr_repo.repository_url}",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 5000,
          "hostPort": 5000
        }
      ],
      "memory": 512,
      "cpu": 256
    }
  ]
  DEFINITION
  requires_compatibilities = ["FARGATE"] # use Fargate as the launch type
  network_mode             = "awsvpc"    # add the AWS VPN network mode as this is required for Fargate
  memory                   = 512         # Specify the memory the container requires
  cpu                      = 256         # Specify the CPU the container requires
  execution_role_arn       = "${aws_iam_role.ecsTaskExecutionRole.arn}"
}
~~~

As described in the above config block, Terraform will create a task named `app-first-task` and also assign the resources needed to power up the container through this task. This process includes assigning the deployed image, container ports, launch type, and the hardware requirements that the container needs to run.

Creating a task definition requires `ecsTaskExecutionRole` to be added to your IAM. The above task definition needs this role, and it is specified as `aws_iam_role.ecsTaskExecutionRole.arn`. In the next step, create a resource to execute this role as follows:

~~~{.terraform caption="main.tf"}
# main.tf
resource "aws_iam_role" "ecsTaskExecutionRole" {
  name               = "ecsTaskExecutionRole"
  assume_role_policy = "${data.aws_iam_policy_document.assume_role_policy.json}"
}

data "aws_iam_policy_document" "assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy_attachment" "ecsTaskExecutionRole_policy" {
  role       = "${aws_iam_role.ecsTaskExecutionRole.name}"
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}
~~~

Run `terraform apply` to add these changes to AWS. Navigate to Amazon ECS Task Definitions, and these changes should reflect as such:

<div class="wide">
![AWS ECS task definition]({{site.images}}{{page.slug}}/qUx4QdM.png)\
</div>

Click on this task to access the specifications created in the above configurations. For example:

- Container launch type
- CPU and RAM resources
- Port mappings

### Container Launch Type

Based on the task definition, Terraform will create the task, and assign the FARGTE launch type and the AWS VPN network mode as follows:

<div class="wide">
![ECS Fargate launch type]({{site.images}}{{page.slug}}/uQU59He.png)\
</div>

### CPU and RAM Resources

Task memory (MiB) and task CPU (unit) resources will be created and assigned to the container as shown:

<div class="wide">
![AWS ECS resources]({{site.images}}{{page.slug}}/LAJ3N2c.png)\
</div>

### Port Mappings

Port mappings for the host (5000), and the container (5000) will be assigned to the resource:

<div class="wide">
![AWS ECS Port mappings]({{site.images}}{{page.slug}}/bnJ5a9s.png)\
</div>

## Launching the Container

At this point, AWS has most of the configurations needed. However, you need to connect all the above-created specifications together to launch your container successfully.

### Creating a VPC

First, you need to create a [Virtual Private Cloud Module (VPC)](https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/latest) and subnet to launch your cluster into. VPC and subnet allow you to connect to the internet, communicate with ECS, and expose the application to available zones.

Go ahead and create a default [VPC](https://earthly.dev/blog/aws-networks/#vpcs) and [subnets](https://earthly.dev/blog/aws-networks/#subnets) information for your AWS availability zones.

~~~{.terraform caption="main.tf"}
# main.tf
# Provide a reference to your default VPC
resource "aws_default_vpc" "default_vpc" {
}

# Provide references to your default subnets
resource "aws_default_subnet" "default_subnet_a" {
  # Use your own region here but reference to subnet 1a
  availability_zone = "us-east-1a"
}

resource "aws_default_subnet" "default_subnet_b" {
  # Use your own region here but reference to subnet 1b
  availability_zone = "us-east-1b"
}
~~~

### Implement a Load Balancer

Next, create a security group that will route the HTTP traffic using a load balancer. Go ahead and implement a load balancer as follows:

~~~{.terraform caption="main.tf"}
# main.tf
resource "aws_alb" "application_load_balancer" {
  name               = "load-balancer-dev" #load balancer name
  load_balancer_type = "application"
  subnets = [ # Referencing the default subnets
    "${aws_default_subnet.default_subnet_a.id}",
    "${aws_default_subnet.default_subnet_b.id}"
  ]
  # security group
  security_groups = ["${aws_security_group.load_balancer_security_group.id}"]
}
~~~

The above configuration creates a load balancer that will distribute the workloads across multiple resources to ensure application's availability, scalability, and security.

### Creating a Security Group for the Load Balancer

The next important part of allowing HTTP traffic to access the [ECS](/blog/how-to-setup-and-use-amazons-elastic-container-registry) cluster is to create a **security group**. This will be crucial for accessing the application later in this guide. Go ahead and add the security group for the load balancer as follows:

~~~{.terraform caption="main.tf"}
# main.tf
# Create a security group for the load balancer:
resource "aws_security_group" "load_balancer_security_group" {
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Allow traffic in from all sources
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
~~~

Configure the load balancer with the VPC networking we created earlier. This will distribute the balancer traffic to the available zone:

~~~{.terraform caption="main.tf"}
# main.tf
resource "aws_lb_target_group" "target_group" {
  name        = "target-group"
  port        = 80
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = "${aws_default_vpc.default_vpc.id}" # default VPC
}

resource "aws_lb_listener" "listener" {
  load_balancer_arn = "${aws_alb.application_load_balancer.arn}" #  load balancer
  port              = "80"
  protocol          = "HTTP"
  default_action {
    type             = "forward"
    target_group_arn = "${aws_lb_target_group.target_group.arn}" # target group
  }
}
~~~

### Create an ECS Service

The last step is to create an ECS Service and its details to maintain task definition in an Amazon ECS cluster. The service will run the [cluster, task, and Fargate](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html) behind the created load balancer to distribute traffic across the containers that are associated with the service. You can achieve this with the following block:

~~~{.terraform caption="main.tf"}
# main.tf
resource "aws_ecs_service" "app_service" {
  name            = "app-first-service"     # Name the service
  cluster         = "${aws_ecs_cluster.my_cluster.id}"   # Reference the created Cluster
  task_definition = "${aws_ecs_task_definition.app_task.arn}" # Reference the task that the service will spin up
  launch_type     = "FARGATE"
  desired_count   = 3 # Set up the number of containers to 3

  load_balancer {
    target_group_arn = "${aws_lb_target_group.target_group.arn}" # Reference the target group
    container_name   = "${aws_ecs_task_definition.app_task.family}"
    container_port   = 5000 # Specify the container port
  }

  network_configuration {
    subnets          = ["${aws_default_subnet.default_subnet_a.id}", "${aws_default_subnet.default_subnet_b.id}"]
    assign_public_ip = true     # Provide the containers with public IPs
    security_groups  = ["${aws_security_group.service_security_group.id}"] # Set up the security group
  }
}
~~~

To access the ECS service over HTTP while ensuring the VPC is more secure, create security groups that will only allow the traffic from the created load balancer. To do so, create a `aws_security_group.service_security_group` resource as follows:

~~~{.terraform caption="main.tf"}
# main.tf
resource "aws_security_group" "service_security_group" {
  ingress {
    from_port = 0
    to_port   = 0
    protocol  = "-1"
    # Only allowing traffic in from the load balancer security group
    security_groups = ["${aws_security_group.load_balancer_security_group.id}"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
~~~

Additionally, add an output config that will extract the load balancer URL value from the state file and log it onto the terminal.

~~~{.terraform caption="main.tf"}
# main.tf
#Log the load balancer app URL
output "app_url" {
  value = aws_alb.application_load_balancer.dns_name
}
~~~

At this point, Terraform is set to create and provision infrastructure on AWS ECS. Go ahead and run the following commands:

- `terraform validate`: This allows you to detect syntax errors, version errors, and other problems associated with your Terraform module (`main.tf`).
- `terraform plan`: Running this command gives you the ability to observe what Terraform will actually perform and what resources it will create.
- `terraform apply`:This uses your configuration to provision infrastructure on AWS. Remember to enter yes when prompted to do so.

## Testing the Infrastructure

![Testing the Infrastructure]({{site.images}}{{page.slug}}/NymMlg2.png)\

Before testing out the infrastructure, let's check the created resources. This includes:

### Services

Refresh the previous deployed cluster. The service to run this container will be updated as follows:

<div class="wide">
![AWS ECS cluster]({{site.images}}{{page.slug}}/XaQ4JJd.png)\
</div>

### VPC

Navigate to **Your VPCs** section and check the created container network:

<div class="wide">
![AWS VPC]({{site.images}}{{page.slug}}/KZvLZZr.png)\
</div>

### Subnets

The following subnets will be created in your VPCs.

<div class="wide">
![AWS subnets]({{site.images}}{{page.slug}}/SgzaM5w.png)\
</div>

### Target Groups

Target groups *route traffic requests* and define health checks for the network load balancer. Below is how Terraform provisioned the Target groups that are in the load balancer available zones:

<div class="wide">
![AWS target groups]({{site.images}}{{page.slug}}/UfM3bF7.png)\
</div>

### Load Balancer

Finally, the load balancer for distributing and accessing the application traffic across the created targets will be created as follows:

<div class="wide">
![AWS load balancer]({{site.images}}{{page.slug}}/BXLGIhy.png)\
</div>

You should see the application's URL on your terminal.

<div class="wide">
![Terraform load balancer output]({{site.images}}{{page.slug}}/S5gXxeM.png)\
</div>

You can also access the URL from your `load-balancer-dev` as the DNS name. Copy it to your browser. You'll see that the AWS ECS provisioned application has been served.

<div class="wide">
![Terraform AWS ESC app]({{site.images}}{{page.slug}}/ooVQetM.png)\
</div>

Note that you can get a **503 Service Temporarily Unavailable** if you test your application immediately after running the `terraform apply` command. Give the infrastructure a few seconds to bring all components online.

To destroy this dev infrastructure and avoid AWS additional costs, run the following command:

~~~{.bash caption=">_"}
terraform destroy
~~~

## Conclusion

In this tutorial, we explored using [Terraform](/blog/kubernetes-terraform) for automating cloud infrastructure tasks. We began with local application creation and then automated its deployment to the AWS ECS platform using Terraform.

As you continue to refine your build process, you might want to consider other tools that can further streamline your workflow. If you're interested in efficient container-based builds, give [Earthly]((https://cloud.earthly.dev/login)) a spin. It's designed to make your build process even smoother.

I hope this guide proved useful to you and that it opens up new possibilities for your cloud infrastructure tasks.

{% include_html cta/bottom-cta.html %}
