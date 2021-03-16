---
title: How to Man in the Middle HTTPS Using mitmproxy
date: '2021-02-11 13:30:00'
---

## 

Have you ever wanted to see what kinds of requests a service or application on your machine is making and what kind of responses it is getting back? &nbsp;Have you ever tried and failed to capture this traffic or modify it to investigate how something works (or doesn't work). &nbsp;If you have, then mitmproxy might be what you need. Being able to scan through and observe HTTP protocol traffic easily is a great debugging aid.

This guide will walk you through installing and using mitmproxy to capture HTTPS requests. &nbsp;We will start with macOS traffic capture, then touch on Linux and Windows and then finally show how to capture docker daemon traffic and docker container traffic.

## What is mitmproxy?

mitmproxy is a command-line tool that acts as a HTTP and HTTPS proxy and records all the traffic. &nbsp;You can easily see what requests are being made and even replay them. &nbsp;It's great for diagnosing problems.

## Installing it

On Mac, mitmproxy is easy to install with brew:

    brew install mitmproxy

On Windows and Linux, [download the binary release](https://docs.mitmproxy.org/stable/overview-installation/) and place it somewhere in your path.

## #1 Start it up

To start up mitmproxy, type `mitmproxy`, and it will start up bound to port 8080.

    >mitmproxy

The command-line interface (CLI) has VIM-like keybindings. `q` will quit, and arrow keys or `h`, `j`, `k`, `l` will move you up and down through the request list. `?` will load the help, and `<<enter>>` will drill in on a specific request.

<figure class="kg-card kg-image-card kg-card-hascaption"><img src="/content/images/2021/02/1.png" class="kg-image" alt><figcaption>help menu for mitmproxy</figcaption></figure>

mitmproxy also has a web interface if you prefer the mouse over VIM keybindings. The advanced functionality is a bit more discoverable in the web interface, but the CLI version is convenient for quick capture sessions.

<figure class="kg-card kg-image-card"><img src="/content/images/2021/02/2.png" class="kg-image" alt></figure><figure class="kg-card kg-image-card"><img src="/content/images/2021/02/3.png" class="kg-image" alt srcset="/content/images/size/w600/2021/02/3.png 600w, /content/images/size/w1000/2021/02/3.png 1000w, /content/images/2021/02/3.png 1476w" sizes="(min-width: 720px) 720px"></figure>

We will use both throughout the tutorial. &nbsp;Whichever you choose, start it up and leave it running.

## #2 Proxy Our Connection

Let's set up our internet connection to use this proxy. On macOS, Under `Setting -> Network`, select your network and click advanced.

<figure class="kg-card kg-image-card kg-card-hascaption"><img src="/content/images/2021/02/4.png" class="kg-image" alt="Setting -&gt; Network on macOS" srcset="/content/images/size/w600/2021/02/4.png 600w, /content/images/2021/02/4.png 672w"><figcaption><code>Setting -&gt; Network</code> on macOS</figcaption></figure>

Under proxies, enable both HTTP and HTTPS proxies and choose port 8080:

<figure class="kg-card kg-image-card kg-card-hascaption"><img src="/content/images/2021/02/5.png" class="kg-image" alt="Setting -&gt; Network-&gt; Advanced on macOS" srcset="/content/images/size/w600/2021/02/5.png 600w, /content/images/2021/02/5.png 669w"><figcaption>Setup Proxy under Setting -&gt; Network-&gt; Advanced on macOS</figcaption></figure>

_On Windows, [follow these steps](https://www.howtogeek.com/tips/how-to-set-your-proxy-settings-in-windows-8.1/) to set up a proxy._

_On Linux, MITM supports a [transparent proxying](https://docs.mitmproxy.org/stable/howto-transparent/) at the network layer._

## Adding mitmproxy as a Certificate Authority

We now have our connection proxied to go through our instance of mitmproxy. &nbsp;However, if we attempt to make an HTTPS-based request in a web browser (loading twitter.com for example), something interesting happens.

<figure class="kg-card kg-image-card kg-card-hascaption"><img src="/content/images/2021/02/6.png" class="kg-image" alt="NET::ERR_CERT_AUTHORITY_INVALID error in Chrome" srcset="/content/images/size/w600/2021/02/6.png 600w, /content/images/size/w1000/2021/02/6.png 1000w, /content/images/2021/02/6.png 1434w" sizes="(min-width: 720px) 720px"><figcaption>Chrome does not recognize the certificate</figcaption></figure>

Chrome is warning us that we might be subject to a man in the middle attack.

### What Is a Man in the Middle

A man in the middle attack (MITM) is a security threat where an attacker can intercept incoming and outgoing requests. &nbsp;You think you are talking to Twitter.com, but you are talking to the man in the middle, who is talking to Twitter for you. &nbsp;This MITM can view everything you send and even change what you receive.

<figure class="kg-card kg-image-card"><img src="/content/images/2021/02/7.png" class="kg-image" alt="Diagram of a man in the middle attack" srcset="/content/images/size/w600/2021/02/7.png 600w, /content/images/size/w1000/2021/02/7.png 1000w, /content/images/size/w1600/2021/02/7.png 1600w, /content/images/size/w2400/2021/02/7.png 2400w" sizes="(min-width: 720px) 720px"></figure>

The HTTPS protocol prevents MITM attacks. &nbsp;The HTTPS protocol is pretty complex, but all we need to know is that HTTPS uses a trusted Certificate Authority (CA) to sign a certificate. Our browsers assume that if a trusted CA signs the certificate, we are talking directly to who we think we are.

You can view what CA signed the certificate of the website you are viewing in your browser.

<figure class="kg-card kg-image-card kg-card-hascaption"><img src="/content/images/2021/02/8.png" class="kg-image" alt="DigiCert certificate for twitter.com" srcset="/content/images/size/w600/2021/02/8.png 600w, /content/images/2021/02/8.png 940w" sizes="(min-width: 720px) 720px"><figcaption>Viewing a certificate in your browser</figcaption></figure>

This is great for protecting online communication but problematic for our debugging purposes. We are trying to man in the middle our own requests. &nbsp;To help overcome this, mitmproxy has generated a certificate. All we need is to get our machine to trust it.

<figure class="kg-card kg-image-card kg-card-hascaption"><img src="/content/images/2021/02/9.png" class="kg-image" alt="Diagram of certificate authority not being trusted" srcset="/content/images/size/w600/2021/02/9.png 600w, /content/images/size/w1000/2021/02/9.png 1000w, /content/images/size/w1600/2021/02/9.png 1600w, /content/images/size/w2400/2021/02/9.png 2400w" sizes="(min-width: 720px) 720px"><figcaption>Getting a Certificate signed by an unknown certificate authority</figcaption></figure>
# How to Add a Trusted Certificate Authority Certificate

mitmproxy generated a certificate and private key the first time you ran it. The certificate generated is specific to your machine and is located in `~/.mitmproxy/mitmproxy-ca-cert.cer`

    > cat ~/.mitmproxy/mitmproxy-ca-cert.cer 
    -----BEGIN CERTIFICATE-----
    MIIC1TCCAb2gAwIBAgIJAOY7y/7Qrqr3MA0GCSqGSIb3DQEBBQUAMBoxGDAWBgNV
    BAMTD3d3dy5leGFtcGxlLmNvbTAeFw0yMTAxMjYxNTQyMjhaFw0zMTAxMjQxNTQy
    MjhaMBoxGDAWBgNVBAMTD3d3dy5leGFtcGxlLmNvbRCCASIwDQYJKoZIhvcNAQEB
    BQADggEPADCCAQoCggEBAMLImmAMUg1zz6GnpoOA7Ln9p53o7v1M4+1O6lYmGtAK
    4zetlcMF3mjtNr+AszBFYBpkhd1ef7rDSOc5YxCQ52SZlJc2l2vVtkn5bL1Xa2/W
    AdzQcNq2meX6Pdm+YBC7KsmM8+uo8pXy3+gj7avWLXQ3BG+WaWRnRtgVoke53a0s
    H+KFwR077XkrIYpOccsrX6+bMrjcnKaEbxb6Q8wdk664c+yf9F+WBC4zcnU43va/
    Vl9ETGVOofab6YMk7CICFWEYj/1OJFIMNcEwWpm1eBDXvzt13d1xkiRTDYq+aRKb
    utuFiYo7pngGjSEttQKl1nVUcDgkFhPE7Kz3mTBn2T8CAwEAAaMeMBwwGgYDVR0R
    BBMwEBIPd3d3LmV4YW1wbGUuY29tMA0GCSqGSIb3DQEBBQUAA4IBAQAxT8EIJUAN
    i842v+CoAOnRTO2jDtjIsxgg6WYlpHu1VL+Mh/ye4hfPz6DyyemM4Df64tEc7Mw8
    KlhNqXfomY2trZHuxfeyMjg9GItmYaoeV+xg5SDYjGmgE2n8nc5FH5TlhimE9gd1
    48NNMFRPXm2cYRz3T4i0HqesBrAmdpWBOQmCqzqF5SR08xqlS8X9ELzkRGTRDiJ5
    4j5m1uI0rHyzSVlBK1DKy1LdkGNtes/OuTSZsnQ6PqZBzIZDhbzS0pz7GP9IqHkK
    K2k43zCas8fHIU5o+0XoFQ7JoA+1AV3S9LYVD2rHfeOMMY/VzTP+b67/KY7H/Wl+
    QyVJfmCmjt2i
    -----END CERTIFICATE-----
    cat mitmproxy-ca.pem
    -----BEGIN PRIVATE KEY-----
    MIIC1TCCAb2gAwIBAgIJAOY7y/7Qrqr3MA0GCSqGSIb3DQEBBQUAMBoxGDAWBgNV
    BAMTD3d3dy5leGFtcGxlLmNvbTAeFw0yMTAxMjYxNTQyMjhaFw0zMTAxMjQxNTQy
    MjhaMBoxGDAWBgNVBAMTD3d3dy5leGFtcGxlLmNvbTCCASIwDQYJKoZIhvcNAQEB
    BQADggEPADCCAQoCggEBAMLImmAMUg1zz6GnpoOA7Ln9p53o7v1M4+1O6lYmGtAK
    4zetlcMF3mjtNr+AszBFYBpkhd1ef7rDSOc5Y9CQ52SZlJc2l2vVtkn5bL1Xa2/W
    AdzQcNq2meX6Pdm+YBC7KsmM8+uo8pXy3+gj7avWLXQ3BG+WaWRnRtgVoke53a0s
    H+KFwR077XkrIYpOccsrX6+bMrjcnKkEbxb6Q8wdk664c+yf9F+WBC4zcnU43va/
    Vl9ETGVOofab6YMk7CICFWEYj/1OJFIMNcEwWpm1eBDXvzt13d1xkiRTDYq+aRKb
    utuFiYo7pngGjSEttQKl1nVUcDgkFhPE7Kz3mJBn2T8CAwEAAaMeMBwwGgYDVR0R
    BBMwE1IPd3d3LmV4YW1wbGUuY29tMA0GCSqGSIb3DQEBBQUAA4IBAQAxT8EIJUAN
    i842v+CoAOnRTO2jDtjIsxgg6WYlpHu1VL+Mh/ye4hfPz6DyyemM4Df64tEc7Mw8
    KlhNqXfomY2trZHuxfeyMjg9GItmYaoeV+xg5SDYjGmgE2n8nc5FH5TlhimE9gd1
    48NNMFRPXm2cYRz3T4i0HqesBrAmdpWBOQmCqzqF5SR08xqlS8X9ELzkRGTRDiJ5
    4j5m1uI0rHyzSVlBK1DKy1LdkGNtes/OuTSZsnQ6PqZBzIZDhbzS0pz7GP9IqHkK
    K2k43zCas8fHIU5o+0XoFQ7JoA+1AV3S9LYVD2rHfeOMMY/VzTP+b67/KY7H/Wl+
    QyVJfmCmjt2i=
    -----END PRIVATE KEY-----

_Note: Once we instruct our machine to trust this certificate, someone with the private key who controlled your internet connection, like your ISP, could use it to MITM your connection. For this reason, don't share your MITM private key, or any private key, with others._

# Add the Certificate on MacOS

On macOS, the easiest way to add a new CA is to copy it to the desktop and then double-click it.

    cp ~/.mitmproxy/mitmproxy-ca-cert.cer ~/Desktop

<figure class="kg-card kg-image-card"><img src="/content/images/2021/02/10.png" class="kg-image" alt="Certificate on Desktop of macOS computer" srcset="/content/images/size/w600/2021/02/10.png 600w, /content/images/2021/02/10.png 632w"></figure>

You will be prompted for your credentials, and the certificate will be added as 'untrusted'.

Double-click on the certificate in the Keychain list and set the 'Secure Sockets Layer' drop down to 'Always Trust':

<figure class="kg-card kg-image-card"><img src="/content/images/2021/02/11.png" class="kg-image" alt="Setting certificate to 'Always Trust'" srcset="/content/images/size/w600/2021/02/11.png 600w, /content/images/size/w1000/2021/02/11.png 1000w, /content/images/2021/02/11.png 1036w" sizes="(min-width: 720px) 720px"></figure>

You will then be prompted for your password again, and then your certificate will be trusted:

<figure class="kg-card kg-image-card"><img src="/content/images/2021/02/13.png" class="kg-image" alt="mitmproxy certificate authority now trusted" srcset="/content/images/size/w600/2021/02/13.png 600w, /content/images/size/w1000/2021/02/13.png 1000w, /content/images/2021/02/13.png 1030w" sizes="(min-width: 720px) 720px"></figure>
## Installing the Trusted Root Certificate on Windows

If you are on Windows, follow this guide [to add the MITM root certificate as a trusted root certificate authority](https://docs.microsoft.com/en-us/skype-sdk/sdn/articles/installing-the-trusted-root-certificate).

## Installing the Certificate on Debian Based Linux Distributions

On Debian-based Linux distributions, follow these steps:

    > mkdir /usr/local/share/ca-certificates/extra
    > cp ~/.mitmproxy/mitmproxy-ca-cert.cer /usr/local/share/ca-certificates/extra/mitmproxy-ca-cert.crt
    > update-ca-certificates

_We will be using these steps later when we work with docker containers on macOS and Windows._

## Great Success!

At this point, assuming you still have mitmproxy running and you still have your network interface setup to proxy through `localhost:8080`, you should be able to view all the HTTP and HTTPS network requests your machine is making in the mitmproxy (or MITMWeb) window.

Here is Slack making requests:

<figure class="kg-card kg-image-card kg-card-hascaption"><img src="/content/images/2021/02/14.png" class="kg-image" alt="mitmweb proxy of slack get request slack.com/beacon/timing?user_id" srcset="/content/images/size/w600/2021/02/14.png 600w, /content/images/size/w1000/2021/02/14.png 1000w, /content/images/size/w1600/2021/02/14.png 1600w, /content/images/size/w2400/2021/02/14.png 2400w" sizes="(min-width: 720px) 720px"><figcaption>mitmweb has captured a request from the slack application</figcaption></figure>

All HTTPS connections now have certificates signed by mitmproxy, which your machine trusts.

<figure class="kg-card kg-image-card kg-card-hascaption"><img src="/content/images/2021/02/15.png" class="kg-image" alt="google.com certificate issued by mitmproxy" srcset="/content/images/size/w600/2021/02/15.png 600w, /content/images/2021/02/15.png 966w" sizes="(min-width: 720px) 720px"><figcaption>Google.com now shows a mitmproxy signed certificate</figcaption></figure>
## MITM the Docker Linux Container Host on macOS & Windows
<figure class="kg-card kg-image-card kg-card-hascaption"><img src="/content/images/2021/02/16.png" class="kg-image" alt="Diagram of docker runtime on macOS and Windows" srcset="/content/images/size/w600/2021/02/16.png 600w, /content/images/size/w1000/2021/02/16.png 1000w, /content/images/2021/02/16.png 1428w" sizes="(min-width: 720px) 720px"><figcaption>Docker containers run differently on macOS and Windows</figcaption></figure>

At this point, &nbsp;we can successfully capture traffic on our host operating system. Unfortunately, this is insufficient for capturing docker container traffic on macOS and Windows. So let's move on to proxying traffic on the Linux Container Host.

On macOS and Windows, Linux containers do not run on the host OS. They can't because they need a Linux host to run. &nbsp;Instead, they run on the Linux Container Host, a VM that Docker Desktop manages.

To see the docker daemon's incoming and outgoing requests, we need to get our proxy settings and our certificate authority into that VM.

> Before we proceed, we need to clear the proxy settings on the host network connection. We can leave mitmproxy (or MITMWeb running).

On Windows and macOS, the easiest way to configure a proxy is via `Docker Desktop.` &nbsp;Configure the proxy settings under `Preferences -> Resources -> Proxies.`

<figure class="kg-card kg-image-card kg-card-hascaption"><img src="/content/images/2021/02/18.png" class="kg-image" alt="Configure the proxy settings under Preferences -&gt; Resources -&gt; Proxies." srcset="/content/images/size/w600/2021/02/18.png 600w, /content/images/size/w1000/2021/02/18.png 1000w, /content/images/size/w1600/2021/02/18.png 1600w, /content/images/size/w2400/2021/02/18.png 2400w" sizes="(min-width: 720px) 720px"><figcaption>Configure the proxy settings under <code>Preferences -&gt; Resources -&gt; Proxies.</code></figcaption></figure>

With that done, the network interface will be proxied. &nbsp;All that is left to do is get our certificate trusted by the Linux container host. Thankfully, Docker Desktop takes care of this for us. &nbsp;On startup, Docker Desktop loads the trusted root certificates from the host machine into the Docker VM, so all we need to do is restart docker. (`Restart Docker` in Docker Desktop).

## Docker MITM on Linux

On Linux, we can add a proxy by editing the docker client config and then restarting.

    > cat ~/.docker/config.json
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

    > sudo service docker restart
    

### Test it

After restarting, we can test the proxying by performing a docker pull for a random image

    ➜ ~ docker pull couchbase:7.0.0-beta
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

We can then see the requests and responses in our proxy:

<figure class="kg-card kg-image-card"><img src="/content/images/2021/02/19.png" class="kg-image" alt="mitmproxy with docker.io requests" srcset="/content/images/size/w600/2021/02/19.png 600w, /content/images/size/w1000/2021/02/19.png 1000w, /content/images/2021/02/19.png 1158w" sizes="(min-width: 720px) 720px"></figure>

We can even see the binary payload of the layer requests and the fact that docker uses Cloudflare as a CDN.

<figure class="kg-card kg-image-card"><img src="/content/images/2021/02/20.png" class="kg-image" alt="mitmproxy request for cloudflare.docker.com" srcset="/content/images/size/w600/2021/02/20.png 600w, /content/images/size/w1000/2021/02/20.png 1000w, /content/images/2021/02/20.png 1146w" sizes="(min-width: 720px) 720px"></figure>
## _Troubleshooting_

_If `docker pull` fails with a certificate error or the requests don't get proxied, make sure you have restarted docker at least once and that the proxy settings are in place._

# Capturing Docker Container Traffic

We now know how to capture traffic on our host machine and the Linux container host. But what happens when we make requests from inside a running container?

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

We are successfully capturing the requests and responses:

<figure class="kg-card kg-image-card kg-card-hascaption"><img src="/content/images/2021/02/21.png" class="kg-image" alt="mitmweb with GET requests to archive.ubuntu.com" srcset="/content/images/size/w600/2021/02/21.png 600w, /content/images/size/w1000/2021/02/21.png 1000w, /content/images/size/w1600/2021/02/21.png 1600w, /content/images/2021/02/21.png 2342w" sizes="(min-width: 720px) 720px"><figcaption>mitmweb</figcaption></figure>

However, we hit problems when we try to use HTTPS:

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

## Adding the CA Cert to our Linux Container

The solution here is a familiar one. &nbsp;We need to follow the steps we used above for configuring Linux to trust a certificate authority, but we need to do it inside our container.

There are several ways to accomplish this.

## Solution #1: Volume Mount The Cert

The simplest solution is to mount the certificate into the proper spot in our container and run `update-ca-certificates`.

### Alpine:

    # Run container and mount in our CA Cert
    > docker run -it -v ~/.mitmproxy/mitmproxy-ca-cert.cer:/usr/local/share/ca-certificates/mitmproxy-ca-cert.cer alpine
    # Add ca-certificates (and curl for testing)
    root@167f5742c295:/# apk update && apk upgrade && apk add ca-certificates && apk add curl
    ...
    
    # include trust our cert
    root@167f5742c295:/# update-ca-certificates
    Updating certificates in /etc/ssl/certs...
    1 added, 0 removed; done.
    Running hooks in /etc/ca-certificates/update.d...
    done.
    
    # Test https
    root@167f5742c295:/# curl https://google.com
    <HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">
    <TITLE>301 Moved</TITLE></HEAD><BODY>
    <H1>301 Moved</H1>
    The document has moved
    <A HREF="https://www.google.com/">here</A>.
    </BODY></HTML>
    
    # Success!

### Ubuntu

The general pattern with some small modifications works on Ubuntu-based images as well.

    > docker run -it -v ~/.mitmproxy/mitmproxy-ca-cert.cer:/usr/local/share/ca-certificates/mitmproxy-ca-cert.crt ubuntu
    
    root@167f5742c295:/# apt update && apt upgrade && apt install ca-certificates curl
    
    root@167f5742c295:/# update-ca-certificates 
    Updating certificates in /etc/ssl/certs...
    1 added, 0 removed; done.
    Running hooks in /etc/ca-certificates/update.d...
    done.
    
    root@167f5742c295:/# curl https://google.com
    <HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">
    <TITLE>301 Moved</TITLE></HEAD><BODY>
    <H1>301 Moved</H1>
    The document has moved
    <A HREF="https://www.google.com/">here</A>.
    </BODY></HTML>
    
    \> # Success!!

## Solution #2: Extend the Image

Volume mounting the certificate and manually running `update-ca-certificates` is an excellent proof of concept, but if you want to run a docker container in the background and have all traffic proxied, then interactive mode won't cut it. In that case, extending the image is the way to go.

## Extending an Alpine Image to Add a Certificate Authority

We can create a new Dockerfile that extends the image we want to proxy and add in the needed certificate.

    FROM alpine # or any alpine based image
    RUN apk update && apk add curl
    WORKDIR /usr/local/share/ca-certificates
    COPY mitmproxy.crt mitmproxy.crt
    RUN update-ca-certificates

We can then build it and tag it with a `:mitm` tag.

    > docker build --tag alpine:mitm .
    [+] Building 1.9s (10/10) FINISHED                             
     => [internal] load build definition from Dockerfile 0.0s
     => => transferring dockerfile: 200B 0.0s
     => [internal] load .dockerignore 0.0s
     => => transferring context: 2B 0.0s
     => [internal] load metadata for docker.io/library/alpin 0.0s
     => CACHED [1/5] FROM docker.io/library/alpine 0.0s
     => [internal] load build context 0.2s
     => => transferring context: 1.36kB 0.2s
     => [2/5] RUN apk update && apk add curl 1.4s
     => [3/5] WORKDIR /usr/local/share/ca-certificates 0.0s
     => [4/5] COPY mitmproxy.crt mitmproxy.crt 0.0s 
     => [5/5] RUN /usr/sbin/update-ca-certificates 0.3s 
     => exporting to image 0.1s 
     => => exporting layers 0.1s 
     => => writing image sha256:ca5be16f3d19c34ea5e29ac1774b 0.0s 
     => => naming to docker.io/library/alpine:mitm 0.0s

Now anytime we run this image, it will be ready to accept responses signed by our certificate authority. And because we didn't change the entry point, we can use it wherever we would use the base image.

    > docker run -it alpine:mitm      
    \> curl https://google.com
    <HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">
    <TITLE>301 Moved</TITLE></HEAD><BODY>
    <H1>301 Moved</H1>
    The document has moved
    <A HREF="https://www.google.com/">here</A>.
    </BODY></HTML>

Any requests by anything running inside the container will be transparently proxied. If you are trying to debug what a service you depend on is doing, this will come in handy.

## Extending an Ubuntu Image to Add a Certificate Authority

A similar process will work with Ubuntu-based images:

    FROM ubuntu
    RUN apt update -y && apt upgrade -y && apt install ca-certificates curl -y
    WORKDIR /usr/local/share/ca-certificates
    COPY mitmproxy.crt mitmproxy.crt
    RUN update-ca-certificates 

    > docker build --tag ubuntu:mitm .
    [+] Building 36.4s (10/10) FINISHED                            
     => [internal] load build definition from Dockerfile 0.0s
     => => transferring dockerfile: 234B 0.0s
     => [internal] load .dockerignore 0.0s
     => => transferring context: 2B 0.0s
     => [internal] load metadata for docker.io/library/ubunt 0.0s
     => CACHED [1/5] FROM docker.io/library/ubuntu 0.0s
     => [internal] load build context 0.0s
     => => transferring context: 35B 0.0s
     => [2/5] RUN apt update -y && apt upgrade -y && apt in 35.0s
     => [3/5] WORKDIR /usr/local/share/ca-certificates 0.0s
     => [4/5] COPY mitmproxy.crt mitmproxy.crt 0.0s
     => [5/5] RUN update-ca-certificates 0.9s 
     => exporting to image 0.4s 
     => => exporting layers 0.3s 
     => => writing image sha256:06fbbeea728364e3bacef503f7c2 0.0s 
     => => naming to docker.io/library/ubuntu:mitm 0.0s

    > docker run -it ubuntu:mitm    
    root> curl https://google.com
    <HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">
    <TITLE>301 Moved</TITLE></HEAD><BODY>
    <H1>301 Moved</H1>
    The document has moved
    <A HREF="https://www.google.com/">here</A>.
    </BODY></HTML>
    # Success

## But wait, There's More
<figure class="kg-card kg-image-card"><img src="/content/images/2021/02/22.png" class="kg-image" alt="Diagram of a man in the middle attack" srcset="/content/images/size/w600/2021/02/22.png 600w, /content/images/size/w1000/2021/02/22.png 1000w, /content/images/size/w1600/2021/02/22.png 1600w, /content/images/size/w2400/2021/02/22.png 2400w" sizes="(min-width: 720px) 720px"></figure>

There we go. We can now capture HTTPS traffic made by any containers we run. Combined with the previous steps, we can now intercept and inspect HTTP and HTTPS protocol traffic on our host machine, on a Linux virtual machine running in a hypervisor, and in the actual running containers.

If you can get something running on your local machine, you can now capture and inspect its network requests. This can be very handy for debugging problems and building up an understanding of how something works without digging into the source code. The setup can be a bit complicated, but I hope you can see why mitmproxy is a great tool to keep in your toolkit.

The fun doesn't stop here, though. &nbsp;[mitmproxy](https://mitmproxy.org/) can modify and replay requests and has an active ecosystem, including [mastermind](https://github.com/ustwo/mastermind) which lets you build mock services based on captured requests and [BDFProxy](https://github.com/secretsquirrel/BDFProxy), which uses mitmproxy to modify standard security updates for nefarious reasons security research projects, and much more.

