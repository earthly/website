---
title: "Docker Slim"
categories:
  - Tutorials
toc: true
author: Sooter Saalu
internal-links:
 - Docker
 - nginx
 - Docker Slim
 - container
excerpt: |
    Learn how to optimize your Docker images and containers with Docker Slim, a tool that can reduce image size up to thirty times without any manual optimization. Discover how Docker Slim performs static and dynamic analysis to generate smaller and more efficient Docker containers, and how it can help you analyze, compress, and secure your Docker resources.
---
<!--sgpt-->**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. This article Earthly is a powerful build tool that can be used in conjunction with Docker Slim to optimize and streamline the Docker development process. [Check us out](/).**

[Docker](https://www.docker.com/) is an open containerization platform for developing, shipping, and running applications. It enables you to package your applications in isolated environments, called containers, where they can run independently from infrastructure. In the container, they have all the dependencies needed for the application to run.

However, a common issue with [Docker](/blog/rails-with-docker) images is their construction and [size](https://semaphoreci.com/blog/2018/03/14/docker-image-size.html). [Docker Slim](https://dockersl.im/) is a tool for optimizing Dockerfiles and Docker images.

It can reduce image size up to thirty times without any manual optimization. It can also help automatically generate security profiles for your Docker containers and has built-in commands that help you analyze and understand your Docker files and images.

In this article, you'll explore the various [Docker](/blog/rails-with-docker) Slim functionalities and how to use them effectively and efficiently to optimize your Docker images.

## What Is Docker Slim

![What is]({{site.images}}{{page.slug}}/question.jpeg)\

Docker Slim was a [Docker Global Hack Day 2015 project](https://www.docker.com/blog/docker-global-hack-day-3-local-edition-winners/#:~:text=Seattle%2C%20WA%3A%20DockerSlim%20by%20Dmitry%20Vorobev%20and%20Kyle%20Quest). It performs static and dynamic analysis on Docker images in order to reduce layers in the images and produce smaller Docker containers.

The current version of Docker Slim carries out inspections of the container metadata and data (static analysis), as well as the running application (dynamic analysis) to build an application artifact graph. This graph is then used to generate a smaller image.

Docker Slim is a versatile tool and is able to work on containers running applications in [Node.js](https://nodejs.org/en/), [Python](https://www.python.org), [Ruby on Rails](https://rubyonrails.org), [Java](https://www.java.com/en/), Go, [Rust](https://www.rust-lang.org), [Elixir](https://elixir-lang.org), or [PHP](https://www.php.net) languages as well as with the following operating systems: [Ubuntu](https://ubuntu.com), [Debian](https://www.debian.org), [CentOS](https://www.centos.org), [Alpine](https://www.alpinelinux.org), and even [Distroless](https://github.com/GoogleContainerTools/distroless#distroless-container-images).

### Docker Slim Use Cases

![What is]({{site.images}}{{page.slug}}/usecase.png)\

[Docker](/blog/rails-with-docker) Slim can help you gain a deeper understanding of your Docker images and what they contain. This is especially crucial when you're working with images you didn't build. Docker Slim has three commands that specifically provide you with an analysis of your Dockerfiles and Docker images giving you more information about its functioning. These [commands](https://github.com/docker-slim/docker-slim#commands) are `xray`, `lint`, and `profile`.

Docker Slim uses the analyzed data on your Docker image to create an image that is up to thirty times smaller than the original. Docker Slim optimizes your Docker image and the resulting container by reducing your image to the files, libraries, executables, and dependencies necessary for your containers' regular operation.

This optimizes your development process, reducing bloat from your containers, making them smaller and more efficient. This benefits you as a software developer or DevOps engineer, as well as your eventual users.

In addition, Docker Slim can help you optimize the security of your image by automatically generating security profiles for your images that are specific to their functions and behavior using the information analyzed during its build process. The tool currently offers auto-generated [Seccomp and AppArmor profiles](https://security.stackexchange.com/questions/196881/docker-when-to-use-apparmor-vs-seccomp-vs-cap-drop).

## Installing Docker Slim

Docker Slim currently works with Linux and Mac operating systems. It can be installed by downloading the [binary packages](https://github.com/docker-slim/docker-slim#downloads) or utilizing a package manager, like [Homebrew](https://github.com/docker-slim/docker-slim#homebrew). The tool is also available to be pulled as a [Docker image](https://hub.docker.com/r/dslim/docker-slim/tags), and Docker Slim offers a [software-as-a-service (SaaS)](https://portal.slim.dev/login?invitecode=invite.1s85zlfnYX0p5TT1XKja49pAHbL) platform to utilize its functionalities.

For the purpose of this article, an Ubuntu (18.04 LTS) environment was used with Docker Slim installed using the prepared Bash script available on the official [Docker Slim GitHub repo](https://github.com/docker-slim/docker-slim/blob/master/scripts/install-dockerslim.sh) and the following CLI command:

~~~{.bash caption=">_"}
curl -sL \
 https://raw.githubusercontent.com/docker-slim/docker-slim/master/scripts/install-dockerslim.sh \
 | sudo -E bash -
~~~

## Using Docker Slim

Docker Slim has an interactive CLI option that offers suggestions and helps you configure your commands. It can be used by running the `docker-slim` command:
<div class="wide">

![Docker Slim interactive CLI]({{site.images}}{{page.slug}}/d1Tcrf3.png)
</div>
There are three main reasons to use Docker Slim in your development process: analysis, compression, and security. Let's review each in turn.

### Analysis

Docker Slim enables you to have a deeper understanding of your Dockerfiles, images, and containers, with tools that can probe the functioning of your Docker artifacts and generate optimization reports.

As mentioned before, there are three Docker Slim commands that cater toward analysis: `lint`, `xray`, and `profile`.

#### The Lint Command

The [`lint` command](https://github.com/docker-slim/docker-slim#lint-command-options) analyzes your Dockerfile, running checks against the Dockerfile instructions. This command provides warnings, and surveys for errors while giving you information about the instructions in your Dockerfile. It checks for missing `.dockerignore` files, invalid instructions or commands, and unnecessary or unwieldy layers in your Dockerfile.

You can explore all the available checks from the `lint` command using the following CLI command:

~~~{.bash caption=">_"}
docker-slim lint --list-checks
~~~

<div class="wide">

![Available `lint` command checks]({{site.images}}{{page.slug}}/PsVxct6.png)
</div>
Using the `lint` command on Docker images is a work in progress. However, you can use the command on your Dockerfiles using the following syntax:

~~~{.bash caption=">_"}
docker-slim lint --target "path-to-your-dockerfile"
~~~

<div class="wide">

![`lint` command results]({{site.images}}{{page.slug}}/GjfCbK7.png)
</div>

#### The Xray Command

The [`xray` command](https://github.com/docker-slim/docker-slim#xray-command-options) analyzes your Docker images, exploring the layers of the Docker image, commands used, files, libraries, and executables, as well as the changes that will be made in the work environment when the Docker image is built. This command can be used to reverse engineer a Dockerfile from its targeted Docker image. It also gives you insight into the object file sizes and how much container space is being wasted.

Docker Slim often produces reports that are saved as `slim.report.json` in the directory, and the `docker-slim` command is run by default. You can change this by utilizing the `--report` tag.

You can use the `xray` command with the following syntax:

~~~{.bash caption=">_"}
docker-slim --report nginx-report.json xray --target nginx --pull
~~~

This command performs static analysis on the `nginx` Docker image, exploring its metadata and data, and creates a `docker-slim` report called `nginx-report.json`. The `pull` tag pulls the target image from a repository if it's not available locally:
<div class="wide">

![`Xray` command results]({{site.images}}{{page.slug}}/GgqeGIb.png)
</div>

#### The Profile Command

The `profile` command carries out a more involved analysis of your [Docker](/blog/rails-with-docker) images. It performs a dynamic analysis where the Docker image is run, and the container created by that image is then analyzed and probed. This command analyzes both the Docker image and the Docker container that is created from that image. In addition, the `profile` command offers advanced HTTP probe functionality by default that can explore your Docker container's accessibility.

You can utilize this command with the following syntax:

~~~{.bash caption=">_"}
docker-slim --report nginx-profile-report.json profile --target nginx
~~~

<div class="wide">

![`profile` command results]({{site.images}}{{page.slug}}/1MA8BOK.png)
</div>

### Compression

One of the main features you can gain from Docker Slim is its compression ability when applied to your Docker images. For your developer teams that utilize Docker in their development and production lifecycles, you might often be left with multiple large-size Docker images. This has a significant impact on the speed of each step in your process, as it takes longer to load and build on larger Docker containers locally or in production.

Docker Slim offers the [`build` command](https://github.com/docker-slim/docker-slim#build-command-options) for this purpose. This command utilizes both static and dynamic analysis to optimize and create a minimized Docker image.

The `build` command uses the following syntax:

~~~{.bash caption=">_"}
docker-slim --report nginx-build-report.json build --target nginx --copy-meta-artifacts .
~~~

The `copy-meta-artifacts` tag helps move the produced files from the build command to a location more convenient for you. The command above creates the reverse-engineered Dockerfile, optimized Dockerfile, your optimized Docker image, security profiles, and other files in your current working directory.

The results of the build command (at the bottom) show a compressed `nginx.slim` image of 12 MB over its original size of 142 MB:
<div class="wide">

![`build` command results]({{site.images}}{{page.slug}}/fHOgINP.png)
</div>
Now you can use the optimized Docker image in your development process in place of your previous image.

### Security

Docker, and in general, containerized applications, can often be more secure than traditional local applications. However, there are considerations to note, such as the permissions allowed by your kernel, the interaction between Docker, your containers and the file system, and any unnecessary loopholes in your configuration profile.
These concerns can be alleviated by adding another safety layer with a unique security configuration profile to your container.

Docker Slim automatically generates [AppArmor](https://apparmor.net/) and [Seccomp](https://docs.docker.com/engine/security/seccomp/) security profiles when the `build` or `profile` commands are used. These security profiles will be specific to your images and their functionality.

You can use the security profile generated in the previous build command using the following syntax:

~~~{.bash caption=">_"}
docker run -it --rm -d -p 8080:80 \
--security-opt apparmor:nginx-apparmor-profile nginx.slim
~~~

This command utilizes the created `apparmor` security profile in the working directory to start up an `nginx` container using the minimized image. An `nginx` web server is up and running at [http://localhost:8080/](http://localhost:8080/) and its security profile protects the container from internal or external threats by restricting program capabilities such as read or write permission on certain files, as well as root access. It also limits network access to bar unpermitted entry.
<div class="wide">

![`nginx` web server]({{site.images}}{{page.slug}}/1v9wRGp.png)
</div>

## Conclusion

Docker Slim works to optimize your Docker development process, utilizing both static and dynamic analysis to generate information about your Docker resources that can be used to optimize and secure your images. It does this by disposing of miscellaneous packages and files, and streamlining your container to reduce its attack surface and vulnerabilities.

The advent of containerized applications has helped scale up the development and production process for DevOps teams. However, Docker's containerization is not perfect, and improvements can be made.

In this article, you learned about Docker Slim and how it can be used to optimize your Docker resources, utilizing the `lint`, `xray`, `profile`, and `build` Docker Slim commands to optimize your Docker images and containers.

{% include_html cta/bottom-cta.html %}