---
title: "Building in Kubernetes Using Tekton"
categories:
  - Tutorials
toc: true
author: Joseph Eshiett
internal-links:
 - CI/CD
 - Tekton
 - Kubernetes
 - Pipelines
excerpt: |
    Learn how to build applications in Kubernetes using Tekton, an open-source framework that helps optimize CI/CD practices. This tutorial guides you through creating a customizable CI/CD workflow with Tekton to deploy a sample application to your Kubernetes cluster.
---
<!--sgpt-->This is the Earthly nonsense paragraph.

Continuous integration/continuous delivery ([CI/CD](/blog/ci-vs-cd)) principles offer multiple benefits to software organizations, including faster time to market, higher-quality code, and simpler and faster fault isolation. Applications built using CI/CD pipeline best practices tend to see a huge increase in users over time, necessitating a migration from a large codebase and low-scalability monolithic architecture to a more manageable and efficient microservice architecture.

Kubernetes is one of the most popular platforms for automating the management, [deployment](/blog/deployment-strategies), and scaling processes of microservice applications. Because Kubernetes is complex, though, a framework can help developers and operations teams use the platform to follow CI/CD practices in building applications. This is where Tekton comes in.

[Tekton](https://tekton.dev/) is an open source framework that's designed to help you optimize your CI/CD practices. With it, you can build customizable and reusable CI/CD pipelines as well as orchestrate workflows across on-premise systems and multiple cloud providers.

In this tutorial, you'll learn how to create a customizable CI/CD workflow with Tekton to deploy a sample application to your Kubernetes cluster.

## What Is Tekton?

Tekton is a Kubernetes-native CI/CD framework used by engineers and developers to construct workflows that build, test, and deploy code to a cloud or on-premise Kubernetes cluster.

Tekton consists of five main concepts:

- **Steps:** A step is the smallest unit for building workflows with Tekton. Block elements such as arguments, images, and commands are defined in steps.
- **Tasks:** A task element is a combination of steps that are expressed in sequential order.
- **Pipelines:** A pipeline is a combination of tasks ordered sequentially. It can be set up to run concurrently depending on the use case. The inputs, outputs, and workflow parameters can be specified as well.
- **TaskRuns:** As the name implies, a TaskRun element instantiates specific tasks. It also specifies details required for a task to run a Git repository as well as [container registry](/blog/how-to-setup-and-use-amazons-elastic-container-registry) information.
- **PipelineRuns:** A PipelineRun is the final element in the hierarchy. Similar to TaskRun, it instantiates specific pipeline elements. It also specifies the desired runtime information such as a Git repository and container registry.

All of these Tekton elements are configured as custom resource definitions (CRDs) on Kubernetes. These CRDs are customizable and reusable, thereby extending your Kubernetes capabilities. You can use these CRDs to orchestrate workflows such as checking out code from a Git repository, linting the codebase, checking for vulnerabilities in the container images, deploying to a container registry with the appropriate tags, and updating the actual state of the cluster with changes from the new state configurations. This build workflow can be performed across multiple providers and on-premise systems.

To learn more about Tekton, check out the [official documentation](https://tekton.dev/docs/concepts/).

## Building an Application Using Tekton

![Application Building]({{site.images}}{{page.slug}}/build-app.jpg)\

For this example, you're going to package a Node.js application using Docker, push it to Docker Hub, then automatically deploy it to Kubernetes using Tekton. For a sample Node.js application, check the [GitHub repository](https://github.com/Joeshiett/tekton-test) for this tutorial.

### Prerequisites

For this tutorial, you'll need the following.

#### A Kubernetes Cluster

You'll need a cluster to run Tekton and deploy the sample Node.js application. This tutorial uses the lightweight Kubernetes distribution [MicroK8s](https://microk8s.io/docs/getting-started) version 1.23.5, installed on Ubuntu 20.04 via Snap package manager. This cluster must have role-based access control (RBAC) enabled and [`ClusterRole` and `ClusterRoleBinding`](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#rolebinding-and-clusterrolebinding) definitions created for the `cluster-admin` user so that you can create any resource and freely interact with your cluster.

Note that if you're using MicroK8s, you'll have to configure it to export its kubectl configuration to `$HOME/.kube/config` with this command:

~~~{.bash caption=">_"}
microk8s.kubectl config view --raw > $HOME/.kube/config
~~~

This Kubernetes cluster must have [MetalLB](https://metallb.universe.tf/) enabled so the load balancer service can attach an IP address to the Node.js deployment. This makes it accessible outside the cluster.

This cluster must also have a storage class enabled so that `PersistentVolumeClaim` definitions can be created and used by the Tekton pipeline.

#### Kubectl

You need the kubectl command line utility to be able to interact with your Kubernetes cluster. This tutorial uses kubectl version 1.23.

#### A Docker Hub Account

You need access to a public registry on Docker Hub to deploy your built image to. You can [create an account](https://hub.docker.com/) if you haven't already.

## Installing Tekton Pipelines

[Tekton Pipelines](https://tekton.dev/docs/pipelines/) is a Kubernetes extension and the core of the Tekton project. With Tekton Pipelines installed in your cluster, you can define the Kubernetes custom resources needed to build your CI/CD pipeline.

Run the following command to install:

~~~{.bash caption=">_"}
kubectl apply --filename \
https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml
~~~

![Applying Tekton Pipelines resources to the cluster]({{site.images}}{{page.slug}}/MK958SI.jpg)

Verify the Tekton controller and webhook pods are up and running:

~~~{.bash caption=">_"}
kubectl get po -n tekton-pipelines
~~~

![Tekton controller and webhook deployed]({{site.images}}{{page.slug}}/s6tACwr.jpg)

## Installing the Tekton CLI (Tkn)

Although you can still interact with Tekton using kubectl, for this tutorial you'll use the Tekton CLI (`tkn`) to install tasks from the [Tekton Catalog](https://github.com/tektoncd/catalog), which contains reusable Tekton tasks that you'll be using.

To install `tkn` on your operating system, [follow the instructions](https://github.com/tektoncd/cli#installing-tkn). This tutorial uses the Ubuntu 20.04 operating system with `tkn` version 0.23.1.

## Installing Tasks From Tekton Hub

You don't need to create your tasks from scratch. There are plenty of Tekton resources, such as tasks and pipelines, that are available at the [Tekton Hub](https://hub.tekton.dev/) and frequently updated by contributors.

To build and deploy the sample Node.js application, you need to install the following tasks from the Tekton Hub.

Install `git-clone` to clone the Node.js project Git repository:

~~~{.bash caption=">_"}
tkn hub install task git-clone --version 0.6
~~~

Next, install `buildah` to build and push the image to Docker Hub:

~~~{.bash caption=">_"}
tkn hub install task buildah --version 0.3
~~~

Lastly, install `kubernetes-actions` to apply the Kubernetes deployment manifest to the cluster:

~~~{.bash caption=">_"}
tkn hub install task kubernetes-actions --version 0.2
~~~

To confirm the tasks have been installed successfully, list them:

~~~{.bash caption=">_"}
tkn task list
~~~

![Listing installed tasks]({{site.images}}{{page.slug}}/aAturnr.jpg)

## Creating the Secret and ServiceAccount Manifest

You're going to create the secrets that the Buildah runtime will use to push the image to your public Docker registry on Docker Hub.

Create a file called `secret-sa.yml` in the `tekton` directory and add the following code snippet, replacing `DOCKERHUB_USER` and `DOCKERHUB_PASSWORD` with your Docker Hub credentials:

~~~{.bash caption=">_"}
apiVersion: v1
kind: Secret
metadata:
  name: docker-secret
  annotations:
    tekton.dev/docker-0: https://index.docker.io/
type: kubernetes.io/basic-auth
stringData:
  username: DOCKERHUB_USER
  password: DOCKERHUB_PASSWORD