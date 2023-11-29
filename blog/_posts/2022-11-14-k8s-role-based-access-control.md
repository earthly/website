---
title: "An Ultimate Guide to Kubernetes Role-Based Access Control"
categories:
  - Tutorials
toc: true
author: Boemo Wame Mmopelwa

internal-links:
 - Kubernetes
 - Cluster
 - RBAC
excerpt: |
    Learn how to implement Role-Based Access Control (RBAC) in Kubernetes to secure resources and components from unauthorized access. This tutorial covers the creation of Roles and RoleBindings at both the cluster and namespace levels, as well as the differences between ClusterRoles and Roles.
last_modified_at: 2023-07-19
---
**This article examines the details of implementing Kubernetes RBAC. Earthly provides secure CI pipelines through isolated build environments. [Learn more about Earthly](/).**

Kubernetes has many resources and components that must be kept out of reach of certain users and service accounts. Resources such as secrets have to be encrypted and have strict access. If everyone in a company who has access to the cluster is given limitless power when using the cluster; this is dangerous because Kubernetes secrets and keys can be stolen and used inappropriately. Mostly, anyone can change the cluster's configurations, and it will be hard to know who made changes in case of vulnerability detection.

For this reason, Kubernetes has a mechanism called **Role-based Access Control** (RBAC) that implements rules that define what service account is allowed to access a certain component or resource in a [cluster](/blog/kube-bench).

Implementing RBAC in Kubernetes is easy. You first have to create a Role or ClusterRole which defines what the user or service account is allowed to access. The ClusterRole is applied at a cluster level while the Role is applied at a namespace level.

Next, you have to create a ClusterBinding or a RoleBinding which binds a Kubernetes cluster user with a role. ClusterBinding is applied at a cluster level, while RoleBinding is applied at a namespace level.

In this tutorial, you will learn how to implement RBAC at the cluster level and namespace level. In addition, you will learn how to use the declarative and imperative approach when implementing RBAC.

## Prerequisites

* You will need a running cluster and Kubectl.
* Basic knowledge of how service accounts work.

## How Does RBAC Work In Kubernetes?

![Image]({{site.images}}{{page.slug}}/how.png)\

The RBAC configuration uses the `rbac.authorization.k8s.io/v1` apiVersion to create Roles and RoleBindings. Since RBAC uses rules to delegate permissions, there is a property called verbs in the rules map which states the permissions given to the service account. For example, the user can be granted the following permissions when working with Kubernetes resources:

* `get`
* `list`
* `watch`
* `create`
* `update`
* `patch`
* `delete`

The resources map states which resources and apiGroups the Role is being applied to:

~~~{.yaml caption=""}
rules:
apiGroups: [""]
verbs: ["get", "list"]
resources: ["services"]
~~~

## Implementing RBAC at a Namespace Level

### Create a Namespace

Since Roles only cover namespaces specifically, let's go ahead and create a namespace called `earthly`. All of the manifests we will create in this segment will have the earthly namespace property. Use the following command to create the earthly [namespace](/blog/k8s-namespaces):

~~~{.bash caption=">_"}
kubectl create namespace earthly
~~~

### Create a Role

Now, let's create a Role that will state the permissions that an authorized user will have over the resources created in the earthly namespace. Create a YAML file called `earthly-access-role.yaml` and add the following contents:

~~~{.yaml caption="earthly-access-role.yaml"}
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: earthly-access-role
  namespace: earthly
rules:
  - apiGroups:
        - apps
        - autoscaling
        - batch
        - extensions
        - policy
        - rbac.authorization.k8s.io
    resources:
      - pods
      - deployments
      - ingress
      - jobs
      - namespaces
      - nodes
      - serviceaccounts
      - services
    verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
~~~

The above role gives the service account access to all of the Kubernetes resources stated in the `resource` map above including services, pods, and nodes. In this case we've given the user full permissions by listing all available actions in the `verbs` section. If you simply wanted to give the service account permission to read resources, without the ability to change or delete them, you might change the verb section to something like"

~~~{.yaml caption="earthly-access-role.yaml"}
   verbs: ["get", "list"]
~~~

Next, you can use the following command to create the above Role:

~~~{.bash caption=">_"}
kubectl apply -f earthly-access-role.yaml
~~~

You will get the following output:

~~~{.bash caption="Output"}
role.rbac.authorization.k8s.io/earthly-access-role created
~~~

Simply creating a role will not provide us any security. We need to then assign the role to users. But first, let's take a look at one other way you can create Role in k8s.

### How to Create a Role Imperatively

When you create a resource in Kubernetes without using YAML file declarations then you are using the imperative approach. In this section, we will use the `kubectl create` command to create a Role without the need of a YAML file. Use the following command which takes in the following flags to create a role imperatively:

**verb**: This flag states all the permissions being given to the user.

**resource**: This flag states the resources which are being restricted by the Role.

**namespace**: This is where you state the name of the namespace in which the role is being applied to.

~~~{.bash caption=">_"}
kubectl create role earthly-access-role --verb=get --verb=list \
--resource=services -n earthly
~~~

You will get the following output:

~~~{.bash caption="Output"}
role.rbac.authorization.k8s.io/earthly-access-role created
~~~

### Viewing a Role Configuration

After creating the Role you can use the following command to view the configuration of the Role at any time:

~~~{.bash caption=">_"}
kubectl get role earthly-access-role -n earthly -o yaml
~~~

You will get the following output:

~~~{.yaml caption="earthly-access-role.yaml"}
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  creationTimestamp: "2022-08-09T06:15:30Z"
  name: earthly-access-role
  namespace: earthly
  resourceVersion: "51762"
  uid: 8591929c-5a66-4f31-95c2-f8ceee149cb0
rules:
- apiGroups:
  - ""
  resources:
  - services
  verbs:
  - get
  - list
~~~

## How To Create A RoleBinding

![Image]({{site.images}}{{page.slug}}/how2.jpg)\

Now we can use our new role by assigning it to a service account. We do this by creating a RoleBinding that will give the service account the permissions stated in the we created Role.

~~~{.yaml caption="earthly-access-role.yaml"}
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: earthly-rolebinding
  namespace: earthly
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: earthly-access-role
subjects:
- namespace: earthly
  kind: ServiceAccount
  name: earthly-service-account
~~~

Use the following command to create the RoleBinding:

~~~{.bash caption=">_"}
kubectl apply -f earthly-rolebinding.yaml
~~~

You will get the following output:

~~~{.bash caption="Output"}
rolebinding.rbac.authorization.k8s.io/earthly-rolebinding created
~~~

### How to Create a RoleBinding Imperatively

In this section, you will learn how to create a RoleBinding with just one command, no YAML file required. This RoleBinding gives the serviceaccount the permissions given by the role in the organization namespace:

~~~{.bash caption=">_"}
kubectl create rolebinding test --role=service-reader  \
--serviceaccount=foo:default -n organization
~~~

You will get the following output:

~~~{.bash caption="Output"}
rolebinding.rbac.authorization.k8s.io/test created
~~~

### Viewing a RoleBinding

Use the following command to view the RoleBinding you just created:

~~~{.bash caption=">_"}
kubectl get rolebinding test -n organization -o yaml
~~~

You will get the following output:

~~~{.yaml caption="earthly-access-role.yaml"}
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  creationTimestamp: "2022-04-05T07:04:02Z"
  name: test
  namespace: organization
  resourceVersion: "47073"
  uid: f169775d-ffd0-4b2b-9e7d-a4125d09644a
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: service-reader
subjects:
- kind: ServiceAccount
  name: default
~~~

## The Difference Between ClusterRoles and Roles

![Image]({{site.images}}{{page.slug}}/differences.jpg)\

The Roles we've created so far only applied RBAC **at the namespace level**, but we can **also create RBAC at the cluster level**.

### Declarative

Let's create a ClusterRole instead of a Role in a declarative manner:

~~~{.yaml caption="earthly-access-role.yaml"}
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: volume-access
rules:
  - apiGroups:
        - apps
        - autoscaling
    resources:
      - pods
      - deployments
      - ingress
      - jobs
      - namespaces
      - nodes
      - serviceaccounts
      - services
    verbs: ["get", "list", "watch", "create", "update"]
~~~

As you can see, this file looks very similar to the one we created for the Role, except this time we use `kind: ClusterRole` instead of `kind: Role`.

### Imperatively

~~~{.bash caption=">_"}
kubectl create clusterrole volume-access -o yaml
~~~

To view the full ClusterRole configuration created by the above command, execute the following command:

~~~{.bash caption=">_"}
kubectl get clusterrole volume-access -o yaml
~~~

You will get the following output:

~~~{.yaml caption="earthly-access-role.yaml"}
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  creationTimestamp: "2022-08-09T18:26:47Z"
  name: volume-access
  resourceVersion: "53231"
  uid: 593c53e8-abe9-4e57-a18e-3cce886631f4
rules:
- apiGroups:
  - ""
  resources:
  - persistentvolumes
  verbs:
  - get
  - list
~~~

### Creating a ClusterRoleBinding

### Imperatively

ClusterRoles require their own type of role binding. Use the following command to create a ClusterRoleBinding called `production` which will be connected to the volume-access ClusterRole you created previously:

~~~{.bash caption=">_"}
kubectl create clusterrolebinding production-1 \
--clusterrole=volume-access --serviceaccount=foo:default
~~~

To view the full ClusterBinding configuration description created by the above command, execute the following command:

~~~{.bash caption=">_"}
kubectl get clusterrolebinding production-1 -o yaml
~~~

### Declarative

If you execute the previous command you will get the following output which is the declarative format of the ClusterRoleBinding:

~~~{.yaml caption="earthly-access-role.yaml"}
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  creationTimestamp: "2022-08-09T18:36:46Z"
  name: production-1
  resourceVersion: "53640"
  uid: 65835854-9dc1-468a-809e-75ab499f562e
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: volume-access
subjects:
- kind: ServiceAccount
  name: default
  namespace: foo
~~~

The table below compares a Role and a ClusterRole. Notice that there are very few distinctions. The Kind value is what differentiates them and then the ClusterRole does not have the namespace field since it is applied at [cluster](/blog/kube-bench) level only.

<table>
  <tr>
   <td><strong>Role</strong>
   </td>
   <td><strong>ClusterRole</strong>
   </td>
  </tr>
  <tr>
   <td><code>apiVersion: rbac.authorization.k8s.io/v1 \
kind: Role \
metadata: \
  creationTimestamp: "2022-08-09T06:15:30Z" \
  name: service-reader \
  namespace: earthly \
  resourceVersion: "51762" \
  uid: 8591929c-5a66-4f31-95c2-f8ceee149cb0 \
rules: \
- apiGroups: \
  - "" \
  resources: \
  - services \
  verbs: \
  - get \
  - list</code>
   </td>
   <td><code>apiVersion: rbac.authorization.k8s.io/v1 \
kind: ClusterRole \
metadata: \
  creationTimestamp: "2022-08-09T18:26:47Z" \
  name: volume-access \
  resourceVersion: "53231" \
  uid: 593c53e8-abe9-4e57-a18e-3cce886631f4 \
rules: \
- apiGroups: \
  - "" \
  resources: \
  - persistentvolumes \
  verbs: \
  - get \
  - list</code>
   </td>
  </tr>
</table>

## Conclusion

In this tutorial, you've learned how to use RBAC for namespace and cluster-level implementations. RBAC is crucial for access control as it limits unauthorised service accounts and users, helping to prevent common issues like secret sprawling. Remember: a lost key is as good as a lost system.

Now that you've secured your Kubernetes with RBAC, the next step is to optimize your build process. For that, you might want to give [Earthly](https://www.earthly.dev/) a shot! It's an excellent tool for streamlining and enhancing your build process.

{% include_html cta/bottom-cta.html %}