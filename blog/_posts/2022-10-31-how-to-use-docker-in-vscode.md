---
title: "How to use Docker in VS Code"
categories:
  - Tutorials
toc: true
author: Temitope Oyedele

internal-links:
 - Docker
 - VS Code
 - Container
excerpt: |
    Learn how to use Docker in VS Code with the Docker extension. This article walks you through the process of building, managing, and deploying containerized applications without leaving your code editor, making Docker management easier and more efficient.
last_modified_at: 2023-07-19
---
**This article explains how to use Docker with VS Code. Earthly ensures consistent builds with the Docker extension in VS Code. [Learn more about Earthly](/).**

Created by Microsoft, the  [Docker extension](https://code.visualstudio.com/docs/containers/overview) makes it easy to build, manage, and deploy containerized applications without leaving your code editor. Simply put, it helps you manage Docker better.

In this article, I'll walk you through how to use Docker in VS Code using the Docker extension. This extension has some exciting features that can [make](/blog/using-cmake) working with Docker easier.  

I'll be using this extension to work with Docker by adding a `dockerfile`, building an image, and also running it. I'll do all this without having to use the terminal at all. Let's get started!

## Prerequisites

To follow along with this article, you will need to have [Docker](/blog/rails-with-docker) installed on your workstation. Instructions on installing and running Docker are [available](https://docs.docker.com/get-docker/), and they should be specific to the operating system you are running. You also need to have [VS Code installed](https://code.visualstudio.com/download).

## Installing the Docker Extension

Head to the extension section in VS Code and type `docker` in the search box. You should see something like this:

![Searching for docker extension]({{site.images}}{{page.slug}}/vVdGELj.png)

The first selection in this image is what you want to look for to install. Click on it to install. Once it's done downloading, you will notice a Docker icon or logo at the bottom left corner of your window. This is the [Docker](/blog/rails-with-docker) explorer.

![Docker icon in VS Code]({{site.images}}{{page.slug}}/wqmhmlw.gif)\

Click on it. All our running and stopped containers are highlighted inside the Docker explorer. Here, you can also see your images, registries, volumes, networks, e.t.c. :

![Containers ,volumes, images, and more]({{site.images}}{{page.slug}}/UQWjQRM.png)

## Building Our Project

Let's create a basic node express.js app to show how you can use the extension.

First, create a folder where you want your project to be stored and open it up in VS Code. Next, create a file called `index.js` and paste the following code:

~~~{.js caption="index.js"}
const express = require("express");
const app = express();
const port = 3000;
 
app.get("/", (req, res) => {
  res.send("Hello World!");
});
 
app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
 
~~~

Basically, the code above is just to create a hello world application. All the code does is make the `app` start a server and listen on port 3000 for connections. Then, the app responds with "Hello World!" for requests to the root URL (/).

You won't do anything else with this app as it's just being used to play around in our Dockerfile

## Adding a Docker File

Traditionally, to add Docker, you would need to:
Create a `dockerfile`.
Add Docker instructions to it.
Build the Docker image from the terminal.
Run the Docker image, also from the terminal.

But with the Docker extension, you can have VS Code do most of the heavy lifting for you.

If you have existing projects with Docker or docker-compose files or you simply prefer to write your own, don't worry, the extension still has a lot to offer you. But if you do want to speed up creating these files, you have the option of letting the extension do some of the heavy-lifting for you.

To generate the Docker files automatically, open the Command Palette by pressing `⇧⌘P` on a Mac or `Control+Shift+P` on a Windows PC. Then type:

~~~{.bash caption=""}
Docker: Add Docker files to Workspace command`:
~~~

![Adding docker files]({{site.images}}{{page.slug}}/bM7WWsn.jpeg)

You'll be asked to choose the application platform you're working with. Just proceed to choose  `node`, and you'll also be asked whether to include Docker compose or not. A compose file is typically used when you want to start up multiple containers, say if you also wanted a database, or if you were trying to run a front-end and a back-end together. Since that's not the case with our project you can choose `No`.

You will then be prompted to select a port. Select  `3000` because `3000` is the port on which our app will listen. Now, the following files are added to your workspace: `.dockerignore` and  `Dockerfile`.

Inside the `Dockerfile` should have something like this:

~~~{.dockerfile caption="Dockerfile"}
FROM node:lts-alpine
ENV NODE_ENV=production
WORKDIR /usr/src/app
COPY ["package.json", "package-lock.json*", "npm-shrinkwrap.json*", "./"]
RUN npm install --production --silent && mv node_modules ../
COPY . .
EXPOSE 3000
RUN chown -R node /usr/src/app
USER node
CMD ["node", "index.js"]
~~~

You're probably already familiar with Docker, but just to highlight all the things the extension gives you, here's a brief explanation of what was generated:
**FROM:**Sets the base image to use for subsequent instructions.
**ENV:** Sets the environment variable key to the value.
**WORKDIR:**Sets the working directory to /usr/src/app.
**COPY:** Copies files or folders from the source to the destination path in the image's filesystem.
**RUN:** Executes any commands on top of the current image as a new layer and commits the results.
**EXPOSE:** Defines the network ports on which this container will listen at runtime.
**USER:**Sets the user name or UID to use when running the image in addition to any subsequent CMD, ENTRYPOINT, or RUN instructions that follow it in the Dockerfile.
**CMD:** Provides defaults for an executing container.

Similar to the `.gitignore`, the `.dockerignore` instructs Docker to hold files and folders that should not be replicated when creating the image.

## Building and Running Your Docker File

To build the Docker image, open the `Command Palette` and execute `Docker Images: Build Image`. You can also right-click the `Dockerfile` in the navigation panel and select `Build image:`

![Building an image]({{site.images}}{{page.slug}}/gn9rNt4.jpeg)

If you check the extension pane and look at the `images` section inside the Docker explorer, you should see the latest project has been added to the docker explorer.

![Our latest project]({{site.images}}{{page.slug}}/qxnlDbj.png)

The following step is to run our `image`. Open the command palette once more, type `docker run`, and then pick `Docker: Run`. It will display a list of all the containers on your system. Select the `docker-node:latest` tag and click `Enter`.
  
![Running a container]({{site.images}}{{page.slug}}/lDRhXAu.jpeg)

You can also run the container by going to the left pane, selecting the Docker explorer, then under `IMAGES`, choose the image you want. Right-click on  `latest`. and click run. You will get the same logs running on the terminal.

![Running docker inside the extension]({{site.images}}{{page.slug}}/OU6RnwE.jpeg)

Once the `docker-node` container runs, You can check the running containers in the same section in our Docker explorer. You can also stop them from here.

You have successfully built an image and ran your image all from VS Code without having to open the command terminal.

You can view the app running in the container in the browser. To do this, right-click on the running container in the docker explorer and click on "open in browser":

 ![view in browser]({{site.images}}{{page.slug}}/Em7k5gV.jpeg)\

### Debugging Our Container

The docker extension includes a VS Code debugger configuration inside `.vscode/launch.json` for debugging when running inside a container. To do this, set a breakpoint in the `get()` handler for the '/' in `index.js` by pressing the f9 key. Then go to the `run and debug section` in VS Code and select `Docker Node.js launch` debugger and start debugging by pressing `f5` :

![The run and debug section]({{site.images}}{{page.slug}}/WSiiCWl.png)

![selecting docker node.js launch]({{site.images}}{{page.slug}}/jcR4gOc.png)\

What you'll notice is that the debugger comes to a halt in `index.js` at the breakpoint:

![Using breakpoints]({{site.images}}{{page.slug}}/dnqMcyX.png)

You can then continue by pressing the play button at the top to continue running.

### Viewing Container Logs

This option is available in the context menu for running [containers](/blog/docker-slim). The integrated terminal will display the logs.

Using the running Node.js container as our example, all you have to do is navigate to Docker Explorer. In the Containers tab, right-click on your container and choose View Logs. You should see it being displayed in the terminal

![Viewing container logs]({{site.images}}{{page.slug}}/P8lZ9Fr.jpeg)

![container logs]({{site.images}}{{page.slug}}/Hn6x6xm.png)\

### Docker Inspect Images

The Docker inspect images is a feature that allows you to inspect the images built and see the details in a JSON file. This allows you to see important information about our image i.e the image ID, when it was created, volumes, and many more. Inside our docker explorer, navigate to `IMAGES` and locate the `project folder/latest` right click and click on inspect:

![Docker inspect]({{site.images}}{{page.slug}}/HMQtXXA.jpeg)

![Json file]({{site.images}}{{page.slug}}/4yCyoeN.jpeg)\

### Other Features

I've barely scratched the surface of what the Docker Extension can do. Some other features you may want to look into further include:

- **Docker commands:**
The Command Palette contains most of the commands for Docker images and containers. Typing `Docker:` will find Docker commands.

- **Azure CLI integration:** The Docker extension for VS Code comes with azure CLI integration, which means the Azure CLI can be executed in a separate, Linux-based container by simply running `Docker Images: Run Azure CLI` command. See [Get started with Azure CLI](https://code.visualstudio.com/docs/containers/debug-common).

- **system Prune:** You can use system prune to run Docker system prune, which clears unused images from your system. To do this, run `Docker:prune system` command

- **IntelliSense:** You can use the IntelliSense feature provided by VS Code when creating and editing Docker files by hand. To use the IntelliSense feature, press `ctrl` + space.

### Conclusion

The VS Code docker extension enhances your productivity by streamlining terminal operations and offering features for faster, error-free Dockerfile creation. The added bonus is its ability to provide vital insights into your Docker environments, including debugging tools, logs, and visual mapping of running images and networks.

And if you're enjoying this streamlined Docker workflow in VS Code, you'll likely appreciate [Earthly](https://www.earthly.dev/) for efficient and consistent container-based builds. Why not dive in and explore its capabilities?

{% include_html cta/bottom-cta.html %}