---
title: "Kubernetes vs. Docker for Local Development"
categories:
  - Tutorials
sidebar:
  nav: "docker"
toc: true
author: Damaso Sanoja
excerpt: |
    Learn the key similarities and differences between Docker and Kubernetes for local development and discover which tool is better suited for your use case. Find out how Docker's versatility and ease of use compare to Kubernetes' built-in container orchestration and unmatched flexibility.
last_modified_at: 2023-07-14
---
**This article addresses the Docker versus Kubernetes debate. Earthly streamlines containerization workflows for both Docker and Kubernetes. Learn more about Earthly.**

You may be wondering, given that [Docker](https://www.docker.com/) is a containerization platform and [Kubernetes](https://kubernetes.io/) is a containerization platform orchestrator, how can the two be compared? Aren't they supposed to play different roles?

This article will explore a use case where such a comparison is quite relevant: local development: is it better to use the Docker runtime or Kubernetes to manage your local container development environment?

Read on to learn the key similarities and differences between these two tools and understand how each of their strengths and weaknesses translates to a local development environment.

## What Is Containerization?

Let's start with the basics. You can think of containerization as a type of operating system virtualization in which applications run packaged with all the necessary components, configurations, and libraries in a user space abstracted from the host OS, called a "container". Since containers are a fully functional and portable computing environment that shares the host OS kernel, applications packaged in containers can be easily moved, independent of the underlying infrastructure.

While the portability of containerized apps and cloud-friendly microservices is one of their main benefits, this is far from the only problem they solve. Consider some of the additional benefits of containerization:

- **Lightweight:** Containers sharing resources with the host OS translates into less overhead and, thus, lower costs than VMs.
- **Isolated:** An incredible advantage of containers is that if one fails, it does not affect the rest. This is crucial for microservice-based applications since it allows specific containers to be repaired, thus minimizing application downtime.
- **More efficient workflow:** The flexibility of the containers makes them easy to set up regardless of the OS. This facilitates the workflow of developers and, therefore, allows faster delivery of applications.
- **Easy to manage:** Thanks to container orchestration solutions, such as Kubernetes, managing and scaling containerized applications and services are relatively simple.

## How Will the Tools Be Compared?

Comparing Docker versus Kubernetes is not a simple task. In order to do so, the following aspects have been taken into account.

1. **Handling of multi-container and single-container deployments:** The current trend of developing cloud-native applications makes orchestrating multiple containers at the same time critical. In this regard, it is worth asking how efficient each tool is for working in single-container and multi-container environments.
2. **Build options:** What options does each tool offer in terms of application [deployment](/blog/deployment-strategies)?
3. **Testing capability:** Keeping technical debt under control makes it essential to consider how hard it is to implement testing on each platform.
4. **Supported tools:** Efficient application development depends on using the right tools for each use case. How varied is the ecosystem of tools for each solution?
5. **Simplicity:** How easy is it to set up, use, and debug apps in each tool?
6. **Support:** How big is the community behind each solution? What kind of support is available?

## Using Docker for Local Development

From a local development perspective, Docker is considered one of the most versatile tools available today. And it's no wonder—Docker provides a wealth of benefits. Here are just a few of its appealing characteristics:

- **Straightforward local installation:** [Getting Docker](https://docs.docker.com/get-docker/) running on your local machine is easy. On Windows or macOS workstations, you only need to install the corresponding binary (Docker Desktop for Windows or Docker Desktop for Mac) and Docker and the included VM will start up when your machine does. As far as Linux is concerned, Docker provides `.deb` and `.rpm` packages for all major architectures.
- **Outstanding portability:** Since Docker is a containerization platform, it stands out for being environment agnostic. In other words, if the application runs on your local machine, it runs anywhere.
- **Widely adopted:** Docker is not the only container runtime available on the market. There are also other container engines, such as [`containerd`](https://containerd.io/), [`rkt`](https://github.com/rkt/rkt), and [`LXC`](https://linuxcontainers.org/). However, among developers, Docker is arguably the most widely used platform for building and deploying apps. Proof of this is its massive repository of container images, [Docker Hub](https://hub.docker.com/), which had [more than 318 billion total pulls by 2020](https://www.docker.com/blog/docker-index-shows-continued-massive-developer-adoption-and-activity-to-build-and-share-apps-with-docker/).
- **Fantastic community:** With over 200 meetups worldwide, the [Docker Community](https://www.docker.com/docker-community) is undoubtedly one of the most vibrant (and best organized) in the industry. In fact, the [Docker Open Source Program](https://www.docker.com/community/open-source/application) provides an incredible amount of resources for noncommercial users, while [Docker Pro](https://www.docker.com/products/pro) is an alternative for professional developers looking to take full advantage of the platform's benefits.
- **Automated container image builds:** Among Docker's greatest benefits for local development is its ability to configure Docker Hub to perform [automated container image builds](https://docs.docker.com/docker-hub/builds/) when you push code to GitHub or Bitbucket. Moreover, you can also run automated tests before the image is published to the registry.

Despite all these benefits, Docker is a tool focused on building, running, and managing containers, and it is rarely used as is in production environments. While, technically, you can use [Docker Compose](https://docs.docker.com/compose/) and [Swarm mode](https://docs.docker.com/engine/swarm/) to manage multiple containers on different nodes, as will be discussed further below, container orchestration tools, like Kubernetes, are better suited for large-scale production deployments.

This explains why most Docker tools focus on optimizing their strengths. That is the case of [Dockerize](https://github.com/jwilder/dockerize), an application that aims to simplify the packaging of applications in Docker containers. On the other hand, tools like [`Portainer`](https://www.portainer.io) seek to provide a friendly GUI to Docker to facilitate the visualization, administration, and access to the most relevant information of Docker containers and images.

## Using Kubernetes for Local Development

In the previous section, you saw that while Docker is considered the most widely used containerization platform today, it is rarely used to orchestrate containers in production. Proof of this is exemplified by figures, such as those provided by [Sysdig](https://sysdig.com/), which show [Kubernetes with a 75% market share](https://www.statista.com/statistics/1224681/container-orchestration-usage-share-worldwide-by-platform/), while Docker Compose only has a 4.8% adoption rate. Here are some of the main reasons for this remarkable difference:

- **Built-in container orchestration:** Unlike Docker, which relies on [Docker Compose](/blog/youre-using-docker-compose-wrong) and Swarm mode to manage multiple containers, Kubernetes is built from the ground up as a platform for container orchestration. This gives it a huge advantage in terms of security, scalability, and stability, as it was intended from the start for enterprise-grade deployments.
- **Production-like environment:** When deploying Kubernetes locally, you can choose between using convenient, lightweight environments, such as [minikube](https://minikube.sigs.k8s.io/), [K3S](https://k3s.io/), or even [Docker Desktop](https://docs.docker.com/desktop/); or taking the time to do a manual installation for a more production-like environment. This flexibility allows you to overcome the inherent limitations of out-of-the-box solutions in terms of networking, nodes, scalability, add-ons, and more.
- **Unsurpassed flexibility:** While the Docker ecosystem revolves around the [Docker Engine](https://docs.docker.com/engine/), Kubernetes has the advantage of being compatible with all types of infrastructures using any type of container runtime. Moreover, this portability allows Kubernetes to manage applications and services running in a single cloud or across multiple clouds more easily than Docker. In other words, Kubernetes can be customized for almost any use case.

While Kubernetes arguably outperforms Docker as a large-scale container orchestration tool, ironically, Kubernetes is not as easy to set up as Docker for local development. As discussed, solutions, like minikube, are limited, so this often forces you to manually install Kubernetes, which is no trivial task.

On the other hand, the enormous versatility of Kubernetes could also be considered a disadvantage in terms of local configuration. One example is the need to configure a dedicated CNI (Container Network Interface) during deployment.

The same can be said for testing tools, monitoring tools, and tools that facilitate local Kubernetes development. Regarding the latter, tools like [Garden](https://garden.io) or [Skaffold](https://skaffold.dev) can be really useful in leveraging Docker's and Kubernetes's strengths. Both tools can speed up development, testing, and [CI/CD](/blog/ci-vs-cd) workflows, as they can detect changes in your source code and automatically build/push/deploy to the cluster.

For example, once configured, with a simple command, you can work on the application code, or even change its configuration and dependencies, knowing that such changes will redeploy pods as needed.

The image below shows a Node.js application driven by Skaffold:

<div class="wide">
![Skaffold Node.js Sample App]({{site.images}}{{page.slug}}/RfRGjY5.png)
</div>

On the other hand, this image shows an example of a [Gatsby](https://www.gatsbyjs.com/) website deployed in Kubernetes wherein the source code changes are monitored by Garden:

<div class="wide">
![Gatsby App Monitored by Garden]({{site.images}}{{page.slug}}/OUNaPmL.png)
</div>

## Conclusion

Having explored the main strengths and weaknesses of Docker and Kubernetes for local development, it is worth asking which is better. As is often the case, it will depend on the use case.

If you are a software developer, your workflow will likely be more closely tied to the Docker ecosystem. However, the rapid adoption of cloud-native apps often leads to running and testing applications on Kubernetes to ensure that all features are functioning as expected.

Regardless of your tool of choice, [Earthly](https://earthly.dev/) can help you optimize your deployment process. This is possible because Earthly allows you to automate your Docker builds in a unique and innovative way, making them better and more repeatable.

{% include_html cta/bottom-cta.html %}