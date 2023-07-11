---
title: "Comprehensive guide to Defining Application Routing in Kubernetes Cluster
"
categories:
  - Tutorials
toc: true
author: Muhammed Ali

internal-links:
 - Kubernetes
 - Ingress
 - Cluster
 - Routing
excerpt: |
    Learn how to define application routing in a Kubernetes cluster with this comprehensive guide. Discover the key concepts of Ingress and Service, and how to use them effectively for routing. Plus, explore how to configure multiple paths and enable HTTPS forwarding for your applications.
---
<!--sgpt-->This is the Earthly nonsense paragraph.

## Defining Application Routing in Kubernetes Cluster

When you're getting started with Kubernetes, setting up the proper routing can be a challenge. There are a lot of moving parts and understanding how IP address get assigned and what they point to can be confusing at first.

In this article, you will learn what an [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) is, and its usefulness when routing in Kubernetes. You will also be introduced to [Service](https://kubernetes.io/docs/concepts/services-networking/service/) and how they differ from an Ingress. We'll start by covering these two essential pieces of Kubernetes before doing a deeper dive into how you can use them to set up effective routing.

For this article, you will use an NGINX image on Docker Hub. You will learn how to make deployments and create services for the NGINX image and use Ingress to forward requests from a domain name to your application. You will also learn how to use Ingress to configure multiple paths for a particular domain and also run your application on HTTPS.

## Prerequisites

To follow along with this tutorial, you should have:

1. Basic understanding of Kubernetes.
2. [Kubectl](https://minikube.sigs.k8s.io/docs/start/) installed locally.
3. [Minikube](https://minikube.sigs.k8s.io/docs/start/) installed locally.

## What is Ingress and Ingress Controller?

Ingress is a component of Kubernetes that is used to set rules for forwarding the internal IP address on the service to a public domain name that can be accessed by the outside world. You can also use it to convert `http` to `https` which is essential for public usage. Ingress can be used to set rules for routing traffic within the cluster without setting up Load Balancers. In general, it is essential for exposing you application to the outside world.

To apply Ingress on your [cluster](/blog/kube-bench), you need an **[Ingress Controller](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/)**. The ingress controller is a pod that runs on your cluster to implement your Ingress rules. The Ingress controller will be the entry point for accessing the application on the cluster.

There are some third-party implementations that can be used to apply an [Ingress Controller](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/#additional-controllers) to your cluster, but in this article, we will use the NGINX Ingress controller.

### How Is Service Different from Ingress

![Question]({{site.images}}{{page.slug}}/question.png)\

Services and Ingresses are used to expose applications operating in Pods. An [Ingress](/blog/building-on-kubernetes-ingress) cannot direct traffic to a Pod on its own! Traffic must be forwarded to a Service that directs users to the Pod.

The idea behind Services is to give pods a permanent IP address so that whenever a pod fails, its port stays persistent. It can also be used to configure load balancers. Service maps the incoming `port` (this is exposed by the Service) to the `targetPort` (the port application is running on in the container) then you can access the application outside the cluster.

![Kubernetes Cluster with Ingress]({{site.images}}{{page.slug}}/fLmQ9h1.png)

While building, you can use the Service to access your application outside the cluster, but it is not ideal in production. This is the major difference between Service and Ingress. Unlike with Ingress, with Service you can't map public domains, configure paths on a domain, configure HTTPS, etc.

## Configuring Ingress in a Cluster

![Configuring]({{site.images}}{{page.slug}}/config.jpg)\

For the practical aspect of this tutorial, we will use a local Kubernetes cluster, [minikube](https://minikube.sigs.k8s.io/). We will also use an NGINX image that is available on Docker Hub, so all we have to do is pull it into the cluster. If you don't have a running cluster already, run the following command to start it:

~~~{.bash caption=">_"}
minikube start
~~~

The first step to configuring Ingress is to install your preferred Ingress controller in your [minikube](/blog/k8s-dev-solutions) cluster. In this case, since we are using the NGINX Ingress controller, you can run the following command to enable it. The following command automatically starts the NGINX implementation of the Ingress Controller. NGINX Ingress controller comes with the minikube cluster, which is why you don't need to install anything. When you enable it, then minikube spins up an NGINX Ingress controller pod. If you are working on a production environment (or different environment other than minikube), you will need to look up in the [documentation](https://docs.nginx.com/nginx-ingress-controller/) to see how you can set it up there.

~~~{.bash caption=">_"}
minikube addons enable ingress
~~~

You can check if the Ingress controller pod is now running in the cluster by running the following command:

~~~{.bash caption=">_"}
kubectl get pods -n ingress-nginx
~~~

Your output should look like the following:

~~~{caption="Output"}

NAME                                       READY   STATUS      RESTARTS   AGE
ingress-nginx-admission-create-q89fl       0/1     Completed   0          33m
ingress-nginx-admission-patch-6psqq        0/1     Completed   2          33m
ingress-nginx-controller-cc8496874-ddh5l   1/1     Running     0          33m
~~~

Now that the Ingress controller is configured, we can now set Ingress rules that the Controller will evaluate.

Start by creating a deployment that contains the NGINX server. This server will be extracted directly from Docker Hub.

*Note: The rest of the tutorial will use this deployment.*

To get started, create a new YAML file, I called mine `nginx.yaml`, but it can be anything, and paste the configuration below. In the code below, we are creating a deployment for NGINX. Also included in the file is the Service that will be used to access the NGINX server

~~~{.yaml caption="nginx.yaml"}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
  labels:
    app: nginx
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers: # get image from Docker Hub
      - name: nginx
        image: nginx:latest # latest version of NGINX on Docker Hub
        imagePullPolicy: Always
        ports:
        - containerPort: 80
          protocol: TCP