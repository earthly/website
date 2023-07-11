---
title: Understanding Docker Logging and Log Files
toc: true
categories:
  - Tutorials
tags:
- docker
- tutorials
author: Sanket Makhija
sidebar:
  nav: "docker"
internal-links:
  - docker log
  - container log
  - docker logging
  - logging
  - log driver
  - logging driver
  - side car logging
  - side-car logging
excerpt: |
    Learn how to effectively manage Docker logging and log files to improve the performance and reliability of your containerized applications. Discover different logging strategies, Docker logging commands, and the various logging drivers supported by Docker.
---
<!--sgpt-->**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. This article is about Docker logging and log files. Earthly is a popular choice for developers and DevOps professionals who are looking for an efficient and reliable build tool for their containerized applications. [Check us out](/).**

Docker logging and its management are an important part of the containerization of your application. Once you've deployed your application, logging is one of the best tools to help reveal errors, aid in debugging, and optimize your application's performance.

With that in mind, let's dive into Docker logging and its log files.

## Introduction To Docker Logging

Developers, DevOps professionals, and product stakeholders all apply knowledge gained from logging to improve a system's performance and reliability. Much of what an application, server, or OS does should be recorded in the logs and aggregated in an easily accessible location. A [log analysis](https://www.sumologic.com/glossary/log-analysis/) then uses all the log events and audit trails to help chalk out a clear picture of events that happen across your application.

In [Docker](https://www.docker.com/), containers are isolated and bundled with software, libraries, and configuration files. In a traditional single-server setup log analysis is centralized on a single node, but with a stateless containerized setup logging becomes more complex. Why? Two reasons:

**1. Containers are transient.** When a Docker container broadcasts logs, it sends them to the application's `stdout` and `stderr` output streams. The underlying container logging driver can start accessing these streams, and the logs are stored on the Docker host in JSON files ([`json-file` is the default logging driver used by Docker](https://docs.docker.com/config/containers/logging/json-file/)). It writes JSON-formatted logs to a file on the host where the container is running. Any logs stored in the container will be deleted when it is terminated or shut down.

**2. Containers are multi-leveled.** There are two levels of aggregation in Docker logging. One refers to the logs from inside the container in your Dockerized application, and the second refers to the logs from the host servers (that is system logs or Docker daemon logs), which are generally located in `/var/log`. A log aggregator that has access to the host pulls application log files and accesses the file system inside the container to collect the logs. Later, you'd need to correlate these log events for analysis.

In this article, you'll learn about different logging strategies you can use in a Dockerized application—how you can access logs and understand Docker logging commands, drivers, configuration, and management to build a highly performant and reliable infrastructure.

## Docker Logging Commands

`docker logs` is a command that shows all the information logged by a running container. The `docker service logs` command shows information logged by all the containers participating in a service. By default, the output of these commands, as it would appear if you run the command in a terminal, opens up three I/O streams: stdin, stdout, and stderr. And the default is set to show only stdout and stdout.

- `stdin` is the command's input stream, which may include input from the keyboard or input from another command.
- `stdout` is usually a command's normal output.
- `stderr` is typically used to output error messages.

The `docker logs` command may not be useful in cases when a logging driver is configured to send logs to a file, database, or an external host/backend, or if the image is configured to send logs to a file instead of stdout and stderr. With `docker logs <CONTAINER_ID>`, you can see all the logs broadcast by a specific container identified by a unique ID.

```bash
$ docker run --name test -d busybox sh -c "while true; do $(echo date); sleep 1; done"
$ date
Tue 06 Feb 2020 00:00:00 UTC
$ docker logs -f --until=2s test
Tue 06 Feb 2020 00:00:00 UTC
Tue 06 Feb 2020 00:00:01 UTC
Tue 06 Feb 2020 00:00:02 UTC
```

`docker logs` works a bit differently in community and enterprise versions. In Docker Enterprise, `docker logs` read logs created by any logging driver, but in Docker CE, it can only read logs created by the json-file, local, and journald drivers.

For example, here's the JSON log created by the [hello-world](https://hub.docker.com/_/hello-world) Docker image using the json-file driver:

```bash
{"log":"Hello from Docker!\n","stream":"stdout","time":"2021-02-10T00:00:00.000000000Z"}
```

As you can see, the log follows a pattern of printing:

- Log's origin
- Either `stdout` or `stderr`
- A timestamp

You can find this log in your Docker host at:

```bash
/var/lib/docker/containers/<container id>/<container id>-json.log  
```

These Docker logs are stored in a host container and will build up over time. To address that, you can implement log rotation, which will remove a chunk of logs at specified intervals, and a log aggregator, which can be used to push them into a centralized location for a permanent log repository. You can use this repository for further analysis and improvements in the system down the road.

To find `container_id`, run the `docker ps` command. It'll list all the running containers.

```bash
$ docker ps
CONTAINER ID   IMAGE       COMMAND             CREATED             STATUS              PORTS     NAMES
cg95e1yqk810   bar_image  "node index.js"     Y min ago           Up Y min            80/tcp     bar_app
```

Then, the `docker logs container_id` lists the logs for a particular container.

```bash
docker logs <container_id>
```

If you want to follow the Docker container logs:

```bash
docker logs <container_id> -f
```

If you want to see the last N log lines:

```bash
docker logs <container_id> --tail N
```

If you only want to see any specific logs, use `grep`:

```bash
docker logs <container_id> | grep node
```

If you want to check errors:

```bash
docker logs <container_id> | grep -i error
```

## Logging Drivers Supported by Docker

Logging drivers, or log-drivers, are mechanisms for getting information from running containers and services, and Docker has lots of them available for you. Every Docker daemon has a default logging driver, which each container uses. Docker uses the json-file logging driver as its default driver.

Currently, Docker supports the following logging drivers:

<!-- vale off -->
|                                     Driver                                      |                                               Description                                               |
| :