---
title: "Container Image Build Tools: Docker vs. Buildah vs. kaniko"
categories:
  - Tutorials
toc: true
author: Kasper Siig

internal-links:
 - Docker
 - Buildah
 - kaniko
 - Image Container
topic: docker
excerpt: |
    This article compares three popular container image build tools: Docker, Buildah, and kaniko. It explores their features, compatibility, and community support, helping readers make an informed decision about which tool is right for their needs. Whether you're new to containerization or looking for alternatives to Docker, this article provides valuable insights into the world of container image building.
last_modified_at: 2023-07-11
---
**This article explores container image tools. Earthly significantly speeds up builds with its advanced caching system while maintaining familiar container workflows. [Check it out](https://cloud.earthly.dev/login).**

When you first start learning about containerization, you're probably going to use [Docker](https://www.docker.com). Docker wasn't the first tool to introduce the world to containerization; however, it's definitely the most popular. As you familiarize yourself with Docker and containerization in general, you may begin to run into use cases where Docker isn't the ideal tool.

For instance, when you need to build your images based on [Dockerfiles](https://docs.docker.com/engine/reference/builder/), you may have cases where Docker isn't the right choice or where it can't be used. Moreover, one of the most common ways to build container images inside Kubernetes was to use what's known as [Docker-in-Docker](https://docs.gitlab.com/ee/ci/docker/using_docker_build.html). Put simply, you spin up a container, and that container is bound to the Docker socket that's on the host. This allows you to use Docker inside the container.

With the [removal of the Dockershim](https://kubernetes.io/blog/2022/02/17/dockershim-faq/) in [Kubernetes](https://kubernetes.io/), this is no longer possible, and engineers are looking to find other tools to help them build their container images.

In this article, you'll be introduced to three container image build tools: Docker, [Buildah](https://buildah.io), and [kaniko](https://github.com/GoogleContainerTools/kaniko). Tools like these can help you build your container images, getting you ready to deploy your applications to platforms like Kubernetes. You'll compare the tools based on features, supported platforms, and community; and by the end, you'll have seen the various ways that you can build container images as well as the pros and cons of each approach, which will help you make an informed decision about which tool is right for you.

## Introduction to Docker, Buildah, and kaniko

![Docker logo]({{site.images}}{{page.slug}}/iFyvSui.png)\

As previously mentioned, Docker is by far [the most popular option](https://trends.google.com/trends/explore?date=all&q=docker,kaniko,buildah) on this list and is the tool that helped containerization gain popularity. Docker was launched in 2013 in order to build images, and today, it's still widely used by many.

![kaniko logo]({{site.images}}{{page.slug}}/7lpG7g4.png)\

kaniko, released in 2018, doesn't have the longevity of Docker yet; however, it's backed by one of the biggest companies in the world: Google. Because of this, kaniko has quickly become a mature product and has been adopted by many engineers.

kaniko was primarily developed with one goal: allowing engineers to build container images inside unprivileged containers or inside Kubernetes.

![Buildah]({{site.images}}{{page.slug}}/ZzocU9y.png)\

Also released in 2018, Buildah doesn't have the same backing or focus that kaniko does. However, not having the same backing as Google doesn't mean it doesn't have a big company behind it. [Red Hat](https://www.redhat.com/en) is the company in charge of Buildah, which makes sense, as they are also the company behind [Podman](https://podman.io/). Podman is a tool that aims to solve the same use case as Docker as well as issues outside of building images. You can read more about the difference between [Podman](/blog/earthly-podman) and Docker [in this blog post](https://www.imaginarycloud.com/blog/podman-vs-docker/#:~:text=Docker%20uses%20a%20daemon%2C%20an,does%20not%20need%20the%20mediator.). Buildah primarily focuses on providing an efficient way of building container images to be [Open Container Initiative (OCI)](https://opencontainers.org/) compliant.

## Features

![Features]({{site.images}}{{page.slug}}/features.png)\

Likely the most important thing to know when you want to choose a container image build tool is its features. When it comes to container image building, the features of each tool tend to be similar; however, there are a few that can be highlighted.

### Docker

Besides having the basic feature that you'd expect of a container image build tool, namely being able to build container images, Docker also has a few other features that make it stand out. Firstly, because of its widespread adoption, you'll see that a lot of CI providers have direct integrations with the `docker build` command, like in [Azure DevOps](https://docs.microsoft.com/en-us/azure/devops/pipelines/ecosystems/containers/build-image?view=azure-devops).

Secondly, Docker as a tool allows you to run containers, whereas the other two options only allow you to build the images. This is, of course, not relevant to the specific use case of container image building, but it's worth keeping in mind that Docker is a more fully formed development tool, while the others are meant to solve a specific problem.

Besides that, not much sets [Docker](/blog/rails-with-docker) apart in terms of pros. This is not intended to make Docker sound like a poor tool choice; however, because it's the status quo, not much makes it stand out. This is more important for other tools, as they have to make a case for becoming the *new* status quo, whereas Docker mainly needs to make sure it provides existing features reliably.

### Buildah

Buildah has a very specific focus, namely being able to build container images without using a full-blown container runtime. This focus has determined its feature set, and as a bonus, you don't even need to install a daemon.

It also shares many of the same features as Docker, including being able to build OCI-compliant container images.

Buildah is perfect in cases where you either can't run as root or where you don't want to install a bloated solution like Docker, such as in a CI scenario.

Tools like [Azure DevOps](https://azure.microsoft.com/en-us/services/devops/) have built-in support for Docker builds; however, this is something you won't always find with Buildah. For [Azure](/blog/azure-functions-node) DevOps, there is a [plug-in](https://marketplace.visualstudio.com/items?itemName=cloudpup.buildah-toolkit) you can use instead, which isn't bad, per se, but you need to be aware that the industry support is lower when choosing Buildah.

### Kaniko

While you can install a plug-in in Azure DevOps to work with Buildah, there's no such luck when it comes to kaniko. Here, you have to run a custom script to work with kaniko. However, it's very easy to work within its CLI form, so this shouldn't be an issue for most.

kaniko focuses mostly on providing a container image build tool that doesn't have to have any privileges, meaning you don't need root access to run kaniko—something that is needed to work with Docker. This is very important when you want to build images inside something like Kubernetes.

## Compatibility

![Compatibility]({{site.images}}{{page.slug}}/compatibility.jpg)\
Aside from the feature set, it's important to know that the tool you choose is compatible with the other parts of your toolchain. Perhaps you're using Kubernetes, and you need to know that the containers being built can be run by [containerd](https://containerd.io/).

### Docker

Docker can be run on every major operating system, including [Windows](/blog/makefiles-on-windows), macOS, and Linux. At the time of writing this article, Linux support for Docker Desktop has just been launched, meaning you can now get a fully supported application to work with Docker on all systems with a UI.

With Docker being one of the leaders that created OCI, it's no surprise that container images built with Docker are going to be OCI compliant. Of course, Docker is also compatible with Dockerfiles. Just like with the feature set, Docker doesn't present anything special, as it's been around since the beginning of mainstream containerization.

As mentioned previously, you'll also find that Docker is compatible with pretty much any CI solution.

### Buildah

Compared to Docker, Buildah can only be installed on Linux systems. For CI or script scenarios, or for those hardcore enough to use Linux as their primary OS, this won't be an issue. However, most engineers use either Windows or macOS, in which case, you could run into issues.

However, once it's installed, it still has much of the same feature set that Docker has in terms of image building, even being able to build from Dockerfiles. However, as mentioned earlier, Buildah *only* handles the building of images, whereas Docker comes with a lot of other functionality, like being able to run the containers after the image is built.

### Kaniko

kaniko, like Buildah, is only able to run on Linux. This is partly because its focus is to run in pipelines that are run inside Kubernetes. For this reason, it makes no sense to spend time developing Windows and macOS support.

Like the other two options in this article, kaniko is also able to build OCI-compliant images, and it can do so from regular Dockerfiles. This lets kaniko be a drop-in replacement for Docker in, say, Kubernetes.

## Community

![Community]({{site.images}}{{page.slug}}/community.png)\

Far from the most important thing to consider, but nonetheless still important, is the community surrounding your tool of choice. The more experience you have, the less important this becomes, as you are more likely to figure out issues for yourself. However, as any engineer knows, you are bound to run into issues you can't figure out for yourself at some point, so a good community is something you should consider.

### Docker

The community surrounding Docker is, without a doubt, the biggest among these three tools. Whenever you run into an issue or you have a question, you can no doubt either find the answer or ask it in almost any public developer forum and get an answer quickly.

Docker isn't backed by a company; rather, Docker is a company in itself. This also means you'll get great support, as the company has one primary focus, which is this tool.

### Buildah

As mentioned previously, Buildah was first built by Red Hat and is today maintained by the [Containers](https://github.com/containers) organization. Buildah has a medium-sized community, meaning you'll likely find answers to your issues or questions. However, there will be times when you have to figure things out for yourself or wait for someone to answer.

### kaniko

kaniko was built by Google, but they mention very clearly at the top of the [GitHub repo](https://github.com/GoogleContainerTools/kaniko) that it is *not* an officially supported tool. However, it still has a great community surrounding it, and you will have a fairly easy time finding answers to your questions.

## Conclusion

As you can see, Docker, Buildah, and kaniko are great options for choosing a container image build tool. Docker is the de facto tool chosen by the industry mainly because it's been around for many more years than the two other alternatives. Buildah is great if you just want an alternative to Docker that can build from the same files and produce the same images. kaniko is likely the best choice if you want to build your images inside of Kubernetes.

No matter the tool you choose to build your images, it's important that the applications inside them get deployed properly. For this, you can check out [Earthly](https://earthly.dev/), a tool to help you create idempotent CI/CD runs.

{% include_html cta/bottom-cta.html %}
