---
title: "Using Terraform with GitHub Actions"
categories:
  - Tutorials
toc: true
sidebar:
  nav: github-actions
author: Keanan Koppenhaver
editor: Mustapha Ahmad Ayodeji
last_modified_at: 2023-06-26
internal-links:
 - Terraform
 - Github Actions
 - CI/CD
 - Pipelines
excerpt: |
    Learn how to automate your Terraform pipelines using GitHub Actions, creating powerful and reliable workflows for managing infrastructure as code. This tutorial guides you through the process of setting up Terraform Cloud, configuring your GitHub repository, and running your GitHub Actions workflow to provision and maintain your infrastructure.
---
**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster. This article is about GitHub Actions, if you'd like to see how Earthly can improve your GitHub Actions builds then [check us out](/earthly-github-actions).**

GitHub Actions is a powerful tool that allows software developers to automate almost everything inside a GitHub repository. From running tests to linting your code, to automatically commenting on pull requests and issues, it's a complete solution that helps projects of all kinds to operate more efficiently.

If you're managing IT infrastructure, you're likely using Terraform, a popular tool for managing infrastructure as code. Thankfully, GitHub Actions and Terraform can work together to create powerful, automated workflows for creating and maintaining even the most complicated deployments.

Using these tools together can help you automate your Terraform pipelines, which is important for making sure they run as frequently and consistently as you would like them to, making your pipelines more repeatable and reliable.

In this article, you'll learn how GitHub Actions and Terraform work together so that you can benefit from this powerful combination.

## Using Terraform and GitHub Actions Together

![Together]({{site.images}}{{page.slug}}/together.png)\

If you're an experienced developer looking to better understand how to use Terraform and GitHub Actions, this tutorial is for you. This means you should already have some knowledge about what Terraform is and how it works to provision infrastructure. In addition, you should have a basic idea of how GitHub Actions works.

### Prerequisites

Before you begin, you'll need the following:

- **A GitHub account:** GitHub is where you will store the code used for this project and where you will run your GitHub Actions workflow. You can take a look at the code that goes along with this tutorial in this [repository](https://github.com/kkoppenhaver/terraform-github-actions).
- **An Amazon Web Services (AWS) account and credentials:** Here, you'll be using resources that fall under the AWS free plan; however, if your account does not qualify for the AWS free plan, following this tutorial might incur some charges in your AWS account, so proceed with care.
- **[A Terraform Cloud account](https://app.terraform.io/public/signup/account):**  Since this tutorial uses Terraform Cloud to create your infrastructure configuration, you'll need to have a Terraform Cloud account before you begin.

Once you have all these accounts set up, you're ready to get started.

### Setting Up Terraform Cloud

When you first set up your Terraform Cloud account and log in, you'll start by creating an organization. An organization is an entity that will hold the workspace that you'll be creating. The organization allows you to collaborate with others and establish an internal workflow that streamlines the process of managing your infrastructure.

Next, you need to create a new workspace and make sure to select **API-driven workflow** when choosing the type. This will ensure that GitHub Actions is able to connect to Terraform later on:

<div class="wide">
![A screenshot showing the setup of a Terraform Cloud Workspace]({{site.images}}{{page.slug}}/iXfO755.png)
</div>

Next, you need to name your workspace. In this example, the workspace is named "ghactions-terraform-demo". This will create an empty workspace.

Next, you need to add your AWS secrets (*ie* `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`) to your Terraform workspace under the **Variables** section of the sidebar. Make sure you add them as sensitive variables so that only Terraform can use them to authenticate with AWS.

<div class="wide">
![Environment variables after getting added to Terraform Cloud]({{site.images}}{{page.slug}}/tXveUyy.png)
</div>

Once you have all that configured, head over to the [**Tokens** page](https://app.terraform.io/app/settings/tokens) and generate an API token. This is what you'll use to connect GitHub Actions to Terraform Cloud, so make sure you store this information in a safe place.

### Creating a GitHub Repository and Configuring Your Action

Now that you've set up Terraform and your API tokens are stored somewhere, head over to GitHub and set up a new repository.

Once you have your repository set up, go to **Settings > Secrets and Variables > Actions** and create a new secret. This is where you need to add the API key you retrieved from Terraform in the previous step. In this example, the secret is `TERRAFORM_API_KEY`, but you can name it whatever you like. If you're using the sample code as a reference, ensure that you replace the name of the secret with whatever you have named yours:

<div class="wide">
![A screenshot showing a properly configured Terraform API key as a GitHub secret]({{site.images}}{{page.slug}}/QGrJluJ.png)
</div>

Now, you can clone your repository to your local system and create two important files within the directory that you just cloned down from GitHub: `.github/workflows/terraform.yml` and `main.tf`.

To fill the contents of these files, you can use the [Terraform example repo](https://github.com/hashicorp/learn-terraform-github-actions), but here's an explanation of the content in each piece:

#### Terraform.yml

This is the actual file that your GitHub action will run through every time it's triggered. There are a few important code snippets in this file:

~~~{.yml caption="terraform.yml"}
on:
  push:
    branches:
      - main
~~~

This defines what triggers your workflow. In this case, your workflow is only triggered when code is pushed to the main branch or when any pull requests to the main branch are merged:

~~~{.yml caption="terraform.yml"}
- name: Setup Terraform
        uses: hashicorp/setup-terraform@v1
        with:
          # terraform_version: 0.13.0:
          cli_config_credentials_token: ${{ secrets.TERRAFORM_API_KEY }}
~~~

This is where GitHub Actions sets up the Terraform CLI and uses your Terraform API key to get everything configured to provision your infrastructure. If you named your secret in GitHub something different, this is where you need to replace that name.

The rest of the workflow file goes through the remainder of the Terraform configuration and applies the configuration specified in `main.tf`, which sets up and deploys a micro Amazon Elastic Compute Cloud (Amazon EC2) server on AWS.

#### Main.tf

There are a few key sections of the `main.tf` that will help you understand how Terraform is going to provision your infrastructure:

- The `terraform` block has all the information about what version of Terraform is running, the information needed to connect this workflow to Terraform Cloud and information about any other dependencies that this particular configuration has.
- The `data "aws_ami" "ubuntu"` block tells Terraform and AWS which operating system and Amazon Machine Image (AMI) to install on the newly-created instance.
- The `resource "aws_instance" "web"` block determines what commands are run on the AWS instance after it's provisioned by Terraform.

Together, this is all the configuration information needed for your GitHub Actions workflow to execute the provisioning of a new cloud resources via Terraform.

### Let's Test It

![Test]({{site.images}}{{page.slug}}/test.png)\

Now that you have everything configured, it's time to make sure your GitHub action runs and provisions your resources with Terraform.

Create a new branch in your GitHub repository or locally via the command line. Inside this branch, navigate to your `main.tf` file and replace the `organization` and the `workspace` parameter value from the default placeholder `REPLACE_ME` with the actual organization and workspace names you created in Terraform Cloud earlier. Then commit and push your branch to GitHub:

<div class="wide">
![Replacing the placeholders for `organization` and `workspace` name]({{site.images}}{{page.slug}}/p9AOwD8.png)
</div>

Once you push your branch, create a pull request (PR) against the main branch of your codebase with your changes and replacements. You'll be able to see the output of the Terraform plan inside your PR, informing you of what resources will be created and/or destroyed with that particular PR. At this point, no action has been taken yet, but this offers a preview of what will happen once the PR is merged:

<div class="wide">
![GitHub Actions info on a PR within the repository]({{site.images}}{{page.slug}}/XhkC0K1.png)
</div>

> **Please note:** If you get an error when your action runs, head over to your GitHub Actions settings and make sure that GitHub Actions has read and write permissions enabled for your repository:

<div class="wide">
![A correctly configured settings page for GitHub Actions permissions]({{site.images}}{{page.slug}}/L6Hsktr.png)
</div>

Once the GitHub action successfully runs on your pull request, you can merge the pull request into the `main` branch and Terraform will provision your infrastructure.

### Verify That the EC2 Instance Was Provisioned

Once your pull request is merged and your infrastructure is provisioned, clicking on the GitHub action will show you all the information about the infrastructure you are creating or modifying:

<div class="wide">
![Terraform output inside of GitHub Actions]({{site.images}}{{page.slug}}/KeD9WyT.png)
</div>

If you're using the infrastructure only for testing purposes and want to avoid charges for the provisioned infrastructure, consider deleting the AWS instance once you've confirmed that it has been provisioned.

## Conclusion

Now that you have a taste for automatically provisioning infrastructure, you could make your `main.tf` file much more complicated and provision all sorts of different resources. Load balancers, databases, and more are now all within your reach using the combination of GitHub Actions and [Terraform](/terraform-lambda).

And if you're looking to continue building out your automation pipeline, consider using [Earthly](https://earthly.dev). Earthly runs everywhere, including GitHub Actions and can improve the reliability of your CI/CD pipelines. It works great with [GitHub Actions](/earthly-github-actions) and Terraform.

{% include_html cta/gha-cta1.html %}
