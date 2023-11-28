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
last_modified_at: 2023-07-19
---
**In this article, you'll learn how to manage Kubernetes secrets. If you manage sensitive data in Kubernetes, Earthly can help you create secure and consistent builds. [Explore how](/).**

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

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-claim # Name of the persistent volume claim
spec:
  storageClassName: hostpath # Name of the storage class
  accessModes:
    - ReadWriteOnce # Indicates this claim can only be read and written once
  resources:
    requests:
      storage: 300Mi # Indicates this claim requests only 300Mi 
                     # of storage from a PV
~~~

Run the command below to create the persistent volume and persistent volume claim:

~~~{.bash caption=">_"}
kubectl apply -f pv.yaml -n example
~~~

<div class="wide">
![Creating Persistent Volume and Claim in Kubernetes Cluster]({{site.images}}{{page.slug}}/6IAuhuq.png)
</div>

Confirm the persistent volume and claim are up and running using the commands below:

~~~{.bash caption=">_"}
kubectl get pv 
# gets the persistent volume for your kubernetes cluster
kubectl get pvc -n example 
# gets the persistent volume claim in the *example* namespace
~~~

<div class="wide">
![Verifying Persistent Volume and Claim]({{site.images}}{{page.slug}}/7LGtteC.png)\
</div>

### Using a Kubernetes Secret as an Environment Variable

Up to this point you have created a persistent volume (PV) and a persistent volume claim (PVC), you are now ready to configure a [StatefulSet](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/) and a service to deploy a PostgreSQL database up to Kubernetes.

The secret **postgres-secret** holds the credentials needed to access the PostgreSQL server, so you will use that secret as an environment variable to configure a statefulSet to deploy a PostgreSQL database.

Create a file called *postgresql-ss.yaml* and add the following:

The code below creates a StatefulSet, and uses a secret as an environment variable (*POSTGRES_USER* and *POSTGRES_PASSWORD*). It uses the `secretKeyRef` attribute to refer to the *postgres-secret* for the *postgres_username* and *posgres_password* key, respectively.  

~~~{.yaml caption="postgresql-ss.yaml"}
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres # The name of the StatefulSet
spec:
  serviceName: postgres # The name of the service this StatefulSet 
  # should use
  selector:
    matchLabels:
      app: postgres
  replicas: 1 # Indicates this StatefulSet should only create one 
  # instance of the postgres database
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
        - name: postgres # The name of the Postgres container
          image: postgres # The image of the Postgres database
          imagePullPolicy: "IfNotPresent"
          env:
          - name: POSTGRES_USER
            valueFrom:
              secretKeyRef:
                name: postgres-secret
                key: postgres_username
          - name: POSTGRES_PASSWORD
            valueFrom:
              secretKeyRef:
                name: postgres-secret
                key: postgres_password
          ports:
          - containerPort: 5432 # The port number postgres listens on
            volumeMounts:
          - name: data
            mountPath: /var/lib/postgresql/data # Data should be mounted 
            # onto this file path
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: postgres-claim # Indicates the postgres database 
          #should use a PVC called postgres-claim
~~~

Execute the command below to create the StatefulSet:

~~~{.bash caption=">_"}
kubectl apply -f postgres-ss.yaml -n example
~~~

<div class="wide">
![Creating Statefulset Postgres]({{site.images}}{{page.slug}}/ZFq3luu.png)
</div>

Confirm that the StatefulSet and the PostgreSQL Pod housing the PostgreSQL database is ready by executing the command below:

~~~{.bash caption=">_"}
kubectl get statefulset -n example
kubectl get pods -n example
~~~

You are good to go with the below output:

<div class="wide">
![Viewing Statefulset and Pods]({{site.images}}{{page.slug}}/PVrxMRQ.png)
</div>

Create a file *postgres-sv.yaml*  and paste in the below code snippets. The code below will create a service so you can start up the PostgreSQL server:

~~~{.yaml caption="postgres-sv.yaml"}
apiVersion: v1
kind: Service 
metadata:
   name: postgres 
   labels:
     app: postgres
spec:
   selector:
     app: postgres
   ports:
     - protocol: TCP
       name: http
       port: 5432
       targetPort: 5432
~~~

Create this service and confirm it is ready by executing the below commands:

~~~{.bash caption=">_"}
kubectl apply -f postgres-sv.yaml -n example
kubectl get service postgres -n example
~~~

<div class="wide">
![Viewing Service (postgres)]({{site.images}}{{page.slug}}/Odu7etg.png)
</div>

Now run the below command to spin up the PostgreSQL server:

~~~{.bash caption=">_"}
kubectl -n example exec -it postgres-0 bash
~~~

If you have the below output, then you have successfully deployed a PostgreSQL database using a secret as an environment variable.

<div class="wide">
![Executing Postgres pod (postgres-0)]({{site.images}}{{page.slug}}/n9AEMF7.png)
</div>

Now type in ***env*** to see all the environment variables available in the PostgreSQL container. The image below shows the secrets and other environment variables:

<div class="wide">
![Viewing Secrets as Environment Variables]({{site.images}}{{page.slug}}/cxlVxWe.png)
</div>

Now type in the command `psql --username=admin postgres` to spin up the PostgreSQL database server. With the below output, you are good to go:

<div class="wide">
![Starting Up Postgres]({{site.images}}{{page.slug}}/F1UKsNi.png)
</div>

### Using a Kubernetes Secret as a Volume Mount

When trying to use a Kubernetes secret, you can also mount it as a volume inside your [deployment](/blog/deployment-strategies) or Pod specification.

Delete the statefulset using the command below:

~~~{.bash caption=">_"}
kubectl delete statefulset postgres -n example
~~~

Edit the *postgres-ss.yaml* file to look like the following:

~~~{.yaml caption="postgres-ss.yaml"}
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres # The name of the StatefulSet
spec:
  serviceName: postgres # The name of the service this StatefulSet 
  # should use
  selector:
    matchLabels:
      app: postgres
  replicas: 1 # Indicates this StatefulSet should only create one instance 
  # of the mysql database
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
        - name: postgres # The name of the postgres container
          image: postgres # The image of the postgres database
          imagePullPolicy: "IfNotPresent"
          env:
          - name: POSTGRES_USER
            value: /var/lib/postgresql/secret/postgres_username
          - name: POSTGRES_PASSWORD
            value: /var/lib/postgresql/secret/postgres_password
          ports:
          - containerPort: 5432 # The port number postgres listens on
          volumeMounts:
          - name: data
            mountPath: /var/lib/postgresql/data # Data should be mounted 
            # onto this file path
          - name: secret-volume
            mountPath: /var/lib/postgresql/secret
      volumes:
      - name: data
        persistentVolumeClaim:
                    claimName: postgres-claim # Indicates the postgres 
                    # database should use a PVC called mysql-claim
      - name: secret-volume
        secret:
          secretName: postgres-secret
          items:
          - key: postgres_password
            path: postgres_password
            mode: 511
          - key: postgres_username
            path: postgres_username
            mode: 511
~~~

Here's what we are doing in the code above:

- Define a volume section under the statefulSet Pod specification, with a name *secret-volume*.
- Specify the type of volume (a secret volume type) and which secret it should use (*postgres-secret*).
- Include the keys Kubernetes should watch out for while creating the statefulset (*postgres_password* and *postgres_username*) alongside their paths which are required (these paths could be anything, like *my-postgres-path*).
- Define a mode **511** which is optional.
- Mount the volume inside the containers section using *volumeMounts* , specify the name of the volume we'd like to mount which is *secret-volume* and then the *mountPath* `/secret` which is where the secret will be saved.
- Add an `env` section to get the POSTGRES_USER and POSTGRES_PASSWORD value from the  */var/lib/postgresql/secret/postgres_username* and */var/lib/postgresql/secret/postgres_password* file paths in the container's file system.

Now run the following commands to recreate the statefulset and to view the pod created by the statefulset:

~~~{.bash caption=">_"}
kubectl apply -f postgres-ss.yaml -n example
kubectl get pods -n example
~~~

<div class="wide">
![Viewing S0tatefulsets and Pods]({{site.images}}{{page.slug}}/cWLsptK.png)
</div>

Now go into the container and type in `env`:

~~~{.bash caption=">_"}
kubectl -n example exec -it postgres-0 bash
~~~

You can see in the image below that the value of the POSTGRES_PASSWORD and POSTGRES_USER are simply file paths containing the exact values of the POSTGRES_PASSWORD and POSTGRES_USER environment variables `/var/lib/postgresql/secret/postgres_password` and `/var/lib/postgresql/secret/postgres_username`, respectively.

<div class="wide">
![Viewing Secret as Volume Mount]({{site.images}}{{page.slug}}/FBv4Q8j.png)
</div>

So with the command below, you can retrieve the POSTGRES_PASSWORD and POSTGRES_USER values:

In a real-world scenario, you might want to use a more secure password, but for this tutorial, the below values works just fine.

~~~{.bash caption=">_"}
cat /var/lib/postgresql/secret/postgres_password
cat /var/lib/postgresql/secret/postgres_username
~~~

<div class="wide">
![Viewing Values from Secret File Paths]({{site.images}}{{page.slug}}/Mb9ZoQt.png)
</div>

In the case of other applications that do not require environment variables to run you can have a secret mounted as a volume using the below pattern:

Create a file *busy-box.yaml*, and paste in the below code snippet. The configuration settings below, uses the secret *postgres-demo-0*  as a volume mount for a busybox pod configuration:

~~~{.yaml caption="busy-box.yaml"}
apiVersion: v1
kind: Pod
metadata:
  name: busybox
spec:
  volumes:
  - name: busybox-secret-volume
    secret:
      secretName: postgres-demo-0
  containers:
  - name: busybox
    image: busybox
    command: ["/bin/sh"]
    args: ["-c", "sleep 600"] 
    volumeMounts:
    - name: busybox-secret-volume
      mountPath: /busybox-data
~~~

Now run the commands below to create the pod in the **example** namespace and also, to confirm if the busybox pod is running without errors:

~~~{.bash caption=">_"}
kubectl apply -f busy-box.yaml -n example
kubectl get pods -n example
~~~

You can see below that the busybox pod was deployed successfully and is in a running state.

<div class="wide">
![Viewing Busybox Pod]({{site.images}}{{page.slug}}/TvaSXz9.png)
</div>

So when you go into the busybox container using the command - `kubectl -n example exec -it busybox sh`. The below command will output the secret mounted as a volume in the busybox container file system:

~~~{.bash caption=">_"}
ls /busybox-data
~~~

<div class="wide">
![Viewing Secret Files *password.txt* and *username.txt*]({{site.images}}{{page.slug}}/HUcLWOp.png)
</div>

Now, if you go into the *busybox-data* directory, you should be able to output the contents of the *password.txt* and *username.txt* files, as shown below:

~~~{.bash caption=">_"}
cd busybox-data
cat password.txt
cat username.txt 
~~~

<div class="wide">
![Outputting *password.txt* and *username.txt* Data]({{site.images}}{{page.slug}}/wy8FJif.png)
</div>

## Getting Resources From a Docker Private Registry Using Secrets

When you try to pull a docker image from a private repository, you'll need to authenticate first. Every docker private repository contains a *config.json* file that houses the authentication values for that repository.

So to be able to pull images from your private repository and deploy on your Kubernetes cluster, your Kubernetes cluster needs explicit access from your private repository. To achieve this, you will need to create a secret object that contains the access token or credentials to your docker repository. Then you configure your Kubernetes resource (deployment or pod) to use that secret using a specific attribute called *imagePullSecrets*.

First, you'll need to make sure you are logged in to your DockerHub account on your machine. Run the command below to confirm:

~~~{.bash caption=">_"}
docker login -u your-username -p your-password
~~~

If you are logged in, you'll have the following output:

<div class="wide">
![Logging in to Docker from Local Machine]({{site.images}}{{page.slug}}/OdMXAnl.png)
</div>

Like I stated earlier, your authentication credentials are stored in the `/.docker/config.json` file. Run the command below to confirm:

~~~{.bash caption=">_"}
cat ~/.docker/config.json
~~~

<div class="wide">
![Viewing Auth Credentials from *~/.docker/config.json*]({{site.images}}{{page.slug}}/rrHUQOg.png)
</div>

In the image above, you can see authentication credentials in the  `~/.docker/config.json` file.

Run the below command to create a secret from the `~/.docker/config.json` file:

The command below will create a secret of type *[kubernetes.io/dockerconfigjson](http://kubernetes.io/dockerconfigjson)*  (which is the required secret type for this use case) called *auth-token* from the file `.docker/config.json` using the *[.dockerconfigjson](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/)* attribute.

~~~{.bash caption=">_"}
kubectl create secret generic auth-token \
    --from-file=.dockerconfigjson=.docker/config.json \
    --type=kubernetes.io/dockerconfigjson -n example
~~~

<div class="wide">
![Creating *auth-token* Secret]({{site.images}}{{page.slug}}/k2b0Y2b.png)
</div>

Now execute the following command to see your secret:

~~~{.bash caption=">_"}
kubectl get secret -n example
~~~

<div class="wide">
![Viewing *auth-token* Secret]({{site.images}}{{page.slug}}/XTQafNv.png)
</div>

Create a Pod specification *private-pod.yaml* to pull the [docker](/blog/rails-with-docker) image from your private repository using the **auth-token** secret you created:

~~~{.yaml caption="private-pod.yaml"}
apiVersion: v1
kind: Pod
metadata:
  name: private-pod # name of the pod
spec:
  containers:
  - name: example-container
    image: mercy30/private-image # a private image in Docker Hub
    ports:
      - containerPort: 80
  imagePullSecrets:
  - name: auth-token
~~~

Apply this pod to your Kubernetes cluster using the command below:

~~~{.bash caption=">_"}
kubectl apply -f private-pod.yaml -n example
~~~

<div class="wide">
![Creating pod Specification private-pod]({{site.images}}{{page.slug}}/qNc3YY6.png)
</div>

Confirm if your pod is running without errors:

~~~{.bash caption=">_"}
kubectl get pods -n example
~~~

If you have the below output, then your Kubernetes [cluster](/blog/kube-bench) was able to pull the image from your Dockerhub private repository using the `.docker/config.json` file which contains the authentication credentials for your DockerHub registry.

<div class="wide">
![Viewing pod private-pod]({{site.images}}{{page.slug}}/Zd61bEv.png)
</div>

## Conclusion

In this tutorial, you've gained a solid understanding of Kubernetes secrets and their implementation as environment variables and volume mounts. You've also learned creation of secrets from a file, via `kubectl`, and from YAML manifest files. We went over the process of authenticating a Kubernetes cluster for image pulling from a private DockerHub repository using a secret from the `.docker/config.json` file and the `imagePullSecrets` attribute. Now, you're equipped to deploy applications securely to Kubernetes using secrets.

As you continue to enhance your Kubernetes skills, you might be interested in exploring more efficiency hacks in automating builds. In this regard, [Earthly](https://www.earthly.dev/) could be a valuable tool to consider.

{% include_html cta/bottom-cta.html %}