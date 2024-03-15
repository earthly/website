---
title: "Building an ARM-Based Docker Image Using GitHub Actions"
categories:
  - Tutorials
toc: true
author: Rahul Rai

internal-links:
 - building an arm-based docker image using gitHub actions
 - arm-based docker image
 - how to build arm-based docker image
 - build arm-based docker image using github actions
excerpt: |
    This tutorial explains how to automate the creation and deployment of Docker images specifically designed for ARM architecture using GitHub Actions. It covers the process of building and running a Docker image on an ARM device, as well as building an ARM-based Docker image on a non-ARM device.
---
**Automating ARM Docker images with GitHub Actions can significantly streamline the development process. Earthly Satellites can produce ARM even faster. [Check it out](https://cloud.earthly.dev/login).**

[ARM processor architecture](https://www.arm.com/architecture) is a family of instruction set architectures (ISAs) for central processing units (CPUs). An ISA helps applications talk to the hardware by specifying the processor's capabilities and outlining how user instructions are executed based on those capabilities.

ARM processors adopt a simplified set of instructions using the [reduced instruction set computer (RISC) model](https://www.arm.com/glossary/risc), which contributes to their efficiency, compactness, and lightness. This architectural choice has fueled the popularity of ARM-based devices, like the affordable and adaptable [Raspberry Pi](https://www.raspberrypi.com/).

In addition to IoT and server devices, ARM architecture is [gaining popularity](https://www.counterpointresearch.com/insights/arm-based-pcs-to-nearly-double-market-share-by-2027/) in the personal computing industry due to its efficiency and cost-effectiveness. Apple's [M1](https://en.wikipedia.org/wiki/Apple_M1) and [M2](https://en.wikipedia.org/wiki/Apple_M2) chips are examples of this shift towards ARM architecture.

The rapid growth of ARM-based devices, combined with the [growing popularity of containerization](https://www.zdnet.com/article/cncf-reports-record-kubernetes-and-container-adoption/), means that application developers need to publish container images for multiple platforms while ensuring compatibility across ARM and x86-x64 architectures as well as Linux and Windows environments. This multi-platform approach helps ensure that applications can run smoothly on a variety of devices, ranging from high-powered servers and desktops to low-end mobiles and ubiquitous IoT devices.

In this article, you'll learn how to automate the creation and deployment of Docker images specifically designed for ARM architecture using GitHub Actions.

## How to Build an ARM-Based Docker Image Using GitHub Actions

With the rising popularity of ARM devices, more and more applications need to be able to run on them. However, since ARM devices aren't typically powerful enough to run heavy development jobs, the development world is mainly X86-based. This means developers usually create Docker images on non-ARM devices, and these images can't run on ARM devices.

You can, in theory, use an emulator such as [QEMU](https://www.qemu.org/) on ARM devices to run Docker images built on non-ARM devices, but that emulation is painfully slow and can reduce productivity. That's why, it's recommended that you build an ARM-based Docker image so that you can run it directly on ARM devices.

For old Docker versions, you needed to have an ARM device or use QEMU to build ARM-based images. However, with the advent of [`buildx`](https://github.com/docker/buildx), it's possible to easily build ARM-based images on non-ARM devices.

### Prerequisites

This tutorial uses a simple Python application that prints out basic information about the system it's running on. All the source code for this tutorial is available in [this GitHub repository](https://github.com/rahulrai-in/arm-gh-actions).

Before you can continue, you'll need:

* The latest version of [Python](https://www.python.org/downloads/).
* [Git](https://git-scm.com/download) installed on your system and a [GitHub account](https://docs.github.com/en/get-started/quickstart/creating-an-account-on-github).
* An ARM device, such as a Raspberry Pi, and a non-ARM device. Codes in this article were tested on a Raspberry Pi 4 running Raspbian 10 and on an AMD device running NixOS 23.11.
* The latest [Docker Desktop](https://docs.docker.com/desktop/) or the latest [Docker Engine](https://docs.docker.com/engine/). The latest Docker Desktop includes [`buildx`](https://github.com/docker/buildx), a Docker CLI plugin that extends the build capabilities of Docker. It enables Docker to build images for multiple platforms. You can also use it to build Docker images in parallel, which can significantly reduce build time. The latest [Docker Engine](https://docs.docker.com/engine/) requires you to install `buildx` separately, as provided in the installation instructions.
* An account in a container registry, such as [Docker Hub](https://hub.docker.com/).

Once you've completed these prerequisites, you're ready to create your demo application and set up GitHub Actions to automate the Docker image generation process.

### Building and Running a Docker Image on an ARM Device

In the first section of this tutorial, you'll build and run a Docker image on an ARM device natively. For this reason, this section is executed on an ARM device.

First, create a new directory, add a file named `main.py` within the directory, and copy and paste the following code into the file:

~~~{.python caption="main.py"}
import platform

print("This program is running on " + platform.machine())
print("Platform system: " + platform.system())
print("Platform version: " + platform.version())
print("Platform node: " + platform.node())
print("Platform architecture: " + str(platform.architecture()))
~~~

This script uses the `platform` module to access the system information and prints it to the console. It prints the machine type, operating system, version, node, and architecture. The following is an example output of the script running on a Raspberry Pi with an ARM processor:

~~~{.bash caption="main.py"}
This program is running on armv7l
Platform system: Linux
Platform version: #1559 SMP Wed Jun 1 13:24:16 BST 2022
Platform node: raspberrypi
Platform architecture: ('32bit', 'ELF')
~~~

You can also verify this output by running `uname -m`. This command prints the architecture of the system it's running on:

~~~{.bash caption=">_"}
$ uname -m
armv7l
~~~

Now it's time to write the [Dockerfile](https://docs.docker.com/engine/reference/builder/). Create a new file named `Dockerfile` in the same directory as the Python script, and copy and paste the following code into it:

~~~{.Dockerfile caption="Dockerfile"}
# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the Python script into the container at /app
ADD main.py /app

# Run the command to execute your Python script
CMD ["python", "./main.py"]
~~~

This Dockerfile uses the official Python image as the base image. Then, it sets the working directory to `/app` and adds the Python script to the container. Finally, it executes the Python script using the `CMD` instruction.

To build the Docker image from the Dockerfile on your local machine, run the following command in the same directory as the Dockerfile (replace `<your-registry-username>`) with the username of your container registry account:

~~~{.bash caption=">_"}
docker build -t <your-registry-username>/python-app .
~~~

This command builds the Docker image using the Dockerfile and tags it with the name `python-app`. Once the build is complete, you can run the Docker image using the following command:

~~~{.bash caption=">_"}
docker run <your-registry-username>/python-app .
~~~

This command creates a container from the Docker image and executes it to print the host platform information to the console. The output generated from the command should be similar to the previous one.

### Building an ARM-based Docker Image on a Non-ARM Device

It's not always possible to use an ARM machine to build ARM-based Docker images. If your development or CI machines are predominantly non-ARM, it makes sense to build the Docker image on non-ARM devices. However, as you'll see, images built on a non-ARM device will not run on an ARM device by default.

To demonstrate, on your non-ARM device, either copy and paste the same code or clone this [GitHub repo](https://github.com/rahulrai-in/arm-gh-actions). Then, run the following command to build the Docker image and push it to the registry:

~~~{.bash caption=">_"}
docker build --push -t <your-registry-username>/python-app .
~~~

> Note: Make sure you are logged in to the registry by running the [`docker login`](https://docs.docker.com/reference/cli/docker/login/) command beforehand.

Go back to your ARM device and run the newly built image:

~~~{.bash caption=">_"}
docker pull <your-registry-username>/python-app
docker run --rm <your-registry-username>/python-app
~~~

You'll face an error message like this:

~~~{.bash caption="Output"}
WARNING: The requested imahe's platform (linux/amd64) does not match the detected host platform (linux/arm/v7) and no specific platform was requested
exec /usr/local/bin/python: exec format error
~~~

This simply means that since the image was created on a non-ARM device, it won't run on an ARM device.

To fix this, you'll need to use `buildx` to build for the ARM platform:

~~~{.bash caption=">_"}
docker buildx build --platform linux/arm/v7  --push -t \
<your-registry-username>/python-app .
~~~

> Note: You might need to use something else instead of `linux/arm/v7`, depending on your ARM device. You can figure out what value to use by looking at the "host platform" value in the error message in the previous step.

Go back to your ARM device and run the image again:

~~~{.bash caption=">_"}
docker pull <your-registry-username>/python-app
docker run --rm <your-registry-username>/python-app
~~~

This time, the image will execute without an error.

At this point, you've created a Docker image for your Python application and tested it on your system. Now it's time to automate the build and image push process using GitHub Actions. In the following section, you'll set up GitHub Actions to build and push the Docker image to a Docker registry every time you push updates to your code.

### Set Up GitHub Actions

To set up GitHub Actions, you have to create a GitHub repository for your application and push the code to it. Once you've pushed your code to the repository, create a new file named `main.yml` in the `.github/workflows` directory. This file contains the workflow definition for your GitHub Action.

Copy and paste the following code into the file:

~~~{.yaml caption="main.yml"}
name: Build ARM Docker Image

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Check out code
        uses: actions/checkout@v2

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v1

      - name: Log in to GitHub Container Registry
        uses: docker/login-action@v1
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v2
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.repository }}:latest
          platforms: linux/arm/v7
~~~

Here's the breakdown of the workflow definition:

* The `name` field defines the name of the workflow (`Build ARM Docker Image`).
* The `on` field defines the event that triggers the workflow (the `push` event on the `main` branch).
* The `jobs` field defines the jobs that are executed as part of the workflow. In this case, there is only one job named `build`.
* The `runs-on` field defines the operating system on which the job is executed (`ubuntu-latest`).
* The `steps` field defines the steps that are executed as part of the job. In this case, there are four steps:
  * The first step checks out the code from the repository.
  * The second step sets up Docker `buildx` to build Docker images for the ARM platform.
  * The third step logs in to the [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry) using the GitHub token.
  * The fourth step builds and pushes the Docker image to the GitHub Container Registry. It uses the `context` field to specify the directory containing the Dockerfile. Then, it uses the `push` field to specify that the image should be pushed to the registry. It also uses the `tags` field to specify the name of the image. Finally, it uses the `platforms` field to specify the platforms for which the image should be built. In this case, it is `linux/arm/v7`, which means that the image will be built for the ARM architecture.

To trigger the workflow, you need to commit and push the workflow definition to the repository. Once you've committed the changes, the workflow is triggered automatically. You can view the status of the workflow by going to the **Actions** tab in your repository. The following screenshot shows the status of one of the workflow runs:

<div class="wide">
![Workflow status]({{site.images}}{{page.slug}}/bXAmOKC.png)
</div>)

Once the workflow is complete, you can view the Docker image in the GitHub Container Registry by clicking the generated package displayed on the **Code** tab in your repository:

<div class="wide">
![Viewing a generated package]({{site.images}}{{page.slug}}/M06co4U.png)
</div>

Click the package to view the details of the Docker image, including the tags, platforms, and the command you can use to pull the image:

<div class="wide">
![Viewing Docker image details]({{site.images}}{{page.slug}}/umeOC8Z.png)
</div>)

You'll notice that you're using Docker's platform emulation using `buildx` to build the ARM-based image. This is because GitHub runners are X86-based. However, ARM-based runners are in [private beta](https://github.blog/changelog/2023-10-30-accelerate-your-ci-cd-with-arm-based-hosted-runners-in-github-actions/), and once they're available to the public, you can build ARM-based Docker images natively. Meanwhile, you can use a [self-hosted ARM runner](https://actuated.dev/blog/native-arm64-for-github-actions) if you want to natively build ARM images.

### Run the Docker Image

Now that you've created the Docker image for your Python application, you can run it on your ARM machine. Simply pull the image from the GitHub Container Registry and run it:

~~~{.bash caption=">_"}
docker run ghcr.io/<user-name>/<repository-name>:latest
~~~

This command creates a container from the Docker image and executes it. The output should be similar to the one shown in the previous section.

## Conclusion

In this article, you learned how to automate the creation and deployment of Docker images for ARM architecture using GitHub Actions. You learned how to set up a Python application, create a Dockerfile, and configure GitHub Actions to automate the build and image push process. This automation ensures that your users have access to the latest version of your application, regardless of their platform.

{% include_html cta/bottom-cta.html %}
