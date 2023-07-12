---
title: "Pulumi vs Terraform"
categories:
  - Tutorials
toc: true
author: Alexander Yu
excerpt: |
    Learn about the differences between Pulumi and Terraform, two popular Infrastructure as Code (IaC) tools. Discover their functionality, learning curves, compatibility, modularity, and community support to help you decide which tool is best for your infrastructure needs.
internal-links:
 - just an example
 - Pulumi
 - Terraform
 - IaC tools
---
There once was a time when technicians manually provisioned application infrastructure. In recent years, as companies began rapidly expanding their infrastructure stacks, they began to realize the shortcomings of manual provisioning:  

* It's costly, since hiring a technician is expensive, and manual processes are time-consuming.
* It's inconsistent, since human errors are inevitable, and can cause unwanted discrepancies between stacks.
* It's not scalable since, as stacks grow, companies have to continually devote resources towards infrastructure management.

To address these shortcomings, the Infrastructure as Code (IaC) paradigm was created. The central idea of IaC is that developers can now use code to define their infrastructure stacks, rather than rely on manual provisioning. This dramatically reduced costs, led to more consistency across infrastructure stacks, and was highly scalable, all because infrastructure provisioning could now be largely automated.

There are many solutions out there that embody IaC, but this article will focus on two particular IaC tools that stand out: [Pulumi](https://www.pulumi.com/) and [Terraform](https://www.terraform.io/). In this article, these tools will be compared in terms of overall functionality, expected learning curve, community support, and other important considerations. This is crucial in helping you decide which IaC tool is better for you.

## Comparing Pulumi and Terraform

<img src="{{site.images}}{{page.slug}}/comparing.jpg">

[Terraform](/blog/kubernetes-terraform) is one of the most well-established IaC tools today. It's a [declarative](https://dev.to/ruizb/declarative-vs-imperative-4a7l) tool, which means you define what you want the final state of your infrastructure to look like, and Terraform will handle how to achieve that state. Terraform is often considered the default IaC tool of choice, especially among larger companies and organizations that have the resources to support the learning curve of [HashiCorp Configuration Language (HCL)](https://www.terraform.io/language), a Domain Specific Language (DSL) unique to Terraform.

Pulumi is a newer IaC tool that has been quickly gaining in popularity. Unlike Terraform, you don't have to learn a DSL in order to use it. Instead, Pulumi supports creating, deploying, and managing all your cloud infrastructure using common programming languages. Note that while you use an imperative language such as Python to create Pulumi files, Pulumi is still considered a declarative tool. However, due to this increased flexibility, Pulumi is often preferred by developers who are already very comfortable with one or more of [the supported languages](https://www.pulumi.com/docs/intro/languages/).

Terraform and Pulumi are open source tools that are very widely used in the industry. To help you determine which one best suits your needs, let's now look into specific factors that you'll want to consider.

## Functionality

<img src="{{site.images}}{{page.slug}}/functionality.png" width="80%" height="60%">

Both tools have the same base functionality: enabling you to easily define and deploy your infrastructure as code. However, because Terraform uses HCL, it naturally comes with more guidelines and restrictions. In contrast, Pulumi allows you to leverage existing concepts in languages, such as loops, classes, and data structures. It's also easier for developers to create built-in testing suites and use other extensions and libraries in their Pulumi programs. While Terraform has no built-in testing functionality, the Terraform CLI contains better tools for troubleshooting a corrupt state.

The open source nature of these tools gives the developer community the opportunity to influence which features get prioritized and delivered. In a clear illustration of this, due to high demand, Terraform launched the [Cloud Development Kit for Terraform](https://www.terraform.io/cdktf), which allows developers to use familiar languages, though it should be noted that the Terraform CDK is a newer tool in active development that, as of this writing, may not be production stable. Similarly, Pulumi launched [`tf2pulumi`](https://www.pulumi.com/tf2pulumi/), a tool that converts HCL into a language of your choice.

## Learning Curve

<img src="{{site.images}}{{page.slug}}/learningcurve.png" width="100%" height="60%">

If you're looking to quickly learn and use one of these tools, you'll probably find that Pulumi is easier to pick up. This is because Pulumi allows you to use your preferred programming language to define your infrastructure stacks—there's no need to learn a specific DSL. If you already know Python, Java, Node.js, Go, or .NET Core, you can get started with Pulumi right away. If you're familiar with Python, you can easily create an AWS DynamoDB table using Pulumi with the following code:

~~~{.bash caption=">_"}
import pulumi
import pulumi_aws as aws

ddb_table = aws.dynamodb.Table("ddb-table",
 attributes = [
  aws.dynamodb.TableAttributeArgs(
   name="Id",
   type="S",
  ),
 ],
 billing_mode = "PAY_PER_REQUEST",
 hash_key = "Id",
 read_capacity = 5,
 write_capacity = 5)
~~~

Note that this is all regular Python syntax. Pulumi has a plethora of code samples in every supported language in their documentation (for example, [it is the `dynamodb.Table` documentation](https://www.pulumi.com/registry/packages/aws/api-docs/dynamodb/table/)). To actually deploy your infrastructure, you'll need to become familiar with various [Pulumi CLI](https://www.pulumi.com/docs/reference/cli/) commands.

To get started with Terraform, you'll first have to become familiar with HCL syntax. Some developers consider this a significant extra hump to get over, but HCL is so widely adopted that it's always a useful skill to have. In addition, while HCL is like learning a new language, much of the syntax is relatively intuitive and simple. For example, to create the same DynamoDB table from the Pulumi example, you can use the following Terraform code:

~~~{.bash caption=">_"}
provider "aws" {
 region = "us-east-1"
}

resource "aws_dynamodb_table" "ddb_table" {
 name = "ddb_table"
 attribute {
  name = "Id"
  type = "S"
 }
 billing_mode = "PAY_PER_REQUEST"
 hash_key = "Id"
 read_capacity = "5"
 write_capacity = "5"
}
~~~

As you can see, this isn't too bad! As with Pulumi, Terraform documents all resource properties and provides multiple code examples in their official documentation (for example, [it is the `aws_dynamodb_table` documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/dynamodb_table)). To actually deploy your infrastructure, you'll also have to become familiar with various [Terraform CLI](https://www.terraform.io/cli/commands) commands.

At first glance, it's certainly true that Pulumi has a much easier learning curve because you can simply draw on your existing knowledge of a language. However, this doesn't mean that it's necessarily "better" than having to learn HCL. Because all Terraform files are written in HCL, any Terraform developer can automatically understand any Terraform file. A Pulumi developer who's unfamiliar with Go may not be able to understand a Pulumi file written in Go. While the learning curve for Terraform may be higher at the onset, it may be worth having everyone in your organization stick to a single DSL.

## Compatibility

Both tools are compatible with most operating systems (Windows, macOS, and Linux), and work well with all common cloud providers (AWS, Azure, Google Cloud, Kubernetes, OpenStack). Both tools are also compatible with most IDEs, although Terraform is at a slight disadvantage here because you'll need to download an external plugin. With Pulumi, you'll get all the inherent benefits of using an IDE, such as code completion and automatic syntax correction.

## Modularity

Infrastructure stacks can get big and complex. As such, it's always best practice to break them up into small, reusable chunks. Terraform natively supports this through the concept of [modules](https://learn.hashicorp.com/tutorials/terraform/module?in=terraform/modules), which is simply a set of Terraform files that you can reference in other areas of your HCL code. Pulumi supports this as well, since you can reuse any class, function, or package that you define in your Pulumi files.

## Community Support

<img src="{{site.images}}{{page.slug}}/community.jpg" width="100%" height="60%">

Both [Terraform](/blog/kubernetes-terraform) and Pulumi are updated frequently and have great support from their respective developer communities. However, Terraform is a more mature tool, and it has a significantly larger community. You'll likely have an easier time finding help for issues that you come across for Terraform compared to Pulumi. One data point that stands out at the time of this writing is the number of Stack Overflow questions tagged with [`terraform`](https://stackoverflow.com/questions/tagged/terraform) (12,983) versus [`pulumi`](https://stackoverflow.com/questions/tagged/pulumi) (317).  

## Conclusion

In this article, you've looked at a quick comparison of Terraform and Pulumi, two popular IaC tools. The following list summarizes the findings:

* **Functionality:** Terraform uses HCL and generally has better troubleshooting mechanisms to fix corrupted states. Pulumi uses familiar programming languages, which makes it easier for developers to add external libraries and implement built-in testing mechanisms.
* **Learning Curve:** If you're new to Terraform, you'll need to learn HCL. If you're new to Pulumi, you can use a programming language that you're already familiar with. However, other Pulumi developers may not necessarily be familiar with that language. Terraform developers will not run into this issue.
* **Compatibility:** Both Terraform and Pulumi are compatible with all major operating systems, cloud providers, and IDEs, though you'll need to install a plugin to use an IDE with Terraform.
* **Modularity:** Both Terraform and Pulumi support modularity.
* **Community Support:** Terraform has a larger developer base, but both tools have excellent documentation and many code examples.

So which tool should you use? [Terraform](/blog/kubernetes-terraform) is still considered the industry leader in IaC tools, but Pulumi is quickly rising in popularity. Both tools help you accomplish the same thing, so for most organizations and developers, this comes down to whether you're willing to invest your time and resources into learning HCL and Terraform. If you prefer the consistency of using HCL for your infrastructure and want a tool with a more robust community, Terraform is the way to go. If you need to optimize for efficiency and would prefer to use a language you're already comfortable with, Pulumi might be the better solution. Either tool will get you on the way to properly scaling your infrastructure code.

{% include_html cta/bottom-cta.html %}
