---
title: "How to Manage Kubernetes Resources Using K9s"
categories:
  - Tutorials
toc: true
author: Boemo Wame Mmopelwa

internal-links:
 - Kubernetes
 - Linux
 - K9s
 - Kubectl
topic: kubernetes
excerpt: |
    Learn how to manage your Kubernetes cluster more efficiently with K9s, a terminal UI tool that simplifies common `kubectl` commands and provides a faster and easier way to interact with your cluster. Install K9s on Linux, explore its features, and discover how it can help you fetch cluster metrics and manage your resources with ease.
last_modified_at: 2023-07-19
---
**We're [Earthly](https://earthly.dev/). We simplify and speed up building software using containerization – perfect if you're into managing Kubernetes resources. [Give us a try](/).**

[Kubectl](https://kubernetes.io/docs/reference/kubectl/) is the de facto and most popular Kubernetes [command line tool](/blog/golang-command-line) used for accessing Kubernetes cluster metrics. However, one needs to know many commands to fetch metrics and operate a Kubernetes cluster using Kubectl. Though the CLI is robust, commands can quickly become cumbersome to run. For example, here is a command for editing a deployment:

~~~{.bash caption=">_"}
kubectl edit deployment/mydeployment -o yaml --save-config
~~~

Not the longest command, but typing things like this over an over can get cumbersome.
Fortunately, there is a terminal UI called [K9s](https://k9scli.io/) that makes interacting with your cluster faster and easier. It abstracts many common `kubectl` commands and maps them to just a few shortcut keys or clicks of the mouse.

In this tutorial, you will learn how to install K9s and use it to fetch cluster metrics and help manage your cluster.

## Installing K9s on Linux Distributions

Before you install K9s, make sure you install [kubectl](https://kubernetes.io/docs/tasks/tools/) if you haven't installed it already. This tutorial will use a [minikube cluster](https://earthly.dev/blog/minikube/) as an example project, but k9s works just as well with any type of Kubernetes cluster.

You can install k9s using [homebrew](/blog/homebrew-on-m1) with the following command.

~~~{.bash caption=">_"}
brew install derailed/k9s/k9s
~~~

This tutorial will focus on using k9s with Linux, but [versions are available](https://k9scli.io/topics/install/) for other operating systems as well.

Confirm the installation was successful by checking the version.

~~~{.bash caption=">_"}
k9s version
~~~

You will get the following output if K9s has been installed successfully:

~~~{.bash caption="Output"}
 ____  __.________
|    |/ _/   __   \______
|      < \____    /  ___/
|    |  \   /    /\___ \
|____|__ \ /____//____  >
        \/            \/

Version:    v0.25.18
Commit:     6085039f83cd5e8528c898cc1538f5b3287ce117
Date:       2021-12-28T16:53:21Z
~~~

To get started, use the `k9s -h` command to display all available commands. This will help you learn K9s faster and give you more clarity about certain commands. In addition, you can learn more about K9s from [K9s documentation](https://k9scli.io/).

~~~{.bash caption=">_"}
Available Commands:
  completion  generate the auto completion script for the specified shell
  help        Help about any command
  info        Print configuration info
  version     Print version/build info
~~~

## Giving K9s Access to Minikube Cluster Metrics

Before we can start using k9s, let us enable the metric-server add-on which will give K9s access to [minikube](/blog/k8s-dev-solutions) cluster metrics. Use the following command to allow K9s to collect metrics from your minikube cluster:

~~~{.bash caption=">_"}
minikube addons enable metrics-server
~~~

You will get the following output:

~~~{.bash caption="Output"}
{% raw %}
! Executing "docker container inspect minikube --format={{.State.Status}}" took
an unusually long time: 6.2066183s
* Restarting the docker service may improve performance.
* The 'metrics-server' addon is enabled
{% endraw %}
~~~

## Using the K9s UI Terminal

Use the following command to launch K9s on your terminal:

~~~{.bash caption=">_"}
k9s
~~~

You will get the following output that shows all clusters present in the Kubeconfig; K9s will automatically read from your Kubeconfig to get information related to your clusters. You can then press on the cluster you want to access:

<div class="wide">

![K9s UI terminal]({{site.images}}{{page.slug}}/MVWzn4m.jpg)\

</div>

If you click on the `0` digit on your computer, you will get all the namespaces in your cluster:

<div class="wide">

![Namespaces]({{site.images}}{{page.slug}}/ZbgGjYh.jpg)\

</div>

You can navigate through the UI terminal using the commands displayed on top of the UI table.

<div class="wide">

![Short keys]({{site.images}}{{page.slug}}/bqMSL9C.jpg)\

</div>

In addition, you can press the `?` key on your keyboard to get all available **short** keys:

<div class="wide">

![A list of short keys]({{site.images}}{{page.slug}}/LZE9kir.jpg)\

</div>

## Editing Resources

With k9s, it's easy to edit a specific manifest. By clicking on the letter `E`, K9s will give you the selected YAML file you want to edit in a text editor:

<div class="wide">

![Editing a manifest]({{site.images}}{{page.slug}}/xXNY5cT.jpg)\

</div>

Change the specifications and save the file, and then close the text editor to get back to the K9s terminal.

## How to Manage Your Cluster Using K9s

Setting up a [logging](/blog/understanding-docker-logging-and-log-files) management system to facilitate your logs can help you manage and track performance and resource issues in your cluster. A logging tool will provide facilities for sorting logs and most of all retrieving the logs later on. K9s will display your namespace's logs. To get a specific namespace's logs, click on the namespace and then click on the `L` key to display the logs.

K9s does not allow you to select text. If you want to copy the logs click on the `C` key.

<div class="wide">

![Fetching logs]({{site.images}}{{page.slug}}/ygZKdOW.jpg)\

</div>

To get a specific time range for displaying logs use the following numbers on your keyboard:

* 1: All logs over the last minute.
* 2: Over 5 minutes.
* 3: Over 15 minutes.
* 4: Over 30 minutes.
* 0: Over the entire lifetime of the pod.

<div class="wide">

![More log commands]({{site.images}}{{page.slug}}/TjS0n00.jpg)\

</div>

Use the escape key to get back to the main terminal.

## Getting Information About Your Cluster

K9s has a search bar which you can access by pressing the colon `:` and typing the resource you want to access. For example, if you press the colon and type "de" k9s will auto-complete to suggest the deploy resource. Press the tab button if you want to complete the suggestion and press enter to get access to the resource:

<div class="wide">

![Navigation]({{site.images}}{{page.slug}}/E1LADKe.jpg)\

</div>

To get your location in K9s, look at the bottom of the K9s UI terminal and you will see your location. The last component on the right is where you are currently at:

<div class="wide">

![Location in K9s]({{site.images}}{{page.slug}}/RoTRox7.jpg)\

</div>

The above picture shows that I am currently accessing the logs. If I press the escape button the [container](/blog/docker-slim) text will be highlighted as yellow to show that I am now accessing containers.

In case you want to go back, press on the escape key. You can also get other navigation features and tasks at the top of every section on K9s UI.

Whenever you need help press on the `?` key to get all keys that can be applied to the resources you selected.

Here are the basic navigation keys you will surely need:

<div class="wide">

![Navigation commands]({{site.images}}{{page.slug}}/gfXg2h0.jpg)\

</div>

Sorting objects and resources boosts your search capability. Use the following keys to sort components and find whatever you are looking for quickly:

<div class="wide">

![Sorting commands]({{site.images}}{{page.slug}}/XDDtbJu.jpg)\

</div>

## Describing Resources

With K9s you don't have to type in long commands to describe a namespace or any other Kubernetes resource; just press the letter `d` and you will get the description:

<div class="wide">

![Describing a namespace]({{site.images}}{{page.slug}}/AtkeKTA.jpg)\

</div>

## Getting an Overview of Resource Metrics

K9s makes cluster management easy because it enables you to get the number of created Statefulsets, DaemonSets, Deployments, and other resources using a command called `:pulses`. This command enhances accessibility because you can view the resources in one pane and most of all you can select the object to describe or edit it.

Before we try to use the `:pulses` command let's create two objects: a `StatefulSet`, deployment and a `service` so that we can get an output when using the `:pulses` command. Create a YAML file called `new-statefulset.yaml` and add the following content:

~~~{.yaml caption="new-statefulset.yaml"}
apiVersion: v1
kind: Service
metadata:
  name: nginx
  labels:
    app: nginx
spec:
  ports:
  - port: 80
    name: name
  clusterIP: None
  selector:
    app: nginx
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: earth
spec:
  selector:
    matchLabels:
      app: nginx
  serviceName: "nginx"
  replicas: 3
  template:
    metadata:
      labels:
        app: nginx
    spec:
      terminationGracePeriodSeconds: 10
      containers:
      - name: nginx
        image: k8s.gcr.io/nginx-slim:0.8
        ports:
        - containerPort: 80
          name: earth
~~~

Use the following command to apply the above objects to the cluster:

~~~{.bash caption=">_"}
kubectl apply -f new-statefulset.yaml
~~~

Next, create a file called `deployment.yaml` and add the following contents:

~~~{.yaml caption="deployment.yaml"}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: boemo-app
  namespace: earth
  labels:
    app: boemo-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: boemo-app
  template:
    metadata:
      labels:
        app: boemo-app
    spec:
      containers:
      - name: server
        image: nginx:1.17
        volumeMounts:
          - name: boemo-app
            mountPath: /usr/share/nginx/html
        ports:
        - containerPort: 80
          protocol: TCP
        resources:
          requests:
            cpu: 100m
            memory: "128M"
          limits:
            cpu: 100m
            memory: "256M"
        env:
        - name: LOG_LEVEL
          value: "DEBUG"
      volumes:
      - name: boemo-app
        configMap:
          name: boemo-app
          items:
          - key: body
            path: index.html
~~~

Apply the above object to your cluster. To get the number of resources and objects available type `:pulses` on the K9s terminal and you will get the following output:

<div class="wide">

![Object metrics]({{site.images}}{{page.slug}}/K2adC8G.jpg)\

</div>

## Draining Nodes and Killing Pods

If you want to drain your node, start by searching for the node and then select it. Press `r` to drain the node. You will get the following dialogue which will request information on the grace period and timeout.

<div class="wide">

![Draining pods]({{site.images}}{{page.slug}}/wSZn9vS.jpg)\

</div>

Press `ctrl + d` to delete a resource or `ctrl+k` if you want to kill a pod:

<div class="wide">

![Deleting a resource]({{site.images}}{{page.slug}}/pXrRkc2.jpg)\

</div>

## Conclusion

In this tutorial, we covered the basics of installing K9s on Linux and managing your cluster with it. Kubernetes is getting friendlier for newbies, thanks to out-of-tree plugins and tools like K9s. If you're just starting on Kubernetes and find Kubectl a bit tough, give K9s a shot - it's definitely a game-changer!

Speaking of game-changers, if you're loving K9s for Kubernetes management, you might also like [Earthly](https://www.earthly.dev/) for simplifying your build automation. It's another tool that can make your development process smoother and more efficient. Check it out!

{% include_html cta/bottom-cta.html %}
