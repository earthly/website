---
title: "Terraform Import - Leaving Click Opps Behind"
categories:
  - Tutorials
toc: true
author: Adam

internal-links:
 - just an example
---
<!-- vale off -->

## From Click Ops to GitOps

Previously I built a REST API, deployed it into a container and got it all running on AWS as a Lambda. But setting this up invovled just clicking around in AWS and occasionally using the AWS CLI.

Today, I'm going to port that whole setup to Terraform so that its easier to manage, reproduce and make changes to. These are the purported benefits of Teraform, or so my coworker Corey tell me. I've never used it before so I'll be learning as I go.

## What is TerraForm

Terraform is an open source tool created by HashiCorp to help you create, manage, and deploy Infrastructure as Code (IaC). Terraform can be used to manage your AWS, GCP, or even [Spotify resources](https://learn.hashicorp.com/tutorials/terraform/spotify-playlist) (Don't ask).

Terraform infrastructure configuration is written in HCL, HashiCorp configuration langauge. It might make sense to know and understand HCL as you get deeper into Terraform, but it's suffienceent for this tutorial to just think of it as fancy YAML.

## Installing

First I install terraform:

~~~{.bash caption=">_"}
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
~~~

Then I create a `main.tf` for my teraform config:

~~~{.bash caption=">_"}
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

Above, I'm pulling in the terraform AWS provider and setting my region. After that I can then `init` things:

~~~{.bash caption=">_"}
terraform init
~~~

~~~{.bash caption=">_"}
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

Terraform then creates `.terraform.lock.hcl` file.

~~~{.bash caption=">_"}
# This file is maintained automatically by "terraform init".
# Manual edits may be lost in future updates.

provider "registry.terraform.io/hashicorp/aws" {
  version = "4.18.0"
  hashes = [
    ...
  ]
}
~~~

`.terraform.lock.hcl` is a lock file. I check this into git, and then the hashes ensure that the provider I've using doens't change without me knowing it, even if run in some other place at some future date.

## Plan And Apply

I don't actually have anything besides a provider declared in my terraform file, but never the less, I can still go thru the whole terraform process to make sure everything is ok.

First I run plan:

~~~{.bash caption=">_"}
$ terraform plan
~~~

~~~{.yaml caption="Output"}
No changes. Your infrastructure matches the configuration.

Terraform has compared your real infrastructure against your configuration and found no differences,
so no changes are needed.
~~~

Then I can apply the changes, just to be sure:

~~~{.bash caption=">_"}
terraform apply 
~~~

~~~{.bash caption=">_"}
No changes. Your infrastructure matches the configuration.

Terraform has compared your real infrastructure against your configuration and found no differences,
so no changes are needed.

Apply complete! Resources: 0 added, 0 changed, 0 destroyed.
~~~

Even though no changes were applied, and I don't yet have any resources being managed by Terraform I do have a new file.

~~~{.bash caption=">_"}
$ git status
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        terraform.tfstate

no changes added to commit (use "git add" and/or "git commit -a")
~~~

## How State Works in Terraform

Terraform is declarative. You describe the end result of the state of the infrastructure you would like to see and Terraform makes it happen. But to get from your declarative specification to list of changes to 'terraform apply` the current state of the world must be captured.

Terraform stores this state in `terraform.tfstate`. At this point I have no resources being mangaged by Terraform so my `.tfstate` is pretty small.

~~~{.bash caption=">_"}
{
  "version": 4,
  "terraform_version": "1.2.3",
  "serial": 1,
  "lineage": "9880ec52-a487-5a8e-db65-c4bc3949ba18",
  "outputs": {},
  "resources": []
}

~~~

Ok, lets move on to creating my first resource. I need to setup ECR. It's where I push my container image to in CI and where the lambda pulls it from.

## Elastic Computer Repository - Terraform

To create a ECR Repository in Terraform, I just googled "ECR Terraform" and ended up on the terraform docs where I found the following resource description:

~~~{.bash caption=">_"}
resource "aws_ecr_repository" "foo" {
  name                 = "bar"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}
~~~

## Understanding Terraform Resources

In the first line, you can see the keyword `resource` followed by `aws_ecr_repository` and `foo`. This is how you declare a terraform resource and a resource is a declaritive thing you want to setup in terraform. The first string is the resource type, `aws_ecr_repository` in this example and the second thing is the name you want to give it. The name is for your own reference and I'll be using it to refer to specific resources from within other resources coming very soon.

Everything after that is a property of the resource and this whole thing is being written in HCL, hashicorp configuration langauge. But as I mentions before, we won't be getting to deep into HCL.

The main thing we need to know is that if we need to later refer to this resource we remove the quotes and add dots (`.`) so that `resource "aws_ecr_repository" "foo"` becomes `resource.aws_ecr_repository.foo` and that resources name would be `resource.aws_ecr_repository.foo.name`.

## Side Note: AWS Provider

The AWS provider will need a way to talk to your AWS account. If you don't have AWS credentials properly setup you may get an error like this:

~~~{.bash caption=">_"}
terraform plan
╷
│ Error: error configuring Terraform AWS Provider: no valid credential sources for Terraform AWS Provider found.
~~~

If the credentials you have are wrong, the error will be a little bit different:

~~~{.bash caption=">_"}
Error: error configuring Terraform AWS Provider: error validating provider credentials: error calling sts:GetCallerIdentity: operation error STS: GetCallerIdentity, https response error StatusCode: 403, RequestID: e816a4d9-6f28-49ef-b245-395c3a758f4a, api error InvalidClientTokenId: The security token included in the request is invalid.
~~~

To debug this you need to understand that the aws provider reads from `~/.aws/confg` and `~/.aws/credentials`, the same way the `aws` cli does. If you have credentials for more than one AWS account available, you can use `AWS_PROFILE` to configure the AWS provider. In my case I do this like so:

~~~{.bash caption=">_"}
$ export AWS_PROFILE=earthly-dev
~~~

It's also possible to configure the profile in terraform by adding it under provider configuration:

~~~{.bash caption=">_"}
 provider "aws" {
   region = "us-east-1"
+  profile = "earthly-dev"
 }
~~~

## ECR & Terraform import

So to add in my Repository for my image I create the following resource

~~~{.bash caption=">_"}
### ECR

resource "aws_ecr_repository" "lambda-api" {
  image_tag_mutability = "MUTABLE"
  name                 = "lambda-api"
}
~~~

And running `terraform plan` I get this:

~~~{.bash caption=">_"}
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
terraform apply --auto-approve
~~~

~~~{.bash caption=">_"}
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
~~~

So Terraforms calls to Amazon via the AWS API failed to create a new repository, because one already existed. This is going to be an ongoing problem because everything I'd like to get into terraform today I've already setup using the AWS UI.

There are a couple ways to manage this.

- Remove everything via UI and recreate in Terraform
  
  I reached out to Corey, my local Terraform expert and this is the path he recommended:

  > Use the UI once to figure out how to set things up but then tear it down and recreate it in Terraform.  

- Use a 'reverse terraformer'
  Tools exist the proport to take an existing cloud accounts and import them into teraform state and generated the teraform config for them. I did briefly try this approach.
  
  [terraformer](https://github.com/GoogleCloudPlatform/terraformer) from google seems a bit out of date and the terraform it generated was for an older version of terraform that I couldn't figure out how to update.

  [terracognita](https://github.com/cycloidio/terracognita) worked better for me. It generated valid terraform but ultimately I didn't understand everything in generated and so I abandoned this for a different approach.

- Use  `terraform import`.
  
  With import, you can pull a resource that already exists into terraform's state. Let me show you how I imported my ECR Repo.

## Terraform Import

To import resources into Terraform I followed these steps

First, I add the resource to my terraform file, like I've already done:

~~~{.bash caption=">_"}
resource "aws_ecr_repository" "lambda-api" {
  image_tag_mutability = "MUTABLE"
  name                 = "lambda-api"
}
~~~

Next, I need to be able to tell Terraform how to import this specific instance. The terraform docs for a resource all have an import section at the bottom that explains how you can import things. You might think for AWS, that an ARN would be the way to import things, but that isn't always the case, so be sure to read the docs.

For ECR, the docs say "ECR Repositories can be imported using the `name`" and so I run my import like this:

~~~{.bash caption=">_"}
terraform import aws_ecr_repository.lambda-api lambda-api
~~~

~~~{.bash caption=">_"}
aws_ecr_repository.lambda-api: Importing from ID "lambda-api"...
aws_ecr_repository.lambda-api: Import prepared!
  Prepared aws_ecr_repository for import
aws_ecr_repository.lambda-api: Refreshing state... [id=lambda-api]

Import successful!

The resources that were imported are shown above. These resources are now in
your Terraform state and will henceforth be managed by Terraform.
~~~

Then apply be able to successfully run.

~~~{.bash caption=">_"}
terraform apply --auto-approve
aws_ecr_repository.lambda-api: Refreshing state... [id=lambda-api]

No changes. Your infrastructure matches the configuration.

Terraform has compared your real infrastructure against your configuration and
found no differences, so no changes are needed.

Apply complete! Resources: 0 added, 0 changed, 0 destroyed.
~~~

## Learning From Terraform State with `terraform show`

The Terraform docs are often terse and values in the resource config do not always map one-to-one onto values you'd find the AWS UI. For me, this meant that I couldn't always figure out exactly what I needed in the resource configuration to match what I had setup in the UI.

Thanksfully you can use `terraform show` to retreive this information. Let's pretend that I needed my repo to use KMS encryption and to scan image on push. I've already setup these options in AWS but I want to see how to do it AWS.

To import this way, I would create as a blank resource:

~~~{.bash caption=">_"}
resource "aws_ecr_repository" "lambda-api" {
}
~~~

And then run import the same way (`terraform import aws_ecr_repository.lambda-api lambda-api`) but after I would use `terraform show` to read its state.

~~~{.bash caption=">_"}
terraform show
~~~

~~~{.bash caption=">_"}
# aws_ecr_repository.lambda-api:
resource "aws_ecr_repository" "lambda-api" {
    arn                  = "arn:aws:ecr:us-east-1:459018586415:repository/lambda-api"
    id                   = "lambda-api"
    image_tag_mutability = "MUTABLE"
    name                 = "lambda-api"
    registry_id          = "459018586415"
    repository_url       = "459018586415.dkr.ecr.us-east-1.amazonaws.com/lambda-api"
    tags                 = {}
    tags_all             = {}

    encryption_configuration {
        encryption_type = "KMS"
    }

    image_scanning_configuration {
        scan_on_push = true
    }

    timeouts {}
}
~~~

And I can easily see how to set the encryption and image scanning options and thereform copy them into my main.tf.

~~~{.bash caption=">_"}
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

This trick was instrumental in me getting my lambda integration ported over to terraform, but I refrain from covering it further. Just remember, if you can't figure out how to configure something in teraform for some reason, just set it up in the UI first, and use import and show to extract a working config.

## AWS ECR Policy Resourse Import

Next up is the ECR Policy. First I created it as a blank resource:

~~~{.bash caption=">_"}
resource "aws_ecr_repository_policy" "lambda-api" {
  }
~~~

Imported is:

~~~{.bash caption=">_"}
$ terraform import aws_ecr_repository_policy.lambda-api lambda-api
~~~

And then with the show trick I extracted the policy I was already using:

~~~{.bash caption=">_"}
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

Note how `repository` is `aws_ecr_repository.lambda-api.name`. Using `lambda-api` here would be perfectly valid, but would leave me two places to update if I wanted to rename the repository.

I can then 'terraform apply` and `terraform plan` that to make sure everything works.

## Terraform Import S3

My lambda also using S3 to cache results and so I need to import my S3 configuration.

First I have my bucket:

~~~{.bash caption=">_"}
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

And then I have to setup and import my bucket lifecycle.

~~~{.bash caption=">_"}
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

~~~{.bash caption=">_"}
terraform import aws_s3_bucket_lifecycle_configuration.text-mode text-mode
~~~

Then I run apply, which will find no changes to apply. You may be wondering how certain yuo can be in all this declarative config, when none of it has actually been applied from terraform. Well I'm going to tackle that last.

## Terraform API Gateway Import

TODO: Add verbage

~~~{.bash caption=">_"}
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

### Terraform Import Lambda

TODO: Add verbage

~~~{.bash caption=">_"}

## Lambda 

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

## Terraform Import API Route and Integration

This part was by far the hardest. In AWS, there is a single button clcik process to hook a lambda up to an API endpoint. Behind the scenes there are a number of seperate things happening. But once I figured out the name of all these little resources, it was easy to import and 'terraform show` them to see how they should be configured.

~~~{.bash caption=">_"}
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

## Give API Gateway access to Lambda
resource "aws_lambda_permission" "earthly-tools-com" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda-api.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:us-east-1:459018586415:yr255kt190/*/*/{path+}"
}
~~~

## Testing this

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
