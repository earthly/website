---
title: "Put Your Best Title Here"
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

Perviously I built a container that was contained full REST API and got it all working on AWS as a Lambda. But setting this up invovled just clicking around in AWS and occasionally using the AWS CLI.

Today, I'm going to port that whole setup to Terraform so that its easier to manage, reproduce and make changes to.

## What is TerraForm


## From Click Ops to GitOps

Failed tools:
https://github.com/GoogleCloudPlatform/terraformer
https://github.com/cycloidio/terracognita

## Installing

First I install terraform:brew install hashicorp/tap/terraform
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

After that, I need to setup ECR. It's where I push my container image to in CI and where the lambda pulls it from.

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
In the first line, you can see the keyword `resource` followed by `aws_ecr_repository` and `foo`. This is how you declare a terraform resource and a resource is a declaritive thing you want to setup in terraform. The first string is the resource type, `aws_ecr_repository` in this example and the second thing is the name you want to give it. The name is for your own reference and I'll be using it to refer to specific resources from within other resources coming very soon. 

Everything after that is a property of the resource and this whole thing is being written in HCL, hashicorp configuration langauge. It might make sense to know and understand HCL as you get deeper into terraform, but it's suffienceent for this tutorial to just think of it as fancy YAML.


...



```
### ECR

resource "aws_ecr_repository" "lambda-api" {
  encryption_configuration {
    encryption_type = "AES256"
  }

  image_scanning_configuration {
    scan_on_push = "false"
  }

  image_tag_mutability = "MUTABLE"
  name                 = "lambda-api"
}
```
The 


I can test this all out by first trying a plan, which will list the changes Terraform things it needs to apply:


That was easy! The way I found the 


```
resource "aws_ecr_repository" "lambda-api" {
  encryption_configuration {
    encryption_type = "AES256"
  }

  image_scanning_configuration {
    scan_on_push = "false"
  }

  image_tag_mutability = "MUTABLE"
  name                 = "lambda-api"
}
```



