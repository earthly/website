---
title: "How to Use Docker Namespaces to Isolate Containers"
categories:
  - Tutorials
toc: true
author: Christoph Berger

internal-links:
 - use docker namespaces
 - isolate containers by using docker namespaces
 - isolating containers with docker namespaces
 - isolating containers
 - using docker namespaces
---

Containers are the Gutenberg press of the IT world: an innovation that profoundly improves the way applications get deployed and managed during runtime.

The primary purpose of a container is to provide applications with a well-defined, replicable, and isolated environment. If an application expects to run on an Alpine Linux system, a container can provide the app with the appropriate Alpine Linux libraries, commands, and system services. This container can run on a Debian or Arch Linux host, and the application inside can still use an Alpine Linux system. Moreover, the application sees restricted versions of the process ID space, the file system, the network, and other OS resources.

These restrictions help isolate containerized apps from each other, which is an important aspect not only from a security perspective but also when it comes to avoiding resource conflicts. (Imagine two processes trying to reserve the same network port.)

To isolate apps, Docker uses Linux namespaces. In short, Linux namespaces divide global system resources into distinct compartments. For instance, a process that is created with a dedicated network namespace can access any network port without coming into conflict with processes in other network namespaces.

In this article, you'll learn more about Linux namespaces and how Docker uses them to achieve process isolation.

## Demystifying Linux Namespaces

Processes need access to resources and contexts provided by the operating system, including the file system, network ports, user context, and shared memory. These resources and contexts are globally available to all processes, which causes two problems:

1. Two processes can come into conflict over requesting an exclusive resource, like a particular network port.
2. Processes might have access to information that belongs to other processes.

Linux namespaces solve both problems. A namespace restricts access to resources and virtualizes these resources. For example, when a process runs inside a network namespace, it can always access port 80, as if that port were exclusively reserved for that process. However, this port is only virtual. The Linux kernel maps this virtual port to a different port at the OS level. In the same manner, a process can get a restricted view of the file system, running processes, and more.

### The History of Namespaces

The idea of namespaces is not new. Before Linux, the operating system [Plan 9 from Bell Labs](https://p9f.org/) had a [concept of namespaces](https://web.archive.org/web/20140906153815/http://www.cs.bell-labs.com/sys/doc/names.html) that controlled access to the file system. Since all system resources in Plan 9 are mapped into the file system, Plan 9 namespaces effectively control access to any resource, not just files and folders.

Another early approach to namespaces is the [Jails](https://docs.freebsd.org/en/books/handbook/jails/) concept from [FreeBSD](https://www.freebsd.org/) and other BSD derivatives. Jails virtualize access to the file system, the set of users, and the network, effectively partitioning a BSD system into several independent virtual systems.

### Different Types of Linux Namespaces

Linux utilizes various types of namespaces for controlling access to specific resource types, including the following:

- The **process ID (PID) namespace** isolates a process from the global list of process IDs. A process started with a PID namespace sees itself as the only process on the system unless it spawns subprocesses that share the parent's PID namespace.
- The **network namespace** provides a process with its own view of network interfaces and routing tables. The process can create virtual Ethernet interfaces to connect to the global network namespace.
- The **Unix time-sharing system (UTS) namespace** allows a process to have its own host name and domain name.
- The **user namespace** restricts the users and groups a process can see. User IDs and group IDs can be remapped, for instance, so that a root user inside the namespace is mapped to an unprivileged user outside the namespace.
- The **mount namespace** manages the file mounts that a process can access.
- The **interprocess communication (IPC) namespace** controls access to interprocess communication facilities like shared memory or shared message queues.
- The **cgroup namespace** limits access to the cgroup file system that hosts hierarchical cgroup configurations. (Control groups, or cgroups, are a mechanism to control how much of a resource a process can use. Examples are disk quotas or network bandwidth limits.)

Closely related to namespaces is the [`chroot` command](https://man7.org/linux/man-pages/man1/chroot.1.html) (and [system call](https://man7.org/linux/man-pages/man2/chroot.2.html)) that moves the root directory for the current process to a chosen directory within the file system.

### How to Create a Separate Namespace for a Process

Running a process in a separate namespace is easy to achieve. The `unshare` command runs a process and "unshares," or separates, one or more namespaces from the parent.

For example, the following command runs a shell in a separate UTS namespace:

~~~{.bash caption=">_"}
sudo unshare --uts bash
~~~

If you want to test this, the following Bash commands read the host name and spawn a shell with a separate UTS namespace, rename the host inside the shell, and read the host name inside and outside the shell:

~~~{.bash caption=">_"}
alice@earthly $ hostname
earthly
alice@earthly $ sudo unshare --uts bash
$ hostname
earthly
$ hostname martian
$ hostname
martian
$ exit
alice@earthly $ hostname
earthly
~~~

While the host name inside the shell is successfully changed, the parent shell does not see the change.

In the same way, you can isolate a process from the host's PID space, network devices, file mounts, users and groups, or interprocess communication.

To manipulate namespaces programmatically, an application can use three syscalls: `clone`, `unshare`, and `setns`.

## Docker's Implementation of Namespaces

When it comes to isolating containers from each other, Docker doesn't reinvent the wheel. Because it's a Linux-native technology, Docker uses Linux namespaces to achieve isolation and resource access control.

### Isolating the Process ID List

Using the PID namespace, Docker hides the global process list from processes inside a container. The first process spawned inside a container gets assigned a PID of 1. If it spawns further processes, they get assigned subsequent PIDs.

### Limiting File Mounts

Containerized applications do not need to access all the mounted file systems on the host to do the tasks they were built for. Separate `mnt` namespaces prevent containers from accessing mounts that belong to another container or the host.

Together with the `chroot` syscall, the `mnt` namespace can change the visible file system for a process. The `chroot` syscall changes the root directory that is visible to a process to a given directory of the host system. The `chroot`ed process can only see that directory and its subdirectories.

### Restricting Interprocess Communication

If two processes communicate with each other through Linux interprocess communication, they have to share the same `ipc` namespace. In general, containerized applications do not talk to applications in other containers (or, if they do, they typically use a REST API or a message queue system). That means that for isolation purposes, each container receives its own `ipc` namespace.

### Remapping Users and Groups

Sometimes it's unavoidable that applications inside containers must run as `root`. To avoid security breaches, Docker can remap the root user inside a container to an unprivileged user ID on the host, effectively preventing privilege escalation attacks.

### Virtualizing the Network

With a network namespace, a container gets a unique, virtual network stack. This includes network interfaces, IP addresses, ports, and routing tables. When each container has its own IP address, virtual networks between containers can be established that isolate network traffic between containers from traffic to and from the host or the host's networks.

## The Benefits of Namespaces

Linux namespaces address three requirements around containerization: security, resource management, and container management.

### Enhanced Security

By limiting access to system resources and contexts, namespaces help improve container security. Intruders that break into a running container are unable to see other containers or host processes. The root user inside the container maps to a user without privileges on the host. That means intruding into a system through a Docker container is much harder than intruding into a system where all processes run inside the host's global namespaces.

### Improved Resource Management

Namespaces also provide the means for managing the resources for a process. If a process does not initiate network connections outside the host, the container can be set up to allow only network communication with the host. Additionally, a reduced list of mounted file systems ensures that a process does not interfere with other processes' file resources.

### Simplified Container Management

Finally, managing containers is simpler if they do not interfere with each other. Imagine that you start two containers that both run a web server listening on port 80. With separate network namespaces in place, each container's port can be remapped to a different available port on the host system.

## Utilizing Namespaces in Docker

How does Docker use Linux namespaces in practice? Let's take a look at three typical requirements for containers and how Docker meets these requirements using namespaces.

### Container Differentiation

Containers provide isolated environments for processes, but they still need to access global resources on the host. To avoid conflicts, Docker differentiates containers by remapping the IDs of resources, such as network ports, process IDs (PIDs), user IDs (UIDs), or group IDs (GIDs).

For instance, a containerized process can have different PIDs inside the container and on the host. If it is the first process spawned inside a container, it sees itself as the process with ID 1. Unless this process spawns subprocesses, it does not see any other processes on the system.

To examine this behavior, you can run a container and inspect the output of `ps` inside and outside the container.

> As a prerequisite, you need [Docker](https://docs.docker.com/engine/install/) installed on your system. The host used in the following examples is a Linux system. If you use a different OS, Docker runs inside a Linux VM. In this case, `ssh` into the VM to follow the steps of the examples. It's also assumed that Docker is [set up for use without `root`](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user).

The following command creates a new container based on an Alpine Linux image and runs the `sh` shell interactively:

~~~{.bash caption=">_"}
docker run --rm -it alpine sh -C
~~~

> **Please note:** Alpine does not come with `bash`. Alpine Linux is used here because the image is small compared to other Linux distros.

The `-C` flag only serves to make finding the `sh` command in the host's `ps` output easier.

You should now see Alpine's `sh` prompt.

Type `ps` to see the PID of the shell:

~~~{.bash caption=">_"}
/ # ps
PID   USER     TIME  COMMAND
    1 root      0:00 sh -C
    7 root      0:00 ps
/ #
~~~

You can see that `sh` has PID 1. Child processes get assigned subsequent PIDs. (Run `ps` again to see its PID increase.)

Now open a new shell on the host and find the `sh` process using `ps` and `grep`:

~~~{.bash caption=">_"}
$ ps ax | grep "sh -C"
   3150 pts/1    Sl+    0:00 docker run --rm -it alpine sh -C
   3186 pts/0    Ss+    0:00 sh -C
   3208 pts/2    S+     0:00 grep --color=auto sh -C
~~~

On the host, the PID of the same `sh` process is entirely different—3186 in this example.

If you start a second Docker container in the same way, the shell inside the container will also have a PID of 1. But as each container has its own PID namespace, the PIDs inside the two containers will not conflict with each other or with the PIDs on the host.

Similarly, Docker can remap other resources, such as network ports or user IDs, to further isolate containers from each other and from the host.

### Container Security

Container security is a complex topic, and many layers of security technology are involved in making containers secure, but everything starts at the Linux namespaces layer.

Linux namespaces are at the core of container security. All other security layers and techniques are stacked on top of namespaces.

In the Linux kernel, these layers include:

- Control groups (cgroups) for setting usage limits on resources (such as disk quotas or bandwidth limitations) so that a single container cannot claim a resource exclusively.
- Capabilities, or a fine-grained list of rights to perform a particular operation. Capabilities overcome the restrictions of the all-or-nothing approach of using root and non-root users.
- Mandatory access control (MAC) systems like AppArmor or SELinux that define access policies that Docker applies to all containers.
- Seccomp profiles that enable or disable the syscalls a process can make.

The Docker platform provides additional security techniques, such as [Docker trusted content](https://docs.docker.com/trusted-content/) and [Docker secrets](https://docs.docker.com/engine/swarm/secrets/), but these don't apply to the level of single-container instances.

Although namespaces are the lowest layer of these security measures, they are indispensable for container security in two ways: they help prevent security breaches and resource hijacking, and they help achieve data privacy in multitenant applications.

#### Security Breaches and Resource Hijacking

Imagine criminals gaining access to a containerized process. In this scenario, thanks to a separate `mnt` namespace and `chroot`, they can only see a small part of the host's file system. A user namespace and UID/GID remapping cause the root user inside the container to be an unprivileged user outside the container. If the intruders manage to break out of the container, they'll have no root privileges outside.

Due to a separate PID namespace, the intruders can only see the processes that run inside the container. They have no way of determining which processes run on the host or in other containers. If the intruders try to scan or block all network ports, a separate network namespace confines their malicious activity to container-local ports, keeping the host network out of reach.

#### Data Privacy in Multitenant Applications

Because namespaces compartmentalize essential resources, they're ideally suited for multitenant scenarios where isolating data is crucial. The same concepts and ideas for preventing security breaches and resource hijacking apply here, too. By isolating processes, file systems, mount points, users, and networks of different tenants, users can confidently run their applications without worrying about data leaking into other tenants' containers.

### Running Docker Containers in the Same Namespace

After talking so much about achieving isolation, it's time to try running two containers in the *same* namespace.

In this scenario, let's assume that two containers can run in the same PID namespace so that they can see each other's processes. Let's also assume a given process has the same PID in both containers.

You'll try this in two different ways: through the Docker CLI and with Kubernetes pods.

#### Running Docker Containers with the Docker CLI

Docker's `run` command has a `--pid` flag that assigns a container to the PID namespace of another container.

To test this, open two shells. In one shell, type the following to start a container named `waldorf`:

~~~{.bash caption=">_"}
$ docker run --rm -it --name waldorf alpine sh
~~~

In the other shell, start a second container named `statler` with the `--pid` flag:

~~~{.bash caption=">_"}
$ docker run --rm -it --name statler --pid=container:waldorf alpine sh
~~~

The `--pid=container:waldorf` flag tells Docker to use `waldorf`'s PID namespace for the `statler` container as well.

Now run `ps` in both shells. You'll see two `sh` processes in each output instead of one, and the PIDs of the shell processes are identical in both containers.

Shell one looks like this:

~~~{.bash caption=">_"}
/ # ps
PID   USER     TIME  COMMAND
    1 root      0:00 sh
    7 root      0:00 sh
   13 root      0:00 ps
~~~

And shell two looks like this:

~~~{.bash caption=">_"}
/ # ps
PID   USER     TIME  COMMAND
    1 root      0:00 sh
    7 root      0:00 sh
   14 root      0:00 ps
~~~

Be aware that the two containers can influence each other. For instance, they could send signals to the other container's processes, including a kill signal. That means you need to use shared namespaces with caution and only if there is no other more secure way of making two containers work together.

#### Sharing PIDs With Kubernetes

Containers that run in the same Kubernetes pod can share PIDs as well. It takes nothing more than a single line in the pod configuration.

> To run the following steps locally, you need a running Kubernetes node, such as the [standalone Kubernetes](https://docs.docker.com/desktop/kubernetes/) setup provided by Docker Desktop.

As an example, the configuration file below starts two containers running a `sleep 1000` command (you're not using interactive shells here):

~~~{.yaml caption=""}
apiVersion: v1
kind: Pod
metadata:
  name: shared-pid-pod
spec:
  shareProcessNamespace: true
  containers:
  - name: waldorf
    image: alpine
    command: ["sleep"]
    args: ["1000"]
  - name: statler
    image: alpine
    command: ["sleep"]
    args: ["1000"]
~~~

Note the following line:

~~~{.yaml caption=">_"}
shareProcessNamespace: true
~~~

This line shares the PID namespace between the containers running in this pod.

Start the pod by calling the following:

~~~{.bash caption=">_"}
$ kubectl apply -f shared-pid-pod.yaml
~~~

Then, check the status of the pod until the status is `Running`:

~~~{.bash caption=">_"}
$ kubectl get pods
NAME             READY   STATUS    RESTARTS   AGE
shared-pid-pod   2/2     Running   0          9s
~~~

Now start an interactive shell in one of the containers and run `ps` to see the running processes:

~~~{.bash caption=">_"}
$ kubectl exec -it shared-pid-pod -c waldorf -- sh
/ # ps
PID   USER     TIME  COMMAND
    1 65535     0:00 /pause
    7 root      0:00 sleep 1000
   13 root      0:00 sleep 1000
   19 root      0:00 sh
   25 root      0:00 ps
/ #
~~~

There are two `sleep 1000` processes visible, one from each container, and they both share the same PID namespace.

#### Using Shared Namespaces in Production

Sharing namespaces between processes lowers the level of isolation between the involved containers and should therefore be used sparingly and only if absolutely necessary. That being said, which of the above approaches—Docker CLI or Kubernetes pods—would be more suitable for production use?

It might be tempting to say that it doesn't really matter because the benefits and risks of sharing namespaces stay the same. However, there are a few arguments that lean towards using Kubernetes pods rather than the Docker CLI for production use:

- **Pods are designed for managing multiple containers.** A pod group's containers share several resources already, including some Linux namespaces. It's therefore perfectly suited for sharing another namespace.
- **Pods use declarative configuration.** Kubernetes pods provide an easy way to configure shared namespaces by setting `shareProcessNamespace: true` in the pod spec. This is less error-prone and much easier to maintain than having to manually specify the right container names and IDs when using `docker run`.
- **A pod is a logical entity for all containers inside it.** Containers that are explicitly set to share a resource (such as the PID namespace) should be started and stopped together in order to maintain consistency. Running such containers in the same pod ensures this.

In general, starting containers through CLI commands is more of an ad hoc approach that does not scale well. Productive environments should be equipped with a software orchestration solution like Kubernetes.

## Conclusion

Linux namespaces are at the core of container isolation in Docker. Namespaces compartmentalize global kernel resources, such as network interfaces, processes, file mounts, and users and groups. With namespaces and `chroot`, a process inside a container may find itself running as the only process on a Linux system, equipped with `root` privileges, while in fact it's only isolated from other processes through separate namespaces and a virtual file system root.

By leveraging namespaces, Docker provides a robust platform for deploying diverse applications on a shared system with a high degree of control and separation.

{% include_html cta/bottom-cta.html %}
