---
title: "Can Rancher Help You Better Manage Kubernetes?"
categories:
  - Tutorials
toc: true
author: Damaso Sanoja
editor: Bala Priya C

internal-links:
 - Rancher
 - Deployment
 - Kubernetes
 - Clusters
excerpt: |
    Learn how Rancher can help you better manage your Kubernetes clusters, regardless of where they're hosted. With features like deploying managed Kubernetes clusters, importing existing clusters, enforcing security, and providing a centralized interface for multi-cluster management, Rancher simplifies the management and monitoring of your Kubernetes deployments.
last_modified_at: 2023-07-14
---
**This article is about Rancher Kubernetes management. Earthly provides precise build automation to enhance your CI pipeline's consistency and speed. [Check it out](https://cloud.earthly.dev/login).**

Recently, multi-cloud and hybrid cloud deployments have gained significant traction as they let you optimize costs, increase scalability, improve agility, and achieve greater operational resilience. However, with these [deployment strategies](/blog/deployment-strategies), managing different Kubernetes clusters with multiple tools and dashboards can be a challenge; Rancher can help you seamlessly manage such deployments at scale.

This article will explore the features and capabilities of [Rancher](https://rancher.com), an open source [Cloud Native Computing Foundation (CNCF) certified Kubernetes distribution](https://www.cncf.io/certification/software-conformance/) designed to make it easy to deploy, manage, and monitor multi-cluster environments from a centralized UI. Here, you'll learn about Rancher and the different deployment options it provides, and understand the aspects that [make](/blog/using-cmake) it unique.

## What Is Rancher?

The main goal of any Kubernetes distribution is to orchestrate container workloads. However, Rancher was created by [SUSE](https://www.suse.com/) to provide capabilities beyond those of conventional [Kubernetes](https://kubernetes.io/) distributions.
Rancher is an enterprise-grade platform that facilitates consistent administering of multiple Kubernetes clusters from a single UI—while addressing key Kubernetes pain points, such as cluster and workload deployment, security management, workload monitoring across multiple clusters, and scalability.

In a nutshell, Rancher simplifies managing, monitoring, importing, and provisioning Kubernetes clusters with just a few clicks from its intuitive UI. But how does Rancher achieve this? The following diagram gives you a high-level overview of the components that make it all possible:

<div class="wide">

![Rancher Architecture Diagram courtesy of Damaso Sanoja]({{site.images}}{{page.slug}}/MbC0MK0.png)

</div>

Here's a breakdown of the main components:

* **Rancher server**: You can think of the Rancher server as the heart of the Rancher cluster, as it includes key components, like [etcd](https://etcd.io), the authentication [proxy](/blog/mitmproxy), the Rancher API server, and cluster controllers. At a high level, its primary function is to allow users to manage, monitor, and provision other Kubernetes clusters through the Rancher UI.
* **[Rancher Kubernetes Engine (RKE)](https://rancher.com/docs/rke/latest/en/)**: *RKE* is a term used to refer to both the RKE library and the RKE command-line utility that can be used to create [RKE](https://rancher.com/products/rke) clusters. RKE is also a CNCF-certified Kubernetes distribution that runs entirely within [Docker](https://www.docker.com/) containers, similar to [K3s](https://k3s.io).
* **Cluster controllers and cluster agents**: These components are responsible for establishing secure communication between the Rancher server and each downstream Kubernetes cluster.
* **Authentication proxy**: On each Kubernetes API call, this component authenticates the caller with local or external authentication services and forwards that call to the appropriate downstream cluster.
* **Node agents**: Under normal circumstances, the `cattle-node-agent` performs several operations on [Rancher Launched Kubernetes](https://docs.ranchermanager.rancher.io/v2.5/pages-for-subheaders/launch-kubernetes-with-rancher) cluster nodes, such as creating or restoring `etcd` snapshots or upgrading the cluster to the latest version. However, each node agent can provide the same functionality as the cluster agent when the latter is not available.

If you're looking to delve deeper into the workings of Rancher server and its components, check out [the official documentation](https://docs.ranchermanager.rancher.io/reference-guides/rancher-manager-architecture/rancher-server-and-components).

## Key Features of Rancher

Now that you know the basics of Rancher, here are the key features that set it apart.

### Deploying Managed Kubernetes Clusters

Rancher allows your DevOps team to seamlessly deploy managed Kubernetes clusters on popular platforms, like [Amazon Elastic Kubernetes Service (EKS)](​​https://aws.amazon.com/eks/), [Azure Kubernetes Service (AKS)](https://azure.microsoft.com/en-us/products/kubernetes-service/), and [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine). It also has drivers that provide support to other vendors, like [DigitalOcean Kubernetes (DOKS)](https://github.com/digitalocean/DOKS), [Linode Kubernetes Engine (LKE)](https://www.linode.com/products/kubernetes/), [Alibaba Cloud Container Service for Kubernetes (ACK)](https://www.alibabacloud.com/product/kubernetes), [Baidu Cloud Container Engine (CCE)](https://intl.cloud.baidu.com/product/cce.html), [Huawei CCE](https://www.huaweicloud.com/intl/en-us/product/cce.html), [Open Telekom Cloud CCE](https://open-telekom-cloud.com/en/products-services/core-services/cloud-container-engine), [Oracle Container Engine for Kubernetes (OKE)](https://www.oracle.com/cloud/cloud-native/container-engine-kubernetes/), and [Tencent Kubernetes Engine (TKE)](https://www.tencentcloud.com/products/tke). With Rancher, development teams can easily create [custom drivers](https://github.com/rancher-plugins/kontainer-engine-driver-example), making it possible for Rancher to support virtually *any* existing Kubernetes platform.

### Deploying Kubernetes Clusters on Any Infrastructure

Rancher's flexibility is not limited to deploying Kubernetes clusters on managed platforms. You can also provision and install Kubernetes on-premise or in compute nodes, like Microsoft [Azure](/blog/continuous-integration), [Cloudscale](https://cloudscale.io/), Google, [Amazon Elastic Compute Cloud (Amazon EC2)](https://aws.amazon.com/ec2/), [Alibaba Cloud Elastic Compute Service (ECS)](https://www.alibabacloud.com/product/ecs), [OpenStack](https://www.openstack.org/), and [VMware vSphere](https://www.vmware.com/asean/products/vsphere.html),to name a few. This allows you to create Kubernetes clusters tailored to your organization's needs while avoiding vendor lock-in.

### Importing Existing Kubernetes Clusters

Deploying and provisioning Kubernetes clusters is a helpful feature, but Rancher offers more. From the Rancher UI, you can also import existing Kubernetes clusters to be managed and monitored from a single unified interface.

### Enforcing Security Across Kubernetes Clusters

Rancher lets your organization enforce [enterprise-level security](https://docs.ranchermanager.rancher.io/pages-for-subheaders/rancher-security) using a central dashboard from which you can manage users, groups, Kubernetes cluster roles, pod security policies, and authentication. Additionally, Rancher provides out-of-the-box support for  [NeuVector](https://neuvector.com), a container-focused open source security application, [Istio](https://istio.io), and [Center for Internet Security Inc. (CIS) security scans](https://www.cisecurity.org) to ensure that the best security practices are implemented.

### Built-In Active Directory, LDAP, and SAML Support

Rancher enforces security and convenience by facilitating authentication mechanisms, such as Active Directory (AD), Azure AD, GitHub, Google, Security Assertion Markup Language (SAML) support for Lightweight Directory Access Protocol (LDAP), and [Okta](https://www.okta.com/).

### Enterprise Support with No Vendor Lock-In

Rancher offers enterprise-level support with the benefit of not tying your organization to a particular vendor; the teams can decide which Kubernetes distro to use depending on the specific use case.

### One Interface to Rule Them All

The biggest advantage of Rancher is the convenience of managing all your Kubernetes clusters from a single dashboard. This eliminates the complexity and inconvenience of accessing vendor-specific dashboards and management tools.

### Easy To Install

Rancher is easy to install both in the cloud and on premise, which makes it optimal for both development and production.

The previous list is just a fraction of the features Rancher brings to DevOps teams. To learn more about all of Rancher's features that DevOps teams can use, check out [the documentation](https://docs.ranchermanager.rancher.io/getting-started/introduction/overview).

## Setup and Maintenance in Rancher

Unlike most Kubernetes distributions, Rancher can be easily installed in virtually any environment, including virtual machines (VMs), containers, hosted Kubernetes, cloud infrastructures, on premise, and the edge. To that end, you can set up Rancher using a Docker container, [Helm](https://helm.sh/) charts, RKE, and more. The following are some scenarios and the recommended environments:

* **Development and testing purposes**: The easiest way to test Rancher is to [install it on a single node using Docker](https://docs.ranchermanager.rancher.io/pages-for-subheaders/rancher-on-a-single-node-with-docker). Another alternative for development and testing purposes is to [use the RKE binary to set up an RKE cluster](https://rancher.com/docs/rke/latest/en/installation/) on VMs or physical nodes running Docker. In this scenario, binaries are available for macOS, Linux x64, Linux ARM (32/64), and Windows (32/64), making it easy to get single or multiple-node RKE clusters up and running in no time. In turn, you can install Rancher on top of such cluster using the [Helm quick start guide](https://docs.ranchermanager.rancher.io/getting-started/quick-start-guides/deploy-rancher-manager/helm-cli) to emulate a production environment. You can as well install Rancher on top of another lightweight Kubernetes distribution like K3s.
* **Production environments**: The best practice for running Rancher in production is to set up a dedicated high-availability (HA) Kubernetes cluster with at least three nodes, a load balancer, and a DNS record. This way, each node can act as a control plane, etcd, and worker, if necessary. You can find more information about HA installations [in Rancher's how-to guides](https://docs.ranchermanager.rancher.io/how-to-guides/new-user-guides/kubernetes-cluster-setup/high-availability-installs). Rancher documentation provides several guides regarding this topic:
  * [Setting Up a High-Availability K3s Kubernetes Cluster for Rancher](https://docs.ranchermanager.rancher.io/how-to-guides/new-user-guides/kubernetes-cluster-setup/k3s-for-rancher)
  * [Setting Up a High-Availability RKE Kubernetes Cluster](https://docs.ranchermanager.rancher.io/how-to-guides/new-user-guides/kubernetes-cluster-setup/rke1-for-rancher)
  * [Setting Up a High-Availability RKE2 Kubernetes Cluster for Rancher](https://docs.ranchermanager.rancher.io/how-to-guides/new-user-guides/kubernetes-cluster-setup/rke2-for-rancher)

The above-listed procedures involve creating a configuration file and then running a script that uses RKE to provision each node. Alternatively, you can use an existing HA cluster and apply Helm charts to install Rancher on top of Kubernetes. In summary, setting up Rancher is straightforward.

Regardless of the method selected, once you've installed Rancher, you'll see the login screen:

<div class="wide">

![Rancher login]({{site.images}}{{page.slug}}/XRqZQuO.png)

</div>

Next, you need to create a new admin password for the Rancher UI:

<div class="wide">

![Rancher admin password]({{site.images}}{{page.slug}}/IVU3FoR.png)

</div>

You then need to confirm the access URL:

<div class="wide">

![Rancher URL]({{site.images}}{{page.slug}}/4vDAC4G.png)

</div>

With Rancher, upgrading, or reverting to a previous version is easy.
If you use a single-node Rancher server on Docker, all you have to do is run the container with the desired version.
If you installed Rancher using RKE or Helm charts, you should run `helm upgrade`.

## Rancher Versions

If you want to use Rancher in production, it's recommended to use the latest stable version. However, to test new builds of Rancher, you may want to use other versions. In [the Rancher "Getting Started" docs](https://docs.ranchermanager.rancher.io/getting-started/installation-and-upgrade/resources/choose-a-rancher-version), you can find more information on how to choose a version of Rancher using Helm charts or Docker images. Additionally, in [this SUSE documentation](https://www.suse.com/suse-rancher/support-matrix/all-supported-versions/rancher-v2-6-7/), you can find the Rancher support matrix.

## Use Cases Where Rancher Excels

You've already learned about some of Rancher's most notable features. Here are some aspects that make this tool unique.

### Kubernetes Deployment and Monitoring on Any Infrastructure

Rancher allows you to deploy Kubernetes clusters on any infrastructure from its convenient UI.

The following screen shows Rancher's main dashboard. Note that only the cluster from which Rancher is running is displayed. To add more clusters, click the **Add Cluster** button located on the top right:

<div class="wide">

![**Add Cluster**]({{site.images}}{{page.slug}}/Djna2a1.png)

</div>

The next screen asks you to select the type of cluster to deploy. At this point, you have these options:

* Register an existing Kubernetes cluster
* Create a new Kubernetes cluster using existing nodes
* Create a new Kubernetes cluster on new nodes

Here's an example; you create a new Kubernetes cluster on new DigitalOcean nodes:

<div class="wide">

![Choose infrastructure or provider]({{site.images}}{{page.slug}}/w0XbsAv.png)

</div>

The next screen lets you create node pools, select a network provider, set the number of nodes, create labels, and much more. From here, you can fully configure the Kubernetes cluster. Once that configuration is ready, you can deploy the cluster:

<div class="wide">

![Configure node options 2]({{site.images}}{{page.slug}}/fAyORCQ.png)

</div>

The next screen shows the main dashboard, where you can see how the cluster is provisioned in real time:

<div class="wide">

![Rancher provisioning 1]({{site.images}}{{page.slug}}/H8TDw9o.png)

</div>

For reference, the following is a screenshot of the DigitalOcean dashboard where you can see how the cluster is provisioned:

<div class="wide">

![Rancher provisioning 2]({{site.images}}{{page.slug}}/Om074Tr.png)

</div>

Once the process is complete, both clusters will be listed in the Rancher dashboard:

<div class="wide">

![New cluster]({{site.images}}{{page.slug}}/csaB5X3.png)

</div>

The hamburger menu to the right of the cluster allows you to perform some basic operations, like editing the cluster, taking a snapshot of the cluster, running a CIS scan, and deleting the cluster:

<div class="wide">

![Cluster management]({{site.images}}{{page.slug}}/uzIHH7K.png)

</div>

If you click on any of the clusters, you will be taken to a screen where you can see the key metrics of each cluster:

<div class="wide">

![Local cluster monitoring]({{site.images}}{{page.slug}}/nwmJOEc.png)

![DigitalOcean cluster monitoring]({{site.images}}{{page.slug}}/SUz4S2j.png)

</div>

If you're familiar with DigitalOcean, you may be interested in knowing which OS was used for each node and the specifications of the RAM, vCPU, and storage (the specific Droplet). An advantage of Rancher is that you can create and manage node templates for any supported host provider and then use those templates during cluster creation. Take a look at this example:

<div class="wide">

![Add node template]({{site.images}}{{page.slug}}/qGY2rTU.png)

</div>

The procedure for deploying managed Kubernetes clusters is similar. In all cases, you must previously configure the necessary access tokens. This will enable the cluster controller to communicate correctly with the cluster agent and perform all the necessary operations.

### Management of Multi-Cluster and Hybrid-Cluster Environments from a Single Interface

But can Rancher help you better manage Kubernetes? In short, the answer is yes.

Go back for a moment to one of the previous screenshots:

<div class="wide">

![DigitalOcean cluster monitoring]({{site.images}}{{page.slug}}/SUz4S2j.png)

</div>

At the top right, you can see a button labeled **Launch kubectl**. If you click on it, another screen similar to the following will be displayed:

<div class="wide">

![kubectl screen]({{site.images}}{{page.slug}}/dbF6OYA.png)

</div>

From here, you can run any command on the selected cluster. As shown, the kubectl `get pods -A` command has been run. This means, without switching contexts in your terminal, you can easily use `kubectl` commands on any of the Rancher-managed clusters.

Rancher's convenience for managing multi-cluster environments doesn't end there. Instead of clicking the **Launch kubectl** button, you could click the yellow button labeled **Cluster Explorer** located at the top left:

<div class="wide">

![**Cluster Explorer** monitoring]({{site.images}}{{page.slug}}/uHvocLA.png)

</div>

This screen offers detailed information about the status of the selected cluster and is ideal for more detailed monitoring of the resources used. On the left, you can see a side menu with multiple options. Take a look at the nodes:

<div class="wide">

![**Cluster Explorer** > **Nodes**]({{site.images}}{{page.slug}}/DOox4sc.png)

</div>

Or you could also handle the cluster role bindings:

<div class="wide">

![**ClusterRoleBindings**]({{site.images}}{{page.slug}}/gu97yHo.png)

</div>

Do you want to configure Git repositories for continuous delivery? You can also do that from the Rancher UI:

<div class="wide">

![**Continuous Delivery**]({{site.images}}{{page.slug}}/frvWmaQ.png)

</div>

Since Rancher uses Helm, you can install any number of applications and tools on each cluster, and you can do it from the convenience of the Rancher marketplace:

<div class="wide">

![Rancher Marketplace]({{site.images}}{{page.slug}}/S3bJzgc.png)

</div>

You can even add or remove the Helm chart according to your needs:

<div class="wide">

![Helm charts]({{site.images}}{{page.slug}}/k3PnZ07.png)

</div>

This is just a brief overview of all the operations that can be done from the Rancher Cluster Explorer. From workload management to storage and RBAC, you can manage multi-cluster and hybrid-cluster environments conveniently from a single interface.

### Centralized Security Policy Management

As briefly mentioned in the previous section, from the Rancher Cluster Explorer, you can manage Kubernetes's role-based access control (RBAC):

<div class="wide">

![RBAC]({{site.images}}{{page.slug}}/QTAF6Il.png)

</div>

This means you can enforce ClusterRoleBindings, ClusterRoles, RoleBindings, and Roles—for both users and services running on your clusters—from the same UI.

### Use Cases That Require Built-In Active Directory, LDAP, or SAML Support

Another layer of security and convenience that Rancher offers is the authentication of those who enter the UI. Kubernetes does not provide any mechanism to manage users, so to block the access of someone in particular to the cluster, their certificates or access token must be revoked.

Rancher, however, does have built-in support for major authentication providers and also offers you absolute control over the permissions granted to each user:

<div class="wide">

![New user]({{site.images}}{{page.slug}}/mkClL91.png)

![Auth Provider]({{site.images}}{{page.slug}}/uf9OBYM.png)

</div>

This allows efficient and secure management of who can enter each cluster and with what permissions they can do so.

### Enterprise Support with No Vendor Lock-In

Rancher allows you to handle multi-cluster and hybrid-cluster environments, no matter what Kubernetes distro you are using. This eliminates vendor lock-in and lets you subscribe to enterprise-level support without being tied to a particular vendor.

### Plug-in Support

Rancher is synonymous with flexibility and convenience; for this reason, its amazing [plug-in support](https://github.com/rancher-plugins) should come as no surprise.

These plug-ins, also called drivers, allow Rancher to communicate with different Kubernetes-hosted solutions and infrastructure providers. You can access Rancher Cluster Drivers from the UI:

<div class="wide">

![Rancher Cluster Drivers]({{site.images}}{{page.slug}}/fZ0CX28.png)

</div>

You can also access the different Node Drivers from the UI:

<div class="wide">

![Rancher Node Drivers]({{site.images}}{{page.slug}}/jnRZONR.png)

</div>

In both cases, you can activate, deactivate, or even add new drivers from Rancher's graphical interface.

## Conclusion

In this article, you learned what Rancher is and how it can help you better manage your Kubernetes clusters regardless of where they're hosted. To that end, you've explored how Rancher solves many Kubernetes pain points by extending its default functionality to allow deployment and monitoring of Kubernetes clusters on any infrastructure, management of hybrid and multi-cluster environments from a single interface, and support for authentication methods such as Active Directory, LDAP, or SAML.In summary, Rancher takes Kubernetes to the next level by adding vital features and enterprise support with no vendor lock-in.

Another tool that is as flexible and easy to use as Rancher is [Earthly](https://earthly.dev), the effortless [CI/CD](/blog/ci-vs-cd) framework that allows you to develop pipelines locally and run them anywhere.

{% include_html cta/bottom-cta.html %}
