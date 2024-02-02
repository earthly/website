---
title: "Mastering Terraform Variables: A Comprehensive Guide for Defining and Utilizing Variable Types"
categories:
  - Tutorials
toc: true
author: Mohammed Osman
editor: Muhammad Badawy

internal-links:
 - Terraform Variable
 - Terraform
 - Guide
 - Reusability
 - Automate
excerpt: |
    Learn all about Terraform variables and how to use them in this comprehensive guide. Discover the different variable types, their usage, and workarounds for their limitations. Whether you're new to Terraform or looking to enhance your skills, this article has got you covered.
last_modified_at: 2023-08-24
---
**This article summarizes Terraform variables. Earthly improves your CI/CD pipeline. Improve your cloud infrastructure. [Check it out](https://cloud.earthly.dev/login).**

[Terraform](https://www.terraform.io/) is a widespread [infrastructure-as-code (IaC)](https://en.wikipedia.org/wiki/Infrastructure_as_code) tool that lets you automate the provisioning and management of cloud resources using the [HashiCorp Configuration Language (HCL)](https://www.linode.com/docs/guides/introduction-to-hcl/).

Terraform's configuration language has many constructs, such as resources, data sources, modules, and variables. Variables are configurable parameters used in Terraform configuration files, allowing for more flexible and dynamic setups. They enable users to customize aspects of their infrastructure without altering the main configuration.

In this guide, you'll learn all about Terraform configuration variables, including the different variable types, their usage, and the different ways to assign and use them. You'll also learn about some of their limitations and how to work around them.

## Basics of Terraform Variables

There are two main benefits of using Terraform variables:

1. **Reusability:** By utilizing variables in your IaaC configuration, you can avoid hardcoding values such as instance type or region names directly. This flexible approach allows you to utilize the same configuration files across multiple environments (*ie* development, testing, and production) or with different settings simply by changing the assigned values to the variable.
2. **Security:** To minimize the risk of exposing sensitive data, it's recommended that you do not hardcode specific values, such as API keys and passwords, directly into your configurations. Instead, you should treat them as variables that can be dynamically provided when needed.

You declare a Terraform variable using the `variable` block. The label after the `variable` keyword is the variable's name, which should be unique across all the variables in the same module:

~~~{.tf caption=""}
variable "image_id" {
  type = string
}
~~~

A Terraform variable block supports several optional arguments. For instance, the `default` argument sets a variable's default value. And the `type` indicates what value types are accepted for the variable. In addition, the `description` specifies the variable documentation. For more information about optional arguments, check out the [official Terraform documentation](https://developer.hashicorp.com/terraform/language/values/variables#arguments).

As an example, the following code shows a `region` variable of the type `string`, a `default` value of `us-west-2`, and a `description`:

~~~{.tf caption=""}
variable "region" {
  description = "The AWS region where resources will be created"
  type  = string
  default  = "us-west-2"
}
~~~

## Variable Types and Usage

![Types]({{site.images}}{{page.slug}}/types.png)\

Terraform supports several types of variables, including environment variables, local variables, and input variables. Let's tTake an in-depth look at each:

### Environment Variables

Terraform utilizes [environment variables](https://developer.hashicorp.com/terraform/cli/config/environment-variables) to set different kinds of configurations at the system level, enabling changes in Terraform's behavior (such as adjusting debugging verbosity or storing secret information).

For example, the environment variable `TF_LOG` controls the logging level, `TF_WORKSPACE` sets the Terraform workspace, and `TF_LOG_PATH` specifies where the log files should persist.

You define a Terraform environment variable by giving it a name in the following format: `TF_VAR_name`, where `name` refers to the environment variable.

In Unix-based systems (such as Linux and macOS), you can define environment variables in the terminal using the export command:

~~~{.bash caption=">_"}
hcl export TF_VAR_region=us-west-2
~~~

In Windows, you define environment variables in the command prompt using this command:

~~~{.bash caption=">_"}
set TF_VAR_region=us-west-2
~~~

### Local Variables

Local variables in Terraform modules simplify complex expressions and increase the readability of your modules and are defined using the `locals` block. Here's an example:

~~~{.tf caption=""}
locals {
  instance_type = "t2.micro"
}
resource "aws_instance" "example" {
  instance_type = local.instance_type
  # Rest of config
}
~~~

In this example, you define the local variable `instance_type` and assign it the value `t2.micro` in the `locals` block. Then you reference the `instance_type` variable from the `example` resource. Notice that you need to put the qualifier `local` before the local variable name to access it.

### Input Variables

Input variables serve as parameters to the Terraform module to customize certain parts of the module without modifying the actual module source code. They can be defined in a separate `.tf` file within the module or as a command line argument unlike local variables, or `locals`, which are internal to a Terraform module and cannot be directly influenced from outside the module.

The supported input variable types are string, number, list, map, Boolean, and object variables.

In the following examples, you'll learn how you can define and use the different input variable types in Terraform modules.

#### String Variables

String variables are used to represent text values. The following code block defines a variable named `instance_type` of type `string` and has a `default` value of `t2.micro`. The variable is used in a Terraform `aws_instance` resource that has the name `example` to specify the type of AWS instance. The variable is accessed using the syntax `var.<variableName>`:

~~~{.tf caption=""}
variable "instance_type" {
  type  = string
  default = "t2.micro"
}
resource "aws_instance" "example" {
  instance_type = var.instance_type
  # Rest of config
}
~~~

#### Number Variables

Number variables are used to represent numerical values.

The following code block defines a variable named `instance_type` of type `number` and has a `default` value of `5`. The variable is used in a Terraform resource of type `aws_instance`, which has the name `example` to specify the count of the AWS instances:

~~~{.tf caption=""}
variable "instance_count" {
  type  = number
  default = 5
}
resource "aws_instance" "example" {
  count = var.instance_count
  # Rest of config
}
~~~

The count parameter in a resource block in Terraform allows you to create multiple instances of that resource. The variable `instance_count` is accessed using the syntax `var.<variableName>`.

#### List Variables

[List variables](https://developer.hashicorp.com/terraform/language/values/variables#list) represent a list sequence of values of a particular type and are used to create multiple resources or provide numerous arguments for a resource. They're used when you want to create multiple instances of a Terraform resource without rewriting the code multiple times.

The following code shows a list variable of a string type that is used to create multiple Amazon Web Services (AWS) subnets using the `count` parameter:

~~~{.tf caption=""}
variable "subnet_ids" {
  type  = list(string)
  default = ["subnet-abcde012", "subnet-bcde012a", "subnet-fghi345a"]
}
resource "aws_instance" "example" {
  count  = length(var.subnet_ids)
  subnet_id  = var.subnet_ids[count.index]
  # Rest of code
}
~~~

#### Map Variables

[Map variables](https://developer.hashicorp.com/terraform/language/values/variables#map) can create a collection of key-value pairs. They are used to dynamically set arguments based on a specific key.

For example, this code block shows a map variable of a string type that assigns `Environment` and `Team` keys to an AWS resource:

~~~{.tf caption=""}
variable "tag_values" {
  description = "Map of tags to assign to the resources"
  type  = map(string)
  default  = {
  Environment = "Development"
  Team  = "DevOps"
  }
}
resource "aws_instance" "example" {
  ami  = "ami-0c94855ba95c574c8"
  instance_type = "t2.micro"
  tags  = var.tag_values
}
~~~

#### Boolean Variables

[Boolean variables](https://developer.hashicorp.com/terraform/language/values/variables#bool) are used to indicate true or false values. They're used to conditionally create resources.

For example, this code shows an `is_prod` Terraform variable with the `default` value of `false`. The variable is used to conditionally decide the instance type and the environment tags of an AWS resource:

~~~{.tf caption=""}
variable "is_prod" {
  description = "Boolean flag indicating if the environment is production"
  type  = bool
  default  = false
}
resource "aws_instance" "example" {
  ami  = "ami-0c94855ba95c574c8"
  instance_type = var.is_prod ? "t2.large" : "t2.micro"
  tags = {
    Environment = var.is_prod ? "Production" : "Development"
  }
}
~~~

#### Object Variables

Object variables group related attributes together. For example, the following code shows a Terraform variable called `instance_config` containing configurations for the instance type, Amazon Machine Image (AMI), and key name:

~~~{.tf caption=""}
variable "instance_config" {
  description = "Configuration for the EC2 instance"
  type = object({
  instance_type = string
  ami  = string
  key_name  = string
  })
  default = {
    instance_type = "t2.micro"
    ami  = "ami-0c94855ba95c574c8"
    key_name  = "my_key_pair"
  }
}
resource "aws_instance" "example" {
  ami  = var.instance_config.ami
  instance_type = var.instance_config.instance_type
  key_name  = var.instance_config.key_name
}
~~~

## Using Terraform Variables

![Using]({{site.images}}{{page.slug}}/using.png)\

After you define the Terraform variables in your Terraform module, there are several ways to assign values to these variables, including the following:

- **Default values:** As you've already seen, `default` values can be used to assign default values to the variable in its `variable` block declaration.
- **Terraform modules:** Terraform variables can be referenced using this format: `var.<name>`.
- **Variable interpolation:** This method consists of using the variable name as part of another string (more on this in the following section).
- **Variable substitution in the CLI:** This involves setting the value of the Terraform variable as part of the command when running Terraform commands.
- **Terraform configuration files:** With this method, you set the variable values in [Terraform configuration files](https://spacelift.io/blog/terraform-tfvars). These files are typically called `terraform.tfvars` or `*.auto.tfvars`.

### Variable Interpolation

In Terraform, you can perform variable interpolation (also referred to as string interpolation, variable substitution, or variable expansion). Variable interpolation allows you to include a variable value within another string, ultimately, helping you build dynamic configuration values.

As an example, the following code shows a variable called `filename` and its usage as a string interpolation in a resource called `index` of type `local_file`, which creates a file in the operating system:

~~~{.tf caption=""}
variable "filename" {
  description = "The name of the file to be created"
  type  = string
  default  = "index"
}
resource "local_file" "index" {
  filename = "${var.filename}.txt"
  content  = "foo!"
}
~~~

This code creates a local file with the name `index.txt`. The `filename` property in the `local_file` resource is interpolated with the value of the defined variable `filename`. The `filename` variable is accessed in the string using the interpolation format: `${var.<variableName>}`.

### Variable Substitution in the CLI

In addition to using variable interpolation to include a variable value within another string, you can also override the values of the variables directly from the command line using the `-var` flag when running Terraform commands. This is commonly used in scripting and automation tasks.

For instance, in the following code block, you override the value of the variable `instance_type` to be equal to `t2.medium` when running `terraform apply` to apply the IaC changes:

~~~{.bash caption=">_"}
terraform apply -var 'instance_type=t2.medium'
~~~

### Terraform Configuration Files

In Terraform, you have the option to utilize configuration files to define variable values to your IaC. Say you have a `main.tf` file that defines an `AWS EC2` configuration like this:

~~~{.tf caption=""}
provider "aws" {
  region = var.region
}
resource "aws_instance" "example" {
  ami  = var.ami
  instance_type = var.instance_type
}
~~~

Here, the configuration uses `var.region`, `var.ami`, and `var.instance_type` variables to set the region, AMI, and instance type.

In addition, the configuration values can be provided in another configuration file named `terraform.tvfars` or any file ending with `.auto.tfvars`. Here's an example of a `terraform.tfvars` file:

~~~{.tf caption=""}
region  = "us-west-2"
ami  = "ami-0c94855ba95c574c8"
instance_type = "t2.micro"
~~~

When you run the `terraform apply` command to apply the changes to your infrastructure, Terraform automatically loads any files with the names `terraform.tfvars` or `*.auto.tfvars` and populates the corresponding variables.

Moreover, you can manually load variable files with different names using the `-var-file` flag when running `terraform apply` or `terraform plan`:

~~~{.bash caption=">_"}
terraform apply -var-file="variables.tfvars"
~~~

## Limitations of Variables and Workarounds

Despite their flexibility and maintainability, Terraform variables have some limitations that you should be aware of, including the following:

- **No built-in encryption:** Sensitive values stored in Terraform are not encrypted. This means you risk exposing them in logs, state files, or the console output. To work around this issue, you would need to use the `sensitive` optional argument in the variable declaration block to prevent Terraform from outputting the variable value.
- **Limited support for complex data types:** Although Terraform supports complex data types such as objects, they can be cumbersome to use, especially when debugging error messages, which can be cryptic. A workaround for this is to make the data structures as simple as possible or, in other words, make it in a flattened structure instead of in complex nested objects.

## Conclusion

In this article, you've learned about Terraform variables, their uses, and limitations. For a deeper understanding, check out the [official documentation](https://developer.hashicorp.com/terraform/language/values/variables) or [this detailed tutorial](https://upcloud.com/resources/tutorials/terraform-variables).

And if you love automation and want to streamline your build processes even further, you might want to check out [Earthly](https://cloud.earthly.dev/login). It's a powerful tool hat can complement your Terraform knowledge and enhance your overall development workflow.

{% include_html cta/bottom-cta.html %}
