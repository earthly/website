---
title: "Deploying Infrastructure as Code with AWS CloudFormation"
categories:
  - Tutorials
toc: true
author: Alexander Yu
editor: Mustapha Ahmad Ayodeji

internal-links:
 - deploying infrastructure
 - deployment with aws cloudformation
 - deploying infrastructure as code
 - code deployment
excerpt: | 
     With AWS CloudFormation, you use a declarative approach to configuring and provisioning just about any resource out of Amazon Web Services' (AWS) massive 200+ service catalog.
last_modified_at: 2023-08-12
---
**This article provides a detailed guide on using AWS CloudFormation. Earthly significantly improves CI/CD pipelines. [Learn more about Earthly](/).**

[AWS CloudFormation](https://aws.amazon.com/cloudformation/) is a foundational service that enables users to create and manage their cloud infrastructure in a programmable and repeatable way. With AWS CloudFormation, you use a declarative approach to configuring and provisioning just about any resource out of Amazon Web Services' (AWS) massive 200+ service catalog. Simply define your desired infrastructure state in a JSON or YAML template, and CloudFormation will help you orchestrate all aspects of provisioning and deploying those resources.

All these stem from the concept of infrastructure as code (IaC), which is the practice of defining and managing infrastructure through regular code. Gone are the days of having to manually provision resources; IaC makes deploying infrastructure more automated, reproducible, and scalable. In addition, teams that use IaC can leverage good software engineering practices, such as testing and code review, since changes to the infrastructure are made by modifying its underlying code or template.

In this article, you'll learn all about AWS CloudFormation. By the end, you should have a good idea of what features CloudFormation has to offer and how you can use them for your AWS-based projects.

## Prerequisites

To get the most out of this article, you may want to try some of the sample templates and commands in your account. To do so, here are a few prerequisites:

* **Set up an AWS account:** If you haven't already, [create a free AWS account](https://aws.amazon.com/resources/create-account/).
* **Become familiar with the AWS Management Console:** It helps to know your way around the AWS Management Console since you'll be executing most commands from there. Note that we won't be using the AWS Command Line Interface (CLI) in this article.

## Creating an AWS CloudFormation Template

In AWS CloudFormation, you create and manage stacks. A stack is simply a collection of AWS resources. But how do you define what goes in your stack? The answer is by using [CloudFormation templates](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-guide.html).

Understanding the ins and outs of CloudFormation templates is a must if you want to become a CloudFormation expert. A CloudFormation template is a JSON or YAML file that describes the desired state of your AWS infrastructure. It defines each of the AWS resources that you want to deploy, along with their configurations. For instance, here's a very simple template that contains just one resource, an Amazon Elastic Compute Cloud (Amazon EC2) instance, written in JSON:

~~~{.json caption=""}
---
{
  "Description": "Simple CloudFormation Template with EC2 Instance",
  "Resources": {
    "MyEC2Instance": {
      "Type": "AWS::EC2::Instance",
      "Properties": {
        "InstanceType": "t2.micro",
        "ImageId": "ami-06a0cd9728546d178",
        "KeyName": "my-keypair"
      }
    }
  }
}

~~~

As you can see from this example, the main component of any CloudFormation template is the [`Resources`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/resources-section-structure.html) component; in it, you define your AWS resources. In this case, you create a single EC2 instance, which is called `MyEC2Instance` (also known as the logical ID). It has resource type `AWS::EC2::Instance`, and all resources in AWS follow a similar `AWS::Service::Resource` naming convention. Then you define specific configuration properties for the EC2 instance.

Take a look at a slightly more involved AWS CloudFormation template that defines the Amazon Virtual Private Cloud (Amazon VPC), subnet, and EC2 security group configurations alongside the instance. This time, using YAML. You'll use this template throughout this article, so save this template in a file called `cfn-template.yml` to follow along:

~~~{.yaml caption="cfn-template.yml"}
---
Description: Simple CloudFormation Template with EC2 Instance, \
VPC, Subnet, and Security Group
Resources:
  MyVPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16

  MySubnet:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref MyVPC
      CidrBlock: 10.0.0.0/24

  MySecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Security group for EC2 instance
      VpcId: !Ref MyVPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          CidrIp: 0.0.0.0/0

  MyEC2Instance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: ami-06a0cd9728546d178
      InstanceType: t2.micro
      SecurityGroupIds:
        - !Ref MySecurityGroup
      SubnetId: !Ref MySubnet
~~~

In this template, you start to make use of more features in CloudFormation to define relationships between resources. As an example, for CloudFormation to understand that the `MySubnet` resource should be associated with `MyVPC`, you can specify the configuration `VpcId: !Ref MyVPC` in `MySubnet`. This [`!Ref`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html) is known as an [intrinsic function](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference.html) in CloudFormation, and you can use it in your templates to get the value of a specified parameter or resource attribute. In this case, all you have to do is provide the logical ID of the resource, `MyVPC`. Later, CloudFormation automatically resolves the reference and substitutes it with the actual value during stack operations (create, update, and delete).

Apart from the `Resources` component, there are plenty of others that we didn't discuss. Here are a few of the main ones that you should be aware of as you develop more complicated templates:

* **`Parameters`:** The [`Parameters`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html) section of a template allows you to define input values that can be customized when creating or updating a stack. This allows users to provide values during stack creation time, which can help make your templates more flexible.
* **`Mappings`:** The [`Mappings`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/mappings-section-structure.html) section lets you create key-value maps for resource configuration. A common use case is to define region-specific settings. For example, the [AWS docs highlight an example](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/mappings-section-structure.html), which uses different AMI IDs based on the region using a CloudFormation Mapping.
* **`Conditions`:** The [`Conditions`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/conditions-section-structure.html) section is where you define conditional statements that control resource creation and configuration based on input parameters or other conditions. For instance, you might use a condition to bypass the creation of a resource in a particular environment (*ie,* test or prod).

## Creating and Updating Stacks

![stack]({{site.images}}{{page.slug}}/stack.png)\

Once your template is saved, you're ready to deploy your stack. To do this, log into your AWS account and head over to the CloudFormation console. Select **Create stack**:

<div class="wide">
![A screenshot showing the CloudFormation console home screen, from where a user can create a stack]({{site.images}}{{page.slug}}/42qKdpA.png)
</div>

Choose **Template is ready** and **Upload a template file**; then upload the `cfn-template.yml` file from the previous section:

<div class="wide">
![A screenshot showing the **Create stack** screen in the CloudFormation console]({{site.images}}{{page.slug}}/FkjcJGC.png)
</div>

Then, to specify stack details, under **Stack name**, enter a name for your stack, such as `ec2-sample-stack`. Keep all the default settings throughout the rest of the setup wizard, and then choose **Submit**.

CloudFormation then creates your stack while you sit back and relax! While CloudFormation creates your resources, you can monitor the stream of events under the **Events** tab. After a couple of minutes, you should see that your stack has been created:

<div class="wide">
![A screenshot showing the successful creation of a stack in CloudFormation]({{site.images}}{{page.slug}}/Qjz8TRy.png)
</div>

So far, you haven't run into any hiccups. However, you may encounter a scenario where you provide CloudFormation with invalid configurations, which can cause issues during stack operations. To demonstrate what happens when CloudFormation encounters issues, as well as walk you through a sample update flow, substitute the `ImageId: ami-06a0cd9728546d178` property in the template with the following:

~~~{.bash caption=">_"}
ImageId: ami-12345678
~~~

Clearly, this is not a valid `ImageId`. Let's see how CloudFormation handles this. Updating an existing stack follows a very similar setup: choose **Update** at the top, then choose **Replace current template**, and upload the new template file with your desired changes. Run through the other steps as before, and try updating your stack.

After a few seconds, you should see the following error thrown by EC2 in your event stream:

<div class="wide">
![A screenshot showing a failed update of a resource in CloudFormation]({{site.images}}{{page.slug}}/rb4rCg6.png)
</div>

This results in an overall stack status of `UPDATE_ROLLBACK_COMPLETE`:

<div class="wide">
![A screenshot showing a stack status of `UPDATE_ROLLBACK_COMPLETE` due to a resource update failure in CloudFormation]({{site.images}}{{page.slug}}/j5adudm.png)
</div>

A [rollback](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stack-failure-options.html) occurs when CloudFormation runs into an issue updating a stack. This means that CloudFormation tries to restore the last known stable state of your stack (*ie* the state before the problematic update). In this case, CloudFormation rolls your stack back to the version with `ImageId: ami-06a0cd9728546d178` since that was the last valid configuration.

Finally, if you decide that you no longer need your stack, you can simply delete it by choosing **Delete**. This deletes all resources in the stack unless you enable termination protection settings on it (more on this later).

## Configuring AWS Resources in CloudFormation

![Configuring]({{site.images}}{{page.slug}}/configure.png)\

You can use CloudFormation to provision hundreds of different types of resources. In this section, we'll take a look at some examples of the most popular ones that you'll probably see in most production stacks.

### EC2 Instances

Earlier, we took a look at the [`AWS::EC2::Instance`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html) resource. The key properties to pay attention to are the `ImageId`, `InstanceType`, and `KeyName`. While the `KeyName` isn't required, if you don't specify one, you won't be able to connect to your instance unless you choose an AMI with an alternative way of logging in.

~~~{.yaml caption="cfn-template.yml"}
---
Description: CloudFormation Template for an EC2 Instance
Resources:
  MyEC2Instance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: ami-12345678  
      # Replace with the desired AMI ID
      InstanceType: t2.micro
      KeyName: my-keypair    
      # Replace with the name of an existing EC2 key pair
      SecurityGroups:
        - !Ref MySecurityGroup  
        # Replace with the logical name of an existing security group
~~~

### VPCs and Subnets

You'll also likely be working with virtual private clouds (VPCs) and associated subnets. Here's a definition of an [`AWS::EC2::VPC`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpc.html) resource with a single public [`AWS::EC2::Subnet`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet.html):

~~~{.yaml caption="cfn-template.yml"}
---
Description: CloudFormation Template for VPC with Subnets
Resources:
  MyVPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      Tags:
        - Key: Name
          Value: MyVPC

  PublicSubnet:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref MyVPC
      CidrBlock: 10.0.0.0/24
      AvailabilityZone: us-east-1a
      Tags:
        - Key: Name
          Value: PublicSubnet
~~~

Here, the `CidrBlock` property defines the CIDR block for the VPC, which is the IP address range for the VPC. The `PublicSubnet` resource specifies the VPC ID (`MyVPC`), the CIDR block for the subnet, and the availability zone (AZ) where the subnet will be created. The template also adds tags to help identify these resources.

### Security Groups

With EC2 instances and VPCs, you'll also definitely come across [`AWS::EC2::SecurityGroup`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group.html) resources. Here's an example of a template that configures a security group with inbound rules to allow SSH access and HTTP access (port 22 and port 80) to an EC2 instance:

~~~{.yaml caption="cfn-template.yml"}
---
Description: CloudFormation Template for Security Group
Resources:
  MySecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: My EC2 Instance Security Group
      VpcId: !Ref MyVPC  # Replace with the logical name of an existing VPC
      SecurityGroupIngress:
        - CidrIp: 0.0.0.0/0
          IpProtocol: tcp
          FromPort: 22
          ToPort: 22
        - CidrIp: 0.0.0.0/0
          IpProtocol: tcp
          FromPort: 80
          ToPort: 80
~~~

The `SecurityGroupIngress` property specifies the inbound rules for the security group. In this case, it allows inbound traffic from any source (`0.0.0.0/0`) on TCP port 22 (SSH) and TCP port 80 (HTTP).

### RDS Databases

For data storage, the [`AWS::RDS::DBInstance`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html) is a very popular option.

~~~{.yaml caption="cfn-template.yml"}
---
Description: CloudFormation Template for RDS Database
Resources:
  MyDBInstance:
    Type: AWS::RDS::DBInstance
    Properties:
      AllocatedStorage: 20
      DBInstanceClass: db.t2.micro
      Engine: mysql
      EngineVersion: 5.7.34
      DBInstanceIdentifier: my-db-instance
      MasterUsername: admin
      MasterUserPassword: adminpassword
      MultiAZ: false
~~~

This template defines important properties such as the `AllocatedStorage`, `DBInstanceClass`, `Engine` (MySQL in this case), `EngineVersion`, `DBInstanceIdentifier`, credential information, and multi-AZ deployment option. Note that you should use a secure and strong master user password in a production scenario.

### S3 Buckets

Last but definitely not least, we have the [`AWS::S3::Bucket`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html) resource.

~~~{.yaml caption="cfn-template.yml"}
---
Description: CloudFormation Template for S3 Bucket
Resources:
  MyS3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-example-bucket
      AccessControl: Private
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: AES256
~~~

The important properties here include the `BucketName`, `AccessControl` policy, and `BucketEncryption` property. In this example, it sets the default server-side encryption algorithm to `AES256`.

## Tips for Managing AWS Resources

![Tips]({{site.images}}{{page.slug}}/tips.png)\

As you learn more about CloudFormation, you'll start to really expand your stacks. Whenever you add or update a resource in your stack, always use CloudFormation to make these changes. In other words, update your template instead of accidentally updating a resource's configuration directly in its service console. Making these out-of-band changes can cause resources to drift from their CloudFormation template configuration.

If your stack has drifted, you can use CloudFormation's [drift detection feature](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/detect-drift-stack.html) to correct these differences.

In addition, to prevent your stack from being accidentally deleted, you can enable [termination protection](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-protect-stacks.html). Once enabled, any attempt to delete the stack automatically fails. Moreover, you might consider configuring the [`DeletionPolicy`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-deletionpolicy.html) on specific resources in your stack. If you specify a `Retain` deletion policy on a resource, CloudFormation doesn't delete the resource even if the associated stack is deleted.

## Advanced CloudFormation Features

So far, you've only scratched the surface of what CloudFormation has to offer. For more advanced users, CloudFormation has a bunch of features that can give you additional flexibility when writing your templates and simplify your overall experience. Here are a few to take note of:

* [**Nested stacks**](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-nested-stacks.html) allow you to create modular templates and reference one template from another. This is crucial for managing complex templates and breaking them down into smaller components.
* [**Custom resources**](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources.html) enables you to define custom logic in your CloudFormation templates. Custom resources use Lambda under the hood, allowing you to essentially create resources that aren't natively supported by CloudFormation.
* [**Change sets**](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-changesets.html) provide a preview of changes that will be made to a CloudFormation stack before they're executed. This is great for reviewing larger infrastructure changes and ensuring that the output is what you expect.
* [**Stack policies**](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/protect-stack-resources.html) can help you restrict or allow specific actions on stack resources for different AWS Identity and Access Management (IAM) roles and users. Organizations often use this to have finer-grained access control within particular CloudFormation stacks.

## AWS CloudFormation Best Practices

Earlier in this article, you authored a CloudFormation template and deployed it using the console. While this workflow is not incorrect, it's also extremely manual—you wouldn't deploy production-level infrastructure like this. Instead, you should follow these best practices:

* **Integrate with continuous integration, continuous delivery (CI/CD) pipelines:** With CloudFormation, infrastructure deployments are essentially code deployments. That means you can incorporate CloudFormation into your CI/CD pipelines to automate and streamline deployments.
* **Organize templates:** CloudFormation is pretty verbose. To help keep templates manageable, break them into smaller components using nested stacks. Internally, you can also devise a folder structure to help you organize and categorize your templates.
* **Reuse templates:** One of the key tenets of CloudFormation and IaC is reusability. Wherever possible, try to create parameterized templates that can be customized for different regions or environments. In addition, consider using [CloudFormation StackSets](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/what-is-cfnstacksets.html) to deploy and manage stacks across multiple accounts and regions.
* **Enable error handling and debugging:** Besides adopting code review best practices, CloudFormation comes with tools to help you handle and safeguard against deployment errors. You can enable detailed CloudFormation stack event logging for enhanced debugging. You can also look into features such as [rollback triggers](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-rollback-triggers.html) to automatically trigger rollbacks if a specific condition isn't met during a stack operation.

## Conclusion

AWS CloudFormation is an intriguing IaC service offering so many features. If you're working with the AWS Cloud, picking up CloudFormation is an absolute must.

Fortunately, you covered a lot of ground in this article! You learned about authoring templates, deployed a stack involving multiple EC2 resources, and discovered advanced features and best practices that can help you make the most of this offering. The next step is to get your hands dirty with templates and take advantage of this powerful service.

[Earthly](https://earthly.dev/) is a build automation tool that you can use in conjunction with CloudFormation. With Earthly, you create Earthfiles that define the steps to build, test, and package your CloudFormation template files. Then you can incorporate Earthly commands within your CI/CD scripts to automate deployments, which is all in line with the CloudFormation best practices you learned. Overall, Earthly gives you greater automation and control over your CloudFormation build workflows—install it and try it out today.

{% include_html cta/bottom-cta.html %}
