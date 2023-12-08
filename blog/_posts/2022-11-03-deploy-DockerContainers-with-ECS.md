---
title: "Deploying Docker Containers with ECS"
categories:
  - Tutorials
toc: true
author: Somtochukwu Uchegbu

internal-links:
 - Docker
 - Container
 - ECS
 - AWS
excerpt: |
    Learn how to deploy Docker containers with AWS ECS, a beginner-friendly and cost-effective container service. With auto-scaling and a serverless option, AWS ECS makes it easy to manage and run your container applications.
last_modified_at: 2023-07-19
---
**The article details how to deploy Django applications on AWS ECS. Developers use Earthly for reliable Docker image construction. [Check it out](https://cloud.earthly.dev/login).**

## What Is AWS ECS

AWS Elastic Container Service (AWS ECS) is a managed container service that is used to run and deploy containers. It is similar to Kubernetes in that it allows us to launch, monitor, and set up docker containers within a specified cluster. Unlike Kubernetes its a AWS specific technology for managing the lifecycle of a [container](/blog/docker-slim).

<div class="notice--info">
AWS ECS is not to be confused with AWS EKS, which is AWS's kubernetes service. EKS competes with Google Kubernetes Service ( GKE ), and Azure Kubernetes Service (AKS).
</div>
With AWS [ECS](/blog/how-to-setup-and-use-amazons-elastic-container-registry), we create a cluster on which we can create various tasks we want to run. These tasks are usually individual containers that handle specific operations.
When deploying our containers, we need actual infrastructure to run our docker containers. There are two options for us here. We can either decide to handle spinning up instances, connecting them to our ECS [cluster](/blog/kube-bench), and monitoring them, or we can use **Fargate**.
Fargate is a serverless way to run docker containers. It works by taking the container we want to deploy, and automatically provisioning the resources needed to deploy that container.

## Why Use AWS ECS

Now that we have a little understanding of what ECS is and how it works. Why should we use it? are there added benefits?
You should use AWS ECS because it's:

* **Beginner-Friendly**: If you are looking for a simple and easy-to-use container service to deploy your container application, ECS is the service for you. All you need to understand is the ECS workflow which is very simple. It takes only five steps to get your container image from your local development environment to the cloud. \
* **Cost-Effectiveness**: It is very cost-effective and easy to manage. With ECS, you only need to pay for the time your services are running, nothing else. If you run your services for 1 hour, you will get billed for the 1 hour your services were running. \
* **Auto Scaling**: ECS provides auto-scaling for your infrastructure. This means that with ECS, our infrastructure will be auto-scaled with respect to the traffic we are receiving in our applications. If by chance our application cannot handle a certain amount of traffic, ECS will provision more EC2 instances and attach them to our cluster to handle the incoming traffic. \
* **Serverless**: With ECS, there is an option to use a serverless approach to provision servers. This is useful because it abstracts some of the difficult aspects such as creating EC2 instances, connecting those instances to our ECS cluster, and managing the health status of our clusters. \

## How To Deploy Docker Containers With AWS ECS

Let's deploy a Django application to ECS.

### Prerequisites

You'll need:

* An AWS account
* Docker installed on your machine
* And the AWS CLI installed

### Step 1

We need to create a simple Django application, which we will containerize locally.

Firstly, we need to create a virtual environment and install our dependencies.

~~~{.bash caption=">_"}
virtualenv env
~~~

~~~{.bash caption=">_"}
pip install django djangorestframework
~~~

Next, we need to activate our virtual environment and create our Django project.

~~~{.bash caption=">_"}
source env/bin/actviate
~~~

~~~{.bash caption=">_"}
django-admin startproject app .
~~~

We then need to create our Django application and add it to our installed apps

~~~{.python caption="manage.py"}
python manage.py startapp api
~~~

Within our app/settings.py file, add this block of code

~~~{.python caption="settings.py"}
INSTALLED_APPS = [ 
    ... 
    'rest_framework', 
    'api' 
    ...
]
~~~

Since we are going to deploy our application, we need to change some configurations in our [settings.py](http://settings.py) file.

One of which includes adding an asterisk to our _ALLOWED_HOST_ list like so

~~~{.python caption="settings.py"}
ALLOWED_HOST = ['*']
~~~

Next, we need to create a simple view in our api/views.py file. Add this block of code

~~~{.python caption="views.py"}
from rest_framework import status 
from rest_framework.response import Response 
from rest_framework.decorators import api_view 

@api_view(['GET']) 
def home_endpoint(request): 
    return Response({"message":"Hello World"}, status=status.HTTP_200_OK)
~~~

We need to create a [urls.py](http://urls.py) file (in our api directory) that will hold the url to this endpoint.

Add this block of code

~~~{.python caption="urls.py"}
from django.urls import path 
from . import views 
urlpatterns = [ 
    path('home', views.home_endpoint, name='home'), 
]
~~~

Next, we need to include our _api_ url's in our _app/urls.py_ file.

~~~{.python caption="urls.py"}
from django.urls import path, include 
urlpatterns = [ 
    path('admin/', admin.site.urls), 
    path('api/', include('api.urls')) 
]
~~~

Finally, we need to create our _requirements.txt_file.

~~~{.bash caption=">_"}
pip freeze > requirements.txt
~~~

### Step 2

We need to create a Dockerfile which will be used for creating a docker image for our application.
**Note**: The Dockerfile should be located in our root directory
Add this block of code to the Dockerfile

~~~{.dockerfile caption="Dockerfile"}
FROM python:3.10.0-alpine 
WORKDIR /usr/src/app 
RUN pip install --upgrade pip 
COPY requirements.txt /usr/src/app/ 
RUN pip install -r requirements.txt 
COPY . /usr/src/app/ 
EXPOSE 8000 
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
~~~

### Step 3

After completing our Dockerfile, we need to head on to AWS to create a docker repository using Elastic Container Registry.

After creating our registry, we will build our docker image and push it to the repository.

On the AWS management console homepage, search for ECR

<div class="wide">

![Image]({{site.images}}{{page.slug}}/image1.png)\

</div>

Click on **Elastic Container Registry**

On the ECR home page, click **Get Started**

In the registry settings, make sure to select **Public** as the repository type.

Next, we need to give our repository a name. In this case, we are going with _django-app._

After that, we need to leave every other setting as is and click on the **Create** button on the bottom right corner of the page.

<div class="wide">

![Image]({{site.images}}{{page.slug}}/image2.png)\

</div>

Next, we need to highlight our newly created repository, and click on the View push commands button.

<div class="wide">

![Image]({{site.images}}{{page.slug}}/image3.png)\

</div>

On the View push commands modal, we are given a detailed guide to follow to successfully push our docker image to our repository.

<div class="wide">

![Image]({{site.images}}{{page.slug}}/image4.png)\

</div>

The push view has a series of instructions, let's go over them.

Firstly, we need to retrieve an authentication token which we will use to authenticate our docker client to our AWS repository.

To do this, we will use the AWS CLI tool and run this command in our terminal

~~~{.bash caption=">_"}
aws ecr-public get-login-password --region us-east-1 | \
docker login --username AWS --password-stdin <REPOSITORY-URI>
~~~

Next, we need to build our docker image.

~~~{.bash caption=">_"}
docker build -t django-app .
~~~

We have tagged it `django-app` for local development. We also need to tag it with the URL of our AWS repository

~~~{.bash caption=">_"}
docker tag django-app:latest public.ecr.aws/w0p8w5x2/django-app:latest 
~~~

Finally, we push our docker image to our AWS repository

~~~{.bash caption=">_"}
docker push public.ecr.aws/w0p8w5x2/django-app:latest
~~~

Now, if we check our AWS repository, we should have an image with the tag latest.

<div class="wide">

![Image]({{site.images}}{{page.slug}}/image5.png)\

</div>

Finally, copy the image URI, because we are going to need it later.

### Step 4

Now that we have our docker image. Let us create our cluster and our tasks.

In the search bar, enter ECS

<div class="wide">

![Image]({{site.images}}{{page.slug}}/image6.png)\

</div>

Click on **Elastic Container Service**

On the ECS home page, on the left pane, click **Clusters**

On the Clusters page, click on **Create Cluster**

Next, on the select templates page, select the **EC2 Linux + Networking** Template

<div class="wide">

![Image]({{site.images}}{{page.slug}}/image7.png)\

</div>

Click **Next Step**

Next, on our cluster configurations page, we need to give our cluster a name.

For our instance configuration, select **On-Demand Instance** as our Provisioning Model type.

<div class="wide">

![Image]({{site.images}}{{page.slug}}/image8.png)\

</div>

Next, for our instance type, we need to select **t2.micro** because it is the free tier instance type.

For the remaining configurations under instance configurations, we leave them as default.

<div class="wide">

![Image]({{site.images}}{{page.slug}}/image9.png)\

</div>

In the Networking section, select a VPC, for subnets, select the first option.

For the **Auto-assign public IP** option, select Enabled, and finally, for security groups, select the first security group

<div class="wide">

![Image]({{site.images}}{{page.slug}}/image10.png)\

</div>

Leave every other setting as default and click on **Create**

After creating our cluster, we need to create one last thing, which is our task.

To create a new task, on the left pane of the home page of ECS click on **Task Definitions.**

Next, click **Create new Task Definition**

For our launch type, we will be selecting EC2

<div class="wide">

![Image]({{site.images}}{{page.slug}}/image11.png)\

</div>

Next, we need to give our task definition a name and leave other settings under Configure task and container definitions and Task execution IAM role section as default.

<div class="wide">

![Image]({{site.images}}{{page.slug}}/image12.png)\

</div>

Now, in our Task Size section, we need to set our container compute resource.

Since we are creating a very basic container, we can set our Task Memory to 100, and Task CPU to 1vCPU

<div class="wide">

![Image]({{site.images}}{{page.slug}}/image13.png)\

</div>

Next, in Container Definitions, we need to set some configurations for our container.

First, we need to give our container a name, and enter our image URI (this is where the image URI we copied earlier comes in).

<div class="wide">

![Image]({{site.images}}{{page.slug}}/image14.png)\

</div>

Finally, we need to configure our Port Mapping settings.

Our host port will be the port we want to expose on our EC2 instance, and our container port will be the port we are exposing in our Dockerfile.

<div class="wide">

![Image]({{site.images}}{{page.slug}}/image15.png)\

</div>

Now that we are done, click the **Add** button to add the new container definition.

After that, we leave all other settings in our Task Definition as default and click on **Create**

Now that we have a cluster and a task definition, all we have to do now is run a task in our cluster.

To do that, go back to the cluster we created, select Tasks, and click on **Run new Task**

Select EC2 as the Launch type and click on **Run Task**

<div class="wide">

![Image]({{site.images}}{{page.slug}}/image16.png)\

</div>

Our task should take some time before it starts running, but once it does, the status will change from PENDING to RUNNING

<div class="wide">

![Image]({{site.images}}{{page.slug}}/image17.png)\

</div>

### Step 5

Finally, before we can send requests to our Django app, we need to configure our server to allow us to send requests to it on the port we defined earlier.

First, we need to get to our EC2 dashboard.

In the search bar, enter **EC2**, and click on EC2.

On the resources page, click on **instances(running)**, and select the running [EC2](/blog/build-your-own-ngrok-clone) instance.

<div class="wide">

![Image]({{site.images}}{{page.slug}}/image18.png)\

</div>

Click on Security, and click on the security group

<div class="wide">

![Image]({{site.images}}{{page.slug}}/image19.png)\

</div>

While on the Security Groups page, click on **Edit inbound rules**

Now, all we need to do is add more inbound rules, one of which will consist of:

* Type: Custom TCP, Port range: 9000, Source: Anywhere-IPv4
And:
* Type: Custom TCP, Port range: 9000, Source: Anywhere-IPv6

Now, we click on **Save rules**.

We have successfully configured our server to allow internet traffic on port 9000.

All we need to do now is go back to our instance dashboard and copy our **Public IPv4 DNS**.

We can now send an HTTP request to that server. We can test this with Postman

<div class="wide">

![Image]({{site.images}}{{page.slug}}/image20.png)\

</div>

As you can see, we got a response of "{"message": "Hello World"}".

With that, we have just successfully deployed our docker container.

## Conclusion

In a nutshell, we dived into container deployment, explored various services, and checked out the perks of using AWS ECS. We even deployed a simple Docker container.

Now, if you're looking to level up your build process efficiency, you might want to try [Earthly]((https://cloud.earthly.dev/login)), especially if you're already working with Docker containers.

{% include_html cta/bottom-cta.html %}
