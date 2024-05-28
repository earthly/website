---
title: "How To Simplify Kubernetes Configuration Using Custom Resources And Controllers"
toc: true
author: Ayomide Akinola

internal-links:
 - Kubernetes
 - Cluster
 - Microservices
excerpt: |
    Learn how to simplify your Kubernetes configuration management using custom resources and controllers. This article guides you through creating a configuration template for your microservice infrastructure and shows you how to use a custom controller to generate microservice configurations from the template.
last_modified_at: 2023-07-19
categories:
  - Orchestration
---
**The article provides an in-depth look at Kubernetes configuration templates. Earthly simplifies the continuous integration pipeline for microservices, benefiting those who use Kubernetes. [Learn more about Earthly](https://cloud.earthly.dev/login).**

## Introduction

Kubernetes is a powerful [container](/blog/docker-slim) orchestration tool that can help you manage your microservices. Often when you have a microservice setup, each microservice requires it's own set of configuration in the Kubernetes cluster that makes it run. The problem is, maintaining closely similar configurations for your microservices, particularly those that use similar tech stacks, can lead to repetitive code that becomes a cumbersome to maintain.

This can be made simpler if all your microservices are managed by a single configuration template. Changes made to this configuration template are easily applied to all the microservices using it. In addition to the maintenance ease, a configuration template can also [make](/blog/using-cmake) it easier to collaborate with other developers because all your microservice configurations and setup are in one place.

In this article, you will learn how to create a configuration template for your microservice infrastructure using custom resources and controllers.

> To follow along with this tutorial, you can make use of [Killercoder's kubernetes cluster playground](https://killercoda.com/playgrounds/scenario/kubernetes).

## Create A Custom Resource

![Custom Resource]({{site.images}}{{page.slug}}/resource.jpg)\

To begin, create a new folder called `k8AppTemplate`. This folder contains all of the files required by your configuration template.

~~~{.bash caption=">_"}
mkdir k8AppTemplate && cd $_
~~~

Next, create the `AppTemplateResource.yaml` file in the `k8AppTemplate` folder and copy and paste the following code into the file:

~~~{.yaml caption="AppTemplateResource.yaml"}
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  # name must match the spec fields below, and be in the form:\
  <plural>.<group>
  name: apptemplates.myapp.domain.com
spec:
  # group name to use for REST API: /apis/<group>/<version>
  group: myapp.domain.com
  # list of versions supported by this CustomResourceDefinition
  versions:
    - name: v1
      # Each version can be enabled/disabled by the Served flag.
      served: true
      # One and only one version must be marked as the storage version.
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                serviceName:
                  type: string
                environment:
                  type: string
                deploymentReplicas:
                  type: integer
                  maximum: 5
                  default: 1
                imageName:
                  type: string
                imageVersion:
                  type: string
  # either Namespaced or Cluster
  scope: Namespaced
  names:
    # plural name to be used in the URL: /apis/<group>/<version>/<plural>
    plural: apptemplates
    # singular name to be used as an alias on the CLI and also for\
    displaying
    singular: apptemplate
    # kind is normally the CamelCased singular type. Your resource\
    manifests use this.
    kind: AppTemplate
    # shortNames allow shorter string to match your resource on the CLI
    shortNames:
    - apptemp
~~~

The first two lines define the apiVersion of Kubernetes and the resource type (CustomResourceDefinition)

~~~{.yaml caption="AppTemplateResource.yaml"}
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
~~~

The metadata session stores additional information about your resource and also defines its name. Resource names are typically an extension of a subdomain, as shown above with `apptemplate.myapp.domain.com` standing as the name and `myapp.domain.com` as the subdomain. You are free to use any subdomain you want.

~~~{.yaml caption="AppTemplateResource.yaml"}
metadata:
    name: apptemplates.myapp.domain.com
~~~

The structural definition of your custom resources is held in the `spec` session. It allows you to specify what data your custom resource collects and how that data should be validated.

~~~{.yaml caption="AppTemplateResource.yaml"}
spec:
  # group name to use for REST API: /apis/<group>/<version>
  group: myapp.domain.com
  # list of versions supported by this CustomResourceDefinition
  versions:
    - name: v1
      # Each version can be enabled/disabled by the Served flag.
      served: true
      # One and only one version must be marked as the storage version.
      storage: true
      schema:
        …
~~~

The `group` value must be similar to the subdomain you used in the `metadata` section to name your custom resource, in this case, `myapp.domain.com`. In the kubernetes REST API, the group name is used to uniquely identify your resources - `/apis/group/<version>`.

In the `spec` section, you can also define different data structures for the various Kubernetes versions you intend to support. Only version 1 will be supported in this tutorial.

~~~{.yaml caption="AppTemplateResource.yaml"}
 schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                serviceName:
                  type: string
                environment:
                  type: string
                deploymentReplicas:
                  type: integer
                  maximum: 5
                  default: 1
                imageName:
                  type: string
                imageVersion:
                  type: string

~~~

Next, you can define a typed data structure for your custom resource in the `schema` section. You will collect the `serviceName` for this tutorial, which will be used to create a unique namespace for each microservice. The `environment` field allows you to specify the microservice's development stage, which can be `production`, `staging`, or `development`. The `deploymentReplicas` property allows you to manage the auto scaling of each microservice [deployment](/blog/deployment-strategies) and has a default value of 1 and a maximum value of 5. You can specify the docker image name and version for each microservice using the `imageName` and `imageVersion` parameters.

~~~{.yaml caption="AppTemplateResource.yaml"}
# either Namespaced or Cluster
  scope: Namespaced
  names:
    # plural name to be used in the URL: /apis/<group>/<version>/<plural>
    plural: apptemplates
    # singular name to be used as an alias on the CLI and for display
    singular: apptemplate
    # kind is normally the CamelCased singular type. Your resource\
    manifests use this.
    kind: AppTemplate
    # shortNames allow shorter string to match your resource on the CLI
    shortNames:
    - apptemp

~~~

You can make your custom resource available to the entire cluster or to a specific namespace. It will be namespace scoped for this tutorial. The other names for your custom resources - `plural`, `singular`, and `shortNames` - are required when using Kubectl or the Kubernetes API to interact with your custom resource.

Save the `AppTemplateResource.yaml` file and then apply the custom resource to your cluster:

~~~{.bash caption=">_"}
kubectl apply -f  AppTemplateResource.yaml
~~~

And you should see a confirmation output,

~~~{.bash caption="Output"}

customresourcedefinition.apiextensions.k8s.io/apptemplates.myapp.domain.com created
~~~

Now, proceed to use the AppTemplate custom resource to create your first microservice configuration. Add a new file, `sample-service.yaml` to the `k8AppTemplate` folder,

~~~{.bash caption=">_"}
touch sample-service.yaml
~~~

Next, copy, and paste the code below into the file,

~~~{.yaml caption="sample-service.yaml"}
apiVersion: "myapp.domain.com/v1"
kind: AppTemplate
metadata:
  name: sample-service
spec:
  serviceName: sample-service
  environment: development
  deploymentReplicas: 2
  imageName: "sample-service_node_app"
  imageVersion: "0.1"
~~~

The first two lines defines version of the custom resource to use and the `kind` of resource as defined in the custom resources

~~~{.yaml caption="sample-service.yaml"}
apiVersion: "myapp.domain.com/v1"
kind: AppTemplate
~~~

The `spec` section contains all the defined data specifications as defined in the custom resource.

~~~{.yaml caption="sample-service.yaml"}
spec:
  serviceName: sample-service
  environment: development
  deploymentReplicas: 2
  imageName: "sample-service_node_app"
  imageVersion: "0.1"
~~~

Save the file and apply, the new microservice apptemplate configuration;

~~~{.bash caption=">_"}
kubectl apply -f sample-service.yaml
~~~

You should see an output similar to this.

~~~{.bash caption="Output"}
apptemplate.myapp.domain.com/sample-service created
~~~

The `sample-service` microservice specific configuration has been created, and can now be used to modify your main configuration template.

Next, create your main configuration template. This template will contain common K8s configuration files like deployment, service, statefulset, [ingress](/blog/building-on-kubernetes-ingress), e.t.c. These configurations will need to be in a git repo for easy maintenance. For the purpose of this tutorial, you can use the configurations in this repository, <https://github.com/Doctordrayfocus/AppTemplateConfigs>

Clone the repository and change into its directory

~~~{.bash caption=">_"}
git clone https://github.com/Doctordrayfocus/AppTemplateConfigs && \
cd AppTemplateConfigs
~~~

> The configuration files in the repository above are mainly for example purposes. The aim is to show you how you can make use of the microservice-specific configuration created from the custom resource to modify the main configuration template.

This configuration template contains deployment.yaml, service.yaml, namespace.yaml files and an `extras` folder. Each of your configuration files has access to all the specifications defined in the appTemplate custom resource. For instance, check out the deployment.yaml code

~~~{.bash caption=">_"}
cat deployment.yaml
~~~

-

~~~{.yaml caption="deployment.yaml"}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${serviceName}-deployment
  namespace: ${environment}-${serviceName}
  labels:
    app: ${serviceName}
spec:
  replicas: ${deploymentReplicas}
  selector:
    matchLabels:
      app: ${serviceName}
  template:
    metadata:
      labels:
        app: ${serviceName}
    spec:
      containers:
      - name: ${serviceName}-deployment
        image: ${DOCKER_REGISTRY}/${imageName}:${imageVersion}
        ports:
        - containerPort: 3000
~~~

Notice that the `serviceName`, `environment`, `deploymentReplicas` and so on, are used as placeholders in this format - `${spec}`.  

You should also take note of the `DOCKER_REGISTRY` placeholder. It is an example of a global variable that can be used by the custom controller that manages the deployment of your microservice. You shouldn't worry about it for now, it will be explained later in the tutorial.

Now that your main configuration template is ready, there has to be a system that will generate new configurations from the main template using the provided microservice-specific configuration and create each microservice by applying these generated configurations to the kubernetes cluster. This system can be provided by a kubernetes custom controller.

## Create A Kubernetes Custom Controller

![Custom Controller]({{site.images}}{{page.slug}}/controller.jpg)\

Kubernetes custom controllers are applications that make use of Kubernetes' declarative REST API to interact with the Kubernetes cluster. They are usually deployed on the cluster and can be written in any programming languages including Go, NodeJS, Python, Java, e.t.c.

To proceed, create a new folder named `controller`. This folder will contain all the configurations for your custom controller.

~~~{.bash caption=">_"}
mkdir controller && cd $_ 
~~~

Because the controller will be accessing and handling resources in your cluster, you will need to configure its access.

To do that, first create a new service account for the controller. ServiceAccount allows you to control who or what has access to your cluster and which resources they can use.

Create a new file `AppServiceAccount.yaml`,

~~~{.bash caption=">_"}
touch AppServiceAccount.yaml
~~~

Copy and paste the following into the file:

~~~{.yaml caption="AppServiceAccount.yaml"}
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-template
~~~

Next, you need to add a `ClusterRoleBinding` to assign some roles and permissions to the service account. For the controller to function properly, it would need to have full access to the cluster - hence `cluster-admin` role.

Create a new file `AppTemplateRoleBinding.yaml`.

~~~{.yaml caption="AppTemplateRoleBinding.yaml"}
touch AppTemplateRoleBinding.yaml
~~~

Copy and paste the code below,

~~~{.yaml caption="AppTemplateRoleBinding.yaml"}
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: app-template-role-binding
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: app-template
  namespace: default
~~~

Next, create a configuration for your custom controller using a `ConfigMap`. This configuration will primarily hold information needed by the controller to detect and manage the custom resource you created earlier. Also, you can use it to set global configurations for your main configuration as used in the `deployment.yaml` file above (DOCKER_REGISTRY).

To continue, create a new file `configMap.yaml`,

~~~{.bash caption=">_"}
touch configMap.yaml
~~~

Copy and paste the following code,

~~~{.yaml caption="configMap.yaml"}
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-template-config
data:
  # your custom resource groupname
  RESOURCE_GROUP: "myapp.domain.com"

  # your custom resource name (plural)
  RESOURCE_NAME: "apptemplates"

  # default api version of your custom resource
  API_VERSION: "v1"

  # default docker container registry
  DOCKER_REGISTRY: "drayfocus"

  # default custom resource namespace
  RESOURCE_NAMESPACE: "default"

  # git repo url for template config files
  CONFIG_REPO_URL: \
  "https://github.com/Doctordrayfocus/AppTemplateConfigs.git"

  # repo sync interval (in seconds)
  SYNC_INTERVAL: "3"
~~~

`RESOURCE_GROUP` defines the group of your custom resource, `RESOURCE_NAME` defines the plural name of your `apptemplate` custom resource, `API_VERSION` defines the api version the custom controller should use, `RESOURCE_NAMESPACE` defines the namespace of your custom resources, `CONFIG_REPO_URL` takes the git repository of your main configuration template, and `SYNC_INTERVAL` defines how frequent the controller should check for updates in your main configuration repository. The configMap can also take global configuration data like the `DOCKER_REGISTRY` data above.

Finally, you need to deploy the controller on your kubernetes cluster, so that it can have access to the cluster.

Now, create a new file `deployment.yaml`,

~~~{.bash caption=">_"}
touch deployment.yaml
~~~

Next, copy, and paste the following into the file,

~~~{.yaml caption="deployment.yaml"}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: apptemplate-controller
spec:
  replicas: 1
  selector:
    matchLabels:
      app: apptemplate-controller
  template:
    metadata:
      labels:
        app: apptemplate-controller
    spec:
      serviceAccountName: app-template
      containers:
        - name: apptemplate
          image: drayfocus/apptemplate-controller:0.49
          ports:
            - containerPort: 8080
          imagePullPolicy: Always
          envFrom:
            - configMapRef:
                name: app-template-config
~~~

In the deployment file, the service account created earlier is attached to the custom controller.

~~~{.yaml caption="deployment.yaml"}
  spec:
      serviceAccountName: app-template
~~~

The configMap was also attached to the custom controller,

~~~{.yaml caption="deployment.yaml"}
 envFrom:
            - configMapRef:
                name: app-template-config
~~~

The `drayfocus/apptemplate-controller:0.49` docker image is used as the engine that runs the custom controller.

> If you are interested in how the `drayfocus/apptemplate-controller:0.49` docker image works, you can browse the code on [github](https://github.com/Doctordrayfocus/AppTemplateController).

Now, apply all the controller configurations to your [cluster](/blog/kube-bench,

~~~{.bash caption=">_"}
cd  ..  &&  kubectl apply -f controller
~~~

You should see the following confirmation:

~~~{.bash caption="output"}
serviceaccount/app-template created
clusterrolebinding.rbac.authorization.k8s.io/app-template-role-binding created
configmap/app-template-config created
deployment.apps/apptemplate-controller created
~~~

Now that your custom controller is running, the `sample-service` microservice you created earlier using the apptemplate custom resource should have all its resources (namespace, deployment, services, ) deployed. To confirm this, check for the microservice namespace

~~~{.bash caption=">_"}
kubectl get namespaces
~~~

You should be able to find the `${environment}-sample-service namespace`, where the `environment` is the value of the environment in the apptemplate e.g development

~~~{.bash caption="output"}
…
development-sample-service    Active     41s
…
~~~

You can also check for its pods

~~~{.bash caption=">_"}
kubectl get pods -n development-sample-service
~~~

-

~~~{.bash caption=">_"}

Sample-service-deployment-69d89bf574-2j4xf      1/1      Running   0    56s
sample-service-deployment-69d89bf574-m5gnx      1/1     Running    0    56s
~~~

To create a new microservice, simply create a new `apptemplate` resources,

~~~{.bash caption=">_"}
# sample-service-2.yaml
apiVersion: "myapp.domain.com/v1"
kind: AppTemplate
metadata:
  name: sample-service-2
spec:
  serviceName: sample-service-2
  environment: production
  deploymentReplicas: 1
  imageName: "sample-service_node_app"
  imageVersion: "0.1"
~~~

Then apply the microservice template to your cluster,

~~~{.bash caption=">_"}
kubectl apply -f sample-service-2.yaml
~~~

You can also view, delete, manage your apptemplate custom resources using `kubectl`.

~~~{.bash caption=">_"}
kubectl get apptemplate
~~~

-

~~~{.bash caption=">_"}
NAME                  AGE
sample-service        13m
sample-service-2      1m
~~~

## Conclusion

This tutorial walked you through using Kubernetes `custom resources` and controllers for easy configuration management. We covered how to define configurations using `custom resources`, built a custom controller, and set up correct permissions with `ServiceAccount` and `ClusterRoleBinding`. All in all, a neat way to manage your microservice configurations.

Now that you've got Kubernetes configuration down, you might be thinking about how to streamline your build process. If so, why not give [Earthly](https://cloud.earthly.dev/login) a shot? It could be the next step in making your development process even smoother. Cheers to simpler Kubernetes management and efficient build processes!

{% include_html cta/bottom-cta.html %}
