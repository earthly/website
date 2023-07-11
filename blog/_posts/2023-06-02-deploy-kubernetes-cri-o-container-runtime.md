---
title: "How To Deploy a Kubernetes Cluster Using the CRI-O Container Runtime"
categories:
  - Tutorials
toc: true
author: Mercy Bassey
editor: Mustapha Ahmad Ayodeji

internal-links:
 - Kubernetes
 - Container
 - CRI-O
 - Automation
excerpt: |
    Learn how to deploy a Kubernetes cluster using the CRI-O container runtime. This tutorial provides step-by-step instructions for setting up the necessary components, configuring the cluster, and deploying your first application.
---
<!--sgpt-->**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. This article is about deploying a Kubernetes cluster using the CRI-O container runtime. Earthly is a popular build tool for CI that can be used in combination with Dockerfiles, making it a great option for readers interested in deploying a Kubernetes cluster using the CRI-O container runtime. [Check us out](/).**

Are you tired of managing your containerized applications manually? Do you want a more efficient and automated way to deploy and manage your applications? Look no further than Kubernetes!

Kubernetes is a powerful platform for managing containerized applications, providing a unified API for managing containers and their associated resources, such as networking, storage, and security. And with the ability to work with different container runtimes like [Docker](https://docs.docker.com/), [Containerd](https://containerd.io/docs/getting-started/), [CRI-O](https://docs.openshift.com/container-platform/3.11/crio/crio_runtime.html) etc. you can choose the runtime that's best for your needs.

[CRI-O](https://cri-o.io/) is an optimized container engine specifically designed for Kubernetes. With CRI-O, you can enjoy all the benefits of Kubernetes while using a container runtime that is tailored to your needs.

In this article, you will learn how to deploy a Kubernetes cluster using the CRI-O container runtime. You'll learn everything you need to know, from setting up the necessary components to configuring your cluster and deploying your first application.

## Prerequisite

To follow along in this tutorial, you'll need the following:

- Understanding of Kubernetes and Linux commands.
- This tutorial uses a Linux machine with an Ubuntu 22.04 LTS (recommended) distribution. Any other version will work fine too.
- Virtual machines (VMs) as master and worker with at least the minimum specifications below:

| Nodes  | Specifications | IP Address |
|