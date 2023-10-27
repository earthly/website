---
title: "A Beginner's Guide to Debugging Docker Containers"
categories:
  - Tutorials
toc: true
author: Prince Onyeanuna
editor: Mustapha Ahmad Ayodeji

internal-links:
 - guide to debug
 - debugging docker containers
 - debugging docker
 - docker containers
 - encountering bugs
excerpt: | 
     Debugging Docker containers can be frustrating. Luckily, Docker provides several commands that make managing and troubleshooting containers easy. In this article, we'll walk you through several real world scenarios and show you some tips and techniques for debugging Docker containers.
last_modified_at: 2023-08-14
---

**We're [Earthly](https://earthly.dev/). We simplify building software with containerization. This article discusses how you can debug Docker containers for different scenarios. However, if you are curious about getting better build times by combining ideas from Makefile and Dockerfile? [Check us out.](https://earthly.dev/)**

Debugging Docker containers can be frustrating. Luckily, Docker provides several commands that make managing and troubleshooting containers easy. In this article, we'll walk you through several real world scenarios and show you some tips and techniques for debugging Docker containers.

## Prerequisites

Although this guide will take a beginner-friendly approach, you must have Docker installed and configured correctly on your operating system. Additionally, you would need the following:

- Basic knowledge of Docker, such as pulling and pushing Docker images, starting and stopping containers, etc.
- Basic understanding of the command line, such as executing commands and primary navigation.

With all these in check, you're sure to make the most out of this article by following the examples, which will give you a good grip on these debugging techniques.

## Docker Debugging Landscape

Before moving into the various debugging techniques and their respective Docker commands, it is essential to understand some unique challenges that arise from debugging containers. These challenges include Docker containers' short-lived (ephemeral) nature, isolated environments, and limited visibility. Understanding the debugging landscape will help you effectively troubleshoot containerized applications.

### Ephemeral Nature of Containers

Docker containers have numerous features that make them highly popular. Some of these features include being lightweight, portable, and disposable. That means you can start, stop and destroy Docker containers with ease.

Although advantageous, these features mean containers would be short-lived, making it challenging to capture and analyze the state of a container at any point in time.

### Isolated Environments

Part of the design of Docker containers is their isolation from the underlying host system and other containers. This feature makes it more secure and improves encapsulation; however, debugging can be complex with this design.

### Limited Visibility

Imagine a scenario where your application comprises multiple interconnected containers. If one container is not working correctly, it may impact the entire application's functionality. However, pinpointing the exact cause of the issue becomes a puzzle due to limited visibility from the host system into individual containers making it challenging to observe internal states, logs, and network interactions.

## Exploring Essential Docker Debugging Commands

The following sections contain various scenarios where debugging and troubleshooting commands are helpful.

### Inspecting Container Status and Logs

One of the essential tasks in debugging Docker containers is gaining insight into their status and examining the logs they generate. This information can help you understand how containers are running, detect any errors or issues, and pinpoint potential areas of concern.

To inspect the status of running containers, we will use the following Docker commands:

- **[Docker ps](https://docs.docker.com/engine/reference/commandline/ps/)**: This command lists all the containers running on your system. They also provide certain information about these containers, which include the container ID, images name, and status. With this command, you can quickly view any container you deploy.

  By simply running `docker ps`, you can easily see the details of all containers. You can also add an option `-a` or `--all` to see all containers (running and stopped containers).

   ~~~{.bash caption=">_"}
   docker ps # Only for running containers 
   docker ps -a # For all running or stopped containers
   ~~~

- **[Docker logs](https://docs.docker.com/engine/reference/commandline/logs/)**: Using this command, you can retrieve important information such as application output, error messages, and other relevant details from a Docker container. During troubleshooting issues, it is crucial to examine these logs to identify errors and understand the application's behavior.
  
   You can use this command by attaching the container ID to it:

   ~~~{.bash caption=">_"}
   docker logs [container]
   ~~~

- **[Docker inspect](https://docs.docker.com/engine/reference/commandline/inspect/)**: To obtain detailed information about a container, utilize the Docker inspect command. The command generates an output in an object format that includes all relevant details about the container, including its creation date and shell.

  The syntax to use this command is as follows:

   ~~~{.bash caption=">_"}
   docker docker_object inspect [OPTIONS] NAME|ID [NAME|ID...]
   ~~~

<div class="notice--info">
`docker_object` refers to the specific Docker object you want to inspect, such as a container, image, network, or volume. You replace `docker_object` with the specific object you want to inspect, for example, container, image, network, or volume.
</div>

Since the focus is on debugging Docker containers, the syntax would be as follows:

~~~{.bash caption=">_"}
docker container inspect [container]
~~~

You should replace the `container` placeholder with either the name or the ID of the specific Docker container you want to inspect.

**Scenario**: Suppose you have deployed multiple containers for your web application, including a web server and a database container. However, you notice that your application throws an error saying **no database connection was found**. Using the following commands above, this is how you would troubleshoot the issue.

1. Using `docker ps`, check whether the database container runs successfully. If not, rerun the docker image to restart the container. If it is, copy its container ID and proceed with further debugging.

   <div class="wide">
   ![**Figure 1**. Docker ps output]({{site.images}}{{page.slug}}/iWzZGFO.png)
   </div>

2. Use the `docker logs` command with the container ID to view the logs of the database container. Make sure to read slowly on each line for error messages from the database connection.
  
   ~~~{.bash caption=">_"}
   docker logs [container]
   ~~~

   <div class="wide">
   ![**Figure 2**. Docker logs output]({{site.images}}{{page.slug}}/gcz4NwP.png)
   </div>

3. After reading the error messages, you would identify some issues such as incorrect database credentials or network configuration problems. Apply the necessary changes, and restart your container.

Although the commands mentioned may be helpful in solving some issues, it's important to note that more complex problems may require additional tools. You must gain knowledge and proficiency in using these tools to handle such situations effectively.

### Accessing Container Shell

Most times, while debugging, there is just so little you can do outside a running container. However, Docker provides commands allowing you to access any container's shell or command line. This ability can be very efficient during troubleshooting, allowing you to interact with the container's environment, execute commands, and investigate issues directly.

You can use the following commands to access the shell of any container:

- **[Docker exec](https://docs.docker.com/engine/reference/commandline/exec/)**: There are two ways to access the command line of a container using this command. They are as follows:

    1. **Executing Commands Directly:** This method of using `docker exec` involves executing commands directly into a running container without the `-it` flags. The `it` flag means the following:

       - `i` (interactive): It enables you to interact with the container, for example, by providing input to the command running inside the container.
  
       - `t` (terminal): This command allocates a terminal for the container.

        <div class="notice--info">
        By using the `-it` flag, you can run interactive commands inside a Docker container, enabling you to interact with the running process and see its output as if you were working directly in a terminal.
        </div>

        This method allows you to run a specific command within the container's environment and receive the output directly in your terminal. It is helpful for one-off commands or situations where you don't require continuous interaction with the container.

        To execute a command directly within a container, use the following syntax:

        ~~~{.bash caption=">_"}
        docker exec [container] [command]
        ~~~

        Replace `container` with the container's ID or name and `command` with the command you want to execute.

        For example, you might use the following command to list the files in a container:

        ~~~{.bash caption=">_"}
        docker exec [container] ls
        ~~~

    2. **Starting an Interactive Shell:** The second method involves starting an interactive shell within a running container using the `docker exec` command with the `-it` flags. This approach allows you to establish an interactive session, like opening a shell directly within the container. It provides a more immersive experience, allowing you to execute multiple commands, navigate the file system, and perform complex troubleshooting tasks.

        To begin an interactive shell in a container, use this syntax:

        ~~~{.bash caption=">_"}
        docker exec -it [container] [shell]
        ~~~

        For example, you might use the following command to start an interactive shell session in a container:

        ~~~{.bash caption=">_"}
        docker exec -it [container] sh
        ~~~

        This command starts an interactive shell using the sh command within the container.

Both methods have advantages and can be utilized based on your specific debugging needs. Using the `docker exec` command directly might be sufficient if you only need to execute a single command. However, if you need continuous interaction and exploration within the container, starting an interactive shell using `docker exec -it` is the way to go.

- **[Docker attach](https://docs.docker.com/engine/reference/commandline/attach/)**: In addition to the `docker exec` command discussed earlier, there's another useful command called `docker attach` that allows you to attach your terminal to a running container's shell. This command is particularly helpful when interacting with a container already running and viewing its output in real time.

    The `docker attach` command lets you connect your terminal directly to a running container and interact with its standard input (`stdin`), output (`stdout`), and error (`stderr`). It's like **attaching** your terminal to the container, allowing you to see its ongoing output and interact with the running processes.

    To use `docker attach`, you need to know the ID or name of the container you want to connect to. Once you have that information, you can execute the following command:

   ~~~{.bash caption=">_"}
   docker attach [container]
   ~~~

**Scenario**: Suppose you are running a Docker container hosting a web application but encounter issues due to misconfigured application settings or script errors. To troubleshoot and resolve this problem, you can utilize the `docker exec`, and `docker attach` commands. Follow the steps below:

1. Using `docker ps`, identify the container running the web application. Make sure to get the container ID or name.

2. Observe the application output. To observe the application's output in real-time, you can attach it to the container using the `docker attach` command:
  
   ~~~{.bash caption=">_"}
   docker attach [container]
   ~~~

   <div class="wide">
   ![**Figure 3** docker ps and docker attach command]({{site.images}}{{page.slug}}/Beoz5Gf.png)
   </div>

   This connects your terminal to the container's output stream, allowing you to see any print statements or error messages generated by the application. Take note of any relevant error messages or unexpected behavior displayed in the terminal.

3. Debug the application. You can now debug the application with the container's shell attached. Examine the error messages, log files, or any other available information to identify the root cause of the issue.

   You can execute commands within the attached shell to investigate further:

   ~~~{.bash caption=">_"}
   docker exec -it [container] /bin/sh
   ~~~

   ~~~{ caption="Output"}
   # ls
   bin build cgi-bin conf error htdocs icons include logs modules
   ~~~

   This command gives you access to the shell of the container, where you can debug errors according to the logs thrown by the application.

4. Make necessary corrections. Make the necessary corrections within the container based on the errors or misconfigurations you identified. Edit configuration files, update scripts, or modify environment variables as required to rectify the issue.

Using the `docker exec` and `docker attach` commands, you can troubleshoot and resolve issues related to misconfigured application settings or script errors within a Docker container. These commands enable you to interact with the container's shell, execute commands, and observe real-time output, facilitating effective debugging and resolution of such issues.

### Examining Resource Usage and Performance

When working with Docker containers, monitoring their resource usage and performance is essential to ensure optimal operation. This section will teach you various Docker commands to examine resource usage and identify performance bottlenecks.

The following commands are essential in monitoring resource usage:

- **[Docker stats](https://docs.docker.com/engine/reference/commandline/stats/)**: This command provides a continuously updating table showing the resource consumption of each container. It displays CPU and memory utilization, network I/O, and container uptime. You can quickly identify the problematic container and investigate further by running docker stats.

   By running `docker stats`, you can easily get this table. The syntax for this command is as follows:

   ~~~{.bash caption=">_"}
   docker stats
   ~~~

- **[Docker top](https://docs.docker.com/engine/reference/commandline/top/)**: The `docker top` command lets you view all the processes inside a container. It displays the running processes' details, such as the process ID (PID), CPU and memory usage, and the associated command.

   To utilize this command, run:

   ~~~{.bash caption=">_"}
   docker top [container]
   ~~~

   Replace `container` with the container's name or ID.

**Scenario**: Imagine you have a container running a database server and notice a significant increase in CPU usage. By executing `docker stats` and `docker top` command together, you can monitor the container's overall resource usage while identifying the specific processes within the container that is responsible for the high CPU consumption.

Below are the steps you would take to troubleshoot this issue:

1. To keep track of the resource usage of your running containers, begin by entering the command `docker stats` into your terminal. This will display a continuously updating table showing the resource consumption of each container:

   ~~~{.bash caption="Output"}
   
   CONTAINER ID  NAME                  CPU %    MEM USAGE / LIMIT    MEM %   NET I/0            BLOCK I/O             PIDS
   97c26147f9a3  my-running-app        0.00%    8.742MiB / 965.7MiB  0.91%   3.28kB / 3.68kB    4.03MB / 4.1kB  82
   6891d44e253   optimistic_dubinsky   0.41%    352.1MiB / 965.7MiB  36.46%  2.04kB / 0B        83.5MB / 267MB   37
   ~~~

2. Identify the container exhibiting abnormal CPU or memory usage based on the information provided by `docker stats` command. Take note of the container's name or ID.

   With the container name or ID in hand, execute the following command to inspect the processes inside the container.

   ~~~{.bash caption=">_"}
   docker top [container]
   ~~~

   Replace `container` with the name or ID of the problematic container.

   ~~~{ caption="Output"}
   UID      PID   PPID  STIME  TTY  TIME      CMD
   lxd      2523  2502  21:06  -    00:00:38  mysqld
   ~~~

3. Review the output of docker top to identify any processes within the container that consume excessive resources. Look for processes with high CPU or memory usage, as well as the associated command that is being executed.

4. Analyze the resource-intensive processes and investigate the root cause of their resource consumption. This may involve examining application code, configuration files, or debugging scripts to identify misconfigurations or inefficiencies.

5. Once you have identified the underlying issue, take appropriate steps to address it. This may involve optimizing code, adjusting application settings, or resolving script errors.

6. Monitor the container's resource usage using docker stats again to verify that the problem has been resolved. Ensure that the CPU and memory utilization return to expected levels.

By following these steps, you can effectively use `docker stats` and `docker top` together to monitor resource usage and identify resource-intensive processes within containers.

### Debugging Network Connectivity

Learning [Docker networking](/blog/docker-networking/) can be tricky. Even with a solid understanding of the fundamentals, debugging Docker network connectivity errors can be frustrating. In this section, we'll take a look at some strategies you can use next time you encounter a network error.

You can use the following commands to resolve network difficulties:

- **[Docker network inspect](https://docs.docker.com/engine/reference/commandline/network_inspect/)**: The `docker network inspect` command allows you to analyze Docker networks and their configuration. It provides detailed information about network settings, IP addresses, and connected containers. To utilize this command, run:
  
   ~~~{.bash caption=">_"}
   docker network inspect [network]
   ~~~

   To inspect a specific network, replace `network` with its name or ID.

- **Docker exec**: The `docker exec` command, as you learned earlier, allows you to execute commands within a running container. It can also be utilized in two ways to debug network connectivity issues:

   1. `ping`: The `docker exec` command, combined with the `ping` utility, allows you to verify network connectivity between containers and external hosts:

      ~~~{.bash caption=">_"}
      docker exec -it [container] ping [host]
      ~~~

      To test a specific container, replace `container` with its name or ID. Similarly, replace `host` with the hostname or IP address of the target host.

   2. `nc`: The `docker exec` command, combined with the [nc](https://www.tutorialspoint.com/unix_commands/nc.htm) utility, allows you to check connectivity to a specific port on a host. To perform a check on the connection between a container and a specific host and port, use the command below:

      ~~~{.bash caption=">_"}
      docker exec -it [container] nc -zv [host] [port]`
      ~~~

      To test a specific container, replace `container` with its name or ID. For the target host, use the hostname or IP address and replace `host`. Lastly, specify the port number by replacing `port`.

      By using the `docker exec` command in different ways, you can effectively debug network connectivity problems in your Docker environment. Whether you need to check connectivity to a specific host or verify port access, these commands provide valuable insights into your containerized applications' network behavior.

**Scenario**: Let's say you are working on a microservices-based application that consists of multiple Docker containers. One of the containers is a frontend web server that needs to communicate with a backend database container. However, you encounter network connectivity issues, and the web server cannot establish a connection with the database.

To troubleshoot and resolve the network problem, you can follow these steps:

1. Verify Docker network configuration: Start by inspecting the Docker network associated with the containers using the following command:
  
   ~~~{.bash caption=">_"}
   docker network inspect [network]
   ~~~

      Replace `network` with the name of the network your containers are connected to.

      <div class="wide">
      ![**Figure 4**. Docker network inspect command]({{site.images}}{{page.slug}}/Ag0u34D.png)
      </div>

      This command will provide detailed information about the network, including the container configurations, IP addresses, and more. Ensure that the front and backend containers are connected to the same network.

2. Check host and port availability
  
   ~~~{.bash caption=">_"}
   docker exec -it 192df0366472 nc 54.91.248.13 8080
   ~~~

   ~~~{ caption="Output"}
   Connection to 54.91.248.13 8080 port [tcp/*] succeeded!
   ~~~

   Replace `container` with the name or ID of the frontend container, `host` with the IP address or hostname of the backend database container, and `port` with the port number the database is running on.

   This command will check if the frontend container can connect to the backend container on the specified host and port. It will provide information on whether the port is open and accessible.

   Ensure that the host and port are correctly specified and that no firewall or network configuration issues block the connection.

3. Verify Network Connectivity: Next, check the network connectivity between the containers by running the command:
  
   ~~~{.bash caption=">_"}
   docker exec -it [container] ping [host]
   ~~~

   <div class="wide">
   ![**Figure 5**. ping command]({{site.images}}{{page.slug}}/fTQij9Z.png)
    </div>

   Replace `container` with the name or ID of the frontend container and `host` with the IP address or hostname of the backend database container.

   This command will send [ICMP echo](https://aws.amazon.com/what-is/icmp/) also known as ping requests, from the frontend container to the backend container. It helps determine if there are any network connectivity issues, such as packet loss or unreachable hosts.  

   <div class="notice--info">
   Internet Control Message Protocol (ICMP) is a network protocol used for troubleshooting purposes. When a device or computer sends an ICMP echo request (ping) to another device, it is essentially asking for a response to confirm the target device's availability and round-trip time.
   </div>

4. Analyze the ping results to identify connectivity problems like high latency or timeouts. Ensure that the frontend container can reach the backend container through the network.

By combining the `docker exec -it nc` command to check host and port availability, the `docker exec -it ping` command to verify network connectivity, and the `docker network inspect` command to examine the network configuration, you can diagnose and troubleshoot network-related issues between Docker containers.

<div class="notice--info">
If you like to learn more about docker networking, you can checkout [this article](https://earthly.dev/blog/docker-networking/)
</div>

## Conclusion

This comprehensive guide has explored essential Docker commands for debugging containers and provided practical scenarios to demonstrate their usage. By adopting a systematic approach to debugging, developers can effectively identify and resolve issues in their Dockerized environments.

We began by understanding the challenges of debugging Docker containers, including their ephemeral nature and limited visibility. Recognizing the need for a systematic approach, we delved into essential Docker debugging commands. We learned how to inspect container status and logs, access container shells, examine resource usage and performance, and debug network connectivity. Through clear explanations and real-world scenarios, we demonstrated the practical application of these commands in troubleshooting common Docker-related problems.

By following the techniques and commands outlined in this guide, developers can gain a comprehensive understanding of Docker debugging and enhance their troubleshooting skills. Remember to approach debugging systematically, using commands such as `docker ps`, `docker logs`, `docker exec`, `docker attach`, `docker stats`, `docker top`, `docker network inspect`, `docker exec -it ping`, and `docker exec -it nc`. With this knowledge, developers can confidently debug Docker containers, resolve issues efficiently, and ensure the smooth operation of their containerized applications.

{% include_html cta/bottom-cta.html %}
