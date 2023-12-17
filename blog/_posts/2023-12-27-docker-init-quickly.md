---
title: "Getting Started (Quickly) with Docker Init"
categories:
  - Tutorials
toc: true
author: Rajkumar Venkatasamy

internal-links:
 - docker init 
 - using docker init
 - how to use docker init
 - getting started with docker init
 - using docker init quickly
excerpt: |
    This markdown content provides a checklist for writing and publishing an article, including steps such as outlining, drafting, proofreading, creating a header image, and adding internal links. It also includes a checklist for optimizing an article for external publication, including adding an author page, optimizing images, and incorporating external links.
---

[Docker](https://www.docker.com/) is a powerful tool that has revolutionized the way developers develop, package, and deploy applications. As part of the [Docker Desktop 4.18](https://docs.docker.com/desktop/release-notes/#4180) release, several new features were introduced, including a [Learning Center](https://docs.docker.com/desktop/use-desktop/#:~:text=The-,Learning%20center,-view%20helps%20you), an [experimental file-watch command](https://docs.docker.com/desktop/release-notes/#:~:text=experimental%20file%2Dwatch%20command), and [`docker init`](https://docs.docker.com/engine/reference/commandline/init/), which is the focus of this article.

The Docker Init plugin simplifies the setup of new Docker projects by facilitating the generation of Docker assets, including Docker images and containers. This is especially useful for developers who want a quick way to manage Docker assets without having to manually configure everything.

In this article, you'll learn all about `docker init` and how you can use it in your Python projects.

## What Is Docker Init?

`docker init` is a command line interface (CLI) command designed to shorten the manual effort and time required to get started with new projects in a Docker container environment. It supports Python, Go, ASP.NET, Node.js, and Rust.

Once Docker is installed, when you execute the `docker init` command, the CLI will help you create the necessary files with meaningful content loaded by default. When you run `docker init`, the following files are created:

* `.dockerignore` controls the contents of your Docker image and helps optimize its size.
* `Dockerfile` contains instructions for building your application's Docker image.
* `compose.yaml` defines services, networks, and volumes for your application.

If any of these files are already present, a cautionary prompt will be displayed, and you'll be offered the choice to replace all the files.

Docker Init supports [Docker Compose](https://docs.docker.com/compose/) out of the box, making it easy to manage multicontainer applications. Moreover, `docker init` is straightforward to use, making it accessible to developers of all skill levels.

## Getting Started With Docker Init

For this guide, imagine that you have a Python backend REST API application that you want to containerize using Docker. This application uses [Flask](https://flask.palletsprojects.com/), a lightweight framework for Python that's widely used to build APIs. For demo purposes, this app has been prebuilt to serve a GET endpoint that returns the string "Welcome to the Docker Init tutorial".

### Understanding Docker Init with a Python Flask Application

Once Docker Desktop is installed, it's possible to verify the existence of Docker Init by running the following command in your terminal:

~~~
docker init --version
~~~

This command will display the version of the Docker Init plugin:

~~~
Version:    v0.1.0-beta.8
Git commit: b06d94d
~~~

After you've verified what version of Docker Init you have, you can navigate to the project's directory (`flask-app`). This is where the Flask application will be built:

~~~
cd flask-app
~~~

The skeleton demo project can be accessed by cloning the repository from GitHub:

~~~
git clone https://github.com/rajkumarvenkatasamy/getting-started-with-docker-init.git
~~~

Note that the Docker-related files are not present at this phase.

### Setting Up the Virtual Environment and Running the Project

Once the project is cloned, it's time to set up a Python virtual environment from the project directory to test the project locally before containerizing the app using the `docker init` command:

~~~
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
~~~

Once the environment is set up and the necessary requirements are installed, you can run the demo application:

~~~
python main.py
~~~

Upon successful execution, an output is displayed indicating that the application is running:

~~~
 * Serving Flask app 'main'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.29.207:5000
Press CTRL+C to quit
~~~

When you open a browser and access [http://localhost:5000/](http://localhost:5000/), you'll be able to see the output in your browser window:

<div class="wide">
![Welcome page]({{site.images}}{{page.slug}}/M247jfD.png)
</div>

### Initializing the Project with Docker Init

With the local non-Dockerized environment set up and verified, the next step is to initialize the project with the `docker init` command:

~~~
docker init
~~~

This command will generate a `Dockerfile`, a `.dockerignore` file, and a `compose.yaml` file in the project directory. After following the prompts in the interactive terminal window, you'll see a message indicating that the Docker files are ready and the application can be started:

~~~
Welcome to the Docker Init CLI!

This utility will walk you through creating the following files with sensible defaults for your project:
  - .dockerignore
  - Dockerfile
  - compose.yaml

Let's get started!

? What application platform does your project use? Python                               
? What version of Python do you want to use? (3.11.5)         
                                           
? What version of Python do you want to use? 3.11.5
? What port do you want your app to listen on? (8000) 5000
                                               
? What port do you want your app to listen on? 5000                         
? What is the command to run your app? (gunicorn 'venv.Lib.site-packages.werkzeug.wsgi' --bind=0.0.0.0:5000) python main.py

? What is the command to run your app? python main.py

CREATED: .dockerignore
CREATED: Dockerfile
CREATED: compose.yaml

✔ Your Docker files are ready!

Take a moment to review them and tailor them to your application.

When you're ready, start your application by running: docker compose up --build

Your application will be available at http://localhost:5000
~~~

## Docker Init: A Closer Look at the Generated Files

After generating the Docker-related files, you can review them in an editor of your choice. The following code is generated automatically by the Docker Init plugin for the demo `flask-app` project.

`.dockerignore` contains:

~~~
# Include any files or directories that you don't want to be copied to your
# container here (e.g., local build artifacts, temporary files, etc.).
#
# For more help, visit the .dockerignore file reference guide at
# https://docs.docker.com/engine/reference/builder/#dockerignore-file

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
**/.toolstarget
**/.vs
**/.vscode
**/*.*proj.user
**/*.dbmdl
**/*.jfm
**/bin
**/charts
**/docker-compose*
**/compose*
**/Dockerfile*
**/node_modules
**/npm-debug.log
**/obj
**/secrets.dev.yaml
**/values.dev.yaml
LICENSE
README.md
~~~

`Dockerfile` contains:

~~~
# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/engine/reference/builder/

ARG PYTHON_VERSION=3.11.5
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
ARG UID=10001
RUN adduser \
   --disabled-password \
   --gecos "" \
   --home "/nonexistent" \
   --shell "/sbin/nologin" \
   --no-create-home \
   --uid "${UID}" \
   appuser

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
   --mount=type=bind,source=requirements.txt,target=requirements.txt \
   python -m pip install -r requirements.txt

# Switch to the non-privileged user to run the application.
USER appuser

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 5000

# Run the application.
CMD python main.py
~~~

`compose.yaml` contains:

~~~
# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Docker compose reference guide at
# https://docs.docker.com/compose/compose-file/

# Here the instructions define your application as a service called "server".
# This service is built from the Dockerfile in the current directory.
# You can add other services your application may depend on here, such as a
# database or a cache. For examples, see the Awesome Compose repository:
# https://github.com/docker/awesome-compose
services:
 server:
   build:
     context: .
   ports:
     - 5000:5000
~~~

By default, the Docker Init plugin adds sensible contents to each of these files, which are now ready to be used. However, they can be further modified to fit the project's needs. For instance, the image name (`image: flask-app:1.0`) can be added explicitly in the `compose.yaml` file:

~~~
services:
 server:
   image: flask-app:1.0
   build:
     context: .
   ports:
     - 5000:5000
~~~

This builds the Docker image of this demo app with the image name `flask-app` and the version label `1.0`.

### Building and Running the Application as a Docker Container

The next step is to build the Docker image of the demo app and execute the app. This can be done using a specific command that builds the `flask-app` image and then uses the image to run the app automatically:

~~~
docker compose up --build
~~~

The generated image can be checked on the machine by running the following command:

~~~
docker images
~~~

Your output should look something like this:

~~~
REPOSITORY                    TAG                            IMAGE ID       CREATED          SIZE 
flask-app                     1.0                            e31234df2eda   2 minutes ago    149MB
~~~

Once the app is running, you can check the status of the container with the following command:

~~~
docker ps
~~~

Your output will look like this:

~~~
CONTAINER ID   IMAGE           COMMAND                  CREATED          STATUS         PORTS                    NAMES
e3dbf0bbd61c   flask-app:1.0   "/bin/sh -c 'python …"   11 seconds ago   Up 9 seconds   0.0.0.0:5000->5000/tcp   getting-started-with-docker-init-server-1
~~~

You can open a browser and access [http://localhost:5000/](http://localhost:5000/) to view the output:

<div class="wide">
![Welcome page with Docker-based app]({{site.images}}{{page.slug}}/M247jfD.png)
</div>

Recall that this is the same output that was obtained before containerizing the demo app.

## Conclusion

Congratulations! You've successfully explored the new `docker init` command using Python's Flask framework. The concepts that you learned about here can be applied to [any application platform supported by the Docker Init plugin](https://docs.docker.com/engine/reference/commandline/init/#:~:text=choose%20one%20of%20the%20following%20templates). For instance, apart from Flask, Docker Init also supports other Python frameworks including [Django](https://www.djangoproject.com/) and [Pyramid](https://trypyramid.com/). For [ASP.Net Core](https://dotnet.microsoft.com/en-us/apps/aspnet), Docker Init can be used to develop ASP.Net core-based applications and projects.

You can use Docker Init with [Rust](https://www.rust-lang.org/) to leverage its performance and safety, or you can use Docker Init with [Go](https://go.dev/) to initialize Go applications for building and deploying Go-based microservices. Docker Init also supports [Node.js](https://nodejs.org/en) frameworks such as [Express.js](https://expressjs.com/), [Koa.js](https://koajs.com/#introduction), and [Sails.js](https://sailsjs.com/).

The key to mastering any tool is practice, so get started experimenting with `docker init` today. Happy coding!

If you're looking to learn even more about `docker init`, check out our other resources:

* [Using Docker Init in Rust](add link when published)
* [Using Docker Init in Node.js](add link when published)
* [Using Docker Init in Go](add link when published)
* [Using Docker Init in Python](add link when published)

{% include_html cta/bottom-cta.html %}

## Outside Article Checklist

* [ ] Create header image in Canva
* [ ] Optional: Find ways to break up content with quotes or images
