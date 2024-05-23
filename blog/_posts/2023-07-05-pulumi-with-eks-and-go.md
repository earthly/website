---
title: "Infrastructure as Code with Pulumi and AWS EKS for Go Developers"
toc: true
author: Mercy Bassey
editor: Ubaydah Abdulwasiu

internal-links:
 - Pulumi
 - AWS EKS
 - GO
 - Cloud
 - Infrastructure
excerpt: |
    Learn how to use Pulumi and AWS EKS to provision infrastructure as code for your GO applications. This tutorial covers creating an S3 bucket, setting up an EKS cluster, and deploying a Docker image to the cluster. Dive into the world of Infrastructure as Code with Pulumi and streamline your cloud infrastructure management.
last_modified_at: 2023-07-19
categories:
  - Cloud
---
**The article examines how Pulumi and Go work together to set up AWS services. Earthly improves continuous integration workflows, whether you are using Pulumi or not. [Learn more about Earthly](https://cloud.earthly.dev/login).**

As the world continues to shift towards cloud-based solutions, managing, and deploying infrastructure in a scalable and automated way has become increasingly important. Infrastructure as Code, often abbreviated as Iac, has emerged as a critical practice in this area, providing a way to manage infrastructure using code, and version control systems.

[Pulumi](https://www.pulumi.com/docs/) is one such IaC tool that allows developers to write code using their preferred programming languages and deploy infrastructure to popular cloud providers.

In this article, we'll see how to use Pulumi to provision an Amazon S3 bucket and an Amazon Elastic Kubernetes Service (EKS) cluster. We'll walk through the steps required to set up our environment and create the necessary infrastructure, all while using Go to write our Pulumi code. Let's dive in!

## Prerequisites

- An understanding of Golang and the fundamentals of its basic packages
- An AWS account and the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html#cliv2-linux-install) installed on your machine.
- [Kubernetes](https://kubernetes.io/releases/download/) is set up on your machine.
- This tutorial uses a Linux OS with an Ubuntu 22.04 LTS distro. But any other OS will work fine.

**Note**: You can find all the code snippets used in this tutorial from this [GitHub repository](https://github.com/mercybassey/Pulumi-andEKS-for-Go-Developers).

## A Brief Overview of Pulumi and AWS EKS

[Pulumi](https://www.pulumi.com/docs/) is a modern Infrastructure as Code (IaC) platform that allows developers and infrastructure teams to build, deploy, and manage cloud infrastructure using familiar programming languages such as Go, Python, JavaScript, and TypeScript. On the other hand, AWS Elastic Kubernetes Service (EKS) is a fully managed Kubernetes service that makes it easy to deploy, manage, and scale containerized applications using Kubernetes on AWS.

By combining Pulumi and AWS EKS, you can automate infrastructure as code for your Kubernetes applications, making managing and deploying applications in the cloud easier. This helps with increased productivity, faster development cycles, and reduced infrastructure management overhead.

## Setting Up the Environment for AWS

Since you'll be working with the AWS S3 and Elastic Kubernetes Service (EKS), you must create an [IAM](https://docs.aws.amazon.com/rolesanywhere/latest/userguide/introduction.html) user with the necessary permissions to work with these AWS services.

<div class=info>
IAM stands for Identity and Access Management. It is a service provided by Amazon Web Services (AWS) that enables you to manage user identities and their permissions for accessing AWS resources. IAM allows you to control access to various AWS services and resources by creating and managing users, groups, and roles. With IAM, you can grant specific permissions to users or groups, allowing them to perform actions on AWS resources while ensuring security and compliance.
</div>

These permissions include the following:

- `AmazonEC2FullAccess`: This allows full access to all actions on the Amazon EC2 service, which includes instance management, security group operations, and more.
- `AmazonEKS_CNI_Policy`: This policy applies to the Amazon EKS node(s) IAM role. It allows the [Amazon VPC CNI plugin](https://docs.aws.amazon.com/eks/latest/userguide/managing-vpc-cni.html) to make calls to AWS APIs on your behalf.
- `AmazonEKSClusterPolicy`: This allows the entity (user, group, or role) to create or delete Amazon EKS Clusters.
- `AmazonEKSServicePolicy`: This provides the permissions necessary to run the Amazon EKS service. It includes permissions for launching and managing the Amazon EKS control plane.
- `AmazonEKSVPCResourceController`: This allows the entity to manage VPC Elastic Network Interfaces (ENI), necessary for the Amazon EKS VPC Resource Controller to operate.
- `AmazonEKSWorkerNodePolicy`: This provides the necessary permissions for worker nodes to connect to the Amazon EKS cluster control plane
- `AmazonS3FullAccess`: Provides full access to all actions on the Amazon S3 service, which includes bucket and object operations.
- `AmazonSSMFullAccess`: This allows full access to all AWS Systems Manager service actions.
- `AWSCloudFormationFullAccess`: This provides full access to AWS CloudFormation. This includes permissions to create, update, and delete CloudFormation stacks.
- `IAMFullAccess`: This allows full access to all actions on the IAM service, such as creating and managing users, roles, policies, and groups.

<div class="wide">
![Viewing permissions policy for IAM user]({{site.images}}{{page.slug}}/3461gRI.png)
</div>

Next, add an [inline policy](https://docs.aws.amazon.com/acm/latest/userguide/authen-inlinepolicies.html) with the following code, you can name it what you like. This tutorial calls this policy *eksCreateCluser*:

~~~{.go caption="main.go"}
{
    "Version": "2012-10-17",  // The version of the policy language
    "Statement": [ // An array of individual statements, each describing \
    one set of permissions.
        {
            "Sid": "EKSPermissions",  //Policy statement identifier
            "Effect": "Allow", // Specifies whether the statement results \
            in an allow or an explicit deny. In this case, it's "Allow".
            "Action": [ // Describes the specific action or actions that \
            the statement will allow or deny.
    // Allow creation, reading, modifying, listing, and deleting the EKS \
    cluster. And then,  allow adding and removing tags from the EKS \
    cluster, respectively.
                "eks:CreateCluster",
                "eks:DescribeCluster", 
                "eks:UpdateClusterConfig", 
                "eks:ListClusters", 

                "eks:DeleteCluster", 
                "eks:TagResource", 
                "eks:UntagResource" 
            ],
            "Resource": [ // Specifies the object or objects to which the \
            action(s) apply. "*" indicates that the action(s) apply to all \
            resources.
                "*"
            ]
        },
~~~

This policy allows the IAM user to perform actions required to create, manage, and delete EKS clusters, such as creating a cluster, updating the cluster configuration, etc.

Lastly, open up your terminal app and run the following commands sequentially to configure the AWS CLI with your IAM user credentials:

~~~{.bash caption=">_"}
aws configure
AWS Access Key ID [****************K3PQ]: <YOUR_ACCESS_KEY_ID>
AWS Secret Access Key [****************dNMD]: <YOUR_SECRET_ACCESS_KEY_ID>
Default region name [us-east-1]: <YOUR_REGION> \
#This tutorial uses the default
Default output format [json]: <YOUR_PREFERRED_OUTPUT_FORMAT> \
#This tutorial uses the default
~~~

With that done correctly, you are ready to start with infrastructure as code with Pulumi and Go for AWS.

## Installing and Configuring Pulumi for Go

To begin using infrastructure as code with Pulumi and AWS, installing, and configuring Pulumi for Go is necessary. The Pulumi official documentation provides commands to install Pulumi for most kinds of [operating systems](https://www.pulumi.com/docs/get-started/install/). Since this tutorial uses a Linux OS with an Ubuntu 22.04 LTS distro, we'll install Pulumi with the following command:

~~~{.bash caption=">_"}
curl -fsSL https://get.pulumi.com | sh
~~~

After a successful installation, you should have something similar to the following output, which confirms that Pulumi was installed successfully:

<div class="wide">
![Installing pulumi]({{site.images}}{{page.slug}}/mNmvI1Q.png)
</div>

### Configuring Pulumi for Go

With Pulumi installed, you must create a Pulumi project specifically for Go. To achieve this, create a directory with the following command; you can call this directory whatever you want. This tutorial uses `pulumi-eks`:

~~~{.bash caption=">_"}
mkdir pulumi-eks #Creates directory
cd pulumi-eks #Sets the directory as the current and working directory
~~~

<div class="notice--info">
💡 If you are using Pulumi for the first time, visit the following address [https://app.pulumi.com/account/tokens](https://app.pulumi.com/account/tokens), login to pulumi cloud and authenticate Pulumi, with either GitHub, Gitlab or Atlassian and generate a token.
</div>

Create a new Pulumi project in the current directory with the following command:

~~~{.bash caption=">_"}
pulumi new
~~~

This command will ask you first to input a token; Go ahead and input the token and hit `Enter` to continue:

<div class="wide">
![Inputting access token for pulumi]({{site.images}}{{page.slug}}/nhBli0o.png)
</div>

Once you have entered the token, you should have the following output that welcomes you to pulumi and asks you to select a platform and programming language. Select the `aws-go` option and press enter to proceed to the next step:

<div class="wide">
![Selecting platform and programming language (aws-go)]({{site.images}}{{page.slug}}/oOSImPM.png)
</div>

In the next step, you'll be prompted to choose a `template`, a `project name`, a `project description`, a `stack name`, and an `aws-region`. Hit `Enter` all through to accept their defaults (this is optional, you can set them based on your preference if you like) and wait a little for pulumi to install all dependencies for your pulumi project; you should see output similar to this:

<div class="wide">
![Inputting template, project name, project description, stack name, and aws region]({{site.images}}{{page.slug}}/GdVSZJd.png)
</div>

Once Pulumi has installed the dependencies, you should have the following output:

<div class="wide">
![Verifying pulumi dependency installation]({{site.images}}{{page.slug}}/INzm0eY.png)
</div>

Now, open up the current directory with your default code editor and you should see that Pulumi initialized a Go project containing the following files:

- A `go.mod` and `go.sum` file: These files are related to Go's module system, which manages dependencies for your project. `go.mod` specifies the module's name and its dependencies. In contrast, `go.sum` stores cryptographic hashes of module versions to ensure that you're using the same dependencies across all environments.
- A `main.go` file: This is the main source file for your Go application. It contains the code that will be executed when you run the application.
- A `Pulumi.yaml` file: This file is the project configuration file that defines your infrastructure as code. It includes information about the cloud provider, the resources to be created, and their properties.
- A `Pulumi.dev.yaml`file: A configuration file that defines configuration settings for the development environment. It's similar to `Pulumi.yaml` but specific to the development environment and overrides any settings defined in `Pulumi.yaml`.

<div class="wide">
![Viewing files created by pulumi]({{site.images}}{{page.slug}}/5SEGnDY.png)
</div>

## Creating an S3 Bucket on AWS

In Pulumi, you declare the desired state of your infrastructure, and Pulumi takes care of provisioning and managing that state. In other words, you define your infrastructure using code, and Pulumi uses that code to create and manage resources in your cloud provider account.

With our installation complete and our code generated, it's time to delve deeper into the workings of Pulumi. What is the structure of a typical Pulumi project? Let's uncover this by diving into an example of creating an Amazon S3 bucket, a fundamental component for storing and accessing data on Amazon's scalable cloud storage service.

Upon opening the `main.go` file, you will encounter example code that demonstrates how Pulumi can be used to create an S3 bucket resource within AWS, which looks something like this:

~~~{.go caption="main.go"}
package main

import (
    "github.com/pulumi/pulumi-aws/sdk/v5/go/aws/s3"
    "github.com/pulumi/pulumi/sdk/v3/go/pulumi"
)

func main() {
    pulumi.Run(func(ctx *pulumi.Context) error {
        // Create an AWS resource (S3 Bucket)
        bucket, err := s3.NewBucket(ctx, "my-bucket", nil)
        if err != nil {
            return err
        }

        // Export the name of the bucket
        ctx.Export("bucketName", bucket.ID())
        return nil
    })
}
~~~

This code imports the required AWS S3 `"github.com/pulumi/pulumi-aws/sdk/v5/go/aws/s3"`  and Pulumi `"github.com/pulumi/pulumi/sdk/v3/go/pulumi"` packages, creates a new Pulumi stack with a single resource (an S3 bucket), and exports the name of the bucket (named `my-bucket`) as an output value.

<div class="notice--info">
💡In Pulumi, a "stack" is an independently configurable instance of a Pulumi program, serving as an isolated environment within a project. Stacks, which can represent different development stages (like 'development', 'staging', 'production'), each have unique configurations and states. They allow for the management of environment-specific settings through variable parameters during deployment

In the context of our program, this Pulumi stack consists of a single resource, which is an Amazon S3 bucket. To identify this bucket for future reference and to expose its value outside the stack, we're designating it as an output value under the name `my-bucket`. This structure of the stack allows us to manage this set of infrastructure in isolation, ensuring that changes, updates, or configurations are encapsulated within this stack, thereby ensuring environmental isolation and reconfigurability.
</div>

To execute this project, run the `pulumi up` command, which is used to execute a Pulumi project. This command will output a preview link containing the changes you are trying to make and then download the plugins for the cloud provider you are using to create resources in your infrastructure, which is AWS S3:

<div class="wide">
![Downloading plugins needed to create S3 bucket on AWS]({{site.images}}{{page.slug}}/T2rwXE4.png)
</div>

Once you open up the preview link over a web browser, you'll see a preview of the resources that will be created or updated in your cloud infrastructure based on the changes you have made to your Pulumi program.

This preview lets you review and confirm the changes before applying them to your infrastructure. It will also show you the resources that will be created, updated, or deleted, along with any configuration options and dependencies.

<div class="wide">
![Viewing proposed updates to be made by pulumi]({{site.images}}{{page.slug}}/DP7XxSm.png)
</div>

Heading back to your terminal, you'll see that Pulumi asks you to verify if you'd like to make the update. Select the `yes` option, and hit `Enter` to continue:

<div class="wide">
![Viewing pulumi confirmation question]({{site.images}}{{page.slug}}/ntLHpph.png)
</div>

Once selected, Pulumi will create an S3 bucket on your AWS account:

<div class="wide">
![Viewing successful updates and bucket name]({{site.images}}{{page.slug}}/UJLDkSe.png)
</div>

Additionally, you can confirm this change on the preview link below; according to the image above; this particular link is `https://app.pulumi.com/mercybassey/pulumi-eks/dev/updates/2`. So Pulumi creates a preview link before the change is made and an update link after the change has been successfully made.

<div class="notice--info">
💡The preview link shows what will happen if you run the update, and the update link shows what happened when you ran the update.
</div>

<div class="wide">
![Viewing resources created by pulumi]({{site.images}}{{page.slug}}/uvLZvjJ.png)
</div>

Now, on your AWS account, you should see your S3 bucket created:

<div class="wide">
![Viewing S3 bucket on AWS account]({{site.images}}{{page.slug}}/EKDnwLN.png)
</div>

### Creating Multiple S3 Buckets

Now that we've seen how to create a single resource and have a better understanding of how pulumi works, it's time to expand our scope. Let's look at how to use Pulumi to set up multiple S3 buckets at once.

Pulumi leverages the power of a programming language to manage infrastructure, enabling us to scale our operations effortlessly. To witness this capability firsthand, let's modify our code to create multiple S3 buckets:

~~~{.go caption="main.go"}
package main

import (
    "fmt"
    "github.com/pulumi/pulumi-aws/sdk/v5/go/aws/s3"
    "github.com/pulumi/pulumi/sdk/v3/go/pulumi"
)

func main() {
    pulumi.Run(func(ctx *pulumi.Context) error {
        for i := 0; i < 3; i++ {
            // Create an AWS resource (S3 Bucket)
            bucket, err := s3.NewBucket(ctx, fmt.Sprintf("my-bucket-%d", i) \
            , nil) // use a unique bucket name.
            if err != nil {
                return err
            }

            // Export the name and ID of the bucket
            ctx.Export(fmt.Sprintf("bucket%dName", i), bucket.ID())
            ctx.Export(fmt.Sprintf("bucket%dID", i), bucket.Arn)
        }

        return nil
    })
}
~~~

The GO code above does the following:

- Creates three AWS S3 buckets using Pulumi and the `pulumi` and `s3` packages from the Pulumi AWS SDK.
- Calls the `pulumi.Run` function in the `main` function to create a new Pulumi program that can be executed with the `pulumi up` command.
- Uses the `s3.NewBucket` function to create a new S3 bucket resource named "my-bucket".

<div class="notice--info">
💡It is crucial to note that every S3 bucket name must be unique across all of Amazon S3. That means no two buckets can share the same name, not just within your account, but across all AWS accounts globally. So, when naming your buckets, ensure that you're using unique identifiers. You may need to use a bucket name other than `my-bucket` for this tutorial since `my-bucket-<some-number>` is likely taken. This will help avoid potential conflicts as you follow along in the tutorial.
</div>

- Calls the `bucket.ID()` method to retrieve the ID of the created bucket.
- Uses the `ctx.Export` function to export the bucket name and the ARN as the `bucketID` output of the Pulumi program so that other programs can use it. This means, if you have multiple Pulumi stacks within a project or across projects, one stack might create resources that other stacks depend upon. By exporting a resource property (like bucket name or ARN in this case), other stacks can import and use that value in their own configuration.

<div class="notice--info">
💡 `bucket.arn` returns the Amazon Resource Name (ARN) of the S3 bucket resource created in the Pulumi program. The ARN is a unique identifier for a resource in the AWS ecosystem. It can be used to identify and access the resource from other AWS services or external applications. Therefore, the `ctx.export` function makes the bucket name and ARN available as an output of the Pulumi program. This means the bucket name and ARN can be accessed in other parts of this Pulumi stack, in other Pulumi stacks, or even outside of Pulumi altogether.

On the other hand, if you need to access exported values within the same Pulumi stack, you can directly reference the exported values. For accessing exported values from another stack or programmatically outside Pulumi, you can use the `getOutput` method on the [`StackReference`](https://www.pulumi.com/docs/concepts/stack/#stackreferences) object or leverage the Pulumi CLI command [`pulumi stack output <output-name>`](https://www.pulumi.com/docs/cli/commands/pulumi_stack_output/) respectively.
</div>

Execute the code with the command `pulumi up`, select *yes*, and you should see the following output:

<div class="wide">
![Viewing resources created by pulumi (three S3 buckets)]({{site.images}}{{page.slug}}/tRiAymO.png)
</div>

Pulumi operates on a desired state model. Considering the output above, when we revised our Go code to define three new buckets, Pulumi looked at this desired state and compared it to the actual state of our infrastructure. It noticed that the initial bucket was no longer part of our code, which it interpreted as us no longer needing that bucket. Without our explicit instruction, Pulumi intelligently deleted this bucket. At the same time, it saw that there were three new buckets in our desired state, so it went ahead and created them. The result was that Pulumi aligned our infrastructure with the state we defined in our code - removing what was no longer needed and creating what was newly defined.

You can also confirm from your AWS account; you should have something similar to this:

<div class="wide">
![Viewing S3 buckets via the AWS S3 page]({{site.images}}{{page.slug}}/sUbMbMP.png)
</div>

You can see the three buckets created with pulumi and that each bucket name uses the expected format (`bucketName-i-bucketArn`).

### Creating an AWS EKS Cluster

Now it's time to do some advanced stuff. This section will explore how to first create an Amazon Elastic Kubernetes Service (EKS) cluster with Pulumi and Go. Then go through creating a [namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/) and then create a deployment in that namespace.

Edit the `main.go` file to look like the following:

~~~{.go caption="main.go"}
package main

import (
    "github.com/pulumi/pulumi-awsx/sdk/go/awsx/ec2"
    "github.com/pulumi/pulumi-eks/sdk/go/eks"
    "github.com/pulumi/pulumi/sdk/v3/go/pulumi"
)

func main() {
    pulumi.Run(func(ctx *pulumi.Context) error {
        // Create a VPC for our cluster.
        vpc, err := ec2.NewVpc(ctx, "vpc", nil)
        if err != nil {
            return err
        }
        // Create an EKS cluster
        eksCluster, err := eks.NewCluster(ctx, "my-pulumi-eks-cluster", \
        &eks.ClusterArgs{
            Name: pulumi.String("my-pulumi-eks-cluster"),
            VpcId: vpc.VpcId,
            PublicSubnetIds:              vpc.PublicSubnetIds,
            PrivateSubnetIds:             vpc.PrivateSubnetIds,
            NodeAssociatePublicIpAddress: pulumi.BoolRef(false),
        })
        if err != nil {
            return err
        }
        // Export the EKS kubeconfig
        ctx.Export("kubeconfig", eksCluster.Kubeconfig)

        return nil
    })
}
~~~

Courtesy of the [official pulumi documentation](https://www.pulumi.com/docs/guides/crosswalk/aws/eks/), the code above creates an Amazon Elastic Kubernetes Service (EKS) cluster on AWS.

1. It creates a [VPC](https://earthly.dev/blog/aws-networks/) for the cluster using the `ec2.NewVpc` method from the `awsx/ec2` package.
2. It creates an EKS cluster called `my-pulumi-eks-cluster` using the `eks.NewCluster` method from the `eks` package.
3. Then, it exports the EKS cluster kubeconfig as an output of the Pulumi program using the `ctx.Export` method.

Before executing the above pulumi program, run the following commands sequentially to install the SDKs:

~~~{.bash caption=">_"}
go get github.com/pulumi/pulumi-awsx/sdk/go/awsx/ec2
go get github.com/pulumi/pulumi-eks/sdk/go/eks
~~~

<div class="wide">
![Downloading EkS and EC2 SDKs]({{site.images}}{{page.slug}}/lBH0MUd.png)
</div>

Now run the `pulumi up` command to execute the pulumi program. Wait for a little for your EKS cluster to be provisioned; once done, you should have something similar to the image below:

<div class="wide">
![Viewing EKS kubeconfig, resources created by pulumi and duration]({{site.images}}{{page.slug}}/BRXibeb.png)
</div>

To find the EKS cluster that you created with Pulumi, go to your AWS Management Console and navigate to the Amazon EKS page. Make sure that you are in the correct region where you created the EKS cluster (us-east-1), and you should see your cluster as shown below:

<div class="wide">
![Viewing EKS cluster over EKS page]({{site.images}}{{page.slug}}/CQDkyvQ.png)
</div>

From the image above, you can see that it's active and uses Kubernetes version `1.25`, which is upgradable and uses the EKS provider.

### Creating a Namespace and a Deployment

Now that you have your EKS cluster created, it's time to test it. You'll achieve this by creating a namespace and then deploying a sample image `mercybassey/node-service` in that namespace.
First, add the following SDKs in your `main.go` file imports:

~~~{.go caption="main.go"}
   "github.com/pulumi/pulumi-kubernetes/sdk/v3/go/kubernetes"
   corev1 "github.com/pulumi/pulumi-kubernetes/sdk/v3/go/kubernetes/core/v1"
   metav1 "github.com/pulumi/pulumi-kubernetes/sdk/v3/go/kubernetes/meta/v1"
   appsv1 "github.com/pulumi/pulumi-kubernetes/sdk/v3/go/kubernetes/apps/v1"
~~~

Importing these SDKs will give you access to the functionalities and types for working with Kubernetes resources.

Next, inside the `pulumi.Run` function, add the following code above the VPC creation function:

~~~{.go caption="main.go"}
imageName := "mercybassey/node-service"
imageTag := "latest"
imageFullName := imageName + ":" + imageTag

// Create a VPC for our cluster.
~~~

This will create and initialize three variables: `imageName`, `imageTag`, and `imageFullName` that define and construct the full name of a Docker image by combining the image name and tag.

Below the EKS cluster creation function, add the following code:

~~~{.go caption="main.go"}

eksProvider, err := kubernetes.NewProvider(ctx, "eks-provider", \
&kubernetes.ProviderArgs{
            Kubeconfig: eksCluster.KubeconfigJson,
        })
        if err != nil {
            return err
        }
~~~

This will create a Kubernetes provider that uses the `kubeconfig` of the created EKS cluster. It will allow us to create and interact with resources within the EKS cluster.

Next, add the following code to create a namespace:

~~~{.go caption="main.go"}
// Create the Kubernetes provider
…
// Create a Kubernetes Namespace
        namespace, err := corev1.NewNamespace(ctx, "my-eks-namespace", \
        &corev1.NamespaceArgs{
            Metadata: &metav1.ObjectMetaArgs{
                Name: pulumi.String("my-eks-namespace"),
                Labels: pulumi.StringMap{
                    "name": pulumi.String("my-eks-namespace"),
                },
            },
        }, pulumi.Provider(eksProvider))
        if err != nil {
            return err
        }
~~~

This will create a new Kubernetes namespace, `my-eks-namespace` in the EKS cluster that tells Pulumi to use the provided `eksProvider` as the Kubernetes provider for this namespace.

Next, add the following code to create a deployment in the EKS cluster:

~~~{.go caption="main.go"}
// Create a Kubernetes Namespace
…
// Deploy the Docker image to the EKS cluster using a Kubernetes deployment
deployment, err := appsv1.NewDeployment(ctx, "my-eks-deployment", \
&appsv1.DeploymentArgs{
    Metadata: &metav1.ObjectMetaArgs{
        Name:      pulumi.String("my-eks-deployment"),
        Namespace: pulumi.String("my-eks-namespace"),
    },
    Spec: &appsv1.DeploymentSpecArgs{
        Replicas: pulumi.Int(1),
        Selector: &metav1.LabelSelectorArgs{
            MatchLabels: pulumi.StringMap{
                "app": pulumi.String("my-app"),
            },
        },
        Template: &corev1.PodTemplateSpecArgs{
            Metadata: &metav1.ObjectMetaArgs{
                Labels: pulumi.StringMap{
                    "app": pulumi.String("my-app"),
                },
            },
            Spec: &corev1.PodSpecArgs{
                Containers: corev1.ContainerArray{
                    corev1.ContainerArgs{
                        Image: pulumi.String(imageFullName),
                        Name:  pulumi.String("my-app-container"),
                        Ports: corev1.ContainerPortArray{
                            corev1.ContainerPortArgs{
                                ContainerPort: pulumi.Int(8080),
                            },
                        },
                    },
                },
            },
        },
    },
}, pulumi.Provider(eksProvider))
if err != nil {
    return err
}
~~~

This will deploy a Docker image `mercybassey/node-service` set to the `imageFullName` variable to the EKS cluster using a Kubernetes deployment. It defines the deployment's metadata, replicas, selector, and container specifications.

Finally, add the following code to export the `kubeconfig`, `deployment-name`, and `namespace-name` to make them accessible outside the stack:

~~~{.go caption="main.go"}

// Deploy the Docker image to the EKS cluster using Kubernetes deployment
…
// Export important resources
ctx.Export("kubeconfig", eksCluster.Kubeconfig)
ctx.Export("deployment-name", deployment.Metadata.Elem().Name())
ctx.Export("namespace-name", namespace.Metadata.Elem().Name())

return nil
~~~

The complete code is expected to look like the following:

~~~{.go caption="main.go"}
package main

import (
   "github.com/pulumi/pulumi-awsx/sdk/go/awsx/ec2"
   "github.com/pulumi/pulumi-eks/sdk/go/eks"
   "github.com/pulumi/pulumi/sdk/v3/go/pulumi"
   "github.com/pulumi/pulumi-kubernetes/sdk/v3/go/kubernetes"
   corev1 "github.com/pulumi/pulumi-kubernetes/sdk/v3/go/kubernetes/core/v1"
   metav1 "github.com/pulumi/pulumi-kubernetes/sdk/v3/go/kubernetes/meta/v1"
   appsv1 "github.com/pulumi/pulumi-kubernetes/sdk/v3/go/kubernetes/apps/v1"
)

func main() {
    pulumi.Run(func(ctx *pulumi.Context) error {
        imageName := "mercybassey/node-service"
        imageTag := "latest"
        imageFullName := imageName + ":" + imageTag

        // Create a VPC for our cluster.
        vpc, err := ec2.NewVpc(ctx, "vpc", nil)
        if err != nil {
            return err
        }

        
        // Create an EKS cluster
        eksCluster, err := eks.NewCluster(ctx, "my-pulumi-eks-cluster", \
        &eks.ClusterArgs{
            Name: pulumi.String("my-pulumi-eks-cluster"),
            VpcId: vpc.VpcId,
            PublicSubnetIds:              vpc.PublicSubnetIds,
            PrivateSubnetIds:             vpc.PrivateSubnetIds,
            NodeAssociatePublicIpAddress: pulumi.BoolRef(false),
        })
        if err != nil {
            return err
        }

        eksProvider, err := kubernetes.NewProvider(ctx, "eks-provider", \
        &kubernetes.ProviderArgs{
            Kubeconfig: eksCluster.KubeconfigJson,
        })
        if err != nil {
            return err
        }

        namespace, err := corev1.NewNamespace(ctx, "my-eks-namespace", \
        &corev1.NamespaceArgs{
            Metadata: &metav1.ObjectMetaArgs{
                Name: pulumi.String("my-eks-namespace"),
                Labels: pulumi.StringMap{
                    "name": pulumi.String("my-eks-namespace"),
                },
            },
        }, pulumi.Provider(eksProvider))
        if err != nil {
            return err
        }
        

        // Deploy the Docker image to the EKS cluster using \
        Kubernetes deployment
        deployment, err := appsv1.NewDeployment(ctx, "my-eks-deployment", \
        &appsv1.DeploymentArgs{
            Metadata: &metav1.ObjectMetaArgs{
                Name: pulumi.String("my-eks-deployment"),
                Namespace: pulumi.String("my-eks-namespace"),
            },
            Spec: &appsv1.DeploymentSpecArgs{
                Replicas: pulumi.Int(1),
                Selector: &metav1.LabelSelectorArgs{
                    MatchLabels: pulumi.StringMap{
                        "app": pulumi.String("my-app"),
                    },
                },
                Template: &corev1.PodTemplateSpecArgs{
                    Metadata: &metav1.ObjectMetaArgs{
                        Labels: pulumi.StringMap{
                            "app": pulumi.String("my-app"),
                        },
                    },
                    Spec: &corev1.PodSpecArgs{
                        Containers: corev1.ContainerArray{
                            corev1.ContainerArgs{
                                Image: pulumi.String(imageFullName),
                                Name: pulumi.String("my-app-container"),
                                Ports: corev1.ContainerPortArray{
                                    corev1.ContainerPortArgs{
                                        ContainerPort: pulumi.Int(8080),
                                    },
                                },
                            },
                        },
                    },
                },
            },
        }, pulumi.Provider(eksProvider))
        if err != nil {
            return err
        }

        // Export the EKS kubeconfig
        ctx.Export("kubeconfig", eksCluster.Kubeconfig)
        ctx.Export("deployment-name", deployment.Metadata.Elem().Name())
        ctx.Export("namespace-name", namespace.Metadata.Elem().Name())

        return nil
    })
}
~~~

So in summary, the code above uses Pulumi to deploy a Docker image into a particular namespace in an EKS cluster using a Kubernetes deployment. We did the following:

- Import the Kubernetes SDK alongside other packages like the `corev1` that provides Kubernetes core API group types, such as Pods, Services, and namespaces. The `metav1` provides types for Kubernetes objects with metadata, like Namespaces, ConfigMaps, and Secrets; then the `appsv1` provides types for Kubernetes objects related to application management, like Deployments, StatefulSets, and ReplicaSets.
- Defined the docker image name and tag as `imageName` and `imageTag`, respectively, and concatenate them to form the full image name `imageFullName`.
- Created a new namespace in the EKS cluster using the `corev1.NewNamespace` function.
- Deployed the Docker image to the EKS cluster using Kubernetes deployment. This is done using the `appsv1.NewDeployment` function, which creates a new deployment object in the specified namespace.
- Export the EKS kubeconfig, deployment name, and namespace name using the `ctx.Export` function, which makes these values available as outputs of the Pulumi program.

Once you execute the `pulumi up` command, you should have the following output, showing that the namespace and deployment have been created:

<div class="notice--info">
💡 If you are so sure of the update, you can bypass the pulumi confirmation question using the following command `pulumi up -y`
</div>

<div class="wide">
![Viewing outputs (deployment-name and kubeconfig)]({{site.images}}{{page.slug}}/JkE6MIe.png)
</div>

<div class="wide">
![Viewing outputs (namespace-name) and resources created]({{site.images}}{{page.slug}}/MmcrJlG.png)
</div>

Now, execute the following command from your working directory to interact with this cluster:

This command takes the `kubeconfig` output from a Pulumi stack and writes it to the `~/.kube/config` file on the local machine, so it can be used by other Kubernetes tools (`kubectl`) and utilities to interact with the cluster.

~~~{.bash caption=">_"}
pulumi stack output kubeconfig > ~/.kube/config
~~~

On your terminal app, run the following commands sequentially to view the resources you have created in your EKS cluster:

~~~{.bash caption=">_"}
kubectl get nodes
kubectl get ns
kubectl get deployments -n my-eks-namespace
kubectl get pods -n my-eks-namespace
~~~

You should have the following output:

<div class="wide">
![Viewing cluster nodes, namespace, deployments, and pods]({{site.images}}{{page.slug}}/pFWYWkZ.png)
</div>

### Deleting All Cluster Resources

You can choose to keep the cluster and its resources for as long as you want; otherwise, you can execute the following command to delete them completely:

~~~{.bash caption=">_"}
pulumi destroy
~~~

or

~~~{.bash caption=">_"}
pulumi destroy -y
~~~

You should see the following output which indicates that the resources are deleted:

<div class="wide">
![Viewing deleted resources]({{site.images}}{{page.slug}}/pXdsVkl.png)
</div>

Once it's done deleting all the resources, you should have the following output:

<div class="wide">
![Verifying that all resources are deleted]({{site.images}}{{page.slug}}/HxnWjnG.png)
</div>

Now, if you head over to the EKS page on the AWS management console, you should see that the cluster was deleted:

<div class="wide">
![Viewing clusters on EKS page]({{site.images}}{{page.slug}}/3G9xAH3.png)
</div>

You can also run the following command if you'd like to delete the stack:

~~~{.bash caption=">_"}
pulumi stack rm <name-of-stack> 
~~~

<div class="wide">
![Deleting the pulumi stack]({{site.images}}{{page.slug}}/BoaVDIv.png)
</div>

## Conclusion

Pulumi is a super flexible tool for creating Infrastructure as Code. In this tutorial, we used it to handle AWS resources, including creating S3 buckets and provisioning an EKS cluster with Go. But that's just the start! Pulumi supports multiple cloud providers and programming languages, meaning you have a huge variety of possibilities for managing your cloud infrastructure.

We used Go to write our Pulumi infrastructure and speaking of Go, if you're building with it and want a more streamlined build workflow, you might want to give [Earthly](https://cloud.earthly.dev/login) a try. It could be a valuable addition to your development toolkit.

{% include_html cta/bottom-cta.html %}
