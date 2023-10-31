---
title: "Docker and Rails: Running Ruby on Rails with Docker"
categories:
  - Tutorials
toc: true
author: Utibeabasi Umanah
internal-links:
 - docker
 - rails
 - docker compose
topic: docker
excerpt: |
    Learn how to run a Ruby on Rails application inside a Docker container and discover best practices for building Docker images. This tutorial covers topics such as creating a Dockerfile, reducing image size with Alpine base images and multistage builds, and running multiple containers with Docker Compose.
last_modified_at: 2023-07-11
---
**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster. This article is about one solution to the complexities of building and deploying Ruby and Rails projects. If you're interested in a containerized approach to building Ruby code then [check us out](/).**

When working with large distributed teams, you often run into the issue of something working on one computer but not others. When building and running applications, each developer has a slightly different development environment. For example, one developer may use a Windows PC to build and run an application that was developed on a Mac. Apart from the differences in the command line, the developer trying to run the applications may not have the required dependencies installed, and the process of finding and installing the correct versions of the dependencies slows development. This is where containerization tools, like [Docker](https://www.docker.com), can help.

Docker lets you package applications with all their dependencies into a single image that can be distributed across teams. By doing so, you only need to install Docker in your development environment to run the application.

If you're building a [Ruby on Rails](https://rubyonrails.org) application, Docker helps to ensure that everyone on the team is running the same version of Ruby and other dependencies your application needs.

In this tutorial, you'll learn how to run a Ruby on Rails application inside a Docker container and what some best practices are for doing so.

## Docker Image

Before you begin this tutorial, you'll need the following prerequisites:

* **Docker:** should be installed on your local machine. Make sure you install the correct version for your [operating system](https://docs.docker.com/get-docker/).
* **[Docker Compose](https://docs.docker.com/compose/):** is needed to manage multiple containers at once. Instructions to install it are available [on the Docker docs](https://docs.docker.com/compose/install/).
* **[Git](https://git-scm.com):** should be installed on your local machine. The sample application you are going to Dockerize is stored in a Git repository on GitHub, and as such, you'll need to have Git installed in order to clone the repository.
* **Ruby on Rails:** needs to be installed if you're creating a new Ruby application. Otherwise, you can clone the [sample project on this GitHub repo](https://github.com/utibeabasi6/docker-rails).

### Writing the Dockerfile

Before you create the Dockerfile, you need a sample application to Dockerize. To clone the sample project, run the following command in your terminal:

~~~{.bash caption=">_"}
git clone https://github.com/utibeabasi6/docker-rails
~~~

You should get an output similar to this:

<div class="wide">
![Cloning a sample project]({{site.images}}{{page.slug}}/UWyi5vm.png)
</div>

Open up the `docker-rails` folder in [Visual Studio Code](https://code.visualstudio.com) or any other IDE, and create a new file called `Dockerfile` in the root directory. In the `Dockerfile`, paste in the following code:

~~~{.bash caption=">_"}
  FROM ruby:2.5.9
  RUN apt-get update && apt-get install -y nodejs
  WORKDIR /app
  COPY Gemfile* .
  RUN bundle install
  COPY . .
  EXPOSE 3000
  CMD ["rails", "server", "-b", "0.0.0.0"]
~~~

Take a look at what each line of code is doing:

* **`FROM`**: instructs Docker to use a specified parent image as a starting point when building the image. Since you're building a Ruby application, you're using the official Ruby image, which has Ruby preinstalled as your base.
* **`RUN`**: is used to run shell commands while building the Docker image. In this tutorial, you're installing [Node.js](https://nodejs.org/en/) because Rails depends on it.
* **`WORKDIR`**: sets the specified directory as the working directory inside the Docker image. Any further commands run in the Dockerfile will be run in the context of this directory.
* **`COPY`**: is used to copy files from the host machine into the Docker image. The syntax for this is `COPY <source> <destination>.`. The period (`.`) refers to the current directory.
* **`EXPOSE`**: informs Docker that the application will be listening on the specified port when the container is run. This command is mainly for documentation purposes and doesn't actually open the port.
* **`CMD`**: is the main entry point to your Docker image. It's the command that is run whenever a container is created.

### Building and Running the Docker Image

Now that you've created a `Dockerfile`, it's time to build the image. In your terminal, change your directory to the `docker-rails` directory and run the following command:

~~~{.bash caption=">_"}
 docker build -t rubyapp .
~~~

<div class="wide">
![Docker build command]({{site.images}}{{page.slug}}/tvFGMGs.png)
</div>

Now, if you run the command `docker images`, you should see the newly created `rubyapp` image:

<div class="wide">
![Docker images output]({{site.images}}{{page.slug}}/2GJxcTo.png)
</div>

It's important to note that the `docker build` command doesn't run the container, it just creates the image. In order to run the application we need to use the image to run a container instance

To create a container from this image, run the command `docker run -p 3000:3000 rubyapp`. This creates a container and binds port `3000` of your host computer to port `3000` of the container. Now navigate to [http://localhost:3000](http://localhost:3000) on your browser, and you should see the newly created Rails application.

Finally, stop the container with `CTRL + C`.

## Best Practices when Building Docker Images

When building Docker images, there are a few best practices you need to take note of, including using an [Alpine](https://hub.docker.com/_/alpine) base image and reducing image size with multistage builds.

### Use an Alpine Base Image

Alpine images are typically smaller and lighter in weight because they don't have most of the unused packages and dependencies other images come with. Making use of these images as a base helps reduce the size of Docker images. This results in faster download speeds when deploying.

Take a look at the current size of our RubyApps image. Run the command `docker images .`:

<div class="wide">
![Docker images output]({{site.images}}{{page.slug}}/2GJxcTo.png)
</div>

As you can see, the image is 995MB in size. This is not ideal, so you need to modify the Dockerfile to make use of an Alpine base image. Replace the code in your Dockerfile with the following:

~~~{.bash caption=">_"}
  FROM ruby:2.5.9-alpine
  RUN apk add \
    build-base \
    postgresql-dev \
    tzdata \
    nodejs
  
  WORKDIR /app
  COPY Gemfile* .
  RUN bundle install
  COPY . .
  EXPOSE 3000
  CMD ["rails", "server", "-b", "0.0.0.0"]
~~~

To begin, you replace the base image with an Alpine image. Because Alpine images use `apk` instead of `apt-get` as a package manager, you have to modify the `RUN` command to reflect this. You then install some necessary packages for your Rails app since the Alpine image is mostly bare.

Now, run the command `docker build -t rubyapp .` to rebuild the image. If you run `docker images` again, you should see that the image size has reduced to 599MB:

<div class="wide">
![Reduced image size]({{site.images}}{{page.slug}}/NOCh5uv.png)
</div>

### Do Multistage Builds

Another way of reducing image size is by having [multistage build](/blog/docker-multistage). In a multistage build, your Dockerfile will compose of multiple steps, where all dependencies are installed in one stage, and the application is built. Then only the files necessary to run the application are included in the final stage.

Replace the code in your Dockerfile with this:

~~~{.bash caption=">_"}
  FROM ruby:2.5.9-alpine AS builder
  RUN apk add \
    build-base \
    postgresql-dev
  COPY Gemfile* .
  RUN bundle install
   FROM ruby:2.5.9-alpine AS runner
  RUN apk add \
      tzdata \
      nodejs \
      postgresql-dev
  WORKDIR /app
  # We copy over the entire gems directory for our builder image, containing the already built artifact
  COPY --from=builder /usr/local/bundle/ /usr/local/bundle/
  COPY . .
  EXPOSE 3000
  CMD ["rails", "server", "-b", "0.0.0.0"]
~~~

The first stage is named `builder` with `AS` as the keyword. Then you install the packages necessary to install the Ruby dependencies. Next, you copy in the `Gemfile` and `RUN bundle install` to install the needed gems.

In the second stage, you install the dependencies necessary to run the app and copy the Ruby gems from the builder stage. You do this by specifying `--from=builder` to tell Docker to copy from the builder stage.

Now you need to rebuild the Docker image by running `docker build -t rubyapp .` and then run the command `docker images`. You will see that your image size has reduced further to 387MB:

<div class="wide">
![Docker images output 387MB]({{site.images}}{{page.slug}}/hzbuxmw.png)
</div>

## Multiple Containers With `docker-compose`

If you run the Docker image you just built, you'll be greeted with an error page in your browser:

<div class="wide">
![Ruby error page]({{site.images}}{{page.slug}}/howuZHw.png)
</div>

Rails expects a [PostgreSQL](https://www.postgresql.org) database to be running on localhost, but that isn't the case since you're running inside of a container. A solution to this is to start a separate PostgreSQL Docker container and point your application to it. Thankfully, Docker has a tool for setting up and managing multiple containers: Docker Compose. Docker Compose is configured with a YAML file, which must be named `docker-compose.yaml` or `docker-compose.yml`.

### Modifying Your Database Settings

Before you write the `docker-compose` file, you need to modify your application to connect to the database. In the config directory, modify the `database.yml` file with the following:

~~~{.bash caption=">_"}
development:
 <<: *default
 # database: app_development

 username: <%= ENV['POSTGRES_USER'] %>
 password: <%= ENV['POSTGRES_PASSWD'] %>
 host: <%= ENV['POSTGRES_HOST'] %>
~~~

Make sure to comment out the `database:` since you'll be using the default database for now. The username, password, and host are set from environment variables.

### Writing the `docker-compose.yaml` File

Create a file called `docker-compose.yaml` and paste in the following code:

~~~{.bash caption=">_"}
  version: "3.9"
  services:
    app:
      image: rubyapp
      environment:
        POSTGRES_USER: postgres
        POSTGRES_PASSWD: example
        POSTGRES_HOST: db
      ports:
        - 3000:3000
    db:
      image: postgres:alpine3.15
      environment:
        POSTGRES_PASSWORD: example
~~~

Here, you define the version as `3.9`; then, you specify two services. The app service is making use of the RubyApps image you just built, and then you set four environment variables for the `POSTGRES_PASSWD`, `POSTGRES_USER`, and `POSTGRES_HOST`. After that, you expose port `3000`.

The second service, `db`, uses the PostgreSQL image, this is an image that gets pulled down from Docker Hub. Then it sets a single environment variable for the `POSTGRES_PASSWORD`.

> Note that you're passing in `db` as the `POSTGRES_HOST` name because Docker Compose runs all the containers on a single network, and you can send requests to other containers through their hostname, which is the same as the service name. So in this example, the hostname for the database container is `db` since you're using `db` as the service name.

Now, start the containers by running `docker-compose up`:

<div class="wide">
![`docker-compose up` output]({{site.images}}{{page.slug}}/j23KsEv.png)
</div>

Navigate to [http://localhost:3000](http://localhost:3000). And you should be greeted with the Rails app:

<div class="wide">
![Ruby default homepage]({{site.images}}{{page.slug}}/HRq8TqN.png)
</div>

## Conclusion

In this article, you learned how to build a Docker image for a Ruby on Rails application and how to reduce image size by making use of Alpine base images and multistage builds. You also learned how to run multiple containers with Docker Compose and connect your application to a database.

[Earthly.dev](https://earthly.dev/) is a free and open source syntax for defining cacheable, parallelizable, and Git-aware build steps. Earthly takes some of the best ideas from Makefiles and Dockerfiles, and combines them into one specification. With Earthly, you can run unit and integration tests, create several Docker images at a time, and easily define multistage builds.

{% include_html cta/bottom-cta.html %}
