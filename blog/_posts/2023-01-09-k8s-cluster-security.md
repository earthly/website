---
title: "Harden Kubernetes cluster with pod and container security contexts"
toc: true
author: Muhammad Badawy

internal-links:
 - Kubernetes
 - Security
 - Pod
 - Cluster
excerpt: |
    Learn how to secure your Kubernetes cluster by applying security contexts to pods and containers. This article explains the concept of security contexts, their implementation in Kubernetes, and provides a step-by-step guide on how to apply them to enhance the overall security of your cluster.
last_modified_at: 2023-07-19
categories:
  - orchestration
---
**This article provides a clear understanding of Kubernetes security contexts. Earthly strengthens CI pipelines with advanced caching. [Learn more about Earthly](https://cloud.earthly.dev/login).**

![K8s Security Context]({{site.images}}{{page.slug}}/FB9gnth.png)\

When it comes to security in Kubernetes, it is vital to secure the individual resources of the cluster. Pods and containers are considered the core resources running in the [cluster](/blog/kube-bench) and are the fundamental building block of Kubernetes workloads. Applying security to the pod and container layer can have a huge impact on the overall security of your cluster.

By default, Kubernetes pods have root access. Running [k8s](/blog/k8s-autoscaling) pods with root or as a privileged user can be very harmful to the host file system for a number of reasons. It can give the attackers the ability to escape out of the pod or container boundaries and get unconstrained access to the host. Security contexts allow you to control what types of access your pods have and accordingly run the pods inside your K8s cluster in a secure manner.
In this blog post, we'll demonstrate how to harden your Kubernetes cluster through security contexts and apply them to pods and containers.

### Security Context as Concept

In most Linux distributions, SELinux (Security Enhanced Linux) is a security module that works inside the kernel to intercept any call and check if it is allowed or not.
A Security Context is a mechanism or tool used by SELinux to enforce access controls and apply certain labels/contexts to the objects (files/directories) in the system; in other words, when an application/process try to access certain files, SELinux checks the security context of the process and the file and determines whether the process has the required permissions to access the file or not.

### Security Context as Implementation in Kubernetes

Security contexts in Kubernetes are considered one of the most important features to harden and secure Kubernetes clusters. They **allow you to control the behaviour of the running pods and containers and how they interact with the host server**, OS and kernel. They authorize to bind certain resources in your cluster (pods and containers) to specific users or groups, restrict pods and containers from interacting with the host operating system processes, other pods and services and allow them to perform their intended tasks while staying secure at the same time.
Samples of security control that can be handled through security contexts include:

- Limiting the privileges that a containerised application receives from the host OS (read-only vs read-write).
- Specifying if permissions can be escalated or not.
- Preventing applications from making direct calls to the kernel via the file system.
- Which SELinux context to be applied to the container's process while it is running.

Now let's jump to a demo which will consists of 3 parts:

1. Risks behind running apps with default configuration.
2. Applying security contexts on pod level.
3. Applying security contexts on pod and [container](/blog/docker-slim) level.

### Prerequisites

- Up and running Kubernetes cluster. [minikube](https://minikube.sigs.k8s.io/docs/start/) or [kind](https://kind.sigs.k8s.io/docs/user/quick-start/) can be used to start one.
- Familiarity with kubectl commands.

### 1- Let's Start the Demo by Clarifying the Risks Behind Running Apps with Default Configuration

The best way to tackle this topic is to demonstrate it in a practical way. So let's apply the below yaml manifest to run a pod with default configuration.

~~~{.yaml caption=""}
echo "
apiVersion: v1
kind: Pod
metadata:
 name: security-context-demo-default
spec:
 volumes:
 - name: sec-ctx-vol-default
   emptyDir: {}
 containers:
 - name: sec-ctx-demo-default
   image: busybox:1.28
   command: [ "sh", "-c", "sleep 1h" ]
   volumeMounts:
   - name: sec-ctx-vol-default
     mountPath: /data/demo
" | kubectl apply -f -
~~~

Now let's jump into the pod with sh terminal:

~~~{.bash caption=">_"}
$kubectl exec -it security-context-demo-default -- sh
~~~

Once you execute the above command, a terminal will be prompted as (/#) which means you are root inside the pod, also we can try the id command to show the exact user and group ids:

~~~{.bash caption=">_"}
#id
uid=0(root) gid=0(root) groups=10(wheel)
~~~

### A Quick Review on the UID and GID

In Linux operating systems, each user is assigned a number which is called a UID (User ID). You can add many users to groups. A group of users is assigned a number which is called the GID (Group ID). These numbers are used to identify users and groups to the OS and to determine the ownership of system resources (files and processes).

Note that root user and group are always assigned number 0, and the first 100 UIDs and GIDs are reserved to be used by the OS, so new users/groups will be assigned a number starting from 500 or 1000 according to Linux distribution.

The risks behind it, is the **root user here is the same root user on your host** and sharing the same kernel. Isolation is only provided by the Container Runtime Interface CRI isolation mechanism like docker.
Also, running as root means the user will have access to all filesystems, which can be easily edited. Any packages can be installed and files can be overwritten. Not good.
Another level of administration permissions can be given to the root user if we add a security context as below:

~~~{.yaml caption=""}
containers:
- name: sec-ctx-demo
  image: busybox:1.28
  command: [ "sh", "-c", "sleep 1h" ]
  volumeMounts:
  - name: sec-ctx-vol-default
    mountPath: /data/demo
  securityContext:
    privileged: true
~~~

Which can give the root user inside that container access to all the volumes mounted in the cluster and of course all sensitive data and credentials. If we try to redeploy the pod with the above security context, then list the available volumes, we will be able to see all system volumes, which is a breach and could allow attackers to perform root-privileged actions to our system.

~~~{.bash caption=">_"}
#ls /dev
~~~

<div class="wide">
![Image]({{site.images}}{{page.slug}}/AqHyZkK.jpg)\
</div>

### 2- Applying Security Contexts on Pod Level

Now let's apply some security contexts to the pod level of a deployment and make sure they are applied correctly and as expected.
`securityContext` is part of `pod/spec` or `pod/spec/containers` sections in the deployment file and can be explained through the below commands:

~~~{.bash caption=">_"}
$kubectl explain pod.spec.securityContext | more
$kubectl explain pod.spec.containers.securityContext | more
~~~

You will be able to see a detailed explanation of securityContext object:

<div class="wide">
![Security Context explanation in K8s]({{site.images}}{{page.slug}}/lPjmTMl.jpg)
</div>

Now let's apply a YAML [deployment](/blog/deployment-strategies) to run a demo pod with security context defined and see how it will impact the behaviour of our app.

~~~{.yaml caption=""}
echo "
apiVersion: v1
kind: Pod
metadata:
 name: security-context-demo
spec:
 securityContext:
   runAsUser: 1000
   runAsGroup: 3000
   fsGroup: 2000
 volumes:
 - name: sec-ctx-vol
   emptyDir: {}
 containers:
 - name: sec-ctx-demo
   image: busybox:1.28
   command: [ "sh", "-c", "sleep 1h" ]
   volumeMounts:
   - name: sec-ctx-vol
     mountPath: /data/demo
" | kubectl apply -f -
~~~

As you can see in the `securityContext` section, we configured the pod to run any container process with user 1000, group 3000 and supplementary group 2000. Which means that the container process will not run as root anymore and user 1000 will be bounded in the mounted volume `/data/demo`, so if we try to create a new file out of the mounted volume, we should get a `permission denied` error. So this will definitely secure our filesystem.
Note here whatever will be created under the mounted volume will take the value of `runAsUser` and `fsGroup`. And this security context will be applied to all the containers running in this pod.
Now let's verify that through running a shell in the pod:

~~~{.bash caption=">_"}
$kubectl exec -it security-context-demo -- sh
~~~

Then checking the user running the container process through id command:

~~~{.bash caption=">_"}
$id
uid=1000 gid=3000 groups=2000
~~~

Also let's check the processes that are running in the container:

~~~{.bash caption=">_"}
$ps -ef
PID   USER     TIME  COMMAND
   1 1000      0:00 sleep 1h
  17 1000      0:00 sh
  24 1000      0:00 ps -ef
~~~

It shows that they are running as user 1000 which is what configured as runAsUser
Now let's go to the mounted volume, create a file and check its permissions:

~~~{.bash caption=">_"}
$cd /data/demo
$touch testfile
$ls -lt
-rw-r--r--    1 1000 2000   6 Nov 12 09:49 testfile
~~~

As you can see, that test file is owned by user 1000 and group 2000 which are configured as `runAsUser` and `fsGroup`
Now let's try to create the same file under `/`:

~~~{.bash caption=">_"}
$cd /
$touch testfile
touch: testfile: Permission denied
~~~

As expected, permission is denied for user 1000 to create new resources out of the mounted volume `/data/demo`
So now we can say that our configurations are configured and tested correctly.

### 3- Applying Security Contexts on Container and Pod Levels

Now we will try to add security context to both pod and container specs. In most cases you want to unify the security context for all the containers running inside the pod, but you may want to specify certain containers to run with specific security context to fulfil the application needs like running with certain UID or capabilities, in that case you can combine pod and container security contexts.
Let's apply the below command:
> Note here: By default, all containers defined in the containers array section in YAML file will inherit the same security context as they are defined in the `pod/spec` section unless the security context for the container is defined in the `pod/spec/containers/securityContext` section. In that case the security context in the container section will have the upper hand and will overwrite the security context in `pod/spec` section.

~~~{.yaml caption=""}
echo "
apiVersion: v1
kind: Pod
metadata:
 name: security-context-demo
spec:
 securityContext:
   runAsNonRoot: true
   runAsUser: 1000
   runAsGroup: 3000
   fsGroup: 2000
 volumes:
 - name: sec-ctx-vol
   emptyDir: {}
 containers:
 - name: sec-ctx-demo
   image: busybox:1.28
   command: [ "sh", "-c", "sleep 1h" ]
   volumeMounts:
   - name: sec-ctx-vol
     mountPath: /data/demo
   securityContext:
     runAsUser: 10000
     readOnlyRootFilesystem: true
" | kubectl apply -f -
~~~

Here we modified the security context of the pod to force the containers running inside it to run as non-root, also we added a security context for the container to run as user 10000 and mount the root filesystem as readonly.
So what is expected here is to have a running container with the below specs:

- Non-root user
- User ID 10000
- Group ID 3000
- Supplementary group 2000
- Read-only root file system

Now let's verify that through running a shell in the pod:

~~~{.bash caption=">_"}
$kubectl exec -it security-context-demo -- sh
~~~

After logging into the container, we can check which user is running the container processes:

~~~{.bash caption=">_"}
$ps -ef
PID   USER     TIME  COMMAND
   1 10000     0:00 sleep 1h
   8 10000     0:00 sh
  15 10000     0:00 ps -ef
$id
uid=10000 gid=3000 groups=2000
~~~

So we can see that the container is running with user 10000, which shows that container configuration overrides pod configuration.
Now let's check the permissions on the file system. when we change directory to any root filesystem and try to create a file for example, you will not be able to do it as it is mounted as read-only filesystem:

~~~{.bash caption=">_"}
$cd /etc
$touch newfile
touch: newfile: Read-only file system
~~~

Then we can check our permission on the mounted file system `/data/demo`:

~~~{.bash caption=">_"}
$cd /data/demo
$touch newfile
$ls -ltr
total 0
-rw-r--r--    1 10000  2000   0 Nov 15 11:20 newfile
~~~

As you can see, that file has been created successfully with the configured UID and GID, which means that through these configurations, users running this container will only have write permission to the mounted file system /data/demo and will not be running as root and will run literally with 1000 user ID.

### Conclusion

In this article, we dove into Kubernetes security contexts, discussing what they are and their implementation. We flagged the dangers of running apps with default or misconfigured setups. We also showed how to apply security contexts to pods and containers to limit permissions. Remember, the security context has a [bunch of options](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.25/#securitycontext-v1-core) like `capabilities` or `seLinuxOptions` to bolster your K8s security.

As you continue to enhance your Kubernetes security, you might also be interested in improving your build automation. If so, why not check out [Earthly](https://cloud.earthly.dev/login)? It could be the next step in optimizing your tech stack. Enjoy!

{% include_html cta/bottom-cta.html %}
