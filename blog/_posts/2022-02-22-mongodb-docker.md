---
title: "Using MongoDB with Docker"
categories:
  - Tutorials
toc: true
author: Soumi Bardhan
internal-links:
 - mongodb
topic: docker
excerpt: |
    Learn how to use MongoDB with Docker to containerize your development environment and easily create isolated instances of MongoDB. This tutorial covers the best practices for running MongoDB in a Docker container, hosting a Flask app, and using Docker volumes to persist data.
last_modified_at: 2023-09-19
---
**"This article examines how MongoDB and Docker work together. Earthly guarantees reproducible Docker builds for MongoDB. [Learn more about Earthly](/)."**

[Docker](https://www.docker.com/) is a powerful development platform that enables users to containerize software. These containers can be run on any machine, as well as in a public or private cloud. Thanks to Docker's lightweight runtime and ability to run processes in isolation, multiple containers can run at the same time on the same VM or server.

[MongoDB](https://www.mongodb.com/) is a NoSQL database service with seamless performance and options for scaling. It uses a JSON-like storage model and doesn't require a predefined database schema. In the real world, much data is unstructured—it doesn't follow a specific schema. NoSQL databases are useful for storing such data. You can just input the data, and new fields will be created. You can also leave fields empty in situations where a lot of data is missing.

MongoDB can be run in a Docker container. There is an [official image](https://hub.docker.com/_/mongo) available on Docker Hub containing the MongoDB community edition, used in development environments. For production, you may custom-build a container with MongoDB's enterprise version.

If you want to use your MongoDB database across several machines, using Docker containers for hosting MongoDB is a great approach – you can easily create new isolated instances. Furthermore, during development, it is easier to start a Docker instance than manually configure a server. If you are developing multiple applications, you can start multiple containers together using a `docker-compose.yaml` file.

In this article, you'll learn the best practices for running a MongoDB container. You'll also learn how to host a simple [Flask](https://palletsprojects.com/p/flask/) app and how to use [Docker volumes](/blog/docker-volumes)  to persist data in a Docker container.

## Docker Components

Before diving into implementation details, let's take a moment to introduce some of Docker's basic concepts.
In a nutshell, Docker containers are stand-alone pieces of software that encapsulate everything needed to run some code, files, dependencies, configurations, and so forth.

The Docker daemon, `dockerd`, manages Docker containers and handles requests via the Docker Engine API.

## Implementing MongoDB in Docker

Now, the first thing you'll want to do to set up your implementation of MongoDB is to [install Docker](https://docs.docker.com/get-docker/), which can be done directly from your terminal. However, using [Docker Desktop](https://www.docker.com/products/docker-desktop) is recommended for a seamless experience.

### Running MongoDB in a Docker Container

For development, it is better to connect to an instance of MongoDB running inside a Docker container locally (instead of a cloud-hosted instance) to save resources. You can pull the latest MongoDB image and run it in a Docker container. For production, the application can connect to a cloud-hosted database using the [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/) or [MongoDB Enterprise Server](https://www.mongodb.com/try/download/enterprise).

In development, you will use Docker to host a MongoDB instance locally. Start by pulling the image for the MongoDB version you want by specifying the tag accordingly:

~~~{.bash caption=">_"}
$ docker pull mongo:4.0.4
~~~

~~~{.merge-code caption=""}
4.0.4: Pulling from library/mongo
7b8b6451c85f: Downloading 36.19MB/43.41MB
ab4d1096d9ba: Download complete
e6797d1788ac: Download complete
e25c5c290bde: Download complete
45aala4d5e06: Download complete
b7e29f184242: Download complete
ad78e42605af: Download complete
1f4ac0b92a65: Download complete
55880275f9fb: Download complete
bd0396c9dcef: Download complete
28bf9db38c03: Downloading 8.608MB/87.07MB
3e954d14ae9b: Download complete
cd245aa9c426: Download complete
~~~

You can start a MongoDB server running the latest version of MongoDB using Docker with the following command:

~~~{.bash caption=">_"}
docker run -d -p 27017:27017 --name test-mongo mongo:latest
~~~

This will pull the latest [official image](https://hub.docker.com/_/mongo/) from Docker Hub. Adding the `-d` flag will ensure that the Docker container runs as a background process, separate from the shell. The `-p` tag signifies the port that the container port is bound back to 27017. You can connect to MongoDB on `localhost:27017`.

To change the port number, you can change the `-p` flag argument to `8000:27017` to use `localhost:8000`. You can also use the `--port` flag to mention the post. Using the latest image helps you avoid version bumps. Execute this to run MongoDB on `port 8000`:

~~~{.bash caption=">_"}
docker run -d --name test-mongo mongo:latest --port 8000
~~~

Or choose your own port:

~~~{.bash caption=">_"}
docker run -d -p 27017:27017 --name example-mongo mongo:latest
~~~

Alternatively, if you pulled the image specifying a version tag, run the Docker container with this command:

~~~{.bash caption=">_"}
docker run -d --name test-mongo mongo:4.0.4
~~~

Then use the following command to open the MongoDB shell. I have used  `mymongo` as an arbitrary container name, though you can replace `mymongo` with `test-mongo` or any other container name of your choosing.

~~~{.bash caption=">_"}
docker exec -it <CONTAINER_NAME> bash
~~~

Your interactive MongoDB shell should look like this:

<div class="wide">
![Interactive MongoDB shell for container]({{site.images}}{{page.slug}}/42ecHnc.png)
</div>

The `show dbs` command will display all your existing databases. Here, you have the admin, config, and local databases, which are empty initially. For details on the different functions that are available from the shell, type "help". This will provide a list of some of the database methods available, including commands to display the database's collections and information.

<div class="wide">
![MongoDb commands]({{site.images}}{{page.slug}}/ZbWETYT.png)
</div>

You can interact with your locally hosted MongoDB instance through this shell directly from your terminal. You can also open up the container CLI using the buttons on Docker Desktop:

<div class="wide">
![Docker desktop: running containers]({{site.images}}{{page.slug}}/hrhqtYp.png)
</div>

To check your container logs, you can use the `docker logs` command followed by the name of your container:

~~~{.bash caption=">_"}
docker logs test-mongo --follow
~~~

<div class="wide">
![Docker logs output for container]({{site.images}}{{page.slug}}/6ppXQIn.png)
</div>

You can also inspect MongoDB's logs with the `docker logs` command:

~~~{.bash caption=">_"}
docker logs example-mongo --follow
~~~

By using the `--follow` flag, the container logs will be updated on your terminal in real time.

### Connecting From Another Container

Once the MongoDB server is running on Docker, you can also run the Flask app in Docker. There is a Dockerfile in the [repository](https://github.com/Soumi7/Mongo-Docker) containing a set of commands to build a Docker image and run it. In this case, connecting both containers to a shared Docker network is a good idea. This will ensure security, as you will not need to publish MongoDB ports to the host. To create a network and connect the MongoDB container to it, use these commands:

~~~{.bash caption=">_"}
docker network create test-network
docker run -d --network test-network --name test-mongo mongo:latest
~~~

Your client container should join the `test-network`, too. Your container will be able to reference the MongoDB container by using the URL `test-mongo:27017`.

### Persisting Data With Volumes

While running MongoDB in Docker, one of the main challenges is storage. Usually, users want to be able to selectively persist data for containers. A good practice is to use volumes to make sure the data persists even after the container is stopped or the Docker daemon is restarted.
By default, the MongoDB image stores its data in the `/data/db` directory. You can mount a volume to this location to enable data persistence. Use this command to create a container `test-mongo` with a [Docker volume](https://docs.docker.com/storage/volumes/) named `data-vol` mounted on it:

~~~{.bash caption=">_"}
docker run -d \
    -p 27017:27017 \
    --name test-mongo \
    -v data-vol:/data/db \
    mongo:latest
~~~

If you want to inspect your volumes, you can do so with the `docker volume inspect` command.

You can check out all the existing volumes to display which volumes are attached to which containers using `docker volume ls`:

~~~{.bash caption=">_"}
> docker volume ls
~~~

~~~{caption="Output"}
DRIVER VOLUME NAME
local 3Fcdd64229ecle6d664F7282F5254b743dce2a9250F84e1d059ddc25698a7294
local 6e6a22f5d527676F53c521ccb08975d9ddf108a8138a1d08d74c1417ed7Ff0e5c
local 6f473750c25bb8a67F292F8bFd295F56d019cF933alOb8bfb7Ffbd6F508155F02
local 9fceebe4F68d1488cd05973e39b277d6a2481a0a07cbOd5474F333300d2ee2a9
local ale1663768c4079642F06f6bb13945c59312b91d6edb744d29d3753dbc63d5a4
local b97a67ebcfd86810F0c9d65e2d62b3d20F8c05c1bba4b79140ef56e8cb4bee16
local c02e17e65cf4426b7d56b62F8Fd835bfeb2684d0e9107c93e23ce16866b1b620
local c8b98cOF64F5bbOc7TH6Fe401961644c698cbcdc2bcec550F44c872940211a51d
local d6bdabd15b59b9ce74727d8e0036e3bbc439e7a706a7d057da3c83155c1fal5e
local d34976aeeb21eebd576d9cbe82b46ed3a4dd736a0747a210dd8Fcb50cc2c230F
local data1
local mongo-data
local new
~~~

### Configuring Your Server

If you want to change the default [MongoDB configurations](https://docs.mongodb.com/manual/reference/configuration-options/), you can use the `--config` flag to pass a location to a text file with configurations. The configuration file follows the YAML format. Here is the command to specify a certain config location:

~~~{.bash caption=">_"}
docker run -d 
    --name test-mongo 
    -v mongo-data:/data/db 
    -v ./mongo.conf:/etc/mongo/mongo.conf
    mongo:latest --config /etc/mongo/mongo.conf
~~~

### Security

You can also add authentication to your MongoDB containers to ensure data security. This will disable unauthorized personnel from connecting to your server.

Add your user account by setting the username and password using the [environment variables](/blog/bash-variables) during container creation. Use the `-e` flag to specify the environment variables `MONGODB_INITDB_ROOT_USERNAME` and `MONGODB_INITDB_ROOT_PASSWORD`:

~~~{.bash caption=">_"}
docker run -d 
    -p 27017:27017 
    --name test-mongo 
    -v mongo-data:/data/db 
    -e MONGODB_INITDB_ROOT_USERNAME=sample-db-user
    -e MONGODB_INITDB_ROOT_PASSWORD=sample-password 
    mongo:latest
~~~

As a result, the database will be started with the user account `sample-db-user`. This new user will be granted root privileges. As the root user will have access control over everything, it is important to provide a safe password. In this case, you can pass the secrets file location as input to the environment variable `MONGODB_INITDB_ROOT_PASSWORD_FILE`. Your password will not be visible on using `docker inspect` to view the container environment variables. To run MongoDB with Docker using your username and password, use the below code:

~~~{.bash caption=">_"}
docker run -d 
    -p 27017:27017 
    --name example-mongo 
    -v mongo-data:/data/db 
    -e MONGODB_INITDB_ROOT_USERNAME=example-user 
    -e MONGODB_INITDB_ROOT_PASSWORD_FILE=/run/secrets/mongo-root-pw 
    mongo:latest
~~~

### Flask App for Student Database Management

In this section, you will create a simple storage app where MongoDB will store records of students' marks. To start, you'll want to open Docker Desktop and delete the containers you just created, as you will be creating a few more now. Then in the Flask web app, you will add functionality for the following:

* Adding a new record to the database
* Editing a record
* Viewing list of all records

This will help ensure that the database is working as expected. Start by cloning this [GitHub repository](https://github.com/Soumi7/Mongo-Docker):

~~~{.bash caption=">_"}
git clone https://github.com/Soumi7/Mongo-Docker.git
~~~

This repository consists of four main sections:

* `templates`: The HTML page templates for different pages.
* `static`: The CSS files for each HTML page.
* `app.py`: The Flask app endpoints are defined here, along with the functions.
* `requirements.txt`: The list of dependencies.

To access the server from your locally hosted Flask app, you will need to export a port using the `-p` flag:

~~~{.bash caption=">_"}
docker run -d -p 27017:27017 --name test-mongo mongo:latest
~~~

Your MongoDB instance will be accessible on `mongodb://localhost:27017`. To visualize and analyze it with a GUI, you can use [MongoDB Compass](https://www.mongodb.com/products/compass).

To run the Flask app, you first need to install Python—any [Python3 version](https://www.python.org/downloads/) will do.

Next, install dependencies by running the following code in your terminal:

~~~{.bash caption=">_"}
python3 -m pip install requirements.txt
~~~

For ease of development, you will run the Python app outside the container and run Mongo inside one. Go ahead and run the Python Flask app with `python3 app.py` now.

<div class="wide">
![Run Flask app]({{site.images}}{{page.slug}}/x66OQjI.png)
</div>

Using the Flask interface, you can add, update, and view records. To get started, go to `localhost:5000`:

<div class="wide">
![Student Grades Database]({{site.images}}{{page.slug}}/RdmkDEB.png)
</div>

Fill in a new record and click on **Submit Grades**. This page will confirm your submission:

<div class="wide">
![New submission accepted for student]({{site.images}}{{page.slug}}/5ppBuz6.png)
</div>

Next, go back to the homepage and click on **Get Grades of all Students**. This page will show all your student records:

<div class="wide">
![List of students and grades]({{site.images}}{{page.slug}}/AlKmLrI.png)
</div>

Add a few more entries and ensure that the app is working as expected. You can also edit submissions for a certain student. After adding a few more records, your database might look like this:

<div class="wide">
![List of students and grades]({{site.images}}{{page.slug}}/ckfPj03.png)
</div>

For this container, you did not attach a volume. So when you create a new container from the same MongoDB image, it will start with an empty database. Go to Docker Desktop and stop the running container `test-mongo`. You can also use `docker stop test-mongo` to stop the container from the terminal. To see the list of running containers and their details, use `docker container list`. Then create another container for MongoDB from the terminal:

~~~{.bash caption=">_"}
docker run -d -p 27017:27017 --name test-mongo2 mongo:latest
~~~

Now go to `localhost:5000` and click on **Get Grades of all Students**:

<div class="wide">
![Empty list of all students]({{site.images}}{{page.slug}}/PPXe3H5.png)
</div>

This time, you will see that all the previous data has been lost, and instead, you are starting with an empty database. This is where volumes come in handy.

Stop the container `test-mongo2`. Create a container called `test-mongo-3` and attach a volume to it. Any data created as part of the lifecycle of that container will be destroyed once the container is deleted. However, you want to persist the data on your local machine, so go ahead and mount a volume using the `-v` argument:

~~~{.bash caption=">_"}
docker run -d -p 27017:27017 --name test-mongo3 -v mongo-data-vol:/data/db mongo:latest
~~~

Then go to `localhost:5000` and add some new records to the student database:

<div class="wide">
![Student records database (Tania, Sam, and Beth)]({{site.images}}{{page.slug}}/xvoPAx6.png)
</div>

When you stop this container and create a new one, you will enable the new container to use the volume of the previous one. Stop this container and create a new container with the `--volumes-from` tag followed by the name of the container with the volume you want to mount onto this container—in this case, `test-mongo-3`:

~~~{.bash caption=">_"}
docker run --volumes-from test-mongo3 -d -p 27017:27017 --name test-mongo4 mongo:latest
~~~

Now, when you go to `localhost:5000`, you will notice that all the data you previously added has remained intact, as Docker attached the volume after the start. Volumes persist until you remove them with the `docker volumes rm` command or by using the `--volumes` flag when destroying a container with `docker rm`.

If your application is running inside a container itself, you can run MongoDB as part of the same Docker network as your application using `--network`. With this method, you will connect to MongoDB on `mongodb://mongodb:27017` from the other containerized applications in the network.

## Conclusion

In this article, you hosted your MongoDB server using Docker. You created a Flask app to test if the server works as expected, and you learned to attach volumes to your container to see how the containers behave with and without them.

There are many advantages of using containers as part of your day-to-day life as a software developer. Containers ensure consistency across operating systems, and by using them, you can ensure uniformity throughout the team. Deploying containers is relatively easy, as your production environment and development will be consistent. By running MongoDB in Docker, you can create new isolated containers from the same image and you can connect the volume associated with one container to another.

[Earthly](https://earthly.dev/) is an automation tool for managing all your [Docker components](https://docs.earthly.dev/docs/guides/docker-in-earthly), images, and containers. With Earthly, you can execute all your builds in containers and ensure uniformity across machines.

{% include_html cta/bottom-cta.html %}