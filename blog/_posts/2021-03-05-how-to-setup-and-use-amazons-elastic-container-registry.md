---
title: How to Setup and Use Amazon's Elastic Container Registry
toc: true
categories:
  - Tutorials
author: Vivek Sonar
sidebar:
  nav: "docker"
internal-links:
  - ecr
  - amazon elastic container registry
  - container registry
  - ecs
  - eks
excerpt: |
    Learn how to setup and use Amazon's Elastic Container Registry (ECR) to store and manage your container images. Discover the benefits of using ECR over Docker Hub and how it integrates with other AWS services like IAM, EKS, and ECS.
---
**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. If you're setting up and using Amazon's ECR, using Earthly to build your containers could really enhance your workflow. [Check it out](/).**

A container is a simple unit that packages all your code and its dependencies so your application can run quickly and reliably from any computing environment. That means you could quickly move from your local environment to your staging and into production. Due to their portability, small size, and convenience, containers are becoming [a method of choice](https://www.cio.com/article/3434010/more-enterprises-are-using-containers-here-s-why.html) for shipping modern applications.

Containers are created from a read-only template called an *Image*. These images need to be stored somewhere so they can be retrieved by any machine authorized to use them. That's where a container registry comes in.

## Docker Hub: Where Many Start

[Docker](https://www.docker.com/) is one of the most well-known pieces of software for working with containerized applications. To help with the storage issue, Docker created [Docker Hub](https://hub.docker.com/) - the world's largest container registry - where developers can share and download pre-built images from others.

While Docker Hub is still the most common option, it's lost a bit of steam since the company started restricting free public repositories to just [a few hundred pulls every 6 hours](https://cloudonaut.io/amazon-ecr-vs-docker-hub-vs-github-container-registry/). Docker Hub also offers some of the same features that ECR does (image scanning, team access) to paid users, but it's likely to be much more expensive than Amazon ECR is when you're starting out.

Finally, the free Docker Hub plan has added a restrictive retention policy. They will delete any container images that haven't been accessed within the last six months, so if you're using Docker Hub for your side project that you update only occasionally, you might be surprised to find it suddenly gone one day.

## Introducing Amazon Elastic Container Registry (ECR)

Amazon ECR is a fully managed container registry offered as part of the AWS suite. Like Docker Hub, it makes storing, sharing, managing, and deploying your images easier, but it's also likely to save you money - especially if you're already using AWS. Simply push your images to ECR and pull the images using container management tool: [Kubernetes](https://kubernetes.io/), [Docker Compose](https://docs.docker.com/compose/), [ECS](https://aws.amazon.com/ecs), [EKS](https://aws.amazon.com/eks), etc.

### Pricing

Generally, public repositories are suitable for open-source developers sharing their work with the world for free. In contrast, private repositories are used by companies to share proprietary images of their internal software. Depending on the privacy level you need, here's how AWS charges for ECR:

- **Private Repositories**: As a part of the AWS free tier, you get 500 MB of storage for one year for private repositories. Beyond that, the storage cost is $0.10 per GB-month of data storage for private repositories.
- **Public Repositories**: ECR offers 50 GB-month of free storage and 500 GB to 5 TB (depending on whether you authenticate with AWS or not) for public repositories. Beyond that, the storage cost is $0.10 per GB-month of data storage.

There may be additional costs depending on your region and usage, so be sure to check the [pricing](https://aws.amazon.com/ecr/pricing/).

### Why ECR?

If you're already bought into the Amazon ecosystem, ECR is an obvious choice for your container registry as you won't have to add a new service to your budget. Besides saving you money, ECR integrates with other standard AWS services, which will hopefully improve developer experience as well.

### [IAM (Identity and Access Management)](https://aws.amazon.com/iam)

[ECR integrates with IAM](https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-policies.html) to configure policies and manage and control access to your images. This means you won't have to share credentials or manage permissions individually for each repository.

### [EKS (Elastic Kubernetes Service)](https://aws.amazon.com/eks)

[Kubernetes](/blog/building-on-kubernetes-ingress) is a widely used container orchestration technology for automating deployments, networking, and scaling your application. Elastic Kubernetes Service is the AWS-managed Kubernetes platform.

EKS allows you to run Kubernetes on AWS without maintaining your own [Kubernetes control plane](https://kubernetes.io/docs/concepts/overview/components/#control-plane-components). You define a manifest file, and the Kubernetes master node will schedule and run the deployments. As you'll see later, you can use images hosted in ECR in this manifest file to easily deploy your workloads from your public or private repositories.

### [ECS (Elastic Container Service)](https://aws.amazon.com/ecs)

Like EKS, ECS is a container orchestration service that makes running, stopping, and managing containers on AWS resources easy. Without getting into all of the specifics, ECS is typically better for teams that want a simple but powerful way to run their containers, while EKS adds the flexibility and security options available in Kubernetes. To learn more about each of AWS's container orchestration tools, read [this article on picking the right one](https://aws.amazon.com/blogs/containers/amazon-ecs-vs-amazon-eks-making-sense-of-aws-container-services/).

When integrating with ECR, ECS users simply have to [add their images to a task definition](https://docs.aws.amazon.com/AmazonECR/latest/userguide/ECR_on_ECS.html). Task definitions are 'JSON' files that describe each container that forms the application. These definitions are similar to Kubernetes manifest files but require their own format and options.

## Using Elastic Container Registry

If you've decided that ECR is the right option for your application, you're ready to set up and start using it. In the remainder of this tutorial, I'll walk you through the steps required to get started with ECR. I'll show you how to push and pull images from ECR and how you can use your ECR images in EKS and ECS.

Typically these steps will be run as part of your continuous integration workflow, but you can also run them locally to get more familiar with the required tooling before you automate them.

### Prerequisites

- [AWS Credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html) with permissions to interact with ECR.
- [Docker installed for your operating system](https://docs.docker.com/get-docker/).
- The [AWS CLI installed locally](https://aws.amazon.com/cli/).

### Creating a New Repository

Assuming you've already got an AWS account and permissions correctly configured, the easiest way to get started is to create a new ECR repository via the Amazon Web Services UI.

Go to the [ECR homepage](http://console.aws.amazon.com/ecr/get-started) and click the *Get Started* button.

![ECR landing page](/blog/assets/images/how-to-setup-and-use-amazons-elastic-container-registry/xX4GGwL.png)

You will be taken to the *Create repository* page, where you can enter all the details for your new repository.

### Configuring Your Repository

![Amazon ECR repository creation menu](/blog/assets/images/how-to-setup-and-use-amazons-elastic-container-registry/SZrf8AQ.png)

Choose a visibility (*Public* or *Private*), name the repository (ideally something short but self-explanatory), and below the name, select any of the other options you need:

- *Tag immutability* - Prevents the same tag from being pushed twice and overwriting a previous version of the tag.
- *Scan on push* - Your images will be scanned for security vulnerabilities each time a new tag is pushed.
- *[KMS encryption](https://medium.com/@suprajaraman/aws-kms-all-about-keys-564245425ecc)* - Allows you to use AWS Key Management Service (KMS) to encrypt the images in this repository.

*Note: your final repository URL structure will be something like this:*

~~~{.bash caption=">_"}
<account-id>.dkr.ecr.<account-region>.amazonaws.com/<repository-name>
~~~

Once your repository is configured, click *Create repository* to initialize your ECR repository. If you want to create a public repository, you can follow the same steps but select `Pubic` instead of `Private`.

![Amazon ECR dashboard](/blog/assets/images/how-to-setup-and-use-amazons-elastic-container-registry/XCZe4vX.png)

### Pushing an Image to the Repository

Before publishing the Image to ECR, make sure you have Docker installed on your workstation and a project with a [Dockerfile](/blog/compiling-containers-dockerfiles-llvm-and-buildkit) that's ready to be built and pushed to ECR.

If you don't have a project ready, create a new file called `Dockerfile` and enter the following (this is based on the official [Docker `alpine:3.7` image](https://hub.docker.com/_/alpine)):

~~~{.dockerfile caption="Dockerfile"}
FROM alpine:3.7
CMD echo 'Hello world'
~~~

Next, [set up your AWS credentials on the CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html) if you haven't already:

~~~{.bash caption=">_"}
aws configure
~~~

Paste your *AWS Access Key ID* and *AWS Secret Access Key*. This will allow your CLI instance access to your AWS account.

If you're using the CLI as part of your continuous integration workflow, you also have the option [to use environment variables](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html) to securely store your credentials.

### Adding Your ECR Credentials to the Docker CLI

Next, you need Docker to be able to push images to your ECR repository. The [`docker login` command](https://docs.docker.com/engine/reference/commandline/login/) will allow you to do this, so using the AWS CLI, retrieve your ECR password and pipe it into the Docker command:

~~~{.bash caption=">_"}
aws ecr get-login-password \
    --region <account-region> \
| docker login \
    --username AWS \
    --password-stdin <account-id>.dkr.ecr.<account-region>.amazonaws.com/
    <repository-name>
~~~

After authentication, you will see `Login Succeeded` as a response. Now you'll be able to push tagged images to your ECR repository.

If you are pushing or pulling images from this machine regularly, you may not want to go through this login process every time. Instead of using `docker login`, you can configure the [Amazon ECR Docker Credential Helper](https://github.com/awslabs/amazon-ecr-credential-helper) to give the [Docker daemon](/blog/what-is-buildkit-and-what-can-i-do-with-it) direct access to your AWS credentials. This method is also convenient for CI environments because it automates the authentication process and caches tokens to minimize your risk of being throttled.

### Pushing an Image To ECR

Next, build the image from your 'Dockerfile':

~~~{.bash caption=">_"}
docker build -t <image-name>:<image-version> .
~~~

Then, tag the image with your ECR repository name:

~~~{.bash caption=">_"}
docker tag <image-name>:<image-version> <account-id>.dkr.ecr.\
<account-region>.amazonaws.com/<repository-name>:<image-version>
~~~

Your image is now ready to push to ECR:

~~~{.bash caption=">_"}
docker push <account-id>.dkr.ecr.<account-region>.amazonaws.com\
<repository-name>:<image-version>
~~~

And just like that, you have pushed our first image to a repository on Elastic Container Registry. In the next section, you'll see how you can use these images for local or remote deployments.

### Pulling a Image From ECR

Whether you want to pull an image from a public ECR repository or your company has private images stored in ECR, pulling works in the same way it does in any container registry. After you've authenticated (using the same steps above), you can use [`docker pull`](https://docs.docker.com/engine/reference/commandline/pull/):

~~~{.bash caption=">_"}
docker pull <account-id>.dkr.ecr.<account-region>.amazonaws.com\
<repository-name>:<image-version>
~~~

Now you can run this image locally.

### Using ECR Images in a Dockerfile

If you are building a new application from a base image stored in ECR, you can use the `FROM` command in your 'Dockerfile' just as you would with any other Docker image. For example:

~~~{.dockerfile caption="Dockerfile"}

FROM: <account-id>.dkr.ecr.<account-region>.amazonaws.com<repository-name>:<image-version>
~~~

Again, you'll need to be authenticated if you want to build an image off a private image in ECR, but this allows you to share base images with your team or the public.

### Using ECR Images in Production Deployments

To use your images from ECR in a container management platform like ECS or EKS, simply add the name and tag of the image you want to use to the relevant configuration file.

#### EKS Manifest

For example, you can use the following EKS manifest to deploy a NodeJS image stored in ECR:

~~~{.yaml caption=""}
apiVersion: batch/v1 
kind: Job 
metadata: 
    name: eks-iam-test-s3 
spec: template: 
    metadata: 
      labels: 
        app: eks-iam-test-s3 
    spec: 
      serviceAccountName: iam-test 
      containers: 
        - name: eks-iam-test 
          image: 123456789012.dkr.ecr.us-west-2.amazonaws.com/aws-nodejs-sample:v1 
          args: ["s3", "ls"] 
      restartPolicy: Never
~~~

When deployed, it will create a job with the name `eks-iam-test-s3` using the `123456789012.dkr.ecr.us-west-2.amazonaws.com/aws-nodejs-sample:v1` image. To see the complete step-by-step process for deploying this job to EKS, see [the AWS documentation](https://docs.amazonaws.cn/en_us/AmazonECR/latest/userguide/ECR_on_EKS.html).

##### ECS Task Definition

ECR images can also be used in ECS task definition files to define your containers:

~~~{.json caption=""}
{
  "containerDefinitions": [
    {
      "name": "sample-app",
      "image": "123456789012.dkr.ecr.us-west-2.amazonaws.com/aws-nodejs-sample:v1",
      "memory": 200,
      "cpu": 10,
      "essential": true
    }
  ],
  "family": "example_task_3",
  "taskRoleArn": "arn:aws:iam::123456789012:role/AmazonECSTaskS3BucketRole"
}
~~~

This definition will deploy a container named `sample-app` using image `123456789012.dkr.ecr.us-west-2.amazonaws.com/aws-nodejs-sample:v1`. More detailed steps are [available in the ECS documentation](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/create-task-definition.html).

## Conclusion

In this tutorial, you learned the basics of containers and container registries. You learned about the differences between Docker Hub and Amazon ECR for public and private repository hosting, and you saw how to set up and use ECR to store your images.

Whether you're using Docker images in production or not, ECR is a useful tool if you're already embedded in the AWS ecosystem. It gives you the advantage of working well with other Amazon services like IAM for security and ECS or EKS for deployments.

If you are pushing images to ECR as part of your build pipeline, check out Earthly's support for [ECR credentials](https://docs.earthly.dev/docs/guides/configuring-registries/aws-ecr). Unlike other build tools, Earthly executes each CI build in an isolated containerized environment, and it can pull images from ECR or any other container registry you choose. It's free to use, so [check Earthly out today](https://earthly.dev/).
