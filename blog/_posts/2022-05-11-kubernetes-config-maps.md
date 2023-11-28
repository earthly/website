---
title: "Kubernetes ConfigMaps and Configuration Best Practices"
categories:
  - Tutorials
toc: true
author: James Walker

internal-links:
 - just an example
topic: kubernetes
excerpt: |
    Learn how to use Kubernetes ConfigMaps to store and inject configuration parameters into your pods. This article covers the use cases for ConfigMaps, how to create them, and how to consume them in your Kubernetes deployments.
last_modified_at: 2023-07-14
---
**In this article, we'll dive into Kubernetes ConfigMaps. If you're struggling with ConfigMaps, Earthly simplifies your build process through consistent, containerized builds. [Discover how with Earthly](/).**

Most applications have configuration parameters that need to be provided at runtime. It's common to use command line arguments, environment variables, and static files to configure software deployed using traditional methods. These techniques are also available to containerized [Kubernetes](https://kubernetes.io/) workloads via the ConfigMap API object.

[ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap) are expressly designed to store config parameters and inject them into running pods. They let you decouple your app's configuration from the individual containers running your deployment. Learning how to use them will increase your system's portability and make it easier to reconfigure your live instances.

In this article, you'll explore the use cases for ConfigMaps, learn how to create them, and know the options you have for providing a ConfigMap's value to your pods. You'll also learn how to configure your Kubernetes deployments without manually updating containers or baking settings into your images.

## Using ConfigMaps

ConfigMaps are ideal for most situations where you want to supply environment-specific configuration values to your pods. They store key-value pairs and make them available to pods as environment variables, command line arguments, or files in a mounted volume.

You can also use a ConfigMap to store the IP address of your app's database server or the URL of a proxy service. Hard-coding this kind of information into your container image tightly couples it to a specific environment. When you have the image accept a value supplied by an external ConfigMap, you can deploy it unmodified to several clusters, like development, test, and production installations. Then you can inject an appropriately configured ConfigMap each time so your image references the correct server for its operating environment.

One limitation with ConfigMaps is their inability to support sensitive data. ConfigMaps are stored in plain text, so they're not suitable for holding values, like passwords, API tokens, and secret keys. This type of config parameter should be injected as a [Kubernetes Secret](https://kubernetes.io/docs/concepts/configuration/secret) instead.

ConfigMaps aren't built for very large amounts of data either: their maximum size is 1 MiB. Larger structures can be broken into several ConfigMaps or handled by mounting a volume containing a regular file.

## Creating a ConfigMap

ConfigMaps are one of the simplest Kubernetes object types. Their manifests only need a `metadata.name` field and some key-value config data pairs nested under `data`. Keys can only use alphanumeric characters, supplemented by `.`, `-`, and `_`.

For example, here's a ConfigMap's YAML definition with three key-value pairs. They expose the target application's dynamically adjustable parameters:

~~~{.yml caption=""}
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  db_host: "https://database.example.com"
  default_user_status: "suspended"
  max_invoice_date: "2022-12-31"
~~~

ConfigMaps can also accommodate values that are expressed in binary format; you just need to use the `binaryData` field instead of `data`. Binary values should be [base64-encoded](https://linux.die.net/man/1/base64) inside the ConfigMap:

~~~{.yml caption=""}
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
binaryData:
  demo: ZXhhbXBsZQo=
~~~

A single ConfigMap may contain `data` and `binaryData` fields. Keys need to be unique across both variants; repetition will cause an error when you add the object to your cluster.

Once you've written your manifest, apply it to your cluster [using kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux):

~~~{.bash caption=">_"}
$ kubectl apply -f config-map.yaml
~~~

## Consuming ConfigMaps in Pods

Now that the ConfigMap exists in your cluster as a static chunk of data, it's not doing anything because no pods reference the object.

There are two ways to link a ConfigMap into a pod's manifest. Your approach should depend on whether you want to use the ConfigMap's data as environment variables, command line arguments, or mounted files. This decision should be based on how your application expects to read its config values.

From a Kubernetes perspective, environment variables can be simple to set up, inspect, and reason about. Mounted files are more sustainable for larger amounts of data. They also support automatic updates after you modify the ConfigMap's `data` field. ConfigMaps injected as environment variables require a pod restart to apply new changes.

Now, look at how you can use both kinds of ConfigMap references with your pods.

### Environment Variables

Set the `spec.containers.envFrom.configMapRef` field to pull a ConfigMap's data into a pod's containers as environment variables:

~~~{.yaml caption=""}
apiVersion: v1
kind: Pod
metadata:
  name: app-pod
spec:
  containers:
 - name: app-container
 command:  ["/bin/sh", "-c", "echo $db_host"]
 image: busybox:latest
   envFrom:
     - configMapRef:
         name: app-config
~~~

Apply:

~~~
$ kubectl apply -f pod.yaml
$ kubectl logs app-pod
~~~

Reference the ConfigMap by the name you assigned in its manifest's `metadata.name` field. Containers created by this pod will be started with environment variables corresponding to the key-value pairs within the ConfigMap. In this example, your application could read the `db_host`, `default_user_status`, and `max_invoice_date` parameters from the environment.

Sometimes you might not need the whole ConfigMap inside a particular pod's containers. Alternatively, you may want to rename a particular key before it's injected into the environment. You can use the `env` field with a `valueFrom` clause to selectively include specific keys from a ConfigMap:

~~~{.yaml}
apiVersion: v1
kind: Pod
metadata:
  name: app-pod
spec:
  containers:
 - name: app-container
   image: busybox:latest
   env:
     - name: ACCOUNTS_INVOICING_MAX_DATE
     - valueFrom:
         configMapKeyRef:
           name: app-config
           key: max_invoice_date
~~~

This pod's containers can access the `max_invoice_date` ConfigMap value as the `ACCOUNTS_INVOICING_MAX_DATE` environment variable.

### Mounted Volume Files

ConfigMaps can be mounted into your containers as files in a volume. When this mechanism is used, your pod references a volume that uses the `configMap` field to source its initial config from a named ConfigMap. That volume is then mounted into the container via the `volumeMounts` field:

~~~{.yaml}
apiVersion: v1
kind: Pod
metadata:
  name: app-pod
spec:
  containers:
 - name: app-container
   image: busybox:latest
   volumeMounts:
     - name: config
       mountPath: "/etc/demo-app"
       readOnly: true
   volumes:
     - name: config
       configMap:
         name: app-config
~~~

The previous example defines a named volume called `config` that references the `app-config` ConfigMap created earlier. The volume is mounted to the `/etc/demo-app` directory within the container. It's advisable to mark the mount as `readOnly`, as you shouldn't change ConfigMap values from within a container. Kubernetes automatically updates the files in the volume as you make changes to the ConfigMap's `data` field, potentially overwriting any alterations you make.

ConfigMaps mounted as volumes expose each `data` key-pair value as a separate file inside the mount point. The key is used as the file name; the file's content will be the corresponding value in the ConfigMap. The container created earlier can get the value of its database host setting by reading the `/etc/demo-app/db_host` file.

### Command Line Arguments

You can use a ConfigMap to set the `command` for your containers. This field supports variable interpolation using environment variables. You can dynamically configure the command by creating a variable that references a ConfigMap value, then use that variable in your `spec.containers.command` field:

~~~{.yaml }
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  default_command: "date"

---

apiVersion: v1
kind: Pod
metadata:
  name: app-pod
spec:
  containers:
 - name: app-container
   image: busybox:latest
   command: ["/bin/sh", "-c", "$(STARTUP_COMMAND)"]
   env:
     - name: STARTUP_COMMAND
     - valueFrom:
         configMapKeyRef:
           name: app-config
           key: default_command
~~~

This example runs the command given by the `$STARTUP_COMMAND` environment variable when the container starts. The variable's value is set to the `default_command` key within the created ConfigMap.

## Setting Up Immutable ConfigMaps

ConfigMaps can be made immutable by setting their `immutable` manifest field to `true`. This locks the `data` and `binaryData` fields, preventing them from ever being changed. It's also forbidden to revert `immutable` to `false` after it has been assigned. Here's the code:

~~~{.yaml}
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  db_host: "https://database.example.com"
immutable: true
~~~

Immutability is useful when you know you'll only need to configure your application during its initial deployment. Removing the ability to change parameters later on guards against unintentional edits as you manage your other objects.

When a ConfigMap *is* mutable, Kubernetes monitors it and periodically applies changes to your pods. This only works when values are mounted as volumes; the environment variables and command line arguments of running containers can't be changed. Enabling immutability allows Kubernetes components to stop polling for ConfigMap changes, [improving cluster performance](https://kubernetes.io/docs/concepts/configuration/configmap/#configmap-immutable).

## Viewing ConfigMap Data

You can view the content of a ConfigMap using kubectl:

~~~{.bash caption=">_"}
$ kubectl describe configmap app-config
~~~

![Viewing ConfigMap data with kubectl]({{site.images}}{{page.slug}}/BCj16VQ.png)

This will show you the ConfigMap's metadata and the key-value pairs within its `data` field.

## Creating ConfigMaps from the Command Line

Kubectl includes some convenience utilities to simplify ConfigMap creation.

You can quickly create a new ConfigMap with specific values:

~~~{.bash caption=">_"}
$ kubectl create configmap app-config --from-literal=db_host=https://database.example.com
~~~

![Creating a ConfigMap with literal values with kubectl]({{site.images}}{{page.slug}}/8Yo8aqK.png)

Another approach lets you automatically create a ConfigMap from an existing config file. Each line in the file will be interpreted as a new key-value pair:

~~~{.bash caption=">_"}
$ cat ./app.conf
~~~

~~~{.ini caption="Output"}
db_host=https://database.example.com
default_user_status=suspended
~~~

Apply:

~~~{.bash caption=">_"}
# Creates ConfigMap with "db_host" and "default_user_status" keys
$ kubectl create configmap app-config --from-file=./app.conf
~~~

Finally, you can populate a ConfigMap from a set of files stored within a directory. This variation reads *each file* into a key within the ConfigMap. The file name will become the key; the file's content will be available as that key's value:

~~~{.bash caption=">_"}
$ ls ./conf
database.conf
users.conf

# Creates ConfigMap with "database.conf" and "users.conf" keys
$ kubectl create configmap app-config --from-file=./conf/
~~~

These mechanisms help you quickly convert existing config files into ConfigMap objects using the imperative `kubectl create` command. The declarative system of `kubectl apply` with YAML manifests is usually more appropriate for managing large config structures that need to be versioned alongside your other application components.

## Conclusion

ConfigMaps are Kubernetes API objects for storing your application's runtime settings. You can provide their data to pods as environment variables or files in a mounted volume. ConfigMaps can also be immutable, a characteristic that forbids dynamic updates to enhance safety and performance.

ConfigMap is a tool used with running containers in your Kubernetes cluster. However, correctly configuring and maintaining your container images are just as important as their runtime settings. [Earthly](https://earthly.dev) can help create a maintainable approach to build time configuration, offering a repeatable syntax that's reproducible and easy to understand. It facilitates more robust builds without the brittleness associated with poor configuration practices.