---
title: "Using Canary Deployments in Kubernetes"
categories:
  - Tutorials
toc: true
author: Sooter Saalu
editor: Bala Priya C

internal-links:
 - Kubernetes
 - Canary
 - CI/CD
 - Deployments
excerpt: |
    Learn how to use canary deployments in Kubernetes to mitigate the risks of application updates and ensure zero downtime for your users. This article explains the concept of canary deployments, how they work in Kubernetes, and how to implement them in your CI/CD pipeline.
---
<!--sgpt-->**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. This article is about using canary deployments in Kubernetes. Canary deployments in Kubernetes are a roll-out strategy that allows you to test and observe updates or new deployments with a small percentage of users before rolling them out to the entire user base. [Check us out](/).**

Has a seemingly harmless update ever caused your application to fail in production? Canary deployments, like the proverbial canary in a coal mine, can help you mitigate the chaotic outcomes of such updates that can potentially cause critical downtime.

[Canary deployments](https://earthly.dev/blog/canary-deployment/) are based on the routing of user traffic such that you can compare, test, and observe the behavior of any update for a small percentage of users. They are an important roll-out strategy in [Kubernetes](https://kubernetes.io), especially when tweaks, updates, or entirely new deployments need to be tested. A canary deployment is an improved iteration of an existing deployment that includes all the necessary dependencies and application code. It exists alongside the original deployment and allows you to compare the behavior of different versions of your application side by side. It helps you test new features on a small percentage of users with minimal downtime and less impact on user experience.

In this article, you'll learn about canary deployments, why they're important, and how to use them to optimize your deployment process. You'll also learn how to fit them into an automatic CI/CD framework.

## Canary Deployments in Kubernetes

Generally, canary deployments involve making small staged releases or updates that are sent to a fraction of your users for live testing and observation. Once enough feedback is gathered and no bugs are encountered, the release can be rolled out to the rest of your user base.

This means that the original application is updated only *after* the quality of the update is assured and zero downtime for your users is guaranteed.

It also allows you to compare the behavior of both versions of the application, test the reception of new features, and how they behave in your production environment. You can tweak the percentage of users that will experience the updates, create experiments, and carry out monitored A/B tests to ensure the final version of your application is the best it can be.

## How You Can Use Canary Deployments in Kubernetes

At its core, a [canary deployment](/blog/canary-deployment) implements a clone of your production environment with a load balancer routing user traffic between the available environments based on your parameters. You can deploy canary rollouts in a similar manner to regular rollouts.

This feature is available for use on [minikube](https://minikube.sigs.k8s.io/docs/), cloud, or locally managed Kubernetes clusters.

Once added to your Kubernetes cluster, the canary deployment will be controlled by services using selectors and labels. This service provides or forwards traffic to the labeled Kubernetes environment or pod, making it simple to add or remove deployments.

Initially, you can have a specific percentage of users test the modified application, compare both the application deployments, and increase the user percentage as your monitoring and user tests produce no errors. This percentage can be gradually increased until all the users have tested the newer version of the application, and then the older version can be taken offline.

This gradual process alleviates any downtime and reduces the impact of your changes until they are tested live while streamlining the transition between application versions. If there are issues with a particular update, only a small section of the user base will be affected, and you can drop the canary deployment until a more stable update is in place.

![Canary deployment architecture diagram]({{site.images}}{{page.slug}}/laz6hB1.png)

## Default Kubernetes Request Flow

For canary deployments, the selectors and labels used in the config or YAML file are different than those used in regular deployments.

In Kubernetes, a deployment declares the desired states of pods and ReplicaSets. The Kubernetes controller helps a cluster move towards the desired state from its current state.

In this flow, you create a service to allow access to all created pods or replicas through a single IP or name, as it abstracts away the individual pod addresses to a specific service name and allows requests within the [cluster](/blog/kube-bench) to reach multiple pods. Then your ingress configuration sets a collection of rules allowing inbound connection to communicate with your cluster services.

In a Kubernetes cluster, you utilize these ingress objects to deploy your application and configure communication both within and outside the cluster.

![Typical Kubernetes request flow]({{site.images}}{{page.slug}}/J9toSTq.png)

### Deployment Definition

When defining a [deployment](/blog/deployment-strategies), you should set up the name of your deployment, the label (Nginx) to match its created objects, the number of replica pods, and the details of the pod to be created.

The following YAML declares a `sample-deployment`, which creates three pod copies of a labeled `nginx` application. This `nginx` application is built with a [Docker](https://www.docker.com/) image named `nginx:1.14.2` and is set to communicate outside of its container through port 8080:

~~~{.yaml caption=""}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sample-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 8080
~~~

You do not need to explicitly declare a deployment strategy; however, the default deployment strategy in Kubernetes is the [RollingUpdate](https://kubernetes.io/docs/tutorials/kubernetes-basics/update/update-intro/) strategy, where pods containing updates replace old pods continuously until all pods are updated. This process is often quick and can be rolled back to a previous deployment.

### Service Definition

Next, you have a service definition matching your deployment labeling and defining access ports for the deployment:

~~~{.yaml caption=""}
apiVersion: v1
kind: Service
metadata:
  name: sample-service
spec:
  selector:
    app: nginx
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
~~~

This code will create a `sample-service` object in your cluster, which binds itself to any pod running `nginx`, defined by the selector label. Any newly created pod from that deployment will also gain access to this service.

It's important to note the name given to the service, the selector labels, and the ports.

### Ingress Definition

The ingress controller is ideal for exposing multiple services through a single external endpoint while also enabling rules to be defined for routing traffic. You can configure ingress controllers to extend your service capabilities and enable external access to your pods with more flexibility:

~~~{.yaml caption=""}
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: ingress-example
  annotations:
    kubernetes.io/ingress.class: nginx
  labels:
    app: nginx

spec:
  rules:
  -host: example.com
  - http:
      paths:
      - path: /
        backend:
          service:
            name: sample-service
            port:
              number: 80
~~~

This code connects to the defined service and extends its capabilities for connections outside the cluster.

### Canary Deployment

Suppose you have a running deployment. To set up a canary deployment, you need to create a replica deployment and a service object with an ingress configuration. This ingress configuration reroutes traffic based on set rules between the stable deployment and the canary deployment.

As such, most of the changes will be in the ingress file for canary development:

~~~{.yaml caption=""}