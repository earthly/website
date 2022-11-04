---
title: "Using Portainer for Docker Container Management"
categories:
  - Tutorials
toc: true
author: James Walker

internal-links:
 - just an example
---

[Docker's CLI](https://docs.docker.com/engine/reference/commandline/cli/) and [API](https://docs.docker.com/engine/api) are powerful tools, but they can be unwieldy when you're working with large container fleets or looking for a more visual experience. [Portainer](https://www.portainer.io), a web-based Docker management system that provides a convenient graphical user interface (GUI), lets you take charge of your containers, images, volumes, and other resources, without memorizing long terminal commands.

Portainer can be used to monitor your Docker installation, interact with containerized apps, and deploy new stacks with minimal effort. A single Portainer instance can connect to multiple Docker hosts, centralizing your container management around one application. It also supports other container environments beyond Docker, including [Kubernetes](https://kubernetes.io/) clusters and [Azure Container Instances](https://azure.microsoft.com/en-us/products/container-instances/#features).


This article will show you how to set up and start using Portainer. You'll also learn the benefits of some of Portainer's headline features, such as how to deploy apps with built-in templates and your own Compose files.

## What Is Portainer?

[Portainer](https://www.portainer.io) is a container management interface. It started out as a GUI for Docker but has expanded to support several other container environments. It has more than 1 million users and over [22,000 GitHub stars](https://github.com/portainer/portainer). Two versions are available: the free and open source Community Edition (CE) and a paid Enterprise Edition (EE).

![Screenshot of the Portainer dashboard](https://imgur.com/9ragLJ6.png)

You can use Portainer whenever you want to interact with your containers from a graphical interface. CLI commands and API endpoints are often handy in development but less ideal for managing production applications. With Portainer, you can easily monitor multiple endpoints and allow team members to access a shared deployment environment.

## Implementing Portainer

Portainer is usually deployed in its own container. This article assumes you're using Docker, but you can also [run Portainer directly in Kubernetes](https://docs.portainer.io/start/install/server/kubernetes) by deploying with the official [Helm chart](https://helm.sh).

Here's an overview of the steps required to get Portainer running:

- Install Docker
- Create a new container that runs Portainer
- Log into the Portainer UI to set up your initial user account
- Use Portainer or the Docker CLI to manage your Docker environment

The following sections will detail each of these steps in turn.

### Installing Docker

Before you go any further in this tutorial, you'll need to install Docker. If you're using Windows or Mac, download and run [the latest version of the Docker Desktop](https://docs.docker.com/get-docker) installer. Linux users can try [the experimental version](https://docs.docker.com/desktop/install/linux-install) of Desktop for Linux or use the following steps to install [Docker Engine](https://docs.docker.com/engine/).

Docker Engine is distributed in the package repositories of all major Linux distributions. It's also available as a direct download in DEB or RPM format. You can obtain detailed instructions for each method and platform [from the official Docker documentation](https://docs.docker.com/engine/install). The following steps assume you're installing from the repository on a Debian-based system.

To begin, install the dependencies required by running the following commands:

```bash
$ sudo apt-get update
$ sudo apt-get install ca-certificates curl gnupg lsb-release
```

Next, add the GPG key used to sign the Docker repository:

```bash
$ sudo mkdir -p /etc/apt/keyrings
$ curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

This lets the `apt` package manager verify the source of your download. Now add the repository to your package list with the following command:

```bash
$ echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

The interpolated commands allow automatic selection of the correct list for your system.

Docker can now be installed with the following command:

```bash
$ sudo apt-get update
$ sudo apt-get install docker-ce docker-ce-cli containerd.io
```

The `docker` CLI requires root privileges by default. You can avoid prefixing commands with `sudo` by adding yourself to the `docker` group:

```bash
$ sudo groupadd docker
$ sudo usermod -aG docker $USER
```

Log out and log back in to apply the change.

Finally, test your installation by starting a container with the Hello World image:

```bash
$ docker run hello-world
```
```
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
2db29710123e: Pull complete
Digest: sha256:7d246653d0511db2a6b2e0436cfd0e52ac8c066000264b3ce63331ac66dca625
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

### Installing Docker Compose

Although not required to use Portainer, [Docker Compose](https://docs.docker.com/compose/) is a popular utility that makes it easier to manage containers in your terminal. Compose will be used in the next step to start Portainer.

Docker Compose used to be an independent binary but has now been integrated into Docker as a plugin. It's included with Docker Desktop and can be added to the Docker Engine installation configured earlier by running the following command:

```bash
$ sudo apt-get install docker-compose-plugin
```

You should now be able to use `docker compose` in your terminal:

```bash
$ docker compose version
Docker Compose version v2.6.0
```

### Deploying Portainer

Portainer has a few dependencies that must be supplied when you start your container:

- It requires a volume to store persistent data.
- Your host's Docker socket should be mounted into the container so that Portainer can access and interact with the Docker daemon.
- You need to bind a port to the container so you can access the web UI.

This requires several flags to be used when you start Portainer with `docker run`:

```bash
$ docker run -d \
  -p 9443:9443 \
  --name portainer \
  --restart unless-stopped \
  -v data:/data \
  -v /var/run/docker.sock:/var/run/docker.sock \
  portainer/portainer-ce:latest
```

A better way to start Portainer is to use Docker Compose. This lets you write the container's configuration into a file so you can bring up the app with a single command. To do so, save the following file as `docker-compose.yml` in your working directory:

```yaml
version: "3"
services:
  portainer:
    image: portainer/portainer-ce:latest
    ports:
      - 9443:9443
      volumes:
        - data:/data
        - /var/run/docker.sock:/var/run/docker.sock
    restart: unless-stopped
volumes:
  data:
```

This encapsulates all the flags given to the `docker run` command in the previous example.

Here, the `image` field is set to `portainer/portainer-ce:latest` to use the latest Portainer CE release from Docker Hub. Change this to `portainer/portainer-ee:latest` if you've purchased an Enterprise Edition license.

The `ports` field sets up a port binding from your host to the container. You'll be able to access the Portainer UI by visiting `https://localhost:9443`. Portainer provides a self-signed HTTPS certificate, which you can override by [mounting your own](https://docs.portainer.io/advanced/ssl#using-your-own-ssl-certificate-on-docker-standalone) into the container.

The `volumes` field sets up a `data` volume that's mounted to `/data` inside the container. Portainer will write your settings to this location, allowing them to persist after the container restarts. The host's Docker socket, `/var/run/docker.sock`, is [bind mounted](https://docs.docker.com/storage/bind-mounts) straight into the container so Portainer can manage the Docker installation it's running within.

Finally, the `restart` field is set to `unless-stopped`, so Docker automatically starts Portainer after the host reboots unless you manually stop the container first.

Now you can use this Compose file to bring up Portainer:

```bash
$ docker compose up -d
```

Next, head to [https://localhost:9443](https://localhost:9443) in your browser. You'll see a security prompt if you're using Portainer's built-in SSL certificate. This configuration shouldn't be used in production or when Portainer is exposed on a public network, but this is safe for local use.

Once you've acknowledged the prompt, you'll get to Portainer's first run screen. Create your initial user account by entering a username and password and pressing **Create user**:

![Screenshot of creating an initial Portainer user account](https://imgur.com/YjSV1Wf.png)

You'll be taken to the environment setup wizard. This is where you connect Portainer to your containerization systems. Click the **Get Started** button to continue with the local Docker socket mounted into the container from your host, and you'll end up on the Portainer dashboard:

![Screenshot of Portainer's environment setup screen](https://imgur.com/1Tbvau5.png)

## Touring the Portainer Dashboard

The dashboard provides an overview of all the environments you've added to Portainer. Although there's only your `local` environment at the moment, you could add Kubernetes clusters and other remote Docker hosts in the future:

![Screenshot of the Portainer dashboard](https://imgur.com/9ragLJ6.png)

Each environment gets a summary tile, giving quick insights into the number of running, stopped, and healthy containers, as well as counts of the images and volumes available. The sidebar to the left of the screen is where you can navigate between environments, resource types, and application-level global settings:

![Screenshot of Portainer's environment-specific dashboard](https://imgur.com/aHaFN81.png)

Clicking into an environment takes you to its own dashboard that summarizes the number of available resources. Clicking any resource type displays a table enumerating all the objects in the environment. Action buttons at the top of the screen are available to perform context-specific functions, such as stopping a container or deleting an image:

![Screenshot of viewing containers in Portainer](https://imgur.com/Sqp8cVh.png)

## Deploying an Application with Portainer Stacks

Portainer provides several options for deploying new applications. One of these is **stacks**, a thin wrapper around Docker Compose functionality. A stack is a collection of one or more containers that collectively provide a complete application. You could have a stack consisting of an API, a database, and a frontend web UI:

![Screenshot of the **Stacks** screen in Portainer](https://imgur.com/ZYdGhRY.png)

To create a new stack, click the **Stacks** menu item on the left sidebar and then press the **Add stack** button on the top-right. There are four ways to define a stack:

- **Web editor**: This lets you type out a Docker Compose file manually.
- **Upload**: This lets you upload an existing Docker Compose file from your machine.
- **Repository**: This automatically loads a Compose file directly from a Git repository.
- **Custom template**: This lets you can create your own reusable templates by heading to **App Templates** > **Custom Templates** on the left sidebar.

Here's a sample Compose file you can try:

```yaml
services:
  db:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
      - MYSQL_DATABASE=${MYSQL_DATABASE}
     - MYSQL_USER=${MYSQL_USER}
     - MYSQL_PASSWORD=${MYSQL_PASSWORD}
    volumes:
       - db:/var/lib/mysql
  wordpress:
    image: wordpress:latest
    ports:
      - 8880:80
    environment:
      - WORDPRESS_DB_HOST=db
      - WORDPRESS_DB_USER=${MYSQL_USER}
      - WORDPRESS_DB_PASSWORD=${MYSQL_PASSWORD}
      - WORDPRESS_DB_NAME=${MYSQL_DATABASE}
volumes:
  db:
```

This Compose file includes two services that run a basic [WordPress](https://wordpress.com/) site. Enter a name for your stack at the top of the screen, then paste the WordPress Compose file into the editor:

![Screenshot of Portainer's stack editor](https://imgur.com/jUpybTw.png)

The Compose file uses environment variable substitution with `${VARIABLE}` syntax to configure the database connection. You need to supply values for these variables when you start your stack. To do this, scroll down the page and press the **Add an environment variable** button to create a new key-value pair. Repeat this for the four required variables:

- `MYSQL_ROOT_PASSWORD`
- `MYSQL_DATABASE`
- `MYSQL_USER`
- `MYSQL_PASSWORD`

![Screenshot of setting Portainer stack environment variables](https://imgur.com/pShRX09.png)

Press the blue **Deploy the stack** button at the bottom of the screen to start your services. It may take a few minutes for Portainer to pull the required images and create your containers. You'll then be taken to the stack's page, which shows the details of the running containers. You can access the created WordPress site by heading to [http://localhost:8880](http://localhost:8880) in your browser:

![Screenshot of viewing a running stack in Portainer](https://imgur.com/EuRGJqK.png)

## Deploying a Portainer Template

Templates are an even easier way to launch new application instances. Portainer comes with a set of built-in templates for popular apps. These can be reached by heading to **App Templates** on the left sidebar. You can also create your own templates based on Compose files:

![Screenshot of Portainer's built-in app templates](https://imgur.com/ellmw8u.png)

You could replicate the WordPress site created earlier by using the official WordPress template. Head to **Add Templates** and enter "wordpress" into the search bar at the top of the screen:

![Screenshot of searching for the WordPress app template in Portainer](https://imgur.com/u62T3Ch.png)

The template comes preconfigured with the services you need to run a WordPress site. You only have to supply a name for your stack and the root password to set it on the MySQL database server. Enter these into the fields at the top of the page, and then press the **Deploy the stack** button at the bottom:

![Screenshot of deploying the WordPress app template in Portainer](https://imgur.com/7JqCXkf.png)

Wait while Portainer pulls your images and creates your containers. The container will be assigned a random port by default. You can find it by navigating to the stack's details page and then scrolling the Containers table so you can view the port published by the WordPress service. This example is accessible on `localhost:49153`:

![Screenshot of viewing a running stack in Portainer](https://imgur.com/Xbx87JS.png)

## Conclusion

[Portainer](https://www.portainer.io) is a convenient and feature-rich interface for Docker containers and other environments. It brings almost all the capabilities of the Docker UI to your web browser, letting you perform management operations on any device.

Portainer is ideal for many different use cases, from your local development workstation to production app monitoring. You can also use it to track containers and images used by CI/CD pipelines and build systems, preventing excess resources from accumulating on your Docker host.

## Outside Article Checklist

- [ ] Create header image in Canva
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
  - Would any images look better `wide` or without the `figcaption`?
- [ ] Run mark down linter (`lint`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `link-opp` and find 1-5 places to incorporate links
- [ ] Add Earthly `CTA` at bottom `{% include cta/cta1.html %}`
