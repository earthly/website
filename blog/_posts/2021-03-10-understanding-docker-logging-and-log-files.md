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
| :-----------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------: |
|                                    **none**                                     |            No logs are available for the container and Docker logs do not return any output.            |
|      **[local](https://docs.docker.com/config/containers/logging/local/)**      |                    Logs are stored in a custom format designed for minimal overhead.                    |
|  **[json-file](https://docs.docker.com/config/containers/logging/json-file/)**  |                 Logs are formatted as JSON. The default logging driver for Docker.                  |
|     **[syslog](https://docs.docker.com/config/containers/logging/syslog/)**     | Writes logging messages to the Syslog facility. The Syslog daemon must be running on the host machine.  |
|   **[journald](https://docs.docker.com/config/containers/logging/journald/)**   |        Writes log messages to journald. The journald daemon must be running on the host machine.         |
|    **[gcplogs](https://docs.docker.com/config/containers/logging/gcplogs/)**    |                       Writes log messages to Google Cloud Platform (GCP) logging.                       |
|    **[awslogs](https://docs.docker.com/config/containers/logging/awslogs/)**    |                             Writes log messages to Amazon CloudWatch logs.                              |
|     **[splunk](https://docs.docker.com/config/containers/logging/splunk/)**     |                      Writes log messages to Splunk using the HTTP Event Collector.                      |
|       **[gelf](https://docs.docker.com/config/containers/logging/gelf/)**       |    Writes log messages to a Graylog Extended Log Format (GELF) endpoint, such as Graylog or Logstash.    |
|    **[fluentd](https://docs.docker.com/config/containers/logging/fluentd/)**    | Writes log messages to fluentd (forward input). The fluentd daemon must be running on the host machine. |
|    **[etwlogs](https://docs.docker.com/config/containers/logging/etwlogs/)**    |   Writes log messages as Event Tracing for Windows (ETW) events. Only available on Windows platforms.   |
| **[logentries](https://docs.docker.com/config/containers/logging/logentries/)** |                                Writes log messages to Rapid7 Logentries.                                |
<!-- vale on -->

### Configuring the Logging Driver

To configure the Docker daemon to a logging driver, you need to set the value of `log-driver` to the name of the logging driver in the daemon.json configuration file. Then you need to restart Docker for the changes to take effect for all the newly created containers. All the existing containers will remain as they are.

For example, let's set up a default logging driver with some additional options.

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "25m",
    "max-file": "10",
    "labels": "production_bind",
    "env": "os,customer"
  }
}
```

To find the current logging driver for the Docker daemon:

```bash
  {% raw %}
$ docker info --format '{{.LoggingDriver}}'

json-file
{% endraw %}
```

You can override the default driver by adding the `--log-driver` option to the docker run command that creates a container.

The following command will start using the Splunk driver:

```bash
docker run --log-driver splunk httpd
```

Modify the `daemon.json` file, to pass the address of the Splunk host to the driver:

```json
{
    "log-driver": "splunk",
    "log-opts": {
        "splunk-url": "172.1.1.1:11111"
    }
}
```

```bash
{% raw %}
$ docker inspect -f '{{.HostConfig.LogConfig.Type}}' <CONTAINER>

splunk
{% endraw %}
```

### Choosing the Delivery Mode of Log Messages From Container to Log Driver

Docker provides two modes for delivering log messages:

- **Blocking (default):** The container interrupts the application every time it needs to deliver a message to the driver. This will add latency in the performance of your application (for some drivers), but it'll guarantee that all the messages will be sent to the driver. Case in point, the json-file driver writes logs very quickly, therefore it's unlikely to cause latency. But drivers like `gcplogs` and `awslogs` open a connection to a remote server and so are more likely to block and cause latency.

- **Non-Blocking:** The container writes and stores its logs to an in-memory ring buffer until the logging driver is available to process them. This ensures that a high rate of logging will not affect application performance. It does not guarantee that all the messages will be sent to the driver. In cases where log broadcasts are faster than the driver processor, the ring buffer will soon run out of space. As a result, buffered logs are deleted to make space for the next set of incoming logs. The default value for `max-buffer-size` is 1 MB.

To change the mode:

```json
{
    "log-driver": "splunk",
    "log-opts": {
        "splunk-url": "172.1.1.1:11111",
        "mode": "non-blocking"
    }
}
```

## Understanding Logging Strategies

Docker logging effectively means logging the events of an application, host OS, and the respective Docker service. There are a few defined logging strategies you should keep in mind when working with containerized apps.

### 1. Application Logging

In this logging strategy, the application running in the containers will have its own logging framework. For example, a Node.js app could use a [`winston`](https://www.npmjs.com/package/winston) library to format and send the logs. With this approach, you have complete control over the logging event.

If you have multiple containers, you need to add an identifier at each container level, so you can uniquely determine the container and its respective logs. But as the size of the logs increases, this will start creating a load on the application process. Due to the transient nature of containers, the logs will be wiped out when a container is terminated or shut down.

To address this, you have two options:

- Configure steady storage to hold these logs, for example, disks/data volumes.
- Forward these logs to a log management solution.

### 2. Data Volumes

In this logging strategy, your container's directory gets links to one of the host machine directories that will hold all the data for you. Containers can now be terminated or shut down, and access logs from multiple containers.

A regular backup is a good idea in order to prevent data corruption or loss in case of a failure. But if you want to shift the containers on different hosts without loss of data, then the data volumes strategy will make that difficult.

### 3. Docker Logging Driver

Docker has a bunch of logging drivers that can be used in your logging strategy. The configured driver reads the data broadcast by the container's `stdout` or `stderr` streams and writes it to a file on the host machine. By default, the host machine holds the log files, but you can forward these events using the available drivers, like Fluentd, Splunk, and awslogs.

Note that the `docker log` command will not work if you use anything other than the `json-file` driver. And if log forwarding over a TCP connection fails or becomes unreachable, the containers will shut down.

### 4. Dedicated Logging Container

Here, you need to set up a dedicated container whose only job is to collect and manage logs within a Docker ecosystem. It'll aggregate, monitor, and analyze logs from containers and forward them to a central repository. The log dependency on the host machine is no longer an issue, and it's best suited for microservices architecture.

This strategy gives you the freedom to:

- Move containers between the hosts.
- Scale up by just adding a new container.
- Tie up all the various streams of log events.

### 5. Sidecar Logging Container

This logging strategy is similar to dedicated logging in that you have a container to hold logs, but here, each application has its own dedicated logging container (note that the application and its log container can be considered as a single unit). This opens up the flexibility of app-level logging customization. By adding custom identifiers, you can identify the specific container that broadcasts the log.

This is best suited for a complex system where each entity customizes the logs, making it popular in microservices deployment. Maintaining a container per application level will require additional resources for management and setup, so it's complex to implement. Also, you may end up losing data when a container from the unit becomes unserviceable.

### 6. Third-Party Logging Services

There are a lot of third-party logging services you can use according to your infrastructure and application needs, enabling you to aggregate, manage, and analyze logs and take proactive preventive actions as a result.

- **[Splunk](http://www.splunk.com/):** Splunk is built to scale from a single server to multiple data centers. It has built-in alerting and reporting, real-time search, analysis, and visualization, which helps you take action against malfunctions faster. It comes with a Splunk Enterprise on-premise deployment and Splunk Cloud. The free plan comes with 500 MB data per day, and the paid plan starts from $150 a month for a GB.
- **[Logstash](https://github.com/elastic/logstash):** Logstash is part of the [Elastic Stack](https://www.elastic.co/products) along with Beats, Elasticsearch, and Kibana. It's a server-side data processing pipeline that ingests data from a multitude of sources simultaneously, transforms it, and then sends it to your favourite "stash." Logstash has over 200 plugins for input, filter/transform, and output. It's free and open source.
- **[Fluentd](http://www.fluentd.org/):** Fluentd is an open-source data collector. Its performance has been well proven, handling 5 TB of daily data, 50,000 messages/sec at peak time. The main reason to use it would be performance. It's free and open source.
- **[PaperTrail](https://www.papertrail.com/):** PaperTrail is a simple and user-friendly service that provides a terminal-like experience. Once the data is sent over the syslog, you can perform tail and search operations with the PaperTrail UI. It's affordable for low volumes but becomes expensive for higher volume. It comes with a free 50 MB/month plan, and paid plans start at $7/month for 1 GB per month.
- **[Loggly](https://www.loggly.com/):** Loggly focuses on simplicity and ease of use for a DevOps audience. It's one of the more robust log analyzers. Primary use cases are for troubleshooting and customer support scenarios, and it provides richer visualizations and more parsing functionality than PaperTrail. It comes with a free 200 MB/day, and paid plans start at $79 a month for 1 GB per day ingestion with a 2 weeks retention.

## Limitations and Challenges of Docker Logging

Docker makes containerized application deployment easier, faster, and streamlines it with limited resources. Log management and analysis are handled differently with Docker as compared to a traditional system, which introduces a new set of challenges and limitations. From storing logs in a file system to forwarding them to a central repository, Docker logging has some pain points you'll need to overcome with a deeper understanding of Docker capability.

### The Only Compatible Driver Is json-file

The json-file driver is the only one that works with the `docker logs` command, a limitation of Docker logs. When you start using any other logging drivers, such as Fluentd or Splunk, the `docker logs` command shows an error and the Docker logs API calls will fail. Also, you won't be able to check the container logs in this situation.

### Docker Syslog Impacts Container Deployment

The reliable way to deliver logs is via Docker Syslog with TCP or TLS. But this driver needs an established TCP connection to the Syslog server whenever a container starts up. And the container will fail if a connection is not made.

  ```bash
  docker: Error response from daemon: Failed to initialize logging driver: dial tcp
  ```

Your container deployment will be affected if you face network problems or latency issues. And it's not recommended that you restart the Syslog server because this will drop all the connections from the containers to a central Syslog server.

### Potential Loss of Logs with Docker Syslog Driver

The Docker syslog driver needs an established TCP or TLS connection to deliver logs. Note that when the connection is down or not reachable, you'll start losing the logs until the connection reestablished.

### Multi-Line Logs Not Supported
  
Generally, either of two patterns is followed for logging: single-line per log or multiple lines with extended information per log, like stack traces or exceptions. But with Docker logging, this is a moot point, because containers always broadcast logs to the same output: `stdout`.

### Multiple Logging Drivers Not Supported

It's mandatory that you use only a single driver for all of your logging needs. Scenarios where you can store logs locally and push it to remote servers are not supported.

### Logs Can Miss or Skip
  
There's a rate limitation setting at the Docker end for journald drivers that takes care of the rate that logs get pushed. If it exceeds, then the driver might skip some logs. To prevent such issues, increase the rate limitation settings according to your logging needs.

## Conclusion

While Docker containerization allows developers to encapsulate a program and its file system into a single portable package, that certainly doesn't mean containerization is free of maintenance. Docker Logging is a bit more complex than traditional methods, so teams using Docker must familiarize themselves with the Docker logging to support full-stack visibility, troubleshooting, performance improvements, root cause analysis, etc.

As we have seen in this post, to facilitate logging, Docker offers logging drivers and commands in the platform which gives you the mechanisms for accessing the performance data and also provides plugins to integrate with third-party logging tools as well. To maximize the logging capabilities there are several methods and strategies which help in designing your logging infrastructure, but each comes with its advantages and disadvantages.

With this understanding of logging, containerization can be a powerful tool. Earthly is a containerized [continuous integration tool](https://earthly.dev/). If you've ever had to deal with flaky builds you should [check it out](https://earthly.dev/).
