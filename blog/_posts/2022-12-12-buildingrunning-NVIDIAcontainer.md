---
title: "Building and Running an NVIDIA Container"
categories:
  - Tutorials
toc: true
author: James Walker
editor: Bala Priya C

internal-links:
 - NVIDIA
 - Container
 - Docker
excerpt: |
    Learn how to build and run NVIDIA containers with GPU access using the NVIDIA Container Runtime. This tutorial explains the architecture of the runtime, installation steps, and how to configure GPU access in Docker containers.
---
<!--sgpt-->**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. This article is about building and running an NVIDIA container. Earthly is a powerful build tool that can be used in conjunction with Dockerfiles to streamline the containerization process. [Check us out](/).**

[NVIDIA Container Runtime](https://github.com/NVIDIA/nvidia-container-runtime) allows containerized applications to access your host's GPU hardware. It facilitates the containerization of systems that would otherwise be off-limits, such as artificial intelligence (AI) and machine learning (ML) workloads. With NVIDIA [Container](/blog/docker-slim) Runtime installed, you can run these apps in containers on *any* host with an NVIDIA GPU.

In this article, you'll learn about the runtime's architecture and how to set it up. You'll also learn how to deploy your own containers with GPU access, broadening the scope of what you can successfully containerize.

## What Is NVIDIA Container Runtime?

NVIDIA Container Runtime is part of the [NVIDIA Container Toolkit](https://gitlab.com/nvidia/container-toolkit/container-toolkit). This set of packages provides a fully supported mechanism for accessing GPU hardware from applications running in containers.

The toolkit works by wrapping the host's standard container runtime with an interface to the NVIDIA driver running on the host. [Docker](https://www.docker.com/) bundles [containerd](https://containerd.io) as its runtime, but this lacks awareness of the GPU hardware.

Installing the NVIDIA Container Toolkit provides a shim around containerd—or any other runtime—that handles GPU provisioning. Container creations that require GPUs should be handled by the NVIDIA runtime. It'll inspect the GPUs to be used and call the [`libnvidia-container` library](https://github.com/NVIDIA/libnvidia-container) to attach them to the container. After configuring GPU access, the NVIDIA system invokes the regular container runtime to continue the rest of the startup process.

You need to use the NVIDIA Container Runtime whenever you containerize an application that's dependent on NVIDIA GPU features. AI and ML workloads are two good containerization candidates that rely on GPUs; but there are many other GPU-accelerated workloads that exist as well, including data analysis and engineering simulations. The NVIDIA Container Runtime simplifies the deployment of these complex apps by packaging them into containers that are portable across different machines.

## Installing NVIDIA Container Runtime

![Installing NVIDIA Container Runtime]({{site.images}}{{page.slug}}/6OQmOUd.png)\

Successfully using NVIDIA GPUs in your container is a three-step process:

1. Install the NVIDIA Container Runtime components.
2. Correctly configure the container image.
3. Start the container with GPU access enabled.

Before you install the runtime, make sure your system satisfies the following prerequisites:

- **Docker is installed and working**. Follow the instructions [in the Docker documentation](https://docs.docker.com/engine/install) if you don't already have Docker installed. The `docker run hello-world` should be running, and `Hello from Docker` should be shown in the response. The runtime also supports [Podman](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#podman) and stand-alone [containerd](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#containerd) installations; however, these aren't the focus of this article.
- **NVIDIA drivers are correctly installed on the host**. Drivers are available to download [from the NVIDIA website](https://www.nvidia.com/en-gb/drivers/unix) if needed.
- **A Debian-based system with the `apt` package manager is needed**. NVIDIA also supports [Amazon Linux](https://aws.amazon.com/amazon-linux-2), [SUSE Linux Enterprise Server (SLES)](https://www.suse.com/products/server/), [CentOS](https://www.centos.org), and [Red Hat Enterprise Linux. (RHEL)](https://www.redhat.com/en/technologies/linux-platforms/enterprise-linux). Installation instructions can be found in the [NVIDIA Container Toolkit documentation](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#installation-guide).

To install NVIDIA Container Runtime, start by making sure that the drivers are detecting the hardware by running the `nvidia-smi` command on the host:

~~~
+