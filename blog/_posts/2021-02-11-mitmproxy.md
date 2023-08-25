---
title: How to Man in the Middle HTTPS Using mitmproxy
categories:
  - Tutorials
toc: true
author: Adam
excerpt: |
    
internal-links:
   - mitmproxy
   - proxy
last_modified_at: 2023-04-17
topic: cli
---
**We're [Earthly.dev](https://earthly.dev/). We make building software simpler and therefore faster – like Dockerfile and Makefile had a baby. We wrote this article because we are big fans of MITMProxy and poking around in the network stack. [Check us out](https://earthly.dev/)!**

## Introduction

Have you ever wanted to see what kinds of requests a service or application on your machine is making and what kind of responses it is getting back? Have you ever tried and failed to capture this traffic or modify it to investigate how something works (or doesn't work). If you have, then mitmproxy might be what you need. Being able to scan through and observe HTTP protocol traffic easily is a great debugging aid.

This guide will walk you through installing and using mitmproxy to capture HTTPS requests. We will start with macOS traffic capture, then touch on Linux and Windows and then finally show how to capture docker daemon traffic and docker container traffic.  

## What Is mitmproxy?

mitmproxy is a command-line tool that acts as a HTTP and HTTPS proxy and records all the traffic. You can easily see what requests are being made and even replay them. It's great for diagnosing problems.

## Installing It

<div class="narrow-code">
On Mac, mitmproxy is easy to install with brew:

~~~{.bash caption=">_"}
> brew install mitmproxy
~~~

On Windows and Linux, [download the binary release](https://docs.mitmproxy.org/stable/overview-installation/) and place it somewhere in your path.

## #1 Start It Up

To start up mitmproxy, type `mitmproxy`, and it will start up bound to port 8080.

~~~{.bash caption=">_"}
> mitmproxy
~~~

</div>

The command-line interface (CLI) has VIM-like keybindings. `q` will quit, and arrow keys or `h`, `j`, `k`, `l` will move you up and down through the request list. `?` will load the help, and `<<enter>>` will drill in on a specific request.
{% include imgf src="1.png" alt="Help menu for mitmproxy" caption="Help Menu for mitmproxy" %}

mitmproxy also has a web interface if you prefer the mouse over VIM keybindings. The advanced functionality is a bit more discoverable in the web interface, but the CLI version is convenient for quick capture sessions.

{% include imgf src="2.png" alt="mitmproxy starting up" %}
{% include imgf src="3.png" alt="mitmweb starting up" %}

We will use both throughout the tutorial. Whichever you choose, start it up and leave it running.

## #2 Proxy Our Connection

Let's set up our internet connection to use this proxy. On macOS, Under `Setting -> Network`, choose your connection and select advanced.

{% include imgf src="4.png" alt="Setting -> Network on macOS" caption="`Setting -> Network` on macOS" %}

Under proxies, enable both HTTP and HTTPS proxies and choose port 8080:

{% include imgf src="5.png" alt="Setup Proxy under Setting -> Network-> Advanced on macOS" caption="Setup Proxy under `Setting -> Network-> Advanced` on macOS" %}

*On Windows, [follow these steps](https://www.howtogeek.com/tips/how-to-set-your-proxy-settings-in-windows-8.1/) to set up a proxy.*

*On Linux, MITM supports a [transparent proxying](https://docs.mitmproxy.org/stable/howto-transparent/) at the network layer.*

## Adding mitmproxy as A Certificate Authority

We now have our connection proxied to go through our instance of mitmproxy. However, if we attempt to make a HTTPS-based request in a web browser (loading twitter.com for example), something interesting happens.

{% include imgf src="6.png" alt="Chrome does not recognize the certificate" caption="Chrome does not recognize the certificate" %}

Chrome is warning us that we might be subject to a man in the middle attack.

### What Is a Man in the Middle?

A man in middle attack (MITM) is a security threat where an attacker can get between incoming and outgoing requests. You think you are talking to Twitter.com, but you are talking to the man in the middle, who is talking to Twitter for you. This MITM can view everything you send and even change what you receive.

{% include imgf src="7.png" alt="Diagram of Man in the middle" %}

The HTTPS protocol prevents MITM attacks. The HTTPS protocol is pretty complex, but all we need to know is that HTTPS uses a trusted Certificate Authority (CA) to sign a certificate. Our browsers assume that if a trusted CA signs the certificate, we are talking directly to who we think we are.

You can view what CA signed the certificate of the website you are viewing in your browser.

{% include imgf src="8.png" alt="Viewing a certificate in your browser" caption="Viewing a certificate in your browser" %}

This is great for protecting online communication but problematic for our debugging purposes. We are trying to man in the middle our own requests. To help overcome this, mitmproxy has generated a certificate. All we need is to get our machine to trust it.

{% include imgf src="9.png" alt="Getting a Certificate signed by an unknown certificate authority" caption="Getting a Certificate signed by an unknown certificate authority" %}

## How to Add a Trusted Certificate Authority Certificate

mitmproxy generated a certificate and private key the first time you ran it. The certificate generated is specific to your machine and is located in `~/.mitmproxy/mitmproxy-ca-cert.cer`

~~~{.bash caption=">_"}
> cat ~/.mitmproxy/mitmproxy-ca-cert.cer 
-----BEGIN CERTIFICATE-----
MIIC1TCCAb2gAwIBAgIJAOY7y/7Qrqr3MA0GCSqGSIb3DQEBBQUAMBoxGDAWBgNV
BAMTD3d3dy5leGFtcGxlLmNvbTAeFw0yMTAxMjYxNTQyMjhaFw0zMTAxMjQxNTQy
MjhaMBoxGDAWBgNVBAMTD3d3dy5leGFtcGxlLmNvbTCCASIwDQYJKoZIhvcNAQEB
BQADggEPADCCAQoCggEBAMLImmAMUg1zz6GnpoOA7Ln9p53o7v1M4+1O6lYmGtAK
4zetlcMF3mjtNr+AszBFYBpkhd1ef7rDSOc5YxCQ52SZlJc2l2vVtkn5bL1Xa2/W
AdzQcNq2meX6Pdm+YBC7KsmM8+uo8pXy3+gj7avWLXQ3BG+WaWRnRtgVoke53a0s
H+KFwR077XkrIYpOccsrX6+bMrjcnKkEbxb6Q8wdk664c+yf9F+WBC4zcnU43va/
Vl9ETGVOofab6YMk7CICFWEYj/1OJFIMNcEwWpm1eBDXvzt13d1xkiRTDYq+aRKb
utuFiYo7pngGjSEttQKl1nVUcDgkFhPE7Kz3mTBn2T8CAwEAAaMeMBwwGgYDVR0R
BBMwEYIPd3d3LmV4YW1wbGUuY29tMA0GCSqGSIb3DQEBBQUAA4IBAQAxT8EIJUAN
i842v+CoAOnRTO2jDtjIsxgg6WYlpHu1VL+Mh/ye4hfPz6DyyemM4Df64tEc7Mw8
KlhNqXfomY2trZHuxfeyMjg9GItmYaoeV+xg5SDYjGmgE2n8nc5FH5TlhimE9gd1
48NNMFRPXm2cYRz3T4i0HqesBrAmdpWBOQmCqzqF5SR08xqlS8X9ELzkRGTRDiJ5
4j5m1uI0rHyzSVlBK1DKy1LdkGNtes/OuTSZsnQ6PqZBzIZDhbzS0pz7GP9IqHkK
K2k43zCas8fHIU5o+0XoFQ7JoA+1AV3S9LYVD2rHfeOMMY/VzTP+b67/KY7H/Wl+
QyVJfmCmjt2i
-----END CERTIFICATE-----
~~~

~~~{.bash caption=">_"}
cat mitmproxy-ca.pem
-----BEGIN PRIVATE KEY-----
MIIC1TCCAb2gAwIBAgIJAOY7y/7Qrqr3MA0GCSqGSIb3DQEBBQUAMBoxGDAWBgNV
BAMTD3d3dy5leGFtcGxlLmNvbTAeFw0yMTAxMjYxNTQyMjhaFw0zMTAxMjQxNTQy
MjhaMBoxGDAWBgNVBAMTD3d3dy5leGFtcGxlLmNvbTCCASIwDQYJKoZIhvcNAQEB
BQADggEPADCCAQoCggEBAMLImmAMUg1zz6GnpoOA7Ln9p53o7v1M4+1O6lYmGtAK
4zetlcMF3mjtNr+AszBFYBpkhd1ef7rDSOc5YxCQ52SZlJc2l2vVtkn5bL1Xa2/W
AdzQcNq2meX6Pdm+YBC7KsmM8+uo8pXy3+gj7avWLXQ3BG+WaWRnRtgVoke53a0s
H+KFwR077XkrIYpOccsrX6+bMrjcnKkEbxb6Q8wdk664c+yf9F+WBC4zcnU43va/
Vl9ETGVOofab6YMk7CICFWEYj/1OJFIMNcEwWpm1eBDXvzt13d1xkiRTDYq+aRKb
utuFiYo7pngGjSEttQKl1nVUcDgkFhPE7Kz3mTBn2T8CAwEAAaMeMBwwGgYDVR0R
BBMwEYIPd3d3LmV4YW1wbGUuY29tMA0GCSqGSIb3DQEBBQUAA4IBAQAxT8EIJUAN
i842v+CoAOnRTO2jDtjIsxgg6WYlpHu1VL+Mh/ye4hfPz6DyyemM4Df64tEc7Mw8
KlhNqXfomY2trZHuxfeyMjg9GItmYaoeV+xg5SDYjGmgE2n8nc5FH5TlhimE9gd1
48NNMFRPXm2cYRz3T4i0HqesBrAmdpWBOQmCqzqF5SR08xqlS8X9ELzkRGTRDiJ5
4j5m1uI0rHyzSVlBK1DKy1LdkGNtes/OuTSZsnQ6PqZBzIZDhbzS0pz7GP9IqHkK
K2k43zCas8fHIU5o+0XoFQ7JoA+1AV3S9LYVD2rHfeOMMY/VzTP+b67/KY7H/Wl+
QyVJfmCmjt2i=
-----END PRIVATE KEY-----
~~~

*Note: Once we instruct our machine to trust this certificate, someone with the private key who controlled your internet connection, like your ISP, could use it to MITM your connection. For this reason, don't share your MITM private key, or any private key, with others.*

## Add the Cert on MacOS

On macOS, the easiest way to add a new CA is to copy it to the desktop and then double-click it.

~~~{.bash caption=">_"}
cp ~/.mitmproxy/mitmproxy-ca-cert.cer ~/Desktop
~~~

{% include imgf src="10.png" alt="Getting a Certificate signed by an unknown certificate authority" %}

You will be prompted for your credentials, and the certificate will be added as `untrusted`.

Double-click on the certificate in the Keychain list and set the 'Secure Sockets Layer' drop down to 'Always Trust'

{% include imgf src="11.png" alt="Setting certificate to Always Trust" %}

You will then be prompted for your password again, and then your certificate will be trusted.

{% include imgf src="13.png" alt="mitmproxy certificate proxy always trusted" %}

## Installing the Trusted Root Certificate On Windows

If you are on Windows, follow this guide [to add the MITM root certificate as a trusted root certificate authority](https://docs.microsoft.com/en-us/skype-sdk/sdn/articles/installing-the-trusted-root-certificate).

## Installing The Cert on Debian Based Linux Distributions

On Debian-based Linux distributions, follow these steps:

~~~{.bash caption=">_"}
> mkdir /usr/local/share/ca-certificates/extra
> cp ~/.mitmproxy/mitmproxy-ca-cert.cer \ 
     /usr/local/share/ca-certificates/extra/mitmproxy-ca-cert.crt
> update-ca-certificates
~~~

*We will be using these steps later when we work with docker containers on macOS and Windows.*

## Great Success

At this point, assuming you still have mitmproxy running and you still have your network interface setup to proxy through `localhost:8080`, you should be able to view all the HTTP and HTTPS network requests your machine is making in the mitmproxy (or mitmweb) window.

Here is Slack making requests:
{% include imgf src="14.png" alt="mitmweb has captured a request from the slack application" caption="mitmweb has captured a request from the slack application" %}

All HTTPS connections now have certificates signed by mitmproxy, which your machine trusts.

{% include imgf src="15.png" alt="Google.com now shows a mitmproxy signed certificate" caption="Google.com now shows a mitmproxy signed certificate" %}

## MITM the Docker Linux Container Host on macOS & Windows

{% include imgf src="16.png" alt="Diagram of docker runtime on macOS and Windows" caption="Docker containers run differently on macOS and Windows" %}

At this point, we can successfully capture traffic on our host operating system. Unfortunately, this is insufficient for capturing docker container traffic on macOS and Windows. So let's move on to proxying traffic on the Linux Container Host.  

On macOS and Windows, Linux containers do not run on the host OS. They can't because they need a Linux host to run. Instead, they run on the Linux Container Host, a VM that Docker Desktop manages.  

To see the docker daemon's incoming and outgoing requests, we need to get our proxy settings and our certificate authority into that VM.

Before we proceed, we need to clear the proxy settings on the [host network](/blog/docker-networking) connection. We can leave mitmproxy (or mitmweb running).

On Windows and macOS, the easiest way to configure a proxy is via `Docker Desktop.`  Configure the proxy settings under `Preferences -> Resources -> Proxies.`

{% include imgf src="18.png" alt="Configure the proxy settings under Preferences -> Resources -> Proxies." caption="Configure the proxy settings under `Preferences -> Resources -> Proxies.`" %}

With that done, the network interface will be proxied. All that is left to do is get our certificate trusted by the Linux container host. Thankfully, Docker Desktop takes care of this for us. On startup, Docker Desktop loads the trusted root certificates from the host machine into the Docker VM, so all we need to do is restart docker. (`Restart Docker` in Docker Desktop).

## Docker MITM on Linux

On Linux, we can add a proxy by editing the docker client config and then restarting.  

~~~{.json caption="~/.docker/config.json"}
{
 "proxies":
 {
   "default":
   {
     "httpProxy": "http://127.0.0.1:8080",
     "httpsProxy": "http://127.0.0.1:8080"
   }
 }
}
~~~

~~~{.bash caption=">_"}
> sudo service docker restart

~~~

### Test It

After restarting, we can test the proxying by performing a docker pull for a random image

~~~{.bash caption=">_"}
➜  ~ docker pull couchbase:7.0.0-beta
7.0.0-beta: Pulling from library/couchbase
83ee3a23efb7: Pull complete
db98fc6f11f0: Pull complete
f611acd52c6c: Pull complete
3aa2029a80db: Pull complete
abe30feace46: Pull complete
9b70018fbd54: Pull complete
d9b67d157052: Pull complete
212afe5e3a9c: Pull complete
ff5e5d4b4f9c: Pull complete
4df60b92878a: Pull complete
eee5137af1d8: Pull complete
c4ef83141448: Pull complete
6a04071b6d8c: Pull complete
f52d17d818b3: Pull complete
Digest: sha256:290a7a0623b62e02438e6f0cd03adf116ac465f70fc4254a4059bcf51e8fa040
Status: Downloaded newer image for couchbase:7.0.0-beta
docker.io/library/couchbase:7.0.0-beta
~~~

We can then see the requests and responses in our proxy:

{% include imgf src="19.png" alt="mitmproxy request for docker.io" %}

We can even see the binary payload of the layer requests and the fact that docker uses Cloudflare as a CDN.

{% include imgf src="20.png" alt="" caption="mitmweb request for Cloudflare.docker.com" %}

## *Troubleshooting*

*If `docker pull` fails with a certificate error or the requests don't get proxied, make sure you have restarted docker at least once and that the proxy settings are in place.*

## Capturing Docker Container Traffic

We now know how to capture traffic on our host machine and the Linux container host. But what happens when we make requests from inside a running container?

~~~{.bash caption=">_"}
> docker run -it ubuntu
root@ca43de1bb8b1:/# apt upgrade & apt update & apt install curl
...
root@167f5742c295:/# curl http://google.com
<HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">
<TITLE>301 Moved</TITLE></HEAD><BODY>
<H1>301 Moved</H1>
The document has moved
<A HREF="http://www.google.com/">here</A>.
</BODY></HTML>
~~~

We are successfully capturing the requests and responses:
{% include imgf src="21.png" alt="" caption="" %}

However, we hit problems when we try to use HTTPS:

~~~{.bash caption=">_"}
root@ca43de1bb8b1:/# curl https://google.com/
curl: (60) server certificate verification failed. CAfile: /etc/ssl/certs/ca-certificates.crt CRLfile: none
More details here: http://curl.haxx.se/docs/sslcerts.html

curl performs SSL certificate verification by default, using a "bundle"
 of Certificate Authority (CA) public keys (CA certs). If the default
 bundle file isn't adequate, you can specify an alternate file
 using the --cacert option.
If this HTTPS server uses a certificate signed by a CA represented in
 the bundle, the certificate verification probably failed due to a
 problem with the certificate (it might be expired, or the name might
 not match the domain name in the URL).
If you'd like to turn off curl's verification of the certificate, use
 the -k (or --insecure) option.
 > exit
~~~

## Adding the CA Cert to our Linux Container

The solution here is a familiar one. We need to follow the steps we used above for configuring Linux to trust a certificate authority, but we need to do it inside our container.

There are several ways to accomplish this.

## Solution #1: Volume Mount The Cert

The simplest solution is to mount the certificate into the proper spot in our container and run `update-ca-certificates`.

### Alpine

First, we run the container and mount in our CA Certificate.

~~~{.bash caption=">_"}
> docker run -it -v ~/.mitmproxy/mitmproxy-ca-cert.cer:/usr/local/share/
ca-certificates/mitmproxy-ca-cert.cer alpine
~~~

Inside the container, add our dependencies:

~~~{.bash caption="alpine prompt"}
> apk update && apk upgrade && apk add ca-certificates && 
apk add curl
...
~~~

Trust our certificate:

~~~{.bash caption="alpine prompt"}
> update-ca-certificates
Updating certificates in /etc/ssl/certs...
1 added, 0 removed; done.
Running hooks in /etc/ca-certificates/update.d...
done.
~~~

Then we can test it with a HTTPS request

~~~{.bash caption="alpine prompt"}
root@167f5742c295:/# curl https://google.com
<HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">
<TITLE>301 Moved</TITLE></HEAD><BODY>
<H1>301 Moved</H1>
The document has moved
<A HREF="https://www.google.com/">here</A>.
</BODY></HTML>
~~~

That is a success!

### Ubuntu

The general pattern with some small modifications works on Ubuntu-based images as well.

First, we run the container and mount in our CA Certificate.

~~~{.bash caption=">_"}
> docker run -it -v ~/.mitmproxy/mitmproxy-ca-cert.cer:/usr/local/share/
ca-certificates/mitmproxy-ca-cert.crt ubuntu
~~~

We update our dependencies:

~~~{.bash caption="ubuntu prompt"}
> apt update && apt upgrade && apt install ca-certificates curl
~~~

We trust our cert:

~~~{.bash caption="ubuntu prompt"}
> update-ca-certificates 
Updating certificates in /etc/ssl/certs...
1 added, 0 removed; done.
Running hooks in /etc/ca-certificates/update.d...
done.
~~~

Then we can test it with a HTTPS request.

~~~{.bash caption="ubuntu prompt"}
root@167f5742c295:/# curl https://google.com
<HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">
<TITLE>301 Moved</TITLE></HEAD><BODY>
<H1>301 Moved</H1>
The document has moved
<A HREF="https://www.google.com/">here</A>.
</BODY></HTML>
~~~

Success!

## Solution #2: Extend the Image

Volume mounting the certificate and manually running `update-ca-certificates` is an excellent proof of concept, but if you want to run a docker container in the background and have all traffic proxied, then interactive mode won't cut it. In that case, extending the image is the way to go.

## Extending an Alpine Image to Add a Certificate Authority

We can create a new Dockerfile that extends the image we want to proxy and add in the certificate.

~~~{.dockerfile caption="Dockerfile"}
FROM alpine # or any alpine based image
RUN apk update && apk add curl
WORKDIR /usr/local/share/ca-certificates
COPY mitmproxy.crt mitmproxy.crt
RUN update-ca-certificates
~~~

We can then build it and tag it with a `:mitm` tag.

~~~{.bash caption=">_"}
> docker build --tag alpine:mitm .
[+] Building 1.9s (10/10) FINISHED                             
 => [internal] load build definition from Dockerfile      0.0s
 => => transferring dockerfile: 200B                      0.0s
 => [internal] load .dockerignore                         0.0s
 => => transferring context: 2B                           0.0s
 => [internal] load metadata for docker.io/library/alpin  0.0s
 => CACHED [1/5] FROM docker.io/library/alpine            0.0s
 => [internal] load build context                         0.2s
 => => transferring context: 1.36kB                       0.2s
 => [2/5] RUN apk update && apk add curl                  1.4s
 => [3/5] WORKDIR /usr/local/share/ca-certificates        0.0s
 => [4/5] COPY mitmproxy.crt mitmproxy.crt                0.0s 
 => [5/5] RUN /usr/sbin/update-ca-certificates            0.3s 
 => exporting to image                                    0.1s 
 => => exporting layers                                   0.1s 
 => => writing image sha256:ca5be16f3d19c34ea5e29ac1774b  0.0s 
 => => naming to docker.io/library/alpine:mitm            0.0s
~~~

Now anytime we run this image, it will be ready to accept responses signed by our certificate authority. And because we didn't change the entry point, we can use it wherever we would use the base image.

~~~{.bash caption=">_"}
> docker run -it alpine:mitm      

> curl https://google.com
<HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">
<TITLE>301 Moved</TITLE></HEAD><BODY>
<H1>301 Moved</H1>
The document has moved
<A HREF="https://www.google.com/">here</A>.
</BODY></HTML>
~~~

Any requests by anything running inside the container will be transparently proxied. If you are trying to debug what a service you depend on is doing this will come in handy.  

## Extending an Ubuntu Image to Add a Certificate Authority

A similar process will work with Ubuntu-based images:

~~~{.dockerfile caption="dockerfile"}
FROM ubuntu
RUN apt update -y && apt upgrade -y && apt install ca-certificates curl -y
WORKDIR /usr/local/share/ca-certificates
COPY mitmproxy.crt mitmproxy.crt
RUN update-ca-certificates 
~~~

~~~{.bash caption=">_"}
> docker build --tag ubuntu:mitm .
[+] Building 36.4s (10/10) FINISHED                            
 => [internal] load build definition from Dockerfile      0.0s
 => => transferring dockerfile: 234B                      0.0s
 => [internal] load .dockerignore                         0.0s
 => => transferring context: 2B                           0.0s
 => [internal] load metadata for docker.io/library/ubunt  0.0s
 => CACHED [1/5] FROM docker.io/library/ubuntu            0.0s
 => [internal] load build context                         0.0s
 => => transferring context: 35B                          0.0s
 => [2/5] RUN apt update -y && apt upgrade -y && apt in  35.0s
 => [3/5] WORKDIR /usr/local/share/ca-certificates        0.0s
 => [4/5] COPY mitmproxy.crt mitmproxy.crt                0.0s
 => [5/5] RUN update-ca-certificates                      0.9s 
 => exporting to image                                    0.4s 
 => => exporting layers                                   0.3s 
 => => writing image sha256:06fbbeea728364e3bacef503f7c2  0.0s 
 => => naming to docker.io/library/ubuntu:mitm            0.0s
~~~

~~~{.bash caption=">_"}
> docker run -it ubuntu:mitm    
root> curl https://google.com
<HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">
<TITLE>301 Moved</TITLE></HEAD><BODY>
<H1>301 Moved</H1>
The document has moved
<A HREF="https://www.google.com/">here</A>.
</BODY></HTML>
# Success
~~~

## But Wait, There's More

{% include imgf src="22.png" alt="man in the middle diagram" %}

There we go. We can now capture HTTPS traffic made by any containers we run. Combined with the previous steps, we can now intercept and inspect HTTP and HTTPS protocol traffic on our host machine, on a Linux virtual machine running in a hypervisor, and in the actual running containers.  

If you can get something running on your local machine, you can now capture and inspect its network requests. This can be very handy for debugging problems and building up an understanding of how something works without digging into the source code. The setup can be a bit complicated, but I hope you can see why mitmproxy is a great tool to keep in your toolkit.

The fun doesn't stop here, though.  [mitmproxy](https://mitmproxy.org/) can modify and replay requests and has an active ecosystem, including [mastermind](https://github.com/ustwo/mastermind) which lets you build mock services based on captured requests and [BDFProxy](https://github.com/secretsquirrel/BDFProxy), which uses mitmproxy to modify common security updates for <del>nefarious reasons</del> security research projects, and much more.  

And if you liked this article you might like to hear a little about the [backstory behind](/blog/introducing-earthly-build-automation-for-the-container-era) [Earthly](https://earthly.dev/).

{% include_html cta/bottom-cta.html %}
