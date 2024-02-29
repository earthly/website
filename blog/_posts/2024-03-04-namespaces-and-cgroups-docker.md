---
title: "How to Use Linux Namespaces and cgroups to Control Docker Performance"
categories:
  - Tutorials
toc: true
author: Avi Singh

internal-links:
 - how to use linux namespaces
 - how to use cgroups
 - linux namespaces to control docker performance
 - cgroups to control docker performance
 - how to use linux namespaces and cgroups
---

[Docker](https://www.docker.com/) is a popular containerization solution for packaging, distributing, and running applications in lightweight environments. However, with growing container density and workload variety comes increased pressure to control container performance. Thankfully, Linux offers powerful tools, including [namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/) and [control groups](https://kubernetes.io/docs/concepts/architecture/cgroups/) (cgroups), that enable fine-grained resource allocation and guarantee the optimal performance of each container.

In this article, you'll learn more about namespaces and cgroups and how to use them to control Docker performance.

## Understanding Linux Namespaces

Linux namespaces provide a mechanism for isolating system resources, enabling processes within a namespace to have their own view of the system, such as process IDs, network interfaces, and file systems. Docker uses namespaces to create isolated containers, each with its own set of resources. This ensures application separation and security.

The following are a few different types of namespaces:

* [PID namespace](https://en.wikipedia.org/wiki/Linux_namespaces#Process_ID_(pid))
* [Network namespace](https://en.wikipedia.org/wiki/Linux_namespaces#Network_(net))
* [Mount namespace](https://en.wikipedia.org/wiki/Linux_namespaces#Mount_(mnt))
* [Unix time-sharing (UTS) namespace](https://en.wikipedia.org/wiki/Linux_namespaces#UTS)
* [Inter-process communication (IPC) namespace](https://en.wikipedia.org/wiki/Linux_namespaces#Inter-process_Communication_(ipc))
* [User namespace](https://en.wikipedia.org/wiki/Linux_namespaces#User_ID_(user))
* [Time namespace](https://en.wikipedia.org/wiki/Linux_namespaces#Time_Namespace)
* [`cgroup` namespace](https://en.wikipedia.org/wiki/Linux_namespaces#Control_group_(cgroup)_Namespace)

Namespaces in Linux provide a way to isolate and virtualize system resources, thus enhancing security by preventing processes in one namespace from directly interacting with processes in another namespace.

Namespaces increase security by providing a level of isolation that prevents unintended interactions between processes. This isolation is particularly valuable in containerization and virtualization scenarios, where multiple applications or services share the same host system but must be kept separate for security reasons.

## Understanding `cgroups`

cgroups are a Linux kernel feature that enable the management and partitioning of system resources by controlling the resources for a collection of processes. Administrators can use cgroups to allocate resources, set limits, and prioritize processes. Docker utilizes cgroups to control and limit the resources available to containers.

Different types of available cgroups include [CPU cgroup](https://kernel.googlesource.com/pub/scm/linux/kernel/git/glommer/memcg/+/cpu_stat/Documentation/cgroups/cpu.txt), [memory cgroup](https://kernel.googlesource.com/pub/scm/linux/kernel/git/glommer/memcg/+/cpu_stat/Documentation/cgroups/memory.txt), [block I/O cgroup](https://kernel.googlesource.com/pub/scm/linux/kernel/git/glommer/memcg/+/cpu_stat/Documentation/cgroups/blkio-controller.txt), and [device cgroup](https://kernel.googlesource.com/pub/scm/linux/kernel/git/glommer/memcg/+/cpu_stat/Documentation/cgroups/devices.txt).

While cgroups are not explicitly designed for security, they play a crucial role in controlling and monitoring the resource usage of processes.

Although namespaces and cgroups may appear similar in definition, they are fundamentally different and serve different purposes. Namespaces perform isolation by creating separate environments for processes that prevent one process from accessing or affecting other processes and/or the system. In contrast, cgroups distribute and limit resources like CPU, memory, and I/O among groups of processes. Often, namespaces and cgroups are used together for process isolation and resource management.

Now that you know more about namespaces and cgroups, it's time to learn how to use them to control Docker performance.

All the code for this article is available in [this GitHub repo](https://github.com/avidunken/namespaceandcgroup/blob/main/commands.md).

## How to Use Namespaces to Control Docker Performance

To decrease a container's attack surface, Docker offers the `--user` option. The default user inside the containers is the root user. With the `--user` flag, you can specify a non-root user and group to run the first process in containers. This lets you limit the potential impact of any security vulnerabilities.

Using the `--user` option may hinder application functionality since some applications require elevated privileges to operate efficiently. When this occurs, your container configuration or app configuration may need to be altered accordingly to provide those permissions and grant the required privileges.

This is where a user namespace can help. By default, Docker runs containers with identical user and group IDs as their host system, which means that if an attacker gains entry through any one container in the system, they could potentially escalate their privileges. User namespaces can help mitigate such attacks by remapping the user IDs (UIDs) and group IDs (GIDs) used in the inside container with the outside container.

To better understand this concept, let's use the user namespace to isolate the containers for security purposes.

## How to Use `namespaces` With Docker

In this scenario, you'll learn about some of the advantages of namespaces in Docker. Run the following command to create a file in the host machine and make it readable to only the root user:

~~~{.bash caption=">_"}
echo "This is a super sensitive file" | sudo tee /secret
sudo chmod 600 /secret
~~~

Let's pretend that the file `/secret` is a very sensitive file that should never be accessed by anyone other than the root. But, what happens when you mount the host filesystem in a Docker container? Let's find out. Run the following command to start a busybox container and mount the host filesystem to it:

~~~{.bash caption=">_"}
sudo docker run -it --rm -v /:/host busybox /bin/sh
~~~

Then, try to access the sensitive file:

~~~{.bash caption=">_"}
$ cat /host/secret
This is a super sensitive file
~~~

As you can see, the root user in the Docker container has UID 0. When this user (with UID 0) tries to access the file in the host filesystem owned by the root user (who also has UID 0) the system happily obliges. But, this is a huge security risk as the Docker container can now freely read or modify any file on the host machine.

To prevent this, you need to make use of namespaces.

First, make sure that your Linux kernel supports user namespaces. To do so, [find the configuration file for your kernel](https://www.baeldung.com/linux/kernel-config) and use grep to search for `CONFIG_USER_NS`. The following command is an example of the Ubuntu kernel:

~~~{.bash caption=">_"}
grep -E '^CONFIG_USER_NS=' /boot/config-$(uname -r)
~~~

The following output confirms that your kernel supports user namespaces:

~~~{ caption="Output"}
CONFIG_USER_NS=y
~~~

Next, open or create the Docker daemon configuration file (usually located at `/etc/docker/daemon.json`) and add the following configuration that sets up user namespaces with default remapping:

~~~{.json caption="daemon.json"}
{
  "userns-remap": "default"
}
~~~

Restart the Docker daemon to apply the changes:

~~~{.bash caption=">_"}
sudo systemctl restart docker
~~~

Run the container again:

~~~{.bash caption=">_"}
sudo docker run -it --rm -v /:/host busybox /bin/sh
~~~

Try to read the file:

~~~{.bash caption=">_"}
$ cat /host/secret
~~~

This time, you'll be faced with a `Permission denied` error.

To better understand what is happening behind the scenes, execute the following command in interactive mode to run a Docker container:

~~~{.bash caption=">_"}
docker run -it nginx sleep 300
~~~

Your output will look like this:

~~~{ caption="Output"}
latest: Pulling from library/nginx
af107e978371: Pull complete 
336ba1f05c3e: Pull complete 
8c37d2ff6efa: Pull complete 
51d6357098de: Pull complete 
782f1ecce57d: Pull complete 
5e99d351b073: Pull complete 
7b73345df136: Pull complete 
Digest: sha256:2bdc49f2f8ae8d8dc50ed00f2ee56d00385c6f8bc8a8b320d0a294d9e3b49026
Status: Downloaded newer image for nginx:latest
~~~

After running the container, check to see if the container is up and running:

~~~{.bash caption=">_"}
docker ps
~~~

In this scenario, you're running an Nginx container and executing the sleep command inside it.

Run the following command to list all currently running processes and filter the results to only show lines containing the word "sleep":

~~~{.bash caption=">_"}
ps -aux | grep sleep
~~~

The `ps` command is used to provide information about processes.

Your output will look like this:

~~~{ caption="Output"}

osboxes     7216  0.0  0.4 1329172 24576 pts/0   Sl+  13:39   0:00 docker run -it nginx sleep 300
231072      7279  0.0  0.0   2484  1280 pts/0    Ss+  13:39   0:00 sleep 300
osboxes     7329  0.0  0.0  17732  2560 pts/1    S+   13:40   0:00 grep --color=auto sleep
~~~

Observe that one `sleep 300` process shows up in the list of processes. It is owned by the user with the UID 231072 (this UID may be different for you). Where is this user coming from? Use the following command to look at the file `/etc/subuid`:

~~~{.bash caption=">_"}
cat /etc/subuid
~~~

Your output should look like this:

~~~{ caption="Output"}
osboxes:100000:65536
ansible:165536:65536
dockremap:231072:65536
~~~

What this tells us is that Docker creates a default user named `dockremap` with host UID 231072. This user is mapped to the UID 0 inside Docker containers. Any process started by the root user in the container is owned by the UID 231072 on the host, thus protecting it from privilege escalation.

Next, use the `docker info` command to verify that user namespace support is enabled correctly:

~~~{.bash caption=">_"}
sudo docker info
~~~

Your output should look like this:

~~~{ caption="Output"}
Client:
 Context:    default
 Debug Mode: false
 Plugins:
  buildx: Docker Buildx (Docker Inc.)
    Version:  v0.10.4
    Path:     /usr/libexec/docker/cli-plugins/docker-buildx
  compose: Docker Compose (Docker Inc.)
    Version:  v2.17.3
    Path:     /usr/libexec/docker/cli-plugins/docker-compose

Server:
 Containers: 2
  Running: 0
  Paused: 0
  Stopped: 2
 Images: 1
 Server Version: 23.0.6
 Storage Driver: overlay2
  Backing Filesystem: extfs
  Supports d_type: true
  Using metacopy: false
  Native Overlay Diff: true
  userxattr: false
 Logging Driver: json-file
 Cgroup Driver: systemd
 Cgroup Version: 2
 Plugins:
  Volume: local
  Network: bridge host ipvlan macvlan null overlay
  Log: awslogs fluentd gcplogs gelf journald json-file local logentries splunk syslog
 Swarm: inactive
 Runtimes: io.containerd.runc.v2 runc
 Default Runtime: runc
 Init Binary: docker-init
 containerd version: 3dce8eb055cbb6872793272b4f20ed16117344f8
 runc version: v1.1.7-0-g860f061
 init version: de40ad0
 Security Options:
  apparmor
  seccomp
   Profile: builtin
  userns
  cgroupns
 Kernel Version: 6.2.0-26-generic
 Operating System: Ubuntu 22.04 LTS
 OSType: linux
 Architecture: x86_64
 CPUs: 5
 Total Memory: 5.744GiB
 Name: osboxes
 ID: 80a2b682-9225-423a-bd2e-a0a3c61e8cf0
 Docker Root Dir: /var/lib/docker/231072.231072
 Debug Mode: false
 Registry: https://index.docker.io/v1/
 Experimental: false
 Insecure Registries:
  127.0.0.0/8
 Live Restore Enabled: false
~~~

The numbers at the end of the `Docker Root Dir` line indicate that the daemon runs inside a user namespace. The numbers should match the subordinate user ID of the `dockremap` user as defined in the `/etc/subuid` file.

## How to Use cgroups to Control Docker Container Resources

Now that you know how you can use namespaces to increase security, let's use cgroups to configure resource limitations. In this example, you'll run a Docker container with CPU limits.

Let's take a look at what cgroups are set up when you run a container. But, before that, you need to know if your system is using cgroup v1 or v2. The easiest way to find that out is to look for the file `/sys/fs/cgroup/cgroup.controllers`. If it exists, you're using cgroup v2, otherwise, you're using cgroup v1.

Run the `nginx` container and note the container ID from the output:

~~~{.bash caption=">_"}
$ docker run -d nginx
~~~

To find the cgroups for this container, you'll need to look into the following locations, based on the cgroup version and the cgroup driver:

* `/sys/fs/cgroup/memory/docker/<container_id>/` on cgroup v1, `cgroupfs` driver (default)
* `/sys/fs/cgroup/memory/system.slice/docker-<container_id>.scope/` on cgroup v1, `systemd driver`
* `/sys/fs/cgroup/docker/<container_id>/` on cgroup v2, `cgroupfs` driver
* `/sys/fs/cgroup/system.slice/docker-<container_id>.scope/` on cgroup v2, `systemd` driver (default)

Here, you can find out different metrics for the container. For example, you can read the max CPU allocated to this container by reading the `cpu.max` file in this directory:

~~~{.bash caption=">_"}
max 100000
~~~

This implies that this container is allowed to consume the maximum available CPU on the host. Let's limit it to half of one CPU. First, kill the container and recreate it with the `--cpus` option:

~~~{.bash caption=">_"}
docker run --cpus 0.5 -d nginx
~~~

The `cpu.max` file should show the following:

~~~{ caption="Output"}
50000 100000
~~~

This shows that the container is only allowed 0.5 CPUs. You can adjust the `--cpus` value according to your desired CPU utilization.

If you want to run a Docker container with memory limits using cgroups, you can use the `--memory` option with the `docker run` command. The following example uses the [official Nginx image](https://hub.docker.com/_/nginx) from Docker Hub:

~~~{.bash caption=">_"}
docker run -d --name new-container --memory=256M ubuntu sleep infinity
~~~

In this command, `-d` makes the container run in the background, and `--name new-container` assigns a name to the container. `--memory 256M` limits the container to use a maximum of 256 mebibytes of memory, and `ubuntu` is the image that's being used. `sleep infinity` tells the Docker command to run.

Now, run `docker ps`. You should see that a container named "new-container" is up and running:

~~~{ caption="Output"}

CONTAINER ID   IMAGE     COMMAND            CREATED          STATUS          PORTS     NAMES
d67613c74bd6   ubuntu    "sleep infinity"   26 seconds ago   Up 25 seconds             new-container
~~~

To verify that the memory limits are applied, run the following `docker stats` command:

~~~{.bash caption=">_"}
docker stats d67613c74bd6
~~~

Your output will look like this:

~~~{ caption="Output"}

CONTAINER ID   NAME            CPU %     MEM USAGE / LIMIT   MEM %     NET I/O       BLOCK I/O   PIDS
d67613c74bd6   new-container   0.00%     388KiB / 256MiB     0.15%     3.42kB / 0B   0B / 0B     1
~~~

You can see the memory limit for this container is now set to 256 MiB.

To get real-time statistics for the running container, including CPU and memory usage, run the following command:

~~~{.bash caption=">_"}
docker stats new-container --no-stream --format "  {% raw %}{{ json . }}{% endraw %}" \
| python3 -m json.tool
~~~

Your output will look like this:

~~~{ caption="Output"}
{
    "BlockIO": "0B / 0B",
    "CPUPerc": "0.00%",
    "Container": "new-container",
    "ID": "d67613c74bd6",
    "MemPerc": "0.15%",
    "MemUsage": "388KiB / 256MiB",
    "Name": "new-container",
    "NetIO": "3.6kB / 0B",
    "PIDs": "1"
}
~~~

In this output, you can see that Docker has applied a memory limit of 256 MiB in the `"MemUsage"` field.

## Conclusion

Mastering Linux namespaces and cgroups is essential for optimizing Docker performance. With the help of these features, administrators can fine-tune resource allocation, enhance security, and ensure the smooth operation of containerized applications.

As the landscape of containerization continues to evolve, a solid grasp of Linux namespaces and cgroups empowers users to harness the full potential of Docker and deliver high-performance, scalable applications. In this article, you learned how namespaces and cgroups are used by Docker, and how you can utilize namespaces for container isolation and cgroups for limiting and monitoring resource usage.

{% include_html cta/bottom-cta.html %}

## Outside Article Checklist

* [ ] Create header image in Canva
