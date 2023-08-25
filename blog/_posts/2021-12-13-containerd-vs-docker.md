---
title: "Comparing Container Runtimes: containerd vs. Docker"
categories:
  - Tutorials
toc: true
author: Johan Fischer
sidebar:
  nav: "docker"
internal-links:
 - containerd
excerpt: |
    
---
**We're [Earthly](https://earthly.dev/). We make building software simpler and speedier with containerization. If you're deep diving into Docker and `containerd`, you'd be interested in how Earthly can streamline your builds. [Check us out](/).**

<!-- vale HouseStyle.Setup = NO -->
You can't have a conversation about modern infrastructure technology without talking about containers. They provide a simple, secure way to package, distribute, and run applications, and because they run within an isolated namespace in a computer, failures within containers won't affect the entire computing environment. And they're lighter than VMs because they don't have to abstract physical resources or require an installed operating system.

That abstraction is done by the container runtime, or the container engine. Having the container runtime take care of low-level operations also means containerized applications can start faster.

Failing to choose the right container technology for your application may lead to suboptimal performance, additional complexity, or insufficient features, so it's important to consider your options carefully.

In this article, you'll take a closer look at Docker container runtimes and [`containerd`](https://containerd.io/), comparing their features, how they add to each other, and what they can do on their own.

<div class="wide">
![Difference between OS-native and containerized applications]({{site.images}}{{page.slug}}/L7vm7q0.png)
</div>

## A Quick Overview of Docker and containerd's History

[Docker](https://www.docker.com/) started the whole container revolution when it released its container technology in 2013. [`containerd`](https://containerd.io/) is a container runtime with an emphasis on simplicity, robustness, and portability. It was and still is included with Docker. It's the runtime Docker uses to pull images from image registries, create containers, manage storage and networking, and interact with containers.

Behind-the-scenes, `containerd` uses another low-level engine to perform those tasks. `containerd` was actually split out of Docker in [2016](https://www.docker.com/docker-news-and-press/docker-extracts-and-donates-containerd-its-core-container-runtime-accelerate) to allow other container ecosystems like Kubernetes, [AWS Fargate](https://aws.amazon.com/blogs/containers/aws-fargate-launches-platform-version-1-4/), and [Rancher](https://rancher.com/) to use it while Docker could build its own technology platform. By implementing the [Kubernetes Container Runtime Interface (CRI)](https://kubernetes.io/blog/2016/12/container-runtime-interface-cri-in-kubernetes/), via the CRI plug-in, containerd became interoperable with Kubernetes.

## A Deep Dive Into `containerd`

Docker put together a number of kernel features to create the container environment. At its core is the runtime, `containerd`, which provides the means to abstract and allocate resources (like CPU, memory, network, or storage).

<div class="wide">
![Core Linux features used by `containerd`]({{site.images}}{{page.slug}}/sYbQkbS.png)
</div>

As a container runtime, `containerd` can:

- Limit the total memory and CPU shares allocated to containers with cgroups.
- Isolate the processes within a container, blocking it from seeing any host process.
- Extract the container image into an isolated part of the host system, processing it within the container so it sees those files as its own entire file system. This ensures the container cannot access any other container's files or the host files. `containerd` can also attach some parts of the host file system into the container when required.
- Create a UID namespace where the UID 0 (root) within the container (root) maps to a different UID on the host system. This feature ensures that, should the container root process be able to access the host system, it's blocked from running as root on the host.
- Set up the environment variables within the container. Some variables may come from the container image as default, while `containerd` can assign others during the container execution.
- Add or remove Linux [capabilities(7)](https://man7.org/linux/man-pages/man7/capabilities.7.html) when starting a container.
- Allow you to create your own network namespace and provide it to `containerd` to attach it to a container when it starts.

### CRI, `runc`, and CRI-O

The Container Runtime Interface (CRI) is a Kubernetes API that allows Kubernetes to run containers using different runtimes as long as the runtime supports CRI. `containerd` interfaces with CRI so either Docker or Kubernetes can use it.

By default, CRI uses [runc](https://github.com/opencontainers/runc) to implement that interface. runc is a low-level runtime that fully implements the [Open Container Initiative (OCI)](https://opencontainers.org/) standard. It provides the low-level functionalities necessary for containers to interact with Linux kernel features.

<div class="align-right">
 {% picture content-240 {{site.pimages}}{{page.slug}}/jz1TsBX.png --picture --img width="200px" --alt {{ The relationship between Docker, `containerd`, and `runc` }} %}
<figcaption>The relationship between Docker, </br>`containerd`, and `runc`</figcaption>
</div>

`containerd` can also use runc's Windows counterpart, [`runhcs`](https://docs.microsoft.com/en-us/virtualization/windowscontainers/deploy-containers/containerd), to run containers in Windows, or use something like [`kata`](https://katacontainers.io/) to run containers on other platforms.

CRI is an open specification, so Kubernetes doesn't have to use `containerd` only. It can use other lightweight runtimes, like [CRI-O](https://cri-o.io/). Just like containerd, CRI-O can pull container images from registries, instantiate them as containers, and stop, start, or restart containers. It also uses a low-level runtime for these tasks.

The difference is that CRI-O was built specifically for Kubernetes.

<div class="wide">
![The relationship between container clients, runtimes, operating system, and hardware]({{site.images}}{{page.slug}}/yMKTMkg.png)
</div>

### Networking

Unlike Docker, `containerd` doesn't manage complex networking configuration. For simple networking, you can instruct containerd to use the host networking. In this mode, any port exposed by the container is visible from the host, and possibly from systems connected to the host (depending on the host firewall settings).

For complex networking needs, you can create the network namespace using the [Container Network Interface (CNI)](https://github.com/containernetworking/cni) project in GitHub and attach that to your containers.

### Calling `containerd` Directly

You can use the ctr command-line tool to call `containerd` directly. For example, you can use ctr to pull and push container images from an [OCI-compliant repository](https://github.com/opencontainers/distribution-spec/blob/main/spec.md), like Docker Hub, just as you would use the Docker CLI.

This is demonstrated in the following code snippet:

``` bash
ctr image pull docker.io/library/nginx:latest
```

With this command, `containerd`, with the help of runc, extracts the NGINX image into an isolated part of the host's file system. Then, with the command below, it creates and attaches the required namespaces and starts the process.

``` bash
ctr run --net-host docker.io/library/nginx:latest nginx
```

In this example, the NGINX container is using the host network:

![A simple nginx container created by `containerd` showing the welcome page]({{site.images}}{{page.slug}}/gMNjMQT.png)

This was a very simple exercise. On the other hand, running a LAMP stack by directly calling with `containerd`, for example, would be challenging. Using Kubernetes to call containerd is a better option here. A simple pod configuration can look like this:

``` yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  containers:
    - name: apache
      image: docker.io/httpd:2.4.51
      ports:
        - containerPort: 80
    - name: php
      image: docker.io/php:8-fpm-bullseye
    - name: mysql
      image: docker.io/mysql:8.0.26
```

## A Deep Dive Into Docker

Docker, a full-featured container runtime and image building application, uses `containerd` as its internal container runtime abstraction. Obviously, it provides the same functionalities as described earlier. However, Docker is aimed more for human users. Although you can run containers using containerd and ctr, Docker is easier to use and achieves the same results.

A simple analogy is comparing the programming languages C and Python. You could develop the same application in both languages, but for most users, the higher level language Python is easier to learn, use, and maintain.

### Using Docker CLI to Run Containers and Build Images

In addition to what `containerd` offers, Docker adds some significant features. For example, it automatically downloads an image from a remote repository if it's not locally present when `docker run` or `docker build` commands are invoked. Similarly, Docker uniquely names all containers at startup (unless a name is provided on the command line). This helps to identify and manage containers.

Using the same example as above, the command to run an NGINX container is simpler with the Docker CLI:

<div class="wide">
![Using the Docker CLI to pull an image and run a container from it]({{site.images}}{{page.slug}}/WipFaOk.png)
</div>

As a full-featured toolkit, Docker creates and [builds](https://docs.docker.com/engine/reference/commandline/build/) new Docker images using a [Dockerfile](https://docs.docker.com/engine/reference/builder/) and a context. Depending on your OS and Docker version, you can build images with cross-platform compatibility.

Let's briefly walk through how to create your own custom NGINX web server image. To begin, create an `index.html` with the following content:

``` html
<!DOCTYPE html>
<html>
  <head>
    <title>My Welcome page!</title>
  <style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
    </style>
  </head>
  <body>
    <h1>My welcome page!</h1>
    <p>If you see this page, you have successfully updated the
default nginx welcome page.</p>
  </body>
</html>
```

Create a Dockerfile with the following content:

``` dockerfile
FROM nginx:latest
COPY index.html /usr/share/nginx/html/index.html
```

Build the Docker image:

``` bash
docker build -t mynginx:latest .
```

Run the locally built image:

``` bash
docker run -p 80:80 mynginx:latest
```

You should see a custom welcome page when you check.

![An NGINX container created from a custom Docker image showing the welcome page]({{site.images}}{{page.slug}}/CKGQSZs.png)

### Docker Networking

Docker offers four built-in drivers to provide container-to-container network[](/blog/docker-networking) functionality.

- `bridge` is the default network driver to use when you need a container to have normal egress access to the host, network, or the internet, but no ingress access from outside.
- `host` allows the container to share the host's networking configuration.
- `overlay` connects several hosts in a [Docker swarm](https://docs.docker.com/engine/swarm/key-concepts/) and allows containers running on different hosts to communicate with each other.
- `macvlan` assigns a MAC address to a container and so it appears as a separate physical network device on your host system.

### Docker Compose

[Docker Compose](/blog/youre-using-docker-compose-wrong) is a simple Docker tool for creating and running applications spanning across multiple containers. This is useful for running setups like the LAMP stack.

With Docker Compose, you write a YAML file to define the containers and a dedicated, isolated network for them using one of the drivers mentioned in the previous section.

Here's an example of a simple Compose file for a LAMP stack:

``` yaml
services:
  apache:
    build: './apache'
    restart: always
    ports:
      - 80:80
      - 443:443
    networks:
      - frontend
      - backend
    volumes:
      - ./public_html:/usr/local/apache2/htdocs
      - ./cert/:/usr/local/apache2/cert/
    depends_on:
      - php
      - mysql
  php:
    build: './php'
    restart: always
    networks:
      - backend
    volumes:
      - ./public_html:/usr/local/apache2/htdocs
      - ./tmp:/usr/local/tmp
  mysql:
    build: './mysql'
    restart: always
    networks:
      - backend
    volumes:
      - ./database:/var/lib/mysql
```

## Think Complementary, Not Competitive

Using Docker by itself is more suitable for a developer desktop environment than a production setup. Its learning curve is much simpler, and the toolkit is wider. For production workload, you'll probably be using a container orchestration system, which may require using Docker over `containerd`. For example, running [Amazon Elastic Container Service (ECS)](https://aws.amazon.com/ecs/) on EC2 instances requires that you use [Docker for the ECS agent](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html) to launch containers.

Realistically, as a DevOps engineer developing an application on your laptop, building on a controlled CI environment, and running in production, you'll probably have to use both `containerd` and Docker to achieve the best results.

## Conclusion

Using the right platform can be difficult, as each comes with its own standards of running containers and technology continues to evolve rapidly.

`containerd` is a lightweight container runtime, suitable either for limited-resource computing environments or when you're using a container management system like Kubernetes. Due to its basic interface and lack of ability to build images, it may not be suitable for your development purposes.

Docker offers a full-featured toolkit to build, run, and manage container images and containers in standalone and networked setups. It provides more features than `containerd` and is more human friendly. Also, Docker uses containerd, which makes it suitable for desktop and continuous integration (CI) build environments. You could use it in production as well if Kubernetes is not available, or if you need isolated network namespaces.

[Earthly](https://earthly.dev/) is a container image building tool that allows you to define simple specifications for building Docker images in a repeatable way. Consider using it with your container services to automate and simplify deployment pipelines.

{% include_html cta/bottom-cta.html %}
