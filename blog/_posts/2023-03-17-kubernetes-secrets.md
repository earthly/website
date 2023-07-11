---
title: "An Introduction to Kubernetes Secrets"
categories:
  - Tutorials
toc: true
author: Mercy Bassey
editor: Bala Priya C

internal-links:
 - Kubernetes
 - PostgreSQL
 - Database
 - YAML
excerpt: |
    Learn how to manage sensitive data in Kubernetes using secrets. This tutorial covers creating secrets, using them as environment variables or volume mounts, and pulling images from private Docker repositories using secrets.
---
<!--sgpt-->This is the Earthly nonsense paragraph.

Generally, applications contain some sensitive data, like authentication tokens, passwords, usernames, and more. As you build in Kubernetes, some of these may go into pod specifications accidentally exposing some sensitive data. So how do we manage such data in Kubernetes? Secrets can help!

In this tutorial, you will learn what Kubernetes secrets are and how to do the following:

- Create a secret object in Kubernetes
- Use a secret
- Use a secret to pull an image from your private [Docker](/blog/rails-with-docker) repository

## Prerequisites

To follow along, you need a Kubernetes cluster that is up and running. This tutorial uses [Minikube](/blog/k8s-dev-solutions).

## What Are Kubernetes Secrets and Why Should You Use Them?

A Kubernetes secret is an object that holds some amount of *sensitive information*, such as authentication keys, tokens, usernames, passwords which can be used as external configurations for pods running in your Kubernetes [cluster](/blog/kube-bench).

[Secrets](https://kubernetes.io/docs/concepts/configuration/secret/) are similar to [ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/) but are specifically intended to hold sensitive information. It is a Kubernetes object on its own, which means it is totally isolated from the pods or other resources using it. So its contents cannot be accessed when viewing, creating, editing or accessing Pods or by other Kubernetes resources using its contents.

If you want to deploy an application or a database to a Kubernetes cluster, you might want to store application or database passwords and usernames as a secret object for security, rather than hard coding them into your application container which becomes visible to everyone checking out the application.

You can find all the code for this tutorial in this [GitHub repository](https://github.com/mercybassey/kubernetes-secrets).

## Configuring a Secret in Kubernetes

There are various ways to configure a Kubernetes secret object. A secret object can be configured via the command line using `kubectl`, from a file (either a .txt or a .conf file), or by writing YAML manifests.

### Creating a Secret via the Command Line

You can use the `kubectl` command to create a secret via the command line.

Run the command below to create a namespace called *example*:

~~~{.bash caption=">_"}
kubectl create -n example
~~~

In this namespace you will deploy a PostgreSQL database that will pull confidential information from the secret you intend to create later on.

<div class="wide">
![Creating Namespace(example)]({{site.images}}{{page.slug}}/avTX0yc.png)
</div>

Execute the `kubectl` command below to create a secret object:

~~~{.bash caption=">_"}
kubectl create -n example secret generic postgres-demo \
--from-literal=username=johndoe --from-literal=password=123456
~~~

<div class="wide">
![Creating Secret postgres-demo]({{site.images}}{{page.slug}}/TmXatgQ.png)
</div>

Considering the command above there are few things to note:

- The term `generic` is used to give the secret a generic name. Depending on what you want to use the secret for, you can also have a *docker-registry* or a *tls* secret, used for a docker-registry or as a TLS secret, respectively. You can run  `kubectl create secret --help` so see the available commands for creating a secret.
- The `-from-literal=` is used to specify a key and literal value to insert in secret (`mykey=somevalue`). You can run  `kubectl create secret generic --help` for more information on creating generic secrets.
- There is no need to encrypt the value as it's done automatically.

Run the command below to view the secret:

~~~{.bash caption=">_"}
kubectl get secret -n example
~~~

You can see the secret `postgres-demo` was created with a secret type of **opaque:**

<div class="wide">
![Viewing Secret postgres-demo]({{site.images}}{{page.slug}}/83fPibh.png)
</div>

In Kubernetes there are various types of secrets; we have:

- **Opaque secrets** :  The default secret type if the type is not specified in a secret configuration file.
- **Service accounts token secrets**: Used to store a token that references a service account. For this secret type the `kubernetes.io/service-account-token`annotation is set to an existing service account name.
- **Docker config secrets**: Stores the credentials for accessing a Docker repository for images. For this type of secret, either the `kubernetes.io/dockercfg` or `kubernetes.io/dockerconfigjson` annotation type is used.
- **Basic authentication secrets**: Used for storing credentials needed for basic authentication, like a username or a password.The annotation type for this type of secret should be `kubernetes.io/basic-auth`.
- **SSH authentication secrets**: For storing data used for SSH authentication. you will have to specify a `ssh-privatekey` key-value pair in the `data` field as the SSH credential to use. The annotation type for this secret is set to `kubernetes.io/ssh-auth`.
- **TLS secret**: For storing a certificate and its associated key that are typically used for TLS. A  `tls.key` and the `tls.crt` key must be provided in the data (or `stringData`) field of the secret configuration. For this secret type, the `kubernetes.io/tls` annotation type is used.
- **Bootstrap token secrets**: Used as a bearer token when accessing new clusters or joining new nodes to an existing cluster. It uses the `bootstrap.kubernetes.io/token` annotation type.

In this tutorial, we'll focus more on the **Opaque** secret type.  

Run the command below to see other information concerning the secret:

~~~{.bash caption=">_"}
kubectl describe secret postgres-demo -n example
~~~

The output below shows you the secret, the type, and its keys alongside its encrypted values:

<div class="wide">
![Describing Secret(postgres-demo)]({{site.images}}{{page.slug}}/mGG33fw.png)
</div>

### Creating a Secret From a File

You can also create a secret from a file. This file could be a file containing some value.

Using your preferred editor, create two files. A *username.txt* and *password.txt* file. This tutorial uses `nano`.

Type in *janedoe* and *123456789* in the *username.txt* and *password.txt* file respectively:

~~~{.bash caption=">_"}
nano username # Type in *janedoe* and save the file 
nano password # Type in *123456789* and save the file 
~~~

Execute the command below to create this secret:

~~~{.bash caption=">_"}
kubectl create -n example secret generic postgres-demo-0 \
--from-file=./username.txt --from-file=./password.txt
~~~

<div class="wide">
![Creating Secret(postgres-demo-0)]({{site.images}}{{page.slug}}/7GB0UUb.png)
</div>

Run the command below, to see the newly created secret:

~~~{.bash caption=">_"}
kubectl get secret -n example
~~~

You should now have two secrets: *postgres-demo*  and *postgres-demo-0*, as shown below:

<div class="wide">
![Viewing Secrets in the Example Namespace]({{site.images}}{{page.slug}}/VgIuIYr.png)
</div>

Execute the following command to see your secret:

~~~{.bash caption=">_"}
kubectl describe secret postgres-demo-0 -n example
~~~

You should see the *password.txt* and *username.txt* files and the number of bytes their values take:

<div class="wide">
![Describing Secret(postgres-demo-0)]({{site.images}}{{page.slug}}/DRSCpIZ.png)
</div>

### Creating a Secret With YAML

You can also create a secret from YAML manifests. One thing to note is the key value will be a [base64](https://developer.mozilla.org/en-US/docs/Glossary/Base64) encoded value.

To explain further, if you'd like to have a username and a password in your secret object, they should hold only base64 encoded values.

Create a file called *secret.yaml* and add the below configuration settings:

~~~{.yaml caption="secret.yaml"}
apiVersion: v1
kind: Secret
metadata:
    name: postgres-secret #name of secret
type: Opaque #key-value pairs secret type
data:
    postgres_password: bW9uZ29kYi1wYXNzd29yZA== #base64 encoded value
    postgres_username: YWRtaW4= #base64 encoded value
~~~

<aside>
💡 To have a base64 encoded value run the following command -**`echo -n 'your-username-or-password-value' | base64`** at the command line.
</aside>

Now, run the command below to create this secret:

~~~{.bash caption=">_"}
kubectl apply -f secret.yaml -n example
~~~

<div class="wide">
![Creating Secret (postgres-secret)]({{site.images}}{{page.slug}}/jziUEu8.png)
</div>

At this point, you should have three secrets in total *postgres-demo, postgres-demo-0, postgres-secret*, when you run the command below:

~~~{.bash caption=">_"}
kubectl get secrets -n example
~~~

<div class="wide">
![Viewing All Secrets in Kubernetes Cluster]({{site.images}}{{page.slug}}/Gsz9PcS.png)
</div>

## How to Use a Secret in Kubernetes

![How]({{site.images}}{{page.slug}}/how.png)\

There are two common ways that you can use a secret in Kubernetes. You can either use it as an environment variable or as a volume mount.

When you use it as an environment variable, the secret gets created as an environment variable which you can then use within containers in Pods. When you use it as a volume mount, your secret will be mounted as individual files inside your [container](/blog/docker-slim) which you can make references to.

To illustrate this, you'll deploy a PostgreSQL database that will make use of the *postgres-secret*. You will create a persistent volume to provision a piece of storage in the cluster and persistent volume claim to request some amount of storage from the persistent volume and then a *statefulSet* to deploy the PostgreSQL database, and then a service to spin up the PostgreSQL server.

You can refer to the guide on [Using Kubernetes Persistent Volumes](https://earthly.dev/blog/kubernetes-persistent-volumes/) for information about Kubernetes persistent volumes and persistent volume claims.

Create a file *pv.yaml*  and add the following configuration settings. This configuration setting will create a persistent volume with *2Gi* of storage and persistent volume claim to use *300Mi* of that storage in your Kubernetes cluster:

~~~{.yaml caption="pv.yaml"}
apiVersion: v1
kind: PersistentVolume
metadata:
   name: postgres-volume # Name of the persistent volume
   labels:
     type: local
spec:
   storageClassName: hostpath # Name of the storage class
   capacity:
     storage: 2Gi # Amount of storage this volume should hold
   accessModes:
     - ReadWriteOnce # To be read and written only once
   hostPath: # Storage class type
     path: '/mnt/data' # File path to mount volume