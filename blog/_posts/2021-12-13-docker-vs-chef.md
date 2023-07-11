---
title: "Chef vs. Docker for Builds and Deployments"
categories:
  - Tutorials
toc: true
author: Keanan Koppenhaver
sidebar:
  nav: "docker"
internal-links:
 - chef
excerpt: Learn the differences between Chef and Docker and how they can be used together in build and deployment pipelines. Discover the strengths of each tool and how they can enhance your infrastructure provisioning and containerization processes.
---
[Docker](https://www.docker.com) and [Chef](https://www.chef.io) are two popular tools in the development world and are used extensively in build and deployment pipelines. However, even though they are used in similar contexts, the two are very different tools.

Chef is a configuration management tool that allows developers to specify how they'd like their infrastructure to be set up through a configuration file. This provides an advantage over traditional methods of provisioning infrastructure because the configuration file can be version controlled and shared easily across teams.

On the other hand, Docker is a tool for containerizing applications. This means packaging an application's code with all its dependencies and other pieces needed for running and deploying the package as one container. With Docker, there's less of a focus on provisioning individual infrastructure pieces and instead it focuses on including everything in a single container which can be deployed as one unit.

Chef can be used to configure infrastructure that Docker containers will eventually run on, and Docker containers can't run without the servers that Chef may have provisioned.

The difference between the two lies in the way they approach the build and deploy pipeline.

In this article, you'll take a deeper look at each tool and learn how to use them effectively.

## Build Process of Chef and Docker

If you run a build with Chef, you have build steps to provision the necessary infrastructure. Then you'll pull in your code from version control, along with installing any packages necessary. Once you run through these steps, you have a "successful deployment" using Chef.

With Docker, you'll likely be deploying an entire container to already-provisioned infrastructure, either an infrastructure you have created or a container system on a cloud provider like AWS.

Since all your scripts and code are pre-installed as part of the Docker container, once you have it up and running on your infrastructure, you have a successful Docker deployment.

If you want to use these tools in tandem, you might let Chef handle your infrastructure provisioning, while Docker handles getting your code and the necessary dependencies on your newly-provisioned infrastructure.

Whether you use them together or separately -- Chef and Docker are both powerful tools to have in your build and deployment toolbox.

## Chef

Chef at its core is a configuration management tool that allows the development or operations team to provision infrastructure through a configuration file, sometimes known as "infrastructure as code". The tool has a central server where all configuration changes are pushed. Once these configuration changes are live on the Chef server, they are then pushed out to the Chef nodes, which is the infrastructure that a user is actually able to provision.

![Chef Homepage]({{site.images}}{{page.slug}}/8XmRSW2.png)\

### Where Chef Excels

Chef makes it easy to deploy the exact same change across many different nodes without having to update each of those nodes manually.

In the past, if you wanted to install a new package on all your servers, you would need to log in to each server, install the package, check that it was installed properly, and then move on to the next server. If your application ran across hundreds of servers, that could be days or weeks of work. And that's without counting the possibility for manual error like missing a server or having one misconfigured.

With Chef, once a configuration change is pushed to the server, it's automatically rolled out to all the nodes that you have configured. This becomes useful in a deployment context because you can deploy new infrastructure across many nodes, and can deploy code changes in an automated manner which allows for a "push once, deploy everywhere" approach.

When you compare Chef and Docker, Chef really excels in the case of infrastructure that has already been provisioned and needs to be updated. For example, if you have one hundred servers that your application is already running on that need updates, each of these servers could be set up as Chef nodes and configured to receive changes from Chef without having to be destroyed and re-provisioned. With Docker, it might make more sense to spin up new containers or virtual machines each time.

### Chef Architecture

This difference in implementation is largely because of the difference between Docker containers and the client/server model that Chef uses. With Docker, each container is pulled down onto its server directly, this pull is triggered by whoever is running the deployment. However, with Chef, there is a central Chef server that is running the deployments and that all clients (or nodes) must connect to. If the server is down, Chef won't be able to run any deployments.

This is very similar to the architecture of another DevOps tool, Kubernetes. Chef nodes and Kubernetes nodes both receive instruction from a central server, which helps them know what state they should be in, what software they should have installed, and how they should process requests. If you're familiar with Kubernetes, using Chef will feel similar.

## Docker

Docker, on the other hand, is a containerization paradigm. That means that instead of making changes to existing infrastructure to match a configuration file, Docker will create a new container image that contains all the necessary code, software packages, and anything else needed to get your code up and running. This container is then deployed to your choice of infrastructure, which can be anything from traditional servers, if they're Docker compatible, or something like [Amazon Elastic Container Service](https://aws.amazon.com/ecs/).

![Docker Homepage]({{site.images}}{{page.slug}}/NgLyXRZ.png)\

### Where Docker Excels

Because of Docker's containerization paradigm, if you want to run a deployment, you need to build a new container and then pull the latest container into your existing infrastructure, stop the old container, and start the new one. This is often accomplished through a [blue/green deployment](/blog/deployment-strategies) scheme.

Chef can more easily make changes to existing servers and configurations. However, one of the benefits of Docker, and services like [ECS](/blog/how-to-setup-and-use-amazons-elastic-container-registry) that make deploying to Docker easy, is its scalability. Chef is best suited to projects that have relatively static infrastructure.

Because Docker is a more recent innovation compared to Chef, many of the abilities that Docker gives you are suited to the needs of modern applications with constantly shifting infrastructure. However, if your needs are more of a hybrid, you can use Docker and Chef together to make your infrastructure work for you in the easiest, most flexible way.

## Chef and Docker Together

As discussed Chef and Docker can both be used for building and deploying code since they have slightly different uses. When you combine the two and use Chef to maintain your infrastructure and deliver your Docker containers with all the code and software necessary to run your application, you have an incredibly powerful combination.

If you're not currently using either of these tools, it's recommended to only adopt one at a time, but, if you're already using one, you might find it helpful to add the other and let them work together.

By using each of these tools for what they're good at—Chef for managing infrastructure and Docker for straightforward, atomic deployments of entire containers—you can make your deployment workflow more sophisticated and stable at the same time.

In this scenario, you will have your build process create a new Docker container with all your latest code changes and publish it to the registry. Chef would then take over, handle connecting to all your latest infrastructure, and ensure that the newly-built Docker container is deployed to all the servers that need it. Chef would also make sure the old container is stopped, and the new container is started through a [blue/green deployment scheme](/blog/deployment-strategies).

And if you're looking for a tool to manage your build pipeline as it gets more complex, consider [Earthly](https://earthly.dev/). It's a syntax for defining your build and works with your existing build system (even if it's not Docker and Chef) to support you as you move into adopting new tools into your pipeline.

## Conclusion

Chef and Docker, while originally conceived for different purposes, are both used in build and deployment pipelines to get the code for applications on the internet into production. While many companies only utilize one or the other, they work very well together, especially when paired with a tool like [Earthly](https://earthly.dev/).

Earthly helps simplify your build syntax, so you can use Docker and Chef to construct a robust build and deploy pipeline that will take your DevOps team to the next level.

{% include_html cta/bottom-cta.html %}
