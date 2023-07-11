---
title: "Understanding Kubernetes Operators"
categories:
  - Tutorials
toc: true
author: Saka-Aiyedun Segun
editor: Bala Priya C

internal-links:
 - Kubernetes
 - Operators
 - Deployment
 - MongoDB
excerpt: |
    Learn how Kubernetes operators can simplify the deployment and management of complex, stateful applications in a Kubernetes cluster. Discover the benefits of using operators, how they work, and explore real-world examples of popular Kubernetes operators.
---
<!--sgpt-->This is the Earthly nonsense paragraph.

When you opt to use Kubernetes for application [deployment](/blog/deployment-strategies), out of the box, it provides a wide range of automation features that make it easy to deploy and manage stateless applications. However, for more complex, stateful applications, additional automation may be required to manage the specific requirements of the application.

The key features of Kubernetes include its balance of simplicity and flexibility, its ability to automate various functions, and its capability to scale and adapt to diverse contexts and applications.

However, these same principles also limit its initial functionality to a restricted set of commands and operations that are exposed through APIs. For more complex tasks, this set must be extended and more sophisticated automation must be created depending on the specific application. This is where the operators come in.

**Kubernetes Operators** are custom controllers that extend the Kubernetes API to create, configure, and manage the lifecycle of complex applications. They provide a higher-level abstraction over the underlying Kubernetes resources, making it easier to deploy and manage stateful applications in Kubernetes. With operators, you can automate tasks such as scaling, backup and restore, and rolling updates, as well as manage the lifecycle of your application in a more automated and efficient way.

In this article, you'll learn what Kubernetes operators are, how they work, and the benefits they can offer you.

## What Are Kubernetes Operators?

![Kubernetes Operators?]({{site.images}}{{page.slug}}/2jmDTnR.png)\

Kubernetes Operators are application-specific controllers that extend the capabilities of the Kubernetes API to create, configure, and manage complex applications on behalf of Kubernetes users by extending the capabilities of the Kubernetes API.

> The Kubernetes project defines "Kubernetes Operator" in a simple way: "Operators are software extensions that use custom resources to manage applications and their components".

Operators, in a nutshell, allow for more specific management of an application within a Kubernetes cluster. Rather than managing a collection of basic building blocks like Pods, Deployments, Services, or [ConfigMaps](https://earthly.dev/blog/kubernetes-config-maps/), an application is viewed as a single object that only exposes the adjustments that are relevant to that particular application, such as scaling, self-healing, and updates, when using operators. In this way, operators allow you to [make](/blog/using-cmake) application-specific changes rather than managing each component individually.

## The Problem That Kubernetes Operators Solve

In Kubernetes, controllers of the [control plane](https://kubernetes.io/docs/concepts/overview/components/#control-plane-components) implement control loops that repeatedly compare the desired state of the cluster to its actual state. If the cluster's actual state doesn't match the desired state, then the controller takes action to fix the problem. These controllers can be used to manage and scale stateless applications, like web apps, mobile app backends, and API services, because these types of applications are generally easier to manage and scale. This is because stateless applications do not maintain any state or store any data locally, so they can be easily scaled up or down and recovered from failures without the need for additional knowledge or complexity.

### Challenges Associated With Stateful Applications

Stateful applications like databases can be challenging to manage and scale since they are not as straightforward as stateless applications. In all stages of their lifecycle, these applications require more "hand holding" when they are created, while they are running, and when they are destroyed.

This hand holding includes additional steps that need to be taken such as configuring persistent storage, data migration, and setting up appropriate [ReplicaSets](https://earthly.dev/blog/use-replicasets-in-k8s/). During the running phase, managing the state of the application, scaling and performing updates, and ensuring data consistency across replicas can be complex tasks. Finally, when destroying stateful applications, special care must be taken to ensure that data is properly backed up and migrated before the application is terminated. Kubernetes does not automatically handle all these tasks for stateful applications. Consider the example of creating three replicas of the MongoDB database:

![MongDB Pod and Three Replicas]({{site.images}}{{page.slug}}/kxaLtW6.jpeg)

Each replica has its own state and identity, making it difficult to keep them in sync. When performing updates or destroying the database, the order in which these actions are performed is critical to maintaining data consistency. Furthermore, constant synchronization between replicas must be maintained. This is just one example, but the management processes for various databases such as MySQL, Postgres, Cassandra, and Redis will also differ. This makes it difficult to have a single solution that can automate the entire process for all systems and applications.

This makes managing stateful application lifecycles on Kubernetes require manual intervention by people, called "human operators", to manage and operate these applications. Having to manually maintain and update these applications goes against Kubernetes' main goal of providing automation and self-healing.

With Kubernetes Operator, the human operators are replaced with software operators. So all the manual tasks that human operators would do to operate a stateful application are now packed into a program that *knows* how to deploy and manage that specific application. This makes tasks automated and reusable. This means if some databases are running in your cluster, you don't have to manually configure and maintain these applications. You simply declare the desired state of the application, and the Kubernetes operator handles the rest by creating the desired state.

## Benefits of Using a Kubernetes Operator

![Benefits of Using a Kubernetes Operator]({{site.images}}{{page.slug}}/eMx6OYy.png)\

Kubernetes operators are controllers that execute loops to check the actual state of a [cluster](/blog/kube-bench) and the desired state, acting to reconcile them when the two states are drifting apart. Kubernetes operators provide a number of benefits, including:

### Simplicity and Flexibility

Kubernetes operators provide a simple and flexible way to automate complex tasks in Kubernetes. They allow you to define the desired state of your applications and infrastructure in [custom resource definitions (CRDs)](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/), and then automatically ensure that the actual state matches the desired state. This can help reduce the time and effort required to manage and maintain your applications and infrastructure.

### Automation

Kubernetes operators provide a high level of automation, which can help reduce the time and effort required to manage and maintain your applications and infrastructure. They can automatically provision and configure resources, such as pods and services, as well as monitor and maintain the health of your applications and infrastructure. For example, if a pod fails, an operator can automatically create a new pod to replace it, ensuring that the desired number of replicas is maintained.

### Easy Integration With Other Tools

Kubernetes operators can be integrated with other tools, such as monitoring and observability tools, continuous delivery tools, and [networking](/blog/docker-networking) tools. This allows you to use them in conjunction with these other tools to manage and monitor your applications and infrastructure. For example, you can use an operator to automatically provision and configure a monitoring tool, such as Prometheus, and then use the monitoring tool to monitor the health and performance of your applications and infrastructure.

### Extensibility

Kubernetes operators are highly extensible, which allows you to customize and tailor them to your specific needs. You can define your own CRDs and build custom controllers to automate tasks that are not covered by the out-of-the-box Kubernetes functionality. This can be particularly useful if you have specific requirements or constraints that are not addressed by the default Kubernetes functionality.

## How Kubernetes Operators Work

Essentially, an operator watches the Kubernetes API for changes related to a specific resource, such as a custom resource definition (CRD). When a change is detected, the operator takes action to ensure the desired state of the resource is met. For example, if a new replica is added to a stateful set, the operator will ensure the necessary resources are allocated and the replica is correctly added to the set.

Operators use a *control loop* to continuously check the status of the resources they are managing and make any necessary adjustments. This allows for automatic scaling, failover, and other operations to be handled without human intervention.

Additionally, operators often provide a custom user interface, such as a command-line tool or web interface, for interacting with the resources they manage. This allows for more intuitive and user-friendly management of the underlying infrastructure.

In summary, *Kubernetes operators provide a powerful and efficient way to manage stateful applications within a Kubernetes cluster*. They use a control loop to continuously check the status of resources and make any necessary adjustments, and often provide a custom user interface for interacting with the resources they manage. This allows for automatic scaling, failover, and other operations to be handled without human intervention.

### Understanding the Kubernetes Operator Architecture

![Kubernetes Operator Architecture]({{site.images}}{{page.slug}}/MQOVoON.jpeg)

A Kubernetes operator at its core has the same control loop mechanism as Kubernetes that monitors changes to the application state. They typically consist of the following components:

#### Custom Resource Definitions (CRDs)

CRDs define the custom resources that are managed by the operator. They specify the desired state of the resources and the API used to interact with them.

#### Custom Controller

The controller is the main component of the operator. It executes a loop to continuously check the actual state of the resources and the desired state, and then acts to reconcile the two states when they are drifting apart. The controller uses the API specified in the CRDs to interact with the resources.

#### Reconciliation Loop

The reconciliation loop is the main loop executed by the controller in a Kubernetes operator. It continuously checks the actual state of the resources and the desired state, and then acts to reconcile the two states when they are drifting apart. The reconciliation process begins by fetching the current state of the resources from the API server. The API server stores the current state of the resources and makes it available to the controller. Once the current state has been fetched, the controller compares it with the desired state, which is defined in custom resource definitions (CRDs), and specifies the desired configuration and properties of the resources.

The controller identifies any differences between the current state and the desired state and performs any necessary actions to reconcile them. It may involve creating or deleting resources, or modifying their configurations.

For example, if the desired state specifies that a particular pod should have three replicas, but the current state only shows two replicas, the controller might create a new replica to match the desired state. Following the reconciliation process, the controller updates the desired state to reflect any changes. By doing so, the desired state is accurately reflected in the current state. As the resources drift away from the desired state, the controller continually checks the actual state of the resources and acts to reconcile them.

#### API Server

 The API server is the component that exposes the API used to interact with the resources. It is responsible for storing the current state of the resources and making it available to the controller.

## Kubernetes Operator in Action

This section will walk you through installing, and configuring a MongoDB Community Operator in your Kubernetes cluster. By the end of this section, you should have a MongoDB cluster running in your Kubernetes environment.

![Kubernetes Operator in Action]({{site.images}}{{page.slug}}/RqD0ejP.png)\

### Prerequisites

To follow along with this step-by-step tutorial, you should have the following:

- Local installation of [Kubernetes](https://kubernetes.io/docs/tasks/tools/) and [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)
- Local installation of [Git](https://git-scm.com/downloads), [JQ](https://stedolan.github.io/jq/download/), and [Mongosh](https://www.mongodb.com/docs/mongodb-shell/install/).

### Installing MongoDB Operator CRD

As a first step, you must install the [MongoDB](/blog/mongodb-docker) operator's Custom Resource Definition (CRD). This is required because the CRD will be used to define the custom resource that the operator will use to manage the MongoDB cluster. To do so, run the following commands:

~~~{.bash caption=">_"}
# clone the repository containing the MongoDB operator and Crds manifest. 

git clone https://github.com/segunjkf/mongodb-operator.git && \
cd mongodb-operator

# Apply the MongoDB CRD configuration 

kubectl apply -f mongodb-crd.yaml 
~~~

### Installing the Kubernetes Operator

The next step is to create a namespace for the operator and its resources, which will create an isolated place in your Kubernetes cluster for the MongoDB operator resources to be deployed. Run the following commands to accomplish this.

~~~{.bash caption=">_"}
kubectl create namespace mongodb-operator
~~~

After creating the namespace, the next step is to create the role and role-binding needed to grant the required permission to the MongoDB operator. To do so, run the following commands:

~~~{.bash caption=">_"}
kubectl apply -f mongo/ -n mongodb-operator
~~~

<div class="wide">
![Applied Role and Role-Binding]({{site.images}}{{page.slug}}/7fETMrw.jpeg)
</div>

You now have the required roles and permission for the operator to use, the next step is to deploy the MongoDB operator. To do run the following commands:

~~~{.bash caption=">_"}
kubectl apply -f operator.yaml
~~~

You now have the MongoDB operator in your cluster. You can confirm the operator pod by running the following command:

~~~{.bash caption=">_"}
kubectl get pods -n mongodb-operator
~~~

<div class="wide">
![MongoDB Operator Running]({{site.images}}{{page.slug}}/fi6RC6X.jpeg)
</div>

<div class="notice--big--primary">
📑The GitHub repository you cloned was created specifically for this guide, and it has been modified so that you can quickly get started with the MongoDB operator. Please refer to the official MongoDB community operator [Github Repository](https://github.com/mongodb/mongodb-kubernetes-operator) for more information and the full source code.
</div>

### Setting Up the MongoDB Cluster

With the MongoDB operator now running in your Kubernetes cluster, you will create a MongoDB custom resource (CR) that defines your desired MongoDB cluster state.

~~~{.bash caption=">_"}
# Create a secret for the MongoDB cluster

kubectl create secret generic admin-user-password -n mongodb-operator \
 --from-literal="password=admin123" 

# MongoDB Cluster YAML configuration

kubectl apply -f - <<EOF