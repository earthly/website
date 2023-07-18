---
title: "Terraform and Kubernetes for Deploying Complex Applications"
categories:
  - Tutorials
toc: true
author: James Konik
internal-links:
 - terraform
excerpt: |
    Learn how to automate the deployment process and manage complex applications using Terraform and Kubernetes. Discover the benefits of scalability, portability, and workload support that these tools offer, and how they can complement each other to streamline your infrastructure management.
---
**We're [Earthly](https://earthly.dev/). We simplify and speed up software builds using containerization. Working with complex deployments like Terraform and Kubernetes? Earthly can help. [Check it out](/).**

As projects increase in complexity, so do the benefits of using tools to automate parts of the deployment process. Scaling your infrastructure and deploying to multiple platforms and locations can become unmanageable without the right workflows in place.

Fortunately, help is available in the form of the increasing selection of tools and platforms, like [Kubernetes](https://kubernetes.io/) and [Terraform](https://www.terraform.io/), that are geared toward solving such problems.

[Kubernetes](https://kubernetes.io/) is an [open source](https://github.com/kubernetes/kubernetes) tool that helps you manage (or orchestrate) containers. Though often [associated](https://kubernetes.io/blog/2020/12/02/dont-panic-kubernetes-and-docker/) with [Docker](https://www.docker.com/), it can be used with any containerization solution.

[Terraform](https://www.terraform.io/) is an [open source](https://github.com/hashicorp/terraform) infrastructure management system. You can use it to make versionable declarations of your infrastructure and keep it as closely monitored as your regular codebase.

If you work with containers, using a tool designed to automate their workflows will save you vast amounts of time. Batch deployments and administration tasks can be done quickly and repeatedly. Taking control of your infrastructure also has huge benefits and prevents it from becoming chaotic.

In this article, you'll learn about what Kubernetes and Terraform can do for you, and how they complement each other. The tools will be compared on scalability, portability, and their ability to support specific workloads.

## Scalability

Provisioning infrastructure often involves minor edits to configuration files—doing small tweaks here and adjusting software versions there—and something that begins simply can soon become complex.

Many of the changes required can get lost. If you don't document the procedure, you can end up with an unstable edifice dependent on a secret sauce that everyone has forgotten they made. That's a big problem when you want to repeat the process—something that becomes more common as you scale up.

Terraform's whole philosophy is geared toward scaling. With its [four phases of adoption](https://www.hashicorp.com/resources/terraform-adoption-journey), it takes you through stages you are likely to encounter as you grow.

With Terraform, your infrastructure adjustment becomes self-documenting and repeatable. Your changes are tracked and can be tuned and repeated as needed. You can also see who made which adjustments, allowing you to ask them why if you need additional information.

It uses declarative files in [HashiCorp Configuration Language (HCL)](https://github.com/hashicorp/hcl) but can also work with other languages.

Like Terraform, Kubernetes is highly scalable and is designed specifically to manage groups of containerized applications. It groups containers into pods, allowing them to be managed simultaneously. At larger scales, [pods are grouped into nodes](https://kubernetes.io/docs/concepts/architecture/nodes/), which could be either a physical or virtual machine.

Kubernetes has some [specific limitations](https://kubernetes.io/docs/setup/best-practices/cluster-large/) in terms of how many pods, nodes, and clusters it can handle. The 300,000 total container limit is an important one for large-scale deployments, like cloud service providers.

Kubernetes is supported by most major cloud providers. In Amazon's case, there's a specific tool, [Amazon Elastic Kubernetes Service (EKS)](https://aws.amazon.com/eks/), which allows you to scale on demand.

### Scaling Workloads

Kubernetes includes autoscaling at [both pod and node level](https://enterprisersproject.com/article/2021/3/kubernetes-autoscaling-explanation).

It uses [horizontal pod autoscaling](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/) to scale pods as required. Users can [set the metrics that control this](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/) via its resource metrics API. It can also be [configured via environment variables](https://kubernetes.io/blog/2016/07/autoscaling-in-kubernetes/).

You can also scale by [changing the number of replicas](https://kubernetes.io/docs/tutorials/kubernetes-basics/scale/scale-intro/) in a deployment.

In contrast, there are different ways to handle scaling with Terraform. It could be farmed out to a service provider. For instance, you can [create an Auto Scaling group](https://blog.gruntwork.io/an-introduction-to-terraform-f17df9c6d180#4c88) in AWS to automatically create and adjust a group of EC2 instances, along with a load balancer, allowing you to present a single IP address to the user. In AWS, you have a choice of [load balancers](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/load-balancer-types.html). You could use an Application Load Balancer (ALB) for HTTP traffic or a Network Load Balancer (NLB) for TCP and [UDP traffic](https://aws.amazon.com/blogs/aws/new-udp-load-balancing-for-network-load-balancer/).

Another way to approach scaling with Terraform is to manage your repos and make sure you [divide responsibility between chunks of code](https://www.hashicorp.com/resources/terraform-workflow-best-practices-at-scale). For example, you need a single repo to handle your network.

### Achieving Scalability

Using both tools means you can scale your infrastructure and applications together. If you have Terraform deploying your Kubernetes nodes to a major cloud provider, you can deliver [applications to a worldwide audience](https://www.doit-intl.com/global-scale-scientific-cloud-computing-with-kubernetes-and-terraform-1-2/).

There are many guides available for [using the tools together](https://shipa.io/development/deploying-microservice-apps-on-kubernetes-using-terraform/). Once you understand the process, it's possible to [deploy very quickly](https://medium.zenika.com/a-custom-kubernetes-cluster-on-gcp-in-7-minutes-with-terraform-and-ansible-75875f89309e).

## Portability

Encapsulation is an inherent benefit of working with Kubernetes because you're already using containerization and avoiding all the problems that go hand in hand with deployment.

Kubernetes's [plug-in architecture](https://ritza.co/articles/kubernetes-vs-docker-vs-openshift-vs-ecs-vs-jenkins-vs-terraform/) means it can readily adapt to other technologies, and its virtualized environments offer a high degree of portability.

Terraform uses providers to interface with data sources, such as APIs and other services. Some of these are provided by [HashiCorp](https://www.hashicorp.com), while others are from a third party or the community. These provide a great degree of flexibility and make it easy to swap between data sources.

It also [uses modules](https://innablr.com.au/blog/why-terraform-and-what-problem-it-solves/) that let you reuse code for specific resources. These make it relatively painless to move identical infrastructure elsewhere.

### Having Support for Tools

Terraform supports all kinds of services, with many plug-ins available. You can use it with its own configuration language or via its CLI. However, you don't have to learn HCL. The [Cloud Development Kit for Terraform (CDKTF)](https://www.terraform.io/cdktf) works with [TypeScript](https://www.typescriptlang.org), [Python](https://www.python.org), [Java](https://www.java.com/en/), [C#](https://docs.microsoft.com/en-us/dotnet/csharp/), and [Go](https://go.dev).

There are [dedicated tutorials](https://learn.hashicorp.com/collections/terraform/aws-get-started) for using it with major services, including [AWS](https://aws.amazon.com), [Azure](https://azure.microsoft.com/en-us/), [Docker](https://www.docker.com), [Google Cloud Platform (GCP)](https://cloud.google.com/gcp), and [Oracle Cloud Infrastructure (OCI)](https://www.oracle.com/cloud/).

Cloud providers offer their own out-of-the-box [Kubernetes services](https://www.aquasec.com/cloud-native-academy/kubernetes-101/kubernetes-as-a-service/). These include [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine), [Amazon EKS](https://aws.amazon.com/eks/), and [Azure Kubernetes Service (AKS)](https://azure.microsoft.com/en-us/services/kubernetes-service/).

Kubernetes works with many different technologies, and its documentation gives guidance on a few specific ones, including [WordPress](https://kubernetes.io/docs/tutorials/stateful-application/mysql-wordpress-persistent-volume/) and [Cassandra](https://kubernetes.io/docs/tutorials/stateful-application/cassandra/).

### Moving a Workload to a New Provider or Platform

Terraform provides templates that let you easily get started with each platform. How much of your existing templates can carry straight over will depend on the specifics of what you're doing.

Terraform's workflow is [divided into two parts](https://www.hashicorp.com/resources/enabling-multi-cloud-with-hashicorp-terraform): [`terraform plan`](https://www.terraform.io/cli/commands/plan) defines what is provisioned, and [`terraform apply`](https://www.terraform.io/cli/commands/apply) actually provisions the infrastructure.

With Kubernetes, it's easy to switch cloud providers. In fact, that kind of portability is [one of its advantages](https://cast.ai/blog/10-best-practices-to-make-switching-cloud-providers-less-painful/). It's supported by all major cloud providers, and containers can be deployed on them relatively easily.

### Achieving Portability

Using Kubernetes to run your applications in containers and then using Terraform to provision the infrastructure let you build a workflow that can be carried over to run on other platforms.

Terraform can be used as part of a [multi-cloud architecture](https://www.containiq.com/post/working-with-terraform-and-kubernetes) strategy.

### Deploying Portable Terraform Scripts Provisioning Kubernetes Clusters

Terraform can deploy to all kinds of cloud services as well as users' own servers. If you want to move to another platform, its encapsulation makes that much easier. Things may not run out of the box, but it should be straightforward to identify what needs to change.

## Workloads

Kubernetes is built around containers, which are stored in pods. The containers are typically [containerd](https://containerd.io/), but Kubernetes can use anything compatible with its [Container Runtime Interface (CRI)](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-node/container-runtime-interface.md).

In contrast, Terraform isn't bound to any specific tool. It uses resources that are generated from providers. There are currently almost 2,000 of these [listed in its documentation](https://registry.terraform.io/browse/providers).

These providers let you create resources on a wide range of platforms, including all the major cloud services, like AWS, Azure, and Google Cloud. Kubernetes is included, too, demonstrating how readily these tools work together.

There are around 200 verified entries, with the rest provided by the community. Of course, you're free to create your own if what you need isn't listed.

### Migrating a Workload from One Tool To the Other

Kubernetes's and Terraform's workloads are distinct, and they don't run the same workloads. However, you can use them together by utilizing each to set up complementary parts of your system. The infrastructure provisioned by Terraform is then used to run your containerized applications deployed with Kubernetes.

Combining the two gives you access to a wide range of platform combinations.

### Knowing the Limitations to What These Tools Can Handle

Because both tools are open source, your engineers have a wide scope for adjusting them to work with the workloads of your choice. Naturally, Terraform is an infrastructure provisioning tool, and Kubernetes is for containers, but beyond that, the sky's the limit.

### Using These Tools Together to Run a Workload

With Terraform used to provision infrastructure and Kubernetes used to manage pods of containers, you can handle both infrastructure and the specifics of your deployment together. In this scenario, you get the benefit of both worlds.

There are plenty of guides to show you how to do this, including [the article "Use Kubernetes and Terraform together for cluster management"](https://www.techtarget.com/searchitoperations/tutorial/Use-Kubernetes-and-Terraform-together-for-cluster-management) from [Tech Target](https://www.techtarget.com/).

## Conclusion

Terraform and Kubernetes efficiently handle different areas: Terraform manages infrastructure, while Kubernetes deploys containers. As your infrastructure diversifies, for example running multiple Kubernetes setups, Terraform's automation becomes increasingly beneficial. Both platforms can significantly enhance productivity individually, even more so when used together. 

Looking to simplify your build process even further? Give [Earthly](https://www.earthly.dev/) a try. This tool can be a great addition to your tech stack, complementing the capabilities of Terraform and Kubernetes by providing a streamlined and efficient build process.

{% include_html cta/bottom-cta.html %}
