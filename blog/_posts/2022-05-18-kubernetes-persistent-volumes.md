---
title: "Using Kubernetes Persistent Volumes"
categories:
  - Tutorials
toc: true
author: James Walker
internal-links:
 - persistent volumes
 - kubernetes persistent volumes
 - kubernetes persistence
topic: kubernetes
excerpt: |
    
---
**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. If you're sailing the K8s seas, [check out Earthly](/).**

Kubernetes [persistent volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes) provide data storage for stateful applications. They abstract a storage system's implementation from how it's consumed by your pods. A persistent volume could store data locally, on a network share, or in a block storage volume provided by a cloud vendor.

Persistent volumes solve the challenges of storing persistent data, such as databases and logs, in Kubernetes. Containers running inside pods are stateless and have ephemeral filesystems. Although your applications can read and write files within their containers, any changes will be lost when the pod is restarted or terminated.

In this article, you'll learn what persistent volumes are, why they're important, and how you can get started using them in your cluster. You'll also see some common management commands for interacting with persistent volumes [using kubectl](https://kubernetes.io/docs/reference/kubectl).

## Why Persistent Volumes Matter

The ephemeral nature of container filesystems prevents you from spinning up a database server in a Kubernetes pod without a special configuration. Otherwise, you'd lose your data as soon as the pod restarted. You also wouldn't be able to scale the database deployment, as all the files would be stored within a specific container.

Persistent volumes solve this issue. They're built atop the simpler [volume system](https://kubernetes.io/docs/concepts/storage/volumes), which provides a shared unit of storage that can be accessed by all the containers in a pod. Kubernetes can restore volumes after an individual container crashes and restarts.

Persistent volumes are a higher abstraction that completely decouples storage from the pods that use it. A persistent volume has its own lifecycle, stores data at the cluster or namespace level, and can be shared between multiple pods. Although persistent volumes are used by pods, they never belong to pods. The volume and its data will remain available in the cluster even after all pods that reference it are gone, allowing it to be reattached to new, future pods.

## When To Use Persistent Volumes

You should use a persistent volume whenever you have data that needs to outlive individual pods. Unless the data is transitory or specific to a single container, it's usually best stored in a persistent volume.

Here are some common use cases:

- **Database storage:** Data in a database should always be stored in a persistent volume so it persists beyond the containers that run the server. You don't want to wipe your users' data each time the pod restarts.
- **Log storage:** Writing container log files to a persistent volume ensures they'll be available after a crash or termination. If they're not written to a persistent volume, the crash will destroy the logs that could have helped you debug the issue.
- **Protection of important data:** Persistent volumes let you [avoid accidental data deletion](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#storage-object-in-use-protection). They include safeguards that prohibit the removal of volumes that are actively used by pods.
- **Data independent of pods:** Persistent volumes make sense whenever your data is of primary importance in your cluster. They give you the tools to manage data independently of application containers, making it easier to handle backups, performance, and storage capacity allocations.

## Creating a Persistent Volume

Persistent volumes may be created either statically or dynamically. A *statically* created volume means that the volume is manually added to your cluster before it's used. A *dynamically* created volume occurs when a non-existing volume is referenced, causing it to be created automatically. You'll now use kubectl to create a volume with the static method.

To start, you need a YAML file for your persistent volume:

~~~{.yaml}
apiVersion: v1
kind: PersistentVolume
metadata:
  name: example-pv
spec:
  accessModes:
 - ReadWriteOnce
  capacity:
 storage: 1Gi
  storageClassName: standard
  volumeMode: Filesystem
~~~

This defines a simple persistent volume with a 1 Gi capacity. A few other configuration options are used to define how the volume is provisioned and accessed.

### Access Modes

The `accessModes` field defines which nodes and pods can access the volume:

- **`ReadWriteOnce`** means all the pods on a single mode are able to read and write data.
- **`ReadOnlyMany`** and **`ReadWriteMany`** allow read-only or read-write access by all the pods across multiple nodes.
- **`ReadWriteOncePod`** is a new option in Kubernetes v1.22 that permits read-write access by a single pod on a single node.

### Volume Mode

A `volumeMode` of `Filesystem` is the default, and usually desired, behavior. It means the volume will be mounted into pods as a directory in each pod's filesystem. The alternative value of `Block` presents the volume as a raw block storage device without a pre-configured filesystem.

### Storage Classes

The `storageClassName` is the most important part of the persistent volume's configuration. The storage classes you can use depend on your cluster's hosting environment.

The `standard` class shown here is available when you're running your cluster [on Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine/docs/concepts/persistent-volumes). You can use [`azurefile-csi`](https://docs.microsoft.com/en-us/azure/aks/concepts-storage) for clusters on Microsoft Azure Kubernetes Service (AKS) or `do-block-storage` with DigitalOcean Managed Kubernetes. If you're running your own cluster, you can set up a storage class that [uses your local disks](https://kubernetes.io/blog/2019/04/04/kubernetes-1.14-local-persistent-volumes-ga) when you provision your installation. Trying to use a storage class that's not available in your environment will cause an error when you create your persistent volume.

### Adding Your Volume to Your Cluster

Use kubectl to add your new persistent volume to your cluster:

~~~{.bash caption=">_"}
$ kubectl apply -f pv.yaml
~~~

When running this command, you might see the following error message:

~~~{.ini caption=""}
The PersistentVolume "example-pv" is invalid: spec: 
Required value: must specify a volume type
~~~

This usually occurs when the underlying storage class uses a provisioner to create your storage. The cloud provider is avoiding allocating storage that's not actively used in your cluster. If this happens, you should use dynamic volume creation to automatically create a persistent volume at the time it's used. This is covered in the next section.

## Linking Persistent Volumes to Pods

Persistent volumes are linked to pods by means of a persistent volume claim. A *claim* represents a pod's request to read and write files within a particular volume.

Persistent volume claims are stand-alone objects. Here's what it looks like to claim the example volume created earlier:

~~~{.yaml caption=""}
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: example-pvc
spec:
  storageClassName: ""
  volumeName: example-pv
~~~

The `volumeName` field references the previously created persistent volume. When you link this claim to a pod, the pod will receive access to the `example-pv` volume. The empty `storageClassName` field is intentional and causes the claim to use the storage class set within the persistent volume's definition.

Persistent volume claims may implicitly create new volumes instead of referencing existing ones. You should supply the volume's details as part of the claim's `spec`. Following is the dynamic volume creation method mentioned earlier:

~~~{.yaml caption=""}
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: example-pvc
spec:
  accessModes:
 - ReadWriteOnce
  resources:
 requests:
   storage: 1Gi
  storageClassName: standard
~~~

The claim now has `accessModes` and `storageClassName` fields to configure the volume that'll be created. The volume's capacity is defined via the `resources.requests.storage` field. Please note that this is a slightly different format from a stand-alone persistent volume.

Apply the claim to your cluster using kubectl:

~~~{.bash caption=">_"}
$ kubectl apply -f pvc.yaml

persistentvolumeclaim/example-pvc created
~~~

Provided that you've specified a storage class that's available in your cluster, the claim creation should succeed, even if the stand-alone volume creation failed with an error. The storage class will dynamically provision a new persistent volume that satisfies the claim.

Finally, you can link the claim to your pods using the `volumes` and `volumeMount` fields in the pod manifest:

~~~{.yaml caption=""}
apiVersion: v1
kind: Pod
metadata:
  name: pod-with-pvc
spec:
  containers:
 - name: pvc-container
   image: nginx:latest
   volumeMounts:
     - mountPath: /pv-mount
       name: pv
  volumes:
 - name: pv
   persistentVolumeClaim:
     claimName: example-pvc
~~~

Then add the pod to your cluster:

~~~{.bash caption=">_"}
$ kubectl apply -f pvc-pod.yaml

pod/pod-with-pvc created
~~~

The persistent volume claim is referenced by the pod's `spec.volumes` field. This sets up a pod volume called `pv`, which can be included in the `containers` section of the manifest and is mounted to `/pv-mount`. Files written to this directory in the container will be stored in the persistent volume, letting them outlive the individual container instances.

## Demonstrating Persistence

You can verify this behavior with a quick example.

Get a shell to the pod created earlier:

~~~{.bash caption=">_"}
$ kubectl exec --stdin --tty pod-with-pvc -- sh
~~~

Now write a file to the `/pv-mount` directory, which the persistent volume was mounted to:

~~~{.bash caption=">_"}
$ echo "This file is persisted" > /pv-mount/demo
~~~

Then detach from the container:

~~~{.bash caption=">_"}
$ exit
~~~

Use kubectl to delete the pod:

~~~{.bash caption=">_"}
$ kubectl delete pods/pod-with-pvc

pod "pod-with-pvc" deleted
~~~

Recreate the pod by applying its YAML manifest again:

~~~{.bash caption=">_"}
$ kubectl apply -f pvc-pod.yaml

pod/pod-with-pvc created
~~~

Get a shell to the container in the new pod and read the file from `/pv-mount/demo`:

~~~{.bash caption=">_"}
$ kubectl exec --stdin --tty pod-with-pvc -- sh
$ cat /pv-mount/demo

This file is persisted
~~~

The content of the persistent volume was not affected by the first pod's deletion. It can be remounted into new pods at any time, preserving everything that's been previously written.

## Managing Persistent Volumes With `kubectl`

You can retrieve a list of your persistent volumes using kubectl:

~~~{.bash caption=">_"}
$ kubectl get pv

NAME                                    CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                                           STORAGECLASS    REASON   AGE
pvc-f90a46bd-fac0-4cb5-b020-18b3e74dd3b6   1Gi     RWO         Delete        Bound pv-demo/example-pvc                             do-block-storage         7m52s
~~~

Similarly, you can view all your persistent volume claims:

~~~{.bash caption=">_"}
$ kubectl get pvc

NAME       STATUS   VOLUME                                  CAPACITY   ACCESS MODES   STORAGECLASS    AGE
example-pvc   Bound pvc-f90a46bd-fac0-4cb5-b020-18b3e74dd3b6   1Gi     RWO         do-block-storage   9m
~~~

If a volume or claim shows a **Pending** status, it's usually because the storage class is still provisioning storage for the volume. You can check what's holding up the process by using the `describe` command to view the object's event history:

~~~{.bash caption=">_"}
$ kubectl describe pvc example-pvc

...
Events:
  Type  Reason              Age                 From                                                                         Message
  ----  ------              ----                ----                                                                         -------
  Normal   Provisioning        9m30s               dobs.csi.digitalocean.com_master_68ea6d30-36fe-4f9f-9161-0db299cb0a9c        External provisioner is provisioning volume for claim "pv-demo/example-pvc"
  Normal   ProvisioningSucceeded  9m24s               dobs.csi.digitalocean.com_master_68ea6d30-36fe-4f9f-9161-0db299cb0a9c        Successfully provisioned volume pvc-f90a46bd-fac0-4cb5-b020-18b3e74dd3b6
~~~

To edit your volumes and claims, it's usually best to modify your YAML file and reapply it to your cluster with kubectl:

~~~{.bash caption=">_"}
$ kubectl apply -f changed-file.yaml
~~~

This uses the Kubernetes declarative API model to automatically detect and apply the changes you made. If you'd prefer to use imperative commands, run the `edit` command to open the object's YAML in your editor. Changes will be applied when you save and close the file:

~~~{.bash caption=">_"}
$ kubectl edit pvc example-pvc
~~~

It's not possible to change volume properties, such as access mode and storage class. Other fields, like the volume's capacity, are implementation-dependent: most major storage classes support dynamic resizes, but [this isn't universal](https://kubernetes.io/blog/2018/07/12/resizing-persistent-volumes-using-kubernetes). You should consult your Kubernetes provider's documentation if in doubt.

Don't manually edit dynamically created persistent volume objects by adding a persistent volume claim. Edit the properties on the claim instead.

To remove a volume or a claim, use the `delete` command:

~~~{.bash caption=">_"}
$ kubectl delete pvc example-pvc

persistentvolumeclaim "example-pvc" deleted
~~~

This will empty and remove the storage that was provisioned by your provider. The data inside the volume will be non-recoverable unless separate backups have been made. Don't delete volumes that were dynamically provisioned by a storage class: as with edits and creations, you should interact with the claim they were created for. The storage class will handle the persistent volume object for you.

## Conclusion

Persistent volumes in Kubernetes enable data storage independent of pods, interfacing with various types of storage through storage classes. This tutorial familiarized you with persistent volume use cases, their distinction from regular volumes, and their implementation inside a Kubernetes cluster. Additionally, you learned about kubectl commands to interact with volumes, allowing seamless running of stateful applications in Kubernetes without data loss post-container restarts.

As you continue to explore and enhance your Kubernetes workflows, you might want to give [Earthly](https://www.earthly.dev/), the efficient build automation tool, a shot. It could be a valuable addition to your development toolkit.

{% include_html cta/bottom-cta.html %}
