---
title: "Creating and Managing Infrastructure with Terraform Init, Plan, and Apply"
categories:
  - Tutorials
toc: true
author: Damaso Sanoja

internal-links:
 - Infrastructure
 - Terraform
 - Virtual Machines
 - Kubernetes
excerpt: |
    
---

**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. This article is on the basics of Terraform but if you're interested in a different approach to building and packaging software then [check us out](/).**

The rapid adoption of the multicloud paradigm has greatly increased the complexity of IT infrastructure management. Deploying virtual machines (VMs) and [Kubernetes](https://kubernetes.io/) on demand in any cloud is becoming the norm. The question is, how can you manage your infrastructure effectively?

To date, the answer is infrastructure as code (IaC), which is a DevOps-inspired methodology that uses code to declaratively manage and provision infrastructure. Some common use cases for IaC include automated provisioning and managing of multicloud and hybrid-cloud environments, deployment of disposable development environments, and the ability to audit and roll back infrastructure changes with relative ease. This brings us to the topic of this article: creating and managing infrastructure with `terraform init`, `terraform plan`, and `terraform apply`.

[Terraform](https://www.terraform.io/) is a powerful open source IaC tool that enables teams to automate and version control their infrastructure configurations, streamlining the process of configuring and maintaining infrastructure through code. This article aims to guide engineers who are dabbling in IaC to understand how to configure, deploy, and manage infrastructure using this versatile tool.

Start by reviewing the available options and requirements for installing Terraform.

## Installing Terraform

The [Terraform CLI](https://developer.hashicorp.com/terraform/cli/commands) is distributed as a [binary package](https://developer.hashicorp.com/terraform/downloads) available for Windows, Linux, macOS, FreeBSD, OpenBSD, and Solaris. It's easy to install using package managers like [Homebrew](https://brew.sh/) on macOS, [Chocolatey](https://chocolatey.org/) on Windows, or [Apt and Yum](https://www.tecmint.com/linux-package-managers/) on Linux.

<div class="notice--big--primary">
It's important to note that if you want to install [Terraform Enterprise](https://developer.hashicorp.com/terraform/enterprise), you need at least 10 GB of disk space on the root volume, 40 GB of disk space for the [Docker](https://www.docker.com/) data directory, 8 GB of system memory, and at least 4 CPU cores.
</div>

Once you've installed Terraform on your local machine, you can verify the installation by running the following command:

~~~{.bash caption=">_"}
% terraform -h
Usage: terraform [global options] <subcommand> [args]

The available commands for execution are listed below.
The primary workflow commands are given first, followed by
less common or more advanced commands.

Main commands:
  init          Prepare your working directory for other commands
  validate      Check whether the configuration is valid
  plan          Show changes required by the current configuration
  apply         Create or update infrastructure
  destroy       Destroy previously-created infrastructure

All other commands:
  console       Try Terraform expressions at an interactive command prompt
  fmt           Reformat your configuration in the standard style
  force-unlock  Release a stuck lock on the current workspace
  get           Install or upgrade remote Terraform modules
  graph         Generate a Graphviz graph of the steps in an operation
  import        Associate existing infrastructure with a Terraform resource
  login         Obtain and save credentials for a remote host
  logout        Remove locally-stored credentials for a remote host
  metadata      Metadata related commands
  output        Show output values from your root module
  providers     Show the providers required for this configuration
  refresh       Update the state to match remote systems
  show          Show the current state or a saved plan
  state         Advanced state management
  taint         Mark a resource instance as not fully functional
  test          Experimental support for module integration testing
  untaint       Remove the 'tainted' state from a resource instance
  version       Show the current Terraform version
  workspace     Workspace management

Global options (use these before the subcommand, if any):
  -chdir=DIR    Switch to a different working directory before executing the
                given subcommand.
  -help         Show this help output, or the help for a specified subcommand.
  -version      An alias for the "version" subcommand.
~~~

As you can see, this command lists the most commonly used commands in Terraform (more on this shortly). For more help installing Terraform, you can check out the [official documentation](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) where you'll find a video and an interactive tutorial.

With the installation out of the way, it's time to move on to creating your first configuration in Terraform.

## Terraform Configuration

![Configuration]({{site.images}}{{page.slug}}/conf.png)\

The IaC methodology revolves around using a declarative syntax to describe through code the desired infrastructure state. To that end, understanding Terraform's syntax is essential.

Terraform uses a syntax known as [HashiCorp Configuration Language (HCL)](https://github.com/hashicorp/hcl). This language was designed to be both human-readable and machine-friendly, which allows developers to easily describe resources and their configurations. Using well-defined building blocks in its syntax, HCL lets you define the desired infrastructure state without specifying the exact steps to achieve it. This enables DevOps teams to create complex configurations that are easy for all stakeholders to understand.

These building blocks include [providers](https://developer.hashicorp.com/terraform/language/providers), [resources](https://developer.hashicorp.com/terraform/language/resources), [data sources](https://developer.hashicorp.com/terraform/language/data-sources), and [modules](https://developer.hashicorp.com/terraform/language/modules).

### Terraform Providers

The `provider` block is a core element of the Terraform configuration because it allows you to manage and provision target infrastructure platforms, such as Amazon Web Services (AWS), Azure, or Google Cloud Platform. One of the advantages of Terraform is that it allows each provider to incorporate their own *resource types* and *data sources* (more on these soon). This allows Terraform to interact with the different components of that infrastructure seamlessly.

Following is an example where the provider is defined as AWS:

~~~{.bash caption=">_"}
provider "aws" {
    region = "us-east-1"
}
~~~

Notice how the region where the resource will be deployed (`us-east-1`) is defined between curly brackets. That's an AWS-specific attribute. You can learn more about the syntax of this block of code on the official [Terraform documentation](https://developer.hashicorp.com/terraform/language/providers). In addition, you can check out available Terraform providers in the [Terraform Registry](https://registry.terraform.io/browse/providers).

### Terraform Resources

After establishing the provider, you need to define what `resource` you want to deploy. [Resources](https://developer.hashicorp.com/terraform/language/resources/syntax) represent infrastructure objects, such as VMs, virtual networks, or DNS records. Here's an example that creates an AWS instance:

~~~{.bash caption=">_"}
resource "aws_instance" "web" {
  ami           = "ami-abcdef"
  instance_type = "t2.micro"
}
~~~

Note that the `resource` block declares both the resource type `aws_instance` and the desired resource name, `web`. Then the specific configuration arguments for that resource (*ie* `ami` and `instance_type`) are defined between curly brackets.

### Terraform Data Sources

Each cloud provider has its own distinctive set of data sources. [Data sources](https://developer.hashicorp.com/terraform/language/data-sources) allow users to fetch infrastructure information or data stored outside of Terraform and incorporate it into their configurations. Following is a sample data source block:

~~~{.bash caption=">_"}
data "aws_ami" "example" {
  most_recent = true

  owners = ["self"]
  tags = {
    Name   = "app-server"
    Tested = "true"
  }
}
~~~

This code allows you to use the `example` Amazon Machine Image (AMI) through the `aws_ami` data source.

### Terraform Modules

Modules are a concept that gives Terraform a lot of flexibility. If your setup is simple, you can define providers, resources, data stores, and more in a single `main.tf` file known as the *root module*. However, if your configuration is complex, you can use the principle of separation of concerns and split it into several `.tf` or `.tf.json` files stored in different directories, aka *child modules*.

That means you can use a single `main.tf` configuration file or a structure similar to this:

~~~{ caption=""}
.
└── tf/
    ├── main.tf
    ├── versions.tf
    ├── variables.tf
    ├── provider.tf
    ├── outputs.tf
    ├── data-sources.tf
~~~

In addition, you can also use a structure similar to the following if required:

~~~{ caption=""}
.
└── tf/
    ├── modules/
    │   ├── network/
    │   │   ├── main.tf
    │   │   ├── dns.tf
    │   │   ├── outputs.tf
    │   │   └── variables.tf
    │   └── data-sources/
    │       ├── main.tf
    │       ├── outputs.tf
    │       └── variables.tf
    └── applications/
        ├── backend/
        │   ├── env/
        │   │   ├── dev.tfvars
        │   │   └── production.tfvars
        │   └── main.tf
        └── frontend-app/
            ├── env/
            │   ├── dev.tfvars
            │   └── production.tfvars
            └── main.tf
~~~

Let's review the configuration files used here:

* **`main.tf`** is used to call other modules and data sources and to create resources.
* **`dns.tf`** is a special type of provider called the [DNS Provider](https://registry.terraform.io/providers/hashicorp/dns/latest/docs) that performs DNS updates for you.
* **`variables.tf`** is a file used for variables. Similar to other programming languages, HCL allows you to use variables. These variables are declared in `variables.tf` to be used in `main.tf`.
* **`outputs.tf`** contains the [outputs](https://developer.hashicorp.com/terraform/language/values) created by `main.tf`.
* **`versions.tf`** is used to define which [versions](https://developer.hashicorp.com/terraform/language/expressions/version-constraints) to use for both the provider and Terraform.
* **`.tfvars`** is used to define environment variables generally used by scripts. In this example, the development and production environments use different environment variables (*ie* `dev.tfvars` and `production.tfvars`).

One of the advantages of using variables and separate configuration files is that it makes it easier to reuse the code. For example, instead of hardcoding the provider attributes, you can create a `variables.tf` file like the following to define `aws_region` as `us-east-1`:

~~~{.bash caption=">_"}
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}
~~~

If you're looking to learn more, check out this article about [customizing Terraform configuration with variables](https://developer.hashicorp.com/terraform/tutorials/configuration-language/variables) or this one about [protecting sensitive input variables](https://developer.hashicorp.com/terraform/tutorials/configuration-language/sensitive-variables).

Now that you have a better idea of how to declaratively create modular and maintainable infrastructure, it's time to learn about the Terraform workflow.

## Terraform Workflow

Once you've written the Terraform configuration, the next logical step is to put the code into action. In the following sections, you'll explore the three stages used in the Terraform workflow: `terraform init`, `terraform plan`, and `terraform apply`. Each command plays an essential role in the workflow, so it's important that you understand the logic behind each one of them.

### `terraform init`

The first step of the workflow is to initialize Terraform's working directory. To do so, you can use the `terraform init` command. Running this command executes the following tasks:

* Configures the backend as specified in the `backend` block of the configuration.
* Downloads the versions of providers and modules specified in the configuration, specifically, in `variables.tf` files.
* Creates a `.terraform.lock.hcl` lock file, which includes the versions and hashes of the providers used during initialization.
* Creates a `.terraform` directory where the providers and modules used in the project are stored.

The purpose of the `terraform init` command is to set up the [Terraform backend](https://developer.hashicorp.com/terraform/language/settings/backends/configuration), modules, and providers. According to the documentation, Terraform uses the backend to store the [state](https://developer.hashicorp.com/terraform/language/state) of your managed infrastructure and configuration.

By default, Terraform uses a [local backend](https://developer.hashicorp.com/terraform/language/settings/backends/local), which stores the state locally in `terraform.tfstate`. However, when multiple individuals or teams need access to your infrastructure state data, it's recommended to use a [remote backend](https://developer.hashicorp.com/terraform/cdktf/concepts/remote-backends) or [Terraform Cloud backend](https://developer.hashicorp.com/terraform/language/settings/terraform-cloud).

Overall, thanks to the `init` step, Terraform achieves several principles of the IaC methodology, including the following:

* Facilitates keeping track of configuration changes using an SCM like Git.
* Ensures that all team members use the same versions of providers and modules stored in the `.terraform.lock.hcl` and `.terraform` directories.
* Streamlines troubleshooting initialization errors.

Regarding the last point, the command `terraform validate` is very helpful. The [`validate`](https://developer.hashicorp.com/terraform/cli/commands/validate) command verifies that the configuration is syntactically valid and internally consistent, regardless of any provided variables or existing state. This means running this command may give some hints about typos or other errors in your configuration.

If you want to practice using this command, check out the ["Initialize Terraform Configuration" tutorial](https://developer.hashicorp.com/terraform/tutorials/cli/init), which shows you how to deploy a container running Nginx locally.

Once the Terraform backend has been initialized and the `.terraform` directory has been created, it's time to run the `terraform plan` command.

### `terraform plan`

The purpose of the `terraform plan` command is very simple; it allows you to review the changes that will be made to the infrastructure once the `terraform apply` command is executed. If you're new to Terraform, you may be wondering what the point of this extra step is. Why not run `terraform apply` directly?

While you would be correct when making a few changes to the infrastructure, things can easily get out of hand when applying a complex configuration involving tens or even hundreds of changes.

Remember that you only have to define the final state of the infrastructure and that Terraform is responsible for determining what steps are necessary to achieve that goal. This means that depending on the complexity of the configuration, Terraform might accidentally delete resources that store vital data or take mission-critical services offline. This is why [creating a Terraform plan](https://developer.hashicorp.com/terraform/tutorials/cli/plan) is so important.

During this stage, your team can preview the actions Terraform would take to modify your infrastructure and fix any potential problems that may arise during execution. To that end, you can instruct Terraform to create a `tfplan` file using the `terraform plan -out tfplan` command.

This allows your team to verify resource changes without applying them. Once done, you can use the saved plan to run `terraform apply`, knowing that all changes have been reviewed and approved beforehand.

At this point, you've initialized the Terraform working directory and reviewed the changes to be made to the infrastructure. Now it's time to apply those changes using `terraform apply`.

### `terraform apply`

If you've followed along so far, you already know that the `terraform apply` command is used to make changes to your infrastructure. Such changes may involve creating new resources, updating current resources, or destroying them if they're no longer needed.

When you run `terraform apply`, the following tasks are performed:

* It preemptively locks the project state so that other Terraform instances or users cannot apply changes while the process is running. This makes sense since two or more instances could try to apply changes simultaneously.
* If `terraform plan` has not been run, it creates a plan and waits for user approval before continuing. This action seeks to prevent the issues discussed in the previous section.
* Once the previous tasks are completed, Terraform proceeds to execute the plan using the values defined in the configuration files as well as the modules and providers installed during the project initialization.
* After the plan has been executed, Terraform updates your project's state file to reflect the changes made to the resources. This file is then unlocked so that new changes can be applied.
* A report is printed onto the console with the changes made as well as the output values defined in its configuration.

Although the process is straightforward, there are still a few other aspects you need to understand.

If any errors are found during the `apply` step, Terraform proceeds to log those errors, update the state file with the changes made so far, and then unlock the file so that the rest of the changes can be executed once the issues are solved.

A simple example is shown in the [documentation](https://developer.hashicorp.com/terraform/tutorials/cli/apply) where Terraform fails to complete `terraform apply` because it references a Docker image that is no longer available in the registry. As explained in the documentation, in some cases, you only need to make the necessary adjustments to the configuration and run `terraform apply` again; after which, Terraform gives you the opportunity to confirm or cancel the proposed changes.

However, you may run into more complex issues during this stage, issues that require reverting changes to a known working state.

Rolling back changes is an advanced Terraform topic that is covered in-depth in a support article titled ["Terraform State Restoration Overview"](https://support.hashicorp.com/hc/en-us/articles/4403065345555-Terraform-State-Restoration-Overview). Basically, you have three alternatives:

1. Restore the last working state backup file.
2. Remove the bad resource from state and re-import the resource.
3. Replicate your setup locally, then perform a state push to override your remote backend's state file (extreme case; only for remote backends).

You may notice that all the solutions revolve around the state file, which is what you'll learn about next.

## Managing State in Terraform

![Managing]({{site.images}}{{page.slug}}/manage.png)\

Throughout this article, the concept of [state](https://developer.hashicorp.com/terraform/language/state) is frequently mentioned. This is because, in Terraform, state data files store information about infrastructure and configuration, mapping real-world resources to user-defined settings.

Consequently, whenever you run `terraform init`, `terraform plan`, or `terraform apply` commands, the saved state is referenced and updated with the latest resources and configuration at the end of the execution process.

State files facilitate change tracking, performance optimization for large infrastructures, and resource management. In addition, since state data files are stored in JSON format, they can be shared among team members if necessary.

Given the importance of the state data file, it's not recommended to manipulate it manually. Instead, the best practice when adding new resources to your infrastructure is to make the corresponding changes to the configuration files and follow the workflow explained in this guide (init, plan, and apply). However, there are special cases where you have to manipulate the Terraform state file, the most common one being importing existing infrastructure.

Explaining this advanced use case is beyond the scope of this guide. However, the documentation has a section that addresses [how to import Terraform configuration](https://developer.hashicorp.com/terraform/tutorials/state/state-import) in detail.

The following are the steps described in the documentation:

1. Identify the existing infrastructure you will import.
2. Import infrastructure into your Terraform state file.
3. Write Terraform configuration that matches that infrastructure.
4. Review the Terraform plan to ensure the configuration matches the expected state and infrastructure.
5. Apply the configuration to update your Terraform state.

## Conclusion

In this tutorial, we've covered the basics of Terraform workflow, including the init, plan, and apply stages, installation options, and syntax fundamentals.

Once you've mastered Terraform, you might want to take your build automation to the next level. Check out [Earthly](https://www.earthly.dev/) for an even smoother experience. You won't regret it!

{% include_html cta/bottom-cta.html %}
