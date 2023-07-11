---
title: "Comparing Local Kubernetes Development Solutions"
categories:
  - Tutorials
toc: true
author: Kasper Siig
internal-links:
 - minikube
 - K3s
 - kubeadm
 - Docker Desktop
 - MicroK8s
 - Kubernetes Development
excerpt: |
    Looking to develop applications locally using Kubernetes? Check out this article comparing the top local Kubernetes development solutions, including minikube, kind, K3s, kubeadm, Docker Desktop, and MicroK8s. Learn about their platform support, setup complexity, flexibility, and community support to help you choose the best option for your needs.
---

Once you've determined that you want to use [Kubernetes](https://kubernetes.io) as your base for developing applications locally, it's time to figure out which development solution is the best. There are many different options out there, but a few select reign over the others as the most common, including [minikube](https://minikube.sigs.k8s.io/docs/), [kind](https://kind.sigs.k8s.io/), [K3s](https://k3s.io/), [kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/), [Docker Desktop](https://docs.docker.com/desktop/kubernetes/), and [MicroK8s](https://microk8s.io/).

In this article, you'll take a more in-depth look at these six tools, and by the end, you should have an easier time picking out the one that works best for you. These options will be compared based on what platforms they support, what the complexity of the setup is, how flexible they are, and what kind of support they provide.

## Why You Need a Local Kubernetes Development Solution

Before comparing the tools themselves, it's important to understand why you want a local Kubernetes development solution in the first place. There are many reasons for wanting a local Kubernetes cluster, like being able to test the [deployment](/blog/deployment-strategies) method you're using, checking how your application interacts with mounted volumes, and testing manifest files. In addition, all these reasons help you avoid the situation where something works on one machine and doesn't on others.

Now, it's no longer enough to spin up your own service and test it; you need to make sure it works properly together with other services, and you need to make sure they properly communicate when deployed to a Kubernetes cluster. This is why today, it's more important than ever to have the possibility of a local Kubernetes cluster.

## Overview of Each Tool

### Minikube

![minikube logo]({{site.images}}{{page.slug}}/E51VHlu.png)\

For a long time, minikube was by far the [most popular](https://trends.google.com/trends/explore?date=all&q=minikube,docker%20desktop,k3s,kubeadm,microk8s) option for local Kubernetes development. Providing a simple CLI tool to start and interact with a Kubernetes cluster was a great option for most engineers to get a simple cluster working. On top of that, it's possible to select different [drivers](https://minikube.sigs.k8s.io/docs/drivers/) so you can choose for yourself whether you want a container or VM-based cluster.

### Kind

![Kind logo]({{site.images}}{{page.slug}}/9eE2wL1.png)\

kind was primarily developed with the intention of being able to test Kubernetes, but it's also useful when you want to test applications running inside Kubernetes, and it is based on containers as nodes.

### K3s

![K3s logo]({{site.images}}{{page.slug}}/NfeQXkM.png)\

K3s is the first project on this list that can proudly state that it's a [Cloud Native Computing Foundation (CNCF) sandbox project](https://www.cncf.io/sandbox-projects/) focusing on providing a Kubernetes cluster with a smaller footprint. K3s is suited well for IoT and ARM processing, and it's also helpful when you want to run a Kubernetes cluster locally.

### Kubeadm

![Kubeadm logo]({{site.images}}{{page.slug}}/gikIAq7.png)\

Due to its complexity, kubeadm isn't the most popular option for engineers when setting up a local Kubernetes cluster. However, since kubeadm can help you better understand the configuration of your cluster, it's a viable solution in some cases. For the most part, it's used when engineers want to run Kubernetes on-premise.

### Docker Desktop

![Docker Desktop logo]({{site.images}}{{page.slug}}/kJMf8ZB.png)\

In recent years, Docker Desktop has taken over minikube in terms of [popularity](https://trends.google.com/trends/explore?date=all&q=minikube,docker%20desktop,k3s,kubeadm,microk8s). Looking at the trend chart, it's important to remember that Docker Desktop, of course, also offers regular [Docker](https://www.docker.com/), which will skew the popularity a bit. However, it's fair to say that being able to run Kubernetes using the already-installed tool has made many choose this option.

### MicroK8s

![MicroK8s logo]({{site.images}}{{page.slug}}/kbvMYid.png)\

Developed by [Canonical](https://canonical.com/), the same company that's behind the widely popular Linux distribution [Ubuntu](https://ubuntu.com/), MicroK8s is the only one on this list that can be considered a proper product. The other options are either CNCF projects or [Kubernetes Special Interest Groups (SIGs)](https://github.com/kubernetes/community/blob/master/README.md#special-interest-groups-sig). MicroK8s offers enterprise support as one of its main selling points.

## What Platforms Are Supported

The most important thing to look into when deciding on a local Kubernetes solution is what platforms it supports. If you're using Windows as your host system, there's no point in looking at a tool that only supports Linux. You also need to understand whether the tool runs natively on the host, in containers, in VMs, or in a completely different way.

In addition, it's important to understand whether you're getting a full-blown Kubernetes version on a small scale or if you're getting a modified version. And it's important to understand the performance implications of the tool you're choosing.

To understand how performant these solutions are, the [Online Boutique](https://github.com/GoogleCloudPlatform/microservices-demo.git), a cloud-native microservices demo app by Google, will be deployed on each solution and timed. Remember that this is purely an indication of performance, with a sample size of one. This is also the reason why deploy times won't be presented in precise measurements.

### Minikube

minikube has support for all three major operating systems: Windows, macOS, and Linux. This means you likely don't have to worry if you plan on rolling out minikube organization-wide since pretty much any PC is able to run it. On top of that, you also get great platform support in terms of *how* minikube should be run, given that it supports many different [drivers](https://minikube.sigs.k8s.io/docs/drivers/), like Docker, [kvm2](https://minikube.sigs.k8s.io/docs/drivers/kvm2/), and [VirtualBox](https://www.virtualbox.org).

With minikube, you're getting pretty close to running inside a full Kubernetes cluster. You'll still feel like you're running a local cluster at times, but more on that later.

In terms of performance, minikube does fairly well, spinning up the [microservice demo](https://github.com/GoogleCloudPlatform/microservices-demo.git) in just a few minutes.

### Kind

Like minikube, kind supports all three major platforms. It works by spinning up Docker containers to act as nodes in your cluster, which are based on an image [created by kind](https://kind.sigs.k8s.io/docs/user/quick-start/#creating-a-cluster). However, if you want to use your own image, that's also possible using the `--image` flag.

Because the image is developed by kind themselves, there may be variations compared to what you find in [Azure](/blog/azure-functions-node) Kubernetes Service (AKS) or Google Kubernetes Engine (GKE), but in the end, it's a solution that conforms to Kubernetes conventions, so you should be able to run all your regular workloads using kind. You'll also get great performance, which is evident with the [microservice demo](https://github.com/GoogleCloudPlatform/microservices-demo.git) deploying in just about a minute and a half.

### K3s

K3s is the first tool on this list that only supports running on Linux due to the fact that K3s isn't actually made to *be* a development solution. Rather, it was developed as a low-resource alternative to Kubernetes (hence the name K3s, which is a play on the abbreviation K8s).

This means that you don't install K3s as a tool with `brew` or `choco`, rather you install it as a [Linux service](https://www.hostinger.com/tutorials/manage-and-list-services-in-linux/#:~:text=Managing%20Linux%20Services-,Linux%20Services,operation%20of%20the%20operating%20system.). Again, this is a testament to the fact that K3s isn't supposed to be a local development tool but rather something to use in production. This does mean that performance is great, with the [microservice demo](https://github.com/GoogleCloudPlatform/microservices-demo.git) being deployed in just about a minute.

### Kubeadm

kubeadm is another option that only runs on Linux; however, you can make it run on all Linux-based servers from Ubuntu to [Raspberry Pi](https://www.raspberrypi.org).

kubeadm isn't just a tool that lets you run local Kubernetes clusters. It was developed to help spin up Kubernetes clusters in general. This means you can find a good amount of infrastructure engineers using kubeadm to administrate clusters in production.

Because of this, kubeadm is the closest you will get to a production-like cluster. You can customize every single part of Kubernetes to exactly what you need, and because of this, you'll get some of the greatest performance, with the [microservice demo](https://github.com/GoogleCloudPlatform/microservices-demo.git) deployed in just under a minute.

### Docker Desktop

Docker Desktop is supported by all the major operating systems (macOS, Windows, and Linux). Today, this is the tool you're most likely to use since most engineers will already have Docker Desktop installed.

Docker Desktop runs Kubernetes by spinning up a single node in a Docker container. The biggest drawback of using it is that you can *only* get a single-node cluster; however, for most, this isn't an issue.

In terms of performance, Docker Desktop performs well, deploying the [microservice demo](https://github.com/GoogleCloudPlatform/microservices-demo.git) in about a minute.

### MicroK8s

MicroK8s again supports the three main operating systems, and you will find easy-to-follow installation instructions on [their website](https://microk8s.io/#install-microk8s). Once installed, you'll see that this is a tool that's made for development, and you'll be heavily using the CLI. Even when running simple `kubectl` commands, you need to prefix it with `microk8s`.

The main reason to choose MicroK8s is that it comes with any of the features you would normally use in a Kubernetes installation, even allowing you to enable a registry to use. Performance is okay but not amazing, with the [microservice demo](https://github.com/GoogleCloudPlatform/microservices-demo.git) deploying in a few minutes.

## Complexity of Setup

![Complexity general image]({{site.images}}{{page.slug}}/complexity.jpg)\

Once you know what platforms each tool supports and you've made sure that it matches the platform and environment you have, you also need to look into how complex the setup is. If the tool has everything you need it to have but it's too complex to set up, then it's no longer the right choice for you. Or perhaps you're looking for something to implement organization-wide; in which case, the complexity of the setup may be one of the most important factors.

### Minikube

Getting started with minikube is incredibly easy. On Linux and macOS, it's as simple as running `brew install minikube`, and on Windows, you run `choco install minikube`. Once the package manager is finished, minikube will be successfully installed. At this point, you just need to run `minikube start` to create a local Kubernetes cluster.

From here, you can start to deploy applications like you would in Kubernetes. The one thing to be aware of is that some functionality has to be added on with the [minikube CLI](https://minikube.sigs.k8s.io/docs/commands/). For example, adding an Nginx Ingress Controller is done via `minikube addons enable ingress`.

### Kind

Getting kind is incredibly simple on Linux and macOS. All you need to do is run `brew install kind`. On Windows, it's also simple, but you need to download a [binary](https://github.com/kubernetes-sigs/kind/releases).

Once you've got it installed, you can create a cluster by running `kind create cluster`. For use cases like [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/), you need to specify some custom configuration, which is done by [passing a YAML file](https://kind.sigs.k8s.io/docs/user/ingress/#create-cluster) to the `--config` flag when creating the cluster. This is a less elegant solution than using a CLI command to enable Ingress, but it allows you to customize your cluster completely.

### K3s

The first thing you need when you want to use K3s is a Linux environment. As stated previously, K3s only works with Linux. If you're already using Linux, there's no simple `brew` command to install it; rather, you need to use the script that you'll find on the [homepage](https://k3s.io/) of the tool: `curl -sfL https://get.k3s.io | sh -`.

Once the installation is done, you can run `kubectl` commands by prepending them with `k3s`. For example, to get all pods, you need to run `k3s kubectl get pods --all-namespaces`.

### Kubeadm

Getting kubeadm set up is the [most involved process](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/) for any of the tools in this article. Quite frankly, this is not the tool you want to use if you just want a local Kubernetes cluster to test on. However, it is the tool you want to use when you're looking to learn more about Kubernetes or if you have a very specific use case.

You should expect to be troubleshooting when setting up a cluster with kubeadm. But when you get it set up, it's the truest to production you'll get.

### Docker Desktop

Docker Desktop is fairly easy and follows the installation principles of the OS you're using. In Ubuntu, it's a `.deb` package; in Windows, it's an `.exe` file; and on macOS, it's a `.dmg` file. From there, it's an easy process if you're familiar with installing regular programs.

Once Docker Desktop is installed, you need to go into the settings and enable Kubernetes, and from there, it's just a matter of waiting a few minutes for Kubernetes to be enabled, and then you're ready to go. You don't need to enable anything else like Ingress to make it work.

### MicroK8s

The setup for MicroK8s is incredibly simple and utilizes the `snap` functionality in Ubuntu. Run `sudo snap install microk8s --classic`, and after a minute or so, you will have MicroK8s installed. From here, you can enable whatever services you want by running `microk8s enable`. For example, you can enable the Kubernetes dashboard by running `microk8s enable dashboard`.

## Flexibility

![Flexibility general image]({{site.images}}{{page.slug}}/Flexibility.jpg)\

When developing a tool, you can be extremely opinionated, not opinionated at all, or somewhere in the middle. If you're new to the space, it may be good to use an opinionated tool that can make decisions for you, but in some cases, it may be better to choose a tool that is incredibly flexible so you can make it conform to what you need. A portion of flexibility is also about how close you can get to something resembling what you're running in production.

### Minikube

minikube isn't very opinionated and mostly lets you handle your Kubernetes cluster the way you want, even giving you the ability to have multiple nodes. You're also able to configure Kubernetes itself by using the `--extra-config` flag.

minikube is made to be a development tool, which you'll notice when you have to use the minikube CLI quite often. However, once resources have been deployed in the cluster, they behave just like you would expect them to in Kubernetes. You're not likely to run into many use cases that can't be handled in minikube.

### Kind

The impression given by kind is that it's not opinionated at all. This is a tool that gives you all the flexibility you want, as long as you know how to use it. It doesn't offer any helpful CLI commands to enable features, opting to use a YAML file instead.

This may turn some away from using the tool, but others will see the benefits of getting a local cluster that acts exactly like what you get in production. You're only limited by your own knowledge. This also means that you should be able to use kind no matter what your use case is.

### K3s

K3s is a tool that's fairly opinionated, given that it serves a very specific use case: running in low-resource environments, like on the edge or in IoT. This means that under the hood, K3s is a modified version of Kubernetes.

It's possible to customize K3s but with limitations. Looking at the page for [advanced options](https://rancher.com/docs/k3s/latest/en/advanced/), you'll see that K3s offers specific instructions for specific scenarios. In most cases, you'll find that K3s behave like a normal Kubernetes cluster in production, but you may find that it doesn't do everything, like if you have made custom configurations to your production Kubernetes cluster.

### Kubeadm

The least opinionated option on this list is kubeadm. It lets you configure every single thing inside a Kubernetes cluster. As mentioned, this will also mean you'll get as close to a production cluster as you can possibly get.

Everything can be configured to make sure it behaves just like your production cluster, and you will likely never run into anything you cannot do, as long as it's supported by Kubernetes.

### Docker Desktop

Docker Desktop is very opinionated when it comes to Kubernetes or at least as opinionated as you can get with Kubernetes. For most use cases, you won't feel a difference between using Docker Desktop and a cloud provider; however, in the cases where you would normally make some special configurations to Kubernetes, you're out of luck. Docker Desktop doesn't allow you to customize Kubernetes in any way.

This means that you'll likely get a cluster that looks like what you're used to in production, as long as your use cases aren't advanced.

### MicroK8s

MicroK8s is also a fairly opinionated tool, not allowing you to configure anything directly in the Kubernetes configuration; rather, you have to do it through the [instructions that they provide](https://microk8s.io/docs/configuring-services).

If you have some advanced use cases, it's likely that you won't be able to run them in MicroK8s.

## Support

![Support general image]({{site.images}}{{page.slug}}/support.png)\

The last point to consider when choosing a tool is: Does the tool have a strong community to answer questions, or does it perhaps have a company that's backing the project and providing support, or are you left to your own troubleshooting and skills? The newer you are to the field, the more important this is to consider.

### Minikube

minikube is a [Kubernetes SIGs project](https://github.com/kubernetes/community/blob/master/README.md#special-interest-groups-sig), meaning that there's a group of people behind this project working on it out of pure interest, as compared to being supported by a company that's interested in making a profit.

It's very likely that whenever you run into an issue, you're going to find an answer. And if you don't, you'll likely be able to ask the question yourself and get an answer quickly.

### Kind

Just like minikube, kind is a Kubernetes SIGs project, meaning devoted people are behind the tool with the goal of providing a tool that's as useful as possible.

When you run into issues, you're likely to find the answer somewhere in the existing documentation or somewhere where another engineer has already asked the question. The community is great and supportive, so no matter your experience level, it should be safe to use kind.

### K3s

K3s is backed by [Rancher](https://rancher.com/), which is one of the biggest companies in terms of delivering Kubernetes-as-a-service. This means that not only do they put great resources toward developing their documentation, but they also have years of experience running Kubernetes professionally as an offering, which can be a great advantage when having to offer support.

On top of that, you'll also find a great community surrounding the product, so it's very likely you're going to find answers to your questions.

### Kubeadm

kubeadm is the official offering of Kubernetes, so you get the full force of the Kubernetes community when you use it. This means you get help from people who know exactly how Kubernetes works in the most inner parts.

Besides the official support channels, you're most likely to find answers in [GitHub issues](https://github.com/kubernetes/kubeadm/issues), as there isn't any [Slack](https://slack.com/) or other forums specifically for kubeadm. Typically, it's bundled into the same forums as Kubernetes in general.

### Docker Desktop

Docker Desktop is by far the most [popular](https://trends.google.com/trends/explore?date=all&q=minikube,docker%20desktop,k3s,kubeadm,microk8s) tool of choice when comparing the tools in this article. However, Docker Desktop, as the name suggests, isn't just about Kubernetes. It's about Docker in general. So it's tough to say exactly how popular the Kubernetes offering inside Docker Desktop is; however, when looking through forums and blog posts, it's fair to say that the community is fairly large.

Chances are that you'll find an answer to most of your questions when working with Docker Desktop.

### MicroK8s

Since MicroK8s is developed by Canonical, they provide an enterprise version of it, and you'll find that their documentation is well-written. They also have articles that can answer a lot of your questions.

If you're not able to find the answer to your question in the existing documentation, you will have to rely on communities, like [Stack Overflow](https://stackoverflow.com), as there's no official MicroK8s community.

## Conclusion

If you're looking for something that is as close to your production cluster as possible, then you will likely have to go with kubeadm or even K3s, if you're running K3s in production. If your goal is to just have an easy cluster to test with, Docker Desktop or minikube will likely be the best choice.

No matter what option you choose for developing your applications locally, you'll have to deploy mthe platform into production. For this, check out [Earthly](https://earthly.dev/), a framework to help you effortlessly deploy your services.

{% include_html cta/bottom-cta.html %}
