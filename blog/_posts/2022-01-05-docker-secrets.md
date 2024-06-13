---
title: "The Complete Guide to Docker Secrets"
toc: true
author: Allan MacGregor
sidebar:
  nav: "docker"
internal-links:
 - docker secrets
topic: docker
excerpt: |
    Learn how to securely manage secrets in Docker with Docker secrets. This article explains the benefits of using Docker secrets and provides a step-by-step guide on setting up Docker Swarm and leveraging Docker secrets in your development workflow.
last_modified_at: 2023-07-11
categories:
  - containers
---
**This article discusses managing Docker secrets. Earthly significantly improves CI pipelines for Docker Swarm users. [Check it out](https://cloud.earthly.dev/login/).**

Even if you've used [Docker](https://www.docker.com/) for your smaller or locally developed software, you might find that it can be daunting for more complex tasks. This can especially be true for secrets management and sharing—areas often overlooked when working with containerized applications.

There isn't a standardized approach for accessing and managing secrets in containers, which has resulted in homegrown or inadequate solutions better geared for more static environments. Fortunately, the Docker ecosystem offers a great option with [Docker secrets](https://docs.docker.com/engine/swarm/secrets/).

This article will explain the benefits of using Docker secrets. You will learn how to set up [Docker Swarm](https://docs.docker.com/engine/swarm/) and leverage Docker secrets as part of your development flow.

## What Is Docker Secrets?

[Docker secrets](https://docs.docker.com/engine/swarm/secrets/) is Docker's secrets management service, offered as part of its container orchestration stack. In Docker, a secret is any piece of data, like passwords, SSH private credentials, certificates, or API keys, that shouldn't be stored unencrypted in plain text files. Docker secrets automates the process of keeping this data secure.

## What Is Docker Swarm?

[Docker Swarm](https://docs.docker.com/engine/swarm/) is a container orchestration tool that allows the management of containers across multiple host machines. It works by clustering a group of machines together; once they are in the group, you can run Docker commands as you normally would.

To use secrets on your Docker container and through [Docker Compose](https://docs.docker.com/compose/), you will need to make sure that you are running your [Docker Engine](https://docs.docker.com/engine/) in Swarm mode.

## Why You Need Secrets Management

Secrets management is an important aspect of container security and for any application handling configuration variables, SSH keys, passwords, API tokens, private certificates, or other data that shouldn't be accessible to anyone outside of your organization.

Secrets can be used to prove a user's identity and to authenticate and authorize the user to access applications and services. Once you start running multiple instances of your containerized applications, you need to keep, synchronize, and rotate all secrets.

A common use case is persisting and prepopulating sensitive data in our containers (for example, database credentials) that might change between environments; another common use case in a microservice architecture is sharing a known secure key or token to authenticate communication between services.

There are several commonly used options for managing secrets.

### Stored in Docker Compose and Stack Files

Often, `docker-compose.yml` files look something like this:

``` yaml
version: '3'

services:

  my_database:
    container_name: my_database
    hostname: my_database
    image: postgres
    volumes:
      - ./volume:/var/lib/postgresql
    environment:
      - POSTGRES_DB=mydb, mydb_dev
      - POSTGRES_USER=notsecure
      - POSTGRES_PASSWORD=aStrongPassword
    ports:
      - 54321:5432
    restart: unless-stopped
```

Unfortunately, this is a common mistake, as this will allow the sensitive information needed by the container to be committed to version control, making it easily accessible by anyone with access to the repository or the file.

### Embedded Into Docker Images

Container images should be both reusable and secure. Creating images with embedded configuration or secrets breaks these principles and leads to a multitude of potential problems:

- If you copy files with sensitive information into the image, they're accessible through a previous layer even if a file is later removed.
- If the image is reliant on external files for configuration, this causes the image to couple with the configuration and breaks the [reusability](/blog/achieving-repeatability) principle.

### Stored in Environment Variables

Storing configuration in environment variables is common practice and recommended in some situations, following the [Twelve-Factor App methodology](https://12factor.net/config). Unfortunately, it is also common practice to use `.env` variables for storing sensitive information. There are a few downsides to this:

- Secrets stored in an environment variable are more vulnerable to accidental exposure.
- These variables are available to all processes, and it can be difficult to track access.
- Applications might accidentally print the entire collection of `.env` variables during debugging.
- Secrets can be shared with subprocesses with little oversight.

## Docker Secrets to the Rescue

As you can see, the above options can potentially compromise your security. Docker secrets offers a solution. It provides the following advantages:

- Secrets are always encrypted, both in transit and at rest.
- Secrets are hard to unintentionally leak by the consuming service.
- Secrets access follows the [principle of least privilege](https://www.docker.com/blog/least-privilege-container-orchestration/).

You're going to set up Docker Swarm with Docker secrets. For this tutorial, make sure of the following:

- Docker client and daemon versions are at least 1.25. Run `docker version` to confirm:

![Docker version]({{site.images}}{{page.slug}}/efa4xhP.png)

- Docker is running on Swarm mode. Run `docker info` to confirm:

![Docker Swarm]({{site.images}}{{page.slug}}/V5HcgCK.png)

## Enabling Swarm Mode

Swarm mode is not enabled by default, so you will need to initialize your machine by running the following command:

``` bash
docker swarm init
```

<div class="wide">
![Docker Swarm init]({{site.images}}{{page.slug}}/c1ildpG.png)
</div>

Running this command turns your local machine into a Swarm manager.

There are a few concepts you'll need to know when working with Docker Swarm:

- **Node:** An instance of the Docker engine connected to Swarm. Nodes are either managers or workers. Managers schedule which containers run while workers execute tasks, and by default, managers are also workers.
- **Services:** A collection of tasks to be executed by workers.

## Creating Your First Secret

Now that you're in Swarm mode, create a sample secret:

```bash
openssl rand -base64 128 | docker secret create secure-key -
```

Pass your secret to a new service:

```bash
docker service create --secret="secure-key" redis:alpine
```

To make use of the secret, your application should read the contents from the `in-memory`, the temporary filesystem created under `/run/secrets/secure-key`:

```
> cat /run/secrets/secure-key 
Wsjmn/7cqixYLH8hABc8fTuv5/oeki2+5Hn4NzVUdNEQquSUfaDJT/80vh0MA1hl
uTCL504xjCEqogq5xFfLNPupKz9isUAESMCkc0nhGb39UZbt3Rk+Qk+J6M3xBSEe
VzgvNfjLkvk4nJqGfyYIx0mxj7zgLmL2NzQzzLEGhPg=
```

All containers in that service can freely access the secret, making it automatically available on the appropriate hosts. Remember, services might be associated with one or more containerized applications; this makes Docker secrets ideal for shared secrets and API credentials.

## About Swarm and Secrets

There are a few more things to note about using Docker Swarm for secrets, according to the [documentation](https://docs.docker.com/engine/swarm/secrets/):

- A service's access to secrets can be allowed or revoked at any time.
- A newly created or running service can be granted access to a secret; then the decrypted secret is mounted into the container in an in-memory filesystem.
- A node only has access to secrets if the node is a swarm manager or running service tasks that have been granted access to the secret.
- A container task can stop running; then the decrypted secrets shared to it are unmounted from that container's filesystem and deleted from the node's memory.
- A secret that's being used by a running service can't be removed.

## Using Secrets With Compose

For a more practical method, take a look at the [official `docker-compose.yml` example](https://docs.docker.com/engine/swarm/secrets/), which leverages the use of Docker secrets in a WordPress site:

```yaml
version: "3.9"

services:
   db:
     image: mysql:latest
     volumes:
       - db_data:/var/lib/mysql
     environment:
       MYSQL_ROOT_PASSWORD_FILE: /run/secrets/db_root_password
       MYSQL_DATABASE: wordpress
       MYSQL_USER: wordpress
       MYSQL_PASSWORD_FILE: /run/secrets/db_password
     secrets:
       - db_root_password
       - db_password

   wordpress:
     depends_on:
       - db
     image: wordpress:latest
     ports:
       - "8000:80"
     environment:
       WORDPRESS_DB_HOST: db:3306
       WORDPRESS_DB_USER: wordpress
       WORDPRESS_DB_PASSWORD_FILE: /run/secrets/db_password
     secrets:
       - db_password


secrets:
   db_password:
     file: db_password.txt
   db_root_password:
     file: db_root_password.txt

volumes:
    db_data:
```

Let's break down the above file. Here is what's happening:

- The `secrets` line under each service defines the Docker secrets you want to inject into the specific container.
- The main `secrets` segment defines the variables `db_password` and `db_root_password` and a file that should be used to populate their values.
- The deployment of each container means Docker creates a temporary filesystem mount under `/run/secrets/<secret_name>` with their specific values.

Unlike the other methods, this guarantees that secrets are only available to the services that have been explicitly granted access, and secrets only exist in memory while that service is running.

## Conclusion

You should now be familiar with some of the most common mistakes developers make when creating containerized applications with secret or sensitive information. Recognizing and avoiding these mistakes will help you keep your applications secure.

Another way to avoid these mistakes is to use secrets management with Docker. Sensitive data is always immutable, never written to disk, and never sent in clear-text format over the network. If you plan to leverage Docker Swarm in production, you should also use Docker secrets for local development.

To further expand on the possibilities of your Docker containers, try [Earthly](https://cloud.earthly.dev/login). The free, open-source build automation tool helps you more easily create and reuse complex container builds. You can also use it to build Dockerfiles. Earthly runs on top of your continuous integration system to improve your workflow.

For more information, check the [Earthly Documentation](https://docs.earthly.dev/).

{% include_html cta/docker-fundamentals-cta.html %}
<!-- {% include_html cta/bottom-cta.html %} -->
