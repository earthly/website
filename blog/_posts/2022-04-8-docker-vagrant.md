---
title: "Vagrant vs. Docker: Are Virtual Machines Ever the Right Option Anymore?"
categories:
  - Tutorials
toc: true
author: Gineesh Madapparambath

internal-links:
 - vagrant
excerpt: |
    Learn about the differences between Vagrant and Docker and how they help create consistent development environments. Discover the benefits and considerations of each technology to choose the right option for your projects.
last_modified_at: 2023-07-14
---
**This article addresses the debate between Vagrant and Docker for consistent environments. Earthly optimizes the build process in conjunction with Docker. Earthly provides build optimization for Docker.**

<!-- vale HouseStyle.OxfordComma = NO -->

There's a modern trend for enterprise applications to either be containerized or deployed in virtual machines (VMs). As a result, software engineers must ensure that their local development environments closely resemble the target infrastructure to ensure that code runs smoothly in production. This in turn requires a fleet of consistent development environments to minimize dependency failures and facilitate system testing. And of course, development teams often work on multiple projects at the same time, so they need to keep operating systems and code libraries separate for each project. Developers have to be able to tear down a development environment and build another one as quickly as possible.

Thanks to an abundance of enterprise-ready open-source applications over the last decade, it's never been easier to create consistent, disposable development environments. Two technologies—[Vagrant](https://www.vagrantup.com/) and [Docker](https://www.docker.com/)—are particularly popular solutions.

For a quick comparison, Vagrant allows developers to automate spinning up VMs in local workstations from a base image, ensuring all the application-specific libraries and components are always present in the VM no matter what physical machine it's running on. Docker, on the other hand, further abstracts the hardware, operating system, and low-level libraries, creating small, lightweight containers with only the required applications and their necessary runtimes installed.

This article covers the differences between Vagrant and Docker and explains how they help create consistent development environments. You'll be able to compare their speed of provisioning, security, usability, ease of replication, and other factors that will help you choose the right technology. Let's get started with some basic introductions.

## Virtual Machines and Vagrant

A VM is identical to an entire computing environment, complete with the hardware resources (CPU, RAM, disk, networking) and an operating system. VMs comprise one or more computer files living inside a physical machine, like a server or a laptop. A special kind of software, called the [hypervisor](/blog/docker-virutal-machines) interfaces with the physical machine's hardware (or in case of Type-II hypervisors, with the operating system) and abstracts its hardware resources.

*Abstracting* simply means when the VM runs, the hypervisor presents it with a finite amount of hardware resources from the actual machine. The VM thinks it's the only machine in an isolated environment, but in reality, there may be multiple VMs running on the same physical machine—all receiving a portion of the underlying CPU, RAM, disk, and network bandwidth.

![Virtual Machines — High Level Overview]({{site.images}}{{page.slug}}/os5KcgR.png)

Using virtualization technology, it's possible to run multiple computing environments in a developer workstation, each for a different purpose. You can use the hypervisor's native GUI or CLI interface to create, start, stop, or delete virtual machines in your laptop.

However, manual operations are not scalable and can be error prone. That doesn't make it easy for you to focus on the actual development work. Vagrant is an open-source tool for creating and maintaining virtual machines and other resources in your development workstation. It uses [vagrant boxes](https://www.vagrantup.com/docs/boxes) as base images for VMs, enabling you to customize the configuration using a [Vagrantfile](https://www.vagrantup.com/docs/vagrantfile).

![Managing a VM lifecycle using Vagrant]({{site.images}}{{page.slug}}/V60VjSt.png)

Vagrant comes with support for VirtualBox and Hyper-V (and Docker) platforms. When building Vagrant environments in other platforms (like AWS, GCP, VMWare, etc.), you can use [provider plugins](https://www.vagrantup.com/docs/providers). These plugins take care of the communication with the platform, and the Vagrantfile provisions the VM. Once the VM is created, your [Vagrant provisioners](https://www.vagrantup.com/docs/provisioning) will do the post-provisioning configuration, install packages, and so on.

Managing development VMs with Vagrant is very useful when you need a specific operating system, and a different OS edition or version for development and testing. It also helps with testing under different system resource capacity.

However, there are some caveats to be aware of:

- Spinning up virtual machines will take time, even when it's automated.
- Vagrant boxes are larger than containers and will need more space on your system.
- Depending on the physical machine's capacity, there may be only a few VMs you can create for your development needs.
- There is no automated way to create networking connections between your VMs. This can be a problem in a multi-node development environment.

## Containers and Docker

Containers provide virtualization at the operating system level (remember that VMs virtualize hardware resources) and allow you to run multiple applications in isolated environments on a single machine. This machine can be a VM or a physical node. The VM can run on an on-premise physical server, a workstation, or it can be a cloud-hosted instance. Each container is bundled with the minimum libraries and dependencies to run the application.

Unlike VMs, containers aren't concerned with hardware abstraction—the container runtime abstracts the resources. A [Dockerfile](https://docs.docker.com/engine/reference/builder/) specifies the application's installation and configuration details. This is a simple text file, used to create *images* (ie, a binary version of the container). The container runtime can download the image from an image repository like [Docker Hub](https://www.docker.com/products/docker-hub) and instantiate the container from it. The container can run on any operating system, as long as there's a Docker runtime installed there.

This makes containers lightweight, portable, and allows the same container image to work on any other machine without dependency issues.

![Docker Containers — High Level Overview]({{site.images}}{{page.slug}}/0VaXggs.png)

Docker is a software collection that runs and manages containerized applications. Each Docker container can either run in isolation from others or in a networked configuration. Docker containers are easy to spin up, which makes your development workflow simple and traceable. You can also have multi-container applications using [Docker Compose](https://docs.docker.com/compose).

However, this involves configuring inter-container networking, service access, ports, and more.

There are some great benefits of using Dockerized application containers. For example:

- Dockerfiles, their associated images and the containers are lightweight and portable.
- Containers use fewer resources than VMs.
- Building and deploying containers takes less time than deploying VMs.
- A physical host can run many more containers than virtual machines.

## Comparing Vagrant and Docker

Technologically, Docker and Vagrant aren't be mutually exclusive. There are strong and weak points for both, and it depends on which feature is more important for your current use case. In fact, depending on your development environment, you might use both.

![Virtual Machines Managed by Vagrant vs. Containers Managed by Docker]({{site.images}}{{page.slug}}/zuFI9gO.png)

Still, let's take a look at some feature comparisons.

### Resource Utilization

Containers are very lightweight compared to VMs. Running Docker allows you to run many containers in the same workstation with a smaller hardware resource consumption. Each container accesses the same CPU or memory of the underlying machine, although their internal processes are isolated from accessing those directly.

Compared to that, each VM created by Vagrant consumes a specific number of CPUs, a certain amount of RAM, and a portion of the disk space. VMs can consume chunks of disk space depending on their operating system or how much data they're saving internally.

### Supported Operating Systems

[Vagrant is available](https://www.vagrantup.com/downloads) for most workstations and sever operating systems such as macOS, Windows, and various flavors of Linux.

Compared to that, Docker was mainly developed for Linux. It is used heavily on macOs and Windows but in that case it is running inside a Linux-based VM.

### Configuration Changes

Once the [Vagrantfile](https://www.vagrantup.com/docs/vagrantfile) is created as infrastructure as code (IaC), it's easy to manage the VMs using Vagrant. You need only a few commands to spin up, halt, or destroy the VMs. However, any changes to the VM's base functionality means you have to recreate the image from scratch, which can be time-consuming.

Dockerfiles, on the other hand, are easy to change—all you need to do is destroy the existing container, rebuild the image, and use that new image. The steps take a lot less time than recreating a VM image and spinning up VMs from it.

### Build Speed

You only need a single command to spin up VMs using Vagrant. However, it will take some time to create the VM and disks.

~~~{.bash caption=">_"}
$ time vagrant init bento/ubuntu-18.04
A `Vagrantfile` has been placed in this directory. You are now
ready to `vagrant up` your first virtual environment! Please read
the comments in the Vagrantfile as well as documentation on
`vagrantup.com` for more information on using Vagrant.
vagrant init bento/ubuntu-18.04  1.41s user 0.24s system 98% cpu 1.679 total

$ time vagrant up        
Bringing machine 'default' up with 'virtualbox' provider...
==> default: Importing base box 'hashicorp/bionic64'....
.
.
.
==> default: Mounting shared folders...
    default: /vagrant => /Users/gini/workarea/newvm
vagrant up  6.53s user 2.38s system 21% cpu 40.645 total
~~~

Stopping or destroying virtual machines is also easy.

~~~{.bash caption=">_"}
$ vagrant halt          # stops the vagrant machine(s)
$ vagrant destroy       # stops and deletes vagrant machine(s)
~~~

Since the Docker containers are lightweight and simple, starting and stopping containers will take only a fraction of the time. This can be very helpful when time is of the essence and you want to quickly test your updated code inside a new container.

You can see the time taken to create an NGINX Docker container from an existing image.

~~~{.bash caption=">_"}
$ time sudo docker run --name mynginx1 -p 80:80 -d nginx
~~~

~~~{.bash .merge-code caption="Output"}
ec2c5e520fff0ef93fd9f432ef625f496886ac4ceceb7066708902f0f007b535

real    0m0.966s
user    0m0.032s
sys     0m0.014s
~~~

~~~{.bash caption=">_"}
$ curl localhost:80
~~~

~~~{.html .merge-code caption="Output"}
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
.
.
.
<p><em>Thank you for using nginx.</em></p>
</body>
</html>
~~~

### Security

By default, VMs managed by Vagrant are only accessible from the localhost. Vagrant creates and uses random SSH key pairs for accessing the machines from the command prompt. There are some weak points though. For example, the default user is `vagrant`, and anyone with access to the workstation console can access the VM.

In comparison, security in network-hosted virtual machines is stronger, because there are network ACLs involved. There are three security layers, which involve the host operating system (these are typically more secure than a desktop OS), the hypervisor, and the guest OS.

Docker containers are lightweight and less isolated than virtual machines. This is because containers use the same kernel and libraries as the underlying operating system, whereas in VMs, the applications can see the guest OS only.

Also, the Docker daemon runs as the root user, which means it has maximum access to everything in the underlying operating system. A malicious process or user breaking into the container could gain access to the host system with root privileges—not ideal from a security perspective. As a Dockerfile developer, you need to tighten less-secure configurations before moving the application from a development environment to production.

### Portability

Both Vagrant and Docker let you create portable environments. You can copy identical Vagrant environments to the same or different hosts using the Vagrantfile. However, you still need to address some things (like IP addresses, hostnames, and shared volumes) if you plan to scale the VMs.

Docker containers are easy to port or scale with a few additional commands, which makes it more flexible.

## Conclusion

Being resource-heavy, virtual machines are hard to deploy and use. Docker containers, on the other hand, fit very well in a fully automated development workflow.

It's a developer's choice to use Vagrant, Docker, or any other tool to create the development environment. Just make sure you consider factors like speed, efficiency, security and integration options.

[Earthly](https://earthly.dev), an open-source application, can help create artifacts or Docker images to speed up the build and deployment of your containerized applications. It can [run on top of popular CI tools](https://docs.earthly.dev/docs/examples) such as Jenkins, GitHub Actions, and CircleCI

To see how it works, check out the sample [GitHub Action workflow](https://docs.earthly.dev/ci-integration/vendor-specific-guides/gh-actions-integration) that uses Earthly.

{% include_html cta/bottom-cta.html %}