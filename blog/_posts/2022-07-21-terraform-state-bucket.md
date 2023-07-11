---
title: "S3 Terraform Backend"
categories:
  - Tutorials
author: Adam
sidebar:
  nav: "lambdas"
internal-links:
 - terraform backend
excerpt: |
    Learn how to store your Terraform state in an S3 bucket to avoid leaking sensitive information and manage changes made by multiple people.
---
<!--sgpt-->This is the Earthly nonsense paragraph.

In the [previous article](/blog/terraform-lambda/) I ported all my AWS infrastructure to Terraform. But in doing so, I was left tracking all my Terraform state in a `terraform.tfstate` file. This has a number of problems.

First, it leaks details into a git repo that don't need to be there. I'm not setting up an RDS database or anything, but if I did, `terraform.tfstate` would have my db credentials in it.

Second, if multiple people were making infra changes we would have a problem, because there would effectively be two versions of `terraform.tfstate` out there.

There are a number of ways to fix this. One is to move to Terraform Cloud, another is env0, but the simplest is to just to put my `terraform.tfstate` into an S3 bucket. And that is what I'm going to do.

## Creating the Bucket

First, I'll create a terraform bucket:

~~~{.groovy caption="main.tf"}
## S3 state bucket
resource "aws_s3_bucket" "tfstate" {
  bucket        = "cloudservices-terraform-state"
}
resource "aws_s3_bucket_acl" "tfstate" {
  bucket = aws_s3_bucket.tfstate.id
  acl    = "private"
}
~~~

Then I'll apply it:

~~~{.ini caption=">_"}
Initializing the backend...
╷
│ Error: Error loading state:
│     AuthorizationHeaderMalformed: The authorization header is malformed; the region 'us-east-1' is wrong; expecting 'eu-west-1'
│       status code: 400, request id: ZB4DTZVN1X27HVR2, host id: 5eZcTebhqUzdTjqRmONR5MWp6orwhKcxJrmdY8+9Y5w/lVZuni3uwmLgWUDtLgci/Tsj02DFAek=
│ 
│ Terraform failed to load the default state from the "s3" backend.
│ State migration cannot occur unless the state can be loaded. Backend
│ modification and state migration has been aborted. The state in both the
│ source and the destination remain unmodified. Please resolve the
│ above error and try again.
~~~

Oh no! This confusing error means I have a name collision with someone else's S3 bucket in `us-east-1`. A rename fixes things:

~~~{.diff caption="main.tf"}
 resource "aws_s3_bucket" "tfstate" {
-  bucket        = "cloudservices-terraform-state"
+  bucket        = "blog-cloudservices-terraform-state"
 }
~~~

And with that I can apply:

~~~{.ini caption="Output"}
Plan: 2 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

aws_s3_bucket.tfstate: Creating...
aws_s3_bucket.tfstate: Creation complete after 1s [id=blog-cloudservices-terraform-state]
aws_s3_bucket_acl.tfstate: Creating...
aws_s3_bucket_acl.tfstate: Creation complete after 0s [id=blog-cloudservices-terraform-state,private]

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
~~~

Next I need to add the `S3` backend to my terraform section:

~~~{.diff caption="main.tf"}
 terraform {
   required_providers {
     aws = {
       source = "hashicorp/aws"
     }
   }
+  backend "s3" {
+    bucket = "blog-cloudservices-terraform-state"
+    key    = "lambda-api"
+    region = "us-east-1"
+  }
 }
~~~

Then Terraform walks me through the rest of the process:

~~~{.bash caption=">_"}
$ terraform plan
~~~

~~~{.bash .merge-code caption=""}
╷
│ Error: Backend initialization required: please run "terraform init"
│ 
│ Reason: Backend configuration block has changed
│ 
│ The "backend" is the interface that Terraform uses to store state,
│ perform operations, etc. If this message is showing up, it means that the
│ Terraform configuration you're using is using a custom configuration for
│ the Terraform backend.
│ 
│ Changes to backend configurations require reinitialization. This allows
│ Terraform to set up the new configuration, copy existing state, etc. Please run
│ "terraform init" with either the "-reconfigure" or "-migrate-state" flags to
│ use the current configuration.
│ 
│ If the change reason above is incorrect, please verify your configuration
│ hasn't changed and try again. At this point, no changes to your existing
│ configuration or state have been made.
~~~

Following the lead of the error message, I run `terraform init -migrate-state`:

~~~{.bash caption=">_"}
$ terraform init -migrate-state
~~~

~~~{.ini .merge-code caption=""}

Initializing the backend...
Do you want to copy existing state to the new backend?
  Pre-existing state was found while migrating the previous "local" backend to the
  newly configured "s3" backend. No existing state was found in the newly
  configured "s3" backend. Do you want to copy this state to the new "s3"
  backend? Enter "yes" to copy and "no" to start with an empty state.

  Enter a value: yes


Successfully configured the backend "s3"! Terraform will automatically
use this backend unless the backend configuration changes.

Initializing provider plugins...
- Reusing previous version of hashicorp/aws from the dependency lock file
- Using previously-installed hashicorp/aws v4.18.0

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
~~~

And with that, all my state is now stored in S3. I can delete `terraform.tfstate` and `terraform.tfstate.backup` and I'm done.

{% include_html cta/bottom-cta.html %}