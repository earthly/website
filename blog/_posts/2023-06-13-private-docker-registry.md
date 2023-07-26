---
title: "How to Set Up a Private Docker Registry on Linux"
categories:
  - Tutorials
toc: true
author: Hitesh Jethva

internal-links:
 - Docker
 - Registry
 - Linux
 - Security
 - Container
 - Images
excerpt: |
    Learn how to set up a private Docker registry on Linux and secure your Docker images in an enterprise environment. This step-by-step guide covers everything from installing Docker and Docker Compose to configuring NGINX and implementing authentication, allowing you to have full control over your Docker registry and ensure the security of your images.
---

**We're [Earthly.dev](https://earthly.dev/). We make building software simpler and therefore faster using containerization. This article covers setting up a private Docker registry on Linux. If you want to know more about building in containers then [check us out](/).**

If you're working with Docker images in an enterprise environment where security is a concern, a private Docker registry is a great solution. While public registries like Docker Hub allow anyone to push and pull images, they have limitations on the number of image pull requests per six hours and limited control over the registry security.

On the other hand, a private registry provides central image management, cost-saving, scanning capabilities, access control, support for external storage, and more security features. With a private registry, you can define your own storage location for all your images and set your own policies to prevent deploying images that don't meet your policy standard.

You have some choices when it comes to setting up a private registry. You could use a third party service like [Amazon ECR](/blog/how-to-setup-and-use-amazons-elastic-container-registry), or you can set up your own registry, which is surprising easy to do.

In this step-by-step guide, you'll learn how to set up your own private Docker registry on Linux. But first, let's take a closer look at Docker registries and the difference between public and private registries.

![step-by-step]({{site.images}}{{page.slug}}/step.png)\

## Prerequisites

To follow this guide, you will need the following:

- Two Ubuntu 22.04 servers. One for the Docker registry, and one to use as a client machine where you will push and pull images.

## Installing Docker and Docker Compose

First, you will need to install Docker and Docker Compose packages on both servers.

The Docker package is already included in the [Ubuntu](https://ubuntu.com/) default repository. However, it is a good idea to install the latest Docker version from their official repository.

Let's start by updating the existing package index.

~~~{.bash caption=">_"}
apt update -y
~~~

Next, you'll need to grab some dependencies to get packages over the secure HTTPS connection.

~~~{.bash caption=">_"}
apt install curl apt-transport-https ca-certificates  -y
~~~

Next, import the [GPG key](https://www.digitalocean.com/community/tutorials/how-to-use-gpg-to-encrypt-and-sign-messages) for Docker to install only authenticate package and add Docker's official repository to APT sources.

~~~{.bash caption=">_"}
echo "deb [arch=$(dpkg --print-architecture) \
signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] \
https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
| tee /etc/apt/sources.list.d/docker.list 
~~~

Since we've added a new software repository to apt, we'll need to update again.

~~~{.bash caption=">_"}
apt update -y
~~~

Finally, install the latest Docker and Docker Compose packages:

~~~{.bash caption=">_"}
apt install docker-ce docker-compose -y
~~~

This command will install both Docker and Docker Compose packages to your server, start the Docker service and enable it to start after the system reboot. You can verify the Docker installation by executing the command given below.

~~~{.bash caption=">_"}
docker --version
~~~

This will show you the Docker version.

<div class="wide">
![Verify Docker Installation]({{site.images}}{{page.slug}}/p1.png)
</div>

<div class="notice--info">
Remember, you'll need to run all of the above commands on both servers before moving on to the next step.
</div>

## Setting Up the Private Docker Registry

In this section, we will learn how to:

1. Create a Docker Compose file that will be used to configure the private registry.
2. Configure and secure NGINX to serve the registry server.
3. Set up basic authentication to ensure that only authorized users can access the registry server.

### Creating the Docker Compose File for the Docker Registry

We'll [use Docker Compose](/blog/youre-using-docker-compose-wrong) to define all the components required for setting up a private registry. Docker Compose makes it easy to define all the services we'll need as well as allow us to spin them all up with a single command.

Let's start by creating a directory to store all configurations for the private registry.

~~~{.bash caption=">_"}
mkdir ~/private-registry
mkdir ~/private-registry/registry-data
~~~

Next, change the directory to the `private-registry` directory and create a `docker-compose.yml` file.

~~~{.bash caption=">_"}
cd ~/private-registry
nano docker-compose.yml
~~~

Add the following section to define the `registry` service and set the registry `image` using the latest tag. The `image` directive downloads the latest version of the `registry`  Docker image from the Docker Hub public registry.

~~~{.yml caption="docker-compose.yml"}
version: '3'

services:
  registry:
    image: registry:latest
~~~

The Docker `registry` image is an official Docker image. It is essentially a server-side application that stores and distributes Docker images. It's going to do a lot of the heavy lifting for us.

Next, add the `port` section to map the host machine port `5000` to the container port `5000`.

~~~{.yml caption="docker-compose.yml"}
    ports:
    - "5000:5000"
~~~

Then, add the `environment` section where we will set up some environment variable related to some basic authentication.

Docker private registry supports several authentication methods, including, HTTP, OAuth, LDAP, and Active Directory authentication. Here, we will use basic HTTP authentication because it is simple and easy to implement. Specifically, we'll be using [htpasswd](https://httpd.apache.org/docs/current/programs/htpasswd.html), which is a utility that creates and manages user authentication credentials for basic HTTP authentication. We need to tell the Docker Registry to use htpasswd by setting the `REGISTRY_AUTH` variable.

We also need to set the `REGISTRY_AUTH_HTPASSWD_REALM` variable. Here we are setting it to Registry, but you can actually set it to whatever you want your users to use. When a user attempts to access a protected resource, such as our private Docker registry, their web client (e.g., a browser or a Docker client) will receive an authentication request from the server. This request includes the [realm](https://stackoverflow.com/questions/12701085/what-is-the-realm-in-basic-authentication) information. The realm serves as a prompt to inform the user which specific protected area they are trying to access and helps them understand why they need to provide credentials.

The last two variables we need to set up, `REGISTRY_AUTH_HTPASSWD_PATH` and `REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY` will tell our registry where to store passwords and where to store the actual images and image data.

~~~{.yml caption="docker-compose.yml"}
    environment:
      REGISTRY_AUTH: htpasswd
      REGISTRY_AUTH_HTPASSWD_REALM: Registry
      REGISTRY_AUTH_HTPASSWD_PATH: /auth/registry.password
      REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY: /registry-data
~~~

Next, add the `volumes` section to bind the `/auth` and `/registry-data` directories on the host file system to the container file system.

[Docker volumes](/blog/docker-volumes) play an important role to persist data in Docker containers and services. The `registry-data` volume will store all Docker images and registry configuration information while the `auth` volume will store and persist all user's passwords. Later, we'll also set up an HTTP authentication to ensure that only authenticated users can access the registry.

~~~{.yml caption="docker-compose.yml"}
    volumes:
      - ./auth:/auth
      - ./registry-data:/registry-data
~~~
  
When you are finished, your final configuration file will look something like this:

~~~{.yml caption="docker-compose.yml"}
version: '3'

services:
  registry:
    image: registry:latest
    ports:
    - "5000:5000"
    environment:
      REGISTRY_AUTH: htpasswd
      REGISTRY_AUTH_HTPASSWD_REALM: Registry
      REGISTRY_AUTH_HTPASSWD_PATH: /auth/registry.password
      REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY: /registry-data
    volumes:
      - ./auth:/auth
      - ./registry-data:/registry-data
~~~

Save the file when you are finished.

### Installing and Configuring NGINX for Docker Registry

NGINX is open-source and the most popular software that you can use as a web server and reverse proxy. The Docker registry container is accessible only from the local host. So we will need to install and configure [NGINX](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/) to forward traffic from the remote machine to the registry container running on port `5000`.

Let's start by installing the `nginx` and `apache2-utils` packages on your server. The `apache2-utils` package will download the `htpasswd` utility needed to set up basic HTTP authentication.

~~~{.bash caption=">_"}
apt install nginx apache2-utils -y
~~~

Now, create an NGINX virtual server block to serve the Docker registry. Basically, this is where we will define how NGINX should handle requests.

~~~{.bash caption=">_"}
nano /etc/nginx/conf.d/registry.conf
~~~

First, add the `listen` directive to specify the NGINX listening port. Next, define the `server_name` with your domain name. Finally, add the error and access log path.

~~~{ caption="registry.conf"}
server {
    listen 80;
    server_name private.linuxbuz.com;
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;
~~~

Next, in the `location /` section, set the `proxy_pass` directive to forward all incoming traffic on domain `private.linuxbuz.com` to the localhost on registry container port `5000`.

~~~{ caption="registry.conf"}
location / {
    if ($http_user_agent ~ "^(docker\/1\.(3|4|5(?!\.[0-9]-dev))|Go ).*$" ) {
    return 404;
    }

    proxy_pass http://localhost:5000;
    proxy_set_header Host $http_host; # required for docker client's sake
    proxy_set_header X-Real-IP $remote_addr; # pass on real client's IP
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_read_timeout 900;
    }
}
~~~

Your final NGINX configuration file will look something like this:

~~~{ caption="registry.conf"}
server {
    listen 80;
    server_name private.linuxbuz.com;
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;
    
location / {
    if ($http_user_agent ~ "^(docker\/1\.(3|4|5(?!\.[0-9]-dev))|Go ).*$" ) {
    return 404;
    }

    proxy_pass http://localhost:5000;
    proxy_set_header Host $http_host; # required for docker client's sake
    proxy_set_header X-Real-IP $remote_addr; # pass on real client's IP
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_read_timeout 900;
    }
}
~~~

Save the file when you are done.

Next, we'll need to define two more settings for NGINX.

- `client_max_body_size`: Sets the upload limit per file. By default, NGINX has an upload limit of 1 MB per file. To allow larger image upload to the Docker registry, you will need to define this value as per your requirement.

- `server_names_hash_bucket_size`: This directive is aligned to a size that is a multiple of the processor's cache line size. The default value of `server_names_hash_bucket_size` is `32` in NGINX. When you define a large server name then you will get the error `could not build the server_names_hash, you should increase server_names_hash_bucket_size: 32`

To update these, edit the NGINX main configuration file.

~~~{.bash caption=">_"}
nano /etc/nginx/nginx.conf
~~~

Define both directives below the line `http {`:

~~~{ caption="nginx.conf"}
client_max_body_size 4000m;
server_names_hash_bucket_size 64;
~~~

Restart the NGINX service to reload the changes.

~~~{.bash caption=">_"}
systemctl restart nginx
~~~

Run the following command to verify the NGINX running status.

~~~{.bash caption=">_"}
systemctl status nginx
~~~

You should see the NGINX running status in the below screenshot.

<div class="wide">
![Verify NGINX status]({{site.images}}{{page.slug}}/p2.png)
</div>

At this point, the NGINX web server is installed and configured to forward traffic to the private registry server.

### Setting Up SSL to Secure Docker Registry

SSL is an encryption security protocol that encrypts the sensitive information sent across the Internet. So adding an SSL certificate is necessary when hosting a registry server on the Internet to keep your images safe and secure. [Let's Encrypt SSL](https://letsencrypt.org/) is an open certificate authority that provides free SSL/TLS certificates to secure your registry server. The main reasons for using a Let's Encrypt SSL certificate are, it's free, automated, and provides an easier way to install and manage certificates.

First, install the [Certbot](https://certbot.eff.org/) Let's Encrypt client package to install and manage the SSL certificate.

~~~{.bash caption=">_"}
snap install --classic certbot
~~~

Next, copy the snap binary to the system path.

~~~{.bash caption=""}
ln -s /snap/bin/certbot /usr/bin/certbot
~~~

Then, run the `certbot` command followed by your domain name to download the SSL certificates, and configure NGINX to use the downloaded certificates for your domain.

~~~{.bash caption=">_"}
certbot --nginx -d private.linuxbuz.com
~~~

You will be asked to provide your real email address and accept the term of service to finish the SSL installation.

<div class="wide">
![Install SSL on registry domain]({{site.images}}{{page.slug}}/p8.png)
</div>

At this point, Let's Encrypt SSL is installed and configured for `private.linuxbuz.com` domain.

### Setting Up Authentication on Private Registry

Security is crucial if you are going to set up a private Docker registry for an enterprise environment. You can use HTTP authentication to secure your Docker registry and allow only eligible users to access it.

First, create an `auth` directory to store the password file.

~~~{.bash caption=">_"}
mkdir ~/private-registry/auth
~~~

Next, navigate to the `auth` directory and use the `htpasswd` command to create a `registry.password` file. The `htpasswd` is a utility used to create a file to store username and password information for Apache basic authentication.

~~~{.bash caption=">_"}
cd ~/private-registry/auth
htpasswd -Bc registry.password adminuser
~~~

You should be prompted to define a password as shown below.

<div class="wide">
![Create a registry user]({{site.images}}{{page.slug}}/p3.png)
</div>

At this point, password-based authentication is configured on the registry. We already defined this auth file when we set up the `REGISTRY_AUTH` in the docker compose. Now, only authenticated users can access the registry.

### Launching Docker Registry Container

Now that we have set up NGINX to route remote traffic to our registry over the secure SSL connection, and implemented authentication using htpasswd, we are finally ready to spin up the Docker registry container.

Let's run the below command to launch the registry container.

~~~{.bash caption=">_"}
cd ~/private-registry
docker compose up -d
~~~

This command will download the registry docker container image and start the container as shown below.

<div class="wide">
![Launch registry container]({{site.images}}{{page.slug}}/p4.png)
</div>

Run the following command to check the Docker registry container status.

~~~{.bash caption=">_"}
docker-compose ps
~~~

This will show you the active status of the registry container.

<div class="wide">
![Verify registry container]({{site.images}}{{page.slug}}/p5.png)
</div>

At this point, your private registry server is started and running.

## Creating a Custom Docker Image To Push To Our New Registry

Now, let's test our new registry by creating a custom docker image on the client server and pushing it to our newly created private registry. For demonstration, we will create a custom Ubuntu image with the NGINX server installed on it.

First, pull the latest Ubuntu image from the Docker Hub registry.

~~~{.bash caption=">_"}
docker pull ubuntu:latest
~~~

Then, run the container using the downloaded image.

~~~{.bash caption=">_"}
docker run -t -i ubuntu:latest /bin/bash
~~~

This will start the image and put you into the Ubuntu shell as shown below.

<div class="wide">
![Run Ubuntu Container]({{site.images}}{{page.slug}}/p6.png)
</div>

Next, update the Ubuntu repository and install the NGINX package inside the container.

~~~{.bash caption=">_"}
apt update -y
apt install nginx -y
~~~

Next, verify the NGINX version.

~~~{.bash caption=">_"}
nginx -v
~~~

You should see the NGINX version in the following output.

~~~{.bash caption=">_"}
nginx version: nginx/1.18.0 (Ubuntu)
~~~

Then, exit from the Ubuntu container.

~~~{.bash caption=">_"}
exit
~~~

Next, create a new image from the running Ubuntu container.

~~~{.bash caption=">_"}
docker commit $(docker ps -lq) ubuntu22-image
~~~

This will create a new custom image named `ubuntu22-image` on your client server.

You can verify the created image using the following command.

~~~{.bash caption=">_"}
docker images
~~~

You should see your newly created image in the following screenshot.

<div class="wide">
![Verify the custom image]({{site.images}}{{page.slug}}/p7.png)
</div>

At this point, you have created a custom image called `ubuntu22-image` on the client server.

## Publishing a Custom Docker Image to the Private Docker Registry

Now, you will need to upload this image from the client server to your private docker registry so that users can download and reuse it.

First, use the `docker login` command on the client server to log in to your private registry.

~~~{.bash caption=">_"}
docker login https://private.linuxbuz.com
~~~

We will need credentials that we set up on the registry server to authenticate the registry.
After successfully authenticating to the registry. You should see the following screen.

<div class="wide">
![Login to registry server]({{site.images}}{{page.slug}}/p9.png)
</div>

Next, tag your custom Ubuntu image that matches your registry server domain name.

~~~{.bash caption=">_"}
docker tag ubuntu22-image private.linuxbuz.com/ubuntu22-image
~~~

Next, verify the tagged image using the following command.

~~~{.bash caption=">_"}
docker images
~~~

<div class="wide">
![Verify tagged image]({{site.images}}{{page.slug}}/p10.png)
</div>

Finally, run the `docker push` command to upload your custom Ubuntu image to the private Docker Registry.

~~~{.bash caption=">_"}
docker push private.linuxbuz.com/ubuntu22-image
~~~

This will upload your custom image to the private registry server as shown below.

<div class="wide">
![Upload image to registry server]({{site.images}}{{page.slug}}/p11.png)
</div>

At this point, you have uploaded the custom Ubuntu image to your private registry server.

## Pulling a Docker Image from the Private Docker Registry

Now let's test out pulling images from the registry.

Again, make sure you log into your private registry using the `docker login` command.

~~~{.bash caption=">_"}
docker login https://private.linuxbuz.com
~~~

Next, pull the Ubuntu image from the private registry to your client server.

~~~{.bash caption=">_"}
docker pull private.linuxbuz.com/ubuntu22-image
~~~

After the successful download, you should see the following screen.

<div class="wide">
![Download image from registry server]({{site.images}}{{page.slug}}/p12.png)
</div>

Now, run the `docker run` command to create a container from the downloaded image.

~~~{.bash caption=">_"}
docker run -it private.linuxbuz.com/ubuntu22-image /bin/bash
~~~

This will start the container and put you into the container shell like before.

<div class="wide">
![Run custom ubuntu image]({{site.images}}{{page.slug}}/p13.png)
</div>

Now, verify the NGINX which you installed earlier.

~~~{.bash caption=">_"}
nginx -v
~~~

This will show you the NGINX version.

~~~{.bash caption=">_"}
nginx version: nginx/1.18.0 (Ubuntu)
~~~

Now, log out from the running container using the `exit` command.

~~~{.bash caption=">_"}
exit
~~~

## Conclusion

In this guide, we've covered how to establish a private Docker registry server on Linux, including setting up basic authentication, enabling SSL, creating a custom image, and verifying the registry server. Docker registry is crucial for secure image storage and management in modern software development.

With the knowledge you've gained today, you're now prepared to implement security best practices for Docker containers and images in an enterprise setting.

If you've enjoyed setting up your own Docker registry and are interested in further boosting your container build processes, take a peek at [Earthly](https://www.earthly.dev/). It's a tool that can help optimize your builds with its unique features like reproducible, portable, and parallel builds.

{% include_html cta/bottom-cta.html %}
