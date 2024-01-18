---
title: "How Kubernetes Autoscaling Works"
categories:
  - Tutorials
toc: true
author: Kasper Siig

internal-links:
 - k8s
 - autoscaling
excerpt: |
    
last_modified_at: 2023-07-14
---
**This article examines Kubernetes autoscaling techniques. Earthly simplifies the build process for seamless Kubernetes deployments. [Learn more about Earthly](https://cloud.earthly.dev/login).**

There are many reasons engineers look to [Kubernetes](https://kubernetes.io/) when running their workloads, like support for containers and orchestration. Another major reason for choosing Kubernetes, though, is being able to automatically scale the services found within a cluster.

Configuring and using autoscaling within your cluster is a great way to make sure that the nodes within your cluster are using the optimal amount of resources, as running at a hundred percent isn't advisable. It's also a great aid in managing costs and making sure that you're not paying for anything you're not using.

In this article, you'll get a close-up look at why you want to use autoscaling in your cluster. Additionally, it'll offer insight into the three different ways that autoscaling can be handled in Kubernetes. You'll also be introduced to some third-party tools that can come in handy when working with autoscaling.

## Why Is Autoscaling Important?

![autoscaling]({{site.images}}{{page.slug}}/autoscaling.jpg)\

As mentioned in the introduction, there are several common reasons for wanting to use autoscaling. First and foremost among these is cost. When you've configured autoscaling correctly and optimally for your workload, you ensure that you're never paying for resources you aren't using. This is a particularly relevant concern for applications that encounter a lot of spikes in resource use.

Another major reason for wanting to configure autoscaling is to ensure that you're able to handle the load that your applications are receiving. A typical example of this is an e-commerce store, which may experience sudden spikes in traffic. This can be because of special events like Black Friday, a product that's gone viral, or a unique offer or sale that the store is offering. No matter what the cause is, any infrastructure administrator appreciates the ability to let the infrastructure take care of adding more resources rather than doing it manually.

You can also use autoscaling just to make sure that your cluster is running as efficiently as possible. As anyone who's ever worked with computers knows, it's not great to be running at a hundred percent capacity, as the server then has no other choice than to start prioritizing workloads, which will slow down some applications, and in some cases, even cause applications to start misbehaving. A proper autoscaling configuration can make sure this never happens.

## How Does Autoscaling Work?

![scaling]({{site.images}}{{page.slug}}/scaling.jpeg)\

In terms of Kubernetes, there are three main ways that autoscaling can be done. The pods themselves can be scaled horizontally or vertically, or the entire cluster can be scaled by adding more nodes to the cluster, a process aptly referred to as *cluster scaling*.

### Horizontal Pod Autoscaler

The [Horizontal Pod Autoscaler (HPA)](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/), quite unsurprisingly, takes care of scaling the pods horizontally. On a high level, the HPA will look at the resources running inside a Kubernetes cluster and determine what the needed action is. By default, it does this every fifteen seconds. If the resource usage of the pods is below the set threshold and the amount of pods is above the specified number needed, the HPA will decrease the number of pods.

Likewise, if the resource usage is above the specified amount and the number of pods is below the specified maximum number of pods, the HPA will increase the number of pods running.

### Vertical Pod Autoscaler

The [Vertical Pod Autoscaler (VPA)](https://github.com/kubernetes/autoscaler/tree/master/vertical-pod-autoscaler) takes care of scaling the pods vertically. Instead of adding more instances to take care of the workload, scaling vertically is the practice of adding more resources to the instances already running.

To understand this type of scaling inside Kubernetes, you need to understand a bit of [Kubernetes Resource Management](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/). While that could be an article on its own, the important thing to know is that Kubernetes handles resource allocation based on resource limits and resource requests. Resource limits are set primarily to make sure that applications can't suddenly spike and consume an excessive amount of resources, potentially taking up resources that should have been available to other applications. The resource requests, on the other hand, make sure that pods are scheduled onto nodes that have enough available resources.

The VPA takes care of scaling up both the requests and the limits of pods that are configured with it. The request is scaled up according to the usage of the pod, and the limit is adjusted to keep the same ratio between the request and the limit.

### Cluster Autoscaler

The third and final way that you can configure autoscaling in Kubernetes is by scaling up the entire cluster. The [Cluster Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler) takes care of increasing the number of nodes inside a cluster, thereby making sure that all pods have a place to run. This is often referred to as the Kubernetes autoscaler, and if you've clicked the links to the VPA and the Cluster Autoscaler, you'll notice that they even share the same repo.

The configuration for this type of autoscaling is the easiest to set up and is typically done through the cloud provider where your Kubernetes cluster is set up.

## Getting the Most Out of Autoscaling

To get the most out of your autoscaling setup, you need to make sure that it's configured according to what you need the most. The first point is to figure out what is most important for you: availability or cost.

The option you choose will help determine how you approach the setup, but there are a few common factors that you need to determine no matter what option you go for. First of all, you need to figure out how long it takes for your application to boot up and be ready to receive requests. Some applications may take five to ten minutes to be ready, which isn't good if you need to add ten more instances in a few minutes.

You also need to figure out how long it takes for the autoscaler to react to a change in traffic, which in some cases can add several minutes to the time it takes to upscale. The simplest way of gauging how long the autoscaler takes is by configuring autoscaling rules according to what you think you'll need and then performing a load test of your application to simulate an increase in traffic. This can be done using tools like [JMeter](https://jmeter.apache.org/). With this information, you can figure out what the thresholds for your metrics need to be.

To get a better understanding of how autoscaling works, consider a scenario where you have an app that experiences daily seasonality, meaning you have a need for autoscaling, but that need ramps relatively predictably rather than spiking unexpectedly. In this case, you have a good idea of how long it takes for your application to go from one percentage of usage to another. This makes it fairly easy for you to configure autoscaling.

Assuming that your application takes five minutes to boot up, you need to figure out the percentage from which it takes your application load five minutes to reach one hundred percent. If it takes five minutes to go from ninety percent to a hundred percent, then ninety percent is your absolute maximum threshold before scaling should begin.

Even in cases like this, where you have a fairly predictable pattern of use, you want to add a buffer to that. How big the buffer needs to be is determined by whether you are aiming for cost or availability. If you are aiming for cost, you may only want to add a buffer of five to ten percent, while if you're more concerned about availability, you may want to add a buffer of ten to fifteen percent.

## Using Lens for Managing Autoscaling

![Lens]({{site.images}}{{page.slug}}/KOeCRbC.png)

There are, of course, third-party tools to help make your life easier when it comes to autoscaling. One of these tools is [Lens](https://k8slens.dev/). Lens is a Kubernetes dashboard that focuses on making it easier to manage Kubernetes. One of the areas that it can help with is managing autoscaling configurations. You can keep track of how many nodes there are inside your cluster, how many pods are in a specific deployment, and change the configurations as you go.

It's worth taking a look at if you are exploring autoscaling, as it provides a more complete overview than what you may get from the command line.

## Conclusion

After reading this article, you know the basics of Kubernetes autoscaling. You're now more familiar with the reasons for wanting to utilize Kubernetes autoscaling, and perhaps you've recognized some of the use cases. You also know what the difference is between the HPA, the VPA, and the CA.

If you're looking to make your life easier in terms of Kubernetes deployments, it's worth checking out [Earthly](https://cloud.earthly.dev/login). They combine the best of Makefiles and Dockerfiles to provide a seamless deployment system.

{% include_html cta/bottom-cta.html %}
