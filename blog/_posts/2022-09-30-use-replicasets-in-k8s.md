---
title: "How to use ReplicaSets in Kubernetes and Why You Should Know About Them"
categories:
  - Tutorials
toc: true
author: Vivek Kumar Singh

internal-links:
 - ReplicaSets
 - Kubernetes
 - Pods
 - Cluster
excerpt: |
    Learn how to use ReplicaSets in Kubernetes to ensure fault tolerance and high availability for your applications. This tutorial explains what ReplicaSets are, how to create them using YAML, and how they work internally. If you want to build a fault-tolerant and scalable system with Kubernetes, understanding ReplicaSets is essential.
last_modified_at: 2023-07-19
---
**This article explains Kubernetes ReplicaSets. Earthly improves Kubernetes workflows by enabling reproducible and parallel builds. [Check it out](/).**

## What Is Kubernetes?

Kubernetes is a container orchestration system. This means that it manages the lifecycle of containers and allows you to deploy applications in a scalable way, with high availability and fault tolerance. Kubernetes is also a [cluster](/blog/kube-bench) manager, which means that it can manage multiple hosts or VMs on your behalf so you don't have to worry about them (or their resources) going down.

## ReplicaSets

In Kubernetes, the place where your application runs is called a pod. It is the fundamental unit of a Kubernetes Cluster. Pods in Kubernetes are not fault tolerant by default. Therefore, unless the pod was not created using a [controller](https://kubernetes.io/docs/concepts/architecture/controller/), Kubernetes will not be able to recover it if a pod crashes inside your Node. One of the controllers in Kubernetes that makes sure a certain number of Pods are operational is called a ReplicaSet. With ReplicaSets, your application gains fault tolerance and high availability.
You will learn about ReplicaSet in this article, including what they are and how to utilise them to give your Kubernetes Pods fault tolerance. You will also learn how to use ReplicaSets to scale your Pods. By the end of this article, you will have a firm foundational grasp of Kubernetes ReplicaSets.

## Kubernetes Installation

To start working with Kubernetes you first need to install it in your system. For this article you need to install these three things:

- Kubernetes
- It will ship with a CLI tool `kubectl` which is used to interact with our running cluster.
- Minikube
- Install [MiniKube](/blog/k8s-dev-solutions), which has a Single Node Master-Worker arrangement so you can experiment with Kubernetes in your system, for educational reasons. Please be aware that you won't be using MiniKube for actual production apps; instead, you'll be using GCP, AWS, or another cloud computing service.
- [Docker](/blog/rails-with-docker)
- Your programmes will be run on the Kubernetes cluster using the container runtime environment Docker. You can also install them as an alternative to Docker if you are familiar with other runtimes like cri-o or [containerd](/blog/containerd-vs-docker).

The installation instructions for the above tools are given in the [Official Kubernetes Documentation](https://kubernetes.io/docs/setup/) and for MiniKube you can check out its [documentation](https://minikube.sigs.k8s.io/docs/start/).

## The Problem With Pods

![Problems]({{site.images}}{{page.slug}}/probs.png)\

The smallest unit in Kubernetes is a pod, which wraps a container. Each Pod operates independently as a logical device. You can use the `kubectl run <name> <image>` command to create a Pod in our MiniKube single-node cluster, however, executing a Pod in this manner is not regarded as best practice. Instead, we'll use a YAML file to create a Pod in this lesson. All of the Pod's specifications are defined in one YAML file. Create a `pod.yml` file and add the following:

~~~{.yml caption="pod.yml"}
apiVersion: v1
kind: Pod
metadata:
  name: server-pod
spec:
  containers:
  - name: server
    image: nginx:latest
    ports:
    - containerPort: 80
~~~

You can see that you are declaring a Pod with the name `server-pod` in the YAML file mentioned above. The `image`, which is nginx, is defined by the Pod's specifications (or `spec`). Type the following command in your terminal to launch the above file. The `ports` field specifies how you will communicate with the container; they are internal to the [container](/blog/docker-slim).

~~~{.bash caption=">_"}
>>> kubectl create -f pod.yml
pod "server-pod" created
~~~

The above command creates any resource that is defined in the file `pod.yml`, in this case the resource is a Pod. Your Pod is up and running, you can see the status of the Pod using the following command.

~~~{.bash caption=">_"}
>>> kubectl get pods
~~~

The above command will produce an output like below. Note that `STATUS` is `ContainerCreating`. It will show Running once it finishes pulling the container image.

~~~{.bash caption="output"}
NAME        READY    STATUS             RESTARTS     AGE
server-pod    0/1    ContainerCreating     0         77s
~~~

The pod you just created is not fault tolerant or scalable; if it goes down, it stays down because there is no mechanism in place to cause it to spin back up. ReplicaSets can help because pods produced using the methods above are susceptible to crashes and Kubernetes won't take any action to recover them on its own.
To delete the above created pod you can run:

~~~{.bash caption=">_"}
kubectl delete pod server-pod
pod "server-pod" deleted
~~~

To check if the pod is deleted, you can run `kubectl get pods`, which will produce the following output.

~~~{.bash caption="output"}
No resources found in default namespace
~~~

## ReplicaSets

ReplicaSets are the controllers used to launch, shut down, and schedule Pods. ReplicaSets accomplish this by tracking the number of active pods continuously and comparing it to the `replicas` key in the YAML file. ReplicaSets instantly produces a new pod if one of the existing pods is deleted or crashes. By adjusting the size of the `replicas` field, ReplicaSets makes it simple to scale up and down your system. This functionality is fantastic if you have a programme that needs a specific number of Pods operating in order to operate properly.

## Defining ReplicaSets Using YAML

ReplicaSet creation is similar to Pod creation. Create the file `my-replicaset.yml` and enter the following configuration to define a replica set.:

~~~{.yml caption="my-replicaset.yml"}
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: my-replicaset
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-pod
  template:
    metadata:
      labels:
        app: my-pod
    spec:
      containers:
      - name: my-server
        image: nginx

~~~

Some of the parameters of note are:

- `apiVersion` is used to specify the version of the API that you'll be using to build your ReplicaSet and get your image from the server.
- `kind` informs Kubernetes that we want to create a ReplicaSet.
- `spec`is the core of the configuration. This is what tells Kubernetes that we should always have 3 pods running at all times.
- `spec.template` is used to inform the ReplicaSet of the configuration to be used when a new Pod is created or the Pod is revived in the event that one of them dies.
Look at the `app` in `selector.matchLabels` that the ReplicaSet uses to keep track of the active Pods. The ReplicaSet would not replicate a Pod if this label is missing from it. Run the following command in your terminal to build the ReplicaSet using the aforementioned parameters.

~~~{.bash caption=">_"}
kubectl create -f my-replicaset.yml
replicaset.apps/my-replicaset created
~~~

After running the above command, you will see a confirmation message. Run the command listed below to verify the Pods' status right away.

~~~{.bash caption=">_"}
kubectl get pods 
~~~

Above command will produce the following output:

~~~{.bash caption="output"}
NAME                  READY       STATUS             RESTARTS    AGE
my-replicaset-58fbh    0/1        ContainerCreating     0        51s 
my-replicaset-lx5hk    0/1        Running               0        51s 
my-replicaset-qrqj2    0/1        ContainerCreating     0        51s 
~~~

You'll notice that your cluster has three pods, which corresponds to the number of replicas indicated in your YAML file.
The command `kubectl get rs` used to obtain summary information about the ReplicaSet, running this command will produce the following output.

~~~{.bash caption="output"}
NAME          DESIRED    CURRENT        READY       AGE
my-replicaset    3        3               0         14s
~~~

`kubectl describe rs -f my-replicaset.yml`is used to offer detailed information about the ReplicaSet. This command will return the following result.

### Deleting Pods in ReplicaSet

Let's terminate a Pod in order to witness the magic of ReplicaSets in action. Run the command listed below to terminate one of the Pods.

~~~{.bash caption=">_"}
kubectl delete pod my-replicaset-58fbh 
~~~

Note that the above pod name would be different in your cluster. Running the above command will produce the following output.

~~~{.bash caption="output"}
pod "my-replicaset-58fbh" deleted
~~~

As soon as you perform the preceding command. To acquire the list of active pods, run `kubectl get pods`. You will get the below output.

~~~{.bash caption="output"}
NAME                  READY   STATUS              RESTARTS    AGE
my-replicaset-lx5hk    0/1    Running               0        5m 10s 
my-replicaset-qrqj2    0/1    Running               0        5m 10s 
my-replicaset-6bk2x    0/1    ContainerCreating     0        35s 
~~~

The list still contains three pods, but you will notice that the Pod you deleted is not present. A new pod is created as soon as the previous pod is eliminated. If you create another pod with the same label then ReplicaSets would terminate any pod because its goal is to keep the running number of Pods equal to the number specified in the YAML file.

### Deleting ReplicaSet

By using the command `kubectl delete rs <rs name>`, where `rs name` is the name of your ReplicaSet, you can destroy ReplicaSets. After you destroy the ReplicaSet, the running Pods will also get deleted.
You may test it, after deleting the ReplicaSet and then typing the command `kubectl get pods` into the terminal.
The above command will generate the following output.

~~~{.bash caption="output"}
No resources found in default namespace
~~~

## Internal Working of ReplicaSets

ReplicaSet requires ongoing communication with the Kubernetes API and Pods in order to function. The specific breakdown of how ReplicaSets accomplish this is shown below.

- Once you run the `kubectl create` command, your request goes to the API server of the minikube node.
- The Controller takes the request and creates the number of pods defined in the YAML.
- After that, the Master Node's Scheduler assigns the Pods to the Worker Nodes (in the case of minikube Master Node and Worker Node are the same).
- Then, after assigning Pods to them, kubelet asks Docker to construct containers on those Pods.
- After the containers are created, kubelet sends the request to the API server that the Pods are created.

## Conclusion

In this tutorial, we've covered how to build Pods using ReplicaSets in Kubernetes. ReplicaSets boost the fault tolerance of Pods, which is why they're commonly used instead of creating Pods directly. While ReplicationControllers are outmoded, you might still come across them. Also, remember other Controllers like StatefulSet for persistent storage apps and DaemonSet for running pod copies across the cluster. These insights are handy for building scalable, fault-tolerant systems.

As you scale your Kubernetes apps, you might find that [Earthly](https://www.earthly.dev/) could be your next step for efficient and reproducible builds. Check it out!

{% include_html cta/bottom-cta.html %}