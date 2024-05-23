---
title: "Using Docker Init in Python"
toc: true
author: Vivek Kumar Singh

internal-links:
 - docker init
 - init in python 
 - using docker in python
 - how to use docker init in python
excerpt: |
    This tutorial explains how to use Docker Init with Python to simplify the creation of Docker configuration files like `Dockerfile`, `compose.yaml`, and `.dockerignore`. Docker Init is a user-friendly tool that generates these files based on project-specific needs, making it easier for developers to containerize their Python applications.
categories:
  - Containers
---
**This tutorial explains Docker Init. Earthly optimizes Docker configurations. [Learn more about Earthly](https://cloud.earthly.dev/login).**

[Docker Init](https://docs.docker.com/engine/reference/commandline/init/) is a new plugin for Docker Desktop that's equipped with a CLI tool that helps you set up project files automatically. It guides you by asking questions that help customize the Docker settings for your project.

Docker Init currently supports a variety of popular languages and frameworks, including Python, Node.js, ASP.NET, and Rust. One of its advantages is that it simplifies creating Docker-based Python projects by generating essential files like `Dockerfile`, `.dockerignore`, and `compose.yaml`. Docker Init is particularly useful for Python server applications, where you often need similar configurations for different projects.

In this article, you'll learn how to use `docker init` with Python. Before you dive into the tutorial, let's talk about why Docker Init was created.

## Why Should You Use Docker Init?

Setting up an application on Docker involves configuring numerous settings to ensure smooth operation. Having to repeatedly create the `Dockerfile` and `docker-compose.yaml` files for multiple applications can become a laborious and time-consuming task.

For instance, here's a sample `Dockerfile` file for a Python project:

~~~{.dockerfile caption="Dockerfile"}
FROM python:latest

ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
~~~

This file includes several configurations for a Python project. However, it lacks adherence to many [best practices](https://docs.docker.com/develop/develop-images/instructions/) that are necessary to ensure the creation of error-free application containers.

Similarly, here's a sample `compose.yaml` file for a Python application:

~~~{.yaml caption="compose.yaml"}
version: '3.9'
services:
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - 8000:8000
    container_name: django_app
~~~

Unfortunately, initiating these files from the ground up can introduce errors. Additionally, creating `Dockerfile` and `compose.yaml` files this way can make it difficult to alter the configuration in the future.

Docker Init guarantees stability out of the box by generating `Dockerfile`, `compose.yaml`, and `.dockerignore` files that are tailored to the specific needs of the project. It's a built-in feature of Docker Desktop, which means you don't have to install any extra software to use it. It's also easy to set up, so you can dive right into creating configurations using the CLI.

## Using Docker Init With Python

Before you begin this tutorial, make sure you have [Docker Desktop](https://www.docker.com/products/docker-desktop/) version 4.18 or newer installed on your system. You can check this by navigating to **Settings** in Docker Desktop. Click **Software updates** on the left-hand side of your screen, and you'll see what version of Docker Desktop you're using:

<div class="wide">
![Docker Desktop version]({{site.images}}{{page.slug}}/dg4i6sO.png)
</div>

To demonstrate the functionality of `docker init`, you'll use a simple Python web application based on [Django](https://www.djangoproject.com/). Go ahead and [clone the application](https://github.com/vivekthedev/docker-init-tutorial).

To be able to containerize this application, you have to create three files: `Dockerfile`, `compose.yaml`, and `.dockerignore`.

Open the terminal in the project folder and run the following command:

~~~{.bash caption=">_"}
docker init
~~~

Once you execute this command, you'll be greeted by the Docker Init CLI welcome screen:

<div class="wide">
![Docker Init CLI welcome screen]({{site.images}}{{page.slug}}/GN3OUFS.png)
</div>

This screen will prompt you to select the platform on which your project will run. Select **Python** and press **Enter** to confirm your selection.

Subsequently, the CLI will prompt you to enter the Python version you'd like to use for this specific project. You can either type in the version or opt for the default Python version installed on your system by simply pressing **Enter**:

<div class="wide">
![Select Python version]({{site.images}}{{page.slug}}/pgWOeqO.png)
</div>

Next, the CLI will ask you to specify the port number where the application will be listening. You can input the port by typing or selecting Django's default port, 8000:

<div class="wide">
![Select a port in the CLI]({{site.images}}{{page.slug}}/v2JX2tt.png)
</div>

Finally, the CLI will ask you to enter the command that will be used to run the app. In this case, the app utilizes the default server provided by Django, which is initiated using the command `python manage.py runserver 0.0.0.0:8000`:

<div class="wide">
![Run the command input in Docker Init]({{site.images}}{{page.slug}}/HdwlWeE.png)
</div>

Run `python manage.py runserver 0.0.0.0:8000` and press **Enter**:

<div class="wide">
![Docker Init final screen]({{site.images}}{{page.slug}}/VFq0YI2.png)
</div>

The Docker Init CLI confirms that the Docker files have been prepared and provides you with a `docker compose up --build` command to start your application within the Docker container.

Now, if you take a look at your project directory, you should see the addition of three new Docker files: `Dockerfile`, `compose.yaml`, and `.dockerignore`.

### 1. Dockerfile

If you open the `Dockerfile`, you'll find that each line is extensively commented on, providing thorough guidance for developers regarding the configurations for the project. The `Dockerfile` adheres to best practices, including the use of [`ARG`](https://docs.docker.com/engine/reference/builder/#arg) instructions for defining variables like the Python version and user ID:

~~~{.dockerfile caption="Dockerfile"}
ARG PYTHON_VERSION=3.11.5
FROM python:${PYTHON_VERSION}-slim as base
~~~

This snippet showcases the utilization of `ARG` to specify the Python version and the subsequent usage of the base image. This approach promotes maintainability and understanding for developers working on the project.

Additionally, the `Dockerfile` creates a non-root user named `appuser` to run the application in the container for security purposes:

~~~{.dockerfile caption="Dockerfile"}
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser
~~~

In this snippet, the user with UID 10001 is created using the `adduser` command with the following attributes:

* `--disabled-password` disables password authentication for the user
* `--gecos ""` omits any additional information about the user
* `--home "/nonexistent"` sets the home directory to `/nonexistent`
* `--shell "/sbin/nologin"` assigns `/sbin/nologin` as the user's login shell, preventing interactive login
* `--no-create-home` ensures that a home directory is not created for the user
* `--uid "${UID}"` assigns the specified UID (10001) to the user

The `Dockerfile` also includes instructions for running the application and building container images.

### 2. `compose.yaml`

The `compose.yaml` file sets up multi-container environments and specifies services, networks, and volumes. While containers usually host a single process, it's possible to run multiples, which is why `compose.yaml` configures each service individually.

`compose.yaml` provides clear guidance on each configuration. It also comes preconfigured with a PostgreSQL database for app integration. However, this database will not be utilized because this specific Python project doesn't rely on an external database.

The server configuration provided by the `compose.yaml` file looks like this:

~~~{.yaml caption="compose.yaml"}
services:
  server:
    build:
      context: .
    ports:
      - 8000:8000
~~~

In this snippet, `compose.yaml` defines a service named `server`. It builds an image from the current directory (`context: .`) and maps port 8000 on the host to port 8000 in the container. This allows access to the service from the host machine.

### 3. `.dockerignore`

The `.dockerignore` file lists all the file types that shouldn't be copied to the container in order to save memory. These include Python cache files, IDE config files, and temporary files:

~~~{ caption=".dockerignore"}
-- omitted --
**/.DS_Store
**/__pycache__
**/.venv
**/.classpath
**/.dockerignore
**/.env
**/.git
**/.gitignore
**/.project
**/.settings
-- omitted --
~~~

The double asterisk is a wildcard that matches zero or more directories recursively. So, `**` will match any subdirectory (and sub-subdirectory, and so on) under the current directory. This ensures that the directory names after the forward slash (`/`) get ignored while creating a container, resulting in reduced build time and image size.

## Running the App in a Docker Container

Now, it's time to run the application in a Docker container using the command provided by the Docker Init CLI. Before you run it, make sure Docker Desktop is running, then open the terminal and execute the following command:

~~~{.bash caption=">_"}
docker compose up --build
~~~

This will pull a Python-based image from the Docker Hub repository and start to build the container. After building the container, Docker runs the command that runs the application specified during the creation of the Docker configuration files. The output looks like this:

~~~{ caption="Output"}
-- omitted --
 ✔ Container dinit-server-1  Recreated                                                                             0.9s
Attaching to dinit-server-1
dinit-server-1  | Watching for file changes with StatReloader
dinit-server-1  | Performing system checks...
dinit-server-1  |
dinit-server-1  | System check identified no issues (0 silenced).
dinit-server-1  | October 24, 2023 - 09:34:34
dinit-server-1  | Django version 4.2.6, using settings 'core.settings'
dinit-server-1  | Starting development server at http://0.0.0.0:8000/
dinit-server-1  | Quit the server with CONTROL-C.
~~~

This application is running on port 8000. You can test it by opening the browser on your system and visiting `http://127.0.0.1:8000/`. When you visit the URL, you'll see the following application window:

<div class="wide">
![Application main window]({{site.images}}{{page.slug}}/9DzZW8H.png)
</div>

As you can see, the Django app is working perfectly inside the container, and you can view and test the app locally.

## Conclusion
<!--sgpt-->
In this tutorial, we've covered Docker Init, an essential tool for effortlessly generating `Dockerfile`, `compose.yaml`, and `.dockerignore` files. Docker Init streamlines the process, promoting best practices and offering a straightforward path for developers diving into containerization.

Loved how Docker Init simplified your setup? Take it further with [Earthly](https://cloud.earthly.dev/login) to make your builds just as smooth and repeatable. Earthly can complement Docker by ensuring that your build process is not only straightforward but also consistent across different environments. Check it out for an even tighter build process that integrates seamlessly with your Docker workflow!

{% include_html cta/bottom-cta.html %}
