---
title: "How to automate a microservice setup in Kubernetes using Earthly"
categories:
  - Tutorials
toc: true
author: Ayomide Akinola

internal-links:
 - kubernetes
topic: kubernetes
funnel: 2
excerpt: |
    Learn how to automate your microservice setup in Kubernetes using Earthly. This tutorial walks you through the process of creating a template, building and deploying your microservices, and automating the entire setup process.
---

## Introduction

Kubernetes(K8s) is an open source system that automates the [deployment](/blog/deployment-strategies), scaling, and management of containerized applications such as microservices. It's designed to [make](/blog/makefiles-on-windows) it easy to deploy applications to a wide range of virtual machines and cloud providers e.g Digital ocean, AWS. K8s is built on a foundation of open standards. It helps you manage the lifecycle of processes running in the container. This guide will walk you through how to automatically setup your microservices with k8s using Earthly.
A complete microservice setup on Kubernetes requires both the configuration and deployment of your application. Each service will have its own unique functionality and operates independently of the other services, and can be deployed individually.

## Why Should Microservice Setup Be Automated?

Microservice configuration and [deployment](/blog/deployment-strategies) should be automated because it makes it easier for you to add new components to the system or change existing ones. For example, if you need to add a new feature or fix a bug in one of your microservices, you can do so without having to manually set up or deploy it on every instance of Kubernetes where it runs. Automation also helps ensure consistency across all instances of Kubernetes and prevents human error from causing problems in your codebase.

Lastly, microservices are applications that run on different hosts, so they need to be configured separately. If you have multiple instances of the same service running, each instance needs its own configuration. This means that you need to have a way to ensure that every instance is configured correctly before it can be deployed. Automating this process makes it easy for you to repeat this process without stress.

## How to Automate a Microservice Setup in Kubernetes Using Earthly

## Prerequisites

- You have Earthly set up. If you don't, you can install it by following these [instructions](https://earthly.dev/get-earthly).

- You have a basic understanding of [Docker](/blog/rails-with-docker) and Kubernetes.
  
## Setup A Template

To automate your microservice setup, you need to create a template that will be used to generate new microservices with default docker and kubernetes configuration, as well as build push [docker](/blog/rails-with-docker) images and deploy kubernetes configuration to your kubernetes cluster.

To get started, create a brand new folder called K8AutoSetup.

(The completed solution is available for reference in [my github repo](https://github.com/Doctordrayfocus/K8AutoSetup))

~~~{.bash caption=">_"}
mkdir K8AutoSetup
~~~

In your code editor, open the new folder and create a new file called "Earthfile." This Earthfile will contain your template's setup, build, and deploy commands. It runs in a docker container and is similar to a dockerfile. It is platform independent, so you can use your template in any environment.

Include an earthfile version, dependencies, and a work directory.

~~~{.bash caption="earthfile"}
VERSION 0.6
FROM bash:4.4
WORKDIR /build-arena
~~~

The string `VERSION 0.6` specifies the earthly version to be used. Because some shell commands will be executed, the `bash:4.4` [docker](/blog/rails-with-docker) image is used here. The `WORKDIR` is the container folder where the operations will take place; it can be set to anything.

## Add Install Target

A "Target" is a set of scripts that perform a specific operation in an Earthfile. You will create an `install` target that will copy, modify, and configure your microservices' configuration files.

Before you proceed, you must include these configuration files in the template.

Create a directory called "**templates**". Then, in the "**templates**" folder, place the "**docker**" and "**kubernetes**" folders. The "**docker**" folder contains all of your Docker configurations, while the "**kubernetes**" folder contains all of your Kubernetes configurations.

Your folder structure should look like this

~~~{.dockerfile caption="Dockerfile"}
$ tree
.
├── Earthfile
└── templates
    └── docker
    └── kubernetes

3 directories, 1 file

~~~

Create a new **Earthfile** in the *docker* directory. This Earthfile will include instructions for creating your Docker image as well as pushing it to a container repository. You will also require some source code, which will be included in the Docker image. You can use this sample nodeJs application [https://github.com/Doctordrayfocus/vue-typescript-template](https://github.com/Doctordrayfocus/vue-typescript-template) for this tutorial.

Add this to your Earthfile.

~~~{.dockerfile caption="Earthfile"}
VERSION 0.6
FROM bash:4.4
WORKDIR /setup-arena
  
project:
    # clone project
    GIT CLONE https://github.com/Doctordrayfocus/vue-typescript-template \
    nodejs
    RUN rm nodejs/package-lock.json
    SAVE ARTIFACT nodejs /nodejs

node-app:
    # We need node js to install and run the app
    FROM node:14.14.0-alpine3.12
    
    ARG version='0.1'
    ARG docker_registry='drayfocus/earthly-sample'
    ARG service='sample'
    ARG node_env='development'
    
    # First, create the application directory
    RUN mkdir -p /app.
      
    ## Then copy our app source code into the image
    COPY +project/nodejs /app.

    # Next, set our working directory
    WORKDIR /app.

    ## Install app packages
    RUN npm install
      
    ## open port 3000
    EXPOSE 3000

    ## Start node server
    ENV NODE_ENV ${node_env}

    IF [ "$node_env" = "development" ]
    CMD ["npm", "run", "dev"]
    ELSE
    CMD ["npm", "run", "build"]
    END
    
    SAVE IMAGE --push ${docker_registry}/${service}_node_app:${version}
    
~~~

The `project` target copies the source code for the app from github into the `nodejs` folder. The file `package-lock.json` is then removed, allowing for a fresh installation of the app packages. Finally, `SAVE ARTIFACT nodejs /nodejs` saves the contents of the `nodejs` folder for use outside the target.

(In a real project, pulling the source from elsewhere in this way may be unnecessary but for tutorial purposes it allows us to focus on the task at hand and ignore the node.js implementation.)

The content of the `node-app` target is very similar to that of a Dockerfile. It creates the docker image from the base image `node:14.14.0-alpine3.12`.

~~~{.bash caption=">_"}
ARG version='0.1'
ARG docker_registry='drayfocus/earthly-sample'
ARG service='sample'
ARG node_env='development'
~~~

You can easily pass arguments to Earthly to customize a target. Each of the preceding arguments has a default value. The `version` argument specifies the version of the docker image. You can configure your Docker container registry using the `docker_registry` argument. The `service` argument specifies the microservice for which the docker image is being built. Furthermore, the `node_env` option allows you to specify the node environment that should be used in the docker image.

~~~{.dockerfile caption="Dockerfile"}

SAVE IMAGE --push ${docker_registry}/${service}_node_app:${version}
~~~

The last line of this target tags and pushes the built docker image to the specified [container](/blog/docker-slim) registry.

Next, you'll add your Kubernetes configuration files, such as ConfigMaps, Secrets, Deployments, Services, and so on. To deploy the node js app, you will need a `service.yaml` and a `deployment.yaml` file.

Each microservice is expected to exist in its own namespace regardless of the type of application you are attempting to build. As a result, you will also require a `namespace.yaml` file.

Because these kubernetes configuration files must be generated automatically, you will create a new **Earthfile** in the **kubernetes** folder. This also makes it easier to automatically generate copies of the configuration files for each project environment, such as "prod," "dev," and "staging."

Add a new **Earthfile** to the **kubernetes** folder. To auto-generate the deployment.yaml file, add this to the Earthfile.

~~~{.yaml caption="deployment.yaml"}
VERSION 0.6

DEPLOYMENT:
    COMMAND
        ARG service='sample'
        ARG env='prod'
        ARG dir="./$service/environments/$env"
        ARG file="$dir/deployment.yaml"
    ARG version='0.1'
    ARG docker_registry='drayfocus/earthly-sample' 

    ARG OUTPUT="apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${service}-deployment
  namespace: ${env}-$service
  labels:
    app: $service
spec:
  replicas: 1
  selector:
    matchLabels:
      app: $service
  template:
    metadata:
      labels:
        app: $service
    spec:
      containers:
      - name: ${service}-deployment
        image: ${docker_registry}/${service}_node_app:v${version}
        ports:
        - containerPort: 3000
"
    RUN mkdir -p $dir
    RUN echo "$OUTPUT" > "$file"
~~~

Add for `services.yaml` auto generation, add

~~~{.yaml caption="services.yaml"}
SERVICE:
    COMMAND
    ARG service='sample'
    ARG env='prod'
    ARG dir="./$service/environments/$env"
    ARG file="$dir/service.yaml"
    ARG OUTPUT="apiVersion: v1
kind: Service
metadata:
  name: $service-service
  namespace: $env-$service
spec:
  selector:
    app: $service
  type: LoadBalancer
  ports:
  - protocol: TCP
    port: 5000
    targetPort: 3000
    nodePort: 31110
"
    RUN echo "$OUTPUT" > "$file"
~~~

Then to auto generate the namespace.yaml file

~~~{.yml caption="namespace.yaml"}
NAMESPACE:
    COMMAND
    ARG service='sample'
    ARG env='prod'
    ARG dir="./$service/environments/$env"
    ARG file="$dir/namespace.yaml"

    ARG OUTPUT="apiVersion: v1
kind: Namespace
metadata:
  name: $env-$service
"
    RUN echo "$OUTPUT" > "$file"
~~~

The above scripts let you specify arguments that can change each configuration file for a specific microservice and project environment.

Return to your main **Earthfile** in the root folder. Both the **docker** and **templates** folders' Earthfiles must be imported into the main **Earthfile**. This is so that the main **Earthfile** can access them. Your main **Earthfile** should now look something like this.

~~~{.dockerfile caption="Earthfile"}
VERSION 0.6
FROM bash:4.4
WORKDIR /build-arena
IMPORT ./templates/kubernetes AS kubernetes_engine
IMPORT ./templates/docker AS docker_engine
~~~

Then add `install` target to initiate template installation from the main **Earthfile**

~~~{.dockerfile caption="Earthfile"}
install:
    ARG service='sample'
    ARG envs='dev,prod'
    ARG version='0.1'
    ARG docker_registry='drayfocus/earthly-sample' 

    WORKDIR /setup-arena
    
    FOR --sep="," env IN "$envs"    
        ENV dir="./$service/environments/$env"
        RUN echo "Creating environment $env"
        RUN mkdir -p $dir
        DO kubernetes_engine+DEPLOYMENT --service=$service --env=$env \
        --dir=$dir --version=$version --docker_registry=$docker_registry
        DO kubernetes_engine+SERVICE --service=$service \
        --env=$env --dir=$dir
        DO kubernetes_engine+NAMESPACE --service=$service \
        --env=$env --dir=$dir
    END
    SAVE ARTIFACT $service AS LOCAL ${service}

~~~

The `install` target accepts the project environments as a comma-separated string, such as `dev,prod`, converts the string to an array, and then uses the templates to generate new kubernetes configuration files for each environment. It also places the template raw configurations and other files in the newly created `service` folder. It then uses `SAVE ARTIFACT $service AS LOCAL ${service}` to export all of these files and folders into a new folder in your local directory with the specified `service` name.

To test your script, run this in this project root folder

~~~{.dockerfile caption="Earthfile"}
earthly +install --service=sample-service
~~~

You should see something like this.

~~~{.bash caption=">_"}
nodejs_engine+setup-templates | --> COPY setup-environment.sh .
nodejs_engine+setup-templates | envs=dev,prod service=sample-service
nodejs_engine+setup-templates | --> COPY kubernetes kubernetes
nodejs_engine+setup-templates | envs=dev,prod service=sample-service
nodejs_engine+setup-templates | --> RUN chmod -R 775 .
nodejs_engine+setup-templates | envs=dev,prod service=sample-service
nodejs_engine+setup-templates | --> RUN mkdir -p $service/environments
nodejs_engine+setup-templates | envs=dev,prod service=sample-service
nodejs_engine+setup-templates | --> RUN ./setup-environment.sh $envs $service $docker_registry $version
nodejs_engine+setup-templates | Setting up deployments deployment.yaml for dev
nodejs_engine+setup-templates | Setting up services service.yaml dev
nodejs_engine+setup-templates | Setting up namespace for dev
nodejs_engine+setup-templates | Setting up deployments deployment.yaml for prod
nodejs_engine+setup-templates | Setting up services service.yaml prod
nodejs_engine+setup-templates | Setting up namespace for prod
g/D/K8AutoSetup+install | envs=dev,prod service=sample-service
g/D/K8AutoSetup+install | --> COPY templates sample-service/templates
g/D/K8AutoSetup+install | envs=dev,prod service=sample-service
g/D/K8AutoSetup+install | --> COPY version-update.sh ./sample-service
g/D/K8AutoSetup+install | envs=dev,prod service=sample-service
g/D/K8AutoSetup+install | --> COPY Earthfile ./sample-service
g/D/K8AutoSetup+install | envs=dev,prod service=sample-service
g/D/K8AutoSetup+install | *cached* --> SAVE ARTIFACT sample-service github.com/Doctordrayfocus/K8AutoSetup+install/sample-service AS LOCAL sample-service
              output | --> exporting outputs
              output | [██████████] 100% copying files
              output | 

 3. Push ⏫ (disabled)
————————————————————————————————————————————————————————————————————————————————

To enable pushing use

        earthly --push ...

 4. Local Output 🎁
————————————————————————————————————————————————————————————————————————————————

Artifact github.com/Doctordrayfocus/K8AutoSetup+install/sample-service output as sample-service

========================== 🌍 Earthly Build  ✅ SUCCESS ==========================

Share your logs with an Earthly account (experimental)! Register for one at https://ci.earthly.dev
~~~

 > Incase you run into errors, ensure all your files are saved

If your script ran without any errors, you should see a new folder named "**sample-service**" created. This folder is a clone of the main template project, but with a "**environments**" folder that contains kubernetes configurations generated during setup for each specified environment.

## Add Build Target  

Add the `build` target to the main **Earthfile** to continue. This target will execute the docker build script and push the completed Docker image to a container registry.

~~~{.dockerfile caption="Earthfile"}
build:
    ARG version='0.1'
    ARG docker_registry='drayfocus'
    ARG service='sample'
    ARG envs='dev,prod'
    ARG node_env="development"

    BUILD docker_engine+node-app --version=$version \
    --docker_registry=$docker_registry --service=$service \
    --node_env=$node_env
~~~

Following the creation of the Docker image, the `deployment.yaml` file for each environment must be updated with the most recent Docker image version. To accomplish this, update your build target.

~~~{.yml caption="deployment.yaml"}
build:
    ARG version='0.1'
    ARG docker_registry='drayfocus'
    ARG service='sample'
    ARG envs='dev,prod'
    ARG node_env="development"

    BUILD docker_engine+node-app --version=$version \
    --docker_registry=$docker_registry --service=$service \
    --node_env=$node_env

    ## Update deployment.yaml with latest versions
    FOR --sep="," env IN "$envs"    
        DO kubernetes_engine+DEPLOYMENT --service=$service \
        --env=$env --version=$version --docker_registry=$docker_registry
        SAVE ARTIFACT $service/environments/$env/* AS LOCAL \
        ${service}/environments/$env/
    END
~~~

Your main **Earthfile** should now look like this,  

~~~{.dockerfile caption="Earthfile"}
VERSION 0.6
FROM bash:4.4
WORKDIR /build-arena
IMPORT ./templates/kubernetes AS kubernetes_engine
IMPORT ./templates/docker AS docker_engine

install:
    ARG service='sample'
    ARG envs='dev,prod'
    ARG version='0.1'
    ARG docker_registry='drayfocus/earthly-sample' 

    WORKDIR /setup-arena
    
    FOR --sep="," env IN "$envs"    
        ENV dir="./$service/environments/$env"
        RUN echo "Creating environment $env"
        RUN mkdir -p $dir
        DO kubernetes_engine+DEPLOYMENT --service=$service \
        --env=$env --dir=$dir --version=$version \
        --docker_registry=$docker_registry
        DO kubernetes_engine+SERVICE --service=$service \
        --env=$env --dir=$dir
        DO kubernetes_engine+NAMESPACE --service=$service \
        --env=$env --dir=$dir
    END
    SAVE ARTIFACT $service AS LOCAL ${service}

build:
    ARG version='0.1'
    ARG docker_registry='drayfocus'
    ARG service='sample'
    ARG envs='dev,prod'
    ARG node_env="development"

    BUILD docker_engine+node-app --version=$version \
    --docker_registry=$docker_registry --service=$service \
    --node_env=$node_env

    ## Update deployment.yaml with latest versions
    FOR --sep="," env IN "$envs"    
        DO kubernetes_engine+DEPLOYMENT --service=$service \
        --env=$env --version=$version --docker_registry=$docker_registry
        SAVE ARTIFACT $service/environments/$env/* AS LOCAL \
        ${service}/environments/$env/
    END
~~~

To test the build target,

Install the template

~~~{.dockerfile caption="Eathfile"}
earthly +install --service=sample-service
~~~

Change directory to "**sample-service**"

~~~{.dockerfile caption="Eathfile"}
cd sample-service
~~~
  
Then run the build target

~~~{.dockerfile caption="Eathfile"}
earthly --push +build --service=sample-service --version=0.1
~~~

> The `--push` argument must be added so that earthly will push the generated docker image to the specified container registry.
> The docker image running earthly must have the right authority to successfully push the docker image to the remote repository. If you use docker hub you can run `docker login --username=your_username --password=your_password`. If you use AWS, follow this [tutorial](https://docs.aws.amazon.com/AmazonECR/latest/userguide/getting-started-cli.html) to authenticate docker. For digitalocean, follow this [tutorial](https://docs.digitalocean.com/products/container-registry/how-to/use-registry-docker-kubernetes/). For Microsoft Azure, follow this [tutorial](https://docs.microsoft.com/en-us/azure/container-registry/container-registry-authentication?tabs=azure-cli). and for Google Cloud, follow this [tutorial](https://cloud.google.com/container-registry/docs/advanced-authentication).

If your build script was successful, you should see an output like this-

~~~{.bash caption="Output"}
nodejs_docker_engine+node-app | docker_registry=drayfocus node_env=developement service=sample-service version=0.1
nodejs_docker_engine+node-app | *cached* --> IF [ "$node_env" = "development" ]
             context | --> local context .
             context | --> local context .
             context | --> local context .
             ongoing | context (5 seconds ago), context (5 seconds ago) and 1 others
             context | [          ]   0% transferring .:
             context | transferred 0 file(s) for context . (387 B, 8 file/dir stats)
             context | [██████████] 100% transferring .:
             context | transferred 0 file(s) for context . (37 B, 1 file/dir stats)
             context | [██████████] 100% transferring .:
             context | [██████████] 100% transferring .:
              +build | service=sample-service version=0.1
              +build | *cached* --> COPY ./templates/php/kubernetes kubernetes
              +build | service=sample-service version=0.1
              +build | *cached* --> COPY environments environments
              +build | service=sample-service version=0.1
              +build | *cached* --> COPY version-update.sh .
              +build | service=sample-service version=0.1
              +build | *cached* --> RUN chmod -R 775 .
              +build | service=sample-service version=0.1
              +build | *cached* --> RUN ./version-update.sh $envs $service $docker_registry $version
              +build | service=sample-service version=0.1
              +build | *cached* --> SAVE ARTIFACT environments +build/environments AS LOCAL environments
              output | --> exporting outputs
              output | [██████████] 100% exporting layers
              output | [██████████] 100% exporting manifest sha256:8a424cfa973897f8ec2defa2368a53932ff1bbf40801fd71e5eeedd2a35c9e64
              output | [██████████] 100% exporting config sha256:3dae0710a0b6810fca60d02196168439a594c1a745e223f0e8d7edabdb6dff60
              output | [██████████] 100% copying files
              output | [██████████] 100% pushing layers
              output | [██████████] 100% pushing manifest for docker.io/drayfocus/sample-service_node_app:0.1@sha256:8a424cfa973897f8ec2defa2368a53932ff1bbf40801fd71e5eeedd2a35c9e64
              output | [██████████] 100% transferring docker.io/drayfocus/sample-service_node_app:0.1

 3. Push ⏫
————————————————————————————————————————————————————————————————————————————————

Pushed image ./templates/nodejs/docker+node-app as drayfocus/sample-service_node_app:0.1

 4. Local Output 🎁
————————————————————————————————————————————————————————————————————————————————

Artifact +build/environments output as environments
Image ./templates/nodejs/docker+node-app output as drayfocus/sample-service_node_app:0.1

========================== 🌍 Earthly Build  ✅ SUCCESS ==========================

Share your logs with an Earthly account (experimental)! Register for one at https://ci.earthly.dev.nodejs_docker_engine+node-app | docker_registry=drayfocus node_env=developement service=sample-service version=0.1
nodejs_docker_engine+node-app | *cached* --> IF [ "$node_env" = "development" ]
             context | --> local context .
             context | --> local context .
             context | --> local context .
             ongoing | context (5 seconds ago), context (5 seconds ago) and 1 others
             context | [          ]   0% transferring .:
             context | transferred 0 file(s) for context . (387 B, 8 file/dir stats)
             context | [██████████] 100% transferring .:
             context | transferred 0 file(s) for context . (37 B, 1 file/dir stats)
             context | [██████████] 100% transferring .:
             context | [██████████] 100% transferring .:
              +build | service=sample-service version=0.1
              +build | *cached* --> COPY ./templates/php/kubernetes kubernetes
              +build | service=sample-service version=0.1
              +build | *cached* --> COPY environments environments
              +build | service=sample-service version=0.1
              +build | *cached* --> COPY version-update.sh .
              +build | service=sample-service version=0.1
              +build | *cached* --> RUN chmod -R 775 .
              +build | service=sample-service version=0.1
              +build | *cached* --> RUN ./version-update.sh $envs $service $docker_registry $version
              +build | service=sample-service version=0.1
              +build | *cached* --> SAVE ARTIFACT environments +build/environments AS LOCAL environments
              output | --> exporting outputs
              output | [██████████] 100% exporting layers
              output | [██████████] 100% exporting manifest sha256:8a424cfa973897f8ec2defa2368a53932ff1bbf40801fd71e5eeedd2a35c9e64
              output | [██████████] 100% exporting config sha256:3dae0710a0b6810fca60d02196168439a594c1a745e223f0e8d7edabdb6dff60
              output | [██████████] 100% copying files
              output | [██████████] 100% pushing layers
              output | [██████████] 100% pushing manifest for docker.io/drayfocus/sample-service_node_app:0.1@sha256:8a424cfa973897f8ec2defa2368a53932ff1bbf40801fd71e5eeedd2a35c9e64
              output | [██████████] 100% transferring docker.io/drayfocus/sample-service_node_app:0.1

 3. Push ⏫
————————————————————————————————————————————————————————————————————————————————

Pushed image ./templates/nodejs/docker+node-app as drayfocus/sample-service_node_app:0.1

 4. Local Output 🎁
————————————————————————————————————————————————————————————————————————————————

Artifact +build/environments output as environments
Image ./templates/nodejs/docker+node-app output as drayfocus/sample-service_node_app:0.1

========================== 🌍 Earthly Build  ✅ SUCCESS ==========================

Share your logs with an Earthly account (experimental)! Register for one at https://ci.earthly.dev.

~~~
  
## Add Deploy Target

Now that your Docker image is complete, you must deploy your app to Kubernetes. That is taken care of by the target.

Return to the main project folder and include the `deploy` target in the main **Earthfile**.

This target's content will differ depending on your cloud service provider. However, the goal is to authenticate `kubectl` so that the kubernetes configurations in the "**environments**" folder can be deployed.

For example,
  
If you use digitalocean-

~~~{.dockerfile caption="Earthfile"}
deploy:
    FROM alpine/doctl:1.22.2
    # setup kubectl
    ARG env='dev'
    ARG DIGITALOCEAN_ACCESS_TOKEN=""
     
    COPY environments environments
      
    # doctl authenticating
    RUN doctl auth init --access-token ${DIGITALOCEAN_ACCESS_TOKEN}

    # save Kube config
    RUN doctl kubernetes cluster kubeconfig save cluster-name
    RUN kubectl config get-contexts


    ## deploy kubernetes configs
    RUN kubectl apply -f environments/${env}/namespace.yaml
    RUN kubectl apply -f environments/${env}
~~~

If you use AWS-
  
~~~{.dockerfile caption="Earthfile"}
deploy:
    FROM guitarrapc/docker-awscli-kubectl
    # setup kubectl
    ARG env='dev'
    ARG ACCESS_KEY_ID=""
    ARG SECRET_ACCESS_KEY=""
    ARG AWS_DEFAULT_REGION=""
     
    COPY environments environments

    # aws authenticating
    RUN aws configure set aws_access_key_id $ACCESS_KEY_ID
    RUN aws configure set aws_secret_access_key $SECRET_ACCESS_KEY
    RUN aws configure set default.region $AWS_DEFAULT_REGION

    # save Kube config
    RUN aws eks update-kubeconfig --region $AWS_DEFAULT_REGION \
    --name cluster-name

    ## deploy kubernetes configs
    RUN kubectl apply -f environments/${env}/namespace.yaml
    RUN kubectl apply -f environments/${env}
~~~

To test the "deploy" target:

Install the template.

~~~{.dockerfile caption="Earthfile"}
earthly +install --service=sample-service.
~~~

Change directory to "sample-service".

~~~{.dockerfile caption="Earthfile"}
cd sample_service.
~~~

Run the build target.

~~~{.dockerfile caption="Earthfile"}
earthly --push +build --service=sample-service --version=0.1.
~~~

Deploy to a specific environment e.g dev (using the digitalocean example)

~~~{.dockerfile caption="Earthfile"}
earthly +deploy --env=dev --DIGITALOCEAN_ACCESS_TOKEN={token}
~~~

<div class="wide">

![earthly +deploy]({{site.images}}{{page.slug}}/Swz2Xq6.png)\

</div>

## Add Auto-Deploy Target

This target doesn't do much. It simply combines the build and deploy targets, so they can be initiated together.

~~~{.dockerfile caption="Earthfile"}
auto-deploy:
    ARG version='0.1'
    ARG docker_registry='drayfocus'
    ARG service='sample'
    ARG env='dev'
    ARG DIGITALOCEAN_ACCESS_TOKEN=""
     
    # build and push docker images
    BUILD +build --version=$version –service=$service \
    --docker_registry=$docker_registry
      
    # Deploy to kubernetes
    BUILD +deploy --env=$env \
    --DIGITALOCEAN_ACCESS_TOKEN=$DIGITALOCEAN_ACCESS_TOKEN
~~~

## Testing Your Template

Bringing everything together. Your main **Earthfile** should look like this now,

~~~{.dockerfile caption="Earthfile"}
VERSION 0.6
FROM bash:4.4
WORKDIR /build-arena
IMPORT ./templates/kubernetes AS kubernetes_engine
IMPORT ./templates/docker AS docker_engine

install:
    ARG service='sample'
    ARG envs='dev,prod'
    ARG version='0.1'
    ARG docker_registry='drayfocus/earthly-sample' 

    WORKDIR /setup-arena
    
    FOR --sep="," env IN "$envs"    
        ENV dir="./$service/environments/$env"
        RUN echo "Creating environment $env"
        RUN mkdir -p $dir
        DO kubernetes_engine+DEPLOYMENT --service=$service \
        --env=$env --dir=$dir --version=$version \
        --docker_registry=$docker_registry
        DO kubernetes_engine+SERVICE --service=$service \
        --env=$env --dir=$dir
        DO kubernetes_engine+NAMESPACE --service=$service \
        --env=$env --dir=$dir
    END
    SAVE ARTIFACT $service AS LOCAL ${service}


build:
    ARG version='0.1'
    ARG docker_registry='drayfocus'
    ARG service='sample'
    ARG envs='dev,prod'
    ARG node_env="development"

    BUILD docker_engine+node-app --version=$version \
    --docker_registry=$docker_registry --service=$service \
    --node_env=$node_env

    ## Update deployment.yaml with latest versions
    FOR --sep="," env IN "$envs"    
        DO kubernetes_engine+DEPLOYMENT --service=$service \
        --env=$env --version=$version --docker_registry=$docker_registry
        SAVE ARTIFACT $service/environments/$env/* AS LOCAL \
        ${service}/environments/$env/
    END

# The content of this depends on the cloud service provider you use
deploy:
    FROM alpine/doctl:1.22.2
    # setup kubectl
    ARG env='dev'
    ARG DIGITALOCEAN_ACCESS_TOKEN=""

    COPY environments environments

    # doctl authenticating
    RUN doctl auth init --access-token ${DIGITALOCEAN_ACCESS_TOKEN}

    # save Kube config
    RUN doctl kubernetes cluster kubeconfig save cluster_name
    RUN kubectl config get-contexts

    ## deploy kubernetes configs
    RUN kubectl apply -f environments/${env}/namespace.yaml
    RUN kubectl apply -f environments/${env}

auto-deploy:
    ARG version='0.1'
    ARG docker_registry='drayfocus'
    ARG service='sample'
    ARG env='dev'
    ARG DIGITALOCEAN_ACCESS_TOKEN=""

    # build and push docker images
    BUILD +build --version=$version --service=$service \
    --docker_registry=$docker_registry

    # Deploy to kubernetes.

    BUILD +deploy --env=$env \
    --DIGITALOCEAN_ACCESS_TOKEN=$DIGITALOCEAN_ACCESS_TOKEN
~~~

You can delete the "**sample-service**" folder or any other folder that was generated during testing.

At this stage, project folder should contain an **Earthfile**, **version-update.sh** and **templates** folder.

Your template is now ready for use. Push the template to a git repository to make it available.

To generate a template for a new microservice, run

~~~{.dockerfile caption="Earthfile"}
earthly {template_git_url}+install --service=service_name
~~~

> `template git url` is the remote git URL of your template repository, for example. github.com/Doctordrayfocus/K8AutoSetup

You can then edit the source code repository in the docker's **Earthfile** with the service's source code repository.

To build and deploy the microservice, run this in the project folder ( and also add it to your CI/CD pipeline)

~~~{.dockerfile caption="Earthfile"}
earthly --push +auto-deploy –-service={service} \
--env={env} –-version={version} \
–-DIGITALOCEAN_ACCESS_TOKEN={DIGITALOCEAN_ACCESS_TOKEN}
~~~

That's it! You have successfully automated your microservices setup and deployment. You can also check out the final project on [github](https://github.com/Doctordrayfocus/K8AutoSetup).

## Conclusion

In this article, you have learned what kubernetes and microservices are, and also why it is necessary to automate your microservice setup(configuration and deployment) in kubernetes. You were introduced to Earthly(Earthly is a [CI/CD](/blog/ci-vs-cd) framework that helps you Develop CI/CD pipelines locally and run them anywhere.) Finally, you learned the steps involved in automating your microservice setup.

{% include_html cta/bottom-cta.html %}
