---
title: "Deployment Strategies in Kubernetes"
categories:
  - Tutorials
toc: true
author: Muhammad Badawy

internal-links:
 - deployment strategies
 - strategies for deployment in kubernetes
 - deployment in kubernetes
 - how to do deployment in kubernetes
excerpt: |
    This article discusses different deployment strategies in Kubernetes, including rolling deployment, blue-green deployment, recreate deployment, and canary deployment. It explains how to implement each strategy and highlights their advantages and disadvantages.
last_modified_at: 2023-10-06
---
**This article explains Kubernetes deployment strategies. Earthly simplifies build processes for containerized applications, improving Kubernetes deployments. [Check it out](/).**

Kubernetes is a container orchestration platform that helps you deploy, manage, and scale containerized applications. One of the key features of Kubernetes is its ability to choose between different deployment strategies. With the right strategy you can easily roll out new versions of your application based on business needs and application requirements.

Each strategy has its own advantages and disadvantages. So how do you choose the right one? In this article, we will discuss the different deployment strategies available in Kubernetes and the pros and cons for each deployment. We will also provide examples of how to implement each strategy.

## Deployment Strategies in Kubernetes

![Strategies]({{site.images}}{{page.slug}}/strategy.png)\

In Kubernetes, a deployment strategy is an approach to managing the rollout and updates of applications in a cluster. It defines how changes to the application are applied, ensuring a smooth transition with minimal disruption to the application's availability.

Kubernetes provides various deployment strategies, each designed to meet different requirements and scenarios.

### Prerequisites

* Basic understanding of Kubernetes and [its Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/).
* Basic understanding of [Kubernetes services](https://kubernetes.io/docs/concepts/services-networking/service/)
* Kubernetes environment up and running.
* [Kubectl](https://kubernetes.io/docs/tasks/tools/) installation.

## Rolling Deployment in Kubernetes

A rolling deployment is the default deployment strategy in Kubernetes. It updates your application gradually, one pod at a time. This means that there is no downtime during the deployment, as the old pods are still running while the new pods are being created.

This type of Kubernetes deployment comes `out of the box`. Kubernetes provides a feature called `Deployment` to manage rolling updates. Here's how it's implemented:

Step 1: Create a Deployment
To begin, you define a Kubernetes Deployment manifest (usually in a YAML file) that describes your application and its desired state, including the container image, replicas, and other configuration options. For example:

~~~{.yml caption="deployment.yaml"}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app-container
        image: your-registry/your-app-image:latest
        ports:
        - containerPort: 80
~~~

Here you need to update the container registry and image with proper values.

Step 2: Apply the Deployment
Use the `kubectl apply` command to create or update the Deployment:

~~~{.bash caption=">_"}
kubectl apply -f deployment.yaml
~~~

Step 3: Monitor the Deployment
You can monitor the progress of the rolling update using the `kubectl rollout status` command:

~~~{.bash caption=">_"}
kubectl rollout status deployment my-app-deployment
~~~

Step 4: Perform the Rolling Update
To perform the rolling update, you can update the image version in the Deployment manifest to the new version. For example, change the image tag from `latest` to a specific version:

~~~{.yml caption="deployment.yaml"}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-deployment
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1  
      # Maximum number of pods that can be created beyond the desired count
      maxUnavailable: 1  
      # Maximum number of pods that can be unavailable at a time
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app-container
        image: your-registry/your-app-image:v2.0.0
        ports:
        - containerPort: 80
~~~

Step 5: Apply the Update
Apply the updated Deployment manifest to trigger the rolling update:

~~~{.bash caption=">_"}
kubectl apply -f deployment.yaml
~~~

Step 6: Monitor the Rolling Update
Monitor the rolling update's progress using the same `kubectl rollout status` command as before:

~~~{.bash caption=">_"}
kubectl rollout status deployment my-app-deployment
~~~

Kubernetes will now gradually update the pods in the Deployment by terminating the old instances and creating new ones with the updated image. The rolling update will be controlled to maintain the specified number of replicas during the process, ensuring the application remains available.

### Advantages and Disadvantages of Rolling Deployment

Advantages of rolling deployments:

* No downtime
* Easy to implement
* Can be used with any type of application

Disadvantages of rolling deployments:

* Can be slow, especially if you have a large number of pods
* Can be difficult to troubleshoot if there are problems with the new version of the application

## Blue-Green Deployment in Kubernetes

A blue-green deployment is a more advanced deployment strategy that can be used to minimize downtime. In a blue-green deployment, you have two identical deployments of your application: one in production (the "blue" deployment) and one in staging (the "green" deployment).

When you are ready to deploy a new version of your application, you first deploy it to the green deployment. Once the green deployment is up and running, you then switch traffic from the blue deployment to the green deployment.

Kubernetes makes it relatively straightforward to implement blue-green deployment using its native features like `Services` and `Deployments`. Here's how you can do it:

### Step 1: Create Blue and Green Deployments

Create two separate Deployment manifests - one for the current live version (blue) and another for the new version (green). Both deployments should have the same labels, so they can be accessed through the same Service. For example:

~~~{.yml caption="blue-deployment.yaml"}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
      version: blue
  template:
    metadata:
      labels:
        app: my-app
        version: blue
    spec:
      containers:
      - name: my-app-container
        image: your-registry/your-app-image:1.0.0
        ports:
        - containerPort: 80
~~~

~~~{.yml caption="green-deployment.yaml"}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
      version: green
  template:
    metadata:
      labels:
        app: my-app
        version: green
    spec:
      containers:
      - name: my-app-container
        image: your-registry/your-app-image:2.0.0
        ports:
        - containerPort: 80
~~~

Notice here the green deployment has different `version` label and different image tag.

### Step 2: Create a Service

Next, you need to create a Service that will serve as the entry point for accessing your application. This Service will route traffic to the current live version (blue). The selector in the Service should match the labels of the blue Deployment. For example:

~~~{.yml caption="blue-deployment.yaml"}
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  selector:
    app: my-app
    version: blue
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
~~~

### Step 3: Deploy Blue Version

Apply the blue Deployment and the Service to deploy the current live version:

~~~{.bash caption=">_"}
kubectl apply -f blue-deployment.yaml
kubectl apply -f service.yaml
~~~

### Step 4: Test Blue Version

Verify that the blue version is working correctly and serving traffic as expected.

~~~{.bash caption=">_"}
kubectl get deployment
kubectl get service
~~~

Further steps can be done from your side to verify traffic flow from service resource to deployment resource to the running pod.

### Step 5: Deploy Green Version

Apply the green Deployment to deploy the new version:

~~~{.bash caption=">_"}
kubectl apply -f green-deployment.yaml
~~~

### Step 6: Switch Traffic to Green Version

Update the Service's selector to match the labels of the green Deployment:

~~~{.bash caption=">_"}
kubectl patch service my-app-service -p \
'{"spec":{"selector":{"version":"green"}}}'
~~~

Now, the Service will route traffic to the green deployment, making the new version live (green), while the blue environment remains available.

### Step 7: Test Green Version

Verify that the green version is working correctly and serving traffic as expected.

At this point, you have completed the blue-green deployment. If any issues arise with the green version, you can quickly switch back to the blue version by updating the Service's selector to match the labels of the blue Deployment again.

Note: It's essential to monitor the deployment and perform appropriate testing before switching traffic from blue to green and vice versa.

## Advantages and Disadvantages of Blue-Green Deployment

Advantages of blue-green deployments:

* Very little downtime
* Easy to troubleshoot
* Can be used with any type of application

Disadvantages of blue-green deployments:

* Requires more resources than a rolling deployment
* Can be more complex to implement if you have large amount of dependant applications

## Recreate Deployment

A Recreate Deployment can lead to a temporary downtime during the update process, as all old instances of your application are completely replaced with the new version. Here's how you can implement the "Recreate" deployment strategy in Kubernetes:

### Step 1: Create a Deployment Manifest

Create a Deployment manifest YAML file that describes your application and its desired state. This manifest should include the specifications for both the old version `v1` and the new version `new-version` of your application. Here's a basic example:

~~~{.yml caption="deployment.yaml"}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-deployment
spec:
  replicas: 3  # Number of replicas for the new version
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app-container
        image: your-registry/your-app-image:v1
        ports:
        - containerPort: 80
~~~

### Step 2: Apply the Deployment

Apply the Deployment manifest using the `kubectl apply` command:

~~~{.bash caption=">_"}
kubectl apply -f deployment.yaml
~~~

### Step 3: Monitor the Rollout

Monitor the progress of the rollout using the `kubectl rollout status` command:

~~~{.bash caption=">_"}
kubectl rollout status deployment my-app-deployment
~~~

### Step 4: Update the Deployment with Recreate Strategy

To implement the "Recreate" strategy, you need to update the Deployment with the new version image and apply the changes. Kubernetes will automatically manage the recreation of pods.

Edit the Deployment manifest to update the image to the new version and specify the deployment strategy:

~~~{.yml caption="deployment.yaml"}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-deployment
spec:
  replicas: 3  # Number of replicas for the new version
  strategy:
    type: Recreate  ## K8s deployment strategy
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app-container
        image: your-registry/your-app-image:new-version  
        # Updated image version
        ports:
        - containerPort: 80
~~~

Apply the changes:

~~~{.bash caption=">_"}
kubectl apply -f deployment.yaml
~~~

### Step 5: Monitor the Rollout Again

Monitor the progress of the rollout as Kubernetes terminates the old pods and creates new pods with the updated configuration.

Keep in mind that the "Recreate" strategy can result in a brief downtime during the update process since all instances of the old version are stopped before the new version is fully deployed. Therefore, it's essential to plan updates during maintenance windows or use strategies like a rolling deployment if downtime is a concern for your application's availability.

## Advantages and Disadvantages of Recreate Deployment

Advantages of `recreate` deployments:

* Simple to implement
* Can be used with any type of application

Disadvantages of `recreate` deployments:

* Can cause downtime
* Can be difficult to troubleshoot if there are problems with the new version of the application

## Canary Deployment

A canary deployment is a deployment strategy that gradually introduces a new version of your application to your users. In a canary deployment, you start by deploying a small number of pods with the new version of your application. These pods are then monitored to see how they perform. If the new version of the application is performing well, you then gradually increase the number of pods with the new version.

Kubernetes provides native features like Services and Deployments to implement canary deployments. Here's how you can do it:

### Step 1: Create Stable Deployment

Create another Deployment manifest for your stable version of the application. This will be the stable Deployment. It should have the same number of replicas as your full desired number of instances. For example:

~~~{.yml caption="stable-deployment.yaml"}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-stable
spec:
  replicas: 8  
  # Set the full desired number of replicas for the stable Deployment
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app-container
        image: your-registry/your-app-image:1.0.0  
        # Current stable version image
        ports:
        - containerPort: 80
~~~

### Step 2: Create a Service

Create a Service that will be used as the entry point for accessing your application. This Service should be a "LoadBalancer" or a "NodePort" type, depending on your infrastructure setup. It will route traffic to the stable Deployment. For example:

~~~{.yml caption="service.yaml"}
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  selector:
    app: my-app
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: LoadBalancer  # or NodePort
~~~

Apply the stable deployment and the service then monitor the sable Deployment to ensure that it is functioning correctly and serving traffic as expected.

~~~{.bash caption=">_"}
kubectl apply -f stable-deployment.yaml
kubectl apply -f service.yaml
~~~

### Step 3: Create Canary Deployment

Create a Deployment manifest for the new version of your application. This will be the canary Deployment. You can set the number of replicas for this Deployment to a small percentage of your overall desired number of instances. For example:

~~~{.yml caption="canary-deployment.yaml"}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-canary
spec:
  replicas: 2  
  # Set a small number of replicas for the canary Deployment
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app-container
        image: your-registry/your-app-image:2.0.0  
        # New version image
        ports:
        - containerPort: 80
~~~

### Step 4: Apply and Test Canary Deployment

Apply the canary Deployment and monitor to ensure that it is functioning correctly and serving traffic as expected. Perform appropriate testing to validate the new version.

~~~{.bash caption=">_"}
kubectl apply -f canary-deployment.yaml
~~~

### Step 5: Gradually Increase Traffic to Canary

Update the Service configuration to gradually route more traffic to the canary Deployment. You can use Kubernetes' weight property for this:

~~~{.bash caption=">_"}
kubectl patch svc my-app-service -p '{"spec":{"ports":\
[{"port":80,"targetPort":80,"protocol":"TCP","name":"http",\
"nodePort":null,"port":80,"targetPort":80,"protocol":"TCP",\
"name":"http","nodePort":null,"weight":20}]}}'
~~~

In this example, the weight of the canary Deployment is set to 20, which means it will receive 20% of the incoming traffic.

### Step 6: Monitor Canary Deployment

Keep monitoring the canary Deployment to ensure there are no issues as it receives more traffic.

### Step 7: Gradually Increase Traffic to Canary

If everything looks good, continue increasing the traffic to the canary Deployment by updating the Service's weight accordingly.

### Step 8: Complete the Deployment

Once you are confident that the canary Deployment is stable and performs well, update the Service configuration to direct all traffic to the canary Deployment:

~~~{.bash caption=">_"}
kubectl patch svc my-app-service -p '{"spec":{"ports":\
[{"port":80,"targetPort":80,"protocol":"TCP","name":"http",\
"nodePort":null,"port":80,"targetPort":80,"protocol":"TCP",\
"name":"http","nodePort":null,"weight":100}]}}'
~~~

The canary Deployment will now receive 100% of the incoming traffic, and the stable Deployment can be safely scaled down or removed.

By following these steps, you can implement a canary deployment strategy in Kubernetes to test and gradually roll out new versions of your application while minimizing the risk of introducing issues to all users.

## Advantages and Disadvantages of Canary Deployment

Advantages of canary deployments:

* Can be used to test new versions of your application with real users
* Can help you to identify problems with the new version of the application early on
* Can be used to gradually roll out a new version of your application to your users

Disadvantages of canary deployments:

* Can be more complex to implement than a rolling deployment
* Requires more resources than a rolling deployment

## Conclusion

The choice of deployment strategy depends on factors like the desired update speed, tolerance for downtime, risk tolerance, and the need for testing new versions before full rollout. Each strategy has its advantages and limitations, so it's essential to select the one that best suits your application and business requirements.

If you need to minimize downtime and deploy different versions at the same time, then a blue-green deployment or a canary deployment may be a good choice. If you need a simple and easy-to-implement deployment strategy, then a rolling deployment may be a better option.

{% include_html cta/bottom-cta.html %}