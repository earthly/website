---
title: "Helm: The Kubernetes Package Manager"
categories:
  - Tutorials
toc: true
author: Mercy Bassey
editor: Bala Priya C

internal-links:
 - Kubernetes
 - Helm 
 - Deployment
 - Charts
excerpt: |
    Learn how to use Helm, the Kubernetes package manager, to deploy complex applications quickly and efficiently. With Helm charts, you can package and distribute collections of Kubernetes YAML files, making deployments more manageable and reusable. Dive into this tutorial to deploy a MongoDB database on Kubernetes using Helm and explore the benefits of using Helm for your application deployments.
---
<!--sgpt-->This is the Earthly nonsense paragraph.

For production and hybrid cloud environments, manual deployments with Kubernetes are time consuming and non reusable. As you deploy different applications with similar configuration settings to Kubernetes, you'll have a large number of YAML files and substantial duplication; this makes the applications difficult to maintain. This is where Helm can help.

With Helm, you can deploy complex applications quickly as Helm charts, resulting in increased productivity, scalability, and [reusability](/blog/achieving-repeatability).

In this tutorial, you'll learn what Helm is, what Helm charts are, and how to deploy a MongoDB database up on Kubernetes with Helm.

## What Is Helm?

[Helm](https://helm.sh/docs/) is a package manager for Kubernetes. It was created in 2015 by [DeisLabs](https://deislabs.io/) as an open-source project and was donated to the Cloud Native Computing Foundation (CNCF) in June 2018 as a work in progress. Since April 2020 Helm has been used as the official package manager for Kubernetes.

With Helm, you can package different collections of Kubernetes YAML files and distribute them on public or private repositories as **Helm Charts**.

## What Are Helm Charts?

[Helm charts](https://helm.sh/docs/topics/charts/) are bundles or collections of Kubernetes YAML files that make up an application. For complex deployments involving database applications, such as MongoDB and MySQL, and monitoring applications like Prometheus, you can use the charts available in existing Helm repositories—without having to configure them yourself.

You can deploy complex applications with manifest files; but it can be difficult to maintain. The reusability of manifest files depends on the environment you choose to run them in.

With Helm, you can deploy different configurations for the same application using a single Helm chart. Helm uses a [template engine](https://pkg.go.dev/text/template) to achieve this. The template engine creates manifest files according to some input parameters which can be overwritten in a `vaues.yaml`file.

Helm charts are file based and follow a convention-based directory structure so they can be stored in chart repositories. Every chart comes with its own version number and other dependencies required to run an application.

Creating and sharing application configuration as charts makes Helm popular amongst developers. You can search for Helm charts on [Helm Search Hub‌](https://helm.sh/docs/helm/helm_search_hub/) or via the command line using the `helm search <keyword>` command. The [Artifact Hub](https://artifacthub.io/) is the main repository to look for a specific helm chart. All you have to do is search for the chart you'll need and the search results for that chart pops up as shown below:

<div class="wide">

![Viewing MongoDB helm chart]({{site.images}}{{page.slug}}/8edmxYX.png)

</div>

You can find Helm charts on GitHub, [GitLab](/blog/gitlab-ci), Bitbucket, and other related platforms. You can also get Helm charts from [verified publishers](https://blog.artifacthub.io/blog/verified-and-official-repos/#verified-publishers) like [Bitnami](https://bitnami.com/). Here's the Prometheus Helm chart made by Prometheus.

<div class="wide">

![Viewing Prometheus helm chart]({{site.images}}{{page.slug}}/hu7aW8m.png)

</div>

Now that you know what a Helm chart is, it's time to dive into its practical use case.

## Prerequisites

To follow along, you'll need to have the following;

- A Kubernetes cluster already up and running
- A Linux machine: This tutorial uses an Ubuntu distribution 20.0.3LTS (You can follow along on any Linux distro. )
- Helm locally installed - You can see the following [guide](https://phoenixnap.com/kb/install-helm)
- A valid domain name: This tutorial uses the domain name [*104-200-26-90.ip.linodeusercontent.com*](http://104-200-26-90.ip.linodeusercontent.com/)

You can find all the configuration settings used in this tutorial in [this](https://github.com/mercybassey/mongodb) GitHub repository.

## Deploying Applications With Kubernetes

When deploying applications to Kubernetes, you'll need to create  `Pod` and `Service` objects, and any other Kubernetes objects that you'll need to deploy your application (all configured in YAML files). To understand how this works, let's deploy a MongoDB database.

### Deploying a MongoDB Database Without a Helm Chart

Create a file called `mongodb-deployment.yaml`, open it up with your favourite code editor, and follow along with the steps outlined in this section.

In the `mongodb-deployment.yaml` file add the configuration settings below to create a *persistent volume* called `mongodb-pv` and a *persistent volume claim* called `mongodb-claim` to use some amount of storage from the persistent volume to persist data for the MongoDB database.

~~~{.yaml caption=""}
apiVersion: v1
kind: PersistentVolume
metadata:
   name: mongodb-pv # Name of the persistent volume
   labels:
     type: local
spec:
   storageClassName: hostpath # Name of the storage class for \
   local Kubernetes clusters
   capacity:
     storage: 3Gi # Amount of storage this volume should hold
   accessModes:
     - ReadWriteOnce # To be read and written only once
   hostPath: # Storage class type
     path: '/mnt/data' # File path to mount volume