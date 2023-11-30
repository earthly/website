---
title: "Using Docker with Postgres: Tutorial and Best Practices"
categories:
  - Tutorials
toc: true
author: Aveek Das
internal-links:
 - docker postgres
 - postgres docker
 - postgres containers
 - database containers
topic: docker
excerpt: |
    Learn how to use Docker with Postgres to simplify data management and streamline the development process. This tutorial covers best practices for running PostgreSQL databases on Docker containers and includes step-by-step instructions for setting up and connecting to a PostgreSQL instance using Docker.
last_modified_at: 2023-07-11
---
****This article discusses PostgreSQL on Docker. Earthly simplifies your build process for scripting PostgreSQL Docker setups. [Check it out](https://cloud.earthly.dev/login).****

Relational databases have been an easy way to store relational data for the last few decades. Over the years, many popular database management systems have been created, but installing them can be tricky.

To avoid all the complications in installing and configuring database servers, users can now leverage [Docker](https://www.docker.com/) containers specially developed to support database solutions.

In this article, you'll learn more about what Docker is and how to use it. Then you'll look at some best practices for running [PostgreSQL](https://www.postgresql.org/) databases on Docker containers. To learn more about Docker, you can check out the [official guide](https://docs.docker.com/).

To learn more about Docker, you can check out the [official guide](https://docs.docker.com/).

## Use Cases for Running PostgreSQL on Docker

When considering running PostgreSQL, you should take into account portability. If you're a developer working on multiple machines, each time you switch a machine, you need to set up and configure the database separately. If you use PostgreSQL inside a Docker container, you can quickly use Docker to spin up PostgreSQL containers and focus on actual development rather than setup.

However, keep in mind that data is not persistent and gets removed as soon as the container is turned off when you're using PostgreSQL inside a Docker container. In order to address this issue, you can mount a local directory as a volume and store PostgreSQL data from the container into the local volume. You'll learn more about this below.

In addition to that, databases are stateful applications, while containers are built to run stateless applications. Also, databases are very resource-intensive applications, and running such databases on a [production workload is not ideal](https://vsupalov.com/database-in-docker/). An alternate solution might be to use any database-as-a-service offering from a cloud vendor, like AWS, [GCP](https://cloud.google.com/gcp/), or Azure in production but use containers for quick development.

## How to Run PostgreSQL Using Docker

In this section, you're going to run a PostgreSQL instance using Docker and use a graphical user interface (GUI) and pgAdmin to connect to the database. To begin, you need to have Docker installed on your machine. You can check if you already have Docker installed on your machine by running the following command on your terminal:

~~~{.bash caption=">_"}
$ docker --version
  Docker version 20.10.1, build dea9396
~~~

If you don't have Docker installed, you can install it from the [official website](https://docs.docker.com/get-docker/).

### Download PostgreSQL Docker Image

With Docker, you can either create or own your images or use images from the repository. In this case, since you're using a PostgreSQL Docker image, it can be pulled from [Docker Hub](https://hub.docker.com/) using the following command:

~~~{.bash caption=">_"}
docker pull postgres
~~~

This command connects you to the Docker Hub and pulls the PostgreSQL image to your machine. By default, Docker pulls the latest image from the Docker Hub.

> Note that Docker uses the default tag **latest** if there are no tags defined in the pull request. However, based on your requirements, you can always specify a specific version of the image that you would want to work with.

~~~{.bash caption=">_"}
$ docker pull postgres
Using default tag: latest
latest: Pulling from library/postgres
ae13dd578326: Pull complete
723e40c35aaf: Pull complete
bf97ae6a09b4: Pull complete
2c965b3c8cbd: Pull complete
c3cefa46a015: Pull complete
64a7315fc25c: Pull complete
b9846b279f7d: Pull complete
ed988fb8e7d9: Pull complete
ed4bb4fd8bb5: Pull complete
ead27f1733c8: Pull complete
7d493bacd383: Pull complete
0920535e8417: Pull complete
db76d5bdbf2c: Pull complete
Digest: sha256:99aa522df573a6f117317ab9627c1ba4717513090fd013b937c91a288933ee90
Status: Downloaded newer image for postgres:latest
docker.io/library/postgres:latest
~~~

## Check Installed Docker Images

Once the PostgreSQL Docker image has been pulled from the Docker Hub, you can verify the image by using the following command:

~~~{.bash caption=">_"}
$ docker image ls
REPOSITORY                                 TAG             IMAGE ID       CREATED         SIZE
postgres                                   latest          5cd1494671e9   15 hours ago    376MB
~~~

This command lists all the images that are installed in your local machine.

## Run the PostgreSQL Docker Container

Now that you have the PostgreSQL Docker image on your machine, you can start the container. As mentioned above, a container is an instance of a Docker image. In order to start the PostgreSQL container, there are a few parameters that you need to provide Docker, which are explained below:

- **--name:** the name of the PostgreSQL container.
- **--rm:** this removes the container when it's stopped.
- **-e:** the only mandatory [environment variable](/blog/bash-variables) is the database password that needs to be provided before creating the container.
- **-p:** the port mapping needs to be provided so that the host port on the machine will map to the PostgreSQL container port inside the container.

~~~{.bash caption=">_"}
docker run \
  --name pgsql-dev \
  –rm \
  -e POSTGRES_PASSWORD=test1234 \
  -p 5432:5432 postgres
~~~

<div class="wide">
![Starting the PostgreSQL container]({{site.images}}{{page.slug}}/G834nrN.png)
</div>

As soon as you run the command above, Docker starts the PostgreSQL container for you and makes it available. Once your container is up and running, you can open another terminal window and connect to the PostgreSQL database running inside the container.

Now, open another terminal window and type in the following command:

~~~{.bash caption=">_"}
$ docker exec -it pgsql-dev bash
root@6b7f283ad618:/#
~~~

This command lets you connect to the PostgreSQL CLI running inside the Docker container. Once the interactive terminal is started, you can connect to the PostgreSQL instance with the following command:

~~~{.bash caption=">_"}
psql -h localhost -U postgres
~~~

This command connects you to the PostgreSQL database using the default PostgreSQL user. The configurations are as follows:

- **Hostname:** you need to provide the hostname on which the PostgreSQL Docker container is running. Usually it's "localhost" if it's running locally.
- **Username:** by default, the PostgreSQL image uses a username "postgres" that you can use to log in to the database.

You can now run SQL queries against this database as usual:

~~~{.bash caption=">_"}
postgres=# \l
                                 List of databases
   Name    |  Owner   | Encoding |  Collate   |   Ctype    |   Access privileges
-----------+----------+----------+------------+------------+-----------------------
 postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 |
 template0 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
(3 rows)

postgres=#
~~~

## Use a Persistent Volume to Store Data

In the above section, you learned how to create and run a Docker container for PostgreSQL. An important point to note is that when you perform any DDL or DML within your database, all the data is written inside the container. This means as soon as you remove the container from your machine, there is no way to access the data.

In order to overcome this, you might want to write the data outside the Docker container into your disk drive. This way, you can run your PostgreSQL container on Docker and store all the data in a directory that is unaffected by Docker operations. At a later point, you can also use another PostgreSQL instance to read from this persistent data by mounting a volume for your Docker container.

Basically, you need to map the data directory of the PostgreSQL from inside the container to a directory on your local machine. This can be done using the following command:

~~~{.bash caption=">_"}
$ docker run \
  --name pgsql-dev \
  -e POSTGRES_PASSWORD=test1234 \
  -d \
  -v ${PWD}/postgres-docker:/var/lib/postgresql/data \
  -p 5432:5432 postgres 
3f1ae1ace07ab7902851d8e968a4a0b245cd4171eaa91181e859f21cbea14415
~~~

As you can see above, you have two new parameters:

- **Detached mode:** denoted by `d`, the detached mode will allow the container to run in the background.
- **Volume:** the local directory on the host is mapped to the data directory for PostgreSQL inside the container.

> Note that both paths are separated by a colon.

When you run the command above, you'll see that the container has started and data files are available in the directory that you have configured while starting the container. (You might need superuser permission to view the contents of the directory.)

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/9310.png --alt {{ Locally mounted directory }} %}
<figcaption>Locally mounted directory</figcaption>
</div>

## Best Practices for Running PostgreSQL on Docker

Docker makes it easy to set up a PostgreSQL database in seconds. But there are few best practices that can ensure a smooth experience and offer extra security.

1. Use a persistent volume to store data. As mentioned above, without a persistent volume, you'll lose data if the container restarts.
1. Use [alpine images](https://hub.docker.com/_/postgres) if possible. They're usually smaller in size. For instance, `postgres:14.2` is 131mb in size whereas `postgres:14.2-alpine` is only 78mb with the same functionality. Additionally, alpine images are [secure](https://alpinelinux.org/about/) because all the userspace binaries are compiled to protect against common vulnerabilities.
1. Backup your data periodically. You can do this by running the `pg_dump` command from the database container:

  ~~~{.bash caption=">_"}
  docker exec -it <container_name> \
    pg_dump -U<user_name> --column-inserts --data-only <db_name> > \
    backup_data.sql
  ~~~
<!-- markdownlint-disable MD029 -->
4. If there is no database when PostgreSQL starts in a container, a default database will be created and it will not accept incoming connections during that time. This may cause issues with automation tools which may try to access the database as soon as the container starts. To mitigate this, you need to ensure that the database is accepting connections before trying to connect to it. If you're using [Docker Compose](https://docs.docker.com/compose/), you can use the [healthcheck](https://docs.docker.com/compose/compose-file/compose-file-v2/#healthcheck) feature:
<!-- markdownlint-enable MD029 -->

~~~{.yaml caption="dockercompose"}
healthcheck:
       test: ["CMD-SHELL", "pg_isready -U postgres"]
       interval: 5s
       timeout: 5s
       retries: 5
~~~

## Limitations of Running PostgreSQL Database with Docker

While the quick start-up and easy configuration of Docker is a boon for development and testing, it's generally not advised to run production databases in Docker. The primary reason is that Docker containers are great for running stateless applications. The containers can be terminated any time and be brought back instantly. Multiple containers of the same application can run at the same time, and being stateless, this doesn't affect the workflow.

However, a database is stateful, and so any disruption caused in a database application can have catastrophic consequences. Even if you use a volume to persist the data, a database container crashing and terminating in the middle of a transaction could spell disaster. For production, it's always recommended to choose platform-as-a-service solutions like GCP, AWS, or Azure.

## Conclusion

In this article, you've learned about running a PostgreSQL instance on Docker. You implemented the instance using Docker and used a GUI and pgAdmin to connect to the database. You also learned about a few best practices like using a persistent volume to store data so that you can offer a smooth experience and secure data.

In order to deploy your container-based applications, you need to implement a CI/CD pipeline that will continuously build your Docker image and deploy it when new versions of your code are available. [Earthly](https://docs.earthly.dev/docs/guides/docker-in-earthly) is a popular CI tool that can be used to automate your container deployments. It provides integrations with most of the popular CI tools. You can learn more about Earthly on their [website](https://earthly.dev/).

{% include_html cta/bottom-cta.html %}
