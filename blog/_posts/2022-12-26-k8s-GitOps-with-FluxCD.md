---
title: "Kubernetes GitOps with FluxCD"
categories:
  - Tutorials
toc: true
author: Saka-Aiyedun Segun

internal-links:
 - Kubernetes
 - FluxCD
 - GitOps
 - Cluster
---

Kubernetes has become the go-to tool for application [deployment](/blog/deployment-strategies). However, it does not offer features for continuous integration and delivery. Continuous delivery can be particularly helpful for larger teams that host and update deployments frequently. One approach to maintaining continuous delivery for Kubernetes is GitOps.

**GitOps** is a software development practice that relies on a Git repository as its single source of truth. Descriptive configurations are committed to Git and then used to create continuous delivery environments. All aspects of the environment are defined via the Git repository; there are no standalone scripts or manual setups.

In this guide, you'll learn how to configure a continuous delivery pipeline with Flux for your Kubernetes cluster. You'll set up this pipeline imperatively by deploying the Flux Prometheus and Grafana monitoring stacks, and declaratively by deploying a '2048 game application' to your Kubernetes cluster.

Let's get started!

## What Is FluxCD?

[Flux](https://fluxcd.io/) is an open-source tool for automating application delivery pipelines to Kubernetes clusters based on GitOps principles. Flux makes use of source control platforms such as Git to allow users to describe their desired application state. It was originally created by Weaveworks but has recently been open-sourced.

Flux is quickly gaining popularity because it integrates with Kubernetes and is simple to set up. Flux, like [Terraform](/blog/kubernetes-terraform), allows DevOps engineers to deploy solutions to Kubernetes via a declarative configuration file that is simple to read and update.

![Flux Continuous Delivery Architecture ]({{site.images}}{{page.slug}}/bwYwEEQ.jpeg)

## Prerequisites

To follow along with this step-by-step tutorial, you should have the following:

Local installation of [Kubernetes](https://kubernetes.io/docs/tasks/tools/) and [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)
A [GitHub account](https://docs.github.com/en/get-started/signing-up-for-github/signing-up-for-a-new-github-account) and [GitHub CLI](https://cli.github.com/manual/installation)
Local installations of [Git](https://git-scm.com/downloads) and [Chocolatey](https://chocolatey.org/install)

## Installing Flux CLI

As a first step, you need to install **FluxCD CLI** on your local machine or a machine with access to your Kubernetes cluster. Flux CLI is a binary executable for all major platforms that implement the Flux architecture. It'll be used to bootstrap the FluxCD toolkit into your cluster.  
If you're using a Windows machine, run the command below to install Flux:

~~~{.bash caption=">_"}
choco install flux
~~~

Run the command below if you're on a Mac:

~~~{.bash caption=">_"}
brew install fluxcd/tap/flux
~~~

If you're using a Linux machine, run this command to install Flux:

~~~{.bash caption=">_"}
curl -s https://fluxcd.io/install.sh | sudo bash
~~~

You now have Flux installed on your machine; you can verify the installation with the `flux --version`  command.

## FluxCD Prerequisites Check

The next step is to run **FluxCD prerequisites check**. It is important to verify FluxCD's compatibility with your cluster before bootstrapping FluxCD toolkits into it. To do so, run the following command:

~~~{.bash caption=">_"}
flux check --pre
~~~

<div class="wide">
![Flux prerequisites checks]({{site.images}}{{page.slug}}/nvzSkid.jpeg)
</div>

## Bootstrapping FluxCD Toolkit Components

![Bootstrapping FluxCD Toolkit Components]({{site.images}}{{page.slug}}/ROJ79k6.png)

After the prerequisite check, the next step is to configure Github credentials and bootstrap Flux Toolkit into your cluster. Flux will use these components of the toolkits to add a CD pipeline on top of your existing Kubernetes cluster.

During the bootstrapping process, Flux creates a Git repository at a specified provider and initializes it with a default configuration. To do so, Flux requires your GitHub username and a personal access token.

Flux will automatically create a GitHub repository and attach the Flux Toolkit components to it. On GitHub, the repository will be available under your account.

This GitHub repository will contain all the configuration for the Flux core components in a [namespace](https://earthly.dev/blog/k8s-namespaces/).

<div class="notice--big--primary">
Flux automatically applies these configurations to your cluster in the specified [namespaces](/blog/k8s-namespaces). This behavior only applies if one or more configurations with the custom resource definitions, [HelmRelease](https://fluxcd.io/flux/components/helm/helmreleases/), [Kustomization](https://fluxcd.io/docs/components/kustomize/kustomization/), [GitRepository](https://fluxcd.io/docs/components/source/gitrepositories/), and [HelmRepository](https://fluxcd.io/docs/components/source/helmrepositories/) are added to this GitHub repository.
</div>

### Generating a Personal Access Token on GitHub

To generate a GitHub token, follow [these instructions](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).

### Configuring GitHub Credentials

If you're following along on a Mac or a Linux machine, run the following commands to configure GitHub Credentials:

~~~{.bash caption=">_"}
export GITHUB_USER=<username>
export GITHUB_TOKEN=<access-token>
~~~

If you're on a Windows machine, then run the following commands to configure GitHub Credentials:

~~~{.bash caption=">_"}
set GITHUB_USER=<username>
set GITHUB_TOKEN=<access-token>
~~~

### Bootstrapping the FluxCD Toolkit Into the Kubernetes Cluster

After you've configured your GitHub credentials, you're ready to bootstrap the Flux Toolkit inside your cluster. To do so, run the following commands:

~~~{.bash caption=">_"}

flux bootstrap github \\

--owner=$GITHUB_USER \\

--repository=fluxcd-demo \\
 
--branch=main \\

--path=./clusters/my-cluster \\

--personal
~~~

This command will create a GitHub repository in your GitHub account named `fluxcd-demo`, add the configurations for the Flux components into the repository, and bootstrap the components into your cluster in the namespace called `flux-system`.

<div class="wide">
![Bootstrapping Flux components]({{site.images}}{{page.slug}}/PpNGYJ.jpg)
</div>

Next, run the following commands to verify that the FluxCD Toolkits have been deployed in your cluster:

~~~{.bash caption=">_"}
kubectl get deployment -n flux-system
~~~

<div class="wide">
![Flux Components in flux-system namespace]({{site.images}}{{page.slug}}/WfMys5P.jpeg)
</div>

### FluxCD Toolkit Components

The Flux Toolkit has been bootstrapped into your cluster, and it consists of four main components:
Source Controller
Helm Controller
Kustomize Controller
Notification Controller

![Architectural Diagram of Flux [Source](https://fluxcd.io)](https://fluxcd.io/img/diagrams/gitops-toolkit.png)

#### Source Controller

[Source Controller](https://fluxcd.io/flux/components/source/) is a controller in a Kubernetes cluster that is responsible for acquiring artifacts, which are tar.gz files containing Kubernetes resource manifest data, from external sources. Based on semantic version policies, it can detect changes in these sources based on cryptographic signatures.

Additionally, the Source Controller can send outbound notifications when updates are available and react to inbound notifications for Git pushes and Helm chart uploads. Clients can access the Source Controller as a read-only service to retrieve artifacts.

#### Helm Controller

[Helm controller](https://fluxcd.io/flux/components/helm/) is the controller in a Kubernetes cluster that is responsible for managing Helm artifacts. The source controller obtains Helm charts from Helm repositories or other sources, and the Helm controller performs actions based on the creation, mutation, or removal of a HelmRelease resource in the cluster. The `HelmRelease` resource describes the desired state of a Helm release. Some parts of the Helm controller's work are shared with the Source Controller.

#### Kustomize Controller

[Kustomize Controller](https://fluxcd.io/flux/components/kustomize/)  is the controller in a Kubernetes cluster that is responsible for reconciling the cluster state with the desired state as defined by Commit manifests obtained from the Source controller. These manifests are used to distribute or apply resources to the cluster.

The Kustomize controller also supports health assessment of deployed resources and dependency ordering, enables garbage collection of deleted resources, and provides notifications of cluster state changes. It also manages permission access in a secure manner for multi-tenant clusters via Kubernetes Service Account impersonation and validates manifests against the Kubernetes API. Kustomizations can target and deliver resources to a remote cluster, even if that cluster does not have its own Flux controllers.

#### Notification Controller

[Notification Controller](https://fluxcd.io/flux/components/notification/) is a Kubernetes operator that specializes in handling inbound and outbound events. It is responsible for connecting to external systems, such as GitHub, GitLab, and the like. It's responsible for notifying the GitOps toolkit controllers about source changes. It also dispatches the events emitted by the GitOps toolkit controllers to external systems, such as Slack, Microsoft Teams, Discord, and RocketChat, based on the severity of the event and the objects involved.

In your browser, go to `https://github.com/your-github-username/fluxcd-demo` to confirm the repository that flux created, `https://github.com/your-github-username/fluxcd-demo/tree/main/clusters/my-cluster/flux-systemclusters/mycluster/flux-system/`, and view the configuration YAML files that Flux used to install the toolkit in your cluster.

<div class="wide">
![Flux Created Github Repository]({{site.images}}{{page.slug}}/PtIz8kg.jpeg)
</div>

## Automating Deployment To Cluster With Flux Cli

![Automating Deployment To Cluster With Flux Cli]({{site.images}}{{page.slug}}/3xIesos.png)

Your cluster now has Flux controllers installed with a [Github](/blog/ci-comparison) repository that was used to bootstrap the components. For all configuration and deployment, Flux will now use the `flux-demo` repository as a "source of truth".

If any configurations are stored, or changes are made to the toolkit components in the `fluxcd-demo` repository, the Flux toolkit automatically applies those configurations and changes to the cluster.

### Installing the FluxCD Prometheus and Grafana Stacks

Next, you should install the FluxCD Prometheus and Grafana stacks from the FluxCD official repository in an imperative way to display the options available in Flux. Registration of the Prometheus and Grafana Git repositories is *required* because it will create a Git source in Flux to monitor the repository for changes. To do so run the following commands:

~~~{.bash caption=">_"}
flux create source git flux-monitoring \ 
--interval=30m \ 
--url=https://github.com/fluxcd/flux2 \ 
--branch=main
~~~

Upon running this command, Flux creates a source repository called `flux-monitoring` in the repository Flux created. The URL for `flux-monitoring` will be set to Flux Repository, which contains the Prometheus and Grafana components. The main branch will be set as the reference to pull changes from, and the interval for checking the changes from the repository will be set to 30 minutes.

<div class="wide">

![Creating Git source for Flux-monitoring]({{site.images}}{{page.slug}}/wVcJF89.jpeg)

</div>

### Create a Kustomization Configuration

Next, run the `flux create` command below to create a kustomization configuration. This configuration applies the kube-prometheus-stack configurations stored in the official [Flux repository](https://github.com/fluxcd/flux2/tree/main/manifests/monitoring/kube-prometheus-stack) to your cluster.

~~~{.bash caption=">_"}
flux create kustomization kube-prometheus-stack \
  --interval=1h \
  --prune \
  --source=flux-monitoring \
  --path="./manifests/monitoring/kube-prometheus-stack" \
  --health-check-timeout=5m \
  --wait
~~~

Let's parse the above command:

* ** `flux create kustomization** kube-prometheus-stack` creates a Kustomization resource with the specified name in the Kubernetes cluster using the Flux tool.

* **--interval=1h** sets the Kustomization resource to update every 1 hour.

* **--prune** enables pruning of deleted resources from the cluster.

* **--source=flux-monitoring** specifies the source for the manifests used by the Kustomization resource.

* **--path="./manifests/monitoring/kube-prometheus-stack"** specifies the path to the manifests for the kube-prometheus-stack deployment.

* **--health-check-timeout=5m** sets the health check timeout to 5 minutes.

* **--wait** waits until the operation is complete.

This Kustomization resource can be used to manage the deployment of the kube-prometheus-stack in the cluster.

<div class="wide">
![Successfully applied Kustomization configuration]({{site.images}}{{page.slug}}/8m03taB.jpeg)
</div>

After installing the Kube-Prometheus-stack, the next step is to install Flux Grafana dashboards, which will be used to monitor and visualize the Flux control plane usage and reconciliation stats from the kube-Prometheus-stack.

~~~{.bash caption=">_"}
flux create kustomization monitoring-config \
  --depends-on=kube-prometheus-stack \
  --interval=1h \
  --prune=true \
  --source=flux-monitoring \
  --path="./manifests/monitoring/monitoring-config" \
  --health-check-timeout=1m \
  --wait
~~~

<div class="wide">

![Successfully Applied Kustomization configuration]({{site.images}}{{page.slug}}/8m03taB.jpeg)

</div>

Here's an overview of the command options:

* `flux create kustomization monitoring-config` creates a Kustomization resource with the specified name in the Kubernetes cluster using the Flux tool.

* **--depends-on=kube-prometheus-stack** specifies that the monitoring-config Kustomization resource depends on the kube-prometheus-stack deployment.

* **--interval=1h** sets the Kustomization resource to update every 1 hour.

* **--prune=true** enables pruning of deleted resources from the cluster.

* **--source=flux-monitoring** specifies the source for the manifests used by the Kustomization resource.

* **--path="./manifests/monitoring/monitoring-config"** specifies the path to the manifests for the monitoring-config deployment.

* **--health-check-timeout=1m** sets the health check timeout to 1 minute.

* **--wait** waits until the operation is complete.

This Kustomization resource can be used to manage the [deployment](/blog/deployment-strategies) of the monitoring-config in the cluster, ensuring that it depends on the kube-prometheus-stack deployment.

### Accessing the Grafana Dashboard

![Accessing the Grafana Dashboard]({{site.images}}{{page.slug}}/xzDcNjZ.png)

To access the Grafana dashboard, you need to forward traffic to the Grafana server. To do so, run the following commands:

~~~{.bash caption=">_"}
kubectl -n monitoring port-forward svc/kube-prometheus-stack-grafana 3001:80
~~~

To log in to your Grafana Dashboard, you should use the default credentials for the kube-Prometheus-stack.

~~~{.bash caption=">_"}
Username: admin
Password: prom-operator 
~~~

Navigate to <http://localhost:3001/d/flux-control-plane> if you're following along on your local machine. Navigate to your server's IP followed by port 3001 (<http://YOUR_SERVER_IP:3001/d/flux-control-plane>) if you're following along with a cloud server.

<div class="wide">

![Grafana Monitoring Dashboard]({{site.images}}{{page.slug}}/aOTsTMx.jpeg)

</div>

The Flux Prometheus and Grafana monitoring stacks have now been deployed to your cluster. These stacks were deployed to your cluster in an imperative manner, which works fine, but it goes against GitOps' principles of using Git repositories as the source of truth for managing deployments in a Kubernetes cluster.

The recommended way to deploy the monitoring stacks is the **declarative approach**. This involves defining the desired state of the cluster in Git repositories, using Git as the source of truth for deployments. The GitOps tooling can then be used to automatically reconcile the desired state with the actual state of the cluster. This approach allows for **better traceability** and control over the deployments, and it aligns with the principles of GitOps.

## Automating Deployment Declaratively to the Cluster with Flux

So far, you've used the Flux CLI to deploy Prometheus and Grafana stacks with Flux to your cluster. In this section, you will use a YAML file to deploy a 2048 game application to your cluster **declaratively**. You can templatize all of your Kubernetes deployment files to Git using this method, making it the source of everything in your Kubernetes environment. With this method, you can easily rollback and update your Kubernetes configuration files.

### Creating a Repository for the Manifests

The first step is to create a Git repository that will host your Kubernetes deployment manifest and FluxCD manifest. To do so, run the following commands:

~~~{.bash caption=">_"}
# create directory ~/2048

mkdir -p 2048/apps

# Switch to the ~/2048 directory and initialize a local Git repository.

cd ~/2048 && git init

~~~

Next, run the below `gh repo` command to create a public GitHub repository (2048). This repository will contain the 2048 game deployment manifest.

~~~{.bash caption=">_"}
gh repo create 2048 --public 
~~~

<div class="wide">
![Created Git Repository]({{site.images}}{{page.slug}}/tjGaG7K.jpeg)
</div>

You now have a Git repository created. The next step is to add the Kubernetes deployment manifest and the Flux manifest.

Now, you'll have to cd into the `app` directory:

~~~{.bash caption=">_"}
cd apps/
~~~

Now create `2048.yaml` in the app/ directory in your preferred editor and add the following configuration:

~~~{.yaml caption="2048.yaml"}
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: 2048-game
  name: 2048-game
spec:
  replicas: 2
  selector:
    matchLabels:
      app: 2048-game
  strategy: {}
  template:
    metadata:
      labels:
        app: 2048-game
    spec:
      containers:
      - image: alexwhen/docker-2048
        name: 2048-game
        ports:
        - containerPort: 80

---
apiVersion: v1
kind: Service
metadata:
  name: game-service
  labels:
    app: game-service
spec:
  ports:
  - name: 2048-game
    port: 80
  selector:
    app: 2048-game  
~~~

This YAML file defines a Deployment and a Service resource in the Kubernetes cluster. The Deployment resource creates two replicas of the 2048 game app and exposes them through a Service.

The Deployment resource uses the specified image for the 2048 game app and sets the container port to 80. It uses the specified labels to identify the app and the replicas, and it uses a matching selector to determine which replicas should be part of the deployment.

The Service resource exposes the 2048 game app replicas through a Service with the specified name and labels. It uses the specified port for the Service and uses the matching selector to determine which replicas should be included in the Service. This allows external clients to access the 2048 game app through the Service.

### Creating a Flux Configuration Manifest

The next step is to create a manifest for Flux configuration to deploy your 2048 game application. In the root folder, create a file named `flux.yaml` and add the following configuration.

~~~{.bash caption=">_"}
## change directory to the root folder (2048)
cd ..
~~~

~~~{.yaml caption="flux.yaml"}
apiVersion: source.toolkit.fluxcd.io/v1beta2
kind: GitRepository  
metadata:
  name: 2048-game 
  namespace: flux-system  
spec:
  interval: 1m  
  url: https://github.com/segunjkf/2048  
  ref:
    branch: main 
~~~

Let's take a closer look at the fields in the above configuration:

* **ApiVersion: source.toolkit.fluxcd.io/v1beta2** denotes the API version for the GitRepository resource.

* **Kind: GitRepository** specifies that this is a GitRepository resource.

* **Name: 2048-game** and **namespace: flux-system** are the metadata fields that specify the name of the GitRepository resource and the namespace in which the GitRepository resource should be created, respectively.

* **Interval:1m** sets the GitRepository resource to update every 1 minute.

* **Url<https://github.com/segunjkf/2048>** specifies the URL for the GitHub repository that contains the manifests for the 2048 game deployment. Please make sure to change this to the URL of the GitHub repository you created.

* **B
ranch: main** specifies the branch to use for the GitRepository resource.

~~~{.yaml caption="flux.yaml"}
apiVersion: kustomize.toolkit.fluxcd.io/v1beta2
kind: Kustomization
metadata:
  name: 2048-game
  namespace: flux-system
spec:
  interval: 5m0s 
  path: ./apps 
  prune: true
  sourceRef: 
    kind: GitRepository
    name: 2048-game
  targetNamespace: 2048-game 
~~~

Here,

* **ApiVersion: kustomize.toolkit.fluxcd.io/v1beta2** specifies the API version for the Kustomization resource.

* **Kind: Kustomization** indicates that this is a Kustomization resource.

* **Metadata** specifies the metadata for the resource, including the name and namespace.

* Other specifications include setting **interval: 5m0s** to update the Kustomization resource every 5 minutes and **path: ./apps** specifies the path to the Kubernetes deployment manifest in the Git repository. In this case, the path is "./apps".

At this point, the flux.yaml file would look like this:

~~~{.yaml caption="flux.yaml"}
apiVersion: source.toolkit.fluxcd.io/v1beta2
kind: GitRepository  
metadata:
  name: 2048-game 
  namespace: flux-system  
spec:
  interval: 1m 
  url: https://github.com/segunjkf/2048  
  ref:
    branch: main 
---
apiVersion: kustomize.toolkit.fluxcd.io/v1beta2
kind: Kustomization
metadata:
  name: 2048-game
  namespace: flux-system
spec:
  interval: 5m0s 
  path: ./apps 
  prune: true
  sourceRef: 
    kind: GitRepository
    name: 2048-game
  targetNamespace: 2048-game 
~~~

Now stage, commit, and push these files to your Git repository.

~~~{.bash caption=">_"}
cd ..

git add .

git commit -m "Automating Flux deployment" 

git branch -M main

## Replace the URL below with the url of the Git Repository you created 

git remote add origin https://github.com/segunjkf/2048.git

git push -u origin main
~~~

<div class="wide">

![Pushing changes to Github]({{site.images}}{{page.slug}}/3VMrhrw.jpeg)

</div>

Before applying the FluxCD configuration file, you must first create a namespace called '2048-game'. This is the namespace where the 2048 game will be hosted. To do so, run the following command:

~~~{.bash caption=">_"}
kubectl create namespace 2048-game
~~~

### Deploying the Application With Flux

Now apply the flux.yaml file to deploy your application with Flux:

~~~{.bash caption=">_"}
kubectl apply -f flux.yaml
~~~

After applying the Flux configuration file, you need to verify if FluxCD has deployed your application. To do so run the following command:

~~~{.bash caption=">_"}
kubectl get pods -n 2048-game
~~~

<div class="wide">

![Pods in the namespace]({{site.images}}{{page.slug}}/sKNfRwQ.jpeg)

</div>

Now, run the below kubectl command to port-forward port 8085 to port 80, the HTTP port for the 2048 game application running in a container. Doing so provides you access to the 2048 game application via a web browser.

~~~{.bash caption=">_"}
kubectl port-forward svc\2048-service -n 2048 8086:80
~~~

As you can see below, the 2048 service has been configured and listens for incoming connections via port 80.

<div class="wide">

![Port forwarding Session]({{site.images}}{{page.slug}}/xjl3AmT.jpeg)

</div>

Finally, open your favorite web browser and navigate to one of the following endpoints:

* <http://localhost:8086> (local) – If you're running a local Kubernetes cluster on your computer

* <http://SERVER_IP:8086> (cloud) – If you're running a Kubernetes cluster on a VM provisioned with a cloud provider. Replace <SERVER_IP> with your server's actual IP address.

![Accessing the 2048 game web UI]({{site.images}}{{page.slug}}/EsDYHXk.jpeg)

### Demonstrating FluxCD's Capabilities

To demonstrate FluxCD continuous delivery capabilities, you make changes to the Git repository and verify that Flux automatically applies the changes to your Kubernetes cluster.

 Open your favorite web browser and navigate to `https://github.com/segunjkf/2048/edit/main/apps/2048.yaml`. Make sure you replace `segunjkf` with your GitHub username.

<div class="wide">

![Making Changes to Git Repository]({{site.images}}{{page.slug}}/Why4uN6.jpeg)

</div>

Now edit the deployment file; change the `replicas` from 2 to 3, save, and commit the changes.

<div class="wide">

![Edited Kubernetes Manifest]({{site.images}}{{page.slug}}/PZsT4GN.jpeg)

</div>

Wait for a few minutes and confirm that FluxCD has applied the new changes to your cluster. ✅

~~~{.bash caption=">_"}
kubectl get pods -n 2048-game
~~~

<div class="wide">

![Pods running in the Namespace]({{site.images}}{{page.slug}}/Ep0PJ7V.jpeg)

</div>

To sum up, you have used Flux to set up a continuous delivery pipeline to your cluster. You deployed a Flux Prometheus and Grafana monitoring stack imperatively and the 2048-game application declaratively.

FluxCD also supports deployments with [Helm](https://fluxcd.io/flux/guides/helmreleases/) and [alerting system](https://fluxcd.io/flux/guides/notifications/) for notification.

## Conclusion

In this guide, you learned how Flux allows you to easily automate Kubernetes manifest deployment; you can push commits to watched repositories and have them automatically applied to your cluster, following GitOps practices.

In addition to GitHub, Flux can also retrieve and bootstrap Git repositories hosted on GitLab. For more information, visit the [official docs](https://fluxcd.io/docs/cmd/flux_bootstrap_gitlab/). Another popular GitOps tool is [ArgoCD](https://earthly.dev/blog/argocd-kubernetes/). Check out this [comprehensive guide](https://earthly.dev/blog/flux-vs-argo-cd/) to see how Flux and ArgoCD compare.

{% include cta/cta1.html %}
