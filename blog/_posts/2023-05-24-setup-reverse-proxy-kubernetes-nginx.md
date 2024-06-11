---
title: "How to Set Up a Reverse Proxy in Kubernetes"
toc: false
author: Somtochukwu Uchegbu
editor: Mustapha Ahmad Ayodeji

internal-links:
 - Reverse Proxy
 - Kubernetes
 - Performance
 - Flask
excerpt: |
    Learn how to set up a reverse proxy in Kubernetes with Nginx and improve the performance and reliability of your application. This tutorial covers configuring the Nginx server, creating a Kubernetes deployment, and setting up a service to expose the deployment to the outside world.
last_modified_at: 2023-07-19
categories:
  - orchestration
---
**This article explains how to set up a Kubernetes Nginx reverse proxy. Earthly improves Docker image creation for Kubernetes by enhancing build performance. [Learn more about Earthly](https://cloud.earthly.dev/login).**

Setting up a reverse proxy in kubernetes can seem a bit overwhelming if it is your first time coming across them. However, it can greatly improve the performance and reliability of your application.

In this article, I will walk you through the steps to set up a reverse proxy in Kubernetes. We will cover how to configure the Nginx server, create a Kubernetes deployment, and set up a service to expose the deployment to the outside world.

To follow this tutorial, you will have to meet these requirements:

- You have a working knowledge of Kubernetes and Docker.
- You have [Minikube](https://minikube.sigs.k8s.io/docs/start/) installed.
- You have [Kubectl](https://kubernetes.io/docs/tasks/tools/) installed.
- You have [Docker](https://docs.docker.com/engine/install/) installed.

## What Are Reverse Proxies?

<div class="wide">
![Image of a Reverse Proxy, source-[Upguard](https://www.upguard.com/blog/what-is-a-reverse-proxy)]({{site.images}}{{page.slug}}/ck0oA2V.png)
</div>

A Reverse proxy is any piece of software or a server that intercepts the incoming request from a client to a server. They are basically used as middlemen between a client and a server.

Reverse proxies, in some cases, secure the server from a client by first inspecting the request from the client for potential security threats before forwarding the request to the server.

Some examples of reverse proxy servers include [Nginx](https://www.nginx.com/), [Apache](https://httpd.apache.org/), [Treafik](https://traefik.io/), [HashiCorp Consul](https://www.consul.io/), etc.

### Uses of Reverse Proxies

Reverse proxies has diverse areas of applications. Here are some of the uses of reverse proxies.

- **Protocol Translation**: They can be used to translate one protocol to another. This way, requests with different protocols e.g HTTPS from the client can be translated to a protocol HTTP the backend server can understand.

- **Caching**: They can be used for caching information for a faster response time. For instance, a reverse proxy may receive repeated requests for a resource from the client, causing it to forward the request to the main server each time, resulting in a delay. The reverse proxy can be used to cache this resource and serve it directly to the client without involving the main server, thereby reducing latency.

- **Load Balancing**: Reverse Proxies can serve as Load Balancers. This way they help to distribute incoming client requests to a connected network of servers at the backend. This is very useful because it reduced the load that one server handles. Different load-balancing algorithms can be configured on the reverse proxies o determine how incoming client requests are routed to other servers.

- **Security**: They can be used to secure your main server. Malicious attacks are thwarted because the reverse proxy's IP address is provided instead of the main server. All incoming requests are handled by the reverse proxy, preventing any malicious attempts from reaching the main server.

- **Site Blocking**: They can be used for restricting access to your main server. The reverse proxy achieves this by accepting all incoming requests and filtering them before passing them to the main server.

### Advantages of Using Reverse Proxies

There are some advantages that come with using Reverse Proxies, some of which include:

- Improved security
- Increased server performance
- Improved scalability
- Better protocol translation, etc.

## Setting Up a Reverse Proxy In Kubernetes

![Setup]({{site.images}}{{page.slug}}/setup.png)\

In this section, you will look at how to set up a reverse proxy server in a Kubernetes cluster. You will set up an Nginx reverse proxy server for a simple Flask application.

### Setting Up Your Flask Server

In this section, you will build a simple Flask server, create a Docker image from it and push the image to DockerHub.

Firstly, Create a virtual environment that will house the dependencies for your Flask server:

~~~{.bash caption=">_"}
virtualenv env
~~~

Next, Install the Flask web framework by running the following command:

~~~{.bash caption=">_"}
pip install flask
~~~

Create a simple python file called *server.py* and add this piece of code:

~~~{.python caption="server.py"}
from flask import Flask, jsonify
app = Flask(__name__)

@app.get("/")
def hello():
    return jsonify({"message": "Hello from Flask!!"}), 200
~~~

Generate a requirements.txt file for the dependencies:

~~~{.bash caption=">_"}
pip freeze > requirements.txt
~~~

Create a Dockerfile that you will use to create a Flask image.

Add the following Docker commands in the Dockerfile:

~~~{.dockerfile caption="Dockerfile"}
FROM python:3.10-alpine
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app/
EXPOSE 5000
CMD ["python3", "server.py"]
~~~

Build the Docker image:

~~~{.bash caption=">_"}
docker build -t <image-name>
~~~

Push the Docker image to DockerHub so that you can access it in your [Minikube](/blog/minikube) cluster:

~~~{.bash caption=">_"}
docker push <image-name> 
~~~

With the above steps, you are done with creating your flask server, creating a Docker image for your server, and pushing it to DockerHub, let's start configuring your reverse proxy.

### Setting Up Your Nginx Server

In this section, you will configure Nginx as a reverse proxy and build a Docker image for it.

Create a separate folder called **custom_niginx**.This folder will house your Dockerfile for the Nginx image, and custom Nginx configuration files.

Next, Create a new file called **nginx.conf** in the **custome_nginx** folder. This file will hold the custom configurations for your reverse proxy server.

Add this block of code to the **nginx.conf** file:

~~~{ caption="nginx.conf"}
events { }

http {

  server {
    listen 8080;

    location /flask {
      proxy_pass http://backend-svc:5000/;
    }
  }
}
~~~

In this new configuration file, you are basically telling your Nginx server to listen on port 8080, and send any requests that come into the server with the path **/flask** to the kubernetes flask service **<http://backend-svc:5000>** which you are going to set up in your kubernetes cluster.

Note: the name of the server that you add as the `proxy_pass` must correspond with the name of your kubernetes flask service.

Next, add the following block of code to your Dockerfile in the *custom_nginx* folder:

~~~{.dockerfile caption="Dockerfile"}
FROM nginx
COPY nginx.conf /etc/nginx/nginx.conf
~~~

The Dockerfile instructs docker to copy your new nginx configuration file and replace the default nginx configuration file with it.

Finally, Create, and push your Docker image to DockerHub.

### Deploying Your Flask Server to Minikube

Now, you need to deploy your Flask server to your [minikube](/blog/minikube) cluster.

Firstly, you will need to create a [deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) and [service](https://kubernetes.io/docs/concepts/services-networking/service/) manifest which you will apply to create a deployment and service for your Flask server.

You can do this by creating a deployment.yml and a service.yml files in the root directory.

In the deployment.yml file, add this block of code to it:

~~~{.yaml caption="deployment.yml"}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
spec:
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: your-flask-image
        resources:
          limits:
            memory: "128Mi"
            cpu: "200m"
        ports:
        - containerPort: 5000
~~~

> Note: replace **your-flask-image** placeholder with the name of the Docker image you pushed to DockerHub

In the deployment configuration above, you assigned port 5000 to the container with the  `containerPort` configuration key because that is the port you exposed in your Dockerfile.

Next, add this block of code to the service.yml file:

~~~{.yaml caption="service.yml"}
apiVersion: v1
kind: Service
metadata:
  name: backend-svc
spec:
  selector:
    app: backend
  type: ClusterIP
  ports:
  - port: 5000
    targetPort: 5000 
~~~

You created a service of type [ClusterIP](https://kubernetes.io/docs/concepts/services-networking/cluster-ip-allocation/) because you only want to expose your pods internally.

If you look closely, the name of this service is **backend-svc**, corresponding to the name of the server you added as the value for the `proxy_passs` in your Nginx configuration file.

Run the following commands to deploy both services:

~~~{.bash caption=">_"}
kubectl apply -f deployment.yml

kubectl apply -f service.yml
~~~

You can access your Flask server with [port forwarding](https://kubernetes.io/docs/tasks/access-application-cluster/port-forward-access-application-cluster/). Essentially, what port-forwarding does is that it allows you to access a port on the kubernetes cluster by creating a network tunnel between your local computer and the Kubernetes cluster, forwarding traffic from that port on the local machine to the assigned port on the Kubernetes Service. This allows you to access the backend application running in the Kubernetes cluster through your local machine.

You can check out your Flask with port forwarding as shown below:

~~~{.bash caption=">_"}
kubectl port-forward svc/backend-svc 5000:5000
~~~

Output:

~~~{ caption="Output"}
Forwarding from 127.0.0.1:5000 -> 5000
Forwarding from [::1]:5000 -> 5000
~~~

This forwards traffic from port 5000 on your local machine to port 5000 on the backend-svc Kubernetes Service.

Now when you visit localhost:5000 on your local machine, you should see your flask server up and running:

<div class="wide">
![Flask Homepage]({{site.images}}{{page.slug}}/iaQtJtX.png)
</div>

### Deploying Your Nginx Server to Minikube

Now that you are done with deploying your Flask server, let's do the same with your Nginx server.

The steps are similar to the ones you followed when deploying your Flask server.

Create your deployment.yml and service.yml manifest files for the Nginx server.

Add the following block of code in the deployment.yml file:

~~~{.yaml caption="deployment.yml"}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: reverse-proxy-depl
spec:
  selector:
    matchLabels:
      app: reverse-proxy-depl
  template:
    metadata:
      labels:
        app: reverse-proxy-depl
    spec:
      containers:
      - name: reverse-proxy-depl
        image: your-nginx-image
        resources:
          limits:
            memory: "128Mi"
            cpu: "200m"
        ports:
        - containerPort: 8080
~~~

As you can see you are assigning the `containerPort` the port 8080 which is the same port you instruct your nginx server to listen to in your nginx configuration file.

Next, add this block of code to the service.yml file:

~~~{.yaml caption="service.yml"}
apiVersion: v1
kind: Service
metadata:
  name: reverse-proxy-svc
spec:
  selector:
    app: reverse-proxy-depl
  type: ClusterIP
  ports:
  - port: 8080
    targetPort: 8080
~~~

Now, to test your reverse proxy server, map the Nginx port 8080 to the Kubernetes port 8080 with the port forwarding command.

Enter this command in your terminal:

~~~{.bash caption=">_"}
kubectl port-forward svc/reverse-proxy-svc 8080:8080
~~~

When you visit the home page of your Nginx server, you should get this 404 response page:

<div class="wide">
![Nginx 404 Page]({{site.images}}{{page.slug}}/Rzf3uc4.png)
</div>

You got the 404 error message because you did not define any rules for the home route in the Nginx configuration.

But when you visit the /flask route, you should see that your request is being handled by the flask server now:

<div class="wide">
![Reverse Proxy Flask Homepage]({{site.images}}{{page.slug}}/Hjz4Fl9.png)
</div>

## Conclusion

In this tutorial, we navigated through setting up a reverse proxy in Kubernetes using Nginx. We built a Flask server, configured Nginx, created Docker images for both, and deployed them to Kubernetes. You can find all the code on this [Github repository](https://github.com/somT-oss/flask-docker).

And if you're looking to further streamline your build processes, you might want to give [Earthly](https://cloud.earthly.dev/login) a try. It's a tool that simplifies build automation, making it a breeze to manage your builds.

{% include_html cta/bottom-cta.html %}
