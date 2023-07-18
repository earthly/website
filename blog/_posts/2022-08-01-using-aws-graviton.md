---
title: "Using AWS Graviton"
categories:
  - Tutorials
toc: true
author: Kealan Parr

internal-links:
 - Amazon
 - AWS
 - EC2
excerpt: |
    Learn about AWS Graviton, a type of processor made by Amazon, and discover its benefits, use cases, and how to deploy applications on it. Find out how Graviton processors offer strong performance, extensive software support, improved security, and the best performance per watt of energy use in Amazon EC2.
---
**We're [Earthly](https://earthly.dev/). We simplify and speed up software builds using containerization. Earthly could be the tool to streamline your CI/CD pipelines. [Give it a try](/).**

[Amazon Web Services (AWS)](https://aws.amazon.com/) is one of the most popular—and comprehensive—cloud service providers. It has over [200 fully-featured services](https://aws.amazon.com/what-is-aws/) on offer. There are enough services that it can be hard to remember them all.

One of these offerings is [Graviton](https://aws.amazon.com/ec2/graviton/), a type of processor made by Amazon. Graviton, released in 2018, [was the first release](https://www.cloudzero.com/blog/aws-graviton), and Graviton2, [released in 2019](https://en.wikichip.org/wiki/annapurna_labs/alpine/alc12b00), is the current primary publicly available offering. [Amazon Elastic Compute Cloud (Amazon EC2) C7g](https://aws.amazon.com/ec2/instance-types/c7g/) instances are currently [powered by Graviton3 processors](https://aws.amazon.com/blogs/aws/new-amazon-ec2-c7g-instances-powered-by-aws-graviton3-processors/) and are newly available for all AWS customers.

In this article, you'll learn more about AWS Graviton, including the AWS services that run on Graviton, some of Graviton's use cases, and the benefits and downsides of using Graviton. You'll also look at how to deploy an application on AWS Graviton.

## What Is Graviton

AWS Graviton processors are ARM-based processors that power a host of cloud services. They were specifically designed to deliver the most efficient performance for your money. They power a [host of services](https://aws.amazon.com/ec2/graviton/) like the following:

- Amazon [EC2](/blog/build-your-own-ngrok-clone)
- Amazon ElastiCache
- Amazon Elastic Kubernetes Service (Amazon EKS)
- Amazon Aurora
- Amazon Relational Database Service (RDS)
- Amazon MemoryDB for Redis
- Amazon OpenSearch
- Amazon EMR
- AWS [Lambda](/blog/aws-lambda-node)

Amazon created the Graviton processors when [they discovered](https://thenewstack.io/aws-graviton-marks-the-emergence-of-arm-for-cloud-native-workloads/) that a large number of Amazon EC2 customers weren't using their full EC2 capabilities.

When they spoke to their customers, from small and large companies alike, they discovered that many of their clients felt the current [X86-64](https://www.techtarget.com/whatis/definition/x86-64) architecture was overkill for their use cases. After this discovery, Amazon decided to offer an alternate processor architecture, in part to offer consumers more choice, especially for companies where a smaller CPU would be sufficient to power their infrastructure. Their new processors are powerful due to their [transistor density](https://en.wikipedia.org/wiki/Transistor_count) but require less power than their predecessors. According to Andy Jassy, CEO of Amazon, [these changes](https://www.zdnet.com/article/aws-graviton2-what-it-means-for-arm-in-the-data-center-cloud-enterprise-aws/) have resulted in a forty percent greater performance, and twenty percent less power consumed when compared to an x86-based processor.

## Benefits of Graviton

![Benefits]({{site.images}}{{page.slug}}/benefits.jpg)\

Graviton offers a number of benefits in a variety of applications, including strong performance, good security practices, and excellent software integrations.

### Best Performance per Dollar

Graviton processors are used on more than one instance type. There are different types of instances, each optimized for different use cases. The types are as follows:

- **[General purpose](https://aws.amazon.com/ec2/instance-types/m6g/):** made for microservices and small-to-medium databases.
- **[Compute optimized](https://aws.amazon.com/ec2/instance-types/c7g/):** made for compute-intensive applications, such as video encoding, gaming, and [HPC](https://en.wikipedia.org/wiki/High-performance_computing).
- **[Memory optimized](https://aws.amazon.com/ec2/instance-types/r6g/):** made for in-memory caches, open source databases, and real-time analytics.
- **[Storage optimized](https://aws.amazon.com/ec2/instance-types/i4g/):** made for NoSQL databases, search engines, and streaming.
- **[Accelerated computing](https://aws.amazon.com/ec2/instance-types/g5g/):** made for machine learning interfaces and graphics applications.

If you were to spend $1 USD across multiple different processor architectures, Graviton processors would deliver roughly [forty percent](https://aws.amazon.com/ec2/graviton) more bang for your buck when compared to current-generation x86-based instances.

This performance is calculated by looking at the compute power the processors offer per watt of energy consumed—and Graviton processors are extremely efficient. This means that you use less computing power for the same tasks, making your workloads more cost-effective.

### Extensive Software Support

Graviton processors are supported by many Linux distributions, such as Amazon Linux 2, Red Hat Enterprise Linux, SUSE, and Ubuntu. In addition to the operating system support, many applications are also supported, ensuring you can use Graviton processors for whatever task you need them to perform.

As long as your code hasn't been built and architected exclusively for x86 architecture, Graviton most likely will run it.

### Improved Security

![Security]({{site.images}}{{page.slug}}/security.jpg)\

Graviton processors have a rich feature set that focuses heavily on security and elasticity. This is done by building Graviton on top of the [Nitro chip](https://aws.amazon.com/ec2/nitro/). This ensures security features like the following:

- Always-on memory encryption
- Dedicated caches for every vCPU
- Support for pointer authentication

Graviton not only offers performance but ensures the cloud workflows you run are secure by default, too.

### Best Performance per Watt of Energy Use in Amazon EC2

Graviton3 architecture uses up to sixty percent less energy on a comparably specced EC2 instance, helping customers reduce their cost and their carbon footprint. Most excitingly, each new Graviton generation so far has come out with better features each time, making them safer and more performant with each new release.

Graviton2 offered [significant improvements](https://www.justaftermidnight247.com/insights/everything-you-need-to-know-about-aws-graviton2/) over the first Graviton offering, boasting substantial performance gains, caches twice as fast as the original, quadruple the compute cores, and five times faster memory.

## Deploying on AWS Graviton

![Deployment]({{site.images}}{{page.slug}}/deployment.png)\

It's worth noting that ARM-based processor architecture isn't compatible with everything. Windows out of the box won't work on it, for example. You'll have to check if your particular use case will work natively on ARM-based architecture. If it won't, you'll need to either migrate it to ARM or see if you can rework your solution.

In this example, you're going to deploy a basic "hello world!" program onto an EC2 instance running Graviton-based architecture.

### Prerequisites

To follow along with this tutorial, you'll need to have a basic grasp of cloud principles as well as an understanding of [Go](https://go.dev/). This will be enough to create an EC2 instance and use it to run [Golang](/blog/top-3-resources-to-learn-golang-in-2021) code, which will run on Graviton architecture.

Graviton processors are only available in [certain regions](https://aws.amazon.com/ec2/graviton), so you may need to change which region you access AWS in.

Before starting, it's important to note that **Graviton instances are not included in the free usage tier**, so you'll incur costs in following this tutorial. Running an instance for a few minutes will cost very little, but it's important to remember to remove this instance once you're done with it to prevent charges from accruing.

### Deploying With Graviton

Go to the AWS Management platform and navigate to **EC2**. The user interface will look something like this:

<div class="wide">

![EC2 Dashboard]({{site.images}}{{page.slug}}/h33nlgS.png)
</div>

Open the **Instances** menu and click **Instances**, highlighted in yellow in the previous picture. This will launch your EC2 instance.

Click the orange button at the top right of the screen that says **Launch instances**:

<div class="wide">

![Launch instances]({{site.images}}{{page.slug}}/DHSQRdB.png)
</div>

Next, you need to change the **Architecture** drop-down to be **64-bit (Arm)**, after which the **Instance Type** drop-down will allow you to pick instances that run Graviton. This is a crucial step for launching an EC2 instance that's specifically running Graviton ARM architecture. Some of the instances running Graviton are as follows:

- m6g
- m6gd
- c7g
- c6gd
- c6gn
- c6G
- r6G
- t4G

If you need an exhaustive list, you can find one on this [YouTube tutorial](https://youtu.be/kAg7U2I2hzQ?t=1974).

You will also need to configure how accessible your EC2 instance will be. For simplicity's sake, this tutorial will be configured to allow access from anywhere. This can be done by allowing SSH traffic from 0.0.0.0/0, which will allow all connections:
<div class="wide">

![Image showing SSH access set to 0.0.0.0/0]({{site.images}}{{page.slug}}/yNxrmhn.png)\
</div>

In order to log in and SSH into your box, you'll need to ensure you have a key pair name. If you don't have one, then create one, as shown in the following UI:

<div class="wide">

![Login for key pair shown]({{site.images}}{{page.slug}}/8HZ4E2e.png)\
</div>

To generate this, go to the **Key pair (login)** header on your AWS UI and click **Create new key pair**:

<div class="wide">

![Login generation]({{site.images}}{{page.slug}}/ceRFkFU.png)
</div>

This essentially downloads a private key to uniquely identify you on the terminal. Make a note of the download location and make sure it's somewhere you can easily access.

Once this is complete, you can click **Launch instances** and start running the instance.

Open a terminal in the directory where you saved your private key. To ensure your key is not publicly accessible, run the following command:

~~~{.bash caption=">_"}
chmod 400 hello.pem
~~~

You can track the status of your instance from your AWS EC2 instances dashboard underneath the **Instance state** header. Once your instance moves from initializing to running, you'll be able to access it:

~~~{.bash caption=">_"}
ssh -i "hello.pem" ec2-user@ec2-184-72-90-10.compute-1.amazonaws.com
~~~

In the previous command, you will need to change `ec2-user@ec2-184-72-90-10.compute-1.amazonaws.com` to your EC2 Public DNS instance, found by going to the instance **Details**, then locate the **Public IPv4 DNS**, as shown subsequently:

<div class="wide">

![EC2 Public DNS]({{site.images}}{{page.slug}}/2VJwTbz.png)
</div>

Now that you can access your EC2 instance, you'll run two commands. The first is to ensure that Go is installed into the machine, and the second is to update the instance:

~~~{.bash caption=">_"}
sudo yum update -y
~~~

~~~{.bash caption=">_"}
sudo yum install -y golang
~~~

These commands will also create the environment variables you need.

Create a Go file by running `touch app.go` and then `vi app.go`, which will use [Vim](https://www.vim.org/) to edit your file.

Insert the following "hello world!" application into the `app.go` file:

~~~{.go caption="app.go"}
package main

import "fmt"

func main() {
 fmt.Println("hello world!")
}
~~~

Pressing **Esc** will allow you to escape Vim's command mode; then type `:wq` to save and exit your folder. The final command you need to run is `go run app.go`.

`go run app.go` will simply compile your code and execute it as a binary, which will run the code you just wrote.

If you've followed along, then you've just deployed a Go application to a Graviton EC2 instance, and you should see "hello world!" displayed in the terminal:

<div class="wide">

!["hello world!" displayed in the EC2 shell]({{site.images}}{{page.slug}}/HrybAr1.png)\
</div>

## Conclusion

In this guide, we've explored the Graviton processor architecture, its common applications, the services it supports, and its pros and cons. We've also walked through deploying an app on a Graviton EC2 instance. Its high performance and energy-efficiency make Graviton a versatile choice for any cloud workflow.

Looking to streamline your cloud workflow even further? Give [Earthly](https://www.earthly.dev/), the build automation tool, a try! It can complement your Graviton-powered applications by simplifying cross architecture builds.

No matter your company's size, combining the power of Graviton with the efficiency of Earthly can offer significant savings and improvements in your development pipeline.

{% include_html cta/bottom-cta.html %}
