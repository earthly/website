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
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 470.141.03   Driver Version: 470.141.03   CUDA Version: 11.4     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  NVIDIA GeForce ... Off  | 00000000:01:00.0  On |                  N/A |
| 41%   73C    P0    70W / 250W |   1267MiB / 11175MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
~~~

This machine has detected a single GPU using the driver version 470.141.03 and Compute Unified Device Architecture (CUDA) 11.4.

### Adding NVIDIA's Package Repository

Run the following command to add the `nvidia-docker` package repository to the system. It registers the repository's GPG key and inserts it into the sources list:

~~~{.bash caption=">_"}
$ distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
   && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey \
   | sudo apt-key add - \
   && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
~~~

Then run `apt update` to update the package lists and discover the NVIDIA container packages:

~~~{.bash caption=">_"}
$ sudo apt update
~~~

### Installing the Package

Use the following command to add the complete NVIDIA Container Toolkit to the system:

~~~{.bash caption=">_"}
$ sudo apt install -y nvidia-docker2
~~~

The installation process is fully automated. Once it's finished, open the `/etc/docker/daemon.json` file. This configures the Docker Engine daemon and is where new container runtimes are registered.

Find or add the `runtimes` key and insert a new field called `nvidia`. The value should be an object with a `path` that points to `nvidia-container-runtime`. Here's a complete example:

~~~{.json caption="daemon.json"}
{
    "runtimes": {
        "nvidia": {
            "path": "nvidia-container-runtime",
            "runtimeArgs": []
            }
        }
}
~~~

Referencing the runtime called `nvidia` will start the containers using the NVIDIA Container Runtime. The next section will show how this is done. If preferred, all new containers can be made to automatically use the runtime by setting the `default-runtime` field, too:

~~~{.json caption="daemon.json"}
{
    "runtimes": {
        "nvidia": {
            "path": "nvidia-container-runtime",
            "runtimeArgs": []
        }
    },
    "default-runtime": "nvidia"
}
~~~

Restart Docker Engine to apply the changes:

~~~{.bash caption=">_"}
$ sudo systemctl restart docker
~~~

### Preparing the Docker Image

![Preparing the Docker Image]({{site.images}}{{page.slug}}/cxSryWJ.png)\

The NVIDIA Container Runtime relies on the CUDA libraries existing *within* the container images. Other images will still work, but they won't see the GPU hardware.

NVIDIA provides a series of preconfigured images under the [`nvidia/cuda`](https://hub.docker.com/r/nvidia/cuda) tag on Docker Hub. These are designed to be used as customizable base images, which are added to the application. Variants are available with many different architectures, operating systems, and CUDA versions. The full list can be viewed on [Docker Hub](https://hub.docker.com/r/nvidia/cuda/tags). Each tag is structured similarly in the format `11.4.0-base-ubuntu20.04`:

- **`11.4.0`**: CUDA version present in the image.
- **`base`**: The NVIDIA image flavor, defining how many libraries are available (see more later).
- **`ubuntu20.04`**: The operating system that the image is based on.

Three different flavors are available for each combination of operating system and CUDA release: `base`, `runtime`, and `devel`. The `base` variant is the slimmest, including the only CUDA runtime. Switching to `runtime` additionally provides the CUDA math libraries and support for [NVIDIA Collective Communication Library (NCCL)](https://developer.nvidia.com/nccl) multi-GPU communication. The third option, `devel`, adds header files and development tools. It's intended for advanced use when heavily customizing the environment.

Basing the image on top of one of the `nvidia/cuda` tags is the recommended way to use CUDA if a suitable option is available. A descendant image can then be built by writing a Dockerfile that layers in the source code:

~~~{.dockerfile }
FROM nvidia/cuda:11.4.0-base-ubuntu20.04
RUN apt update
RUN apt-get install -y python3 python3-pip
RUN pip install tensorflow-gpu

COPY src/ .
# ...
~~~

The provided base images won't be suitable for every situation, though. So a different operating system may be used, or the image can be more heavily customized. In this case, the CUDA libraries can be manually installed.

The instructions vary by architecture, operating system, and CUDA release, so it's best to use the Dockerfile from [one of the official images](https://gitlab.com/nvidia/container-images/cuda/-/blob/master/dist/11.5.0/ubuntu2004/base/Dockerfile) as a starting point.

The image will need to add the correct CUDA package repository, install the library, and then set some environment variables that advertise GPU support to the NVIDIA Container Runtime:

~~~{.dockerfile}
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
~~~

The container runtime won't attach the hardware if these variables are missing. These can be supplied when starting the container if baking them into the image is not preferred (and is shown later in this guide).

### Starting Containers With GPU Access

`docker run` has a `--gpus` flag, which enables container GPU access. Including this flag in the command will prompt the NVIDIA Container Runtime to connect the hardware to the new container. If you prefer using `nvidia` runtime, you should specify this explicitly if it wasn't set as the *default* earlier on.

Make sure that the installation is working by running the `nvidia-smi` command within an image:

~~~{.bash caption=">_"}
$ docker run -it --gpus all --runtime nvidia \
nvidia/cuda:11.4.0-base-ubuntu20.04 nvidia-smi
~~~

~~~
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 470.141.03   Driver Version: 470.141.03   CUDA Version: 11.4     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  NVIDIA GeForce ... Off  | 00000000:01:00.0  On |                  N/A |
| 42%   74C    P0    70W / 250W |   1333MiB / 11175MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
~~~

This example uses one of the provided `nvidia/cuda` images to verify that the container has access to the host's GPUs. The `nvidia-smi` command is accessible (it would be missing if the container runtime hasn't provided the GPU), detects the hardware, and shows the same results as when it was run directly on the host earlier in this article. The GPU is working inside the container.

## Troubleshooting Containers With  Missing GPU's

![Troubleshooting Containers With  Missing GPU's]({{site.images}}{{page.slug}}/0eTTW9p.png)\

Troubleshooting problems with NVIDIA Container Runtime can usually be done by following this procedure:

1. **Make sure the container is started with the correct runtime**. The NVIDIA runtime must be registered in the Docker daemon config file and selected for the container using the `--runtime` flag. Alternatively, set it as the `default-runtime` in the config file.
2. **Make sure that GPU access is enabled with the `--gpus all` flag**. GPUs will not be provided without this flag, even if the configuration is otherwise correct.
3. **Ensure that CUDA versions match**. Results can be unpredictable or completely broken if the CUDA library version inside the container is significantly different than the release being used on the host. The example host earlier has CUDA 11.4, so the same version was used when selecting the container image to run.

## Configuring GPU Access

The NVIDIA Container Runtime provides a few configuration options for controlling the GPUs made available to the containers. These are enabled using environment variables set within the container. Docker's `--gpus` flag also offers some overlapping controls.

### Using Specific GPUs

On systems with multiple GPUs, it's often preferred to [make](/blog/using-cmake) only a subset of the hardware available to a container. There are a few ways of doing this:

#### Make Two GPUs Available

~~~{.bash caption=">_"}
$ docker run -it --gpus 2 --runtime nvidia \
nvidia/cuda:11.4.0-base-ubuntu20.04 nvidia-smi
~~~

#### Make a Specific GPU Available

~~~{.bash caption=">_"}
$ docker run -it --gpus '"device=1"' --runtime \
nvidia nvidia/cuda:11.4.0-base-ubuntu20.04 nvidia-smi
~~~

#### Make Two Specific GPUs Available

~~~{.bash caption=">_"}
$ docker run -it --gpus '"device=0,1' --runtime \
nvidia nvidia/cuda:11.4.0-base-ubuntu20.04 nvidia-smi
~~~

#### Alternatively, Use an Environment Variable

~~~{.bash caption=">_"}
$ docker run -it --runtime nvidia -e \
NVIDIA_VISIBLE_DEVICES=0,1 nvidia/cuda:11.4.0-base-ubuntu20.04 nvidia-smi
~~~

Run the following command on the host to find the indexes of the GPU hardware to supply to `--gpus` or `NVIDIA_VISIBLE_DEVICES`:

~~~{.bash caption=">_"}
$ nvidia-smi -L
~~~

~~~
GPU 0: NVIDIA GeForce GTX 1080 Ti (UUID: GPU-5ba4538b-234f-2c18-6a7a-458d0a7fb348)
GPU 1: NVIDIA GeForce GTX 1060 (UUID: GPU-c6dc4e3b-7f0d-4e22-ac41-479ae1c6fbdc)
~~~

Setting `--gpus '"device=1"'` or `NVIDIA_VISIBLE_DEVICES=1` will make only the GTX 1060 available to the container.

### Customizing Driver Capabilities

Not every application needs all the capabilities of the NVIDIA driver. The `NVIDIA_DRIVER_CAPABILITIES` [environment variable](/blog/bash-variables) allows only a subset of libraries to be mounted onto the container. And most containerized apps won't be using the GPU to render graphics, so it's possible to filter only the `compute` (CUDA/OpenCL) and `utility` (`nvidia-smi`/NVML) capabilities:

~~~{.bash caption=">_"}
$ docker run -it --runtime nvidia -e \
NVIDIA_DRIVER_CAPABILITIES=compute,utility \
nvidia/cuda:11.4.0-base-ubuntu20.04 nvidia-smi
~~~

The full list of known capability names is available in the [NVIDIA documentation](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/user-guide.html#driver-capabilities).

### Requiring Specific Hardware and Drivers

The `NVIDIA_REQUIRE_*` [environment variables](/blog/bash-variables) allow for constraining GPU access based on specific characteristics of the host environment.

The following four options are available:

- **`cuda`**: filter by CUDA version
- **`driver`**: filter by driver version
- **`arch`**: require a specific CPU architecture
- **`brand`**: require a specific GPU model family, such as GeForce or Tesla

Here's an example where the [container](/blog/docker-slim) image is constrained to GeForce GPUs with CUDA version 11.0 or newer:

~~~{.bash caption=">_"}

$ docker run -it --runtime nvidia -e \
NVIDIA_REQUIRE_CUDA="cuda>=11.0 brand=GeForce" \
nvidia/cuda:11.4.0-base-ubuntu20.04 nvidia-smi
~~~

Multiple constraints passed to the same environment variable are always combined with a logical *and* clause.

## Conclusion

Docker containers don't get automatic access to the system's GPU hardware. Containers lack the drivers that enable GPU communications. This necessitates the use of a vendor-specific layer to expose GPUs inside containers.

[NVIDIA](https://www.nvidia.com/en-us/) hardware is supported by the company's [container](/blog/docker-slim) runtime that wraps the default container runtime with an interface to the host's NVIDIA drivers. GPU support can then be added to the images by basing them on an official NVIDIA CUDA image or manually installing the CUDA libraries inside the Dockerfile.

Containers are a great way to run [CI](https://earthly.dev/blog/continuous-integration/) pipelines because they enable *reproducible builds* that work on any device. The NVIDIA Container Runtime allows the extension of containerized pipelines to include AI and ML workloads, too.

{% include_html cta/bottom-cta.html %}
