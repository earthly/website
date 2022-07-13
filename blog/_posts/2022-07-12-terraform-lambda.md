---
title: "From Click Opps to Terraform"
categories:
  - Tutorials
toc: true
author: Adam

internal-links:
 - just an example
---
### Writing Article Checklist

- [ ] Write Outline
- [ ] Write Draft
- [ ] Fix Grammarly Errors
- [ ] Read out loud
- [ ] Write 5 or more titles and pick the best on
- [ ] First two paragraphs: What's it about? Why listen to you?
- [ ] Create header image in Canva
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
- [ ] Run mark down linter (`lint`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `link-opp` and find 1-5 places to incorporate links to other articles
- [ ] Add Earthly `CTA` at bottom `{% include cta/cta1.html %}`
- [ ] Raise PR
<!-- vale off -->

Previously I built a container that was contained full REST API and got it all working on AWS as a Lambda. But setting this up invovled just clicking around in AWS and occasionally using the AWS CLI.

Today, I'm going to port that whole setup to Terraform so that its easier to manage, reproduce and make changes to.

## What is TerraForm

## From Click Ops to GitOps

## Installing

First I install terraform:

```
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
```

Then I create a `main.tf` for my teraform config:

```
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}
```

Above, I'm pulling in the terraform AWS provider and setting my region. After that I can then `init` things:

```
terraform init
```

```
Initializing the backend...

Initializing provider plugins...
- Finding latest version of hashicorp/aws...
- Installing hashicorp/aws v4.22.0...
- Installed hashicorp/aws v4.22.0 (signed by HashiCorp)

Terraform has created a lock file .terraform.lock.hcl to record the provider
selections it made above. Include this file in your version control repository
so that Terraform can guarantee to make the same selections by default when
you run "terraform init" in the future.

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
```

Terraform then creates `.terraform.lock.hcl` file.
```
# This file is maintained automatically by "terraform init".
# Manual edits may be lost in future updates.

provider "registry.terraform.io/hashicorp/aws" {
  version = "4.18.0"
  hashes = [
    ...
  ]
}
```

`.terraform.lock.hcl` is a lock file. I check this into git, and then the hashes ensure that the provider I've using doens't change without me knowing it, even if run in some other place at some future date. 

## Plan And Apply

I don't actually have anything besides a provider declared in my terraform file, but never the less, I can still go thru the whole terraform process to make sure everything is ok. 

First I run plan:

```
terraform plan
```
```
No changes. Your infrastructure matches the configuration.

Terraform has compared your real infrastructure against your configuration and found no differences,
so no changes are needed.
```

Then I can apply the changes, just to be sure:

```
terraform apply 
```
```
No changes. Your infrastructure matches the configuration.

Terraform has compared your real infrastructure against your configuration and found no differences,
so no changes are needed.

Apply complete! Resources: 0 added, 0 changed, 0 destroyed.
```

Even though no changes were applied, and I don't yet have any resources being managed by Terraform I do have a new file. 

```
$ git status
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        terraform.tfstate

no changes added to commit (use "git add" and/or "git commit -a")
```

## How State Works in Terraform

Terraform is declarative. You describe the end result of the state of the infrastructure you would like to see and Terraform makes it happen. But to get from your declarative specification to list of changes to 'terraform apply` the current state of the world must be captured. 

Terraform stores this state in `terraform.tfstate`. At this point I have no resources being mangaged by Terraform so my `.tfstate` is pretty small.

```
{
  "version": 4,
  "terraform_version": "1.2.3",
  "serial": 1,
  "lineage": "9880ec52-a487-5a8e-db65-c4bc3949ba18",
  "outputs": {},
  "resources": []
}

```


Ok, lets move on to creating my first resource. I need to setup ECR. It's where I push my container image to in CI and where the lambda pulls it from.

## Elastic Computer Repository - Terraform

To create a ECR Repository in Terraform, I just googled "ECR Terraform" and ended up on the terraform docs where I found the following resource description:

```
resource "aws_ecr_repository" "foo" {
  name                 = "bar"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}
```

## Understanding Terraform Resources

In the first line, you can see the keyword `resource` followed by `aws_ecr_repository` and `foo`. This is how you declare a terraform resource and a resource is a declaritive thing you want to setup in terraform. The first string is the resource type, `aws_ecr_repository` in this example and the second thing is the name you want to give it. The name is for your own reference and I'll be using it to refer to specific resources from within other resources coming very soon. 

Everything after that is a property of the resource and this whole thing is being written in HCL, hashicorp configuration langauge. It might make sense to know and understand HCL as you get deeper into terraform, but it's suffienceent for this tutorial to just think of it as fancy YAML.


## Side Note: AWS Provider

The AWS provider will need a way to talk to your AWS account. If you don't have AWS credentials properly setup you may get an error like this:
```
terraform plan
╷
│ Error: error configuring Terraform AWS Provider: no valid credential sources for Terraform AWS Provider found.
```

If the credentials you have are wrong, the error will be a little bit different:

```
Error: error configuring Terraform AWS Provider: error validating provider credentials: error calling sts:GetCallerIdentity: operation error STS: GetCallerIdentity, https response error StatusCode: 403, RequestID: e816a4d9-6f28-49ef-b245-395c3a758f4a, api error InvalidClientTokenId: The security token included in the request is invalid.
```

To debug this you need to understand that the aws provider reads from `~/.aws/confg` and `~/.aws/credentials`, the same way the `aws` cli does. If you have credentials for more than one AWS account available, you can use `AWS_PROFILE` to configure the AWS provider. In my case I do this like so:
```
$ export AWS_PROFILE=earthly-dev
```

It's also possible to configure the profile in terraform by adding it under provider configuration:
```
 provider "aws" {
   region = "us-east-1"
+  profile = "earthly-dev"
 }
```

## ECR & Terraform import

So to add in my Repository for my image I create the following resource
```
### ECR

resource "aws_ecr_repository" "lambda-api" {
  image_tag_mutability = "MUTABLE"
  name                 = "lambda-api"
}
```
And running `terraform plan` I get this:

```
Terraform used the selected providers to generate the following execution plan.
Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # aws_ecr_repository.lambda-api will be created
  + resource "aws_ecr_repository" "lambda-api" {
      + arn                  = (known after apply)
      + id                   = (known after apply)
      + image_tag_mutability = "MUTABLE"
      + name                 = "lambda-api"
      + registry_id          = (known after apply)
      + repository_url       = (known after apply)
      + tags_all             = (known after apply)
    }

Plan: 1 to add, 0 to change, 0 to destroy.
```

There is a potential problem here though. I've already setup this repository in AWS. Terraform only tracks the state of resources it is managing, but I created a repository with this same name in the UI. How is this going to work.

```
terraform apply --auto-approve
```
```
Plan: 1 to add, 0 to change, 0 to destroy.
aws_ecr_repository.lambda-api: Creating...
╷
│ Error: failed creating ECR Repository (lambda-api): RepositoryAlreadyExistsException: The repository with name 'lambda-api' already exists in the registry with id '459018586415'
│ 
│   with aws_ecr_repository.lambda-api,
│   on main.tf line 14, in resource "aws_ecr_repository" "lambda-api":
│   14: resource "aws_ecr_repository" "lambda-api" {
│ 
╵
```




## Notes

Failed tools:
https://github.com/GoogleCloudPlatform/terraformer
https://github.com/cycloidio/terracognita