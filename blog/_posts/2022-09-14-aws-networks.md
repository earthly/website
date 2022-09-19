---
title: "Introduction to Networking the AWS Way."
categories:
  - Tutorials
toc: true
author: Josh

internal-links:
 - just an example
---

When you create an AWS account a lot of resources get created for you by default. This is great if you want to get started quickly. The infrastructure is already in place for you to set up an instance, lambda, or api gateway. But what exactly is all this stuff that gets created? If your not someone who is super familiar with networking, it can be a little overwhelming. So in this tutorial we'll create all these resources from scratch. The actual thing we will accomplish is pretty simple: deploy a webserver on an ubuntu machine. You could do this in about 5 minutes using the AWS defaults. But in order to better understand what they are and what they do, we'll create them ourselves.

This article is for people who want to know more about setting up a cloud network, and how networks work in general. Yes, we will be using AWS as our cloud platform, but I’m coming to this as someone who knows very little about setting up a network. I don’t have a complicated home network and a lot of my experience working with AWS was in networks that were already set up.

Our goals for today will be to set up a network with two subnets. One subnet will be accessible from the internet and the other will not. We’ll deploy a static web page in the first subnet and a database in the second. We’ll take a look at some security measuers and hopeuflly get a better understanding of IP addresses, networks, subnets, subnet masks etc.

To follow along you’ll need to set up an AWS account.

## Regions and Availability Zones

These ideas are going to come up a few times as we create our network. AWS is split up into [Regions and Availability Zones](https://aws.amazon.com/about-aws/global-infrastructure/?p=ngi&loc=1). So what does that mean? Regions are large areas geographical areas. They have names like US East, US West, Asian Pacific East, Asian Pacific West. There's one in Canada and one in South America and many more around the world. Within those regions are the actually data centers where your AWS services run. There are multiple data centers within each region. These data centers are called Availability Zones.

This is part of the power of using AWS because when you deploy something like, say, a Database, you can deploy it across multiple availability zones. This ensures that if something were to happen at one data center, your data would be still be safe at the other one. It's also helpful if you have clients accessing your services from different parts of the country, or the world, because it allows you to deploy close to where your users are.

## VPCs
Ok, we are getting very close to actually being able to create something. To start, we'll create a VPC.

A VPC is your Virtual Private Cloud. It’s basically your own private network on AWS. Diagrams of cloud networks tend to just look like a bunch of boxes inside of other boxes. Here’s one.

This is helpful, especially when we start to think about communication. That’s really what a network is all about, different devices and services talking to each other.

We can start by thinking about the pieces of our network as boxes. The main box is AWS. AWS runs the actual hardware and data centers where our applications will run. Within AWS you start by creating a VPC. This is a private network within AWS and it's the main box all of your other boxes will go into. Every other AWS resource your create will live inside of a VPC. You can have multiple VPCs within AWS but we'll just be working with one in this tutorial.

When a user creates a VPC they can run any number of services inside it. We can think of this as the main container we get to work with.

## Creating A New VPC

Let's start by creating our first VPC.

Sign into your AWS console. In the upper right, you should be able to see which region you are in. Navigate to the VPC service.

{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/vpc-home.png --alt {{VPC Dashboard }} %}
<figcaption>The Main VPC Dashboard</figcaption>

In the image above, you can see I already have some VPCs, subnets, and route tables created. When you first create an AWS account, Amazon will automatically set up a VPC for you in every region. These default VPCs come with a lot of the things you'll need to get going right away, including CIDR ranges, subnets, routers, and security groups. If some or all of those are new to you don't worry, we are going to ignore the default VPC and create everything from scratch for this tutorial.

Click the button in the upper left that says `Create VPC`. There's an option `VPC and more` that will walk you through creating your VPC, subnets, routers etc all at once. This is a great tool to get set up quickly, but for learning purposes, we are going to skip out on doing it the easy way and just select `VPC only`.

{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/vpc-only.png --alt {{VPC Create Options}} %}

First thing we need to do is name our VPC. Instead of picking something lame like `test-vpc-one` or `my-vpc`, let's call it `the-greatest-vpc-of-all-time`.

Next we'll need to define an IPv4 CIDR range. CIDR ranges could be an article all on their own. I've provided a quick explination below, along with more resources if you really want to dive in. The quick version is that this is the range of IP addresses that will be aviable to us on our network. We'll be able to assign addresses from that range to the services we create in the VPC. Note that these are all internal IPs, meaning they won't be accessible outside of the VPC. For that, we'll need to create something else which we will get to later.

For now, we are going to use the same CIDR range that AWS would have given us if we'd used default VPC: `172.31.0.0/16`. This uses a range called RFC 1918, which is not used on the internet, so there's no chance any of our internal network addresses will conflict with one's on the internet. The `/16` means we'll have 65,536 IP addresses to use on our VPC. More than enough.

That's all we'll need to do for this section. Click `Create VPC` and we're done.

{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/vpc-home.png --alt {{VPC Attributes}} %}
<figcaption>Our New VPC</figcaption>

<div class="notice--big--primary">

## On CIDR Notation

When we define a network, we need to define a range of IP addresses that devices on that network can use to identify themselves and talk to other devices on the network. 
IP addresses. Four numbers, each one is called an octet because it represents an 8 bit value. 8 bits means each number can range in value from 0 - 255. So 0.0.0.0 to 255.255.255.255

Ip addresses actually represent 2 pieces of information. The address for the device, but also the address for the device the network is on.

CIDR blocks are internal IP ranges. A notation for multiple address. The /  number is how many binary numbers can be fixed.
The number after the slash is important, but to understand how, we need to think about our ip address as a binary number. 
First two numbers represent the network. Last two, the device. Subnet masks are for telling us which part of the ip is for the network and which is for the host. 1 is network 0 is host.

An Ip address is made up of 4 numbers seperated by dots. Each number can be a value between 0 and 255. In binary, we can express an ip address with 32 digits like this. Say we wanted to have the max, which is 255.255.255.255.

11111111.11111111.11111111.11111111

Ok, so back to the number after the /. That number can be between 1 and 32 and it tells us how many of the 32 binary digits should be fixed numbers - numbers that will always be the same. This is helpful when we want to express a range of IPs. 

So if we say, 192.168.0.1/24 we are saying I want to create a a range of ips and I want 24 of the numbers (thinking in binary now) to but unchangeable.

If you want to truly understand CIDR ranges [this video](https://www.youtube.com/watch?v=v8aYhOxZuNg) and [this article](https://www.digitalocean.com/community/tutorials/understanding-ip-addresses-subnets-and-cidr-notation-for-networking) are great places to start. 

</div>

Creating
  - VPC Actions - edit DNS host names - Enable. We will need this dns host name so we can ssh into our instance later.

  RFC 1918 range
  172.31.0.0/16 - first 2 numbers are network, rest are for devices.
  172.31.0.0/24 - diffence here is that the 0 counts as part of the network address
  172.31.1.0/24

## Subnets

Subnets are the next container we need to create. The services we want to create today can't be deployed directly into the VPC. We first need to divide the VPC into subnets. These are subsets of the IP CIDR range we set up earlier. Subnets allow us to group things in our network, which makes communication and security easier to deal with. In our case, we'll use subnets to help us control access to the outside internet. We'll need to deploy our webserver into a subnet that can reach the Internet, but we'll want our database in a separate subnet that is block off from the Internet. 

In the left hand menu, under the Virtual Private Cloud section, select `subnets`. This will bring you to a list of all the subnets that exist in your selected region. Remember, AWS created a default VPC for you when you created an account, so you should see a few subnets that exist in that default VPC. For now we can ignore those.

In the upper right click `Create subnet`. The first thing it will ask for is the VPC you want your new subnet to live in. Select the one we just created. 

Below that there will be a section where we can configure settings for our new subnet. This first subnet will be where we put our webserver, so let's call it `webserver-subnet` to make it easy to keep track of.

Next we need to choose which Availability Zone our subnet should live it. Remember, VPCs take up entire regions. Within the VPC we have many subnets that each live in an Availability Zone. We can choose where to put the subnet, or let AWS randomly choose. For our purposes it doesn't really matter. The main point here is knowing that a subnet has a specific AZ.

Last thing we need to do is set up a CIDR range for the Subnet. This is needs to be a subset of IPs we set up for the entire VPC. In this case we will use `172.31.0.0/24`.

Once your done click `Create Subnet`.

## Creating an EC2 Instance

Ok, so so far we've just been clicking buttons in the AWS UI, which isn't very exciting. Now, we finally get to create something a little more tangible, an actual [EC2 instance](https://aws.amazon.com/ec2/). An Amazon Elastic Compute Cloud (EC2) instance is a virtual machine we can deploy into a subnet. Basically, this is the computer we want to add to our network. We'll use this machine to run an nginx server that will be accessible from the Internet. 

In the search bar in the top menu search for EC2.

{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/search-for-ec2.png --alt {{Navigate to EC2 Dashboard }} %}
<figcaption>Search for EC2</figcaption>

On the next page select `Instances` from the side menu. This is where you'll find a list of all EC2 instances running in your current region. If you're working with a new account you won't see any instances running. In the upper right corner click `Launch instances`. This will take you to a page where you can configure your virtual machine.

### Name and OS

Give your instance a name and then under Application and OS Images you can select an OS to to use on your instance. I'll be using Ubuntu for this tutorial.

{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/os-versions.png --alt {{OS and Version for Instance}} %}
<figcaption>Select Your OS and Version</figcaption>

For version I used Ubuntu Server 22.04.

Instance Type doesn't really matter here since we won't be doing much with this beyond installing nginx. I chose `t2.micro` because it's part of the Free Tier. 

### Key pair
We'll need to create a key pair so we can ssh into the EC2 instance and install nginx. After you click create pair you'll automatically download the key. Make note of it's location because we will need it later.

{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/key-pair.png --alt {{ Key Pair}} %}
<figcaption>Create a key pair so we can access the instance later.</figcaption>

### Network Settings 

For me, AWS set the VPC for my instance as the default VPC. To change it to the `the-greatest-vpc-of-all-time` click edit in the upper right corner of the networking section. 

{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/edit-vpc-ec2.png --alt {{ Edit VPC }} %}
<figcaption>Make sure we are using the correct vpc.</figcaption>

Now you should be able to edit the VPC and choose the one we just created. From there you can also edit the subnet. We only have one right now so we don't have a choice. 

Auto assign public IP.

### Security Groups

Let's pause for a second and discuss security groups. Security groups are your firewall for your network. They allow you to set up rules about which traffic is allowed to enter and exit the network and under what circumstances. After you set up these rules, you can reuse them by adding more instances to each security group.

So back in our instance creation, we need to select a security group. We don't have any yet in this VPC, so we can create one. We need to add three rules for our security group. 

1. SSH - so we can access the machine and install nginx. 
2. HTTP - For web traffic
3. HTTPS - Also for web traffic

Luckily AWS already has some presets that will help us out. You can add rules with the `Add security group rule` button at the bottom. For source type for each one you can select `Anywhere`. This is standard for HTTP and HTTPS since you generally want to allow traffic from anywhere to your website. (You have the option of black listing IPs in the future if you need to to.) For SSH you probably do not want to leave it open to anyone, but for testing purposes we won't worry about it.

Your instance will take a minute or two to launch. You can check the status by returning to the EC2 Dashboard and clicking on Instances (running).

{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/running-instance.png --alt {{ Instance Status}} %}
<figcaption>Instance status</figcaption>

## Internet Gateway 

The Internet Gateway is what gives your VPC a tunnel to the internet. Without one, traffic is limited to within the VPC. Go to your VPCs dashboard. In the menu on the left, click on Internet Gateways. Then in the upper right click Create internet gateway. All we need to do here is give our gateway a name.

{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/gateway.png --alt {{ Create an Internet Gateway }} %}
<figcaption>Create an internet gateway to allow access to the internet</figcaption>

## Route Table
Now that we have the gateway created we need one last thing before we can access our EC2 instance, a route table. The gateway allows us access to the interent, the route table is what says which traffic can go where. Every subnet you create within a VPC will need to be associated with a route table. 

You should see Route Tables in the left hand menu. Click it and you'll be taken to the dashboard for the route tables. There will be some default tables created already, but let's create a new one. Click create route table in the upper left. Give your route-table a name and make sure you associate it with the correct VPC. 

{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/route-table.png --alt {{ Create an route table }} %}
<figcaption>Create an route table </figcaption>

## Something Might go Here about the route table connecting to the subnet

## Connecting to our new EC2 instance

Now, finally, we should have be able to access the EC2 instance. Back on the dashboard for your instance, locate the public ipv4 address.

{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/ipv4-address.png --alt {{ Your instance IP}} %}
<figcaption>Copy the IP address for the instance </figcaption>


In your terminal, use the pem key to ssh into the running instance using the following command `ssh -v <path-to-key>/web-server-key-pair.pem ubuntu@<ip-address-for-your-instance>`

```bash
ssh -i Downloads/web-server-key-pair.pem ubuntu@54.159.44.62
```
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/ubuntu.png --alt {{ Connected to Ubuntu Server}} %}
<figcaption>Success! We've connected to our Ubuntu server </figcaption>

<div class="notice--info">

### WARNING: UNPROTECTED PRIVATE KEY FILE!

If you get an error: `WARNING: UNPROTECTED PRIVATE KEY FILE!`, you'll need to update the permissions on the pem key. 

```bash
chmod 400  <path-to-key>/web-server-key-pair.pem
```
Then try ssh again.
</div>

### Nginx

Connecting Via ssh proves our instance is reachable from the internet. Hurray!! Just to take it one step further, let's confirm that HTTP is working by installing nginx and connecting via a web browser. Nginx is a lightweight webserver that is super easy to install and set up. While you are still connected to the EC2 instance run:

```bash
sudo apt update
sudo apt install nginx
```
That's it. No more setup is needed. Now, copy and paste the same IP address into your browser and you should see the nginx welcome page returned. 

{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/ubuntu.png --alt {{ Nginx Welcome Page }} %}
<figcaption>Our new server is returning the nginx welcome page </figcaption>

## Conclusion 

Again I want to point out that everything we've done so far is what AWS gives you for free with the default VPCs it sets up in each region, and you are fine to use those resources out of the box. I for one love when things are done for me, but hate not knowing how things are done. It's a real personal problem. Anyway, I hope this helped you better understand some of the basic networking concepts in AWS.


### Writing Article Checklist

- [ ] Write Outline
- [ ] Write Draft
- [ ] Fix Grammarly Errors
- [ ] Read out loud
- [ ] Write 5 or more titles and pick the best on
- [ ] First two paragraphs: What's it about? Why listen to you?
- [ ] Create header image in Canva
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
- [ ] Run mark down linter (`lint`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `link-opp` and find 1-5 places to incorporate links to other articles
- [ ] Add Earthly `CTA` at bottom `{% include cta/cta1.html %}`
- [ ] Raise PR
