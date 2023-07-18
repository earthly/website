---
title: "Apply Mutual TLS Over a Kubernetes Nginx Ingress Controller"
categories:
  - Tutorials
toc: true
author: Muhammad Badawy
editor: Bala Priya C

internal-links:
 - Kubernetes
 - Nginx
 - Ingress
 - Transport Layer Security
excerpt: |
    Learn how to apply mutual TLS (Transport Layer Security) over a Kubernetes Nginx Ingress Controller to enhance the security of your communication sessions. This article explains the differences between TLS and mTLS, and provides a step-by-step guide on how to implement mutual TLS authentication in a Kubernetes environment.
---
**Busy with Kubernetes? [Earthly](https://earthly.dev/) can help. We make building apps faster using containerization. [Check us out](/), it could make things smoother for you.**

## The Problem That Mutual TLS Solves

Mutual TLS (Transport Layer Security) concept lies under the umbrella of **Zero Trust Policy** where strict identity verification is required for any client, person, or device trying to access resources in a private network.

Mutual TLS solves the problem of authenticating both the client and the server in a communication session. In traditional TLS, only the server is authenticated to the client, leaving the client vulnerable to [man-in-the-middle](https://en.wikipedia.org/wiki/Man-in-the-middle_attack) attacks.

Mutual TLS provides an additional layer of security by requiring the client to also present a digital certificate, which is verified by the server, ensuring that both parties in the communication are who they claim to be. This helps to prevent unauthorized access and protect against impersonation attacks.

In this article, you'll learn the differences between TLS and mTLS, and demystify how to apply both TLS and mTLS connections between a client and a Kubernetes endpoint exposed through an [Nginx](/blog/docker-slim) Ingress Controller.

## Differences Between TLS and MTLS

[Transport Layer Security (TLS)](https://www.cloudflare.com/learning/ssl/transport-layer-security-tls/) is a protocol used to secure communication over a computer network. It provides a secure channel between two devices communicating over the internet, or between a client and a server.

TLS uses a combination of [public key and TLS certificate](https://www.cloudflare.com/learning/ssl/what-is-ssl/) encryption to secure the transmission of data. In a TLS connection, the client and server exchange messages to negotiate a set of [encryption](/blog/encrypting-data-with-ssh-keys-and-golang) keys that will be used to secure the connection. Once the keys have been negotiated, the client and server use them to encrypt and decrypt the data transmitted between them. TLS certificates can be named as SSL certificates and this is because [TLS is an evolved version of SSL (Secure Sockets Layer)](https://www.ssl.com/faqs/faq-what-is-ssl/).

Mutual TLS (mTLS) is an upgrade of TLS that requires both the client and the server to authenticate each other using digital certificates. In a mutual TLS connection, the client presents its own certificate to the server, and the server presents its own certificate to the client. This ensures that both the client and server are who they claim to be, providing an additional layer of security to the connection.

The diagram below shows what we'll implement in the next steps. We'll start by deploying an Nginx [Ingress](/blog/building-on-kubernetes-ingress) Controller, then deploy a simple HTTP application and expose it. We'll then apply routing rules through a Kubernetes ingress resource. After that we'll learn how to apply TLS and mutual TLS connections between the client and a Kubernetes endpoint.

<div class="wide">
![Kubernetes deployments diagram]({{site.images}}{{page.slug}}/ptpr1xB.png)
</div>

Let's get started!

## Deploying Nginx Ingress Controller to a Kubernetes cluster

Nginx Ingress Controller is used to handle external traffic to a Kubernetes [cluster](/blog/kube-bench). It provides [load balancing, SSL termination, and name-based virtual hosting](https://docs.nginx.com/nginx-ingress-controller/intro/overview/), among other features. Deploying an Nginx Ingress Controller to a Kubernetes cluster allows for easier and more efficient management of external traffic to the cluster and its services. Additionally, it can improve the scalability of the cluster.

To proceed, you should have the following prerequisites:

- Up and running Kubernetes cluster. You can use [minikube](https://minikube.sigs.k8s.io/docs/start/) or [kind](https://kind.sigs.k8s.io/docs/user/quick-start/) to start one in a local environment.
- Local installations of Kubectl and openssl

Usually you need to check the Nginx Ingress official website to verify the installation steps according to your Kubernetes environment. You can check the [README](https://github.com/kubernetes/ingress-nginx/blob/main/README.md#readme) file and also the [Getting Started](https://kubernetes.github.io/ingress-nginx/deploy/) document related to the [Nginx](/blog/docker-slim) Ingress Controller.

For this demo, I'm using minikube as my Kubernetes cluster environment, so Nginx Ingress Controller can be enabled as below:

~~~{.bash caption=">_"}
$ minikube addons enable ingress
~~~

The pods related to Nginx Ingress Controller are deployed in ingress-nginx namespace. Now let's do a pre-flight check to make sure these pods are up and running before proceeding with next steps:

~~~{.bash caption=">_"}
$ kubectl get pods -n ingress-nginx
~~~

The image below shows the Nginx Ingress Controller pods running in `ingress-nginx` namespace as expected, and we can proceed with the following.

<div class="wide">
![Pre-flight check]({{site.images}}{{page.slug}}/dD0bZEn.png)
</div>

## Deploying and Exposing an HTTP Application

After making sure that all pods in the `ingress-nginx` namespace are up and running, let's deploy an HTTP application through [Kubernetes deployment](https://kubernetes.io/docs/concepts/workloads/Controllers/deployment/) to act as a backend service as below:

~~~{.bash caption=">_"}
$ kubectl create deployment demo-app --image=httpd --port=80
~~~

Then expose this [deployment](/blog/deployment-strategies) locally through a service of [type ClusterIP](https://kubernetes.io/docs/concepts/services-networking/service/). The [Kubernetes service](https://earthly.dev/blog/dev-guideto-k8services/) resource is used to expose a deployment of an application either locally within the cluster or externally outside the cluster. It creates a stable endpoint for clients to access the applications running in the pods. It acts as a load balancer as it is designed to circulate the traffic to the set of pods running the application.

In our demo, we choose to expose the deployment locally within the cluster through a Kubernetes service of type ClusterIP and externally through the Nginx Ingress Controller.

ClusterIP is a type of Kubernetes service which exposes an application within the cluster. It provides load balancing and high availability, so the traffic coming from outside (internet) to the application will hit the external endpoint exposed by Nginx Ingress Controller, which then redirects the traffic to one of the nodes within the cluster. The traffic will be redirected to one of the pods through the service. This enables load balancing and service discovery within the cluster. More details will be provided in the next steps.

~~~{.bash caption=">_"}
$ kubectl expose deployment demo-app
~~~

The above command will create a service named `demo-app`. You need to expose this Kubernetes service to be accessible from outside the cluster. This can be done through a [Kubernetes ingress resource](https://kubernetes.io/docs/concepts/services-networking/ingress/) which will use Nginx as Ingress class and will be hosted through test.localdev.me which is our localhost DNS.

~~~{.bash caption=">_"}
$ kubectl create ingress test-localhost --class=nginx \
--rule="test.localdev.me/*=demo-app:80"
~~~

So "test.localdev.me" will be our external gate to access the applications running in the Kubernetes cluster. When we `curl` "test.localdev.me" from the internet, the Nginx Ingress Controller will route the traffic to the "demo-app" service inside the cluster which will redirect the traffic to one of the application pods to serve it.

<div class="notice--info">
The entire wildcard domain entries of *.localdev.me points to 127.0.0.1 and this can be tested by executing the following command: `nslookup test.localdev.me`.
</div>

Next, let's test the connection to our endpoint application from outside the cluster, which will be made through [port-forward technique](https://kubernetes.io/docs/tasks/access-application-cluster/port-forward-access-application-cluster/) from our local machine on port 8080 to the Ingress Controller service on port 80 in the `ingress-nginx` namespace:

~~~{.bash caption=">_"}
$ kubectl port-forward -n ingress-nginx \
service/ingress-nginx-controller 8080:80
~~~

Leave the above command running in the terminal and from another terminal, let's try to curl the local endpoint:

~~~{.bash caption=">_"}
$ curl http://test.localdev.me:8080
~~~

The response should be as shown below. This means that you are able to connect to the Kubernetes endpoint through the Nginx Ingress Controller but with an HTTP connection that is not secure.

~~~{ caption="Output"}
<html><body><h1>It works!</h1></body></html>
~~~

Our goal in the next section is to secure this call, so we should be able to hit the URL "test.localdev.me" with the HTTPS protocol. This will require a TLS server certificate to be in place and configured in a proper way. So let's move to the next section.

## Enabling TLS Through Self-Signed Certificate

So far, we have deployed an Nginx Ingress Controller and HTTP application to Kubernetes, exposed this application to the outside world through an ingress resource and were able to successfully access the application from outside the cluster through a HTTP connection that's not secure.

In this section, we will focus on the steps needed to generate a server TLS certificate which will be used to validate the request through the client-server connection.
When a user/client navigates through a server/app/website that uses TLS, the connection is established through **TLS handshake**. It starts with a client sending a message to the server asking to set up an encrypted session. Then the server responds with a public key and TLS certificate.

The client verifies the certificate and uses the public key to generate a new pre-master key, then sends it to the server. The server decrypts the pre-master key using a private key. Finally client and server use the pre-master key to issue a shared secret which will be used to encrypt the messages.

<div class="wide">
![TLS connection diagram]({{site.images}}{{page.slug}}/mTZ9rWM.png)
</div>

Now you need to generate a self-signed server certificate for domain "test.localdev.me". By creating a server certificate for a specific domain, the client can verify that it is communicating with the intended server and not an imposter, thus providing security and trust to the client that it is communicating with the right server.`openssl` command will be used here to generate a self-signed server certificate as below:

~~~{.bash caption=">_"}
$ openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
-keyout server.key -out server.crt -subj \
"/CN=test.localdev.me/O=test.localdev.me"
~~~

At this point, we have a server certificate "server.crt" which needs to be defined to the Kubernetes cluster through a Kubernetes secret resource. The following command will create a secret named "self-tls" that holds the server certificate and the private key:

~~~{.bash caption=">_"}
$ kubectl create secret tls self-tls --key server.key --cert server.crt
~~~

The Ingress Controller needs to be modified to add a tls section to refer to the created secret which holds the server certificate.

~~~{.bash caption=">_"}
$ kubectl edit ingress test-localhost
~~~

The above command will open a `vi` session to modify the ingress resource. You can refer to the YAML below to add the "tls:" section which will link the secret we just created "self-tls" to the hostname "test.localdev.me". So it is expected when a client hits this hostname with HTTPS protocol, "self-tls" server certificate will be provided to the client to be verified. After verification, the request will be redirected to inside the cluster and a secure session will be initiated.

This YAML is the declarative representation of the ingress resource "test-localhost" that has been created in previous steps. It contains the needed rule to route the external traffic coming through "test.localdev.me" to the target service "demo-app".

~~~{.yaml caption=""}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: test-localhost
  namespace: default
spec:
  ingressClassName: nginx
  rules:
  - host: test.localdev.me
    http:
      paths:
      - backend:
          service:
            name: demo-app
            port:
              number: 80
        path: /
        pathType: Prefix
  tls:
  - hosts:
    - test.localdev.me
    secretName: self-tls
~~~

Now we want to hit the hostname (test.localdev.me) on port 443 to test the HTTPS connection through the port-forward technique. The below command will forward traffic from port 443 on the local machine to the Nginx Ingress Controller service running on port 443 inside the namespace `ingress-nginx`.

~~~{.bash caption=">_"}
$ sudo kubectl port-forward -n ingress-nginx \
service/ingress-nginx-controller 443:443
~~~

<div class="notice--info">
`sudo` is required here to allow incoming traffic on port 443.
Also keep that command running in a separate session as port-forwarding will be used for the rest of the article.
</div>

From another terminal, let's try to curl the local endpoint with HTTPS protocol:

~~~{.bash caption=">_"}
$ curl -k -v https://test.localdev.me/
~~~

 `-k` is used to skip self-signed certificate verification and `-v` to see some logs.

You can see through the logs that only one certificate has been verified which is the server certificate.
![TLS handshake]({{site.images}}{{page.slug}}/Xj3eaz8.png)

Now we have a successful TLS connection which enables server certificate validation. Next, we will enable the mutual TLS to also validate the client identity.

## Enabling Mutual TLS Through Self-Signed Certificate

In this section, we will add an extra layer of security which is client certificate validation. This helps to ensure that only authorized clients are able to establish a secure connection with the server, and can prevent unauthorized access to sensitive information. So we will create a CA [(Certificate Authority)](https://www.ssl.com/faqs/what-is-a-certificate-authority/) as our verification gate, and also a client's certificate and key which are the trusted identity of the client.

<div class="wide">
![Mutual TLS connection diagram]({{site.images}}{{page.slug}}/7FExOTX.png)
</div>

First let's create a CA. The main purpose of a CA is to affirm the identity of the certificate holder so that the recipient of the certificate can trust that the certificate was issued by a reputable and trustworthy entity.

~~~{.bash caption=">_"}
$ openssl req -x509 -sha256 -newkey rsa:4096 -keyout ca.key \
-out ca.crt -days 356 -nodes -subj '/CN=My Cert Authority'
~~~

Now you have the CA created "ca.crt" and we want to define it to the Kubernetes cluster through a Kubernetes resource. And again, we'll define it as a Kubernetes secret.
Run the following command to create a secret named ca-secret of type generic to hold the "ca.crt file"

~~~{.bash caption=">_"}
$ kubectl create secret generic ca-secret --from-file=ca.crt=ca.crt
~~~

Next we need to generate a [Certificate Signing Request](https://en.wikipedia.org/wiki/Certificate_signing_request) (CSR) and client key. CSR is a request for a certificate that contains information about the certificate holder. It will be submitted to the CA with the client key to generate the client certificate.
The output of the following command is a client CSR "client.csr" and a client key "client.key".

~~~{.bash caption=">_"}
$ openssl req -new -newkey rsa:4096 -keyout client.key \
-out client.csr -nodes -subj '/CN=My Client'
~~~

Now we need to sign this CSR with the CA to generate the client certificate which can be done via the below command.

~~~{.bash caption=">_"}
$ openssl x509 -req -sha256 -days 365 -in client.csr \
-CA ca.crt -CAkey ca.key -set_serial 02 -out client.crt
~~~

At this point, we have a client key "client.key" and client certificate "client.crt" which will be used when communicating with the server through mutual TLS connection.

Again the ingress resource needs to be modified to add [client verification annotations](https://github.com/kubernetes/ingress-nginx/blob/main/docs/user-guide/nginx-configuration/annotations.md). One of these annotations "nginx.ingress.kubernetes.io/auth-tls-secret" is to refer to the CA secret "default/ca-secret" which will verify the identity of the clients requesting to communicate with the server. Another one "nginx.ingress.kubernetes.io/auth-tls-verify-client" is to enable verifying the client certificate.

~~~{.bash caption=">_"}
$ kubectl edit ingress test-localhost
~~~

Below are the 4 annotations that need to be added to ingress resource to allow client TLS verification.

~~~{.yaml caption=""}
metadata:
  annotations:
    nginx.ingress.kubernetes.io/auth-tls-pass-certificate-to-upstream: \
    "true"
    nginx.ingress.kubernetes.io/auth-tls-secret: default/ca-secret
    nginx.ingress.kubernetes.io/auth-tls-verify-client: "on"
    nginx.ingress.kubernetes.io/auth-tls-verify-depth: "1"
~~~

## Validating the Mutual TLS Scenario

Now if you try to curl the Kubernetes exposed endpoint without providing the client cert, you should get an error mentioning that no SSL certificate provided, which means that annotations in the previous step are working correctly.

~~~{.bash caption=">_"}
$ curl -k https://test.localdev.me
~~~

As you see, the error appears as expected because no client SSL certificate was provided during the call.

<div class="wide">
![400 Error]({{site.images}}{{page.slug}}/iPruOBz.png)
</div>

Try the same call by providing a client key and a certificate and use '-v' to get more logs:

~~~{.bash caption=">_"}
$ curl -k -v https://test.localdev.me/ --key client.key \
--cert client.crt
~~~

As you can see in the output of the command that certificate verification "CERT verify" has been made twice, **one for server certificate** and another one for the **client certificate** then the call works as expected. Both client and server identities are verified and trusted for a mutual secure connection.

<div class="wide">
![Mutual TLS Handshake]({{site.images}}{{page.slug}}/E9FDfel.png)
</div>

You can find the complete ingress file on [GitHub](https://github.com/Badawekoo/devops/blob/main/kubernetes/ingress/nginx-ingress-Controller.yaml).

## Notes on Applying Mutual TLS in Production Environment

These notes are to be taken into consideration when you try the mutual TLS implementation in a Kubernetes production environment:

- Nginx Ingress Controller will be installed according to your Kubernetes production environment. You can check this [installation guide](https://kubernetes.github.io/ingress-nginx/deploy/) for more context.
- Once you have the Ingress Controller installed, you need to configure a DNS record of type A for your domain name to point to the public IP of the Ingress Controller.
- Server certificate and CA certificate should be issued from a trusted certificate provider and you just need to apply them into Kubernetes as secrets.

## Conclusion
<!--sgpt-->
Mutual TLS offers comprehensive security for client-server communication, ensuring both parties are verified. We've explored the distinctions between TLS and mTLS, and illustrated how to secure Kubernetes Nginx Ingress Controller endpoints. 

Once you've secured your Kubernetes environment, you might want to streamline your build process. Consider exploring [Earthly](https://www.earthly.dev/), your next favorite build automation tool, to make this process more efficient and reliable.

For further learning, dive into Kubernetes' other security aspects like Security Context in Kubernetes and Kubernetes Compliance Scan.

{% include_html cta/bottom-cta.html %}