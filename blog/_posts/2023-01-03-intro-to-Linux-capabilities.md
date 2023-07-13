---
title: "An Introduction to Linux Capabilities"
categories:
  - Tutorials
toc: true
author: Anurag Kumar
editor: Bala Priya C

internal-links:
 - Kubernetes
 - Linux
 - Containers
 - Pods
excerpt: |
    Learn about Linux capabilities and how they allow for fine-grained control over the privileges of running processes. Discover how to use capabilities in Docker containers and Kubernetes, and understand the importance of setting the right capabilities for your containerized workloads.
---
**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. [Give us a try](/).**

In Linux, capabilities are a way to assign specific privileges to a running process. They allow us to have more fine-grained control over the privileges that processes have on a Linux system.

In this article, you'll learn about capabilities in Linux. You'll also learn how you can use capabilities in the context of Docker containers and Kubernetes.

## Linux Capabilities: An Overview

We'll take some examples to understand Linux capabilities.

In Unix, we have two main controls: superuser (root) and normal user (non-root). The UID stands for user identifier and is used to determine what a user can do within the system. The UID of the root user is set to 0 meaning it can do (almost) anything and has the maximum number of privileges. A non-zero UID signifies that it's a normal user who generally does not have permissions to install software, modify system files, and more.

Linux kernel capabilities are supported not only for processes, but for all threads in a process as well. You need capabilities to reduce the attack surface. You can restrict permissions using Linux capabilities without giving complete permissions.

Here's an illustration of Linux capabilities.

![Linux Capabilities]({{site.images}}{{page.slug}}/CKk02DO.png)\

In the above illustration, in (A), the process has complete access to the system. In (B), the process has access to the system, but the privileges are now divided into sections. In (C), the process has restricted capabilities.

## History & Tools

Capabilities are important because they let us decide the required capabilities for a process instead of giving it full access—even if it's not required. The capabilities feature was introduced in 2.2 kernel in the year 1999, but it was only scoped to processes. In 2008, capabilities were introduced for files too.

Now, let's install some packages which come with system executables that will help us in working with Linux capabilities.

### `libcap2-bin`

The two basic commands that we have to get and set capabilities are `setcap` and `getcap`. `getcap` gives you the list of capabilities, whereas `setcap` is used to set specific capabilities to an executable.

Please note that for using `setcap`, you have to pass the original file, not the file with symlink. Symlink in Linux is a special file that points to another file.

~~~{.bash caption=">_"}
$ sudo setcap cap_net_bind_service+ep /path/to/the/file
~~~

After running this command, the file will be having `cap_net_bind_service` capability, meaning it has the privilege to bind any port less than 1024 on the host.
For `getcap` you need to do the same.

~~~{.bash caption=">_"}
$ sudo getcap /path/to/the/file
~~~

To use these commands, you should install the libcap2-bin package. libcap2-bin comes with some other tooling that includes `capsh` and `getpcaps`. `capsh` is also used to get the capabilities and is helpful in decoding, which we'll see later. `getpcaps` is helpful when you want to check with what capabilities a Linux process is running.

To illustrate, let's take an example of `ping`. It requires you to open a raw socket. Only a root user can open a raw socket or a port under 1024. How can we give the necessary capabilities to a particular process? We can do so using the `setcap` binary that we use to set specific Linux capabilities to an executable.

You can set the particular `net_raw` capability to ping:

~~~{.bash caption=">_"}
$ sudo setcap cap_net_raw=ep ping
~~~

Note: In some systems, ping doesn't have a SUID set for ping.

To summarize, capabilities involve breaking your root privileges into different levels and help you to give specific capabilities to each process.

Let's try to understand what some capabilities can do. The best guide here is the man page of capabilities. Open up your terminal and type `man capabilities`. You'll see approximately 37 capabilities, and each serves different functions.

For example:

- `CAP_CHOWN` changes the ownership of a file. It allows root to make arbitrary changes to file UIDs and GIDs.
- `CAP_KILL` kills any process that's running in the system.
- `CAP_NET_BIND_SERVICE` allows you to open a port which is less than 1024  even if a process is not running as root.

There are many more and if you're interested you can refer to the man page.

### `libcap-ng-utils`

There is another package which is quite useful when it comes to dealing with capabilities named `libcap-ng-utils` and it comes with `netcap`, `filecap`, and `pscap` toolings. These tools are useful when you're dealing with capabilities in Linux. `filecap` gives you all the capabilities of an executable file and `pscap` gives you all the capabilities of a running process. `netcap` gives you the report of the capabilities of the processes which are communicating over a network using TCP, UDP, and more.

## Capabilities in the Context of Containers

![Docker]({{site.images}}{{page.slug}}/AU6ehOs.png)\

When you start a container by default, it starts with some capabilities given by the container runtime. Tools like Docker give you the flexibility to add and drop capabilities depending on the requirements. To work with this, you need to know what capabilities required by your container will not work according to expectation.

For example, let's run a busybox container and check the capabilities with which the process is running. A busybox container is a container based on a busybox image. It's a lightweight container that comes with many commonly used UNIX utilities like awk, grep, and tar.

~~~{.bash caption=">_"}
$ docker run --rm -it busybox sleep 1h &
~~~

Now you need to get the PID of the running container and for this you can use `docker inspect <container-id>`. The PID stands for process ID. It is a unique numeric ID for every process that's running on a Linux system.

~~~{.bash caption=">_"}
$ docker inspect 7666636cd08c | grep -i PID
~~~

~~~{.bash caption="Output"}
            "Pid": 23764,
            "PidMode": "",
            "PidsLimit": null,
~~~

There are five different types of process capabilities set. Let's understand what each of the capabilities signify:

- `CapInh` (Inherited capabilities) are the capabilities that are passed down from a running parent process to its child process.
- `CapPrm`(Permitted capabilities) are the capabilities that a process is allowed to have.
- `CapEff` (Effective capabilities) set is all the capabilities with which the current process is executing.
- `CapBnd` (Bounding capabilities) set is the maximum set of capabilities that a process is allowed to have.
- `CapAmb` (Ambient capability) set includes the capabilities that are in effect currently. It can be applied to the current process or its children at a later time.

### Understanding Effective Capabilities

In this article, we will focus on effective capabilities set. Most of the time you'll use the effective capability.

To get the capabilities of the container, run the following command:

~~~{.bash caption=">_"}
$ grep Cap /proc/<container-pid>/status
~~~

~~~{.bash caption="Output"}
CapInh: 00000000a80425fb
CapPrm: 00000000a80425fb
CapEff: 00000000a80425fb
CapBnd: 00000000a80425fb
CapAmb: 0000000000000000
~~~

These are the five types of capabilities that we discussed above. We will also see how to decode the unreadable part.

This output is not readable, so to read this we'll use a binary which comes from the `libcap2-bin` package named `capsh`.

At this point, [make](/blog/using-cmake) sure you have the [libcap2-bin package installed](https://command-not-found.com/capsh). To decode the effective capability, get the text written after `CapEff:` and use the following command, and you should see output like this.

~~~{.bash caption=">_"}
$ capsh --decode=00000000a80425fb
~~~

~~~{.bash caption="Output"}
0x00000000a80425fb=cap_chown,cap_dac_override,cap_fowner,
cap_fsetid,cap_kill,cap_setgid,cap_setuid,cap_setpcap,
cap_net_bind_service,cap_net_raw,cap_sys_chroot,cap_mknod,
cap_audit_write,cap_setfcap
~~~

The output shows different capabilities that the process has. For example, `cap_chwon` capability gives a program the ability to change the owner of a file or a directory. This capability is used by the `chown` command. Similarly, If you want a process to allow opening/listening to a port less than 1024 then you can use cap_net_bind_service which allows a process to bind to ports less than 1024. You can read more about [capabilities](https://man7.org/linux/man-pages/man7/capabilities.7.html).

Alternatively, if you have the PID of the process, you can also use `getpcaps` to get the capabilities of the process.

~~~{.bash caption=">_"}
$ getpcaps 23808
~~~

~~~{.bash caption="Output"}

23808: = cap_chown,cap_dac_override,cap_fowner,cap_fsetid,cap_kill,cap_setgid,cap_setuid,cap_setpcap,cap_net_bind_service,cap_net_raw,cap_sys_chroot,cap_mknod,cap_audit_write,cap_setfcap+eip
~~~

Note: 23808 is the PID of the container, and it can be different in your case.
The capabilities mentioned above the capabilities of the container which is running as a process on your host system.

### Running a Privileged Container

![Running a Privileged Container]({{site.images}}{{page.slug}}/uoCn5gJ.png)\

To run a privileged container, you can pass a `--privileged` flag while running the container. You might want to run a privileged container when your container needs to modify sensitive system files that are not accessible to a non-privileged container. You can also run containers with privilege when you need access to certain hardware resources.

~~~{.bash caption=">_"}
$ docker run --privileged -d nginx
~~~

The above command will run a container based on `nginx` image in detached mode with privileged access. The `--privileged` flag is used to run the container with privileged access. This means that the container will have access to all the host system resources, including the network and the host's filesystem.

What happens under the hood is that the container will start with all the capabilities, and it can do anything within the container as well as the host system. For example: opening a port under 1024, accessing all the files, mounting file systems, killing any process.

Let's understand this with an example.

A normal container will *not* give you access to your host disks or device files, but with privileged containers, we can access those disks as well as device files. It means that the container can potentially read, modify, and delete important files on the host system.

For example, let's run an Ubuntu container without a privileged flag:

~~~{.bash caption=">_"}
$ docker run --rm -it ubuntu 
~~~

And then, within the container, First execute this command `fdisk -l` and then `ls /dev`. `fdisk -l` will list all the partitions on a disk. Along with this, the command will also show parameters like size and type. An Ubuntu container doesn't have the `fdisk` command by default, so for that, run the command `apt-get update && apt-get install fdisk`.

Post installation, if you run `fdisk -l` then you'll not get anything! If you execute the command `ls /dev` for listing all the device files, then you'll get this output.

~~~{.bash caption=">_"}
root@461c672e930a:/# ls /dev
~~~

~~~{.bash caption="Ouput"}
console  core  fd  full  mqueue  null  ptmx  pts  \
random  shm  stderr  stdin  stdout  tty  urandom  zero
~~~

Now, if you repeat the same steps in a privileged container, then you'll see that you're able to read the disk information available on the host system. If an attacker has access to the host system, then they can gather information about other containers that are running on it and identify potentially vulnerable targets.

~~~{.bash caption=">_"}
$ docker run --privileged --rm -it ubuntu
~~~

In the privileged container, try executing the same command that we have executed in the normal container.

~~~{.bash caption=">_"}
root@190c563af469:/# fdisk -l
~~~

This lists the partition table entries:

~~~{.bash caption="Output"}
# output (truncated)

Disk /dev/loop0: 61.77 MiB, 64770048 bytes, 126504 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
… 
…
…

Disk /dev/vda: 10 GiB, 10737418240 bytes, 20971520 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: 3D5B5FC8-E964-4310-AC68-89DD2E51D6D4

Device      Start      End  Sectors  Size Type
/dev/vda1  227328 20971486 20744159  9.9G Linux filesystem
/dev/vda14   2048    10239     8192    4M BIOS boot
/dev/vda15  10240   227327   217088  106M EFI System
~~~

Next, run the `ls /dev` command:

~~~{.bash caption=">_"}
root@190c563af469:/# ls /dev
~~~

~~~{.bash caption="Output"}
# output (truncated)

autofs           full          loop1   mem     pts       stdout  tty15  tty23  tty31  tty4   tty48  tty56  tty7    ttyS14  ttyS22  ttyS30     udmabuf  vcs6   vcsu1  vda15
btrfs-control    fuse          loop2   mqueue  random    tty     tty16  tty24  tty32  tty40  tty49  tty57  tty8    ttyS15  ttyS23  ttyS31     uinput   vcsa   vcsu2  vfio
… 
…
…
fd               loop0         mcelog  ptmx    stdin     tty14   tty22  tty30  tty39  tty47  tty55  tty63  ttyS13  ttyS21  ttyS3   ttyprintk  vcs5     vcsu   vda14
~~~

In the output, you can see that we're able to read the disk information in a privileged container and the number of device files which we have access to is much larger than a normal container.

You can try running privileged tasks by execing into the container. You can also grep the capabilities like we did earlier, and you'll see that the container is having all the privileges.

### Running a Container with Zero Privileges

If you're using Docker, then you can use the flag `--cap-drop=all` to run a container with zero privileges. Running a [container](/blog/docker-slim) with zero privileges means that the container is not allowed to access any of the host system's resources.

By running containers with zero privileges, you can limit the potential damage that can be caused by a compromised container. Even if an attacker gets inside the container, they might not be able to compromise the host system or any other container. The blast surface will be very strict in this case.

~~~{.bash caption=">_"}
$ docker run --rm --cap-drop=all -it busybox sleep 1h &
~~~

If you grep the capabilities like we did above, you'll see the effective capability is now `CapEff: 0000000000000000` and if you decode the string then you will get no capabilities.

~~~{.bash caption=">_"}
$ capsh --decode=0000000000000000
~~~

~~~{.bash caption="Output"}
0x0000000000000000=
~~~

### Running a Container with Certain Privileges

Now, let's try and understand how we can run a container with certain privileges.
If you're using [docker](/blog/rails-with-docker), then you can use `--cap-add` to add capabilities and `--cap-drop` to drop the capabilities. For example, if you want to run a container with `sys_admin` capabilities and drop everything else, then you can do it as follows:

~~~{.bash caption=">_"}
$ docker run --rm --cap-drop=all --cap-add=sys_admin \
-it busybox sleep 1h &
~~~

Please note that if you want to add or drop more than one privileges, then you have to add the same flag again.

For example, say if you want to run a container dropping all capabilities and only using SYS_ADMIN & NET_ADMIN capabilities. You need to use the `--cap-add` flag twice.

~~~{.bash caption=">_"}
$ docker run --rm --cap-drop=all --cap-add=sys_admin \
--cap-add=net_admin -it busybox sleep 1h &
~~~

## Capabilities in the Context of Kubernetes

Kubernetes is an open-source container orchestrator that manages containerized workloads. Some examples of what Kubernetes can do, in addition to managing containerized workloads, include:

- Service Discovery and Load Balancing: Kubernetes provides built-in support for     load balancing requests across multiple replicas of your application.
- Self Healing : With the help of controllers, Kubernetes monitors the health of your containerized application and if the container or pod crashes, then Kubernetes tries to run the container again or reschedule the pod.
- Configuration Management: Kubernetes has support for [ConfigMaps for configuration management](https://earthly.dev/blog/kubernetes-config-maps/).

It's a CNCF graduated project. Since it manages containers, you can set the capabilities here. The orchestrator will [make](/blog/makefiles-on-windows) sure that the container runs with the given capabilities only.

### Setting the Right Capabilities in Pods

![Setting the Right Capabilities in Pods]({{site.images}}{{page.slug}}/ONAYoLA.png)\

By using `SecurityContext` in Kubernetes manifest, you can set the capabilities in containers. Let me illustrate the same with one sample manifest:

~~~{.yaml caption=""}
apiVersion: v1
kind: Pod
metadata:
  name: pod
spec:
  containers:
  - command:
    - sleep
    - "100000"
    image: ubuntu
    name: ubuntu-pod 
    securityContext:
      privileged: false 
      capabilities:
        drop:
          - ALL 
        add: 
          - SYS_ADMIN
          - NET_ADMIN
~~~

The above Kubernetes manifest will create a Pod with Ubuntu image, and it has only two capabilities: SYS_ADMIN and NET_ADMIN.
In the above manifest, we are dropping all other capabilities.

This is much better than running a pod with `privileged: true` which will add all the Linux capabilities, that counts to approximately 37.

`SYS_ADMIN` is almost similar to giving root level access to the containers, and you should avoid it if it's not required. If you look up the man page of capabilities, then `SYS_ADMIN` is also termed as the new root. Similar to `SYS_ADMIN`, `NET_ADMIN` allows you to perform all the privileged networking operations on your system.

While using capabilities in Kubernetes, you should drop the CAP word in the prefix. We are doing the same thing as before, but the format of writing capabilities is a little different.

Even if you're using a multi-container pod, you can set the SecurityContext in each container. You can also use tools like [tracee](https://github.com/aquasecurity/tracee), [inspektor-gadget](https://www.inspektor-gadget.io/) and other [eBPF](https://ebpf.io/)-based tools to trace the capabilities of the container. This will be useful if you're not sure of the capabilities required by your application.

## Conclusion

I hope this guide helped you understand Linux capabilities and why they're important. If you're running containerized workloads, then you should check with what privilege your container is running. You should only try to give the minimum required capabilities to the container.

By setting the right capabilities for your [container](/blog/docker-slim), you are reducing the attack surface. Even if someone breaks into the container, you can control the damage.
As with most other Linux commands, you can use the `man` page to learn more about capabilities.

{% include_html cta/bottom-cta.html %}
