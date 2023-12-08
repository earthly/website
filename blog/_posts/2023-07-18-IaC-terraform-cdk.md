---
title: "Infrastructure as Code Made Easy: A Beginner's Guide to Terraform CDK"
categories:
  - Tutorials
toc: true
author: Alexandre Couedelo
editor: Mustapha Ahmad Ayodeji

internal-links:
 - Terraform
 - Infrastructure
 - IaC
 - Guide
 - CDK
 - Cloud Development
excerpt: |
    This article introduces the Terraform CDKTF, a programmatic way to create infrastructure as code (IaC). It explains the basics of CDKTF, its core components, and how to deploy an AWS stack using TypeScript. The article also provides best practices for using CDKTF and highlights the benefits of incorporating testing and continuous integration into your infrastructure provisioning process.
last_modified_at: 2023-07-19
---
**This article introduces the basics of CDKTF. Earthly provides reproducible builds for cloud infrastructure and everything else. [Learn more about Earthly](https://cloud.earthly.dev/login).**

If you're reading this article, chances are you're interested in [Terraform](https://www.terraform.io/). Well, let me get right to the point: Terraform is fantastic! Widely adopted across the industry, Terraform lets you provision your cloud infrastructure and, more generally, configure any third-party providers. In fact, you probably wouldn't be able to think of a software-as-a-service (SaaS) offering today that wouldn't create a Terraform provider to simplify the adoption of their product.

The [Cloud Development Kit for Terraform (CDKTF)](https://developer.hashicorp.com/terraform/cdktf) is an alternative to the traditional HashiCorp Configuration Language (HCL). With it, you can create infrastructure as code (IaC) using your favorite programming language, obliviating any HCL limitations and opening up a broad range of options.

This article is a beginner's introduction to CDKTF; however, you should already be familiar with Terraform and HCL. You'll learn about the basics of CDKTF, its core components, and how to deploy a small Amazon Web Services (AWS) stack using TypeScript.

## Why You Need CDKTF

Terraform's success can be attributed to three main factors:

1. It uses the declarative language, HCL, which was created to unify configuration management (it's important to note that some also see this as a constraint).
2. The state engine, which records the resources created and managed by Terraform, lets you plan, visualize, and apply changes to your infrastructure.
3. The availability of client libraries called providers makes it easier to work with.

As mentioned, while HCL is simple and easy to learn and is well suited for simple architecture provisioning, it's not a programming language, so problems can occur when building reusable modules, such as having optional resources in a module, calculating IP ranges to assign to all modules, and manipulating data.

To reduce these issues, HashiCorp introduced [Terraform functions](https://developer.hashicorp.com/terraform/language/functions), but these only cover a small subset of the computations you may need. Other solutions like Terragrunt allow you to template and manipulate HCL.

Imagine if you could utilize your preferred programming language to address these challenges. Fortunately, CDKTF provides precisely this opportunity.

> **Please note:** CDKTF isn't better than HCL, but it's an option for when you need a procedural programming language to create an abstraction to manage your infrastructure better.

## Getting Started With CDKTF

CDKTF supports five programming languages: TypeScript, Python, Java, C#, and Go. When choosing which language to use, you should pick the one you and your team are the most confident with.

CDKTF itself is written in TypeScript and relies on tools like [jsii](https://aws.github.io/jsii/) and [projen](https://github.com/projen/projen#getting-started) to generate the APIs for other programming languages. This makes TypeScript the de facto language for those without a strong preference. Python is also another popular option and works well for this purpose.

The following illustration demonstrates the CDKTF process:

<div class="wide">
![CDKTF process courtesy of Alexandre Couëdelo]({{site.images}}{{page.slug}}/ltT056e.png)
</div>

The code you write with CDKTF [synthesizes](https://developer.hashicorp.com/terraform/cdktf/cli-reference/commands#synth) a JSON-compatible configuration that Terraform uses to [plan infrastructure configuration](https://developer.hashicorp.com/terraform/cli/commands/plan). In sum, the CDKTF process happens before the regular Terraform plan process.

### Prerequisites

Before you get started creating infrastructure with CDKTF, you need to set up your local environment. To do so, you need the following:

- [Terraform version 1.2](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) or above. It's recommended that you install Terraform with the [`tfenv`](https://github.com/tfutils/tfenv) CLI, as it makes it easy to manage versions of Terraform.
- [CDKTF CLI](https://developer.hashicorp.com/terraform/cdktf/cli-reference/cli-configuration).
- [Node.js (LTS - v18.12.0)](https://nodejs.org/en). It's recommended that you install Node.js via `nvm` as it makes managing node versions easy.
- [Terraform Cloud account](https://app.terraform.io/session). You will use this as your remote state solution.
- [New AWS Free Tier account](https://aws.amazon.com/account/). This includes a fresh Identity and Access Management (IAM) user and its AWS credential.

For Linux and macOS users relying on [Homebrew](https://brew.sh/), you can use the following command to get everything you need:

~~~{.bash caption=">_"}
brew install nvm tfenv cdktf
~~~

To get the last version of Node.js, use `nvm`:

~~~{.bash caption=">_"}
nvm use lts
~~~

And to get the latest version of Terraform, use `tfenv`:

~~~{.bash caption=">_"}
tfenv install latest && tfenv use latest
~~~

Finally, check your version of `terraform`, `node`, and `cdktf`. As a reference, the following is what was used for this tutorial:

Terraform version:

~~~{.bash caption=">_"}
terraform -version
~~~

Terraform version output:

~~~{ caption="Output"}
Terraform v1.4.6
on linux_amd64
~~~

Node version:

~~~{.bash caption=">_"}
node -v
~~~

Node version output:

~~~{ caption="Output"}
v18.15.0
~~~

CDKTF version:

~~~{.bash caption=">_"}
cdktf --version
~~~

CDKTF version output:

~~~{ caption="Output"}
0.16.1
~~~

You can find all the code for this tutorial in [this GitHub repo](https://github.com/xNok/terraform-cdk-demo).

### Creating a New CDK Project

The `cdktf` CLI lets you easily bootstrap a project. To do so, create a new folder and change the current directory to that folder:

~~~{.bash caption=">_"}
mkdir typescript-aws-stack
cd typescript-aws-stack
~~~

Then execute the `cdktf init` command:

~~~{.bash caption=">_"}
cdktf init --template="typescript" --providers="aws@~>4.65"
~~~

The `--template` flag indicates the template to use; it can be the name of a [built-in template](https://github.com/hashicorp/terraform-cdk/tree/main/packages/cdktf-cli/templates) or the URL to any [remote template](https://developer.hashicorp.com/terraform/cdktf/create-and-deploy/remote-templates). The `--providers` flag is the comma-separated list of providers to install while initializing the template.

Then, you're prompted with a series of questions. The initial one is this: "Do you want to use Terraform Cloud for remote state management?" You should always use a [remote state option](https://developer.hashicorp.com/terraform/language/state/remote), and Terraform Cloud is the most convenient option in this scenario since it's free and built into the Terraform solution.

If you want to use another remote backend solution, answer no and refer to the [remote backend documentation](https://developer.hashicorp.com/terraform/cdktf/concepts/remote-backends). However, this tutorial assumes you chose Terraform Cloud.

~~~{.bash caption=">_"}
└ cdktf init --template="typescript" --providers="aws@~>4.65"
~~~

Output:

~~~{ caption="Output"}
Welcome to CDK for Terraform!

By default, `cdktf` lets you manage the state of your stacks using 
Terraform Cloud for free.
`cdktf` will request an API token for app.terraform.io using your browser.

If login is successful, `cdktf` will store the token in plain text in
the following file for use by subsequent Terraform commands: 
`/home/gitpod/.terraform.d/credentials.tfrc.json`.

Note: The local storage mode isn't recommended for storing the 
state of your stacks.

? Do you want to continue with Terraform Cloud remote state 
management? Yes
~~~

The `cdktf` generates the following template:

~~~{.bash caption=">_"}
└ tree -L 1
~~~

Output:

~~~{ caption="Output"}
.
├── cdktf.json
├── help
├── jest.config.js
├── main.ts
├── node_modules
├── package.json
├── package-lock.json
├── setup.js
├── __tests__
└── tsconfig.json
~~~

Here, the only thing you need to pay attention to is the `main.ts` file. This file is the entry point for `cdktf` and is executed whenever you invoke a `cdktf` command. The minimal viable code creates a `cdktf` and calls the `synth` method:

~~~{.ts caption="main.ts"}
import { App } from "cdktf";

const app = new App();
app.synth();
~~~

The [synthesize](https://developer.hashicorp.com/terraform/cdktf/cli-reference/commands#synth) process (*, i.e.,* `synth`) is the core of CDKTF; it combines all [the stacks](https://developer.hashicorp.com/terraform/cdktf/concepts/stacks) and converts them into [JSON configuration files](https://developer.hashicorp.com/terraform/language/syntax/json) that Terraform can use to plan and apply infrastructure configurations. This means a CDKTF program defines a set of `TerraformStack`s and registers them in the `App`. Following is exactly what the generated code does:

~~~{.ts caption="main.ts"}
// Your stack definition
class MyStack extends TerraformStack {
  constructor(scope: Construct, id: string) {
    super(scope, id);
    // define resources here
  }
}

// Create a CDKTF App
const app = new App();

// Register the Stack to your App
const stack = new MyStack(app, "typescript-aws-stack");

// Define the Remote State Configuration
new CloudBackend(stack, {
  hostname: "app.terraform.io",
  organization: "<YOUR ORG ID>",
  workspaces: new NamedCloudWorkspace("typescript-aws-stack")
});
// Execute the synth process
app.synth();
~~~

The generated template defines `MyStack` and contains a collection of resources. It also defines the `App` mentioned previously, and configures the Terraform Cloud remote state via `CloudBackend`. (If you want to use another remote state provider, refer to [this documentation](https://developer.hashicorp.com/terraform/cdktf/concepts/remote-backends). Because no resources are defined in `MyStack`, the boilerplate doesn't do anything.

### Configuring the Providers

Similar to Terraform, before using a provider, you need to configure it. When you invoked `cdktf init`, you specified `--providers="aws@~>4.65"`, which added the AWS provider to your project. Providers are added to your `package.json` and installed when invoking `npm install`.

Ultimately, this means you can import classes from the [`@cdktf/provider-aws`](https://github.com/cdktf/cdktf-provider-aws/blob/HEAD/docs/API.typescript.md) library.

Import `AwsProvider` and invoke its constructor in the `MyStack` constructor method:

~~~{.ts caption="main.ts"}
import { AwsProvider } from "@cdktf/provider-aws/lib/provider";

// You stack definition
class MyStack extends TerraformStack {
  constructor(scope: Construct, id: string) {
    super(scope, id);
    // Define AWS Provider
    new AwsProvider(this, "AWS", {
      region: "us-west-1",
    });
  }
}
~~~

> **Please note:** `AwsProvider` requires authentication to your AWS account. The implied way is to use credentials by setting them in your terminal:

~~~{.bash caption=">_"}
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
~~~

Please refer to the official documentation for more information about the [different approaches to authenticating to AWS](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#authentication-and-configuration).

To illustrate how to install a provider outside the `init` process, install a GitHub provider via npm. Later in the tutorial, you'll use this provider to add environment variables to [GitHub Actions](https://github.com/features/actions) via Terraform. This is a common practice to bridge the gap between infrastructure provisioning and CI/CD:

~~~{.bash caption=">_"}
npm install --save @cdktf/provider-github
~~~

Now that the provider is installed, you can instantiate the provider in `MyStack`:

~~~{.ts caption="main.ts"}
import { AwsProvider } from "@cdktf/provider-aws/lib/provider";
import { GithubProvider } from "@cdktf/provider-github/lib/provider";

// You stack definition
class MyStack extends TerraformStack {
  constructor(scope: Construct, id: string) {
    super(scope, id);
    // Define AWS Provider
    new AwsProvider(this, "AWS", {
      region: "us-west-1",
    });

    new GithubProvider(this, "GitHub", {})
  }
}
~~~

The GitHub provider requires a personal access token to perform actions on your behalf. Follow [this official GitHub tutorial](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) to create an access token and define the corresponding environment variable in your terminal:

~~~{.bash caption=">_"}
GITHUB_TOKEN=
~~~

## CDKTF in Action

Now that your project is configured, you can add resources to `MyStack`.

### Creating Resources Using CDK

Resources are a TypeScript `class` exported by a provider. In this case, you need `Instance` from `provider-aws` to create an [Amazon Elastic Compute Cloud (Amazon EC2)](https://aws.amazon.com/ec2/) instance as well as `ActionsVariable` and `DataGithubRepository` from `provider-github` to configure the action variables for your repository:

~~~{.ts caption="main.ts"}
// [...] previous import
import { Instance } from "@cdktf/provider-aws/lib/instance";
import { ActionsVariable } from "@cdktf/provider-github/lib/actions-variable"
import { DataGithubRepository } from "@cdktf/provider-github/lib/data-github-repository"

// You stack definition
~~~

In the `MyStack` constructor, you need to instantiate and configure those resources. For instance, to create a new EC2 instance, you need to instantiate `Instance`. The first parameter is always the stack itself (i.e., `this`), which is a unique identifier for the resources (the name must be unique across all resources), and the second is a map of configuration for the resource:

~~~{.ts caption="main.ts"}
const ec2Instance = new Instance(
            this,      // stack reference
      "compute,"// unique ID
            {          // Configuration Map
          ami: "ami-01456a894f71116f2",
          instanceType: "t2.micro",
        }
    );
~~~

Now you need to repeat the operation and define each of the resources. Let's add an  `ActionsVariable` and a `DataGithubRepository` to the Stack:

~~~{.ts caption="main.ts"}
class MyStack extends TerraformStack {
  constructor(scope: Construct, id: string) {
    super(scope, id);

    new AwsProvider(this, "AWS", {
      region: "us-west-1",
    });

    new GithubProvider(this, "GitHub", {})

    // AWS
    const ec2Instance = new Instance(this, "compute", {
      ami: "ami-01456a894f71116f2",
      instanceType: "t2.micro",
    });

    // GITHUB
    const repo = new DataGithubRepository(this, "repo", {
      fullName:  "xNok/terraform-cdk-demo",
    })

    new ActionsVariable(this, "public_ip", {
      repository: repo.name,
      value: ec2Instance.publicIp, // ActionsVariable depends on ec2Instance
      variableName:"PUBLIC_IP"
    })

    // OUTPUT
    new TerraformOutput(this, "public_ip", {
      value: ec2Instance.publicIp,
    });
  }
}
~~~

When you access the attribute `ec2Instance.publicIp` to define the attribute `value` of an `ActionsVariable`, it implicitly creates dependencies between `ActionsVariable` resources and the `Instance` referenced by the variable `ec2Instance`. This means that Terraform will create the `ActionsVariable` name `public_ip` after the `Instance` called `compute`, which is exactly what you want.

In this snippet, you also utilize [`TerraformOutput`](https://developer.hashicorp.com/terraform/language/values/outputs) to expose the `public_ip` information. You'll see the `public_ip` value displayed in your terminal when applying, and it can be used to [share data between stacks](https://developer.hashicorp.com/terraform/cdktf/concepts/variables-and-outputs#output-values).

At this point, you're done coding, and your stack is ready to be deployed. Simply call the following:

~~~{.bash caption=">_"}
cdktf deploy
~~~

This triggers the `synth` process of turning your code into Terraform JSON representation, then immediately calls `terraform apply`. You should already be familiar with the output from `cdktf deploy`; this is the `terraform plan` output asking you if you want to apply those changes:

~~~{ caption="Output"}
[...]
Plan: 2 to add, 0 to change, 0 to destroy.
                      
                      Changes to Outputs:
                        + public_ip = (known after apply)
typescript-aws-stack  
                      Do you want to perform these actions in workspace 
                      "typescript-aws-stack"?
                        Terraform will perform the actions described above.
                        Only 'yes' will be accepted to approve.

Please review the diff output above for typescript-aws-stack
❯ Approve  Applies the changes outlined in the plan.
  Dismiss
  Stop
~~~

Press **Enter** to approve the changes, then wait a few minutes for the provisioning to finish. If you go to the AWS Management Console, you should see your EC2 instance up and running:

<div class="wide">
![AWS Management Console]({{site.images}}{{page.slug}}/j7Z8EMd.png)
</div>

In GitHub, you should also find the IP address for this instance in **Security > Secrets and variables > Actions > Variables > Repository variables**. Everything is ready for your CI/CD to call that instance:

<div class="wide">
![GitHub Actions Settings]({{site.images}}{{page.slug}}/l8CiW8I.png)
</div>

### Modifying and Deleting Resources

After the initial creation, you can modify resources by editing the code and calling `cdktf deploy` again. For this example, you need to add tags to that AWS instance. In AWS, tags help you identify and organize your resources. For instance, adding a tag stating which Git repository is associated with that instance is beneficial to figure out how resources are provisioned. To do so, simply edit the code to look like this:

~~~{.ts caption="main.ts"}
// AWS
    const ec2Instance = new Instance(this, "compute", {
      ami: "ami-01456a894f71116f2",
      instanceType: "t2.micro",
      tags: {
        "repo": "xNok/terraform-cdk-demo",
      }
    });
~~~

Then trigger a new deployment plan:

~~~{.bash caption=">_"}
cdktf deploy
~~~

You should see the changes outputted in your console:

~~~{ caption="Output"}
typescript-aws-stack  Terraform used the selected providers to generate 
the following execution plan.
  Resource actions are indicated with the following symbols:
  ~ update in-place

Terraform will perform the following actions:
typescript-aws-stack    # aws_instance.compute (compute) will be updated 
in-place
  ~ resource "aws_instance" "compute" {
        id                                   = "i-0691ac8513c7242fa"
      ~ tags                                 = {
          + "repo" = "xNok/terraform-cdk-demo"
        }
      ~ tags_all                             = {
          + "repo" = "xNok/terraform-cdk-demo"
        }
        # (30 unchanged attributes hidden)

        # (7 unchanged blocks hidden)
    }

Plan: 0 to add, 1 to change, 0 to destroy.
typescript-aws-stack  
                      Do you want to perform these actions in workspace 
                      "typescript-aws-stack"?
                        Terraform will perform the actions described above.
                        Only 'yes' will be accepted to approve.

Please review the diff output above for typescript-aws-stack
❯ Approve  Applies the changes outlined in the plan.
  Dismiss
  Stop
~~~

Approve the changes and wait for the task to complete:

~~~{ caption="Output"}
typescript-aws-stack  aws_instance.compute (compute): 
Modifying... [id=i-0691ac8513c7242fa]
typescript-aws-stack  aws_instance.compute (compute): 
Modifications complete after 1s [id=i-0691ac8513c7242fa]

                      Apply complete! Resources: 0 added, 1 changed, 
                      0 destroyed.

                      Outputs:
                      public_ip = "50.18.32.211"

  typescript-aws-stack
  public_ip = 50.18.32.211
~~~

Once the provisioning is completed, go to the AWS Management Console and look at the instance tags. You should see that your `repo` tag has been added to that instance:

<div class="wide">
![EC2 instance tags]({{site.images}}{{page.slug}}/jGUj8ai.png)
</div>

Finally, do some cleanup and delete the instance you created. To do so, call the following:

~~~{.bash caption=">_"}
cdktf destoy
~~~

Once again, you see the plan, and Terraform prompts you to approve it. Approve the changes and wait for the operation to complete:

~~~{ caption="Output"}
Plan: 0 to add, 0 to change, 2 to destroy.
                      
                      Changes to Outputs:
                        - public_ip = "50.18.32.211" -> null
typescript-aws-stack  
                      Do you really want to destroy all resources in 
                      workspace "typescript-aws-stack"?
                        Terraform will destroy all your managed 
                        infrastructure, as shown above.
                        There is no undo. Only 'yes' will be accepted 
                        to confirm.
~~~

Now you're back to square one. Everything should be removed, the instance terminated, and the repository variable removed.

## Using Variables and Conditions in CDKTF

Variables are useful to create configurable and reusable `Stack`. Configurable because by replacing `hard-coded` values with variables, you can change the behavior of your Stack without changing code, and reusable since you can deploy the "same Stack" with a different set of variables.

You can use a Terraform variable or your programming language to read a variable from anywhere. There are two ways to define variables in CDKTF: In the first case, you're limited to what you used to do with Terraform (i.e., `variable` and `tfvars` files). However, you can implement any abstraction you like using your programming language. You can define your own YAML to configure stacks and make HTTP calls to an API to collect the necessary information.

The second approach opens up even more possibilities that are out of the scope of this article. As a rule of thumb, use a Terraform variable to make the execution of `cdktf` configurable. However, to fully leverage CDKTF, build your own abstraction and implement a mechanism to read variables, allowing you to take full advantage of its capabilities.

### Variable: The Terraform Way

To use variables in accordance with the Terraform way, you utilize the [`TerraformVariable` class](https://developer.hashicorp.com/terraform/language/values/variables). In this case, you can add variable definitions to your stack:

~~~{.ts caption="main.ts"}
   const imageId = new TerraformVariable(this, "imageId", {
      type: "string",
      default: "ami-01456a894f71116f2",
      description: "What AMI to use to create an instance",
    });

    const imageSize = new TerraformVariable(this, "imageSize", {
      type: "string",
      default: "t2.micro",
      description: "What size to use to create an instance",
    });

    const repoId = new TerraformVariable(this, "repoId", {
      type: "string",
      default: "xNok/terraform-cdk-demo",
      description: "Which repository manage this instance",
    });
~~~

These variables usually work with the following [Terraform input variables](https://developer.hashicorp.com/terraform/language/values/variables):

- Define a `*.tfvars` file and use the `--var-file` argument when calling `cdktf`
- Use the `-var` argument when calling `cdktf`: `var="imageId=ami-abc123"`
- Use environment variables `TF_VAR_<your variable>` before calling `cdktf`

Always use a Terraform variable when dealing with secret/sensitive variables. This ensures that secrets are not embedded in the Terraform JSON representation after the `synth` process.

### Variable: The Programming Way

The following is only one example of how you could structure your code to fetch variables from an external source. Ideally, you want to define a new interface, `MyStackConfig` that defines the type structure for your configuration:

~~~{.ts caption="fetchConfig.ts"}
interface MyStackConfig {
  imageID: string;
  imageSize: string;
  repo?: string;
}
~~~

Then `MyStack` constructor should accept an attribute `config` of type `MyStackConfig`:

~~~{.ts caption="fetchConfig.ts"}
class MyStack extends TerraformStack {
  constructor(scope: Construct, id: string, config: MyStackConfig) {
     super(scope, id);
     // your resources and provider
  }
}
~~~

Lastly, before registering `MyStack` to the `App`, you need a function that provides the config (*e.g.,* an object of type `MyStackConfig`). Here, the function is called `fetchConfig`:

~~~{.ts caption="fetchConfig.ts"}
// fetching the config
const fetchedMyStackConfig = fetchConfig("typescript-aws-stack")

// Instantiating the App
const app = new App();

// Register the Stack to your App
const stack = new MyStack(app, "typescript-aws-stack", fetchedMyStackConfig);

// Configure The Remote State
new CloudBackend(stack, {
  hostname: "app.terraform.io",
  organization: "<YOUR ORG ID>",
  workspaces: new NamedCloudWorkspace("typescript-aws-stack")
});
// Execute the synth process
app.synth();
~~~

Now the question is: How can you retrieve configs to create your stack? or, in other words, what should `fetchConfig` do? Let's take a look at a few different options:

One option is to define a configuration format in YAML or JSON that developers use to provision the resources they need. Following is a minimal example to retrieve configs from YAML configurations:

~~~{.ts caption="fetchConfig.ts"}
import {load} from 'js-yaml';
import {readFileSync} from 'fs';

// Define a structure for the configurations
interface MyStackConfig {
  imageID: string;
  imageSize: string;
  repo?: string;
}

export function fetchConfig(stack: string): MyStackConfig {
    // read the YAML file and cast it as Config
    const yaml = load(readFileSync(stack + '.yaml', "utf8")) as Config;
    return yaml;
}
~~~

Another option is to create an API that acts as a service catalog that returns the required resources for an application and desired configuration. Here's an example where you retrieve configuration from an API:

~~~{.ts caption="fetchConfig.ts"}
import fetch from 'node-fetch';

interface MyStackConfig {
  imageID: string;
  imageSize: string;
  repo?: string;
}

export async function fetchConfigApi(stack: string): Promise<MyStackConfig > {
    // Call the API and cast it as Config
    const response = await fetch('https://api.example.com/' + stack);
    const config = await response.json() as Config;
    return config
}

~~~

This is exactly where CDKTF shines. Now, you have a programming language at your disposal, and it's up to you to create an abstraction on top of Terraform.

## Best Practices for CDKTF

When working with CDKTF, there are several best practices you should follow to ensure efficient and effective management of your infrastructure. Here are some key recommendations to keep in mind:

### Create a Clear and Logical Structure

CDKTF offers new opportunities for creating dynamically reusable IaC. However, structuring code is not the same as organizing HCL configuration. Moving to the coding realm emphasizes the importance of organization and structure in the success of any project. It's best to follow the [CDKTF organization of resources](https://developer.hashicorp.com/terraform/cdktf/concepts/cdktf-architecture) to create a clear and logical structure for the codebase.

Applications are the top-level concept defined in `main.ts` and are the entry point of your Terraform CDK script. Apps are made of stacks that can be reused multiple times (*e.g.,* to create a production and development stack), and stacks are made of resources and constructs. [Constructs](https://developer.hashicorp.com/terraform/cdktf/concepts/constructs) are analogous to Terraform modules in the sense that they let you build reusable and configurable sets of resources.

For this reason, you should aim to build a library of composable stacks or constructs. This means that your app imports those resources to define the infrastructure configuration:

<div class="wide">
![CDKTF app organization]({{site.images}}{{page.slug}}/dRa2Hkq.png)
</div>

### Incorporate Testing and Continuous Integration

Testing and continuous integration are crucial to ensure that your software functions as intended. However, many developers don't test Terraform configurations due to the lack of a simple and comprehensive testing framework.

That's not the case anymore. With CDKTF, you can use your language's testing framework. Additionally, CDKTF provides an [assertion library](https://developer.hashicorp.com/terraform/cdktf/test/unit-testscloud%20testing) to test for the synth process.

## Conclusion

CDKTF offers a cool way to build Infrastructure as Code (IaC) using your favorite programming languages. It generates a JSON configuration that Terraform can use instead of the usual HCL. This article showed you basics of using CDKTF. While it may seem unnecessary for simple tasks, its true power shines in complex Terraform modules.

To dig deeper into CDKTF, check out these HashiCorp articles about [integrating existing Terraform modules with CDKTF](https://developer.hashicorp.com/terraform/cdktf/concepts/modules) and [constructs building blocks](https://developer.hashicorp.com/terraform/cdktf/concepts/constructs).

And if you're looking to streamline your build automation process further, you might want to give [Earthly]((https://cloud.earthly.dev/login)) a try! It's a powerful tool that can complement your use of CDKTF by providing a consistent and efficient build environment.

{% include_html cta/bottom-cta.html %}
