---
title: "Using Spinnaker for Kubernetes Deployments"
categories:
  - Tutorials
toc: true
author: Sanni Michael
sidebar:
  nav: "deployment-strategies"
internal-links:
 - spinnaker
excerpt: |
    Learn how to use Spinnaker, an open-source continuous delivery platform, to automate and standardize software releases to Kubernetes clusters. This tutorial provides step-by-step instructions on setting up Spinnaker, configuring providers and storage, and deploying applications with pipelines.
---
**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. This article is about using Spinnaker for Kubernetes deployments. Earthly is a powerful build tool that can be used in conjunction with Spinnaker to automate and streamline the software release process to Kubernetes clusters. [Check us out](/).**

[Kubernetes has become the standard for deploying and managing containerized applications](https://newrelic.com/blog/how-to-relic/what-is-kubernetes), but there are a lot of questions to be answered in the cloud native space. And they all seem to center around a single theme:

How do you constantly release software with speed, quality, and confidence?  

This is where Spinnaker comes in. [Spinnaker is an open-source continuous delivery platform](https://spinnaker.io/) that offers an automated and repeatable process for releasing changes to major cloud platforms. In this article, you'll learn what Spinnaker is, its use cases, and how to deploy a sample application to your Kubernetes cluster using Spinnaker.

## So…What Does Spinnaker Do?

As a continuous delivery platform, Spinnaker gives development teams the ability to rapidly release software updates without worrying too much about the underlying cloud infrastructure. Teams can focus on writing code and developing features and leave Spinnaker to deal with:

- Automating and standardizing releases.
- Responding to deployment triggers. A deployment trigger could be a commit in GitHub or a job in [Jenkins](/blog/jenkins-stages-pipelines), for example.
- Easy integration with monitoring software like Prometheus, Stackdriver, or Datadog for data collection and analysis.

## Implementing Spinnaker

Before you dive in, there are a few prerequisites you need to have installed:

- [`kubectl`](https://kubernetes.io/docs/tasks/tools/)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
- [`eksctl`](https://docs.aws.amazon.com/eks/latest/userguide/eksctl.html)

### Step 1—Set Up Halyard

[Halyard](https://spinnaker.io/docs/reference/halyard/) is a CLI tool that manages the lifecycle of your Spinnaker deployment. You'll use it to write, validate and update deployment configurations.

There are two ways to set up Halyard:

- [Locally on Debian/Ubuntu or macOS](https://spinnaker.io/docs/setup/install/halyard/#install-on-debianubuntu-and-macos)
- [Using Docker](https://spinnaker.io/docs/setup/install/halyard/#install-halyard-on-docker)

This tutorial uses a local installation of Halyard on macOS.

Get the latest version of Halyard:

``` bash
curl -O https://raw.githubusercontent.com/spinnaker/halyard/master/install/macos/InstallHalyard.sh
```

Then, install it:

``` bash
sudo bash InstallHalyard.sh
```

And verify installation run:

``` bash
hal -v
```

### Step 2—Set Up a Cluster

This article uses [Elastic Kubernetes Service (EKS)](https://aws.amazon.com/eks/) for the Kubernetes cluster. You'll need to create a Kubernetes cluster or use an existing one.

Spinnaker uses a service account to communicate with the cluster, so set up a service account, a cluster role, and cluster role binding. Note that if you wish to allow Spinnaker access to specific namespaces, then you can use a role and role binding instead of a cluster role.

Create the [Amazon EKS](/blog/how-to-setup-and-use-amazons-elastic-container-registry) cluster for Spinnaker. `eksctl` is used for managing EKS clusters from the command line:

``` bash
eksctl create cluster --name=eks-spinnaker --nodes=2 --region=us-west-2 --write-kubeconfig=false
```

Let's break down the previous code snippet:

- `--name` specifies the name of the cluster.
- `--nodes` specifies how many worker nodes to set up.
- `--region` chooses a region where the cluster should be deployed.
- `--write-kubeconfig` disables writing the cluster config to the Kubernetes config file locally.

This takes around twenty minutes, so you might need to grab a cup of coffee. Once it's done, you should see something like this :

<div class="wide">
![An EKS cluster]({{site.images}}{{page.slug}}/qrmmB7g.png)
</div>

Retrieve the EKS cluster config and contexts:

``` bash
aws eks update-kubeconfig --name eks-spinnaker --region us-west-2 --alias eks-spinnaker
```

This command obtains the cluster config and contexts and appends them to your local kubeconfig file at `~/.kube/config`.

Set the current kubectl context to the cluster for Spinnaker:

``` bash
kubectl config use-context eks-spinnaker
```

To create a service account, cluster role, and cluster binding, first create a `service-account.yaml` file and paste this in:

``` yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
 name: spinnaker-role
 namespace: spinnaker
rules:
- apiGroups: [""]
  resources: ["namespaces", "configmaps", "events", "replicationcontrollers", "serviceaccounts", "pods/logs"]
  verbs: ["get", "list"]
- apiGroups: [""]
  resources: ["pods", "services", "secrets"]
  verbs: ["*"]
- apiGroups: ["autoscaling"]
  resources: ["horizontalpodautoscalers"]
  verbs: ["list", "get"]
- apiGroups: ["apps"]
  resources: ["controllerrevisions", "statefulsets"]
  verbs: ["list"]
- apiGroups: ["extensions", "app"]
  resources: ["deployments", "replicasets", "ingresses"]
  verbs: ["*"]
