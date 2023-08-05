---
title: "Automating Infrastructure with Terraform Functions: Best Practices and Examples"
categories:
  - Tutorials
toc: true
author: Vivek Kumar Singh
editor: Ubaydah Abdulwasiu

internal-links:
 - automating infrastructure
 - terraform functions
 - automating with terraforms functions
 - best practices to automate
---

**We're [Earthly.dev](https://earthly.dev/). We make building software simpler and therefore faster using containerization. This article covers automating infrastructure using terraform functions. If you want to know more about building in containers, then [check us out](/).**

[Terraform](https://www.terraform.io/) is an open-source infrastructure as code (IaC) tool that enables developers and system administrators to define, provision, and manage cloud infrastructure using a declarative language. This powerful tool helps streamline the process of deploying and maintaining infrastructure, ensuring that resources are provisioned in a predictable and reproducible manner, ultimately improving collaboration, reducing human error, and increasing overall productivity.

One of Terraform's key features is its built-in functions that automate tasks in infrastructure management. These functions allow you to perform complex operations and calculations, making your code more flexible and reusable.

In this article, you'll learn more about Terraform functions and their practical implementation in infrastructure provisioning configurations. Additionally, you'll learn about some best practices that you can implement to help you efficiently manage and deploy infrastructure resources.

## Why You Need Terraform Functions

Terraform functions are crucial in dynamically determining values within your Terraform configurations at runtime. They enable you not only to calculate values and manipulate tasks but also to streamline repetitive tasks. Designed to be lightweight and efficient, Terraform functions are particularly well-suited for large-scale infrastructure automation projects.

Moreover, Terraform functions provide powerful capabilities for manipulating and transforming data within your configurations. Whether it's performing numerical operations utilizing string functions or managing file systems, these functions provide the necessary tools for enhanced flexibility and control in your Terraform workflow.

While Terraform functions provide a lot of flexibility and power, there are also some alternative approaches to consider. One alternative is using a different scripting language like Python or Ruby to perform complex operations outside your Terraform code. This allows for more flexibility and control, but introduces additional complexity and may require specialized knowledge.

Although predefined values can be fed into the configuration file, this approach may restrict the overall flexibility of your Terraform configuration. In such cases, runtime values can't be computed, limiting the dynamic nature of your runtime setup.

To execute the code snippets in this article, you must install Terraform locally on your system by following the official [Terraform installation](https://developer.hashicorp.com/terraform/downloads) guide. Alternatively, you can utilize an online Terraform playground to run the code examples in your browser.

## Types of Terraform Functions

Terraform functions are essential building blocks within the Terraform language that enable developers to express complex infrastructure requirements and automate infrastructure deployment. From mathematical operations to string manipulation and conditional logic, Terraform functions offer diverse capabilities, contributing to infrastructure automation's flexibility and extensibility. The following are types of terraform functions:

### String Functions

[String functions](https://developer.hashicorp.com/terraform/language/functions/chomp) help manipulate and transform string values. These functions are useful when working with variables, rendering templates, or constructing dynamic resource names. They allow developers to perform concatenation, substring extraction, case conversion, and regular expression matching operations.

For instance, in the following example, the `split` function divides a string into a list consisting of region, branch, and ID values. The `split` function specifies a separator, which can be any character, such as a space, comma, or hyphen. The string is then split at each occurrence of the separator, resulting in a list of individual elements.

In your Terraform playground window, add the following code:

~~~
variable "vm_data" {
    default = "north-B-08dh89"
}
~~~

In this code, a new variable, `vm-data`, is created. This stores the default value of `north-B-08dh89`. You can reference this variable in your code to use this value.

Now, append the following lines of code in the previous snippet:

~~~
locals {
   vm_vals = split("-", var.vm_data)
}
~~~

This code defines a local value named `vm_vals` using the `locals` block. The value `vm_vals` is assigned to the result of the `split` function applied to the variable `var.vm_data`. In this case, the split function returns a list of strings `["north", "B", "08dh89"]`, which can be accessed using indexes.

You can use this value in your resources in the Terraform configuration like this:

~~~
resource "aws_instance" "app"{
    region = local.vm_vals.value[0]
    branch = local.vm_vals.each.value[1]
    id     = local.vm_vals.each.value[2]

}
~~~

Here, a resource block is named `aws_instance` and labeled `app`. It creates an Amazon Web Services (AWS) instance whose configurations are defined using the element in the list `vm_vals`. You can see that utilizing the `split` function made it much easier to pull out each element from a hyphen-separated string.

### Collection Functions

In Terraform, the [collection function](https://developer.hashicorp.com/terraform/language/functions/alltrue) allows you to work with data structures such as lists, maps, and sets to perform operations like filtering, mapping, joining, and merging collections. These functions are especially useful when working with large data sets or when transforming and reshaping data structures to meet specific requirements.

Additionally, collection functions provide a convenient way to iterate over elements, apply transformations, and generate new collections based on the original data. However, when using collection functions excessively or in complex scenarios, use caution, as they can lead to decreased readability and maintainability of the Terraform code.

One of the scenarios in which collection functions are useful is when you want to sort the order of resources in your configuration using the `sort` collection function. Or you could reverse the order using the `reverse` function:

~~~
variable "servers" {
  type = list(string)
  default = ["ServerC", "ServerA", "ServerB"]
}
~~~

In this code, the `servers` variable is defined with a list type and provides a default value of `["ServerC", "ServerA", "ServerB"]`. To sort the elements in this variable, you can use the `sort` function:

~~~
locals {
    names = sort(var.servers)
}
~~~

Here, the local value `names` is assigned the sorted version of the `var.servers` variable. In this case, the `names` variable stores the value `["ServerA", "ServerB", "ServerC",]`.

You can also use the built-in function `reverse` to reverse the order of server names. To do this, modify the previous code like this:

~~~
locals {
    names = sort(var.servers)
    reversed_names = reverse(local.names)
}

~~~

This code creates a different `reversed_names` variable that stores the value returned by the `reverse` function. In this case, the value is `["ServerC", "ServerB", "ServerA"]`.

### Encoding Functions

[Encoding functions](https://developer.hashicorp.com/terraform/language/functions/base64decode) enable developers to encode and decode data using various encoding schemes, such as [Base64](https://developer.hashicorp.com/terraform/language/functions/base64encode) or [URL encoding](https://developer.hashicorp.com/terraform/language/functions/urlencode). They're particularly useful when working with sensitive information, such as credentials or secrets, as they ensure that data is properly encoded and can be safely used in configuration files or passed between resources. However, it's important to note that encoding functions should not be used as a substitute for encryption or strong security measures.

If you have some secret data in the configuration, you can use the `base64encode` function to transmit the data securely.

Run the following code in your Terraform console:

~~~
base64encode("secret_key")
~~~

Running this code returns the following output:

~~~
"c2VjcmV0X2tleQ=="
~~~

Here, you can see that the original string, `secret_key`, gets encoded in Base64 encoded form.

Terraform also has a `base64decode` function to decode the encoded string. Run the following code in your Terraform console:

~~~
base64decode("c2VjcmV0X2tleQ==")
~~~

With `base64decode`, you can see the original string:

~~~
secret_key
~~~

### File System Functions

[File system functions](https://developer.hashicorp.com/terraform/language/functions/abspath) are powerful when working with files and directories within the Terraform ecosystem. These functions allow developers to read, write, and manipulate files and directories as part of the infrastructure provisioning process.

File system functions are useful when generating or managing files dynamically. However, because Terraform is mainly designed for infrastructure provisioning, you should limit using file system functions.

In the following example, the `file` function in Terraform reads the contents of a specified file and returns them as a string. This can be useful when you need to use the contents of a file as input for a resource or data source in your Terraform configuration.

In your Terraform console, run the following code:

~~~
file("ip_addresses.txt")
~~~

Running the previous code returns the contents of the file in the console:

~~~
192.168.1.10
10.0.0.22
172.16.0.101
203.0.113.55
192.0.2.33
198.51.100.77
~~~

### Numeric Functions

Numbers play a significant role in programming languages, and Terraform is no exception. Within Terraform, you can access a range of built-in [numeric functions](https://developer.hashicorp.com/terraform/language/functions/abs) that you can call from within expressions to transform and combine values. These functions perform numerical operations, such as calculating the maximum, minimum, power/exponent, and logarithm.

For instance, numeric functions like `min` and `max` allow for dynamic decision-making in infrastructure provisioning. In the following example, the resource determines the `min_size` and `max_size` based on the values returned by the `min` and `max` functions.

Type the following code in your Terraform console:

~~~
variable "desired_capacity" {
  type        = number
  default     = 5
}
~~~

Here, you define a variable (*ie* `desired_capacity`) with a default value of `5`. You use this value to compare the autoscaling size after comparing it using the numeric functions. To do this, in the same console, write the following code:

~~~
resource "aws_autoscaling_group" "app" {
  name  = "my-autoscaling-group"
  min_size = min(var.desired_capacity, 2)
  max_size = max(var.desired_capacity * 2, 10)
}
~~~

In this code, a new resource (*ie* `aws_autoscaling_group`) is defined with two dynamically generated variables: `min_size` and `max_size`. The `min` function ensures the resource size does not exceed `2`. It returns the minimum value passed to the function as an argument. In comparison, the `max_size` variable does not go above `10`.

### Date and Time Functions

Terraform includes several built-in functions for working with [dates and times](https://developer.hashicorp.com/terraform/language/functions/formatdate). These functions allow you to perform date calculations, format timestamps, and schedule tasks for infrastructure provisioning.

In the following example, the `formatdate` and `timestamp` functions are used to convert a timestamp into a different date format.

Run the following code in your Terraform console:

~~~
formatdate("EEEE DD MMM YYYY", timestamp())
~~~

Your output should look like this:

~~~
"Thursday 15 Jun 2023"
~~~

The `formatdate` function has a lot of specification syntax to make it highly customizable. These specifications are listed on the [Terraform website](https://developer.hashicorp.com/terraform/language/functions/formatdate#specification-syntax).

### Hashing Functions

Terraform [hashing functions](https://developer.hashicorp.com/terraform/language/functions/base64sha256) help you generate hash values from input data within Terraform code. These functions enable you to generate unique identifiers or checksums based on the content of variables or resources.

Hashing functions are particularly useful when you need deterministic and unique values. They provide a reliable and consistent way to generate unique identifiers, even when the input data changes slightly. They can be used to encrypt admin passwords when receiving them from external resources. It is also used to hash the contents of a plaintext file.

In production systems, hashing functions are used to encrypt sensitive data like passwords while transmitting them. Unlike encoding functions, hash values cannot be retrieved to get the original string.

For instance, in the following example, the `admin_password` value undergoes a secure transformation utilizing the `sha256` hashing algorithm:

~~~
variable "admin_password" {
  description = "User password"
  default = "secretpassword"
}

resource "aws_db_instance" "database" {

  master_password = sha256(var.admin_password)
}
~~~

The resulting hash value is then assigned to the `master_password` attribute, which ensures that the sensitive information remains protected through encryption.

### IP Network Functions

When working with IP addresses and network-related operations within Terraform, there's a set of built-in [IP network functions](https://developer.hashicorp.com/terraform/language/functions/cidrhost) is available. These functions enable developers to manage IP addresses and calculate subnets and IP addresses for a given IP network address prefix.

For instance, when you need to provision a set of virtual machines within a subnet with a specific [CIDR block](https://www.techtarget.com/searchnetworking/definition/CIDR), you can use `cidrsubnet` to calculate the individual IP addresses for each machine within the subnet. To do so, open the Terraform console and add the following code:

~~~
variable "subnet_cidr_block" {
  description = "CIDR block for the subnet"
  default     = "10.0.0.0/24"
}

resource "aws_instance" "example" {
  count         = 3
  subnet_id     = aws_subnet.example.id

  private_ip = cidrsubnet(var.subnet_cidr_block, 8, count.index)
}

~~~

Here, the `cidrsubnet` function allocates a unique IP address from the specified subnet CIDR block for each instance. The `count.index` value ensures each instance receives a distinct IP address within the subnet.

### Type Conversion Functions

Terraform includes several built-in functions for performing [type conversions](https://developer.hashicorp.com/terraform/language/functions/can). These functions allow you to convert values from one type to another explicitly. However, explicit type conversions are rarely necessary in Terraform because it automatically converts types when required.

The most common type conversion use case involves using `try`. The `try` function handles potential null or undefined values. In the following example, you can see how the `try` function attempts to convert the data to a string but also provides a fallback value `"NA"` in case the conversion fails:

~~~
variable "data" {
    default = 156
}

locals {
    external_data = try(tostring(var.data), "NA")
}
~~~

## Conclusion

Terraform's built-in functions provide a powerful and flexible way to enhance your infrastructure provisioning code. These functions allow you to perform calculations, manipulate data, and dynamically generate configuration values within your Terraform code. With many functions available, you can easily tailor your infrastructure provisioning process to meet your needs.

In this article, you learned about the various built-in functions Terraform supports, including type conversion, hashing, and numeric. If you're looking to take your infrastructure provisioning to the next level, be sure to explore the many possibilities offered by Terraform's built-in functions. DevOps engineers can increase the efficiency of their workflows. Incorporating Terraform functions into infrastructure automation can significantly benefit the management and provisioning of resources.

## Outside Article Checklist

- [ ] Optional: Find ways to break up content with quotes or images


{% include_html cta/bottom-cta.html %}
