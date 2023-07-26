---
title: "Developer Tools for Kubernetes"
categories:
  - Tutorials
toc: true
author: Kasper Siig

internal-links:
 - Kubernetes
 - CI/CD
 - IDE
 - Cluster
excerpt: |
    Learn about the essential developer tools for Kubernetes that can help you become more efficient and productive in your workload. From integrated development environments to package managers and tools for faster development, this article covers a range of tools that can simplify your Kubernetes journey.
---
**We're [Earthly](https://earthly.dev/). We simplify software building using containerization. [Check it out](/).**

When you get started on your path as a developer, you may notice from the beginning that there's an abundance of different tools to choose from. At the same time, it may not even be clear why you need to use specialized tools rather than simply using the programs natively.

To put it simply, tools are there to assist you in becoming more efficient in your workload, making sure that you aren't wasting time getting work done. On top of that, some tools may even bring more advanced capabilities to your workload, like being able to view the status of multiple different services at once.

This is especially true when you start working with Kubernetes. You will notice that there's an abundance of tools to help you in your developer journey. For example, you may find that deploying to Kubernetes can cause issues you wouldn't otherwise experience, as access control may be different than what you're used to. Or, perhaps you find that deploying using only standard Kubernetes manifests is too much of a hassle.

In this article, you'll be introduced to tools in three different categories. In terms of [Kubernetes](https://kubernetes.io) manifests, you'll be introduced to [Helm](https://helm.sh/) and [Kustomize](https://kustomize.io/). In the area of developer environments, you'll learn about the differences between [Skaffold](https://skaffold.dev/), [Tilt](https://tilt.dev/), and [Garden](https://garden.io/). Lastly, in terms of cross-language integrated development environments (IDEs), you'll be introduced to [Lens](https://k8slens.dev/) and [Gitpod](https://www.gitpod.io/). You'll learn about the strengths and weaknesses of each tool as well as what assets they provide so that you can confidently decide which tool you want to add to your workflow.

## Integrated Development Environments

Most engineers use their favorite integrated development environment (IDE) when it comes to Kubernetes, like [VSCode](https://code.visualstudio.com) or a [JetBrains](https://www.jetbrains.com) product. However, there are advantages to looking outside of what you normally use to see if you can reap any benefits from an IDE change. Following are two IDEs you should consider implementing in your Kubernetes workflow:

### Lens

<div class="wide">

![Lens]({{site.images}}{{page.slug}}/E6V8MLx.png)\

</div>

The goal of [Lens](https://k8slens.dev/) is to provide an improved IDE for modern workloads. Lens has a focus on Kubernetes specifically, giving you insight into how your cluster is working and allowing you to create new resources directly from your IDE.

Lens provides you with complete insight into your Kubernetes cluster. For many people, it can become a complete replacement for `kubectl`, because it lets you manage your cluster through a graphical user interface (GUI). For many, managing a Kubernetes cluster (or perhaps even multiple clusters) is overwhelming and a GUI helps simplify that process.

With Lens, you get an overview of all pods, deployments, and services directly in your IDE. You can even quickly switch between different Kubernetes contexts if needed. While this is far from a necessary tool in your Kubernetes toolset, it's a huge increase in quality-of-life.

There are other tool options in the market like [K9s](https://k9scli.io/), however, that's a tool designed for the terminal, and it can only show you one cluster at a time. In addition, because it runs in the terminal, it's limited by the design choices of the terminal, where Lens is able to be a more fully-fledged application.

When you first get started with Lens, it can be a bit confusing because you get overloaded with information about your cluster. However, once you start using it and figure out what you need to look at, it can quickly become an integrated part of your workflow.

### Gitpod

<div class="wide">

![GitPod]({{site.images}}{{page.slug}}/gitpod.png)\

</div>

The goal of [Gitpod](https://www.gitpod.io/) is to create developer environments based on Git repositories. This makes it easy to have your very own developer environment. Inside your Git repo you can define a `.gitpod.yaml` file, in which you can define tasks to be run when you spin up an IDE based on a branch. With this, you can easily have an IDE where `kubectl` is automatically connected to your cluster, and you can even have it deploy your application automatically so you can develop directly in your cluster, using tools like Skaffold, which is covered later in this post.

As is perhaps clear from the previous paragraph, Gitpod has no clear focus on providing you with Kubernetes functionality, however because of how dynamically it can be configured, you can set it up to help you with many different scenarios. For example, you can self-host Gitpod and make it spin up the IDE inside your Kubernetes cluster, giving you direct network access to your resources. This way, you won't have to spin up local resources, and instead you can use the actual development resources you have running in the cloud.

One of the shortcomings that you will find with Gitpod, is that you're unlikely to get your very own terminal with you. Unless you've created an install script that you can run to set everything up, you will be stuck with the terminal created by Gitpod. For many this won't be an issue, but if you're the type of engineer who's spent a lot of time configuring your terminal, this will be a pain point.

## Package Managers

![Package Managers]({{site.images}}{{page.slug}}/manager.jpg)\

Getting services deployed to Kubernetes is fairly straightforward. You just run `kubectl apply` pointing to your manifest files, and your application will quickly deploy. However, once you start getting more serious about your deployments, like wanting to have version management, or different environments, the simple `kubectl apply` command may become somewhat lackluster. Here are two tools that can help you solve this issue:

### Helm

[Helm](https://helm.sh/) is a package manager for Kubernetes. The main purpose of this tool is to provide an easier and more structured [deployment](/blog/deployment-strategies) process. Helm integrates deeply into your workflow, which may turn some off of the tool, however the complete integration provides you with some options you otherwise wouldn't have access to.

For example, with Helm you can get version management of your applications, allowing for easy rollback should anything go wrong. One of the biggest ways you'll feel the deep integration of Helm is by the way that it uses template files, with values being replaced by a `values.yaml` file. For example, the template for a [deployment](/blog/deployment-strategies) in Helm may look like this:

{% raw %}

~~~{.yaml caption="values.yaml"}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
~~~

{% endraw %}

Then in the `values.yaml` file you would write:

~~~{.yaml caption="values.yaml"}
replicaCount: 3
~~~

This is a very simple example, and in most Helm charts you change every value into either a variable that's pulled from the `values.yaml` file, or that's in some way pulled from Helm directly.

As previously mentioned, one of Helm's advantages is that it integrates completely into your workflow, however, that may also be its biggest drawback. You *have* to integrate it into your workflow. You can't just use Helm for a small part of your deployment into Kubernetes. You can build around it, but it will always be *the* way of deploying your application to Kubernetes once you start using it.

Working with Helm is fairly easy, as most of the time you won't be working with and writing the templates, but instead you'll just be using it to deploy your application. Helm is a great tool to use when you want an overarching way of deploying your applications, with a proper view into versions and configurations.

### Kustomize

[Kustomize](https://kustomize.io/) has the same goal as Helm, however it approaches it differently. While Helm focuses on providing templates that you can then build around, Kustomize focuses on building around the existing Kubernetes manifest files. The general way to use Kustomize is to create a folder called `base`, in which you write manifest files like you otherwise would, no special variables needed.

Then, you create another folder called `overlays`, in which you can create separate folders for `dev`, `staging`, `qa`, etc. In these folders you create one file called `kustomization.yaml` which will define what files provide the base for your deployment as well as what files should be used to patch the base.

As of writing, Kustomize has been built directly into `kubectl` and can be used with the `-k` flag. Deploying a "kustomized" version is as simple as executing `kubectl -k <kustomization_directory>`.

The integration into `kubectl` is a testament to how popular Kustomize is and you can be assured that you will find a great community should you run into any issues. In essence, it's a simple tool that doesn't do a whole lot, however it can provide you with great functionality in those cases where you don't want your entire workflow to change.

## Faster Development

When you start working with Kubernetes you should focus on learning Kubernetes. However, as you get more familiar with the tool, you may start to feel that certain areas can be optimized. One of the biggest areas that can be improved is that of development. Using only native Kubernetes tools, you would have to run `kubectl apply` every time you [make](/blog/makefiles-on-windows) a change to your application if you want to see how your application works inside a cluster. Following are three tools that can make your development experience better:

![Faster Development]({{site.images}}{{page.slug}}/fdevelopment.png)\

### Tilt

[Tilt](https://tilt.dev/) has a strong focus on solving the pains of microservice development. This means that it's not unique to workloads running on Kubernetes; in fact, it heavily focuses on workloads running locally, even if it's just a local Kubernetes cluster in development. This comes to life in the fact that in the Tilt UI you are getting an overview of different services, and how they're deployed.

This tool is best for you if you're working with many different services at once, for example a backend, a frontend, and a database. Or, perhaps many different parts of a webshop at once. In any case, that's what you would use Tilt for; getting an overview of all the development resources you are working with, where they're deployed, when they're deployed, logs from them, and so on.

If you're not working with many different microservices, there's a good chance Tilt isn't the right choice for you, as it only leaves you with the functionality of live reloading. (Please note, this is something the tool Skaffold accomplishes and is covered later in this post.) However, Tilt does provide a [WebUI](https://docs.tilt.dev/tutorial/3-tilt-ui.html) that you can use to view things like logs, which is something that Skaffold doesn't offer.

### Garden

The primary focus of [Garden](https://garden.io/) is to make it as easy as possible to work with your Kubernetes cluster, and especially the resources you have running in your cluster, at least when it comes to development. The tool positions itself as an "automation platform for Kubernetes development and testing".

By defining a `garden.yaml` file in the root of your projects, Garden will collect all the information from different repos into a full graph of your stack. With this, you can not only get a great overview of how your services are deployed and working together, but it also allows for developers to easily spin up a development environment in a private namespace within your cluster.

In essence, Garden helps as much with faster local development, as it does with increasing the speed of development throughout your entire organization. Like you saw with Helm and Kustomize, some tools are created for building around what you would normally do, and some are about changing the paradigm completely. Garden is one of the tools that completely wants to change the paradigm on how you deploy your services.

This is a tool you want to use if you are either just getting started with your Kubernetes cluster, or if you are looking to do a complete overhaul of your cluster deployment. It's not a tool meant for lone engineers to start using locally.

### Skaffold

[Skaffold](https://skaffold.dev/) will likely be your go-to tool if you want something that heavily specializes in the use case of local Kubernetes. You start out by defining a simple `skaffold.yaml` file in your root directory, which could look something like this:

~~~{.yaml caption="skaffold.yaml"}
apiVersion: skaffold/v2beta29
kind: Config
build:
  artifacts:
  - image: hello-world
deploy:
  kubectl:
    manifests:
      - k8s-files/*
~~~

This may look confusing, however it simply states what the image should be called, and what manifest files should be used. In this case it will use all the files in the `k8s-files` directory, and build the Dockerfile that you'll also need to have in your root directory, tagging it as `hello-world`. But, what does it use this for?

Well, once you've gotten those files created, you can run `skaffold dev`, and Skaffold will build your image, and deploy your resources based on the k8s-files directory. Then, once you make changes to your application, Skaffold will automatically redeploy your application. If you are familiar with [nodemon](https://www.npmjs.com/package/nodemon) in Node.js then it's the exact same functionality, except for Kubernetes.

Skaffold has the huge advantage that it doesn't affect your production environment or your colleagues at all. It's not something that integrates heavily into your workflow if you don't want it to. You add the `skaffold.yaml` file to your project, and then you can use it if you want. With this tool, you can test that your application runs perfectly inside a Kubernetes cluster like you would expect it to. Skaffold is great when you want something that simply compliments your development process, as well as something that's not necessarily everyone *has* to use, but everyone *can*.

## Conclusion

Kubernetes is a powerful tool that can become complicated to maintain and develop. Fortunately a robust ecosystem of tools has been popping up lately to help you with some of the heavy lifting. So whether your looking to ease some of the pains of local development, or reduce the amount of code you need to maintain, or simplify deployments and monitoring, there's bound to be a tool to help you out.

Let us know if there are any tools we missed that you love working with or that have solved a significant problem for you and your team.

Another option that you should consider when you start working with Kubernetes is [Earthly](https://earthly.dev/). It's a great tool for setting up your [CI/CD](/blog/ci-vs-cd) pipeline, and it integrates the best parts of Makefiles and Dockerfiles.

{% include_html cta/bottom-cta.html %}
