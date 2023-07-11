---
title: "Securing Grafana with HTTPS using Nginx and Certbot"
categories:
  - Tutorials
toc: true
author: Emediong Samuel
editor: Muhammad Badawy

internal-links:
 - Grafana
 - Security
 - HTTPS
 - Nginx
 - Certbot
 - Analytics
excerpt: |
    Learn how to secure your Grafana site with HTTPS using Nginx and Certbot in this comprehensive guide. Protect your sensitive data, establish trust, and enhance your website's reputation with HTTPS encryption and enhanced security.
---

**We're [Earthly.dev](https://earthly.dev/). We make building software simpler and therefore faster using containerization. If you want to know more about building in containers then [check us out](/).**

[Grafana](https://grafana.com/), a widely used open-source analytics and monitoring platform, has gained immense importance as an essential tool for tech companies and organizations globally. Its real-time [data visualization](https://www.tableau.com/learn/articles/data-visualization#:~:text=Data%20visualization%20is%20the%20graphical,outliers%2C%20and%20patterns%20in%20data.), querying, and analysis capabilities make it invaluable for monitoring system performance, network traffic, and other metrics.

However, Grafana's default setting comes without a secure connection, meaning that unauthorized parties may intercept and access sensitive data transmitted through Grafana. Fortunately, [Nginx](https://nginx.org/en/) and [Certbot](https://certbot.eff.org/pages/about) can help provide additional security measures beyond these defaults. Nginx acts as a reverse proxy while Certbot generates and installs an [SSL/TLS](https://www.cloudflare.com/learning/ssl/transport-layer-security-tls/) certificate, allowing for [HTTPS](https://www.thesslstore.com/blog/what-is-https-what-https-stands-for/#:~:text=What%20Does%20HTTPS%20Stand%20For%3F%20A%20Simple%20Definition%20and%20Explanation%20of%20What%20HTTPS%20Is) encryption and enhanced security.

In this article, I'll provide you with a comprehensive guide on how to secure your Grafana site with `HTTPS` using `Nginx` and `Certbot.` Let's dive right in!

## Why You Should Care About HTTPS Security

![An Http image]({{site.images}}{{page.slug}}/TrNLHGf.png)\

In today's digital landscape, the significance of HTTPS security cannot be overstated. Modern web browsers, including Google Chrome, have implemented warning messages that alert users when they attempt to visit sites lacking HTTPS encryption. This warning can discourage users from accessing the site altogether. Without HTTPS security, any data transmitted between your Grafana server and client, such as credentials, queries, usernames, and passwords, are sent in plain text. This means that it can be intercepted and read by malicious third parties.

HTTPS, on the other hand, encrypts the transmission of data between the user's browser and the web server. This encryption makes it challenging for hackers to intercept or manipulate the data, ensuring that sensitive information remains confidential and protected from unauthorized access. Moreover, HTTPS provides website authentication, enabling users to verify the legitimacy of the website they are interacting with. This plays a crucial role in preventing phishing attacks and other malicious activities that exploit user trust.

Furthermore, HTTPS has gained increasing importance for website ranking, as search engines now prioritize secure sites over non-secure ones. Implementing HTTPS safeguards your users' data, establishes trust, and enhances your website's reputation.

Now that you comprehend the significance of HTTPS security, let's delve into the practical aspects of implementing it in your Grafana setup.

## Installing and Configuring Grafana and Nginx

![Installing]({{site.images}}{{page.slug}}/installing.png)\

This section will guide you through the installation and configuration process of Nginx and Grafana and setting up a reverse proxy with Nginx.

Let's start by discussing Nginx. Nginx is an open-source web server and [reverse proxy](https://www.nginx.com/resources/glossary/reverse-proxy-server/#:~:text=A%20reverse%20proxy%20server%20is,traffic%20between%20clients%20and%20servers.) software that is renowned for its exceptional performance, stability, and capability to handle heavy traffic loads. While its primary function is to serve web content, it can also act as a reverse proxy. This means that Nginx can receive client requests, forward them to other servers or applications, and then deliver the response back to the client. Consequently, the client appears to be communicating directly with the proxy server.

Before proceeding, please ensure that you have the following prerequisites in place:

* A registered domain name: This is needed to complete the final steps of this guide. You can obtain one by registering with [NameCheap](https://www.namecheap.com/) or any domain registrar of your choice.
* Set up your server's `DNS` record: Add an `A` record for your_domain that points to your server's `public IP address`. This step ensures that your domain correctly resolves to your server.
* Lastly, an up-and-running Linux machine. For the purposes of this demonstration, we will be using Ubuntu.

If you have the prerequisites in order, you can proceed with the installation and configuration process.

### Step 1: Installing Nginx

Note: If you are using a different Linux distribution other than Ubuntu, [Link](https://nginx.org/en/linux_packages.html) to access the appropriate commands for your Linux distribution.

To begin, open your terminal and execute the following command to update your local package list and install Nginx:

~~~{.bash caption=">_"}
sudo apt-get update && sudo apt-get upgrade 
sudo apt-get install nginx
~~~

When prompted, press `Y` to confirm the installation and allow the update/upgrade process to proceed. This ensures that you have the latest software packages available. During the upgrade process, you may encounter prompts asking whether to restart certain services.

<div class="wide">
![A screenshot of an AWS Ubuntu server]({{site.images}}{{page.slug}}/FJF1WHN.png)
</div>

If such prompts appear, press `ENTER` to allow the default option, which will restart all the services listed in the prompt.

<div class="wide">
![An output screenshot after pressing `enter`]({{site.images}}{{page.slug}}/xkypavb.png)
</div>

Nginx and its required dependencies will be installed on your local machine. Once installation is complete, Nginx should already be up and running. To verify this, type the command:

~~~{.bash caption=">_"}
systemctl status nginx
~~~

You will see the `active (running)` message highlighted in green, indicating that the Nginx service is running successfully, as shown in the screenshot below.

<div class="wide">
![A screenshot of the Nginx service status]({{site.images}}{{page.slug}}/Cd3nakr.png)
</div>

However, a more reliable way to verify your Nginx installation is by requesting a page directly from Nginx. To do this, open your web browser and enter the URL `http://your_server_ip`, i.e. your server's public `IP address` or the associated `domain name` assigned to access your server. This is if you're using a server on a cloud platform. However, If you're implementing this on your local machine, you can use this command on your terminal:

~~~{.bash caption=">_"}
curl -4 icanhazip.com
~~~

**Note:** Your local machine only has a private IP address which is used for communication within your local network. The command above assigns you a public `IP address` by your internet service provider (ISP), which is used to identify your network on the internet, and is associated with your internet router or modem, not directly with your local machine.

You can also use a private browser window to access `http://your_server_ip` to avoid connection problems from previously cached data. If there are no glitches, you will see the **Welcome to Nginx** landing page, as shown below:

<div class="wide">
![A screenshot of the Nginx welcome page]({{site.images}}{{page.slug}}/nP6QGMF.png)
</div>

### Step 2: Adjust the Firewall Setting

After installing Nginx, it is best practice to verify the accessibility of your target port and make necessary adjustments if needed. Nginx uses `port 80` for `HTTP` traffic and `port 443` for `HTTPS` traffic. Since we are setting up a reverse proxy functionality, we need to allow incoming traffic on `port 80`. To achieve this, run the following command:

~~~{.bash caption=">_"}
sudo ufw enable
~~~

The `ufw` command is ubuntu-specific. It manages, enables, and activates the configured firewall rules, providing protection for the server by blocking unauthorized incoming connections.

Next, allow traffic to `port 80`

~~~{.bash caption=">_"}
sudo ufw allow 80
~~~

To verify the changes, use the command below:

~~~{.bash caption=">_"}
sudo ufw status
~~~

The output will display `port 80` as `allow Anywhere` and `allow Anywhere (v6), indicating that the`HTTP` functionality is established.

### Step 3: Installing Grafana

Not using Ubuntu Linux? Please check [guide](https://grafana.com/docs/grafana/latest/setup-grafana/installation/) for installation commands appropriate for your OS distribution.

For Ubuntu/Debian;

Download the Grafana `GPG key` with the `wget` command:

~~~{.bash caption=">_"}
wget -q -O - https://packages.grafana.com/gpg.key | \
gpg --dearmor | sudo tee /usr/share/keyrings/grafana.gpg > /dev/null
~~~

This command retrieves the Grafana [GPG key](https://www.goanywhere.com/blog/what-is-gpg), converts it to plain text, and saves it to the `/usr/share/keyrings/grafana.gpg` file with sudo privileges.

Next, add the [Grafana repository](https://packages.grafana.com/) to your [APT](https://wiki.debian.org/Apt) sources:

~~~{.bash caption=">_"}
echo "deb [signed-by=/usr/share/keyrings/grafana.gpg] \
https://packages.grafana.com/oss/deb stable main" | sudo \
tee -a /etc/apt/sources.list.d/grafana.list
~~~

Adding the Grafana `repository` to `APT sources` allows for seamless updates of Grafana packages. `APT` can automatically check and install the latest version of Grafana, ensuring access to new features, bug fixes, and security patches.

Update your package list and install Grafana:

~~~{.bash caption=">_"}
sudo apt-get update && sudo apt-get install grafana
~~~

Start the Grafana server using the `systemctl` command:

~~~{.bash caption=">_"}
sudo systemctl start grafana-server
~~~

Next, check the service status to ensure that your Grafana is active:

~~~{.bash caption=">_"}
sudo systemctl status grafana-server
~~~

You will see the `active (running)` status, as shown in the screenshot below.

<div class="wide">
![Screenshot of an active Grafana server]({{site.images}}{{page.slug}}/s4jw8iV.png)
</div>

Lastly, set up your Grafana service to start automatically upon boot.

~~~{.bash caption=">_"}
sudo systemctl enable grafana-server
~~~

The above command will generate an output showing that Grafana is now set to autostart upon boot using the symbolic link created by  `systemd`.

<div class="wide">
![An output of the systemctl autostart command]({{site.images}}{{page.slug}}/xwNXeQg.png)
</div>

Now that Grafana is successfully installed, the next step is establishing a reverse proxy.

### Step 4: Setting Up A Reverse Proxy

In many Linux distributions, including Ubuntu, Nginx comes with a default server block preconfigured to serve documents from the `/var/www/html` directory. However, for this setup, we will create a new directory within the `/var/www` directory specifically for your domain. In this example, we'll be using `/var/www/your_domain`. Remember to always replace `your_domain` with your actual domain.

To begin, execute the following command in your terminal to create the necessary directory:

~~~{.bash caption=">_"}
sudo mkdir /var/www/`your_domain`
~~~

On Ubuntu (and many other Linux distributions), Nginx typically uses the user account `www-data` by default for normal operation. This default user allows the Nginx process to access and serve content that the www-data user has permission for. This user exists by default in any Debian distribution like Ubuntu.

Then, granting ownership of the directory to the `www-data` user and group is important. This ensures that Nginx has proper access and permissions for reading and serving web files and directories to fulfill web requests.

~~~{.bash caption=">_"}
sudo chown -R www-data:www-data /var/www/`your_domain`
~~~

The `-R` option in the command above stands for `recursive.` When used with the `chown` command, the "-R" option instructs it to operate recursively on directories, meaning it will change the ownership of the specified directory and all its files and directories.

Now, let's proceed to modify the `default` Nginx configuration file. The `default` Nginx configuration file is one of the many `default` files provided by Nginx. In this case, we are modifying the " default " file in the `/etc/nginx/sites-available/` directory. We are choosing to modify this file because it serves as a base configuration for Nginx.

Open your preferred editor, for example, `vim` or `nano` and input the following command:  

~~~{.bash caption=">_"}
sudo nano /etc/nginx/sites-available/default
~~~

You can comment out or delete the existing configuration and replace it with the following code block:

~~~{.bash caption=">_"}
server {
    listen 80;
    server_name your_domain;

    location / {
        proxy_pass http://localhost:3000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
~~~

Let's go through each section of this default configuration file:

`server`: Defines the configuration for a specific server within Nginx.

`listen 80;`: Specifies that Nginx should listen on port 80 for incoming HTTP requests.

`server_name your_domain;`: Sets the server name or domain name for which the configuration applies.

`location / { ... }`: Handles requests that match the root location "/".

`proxy_pass http://localhost:3000/;`: Forwards requests to the backend server at <http://localhost:3000/>.

`proxy_set_header`: Sets additional headers to preserve client information in forwarded requests.

`Host $host;`: Sets the "Host" header to the original host requested by the client.

`X-Real-IP $remote_addr;`: Sets the "X-Real-IP" header to the client's IP address.

`X-Forwarded-For $proxy_add_x_forwarded_for;`: Sets the "X-Forwarded-For" header to a list of client IP addresses.

The above configuration is designed to establish a reverse proxy that forwards requests from `your_domain` to your Grafana instance running on `http://localhost:3000`. Remember to replace `your_domain` with your own domain.

Next, ensure that there are no syntax errors in your Nginx configuration file by typing the command:

~~~{.bash caption=">_"}
sudo nginx -t
~~~

If your file is error-free, restart `Nginx` to apply changes:

~~~{.bash caption=">_"}
sudo systemctl restart nginx
~~~

With these steps completed, Nginx is now set up to serve your `domain name`. To test this out, enter `your domain` name in your web browser by typing `http://your_domain.com`

<div class="wide">
![A screenshot of my domain routing to Grafana via Http]({{site.images}}{{page.slug}}/RXkmEwH.png)
</div>

### Step 5: Obtaining SSL/TLS Certificates with Certbot

An SSL/TLS certificate serves as a digital security protocol that protects the connections between your web browser, the websites you visit, and their servers. Its primary function is to encrypt the data exchanged during your online communication, guaranteeing both authenticity and privacy within a sophisticated cryptographic framework known as public key infrastructure [PKI](https://www.enisa.europa.eu/topics/incident-response/glossary/public-key-infrastructure-pki).

**PKI** relies on a certificate authority (CA) that validates the authenticity of a website's identity and the legitimacy of the browser connecting to it. This process ensures online security for businesses of all sizes, ranging from large tech companies to small online enterprises and individual users.

### Installing Certbots

Before proceeding, choosing the appropriate plugin that corresponds to your web server is important. [Certbot](https://certbot.eff.org/) provides a variety of plugins tailored to different web servers, including `Apache` and `Nginx.` This determines how Certbot interacts with your web server to acquire and configure certificates.

To begin, you'll need to install "Certbot" using the [`Snap`](https://ubuntu.com/core/services/guide/snaps-intro#:~:text=Snaps%20are%20a%20secure%20and%20scalable%20way%20to%20embed%20applications%20on%20Linux%20devices.%20A%20snap%20is%20an%20application%20containerised%20with%20all%20its%20dependencies.) package management system on your Linux server. This ensures you have the framework to effectively use Certbot and its plugins.

For Linux distributions different from `Ubuntu`, please check [this link](https://certbot.eff.org/instructions) to choose your web server type and operating system, then proceed with the command provided.

For Ubuntu/Debian:

Install the Certbot `snap` package:

~~~{.bash caption=">_"}
sudo apt install snapd
~~~

Next, update your package list, and enable `classic snap` support:

~~~{.bash caption=">_"}
sudo apt update && sudo snap install core; sudo snap refresh core
~~~

The above command fetches the latest version of each package and dependency installed on your system and installs the initial version of the `core snap package`, while the `snap refresh core` command refreshes it to ensure you have the latest updates, bug fixes, and security enhancements.

To ensure a clean installation, remove any old version of `certbot` packages if you have any. This will create a clean slate for the subsequent steps:

~~~{.bash caption=">_"}
sudo apt remove certbot
~~~

Next, install certbot

~~~{.bash caption=">_"}
sudo snap install --classic certbot
~~~

By enabling the `--classic` flag support, It installs the Certbot snap package in `classic mode`, allowing it to interact with the host system and perform tasks such as managing SSL/TLS certificates. The `--classic` "flag" is typically used for applications requiring deeper system integration.

<div class="wide">
![A screenshot of certbot successfully installed]({{site.images}}{{page.slug}}/WRA0hSo.png)
</div>

Afterward, create a symbolic link for certbot:

~~~{.bash caption=">_"}
sudo ln -s /snap/bin/certbot /usr/bin/certbot
~~~

By creating this symbolic link, you can run the `certbot` command from anywhere in the system by simply typing `certbot`, and the system will recognize it as a reference to the actual executable located at `/snap/bin/certbot`.

Now that `certbot` is installed, let's adjust the firewall settings to allow `HTTPS` traffic and remove any `HTTP` rule if earlier created:

~~~{.bash caption=">_"}
sudo ufw allow 'Nginx Full'
~~~

This command enables [UFW](https://wiki.ubuntu.com/UncomplicatedFirewall#:~:text=The%20Uncomplicated%20Firewall,and%20graphical%20frontends.) to open the required ports for Nginx, allowing external requests to reach your server and access your website via HTTP and HTTPS.

~~~{.bash caption=">_"}
sudo ufw delete allow 'Nginx HTTP'
~~~

This command removes any previously created firewall rule for HTTP, allowing you to utilize the full access of HTTP and HTTPS via the `Nginx Full` command.

Next, run the following command to fetch an SSL/TLS certificate for your domain.

~~~{.bash caption=">_"}
sudo certbot --nginx -d `your_domain`
~~~

Certbot will automatically identify your Nginx server configuration and prompt you to provide your email address for urgent renewal and security notices. Make sure to review and agree to Certbot's terms of service presented during this step.

<div class="wide">
![Deploying SSL Certificate]({{site.images}}{{page.slug}}/OMPOKXZ.png)
</div>
<div class="wide">
![Deploying SSL Certificate]({{site.images}}{{page.slug}}/2DakRiS.png)
</div>

The screenshots above show that the SSL/TLS certificate for the domain `emediong.xyz` was successfully obtained using Certbot.

### Step 6: Testing HTTPS Protection

Now that your HTTPS connection is set up, it's time to test it. Open your web browser and enter your domain, but this time use the `HTTPS` protocol:

~~~{.bash caption=">_"}
https://your_domain.com
~~~

To ensure a smooth connection, using a private browser window is recommended as it provides you with a clean slate, and any potential conflicts or connection issues caused by cached data or stored cookies are avoided. ,

When successfully access Grafana, you will notice a black padlock icon in the top left corner of your browser's address bar. This icon signifies that your site is now HTTPS-secured.

<div class="wide">
![Screenshot of a secured Grafana website]({{site.images}}{{page.slug}}/BUb7VJr.png)
</div>

From here, enter `admin`  as both the `Email/username` and `Password` to log in, then proceed to set up your desired password to enhance the security of your account. When these steps are completed, you will be logged into Grafana, where you can view your dashboard and everything else.

## Conclusion

In this article, you have gained valuable insights into the importance of enabling HTTPS protection for Grafana and all websites. A comprehensive step-by-step guide has been provided, outlining the process to achieve this security measure.

The importance of HTTPS cannot be overstated, particularly in today's ever-evolving digital landscape. With a surge in cyber threats and a heightened focus on safeguarding data privacy, it has become imperative to prioritize the security of applications like Grafana. Through the implementation of HTTPS, organizations, and individuals can effectively demonstrate their commitment to protecting sensitive data and cultivating a secure environment for users.

For more articles similar to this one, stay in the loop, [Earthly.dev](https://earthly.dev/blog/) is a valuable resource to explore.

{% include_html cta/bottom-cta.html %}
