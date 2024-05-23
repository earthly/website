---
title: "LXC vs Docker: Which Container Platform Is Right for You?"
toc: true
author: Eric Kahuha

internal-links:
 - lxc
 - lxd
 - chroot
topic: docker
excerpt: |
    Are you confused about whether to use LXC or Docker for your containerization needs? This article compares the two container platforms in terms of host machine utilization, simplicity, speed, security, ease of use, scalability, and tooling. Whether you're a developer looking for simplicity or a system administrator in need of control, this article will help you make an informed decision.
last_modified_at: 2023-07-11
categories:
  - Cloud
---
**This article compares LXC and Docker. Earthly enhances Docker by streamlining the container build process with advanced caching and parallelization. [Check it out](https://cloud.earthly.dev/login).**

[Linux Containers](https://linuxcontainers.org/) (LXC) is an OS-level virtualization technology that enables you to create and run multiple Linux operating systems (OS) simultaneously on a single Linux machine (LXC host). LXC provides a set of tools to manage your container as well as templates to create a virtual environment of [the most common Linux OS](https://uk.lxd.images.canonical.com/).

[Docker](https://docs.docker.com/get-started/overview/) is an open-source containerization technology that focuses on running a single application in an isolated environment. Its [Docker Engine](https://docs.docker.com/engine/) enables you to create, run, or distribute containers. You can also share applications and collaborate with other developers using [Docker Hub](https://hub.docker.com/).

While LXC and Docker have much in common in terms of their architecture and usage, they also differ in many ways. This article will compare their host machine utilization, simplicity, speed, security, ease of use, scalability, and tooling. We'll also discuss the best traits of these tools as well as their downsides.

## Comparing LXC vs Docker

Let's get started by taking a closer look at each of the comparison criteria areas outlined above and exploring how LXC and Docker function under each category.

### Host Machine Utilization

Both LXC and Docker containers communicate with the kernel of the host machine. So what, you may ask?

Sharing the kernel of the host system is what defines a container—you can find this definition all over the internet. The reason is that container technologies attempt to offer a better alternative to [Virtual Machines](https://www.atlassian.com/continuous-delivery/microservices/containers-vs-vms#:~:text=The%20key%20differentiator%20between%20containers,above%20the%20operating%20system%20level.). As a result, the prevalent definition is the one that is the most relevant to differentiating virtual machines (VMs) from virtual environments (VEs, otherwise known as container technologies).

<div class="wide">
![VM vs VE]({{site.images}}{{page.slug}}/EUXeGou.png)
</div>

How these virtualization technologies (VM or VE) differ is in how they use the host machine. But in order to compare two container technologies (VEs)—LXD and Docker—we'll need to dig a little deeper than that first definition.

In Linux, memory is divided between the [kernel space](http://www.linfo.org/kernel_space.html), reserved for the core of the operating system in charge of managing CPU, memory, and devices, and the [user space](http://www.linfo.org/user_space.html).

Saying that LXC shares the kernel of its host does not convey the whole picture. In fact, LXC containers are using Linux kernel features to create isolated processes and file systems.

<div class="wide">
![Kernel space vs user space]({{site.images}}{{page.slug}}/B2Qvs65.png)
</div>

Let's take a look at a couple of examples. In Linux, you can use the `ps` command to list the running processes. If you are running things in LXC and run `ps` from the host, you will see a list of running processes, including your container (yes, containers are first and foremost processes from the host point of view). However, if you run the same `ps` command from the LXC container, you will only see the processes started inside the container. LXC leverages [kernel namespaces](https://www.nginx.com/blog/what-are-namespaces-cgroups-how-do-they-work/) to achieve this feature.

Similarly, on your Linux host machine, you have `/bin`, the standard root directory for the executables. In the container's user space, you have another `/bin`. The container's user space is bundled inside of the container, and can be shipped to a different host. This user space isolation is the reason you can have an Alpine Linux container on a Ubuntu host machine, as programs in Linux containers are isolated from the rest of the system. LXC leverages [`chroot`](https://en.wikipedia.org/wiki/Chroot) to achieve this feature.

Docker used LXC, [prior to version 1.0](https://www.infoq.com/news/2014/03/docker_0_9/#:~:text=LXC%20itself%20recently%20announced%20the,%2C%20Solaris%2C%20OpenSolaris%20and%20illumos.), to create isolation from the host system. Later, Docker developed its own replacement for LXC called [`libcontainer`](https://github.com/opencontainers/runc/tree/master/libcontainer). This is why Docker and LXC have so much in common.

In terms of host utilization, Docker differs from LXC in two additional ways:

- It offers an abstraction for machine-specific settings, such as [networking](/blog/docker-networking), [storage](/blog/docker-volumes), [logging](/blog/understanding-docker-logging-and-log-files), etc. These are part of the Docker Engine and make Docker containers are more portable, as they rely less on the underlying physical machine.
- Docker containers are made to run a single process per container.

<div class="wide">
![Docker vs LXC]({{site.images}}{{page.slug}}/GqtGCm4.png)
</div>

### Simplicity

Linux containers (LXC) are more flexible in design. They are bit closer to virtual machines – you can configure and install anything with LXC the same way you would with VMs. Kernel features like `chroot`, `cgroups`, and `namespaces` can be leveraged to create an LXC virtual environment. These kernel mechanisms help control resource usage and the visibility that processes have on the rest of the system.

As we mentioned before, Docker containers were originally forked from the LXC project. However, the difference is in the design: Docker containers were designed specifically for microservices applications. That makes them very different from VMs. Docker is simple for developers to use; the [networking](/blog/docker-networking), [storage](/blog/docker-volumes), and [logging](/blog/understanding-docker-logging-and-log-files) abstraction make it so that devs need little (or no) prior Linux knowledge.

The simplicity that Docker offers to developers is what made it so popular. Both platforms are simple to use, but target different audiences.

### Speed

LXC boasts fast boot times when compared to a virtual machine – it doesn't need to package an entire OS and a complete machine setup with network interfaces, virtual processors, and a hard drive.

Docker containers are also lightweight, which contributes significantly to their speed. Docker adds an additional layer to abstract storage and networking, but you should not see significant performance issues caused by that in most cases. Creating and running a Docker container takes seconds. Because Docker can run on an existing OS that is already initialized, you can boot a container from its image almost instantly.

Docker supports [layered containers](https://www.flockport.com/guides/understanding-layers) by default. This means that the resulting container is the sequential combination of changes made to the file system, similar to a Git history. Layers can be downloaded in parallel, which can give you a speed advantage when starting many containerised applications in several machines simultaneously.

One point that goes in Docker's favor is the trend is to create [`distroless`](https://github.com/GoogleContainerTools/distroless) Docker images. With distroless, you have the bare minimum—just your application, compiled code, and the necessary binding. LXC images aim to replicate Linux distributions, such as Ubuntu, Debian, or Alpine. The fact that Docker aims to package single applications might give you the upper hand when provisioning hundreds of containers.

The performance difference between LXC and Docker is almost insignificant. Both provide fast boot times. Downloading an LXC image might be slower than distroless Docker images, but not all Docker images are distroless, giving Docker room for improvement as compared to LXC.

### Security

LXC is enriched with security configurations such as group policies and a default AppArmor profile to protect the host from accidentally misusing privileges inside the container.

Docker separates the operating system from the services running on it to ensure secure workloads, but the fact that Docker runs as root can increase exposure to malware. This is because the Docker daemon—which manages Docker objects like networks, containers, images, and volumes, and attends to Docker API requests—also runs as root on the host machine. Developers commonly audit Docker installations to identify potential vulnerabilities.

LXC places security at the forefront. It gives you security features, including Linux capability support, to help you keep control of your container environment and the hosted apps. Docker's approach of keeping the different application components in separate containers is a plus. But this strategy also has its own security downsides if you're hosting complicated applications that may require the attention of an experienced security engineer.

### Ease of Use

Getting started with LXC is easy; it requires installing LXC's recent versions compatible with your Linux distribution. This makes LXC commands, templates, and `python3 binding` available to create containers. Furthermore, LXC runs a standard operating system unit for each container, which means your apps are hosted in a standard Linux OS. In that way, migrating to LXC containers from bare metal or virtual machine servers is more manageable than moving to Docker containers.

On the other hand, Docker makes it easy to work with containers and run programs. With Docker, you can package containers and ship them for use on other machines. You can use the `docker build` command to build images from a Dockerfile. As an open-source container platform, getting started with Docker is straightforward. All you need is an OS that supports containers natively, like Linux, Docker for Mac/Windows, or VirtualBox, installed on your computer.

Both LXC and Docker are easy to use and provide documentation and guides to help you create and deploy containers. Their support for libraries and bindings for languages like Java and Python is a plus for developers.

### Scalability

LXC is less scalable compared to Docker. Its images are not as lightweight as those of Docker. However, LXC images are more lightweight than those of physical machines or virtual machines. That makes it ideal for on-demand provisioning and autoscaling. Also, the fact that you can use LXC to implement lightweight virtual machines without a hypervisor makes Linux containers a scalable option.

With Docker, you can break out the functionality of applications into individual containers. You can, for instance, run your Oracle database in one container while running your Cassandra server and ASP.NET app in other separate containers. You can then link these three containers together and create an application, allowing for the independent scaling of components.

### Tooling

LXC tooling allows you to run several commands, enabling you to manage tasks such as creating, launching, and deleting LXC containers. This tooling also allows you to reuse automation scripts that you may have utilized on VM or bare metal running on VirtualBox or other virtualized production environments. With such a portability feature, it is seamless to migrate applications from a traditional Linux server to a Linux container.

The Docker command-line interface (CLI) is the heart of Docker tooling. It gives you control over your containers, allowing you to list and manage images. You can also use the Docker registry to access and distribute images for frequently used applications.

Both LXC and Docker tooling provide essential functionalities for a greater developer experience. However, each tool has a tooling feature that makes it stand out. LXC tooling excels in migrating apps from a traditional Linux server to a Linux container. But if you want to prioritize developer experience, go for Docker.

## Linux Containers

Now, let's take a closer look at some of the specifics for each platform, and summarize the key insight for each, starting with LXC.

While LXC is not a full-fledged virtual machine, it provides operating-system-level virtualization via a virtual environment, which contains its own userspace and processes. Linux containers depend on the functionality of the Linux kernel to isolate containers. The host CPU divides memory allocations into namespaces to control RAM and CPU usage.

The fact that LXC bundles only the required application/OS means an improvement on the performance of the bare metal. The LXC virtual environment allows you to create containers containing a Linux distribution and your applications. In this case, all the containers share the underlying kernel and hardware resources.

Some of LXC's best traits include the following:

- LXC excels in running multiple Linux distributions on a single server.
- LXC gives you a lot of control over the features it is based on (namespace, cgroup, chroot, etc). For the more technical audience, such as system administrators, this is a great advantage.
- LXC lets you control a virtual environment easily, while increasing app portability and easing their distribution inside containers.

Furthermore, using Linux containers is particularly appropriate for several scenarios, including:

- Making test upgrades and changes to a suite of applications in a simple way. You can create a clone in seconds, roll it out when satisfied with the changes, and delete the original instance.
- Launching new instances quickly and running multiple versions of web stacks and applications. You can, for instance, experiment specific versions of Python or Ruby for a particular app before upgrading.

## Docker

Docker was designed to improve application portability. They wanted to ensure that the entire programming team worked on the same test environment and configurations as the production environment. This ability to share and use applications, all while avoiding the classic developer "it works on my machine" complaint, is the crucial element of Docker's success.

Docker invented a descriptive format, `Dockerfile`, to make the creation of containers very simple and maintainable. Each instruction in the Dockerfile creates a layer versioning the changes made to the container image.

Some of Docker's best traits include the following:

- Docker includes an abstraction layer for storage, networking, and logging that makes Docker containers easy to configure and use at scale.
- Docker offers cross-platform support. Although it was primarily developed as a Linux-only technology, Docker containers can now run on Windows and Mac, thanks to [Docker Desktop](https://www.docker.com/products/docker-desktop). Windows containers using Windows kernel is also an option.
- Docker container images are composed of layers. This offers better performance (caching and parallel downloading) and a versioning system.

However, using Docker also involves some challenges. Consider a few of its downsides:

- Docker containers are not designed to replace Linux machines. Some workloads, such as stateful applications, may not benefit from Docker features.
- Docker doesn't give the low level control available in LXC. For some this may be a downside.

## Wrapping Up

Both LXC and Docker are effective container technologies, and the choice between them depends on your needs.

LXC, is a serious contender to virtual machines. So, if you are developing a Linux application or working with servers, and need a real Linux environment, LXC should be your go-to.

Docker is a complete solution to distribute applications and is particularly loved by developers. Docker solved the local developer configuration tantrum and became a key component in the CI/CD pipeline because it provides isolation between the workload and reproducible environment.

In the same way that Docker extended the features of LXC to make it easy to package applications and make operating them more developer-friendly, [Earthly](https://cloud.earthly.dev/login) built on top of Dockerfile to create tools better suited to manage the CI/CD workload. Be sure to check it out to help automate and simplify your development pipeline using either Docker or LXC.

{% include_html cta/bottom-cta.html %}
