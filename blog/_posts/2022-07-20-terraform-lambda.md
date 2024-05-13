---
title: "Terraform Import - Leaving Click Ops Behind"
categories:
  - Tutorials
toc: true
sidebar:
  nav: "lambdas"
author: Adam

internal-links:
 - terraform import
excerpt: |
    Learn how to import existing infrastructure into Terraform and manage it as code. Follow along as the author imports resources such as AWS Lambda, ECR, S3, and API Gateway, and tests the infrastructure by destroying and recreating it.
last_modified_at: 2023-07-14
---
**The article summarizes how to import infrastructure into Terraform. Earthly provides DevOps professionals with consistent build environments. [Check it out](https://cloud.earthly.dev/login).**

## From Click Ops To GitOps

Previously I built a [REST API](/blog/aws-lambda-api-proxy/), deployed it into a container and got it all running on AWS as a Lambda. But setting this up involved just clicking around in AWS and occasionally using the AWS CLI.

Today, I'm going to port that whole setup to Terraform so that its easier to manage, reproduce, and make changes to. ( These are the purported benefits of Terraform, or so my coworker Corey tells me. I've never used it before so I'll be learning as I go. )

**Read this to learn about Terraform from a noob's perspective. The specifics of my infrastructure import may not be relevant to you, but hopefully my thinking process and take-aways will be.**

Ok, follow along with me as import my infrastructure into Terraform.

## What Is TerraForm

Terraform is an open source tool created by HashiCorp to help you create, manage, and deploy Infrastructure as Code (IaC). Terraform can be used to manage your AWS, GCP, or even [Spotify resources](https://learn.hashicorp.com/tutorials/terraform/spotify-playlist) (Don't ask).

Terraform infrastructure configuration is written in HCL, HashiCorp configuration language. It might make sense to know and understand HCL as you get deeper into Terraform, but it's sufficient for this tutorial to just think of it as fancy YAML.

## Installing

First I install terraform:

~~~{.bash caption=">_"}
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
~~~

Then I create a `main.tf` for my terraform config:

~~~{.groovy caption="main.tf"}
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
~~~

Above, I'm pulling in the terraform AWS provider and setting my region. After that I can `init` things:

~~~{.bash caption=">_"}
$ terraform init
~~~

~~~{.ini .merge-code caption=""}
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
~~~

This creates a `.terraform.lock.hcl` file.

~~~{.groovy caption=""}
# This file is maintained automatically by "terraform init".
# Manual edits may be lost in future updates.

provider "registry.terraform.io/hashicorp/aws" {
  version = "4.18.0"
  hashes = [
    ...
  ]
}
~~~

`.terraform.lock.hcl` is a lock file. I check this into git, and the hashes in it will ensure that the provider doesn't change without me knowing it, even if run in some other place at some future date.

## Plan and Apply

I don't have anything besides a provider declared in my terraform file, but never the less, I can still go thru the whole terraform process to make sure everything is ok.

<div class="notice--info notice--big">

### Terraform Workflow

- Write: write your infrastructure as code.
- Plan: Run `terraform plan` to see a preview of the changes.
- Apply: Run `terraform apply` to apply the changes.

</div>

First I run plan:

~~~{.bash caption=">_"}
$ terraform plan
~~~

~~~{.ini .merge-code caption=""}
No changes. Your infrastructure matches the configuration.

Terraform has compared your real infrastructure against your configuration 
and found no differences, so no changes are needed.
~~~

Then I can apply the changes, just to be sure:

~~~{.bash caption=">_"}
$ terraform apply 
~~~

~~~{.ini .merge-code caption=""}
No changes. Your infrastructure matches the configuration.

Terraform has compared your real infrastructure against your configuration 
and found no differences, so no changes are needed.

Apply complete! Resources: 0 added, 0 changed, 0 destroyed.
~~~

<div class="notice--info">

## Side Note: AWS Provider

The AWS provider will need a way to talk to your AWS account. If you don't have AWS credentials properly setup you may get an error like this:

~~~{.bash caption=">_"}
terraform plan
~~~

~~~{.ini .merge-code caption=""}
╷
│ Error: error configuring Terraform AWS Provider: 
no valid credential sources for Terraform AWS Provider found.
~~~

If the credentials you have are wrong, the error will be a little bit different:

~~~{.ini caption=""}
Error: error configuring Terraform AWS Provider: error validating provider 
credentials: error calling sts:GetCallerIdentity: operation error STS: 
GetCallerIdentity, https response error StatusCode: 403, RequestID: 
e816a4d9-6f28-49ef-b245-395c3a758f4a, api error InvalidClientTokenId: 

The security token included in the request is invalid.
~~~

To debug this you need to understand that the aws provider reads from `~/.aws/confg` and `~/.aws/credentials`, the same way the `aws` cli does. If you have credentials for more than one AWS account available, you can use `AWS_PROFILE` to configure the AWS provider. In my case I do this like so:

~~~{.bash caption=">_"}
$ export AWS_PROFILE=earthly-dev
~~~

It's also possible to configure the profile in terraform by adding it under provider configuration:

~~~{.diff caption="main.tf"}
 provider "aws" {
   region = "us-east-1"
+  profile = "earthly-dev"
 }
~~~

</div>

Even though no changes were applied, and I don't yet have any resources being managed by Terraform, I do have a new file.

~~~{.bash caption=">_"}
$ git status
~~~

~~~{.ini .merge-code caption=""}
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        terraform.tfstate

no changes added to commit (use "git add" and/or "git commit -a")
~~~

## How State Works in Terraform

Terraform is declarative. You describe the end result of the state of the infrastructure you would like to see and Terraform makes it happen. But to get from your declarative specification to list of changes to `terraform apply` the current state of the world must be captured.

Terraform stores this state in `terraform.tfstate`. At this point I have no resources being managed by Terraform so my `.tfstate` is pretty small.

~~~{.yaml caption=".tfstate"}
{
  "version": 4,
  "terraform_version": "1.2.3",
  "serial": 1,
  "lineage": "9880ec52-a487-5a8e-db65-c4bc3949ba18",
  "outputs": {},
  "resources": []
}

~~~

Ok, lets move on to creating my first resource. I need to set up ECR first because it's where I store the docker image that is my lambda.

## Elastic Computer Repository - Terraform

To create a ECR Repository in Terraform, I just googled "ECR Terraform" and ended up on the terraform docs where I found the following resource description:

~~~{.groovy caption="main.tf"}
resource "aws_ecr_repository" "foo" {
  name                 = "bar"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}
~~~

<figcaption>Figure ECR: Terraform Doc's sample ECR resource definition</figcaption>

<div class="notice--info notice--big">

## Understanding Terraform Resources

A resource is a declarative bit of HCL describing a piece of infrastructure. In the first line, you can see the keyword `resource` followed by `aws_ecr_repository` and `foo`. This is how you declare a terraform resource. The first string is the resource type, `aws_ecr_repository` in this example and the second thing is the name you want to give it. The name is for your own reference and I'll be using it to refer to specific resources from within other resources coming very soon.

Everything after that is a property of the resource and this whole thing is being written in HCL, HashiCorp configuration language. But as I mentions before, we won't be getting to deep into HCL.

The main thing we need to know is that if we need to later refer to this resource we remove the quotes and add dots (`.`) so that `resource "aws_ecr_repository" "foo"` becomes `resource.aws_ecr_repository.foo` and that resources name would be `resource.aws_ecr_repository.foo.name`.

</div>

## Terraform Import ECR

So to add in my Repository for my image, I copy the Terraform docs and I create the following resource:

~~~{.groovy caption="main.tf"}
### ECR

resource "aws_ecr_repository" "lambda-api" {
  image_tag_mutability = "MUTABLE"
  name                 = "lambda-api"
}
~~~

And running `terraform plan` I get this:

~~~{.ini caption=""}
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
~~~

There is a potential problem here though. I've already setup this repository in AWS. Terraform only tracks the state of resources it is managing, but I created a repository with this same name in the UI. How is this going to work? Let's find out.

~~~{.bash caption=">_"}
$ terraform apply --auto-approve
~~~

~~~{.ini .merge-code caption=""}
Plan: 1 to add, 0 to change, 0 to destroy.
aws_ecr_repository.lambda-api: Creating...
╷
│ Error: failed creating ECR Repository (lambda-api): 
|  RepositoryAlreadyExistsException: The repository with name 'lambda-api'
|   already exists in the registry with id '459018586415'
│   with aws_ecr_repository.lambda-api,
│   on main.tf line 14, in resource "aws_ecr_repository" "lambda-api":
│   14: resource "aws_ecr_repository" "lambda-api" {
│ 
╵
~~~

You can see that Terraform calls the AWS API , which fails to create a new repository, because one already existed. This is going to be an ongoing problem because everything I'd like to get into terraform today I've already set up using the AWS UI.

There are a couple ways to manage this.

- Remove everything via UI and recreate in Terraform.
  
  I reached out to Corey, my local Terraform expert and this is the path he recommended:

  > Use the UI once to figure out how to set things up but then tear it down and recreate it in Terraform.  

- Use a 'reverse terraformer'.

  Tools exist that proport to take an existing cloud accounts and import them into Terraform state and generated the Terraform config for them. I did briefly try this approach.
  
  [terraformer](https://github.com/GoogleCloudPlatform/terraformer) from Google seems a bit out of date and the terraform it generated was for an older version of terraform that I couldn't figure out how to update.

  [terracognita](https://github.com/cycloidio/terracognita) worked better for me. It generated valid Terraform but ultimately I didn't understand the structure of the resources generated, which is part of the reason I'm doing this. So I abandoned this for a different approach.

- Use  `terraform import`.
  
  With import, you can pull in an resource existing resource into terraform's state. Let me show you how I imported my ECR Repo.

## Terraform Import

To import resources into Terraform, I followed these steps. First, I add the resource to my terraform file, like I've already done:

~~~{.groovy caption="main.tf"}
resource "aws_ecr_repository" "lambda-api" {
  image_tag_mutability = "MUTABLE"
  name                 = "lambda-api"
}
~~~

Next, I need to be able to tell Terraform how to import this specific instance. The terraform docs for a resource all have an import section at the bottom that explains how you can import things. You might think for AWS, that an ARN would be the way to import things, but that isn't always the case, so be sure to read the docs. ( I got stuck trying to import by ARN for a bit :) )

For ECR, the docs say "ECR Repositories can be imported using the `name`" and so I run my import like this:

~~~{.bash caption=">_"}
terraform import aws_ecr_repository.lambda-api lambda-api
~~~

~~~{.ini .merge-code caption=""}
aws_ecr_repository.lambda-api: Importing from ID "lambda-api"...
aws_ecr_repository.lambda-api: Import prepared!
  Prepared aws_ecr_repository for import
aws_ecr_repository.lambda-api: Refreshing state... [id=lambda-api]

Import successful!

The resources that were imported are shown above. These resources are now in
your Terraform state and will henceforth be managed by Terraform.
~~~

Then I apply:

~~~{.bash caption=">_"}
terraform apply --auto-approve
~~~

~~~{.ini .merge-code caption=""}
aws_ecr_repository.lambda-api: Refreshing state... [id=lambda-api]

No changes. Your infrastructure matches the configuration.

Terraform has compared your real infrastructure against your configuration and
found no differences, so no changes are needed.

Apply complete! Resources: 0 added, 0 changed, 0 destroyed.
~~~

And I'm all set: My repository is now managed by Terraform.

## Learning From Terraform State with `terraform show`

The Terraform docs are often terse and values in the resource config do not always map one-to-one onto values you'd find the AWS UI. For me, this meant that I couldn't always figure out exactly what I needed to put in the resource configuration to match what I had set up in the UI. Thankfully you can use `terraform show` to retrieve this information.

Let's pretend that I needed my repo to use KMS encryption and to scan image on push. I've already setup these options in AWS but I want to see how to do it AWS.

To import without knowing the config I need, I would create as a blank resource:

~~~{.bash caption="main.tf"}
resource "aws_ecr_repository" "lambda-api" {
}
~~~

And then run import the same way (`terraform import aws_ecr_repository.lambda-api lambda-api`) but after I would use `terraform show` to read its state.

~~~{.bash caption=">_"}
$ terraform show
~~~

~~~{.groovy .merge-code caption=""}
# aws_ecr_repository.lambda-api:
resource "aws_ecr_repository" "lambda-api" {
    arn                  = "arn:aws:ecr:us-east-1:459018586415:repository/
                            lambda-api"
    id                   = "lambda-api"
    image_tag_mutability = "MUTABLE"
    name                 = "lambda-api"
    registry_id          = "459018586415"
    repository_url       = "459018586415.dkr.ecr.us-east-1.amazonaws.com/
                            lambda-api"
    tags                 = {}
    tags_all             = {}

    encryption_configuration {      # <- Here is what I need!
        encryption_type = "KMS"
    }

    image_scanning_configuration {  # <- Here also !
        scan_on_push = true
    }

    timeouts {}
}
~~~

And I can easily see how to set the encryption and image scanning options and therefor copy them into my `main.tf`.

~~~{.groovy caption="main.tf"}
resource "aws_ecr_repository" "lambda-api" {
  image_tag_mutability = "MUTABLE"
  name                 = "lambda-api"
  encryption_configuration {
      encryption_type = "KMS"
  }
  image_scanning_configuration {
        scan_on_push = true
  }
}
~~~

This trick was instrumental in me getting my lambda integration ported over to terraform, but I'll refrain from focusing on it depth. Just remember, if you can't figure out how to configure something in Terraform for some reason, one approach is to set it up in the UI first, and use `terraform import` and `terraform show` to extract a working config.

## AWS ECR Policy Resource Import

Next up is the ECR Policy. First I created it as a blank resource:

~~~{.groovy caption="main.tf"}
resource "aws_ecr_repository_policy" "lambda-api" {
  }
~~~

Imported is:

~~~{.bash caption=">_"}
$ terraform import aws_ecr_repository_policy.lambda-api lambda-api
~~~

And then, with the `terraform show` trick I used above, I extracted the policy I was already using:

~~~{.groovy caption="main.tf"}
resource "aws_ecr_repository_policy" "lambda-api" {
  policy = <<POLICY
{
  "Statement": [
    {
      "Action": [
        "ecr:BatchGetImage",
        "ecr:GetDownloadUrlForLayer",
        "ecr:SetRepositoryPolicy",
        "ecr:DeleteRepositoryPolicy",
        "ecr:GetRepositoryPolicy"
      ],
      "Condition": {
        "StringLike": {
          "aws:sourceArn": "arn:aws:lambda:us-east-1:459018586415:function:*"
        }
      },
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Sid": "LambdaECRImageRetrievalPolicy"
    }
  ],
  "Version": "2008-10-17"
}
POLICY

  repository = aws_ecr_repository.lambda-api.name
}
~~~

Note how `repository` is `aws_ecr_repository.lambda-api.name`. Using `"lambda-api"` here would be perfectly valid, but would leave me with two places to update if I wanted to rename the repository. Also note the use of Heredoc string starting and ending with `POLICY`.

<div class="notice--info notice--big">

### Terraform `heredoc`

Heredoc strings work like this:

~~~{.bash caption=""}
value = <<EOT
hello
world
EOT
~~~

</div>

I can then `terraform apply` and `terraform plan` that to make sure everything works.

## Terraform Import S3

My lambda also uses S3 to cache results and so I need to import my S3 configuration.

First I have my bucket:

~~~{.groovy caption="main.tf"}
resource "aws_s3_bucket" "text-mode" {
  arn           = "arn:aws:s3:::text-mode"
  bucket        = "text-mode"
  force_destroy = "false"
  hosted_zone_id = "Z3AQBSTGFYJSTF"
}
~~~

Which I import:

~~~{.bash caption=">_"}
terraform import aws_s3_bucket.text-mode text-mode
~~~

And then I have to setup my bucket lifecycle.

~~~{.groovy caption="main.tf"}
resource "aws_s3_bucket_lifecycle_configuration" "text-mode" {
  bucket = aws_s3_bucket.text-mode.id
  rule {
    id     = "delete_files_after_14_days"
    status = "Enabled"

    expiration {
      days = 14
    }
  }
}
~~~

And import it.

~~~{.bash caption=">_"}
terraform import aws_s3_bucket_lifecycle_configuration.text-mode text-mode
~~~

Then I run apply, which will find no changes to apply.

You may be wondering how certain I can be in all this declarative config, when none of it has actually been applied from terraform, only imported. Well I'm going to tackle that last.

## Terraform API Gateway Import

Next up is my API Gateway.

First I need to import my domain certificate and set up the API gateway to use it.

~~~{.groovy caption="main.tf"}
## API GATEWAY

# ## Domain Name

resource "aws_acm_certificate" "earthly-tools-com" {
    domain_name               = "earthly-tools.com"
    subject_alternative_names = [
        "earthly-tools.com",
    ]

    options {
        certificate_transparency_logging_preference = "ENABLED"
    }
}

resource "aws_api_gateway_domain_name" "earthly-tools-com" {
  domain_name              = "earthly-tools.com"
  regional_certificate_arn = aws_acm_certificate.earthly-tools-com.arn

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}
~~~

And import it by ARN, which I got from the AWS UI:

~~~{.bash caption=">_"}
$ terraform import aws_acm_certificate.cert arn:...
$ terraform import aws_api_gateway_domain_name.earthly-tools-com earthly-tools.com
~~~

Then I need to set up the API, the API Stage and map it to the domain.

~~~{.groovy caption="main.tf"}
resource "aws_apigatewayv2_api" "earthly-tools-com" {
   api_key_selection_expression = "$request.header.x-api-key"
    description                  = "Created by AWS Lambda"
    disable_execute_api_endpoint = true
    name                         = "text-mode-API"
    protocol_type                = "HTTP"
    route_selection_expression   = "$request.method $request.path"
}

resource "aws_apigatewayv2_stage" "earthly-tools-com" {
  api_id = aws_apigatewayv2_api.earthly-tools-com.id
  name   = "default"
  auto_deploy = true
}

resource "aws_apigatewayv2_api_mapping" "earthly-tools-com" {
  api_id      = aws_apigatewayv2_api.earthly-tools-com.id
  domain_name = aws_api_gateway_domain_name.earthly-tools-com.domain_name
  stage       = aws_apigatewayv2_stage.earthly-tools-com.id
}
~~~

To import these, I need to get the API identified from AWS.

~~~{.bash caption=">_"}
terraform import aws_apigatewayv2_api.earthly-tools-com yr255kt190
terraform import aws_apigatewayv2_route.earthly-tools-com yr255kt190/afjkrcc
terraform import aws_apigatewayv2_api_mapping.earthly-tools-com a09jn5/earthly-tools.com
~~~

Notice how things are becoming a bit more intricate. I got stuck a little bit at the api mapping resource, because it's not a concept presented in the AWS UI. I reached out to Corey, my local terraform expert, and confessed that API Gateway in Terraform seemed overly complicated. He suggested instead of trying to setup each individual resource like this, that its much better to find a module someone has built and use that. Specifically he recommends [this module](https://github.com/terraform-aws-modules/terraform-aws-apigateway-v2) and in the future I may reach for it or one of those off-the-shelf modules rather than figuring this all out myself.

### Terraform Import Lambda

The lambda import was one of the easiest parts, and in particular felt pretty useful, since I do have some specific setting set up in my lambda that I don't want to lose.

I imported using the arn:

~~~{.bash caption=">_"}
terraform import aws_lambda_function.text-mode arn...
~~~

Then I grabbed the details from Terraform by doing `terraform show -no-color > file.tf` and finding my lambda and adding the details back into my terraform file.

~~~{.groovy caption="main.tf"}

resource "aws_lambda_function" "lambda-api" {
  function_name                  = "lambda-api"
  image_uri                      = "459018586415.dkr.ecr.us-east-1.amazonaws.com/lambda-api:latest"
  memory_size                    = "500"
  package_type                   = "Image"
  reserved_concurrent_executions = "-1"
  role                           = "arn:aws:iam::459018586415:role/service-role/lambda-api-role-hb6fczbh"
  timeout                        = "120"
  architectures = ["x86_64"]

  environment {
    variables = {
      HOME = "/tmp"
    }
  }

  ephemeral_storage {
    size = "512"
  }

  tracing_config {
    mode = "PassThrough"
  }
}
~~~

I did a similar process for the lambda permissions, since the API needs permissions to call the lambda. The end result looks like this:

~~~{.groovy caption="main.tf"}
## Give API Gateway access to Lambda
resource "aws_lambda_permission" "earthly-tools-com" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda-api.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:us-east-1:459018586415:
                  ${aws_apigatewayv2_api.earthly-tools-com.id}/*/*/{path+}"
}
~~~

Note that `terraform show` returned the current api arn for `source_arn` and I needed to replace that with a path to make this future proof. This is something to keep vigilant for when using `terraform show` or you might end up with resources hardcoded to values that quickly go out of date.

## Terraform Import API Route and Integration

Integrating the lambda with the API was by far the hardest part for me. In AWS, there is a single button click process to hook a lambda up to an API endpoint. Behind the scenes there are a number of separate things happening. But once I figured out the name of all these little resources, it was easy to import and `terraform show` them to see how they should be configured.

~~~{.groovy caption="main.tf"}
## Attach Lambda to API Gateway
resource "aws_apigatewayv2_integration" "earthly-tools-com" {
   api_id = aws_apigatewayv2_api.earthly-tools-com.id
   connection_type        = "INTERNET"
    integration_method     = "POST"
    integration_type       = "AWS_PROXY"
    integration_uri        = aws_lambda_function.lambda-api.arn
    payload_format_version = "2.0"
    request_parameters     = {}
    request_templates      = {}
    timeout_milliseconds   = 30000
}

resource "aws_apigatewayv2_route" "earthly-tools-com" {
  api_id = aws_apigatewayv2_api.earthly-tools-com.id
  route_key            = "ANY /{path+}"
  target               = "integrations/${aws_apigatewayv2_integration.earthly-tools-com.id}"
  api_key_required     = false
  authorization_scopes = []
  authorization_type   = "NONE"
  request_models       = {}
}
~~~

After importing all those and applying them, I have all the infrastructure behind [text-mode](https://earthly-tools.com) in terraform. Now its time to test things.

## Testing by Destroying

So far Terraform has deployed zero of these changes. It's possible that I'm missing important resources, or my config for them is incorrect. After all, this is my first time using Terraform and many of the resources diverge from the AWS UI: the lambda trigger I used in the UI isn't even a terraform concept.

The easiest way to test all this out is to destroy and then recreate the resources in question. There are a couple of ways to do that. One is using `terraform destroy` which will destroy all the infrastructure. But instead I'm going to comment out resources and run apply to remove them. After that, I'll un-comment them, apply again and see if everything works.

(If your dealing with an important production environment you might not want to do this and instead test things in a separate workspace, but for me this works great.)

First I commented everything out and ran `terraform apply --auto-approve`:

~~~{.bash caption=">_"}
$ terraform apply 
...
aws_ecr_repository_policy.lambda-api: Destroying... [id=lambda-api]
aws_ecr_repository_policy.lambda-api: Destruction complete after 0s
aws_ecr_repository.lambda-api: Destroying... [id=lambda-api]
aws_ecr_repository.lambda-api: Destruction complete after 0s
aws_apigatewayv2_api_mapping.earthly-tools-com: Destroying... [id=zgbzhv]
aws_lambda_permission.earthly-tools-com: Destroying... [id=terraform-20220715135453156200000001]
aws_apigatewayv2_route.earthly-tools-com: Destroying... [id=yha7yhv]
aws_lambda_permission.earthly-tools-com: Destruction complete after 0s
aws_apigatewayv2_route.earthly-tools-com: Destruction complete after 1s
aws_apigatewayv2_integration.earthly-tools-com: Destroying... [id=9js97ns]
aws_apigatewayv2_api_mapping.earthly-tools-com: Destruction complete after 1s
aws_api_gateway_domain_name.earthly-tools-com: Destroying... [id=earthly-tools.com]
aws_apigatewayv2_stage.earthly-tools-com: Destroying... [id=default]
aws_apigatewayv2_integration.earthly-tools-com: Destruction complete after 0s
aws_lambda_function.lambda-api: Destroying... [id=lambda-api]
aws_lambda_function.lambda-api: Destruction complete after 0s
aws_api_gateway_domain_name.earthly-tools-com: Destruction complete after 0s
aws_apigatewayv2_stage.earthly-tools-com: Destruction complete after 0s
aws_apigatewayv2_api.earthly-tools-com: Destroying... [id=yr255kt190]
aws_apigatewayv2_api.earthly-tools-com: Destruction complete after 1s

Apply complete! Resources: 0 added, 0 changed, 12 destroyed.
~~~

At which point, I can confirm nothing worked:

~~~{.bash caption=">_"}
curl https://earthly-tools.com/text-mode
{"message":"Internal Server Error"}%        
~~~

Then I started un-commenting resources working from the top down and applying as I went. Until I got this:

~~~{.bash caption=""}
aws_ecr_repository_policy.lambda-api: Creation complete after 1s [id=lambda-api]
╷
│ Error: error creating Lambda Function (1): InvalidParameterValueException: Source image 459018586415.dkr.ecr.us-east-1.amazonaws.com/lambda-api:latest does not exist. Provide a valid source image.
│ {
│   RespMetadata: {
│     StatusCode: 400,
│     RequestID: "9b458fc2-7897-4d46-88f0-5b52494ec276"
│   },
│   Message_: "Source image 459018586415.dkr.ecr.us-east-1.amazonaws.com/lambda-api:latest does not exist. Provide a valid source image.",
│   Type: "User"
│ }
│ 
│   with aws_lambda_function.lambda-api,
│   on main.tf line 126, in resource "aws_lambda_function" "lambda-api":
│  126: resource "aws_lambda_function" "lambda-api" {
│ 
╵
~~~

It turns out that the lambda needs to have a container in place before being created. So I uncommented the lambda and did a docker push

~~~{.bash caption=">_"}
docker push 459018586415.dkr.ecr.us-east-1.amazonaws.com/lambda-api:latest
The push refers to repository [459018586415.dkr.ecr.us-east-1.amazonaws.com/lambda-api]
559fe089aa1d: Pushed 
b55abedf5128: Pushed 
b1c80662fa4b: Pushed 
77b0856837f7: Pushed 
70997e1fac5a: Pushed 
e44da8829878: Pushed 
247247b540ad: Pushed 
8f1e63e879eb: Pushed 
d692ab088a9b: Pushed 
latest: digest: sha256:b41b0d958721920341cb1cf03fb2778f72ff8c5a7ab2ff8589cb6c5cded14fb0 size: 2205
~~~

Pushing a docker image via Terraform is not easy, nor is building a docker image, so I've simply added a comment to my Terraform telling me what to do next time.

~~~{.bash caption=">_"}
# Container must exist in order to create Lambda function,
# If lamda creation fails, push and rerun
~~~

It's not ideal but it works and with that I could apply the remain resources:

~~~{.bash caption=">_"}
$ terraform apply 
...
aws_apigatewayv2_stage.earthly-tools-com: Creating...
aws_lambda_function.lambda-api: Creating...
aws_apigatewayv2_stage.earthly-tools-com: Creation complete after 1s [id=default]
aws_apigatewayv2_api_mapping.earthly-tools-com: Creating...
aws_apigatewayv2_api_mapping.earthly-tools-com: Creation complete after 0s [id=zgbzhv]
aws_lambda_function.lambda-api: Still creating... [10s elapsed]
aws_lambda_function.lambda-api: Still creating... [20s elapsed]
Apply complete! Resources: 6 added, 0 changed, 0 destroyed.
~~~

But with that change applied, I was back with a running web service.

~~~{.bash caption=">_"}
$ curl https://earthly-tools.com/text-mode
~~~

~~~{.ini .merge-code caption=""}
Earthly.dev Presents:

  _____                 _
 |_   _|   ___  __  __ | |_
   | |    / _ \ \ \/ / | __|
   | |   |  __/  >  <  | |_
   |_|    \___| /_/\_\  \__|

  __  __               _
 |  \/  |   ___     __| |   ___
 | |\/| |  / _ \   / _` |  / _ \
 | |  | | | (_) | | (_| | |  __/
 |_|  |_|  \___/   \__,_|  \___|

~~~

This is why this testing stage is so important. Implicit dependencies meant my Terraform couldn't be rerun and its better to discover this now rather then during an incident.

## Conclusion

And with that I have all my resources imported and I've successful verified I can tear them down and recreate them. Now that I've done this, I have a good understanding of the basics of Terraform, importing resources and how to approach infrastructure as code.

Initially, I found working with Terraform to be a challenge. But I now have the understanding I need to work with more complex infrastructure-as-code, like our Earthly Cloud infrastructure. Terraform seems useful and I'd like to learn more about it.

The Terraform code written here for sure could be improved. I could be extracting my code into separate modules and separating out variables and using workspaces and lifecycles to create a better factored infrastructure as code solution. But doing it from first principles and keeping things simple has been instructive and hopefully reading this conversion build log is valuable for you.

You can find the full all the source on [GitHub](https://github.com/earthly/cloud-services-example/tree/terraform-import).

{% include_html cta/bottom-cta.html %}
