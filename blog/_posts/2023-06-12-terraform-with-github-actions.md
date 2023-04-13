---
title: "Using Terraform with GitHub Actions"
categories:
  - Tutorials
toc: true
author: Keanan Koppenhaver

internal-links:
 - Terraform
 - Github Actions
 - CI/CD
 - Pipelines
---

[GitHub Actions](https://github.com/features/actions) is a powerful tool that allows software developers to automate almost everything inside a [GitHub](/blog/ci-comparison) repository. From running tests to linting your code, to automatically commenting on pull requests and issues, it's a complete solution that helps projects of all kinds to operate more efficiently.

If you're managing IT infrastructure, you're likely using [Terraform](https://www.terraform.io), a popular tool for managing infrastructure as code. Thankfully, GitHub Actions and Terraform can work together to create powerful, automated workflows for creating and maintaining even the most complicated deployments.

Using these tools together can help you automate your Terraform pipelines, which is important for making sure they run as frequently and consistently as you would like them to, making your pipelines more repeatable and reliable.

In this article, you'll learn how GitHub Actions and [Terraform](/blog/kubernetes-terraform) work together so that you can benefit from this powerful combination.

## Using Terraform and GitHub Actions Together

If you're an experienced developer looking to better understand how to use Terraform and GitHub Actions, this tutorial is for you. This means you should already have some knowledge about [what Terraform is](https://developer.hashicorp.com/terraform/intro) and how it works to provision infrastructure. In addition, you should have a basic idea of how GitHub Actions [helps developers automate tasks within their repos](https://docs.github.com/en/actions/learn-github-actions/understanding-github-actions).

### Prerequisites

Before you begin, you'll need the following:

- **A GitHub account:** GitHub is where you will store the code used for this project and where you will run your automation through GitHub Actions. If you don't already have an account, [sign up now](https://github.com/signup). You can take a look at the code that goes along with this tutorial in this [repository](https://github.com/kkoppenhaver/terraform-github-actions).
- **An [Amazon Web Services (AWS) account](https://aws.amazon.com/account/) and credentials:** Here, you'll be using resources that fall under the [AWS free plan](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=*all&awsf.Free%20Tier%20Categories=*all); however, if your account does not qualify for the AWS free plan, following this tutorial might incur some charges in your AWS account, so proceed with care.
- **[A Terraform Cloud account](https://app.terraform.io/public/signup/account):**  Since this tutorial uses Terraform Cloud to create your infrastructure configuration, you'll need to have a Terraform Cloud account before you begin.

Once you have all these accounts set up, you're ready to get started.

### Setting Up Terraform Cloud

When you first set up your Terraform Cloud account and log in, you'll start by creating an organization. An organization is an entity that will hold the workspace that you'll be creating. The organization allows you to collaborate with others and establish an internal workflow that streamlines the process of managing your infrastructure.

Next, you need to create a new workspace and make sure to select **API-driven workflow** when choosing the type. This will ensure that GitHub Actions is able to connect to Terraform later on:

![A screenshot showing the setup of a Terraform Cloud Workspace]({{site.images}}{{page.slug}}/iXfO755.png)

Next, you need to name your workspace. In this example, the workspace is named "ghactions-terraform-demo". This will create an empty workspace.

Next, you need to add your AWS secrets (*ie* `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`) to your Terraform workspace under the **Variables** section of the sidebar. Make sure you add them as sensitive variables so that only Terraform can use them to authenticate with AWS.

![Environment variables after getting added to Terraform Cloud]({{site.images}}{{page.slug}}/tXveUyy.png)

Once you have all that configured, head over to the [**Tokens** page](https://app.terraform.io/app/settings/tokens) and generate an API token. This is what you'll use to connect GitHub Actions to [Terraform](/blog/kubernetes-terraform) Cloud, so make sure you store this information in a safe place.

### Creating a GitHub Repository and Configuring Your Action

Now that you've set up Terraform and your API tokens are stored somewhere, head over to [GitHub](/blog/ci-comparison) and [set up a new repository](https://github.com/new).

Once you have your repository set up, go to **Settings > Secrets and Variables > Actions** and create a new secret. This is where you need to add the API key you retrieved from Terraform in the previous step. In this example, the secret is `TERRAFORM_API_KEY`, but you can name it whatever you like. If you're using the sample code as a reference, ensure that you replace the name of the secret with whatever you have named yours:

![A screenshot showing a properly configured Terraform API key as a GitHub secret]({{site.images}}{{page.slug}}/QGrJluJ.png)

Now, you can clone your repository to your local system and create two important files within the directory that you just cloned down from GitHub: `.github/workflows/terraform.yml` and `main.tf`.

To fill the contents of these files, you can use the [Terraform example repo](https://github.com/hashicorp/learn-terraform-github-actions), but here's an explanation of the content in each piece:

#### Terraform.yml

This is the actual file that your GitHub action will run through every time it's triggered. There are a few important code snippets in this file:

~~~
on:
  push:
    branches:
      - main
~~~

This defines what triggers your workflow. In this case, your workflow is only triggered when code is pushed to the main branch or when any pull requests to the main branch are merged:

~~~
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

Now that you have everything configured, it's time to make sure your GitHub action runs and provisions your resources with Terraform.

Create a new branch in your GitHub repository or locally via the command line. Inside this branch, navigate to your `main.tf` file and replace the `organization` and the `workspace` parameter value from the default placeholder `REPLACE_ME` with the actual organization and workspace names you created in Terraform Cloud earlier. Then commit and push your branch to GitHub:

![Replacing the placeholders for `organization` and `workspace` name]({{site.images}}{{page.slug}}/p9AOwD8.png)

Once you push your branch, create a pull request (PR) against the main branch of your codebase with your changes and replacements. You'll be able to see the output of the Terraform plan inside your PR, informing you of what resources will be created and/or destroyed with that particular PR. At this point, no action has been taken yet, but this offers a preview of what will happen once the PR is merged:

![GitHub Actions info on a PR within the repository]({{site.images}}{{page.slug}}/XhkC0K1.png)

> **Please note:** If you get an error when your action runs, head over to your GitHub Actions settings and make sure that GitHub Actions has read and write permissions enabled for your repository:

![A correctly configured settings page for GitHub Actions permissions]({{site.images}}{{page.slug}}/L6Hsktr.png)

Once the GitHub action successfully runs on your pull request, you can merge the pull request into the `main` branch and Terraform will provision your infrastructure.

### Verify That the EC2 Instance Was Provisioned

Once your pull request is merged and your infrastructure is provisioned, clicking on the GitHub action will show you all the information about the infrastructure you are creating or modifying:

![Terraform output inside of GitHub Actions]({{site.images}}{{page.slug}}/KeD9WyT.png)

If you're using the infrastructure only for testing purposes and want to avoid charges for the provisioned infrastructure, consider deleting the AWS instance once you've confirmed that it has been provisioned.

## Conclusion

Now that you have a taste for automatically provisioning infrastructure, you could make your `main.tf` file much more complicated and provision all sorts of different resources. Load balancers, databases, and more are now all within your reach using the combination of [GitHub Actions](https://github.com/features/actions) and [Terraform](https://www.terraform.io).

And if you're looking to continue building out your automation pipeline, consider using [Earthly](https://earthly.dev), a continuous integration, continuous delivery (CI/CD) platform that runs everywhere. Earthly makes [CI/CD](/blog/ci-vs-cd) easy and [works natively with GitHub Actions](https://docs.earthly.dev/ci-integration/vendor-specific-guides/gh-actions-integration), so it couldn't be easier to get started.

{% include_html cta/cta2.html %}


## Outside Article Checklist

- [ ] Create header image in Canva
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
  - Would any images look better `wide` or without the `figcaption`?
