---
title: "Best Practices for Reusable Workflows in GitHub Actions"
categories:
  - Tutorials
toc: true
author: Kumar Harsh

internal-links:
 - practices for reusable workflows
 - reusable workflows in gitHub actions
 - how to reuse workflows in github actions
 - workflows in github actions
excerpt: |
    GitHub Actions reusable workflows are predefined templates that allow developers to quickly scaffold processes and accelerate software delivery. Best practices for using reusable workflows include parameterizing workflows, documenting them, using composite actions, considering a dedicated workflows repository, versioning workflows, testing them, following naming conventions, considering platform compatibility, and continuously improving and refining workflows based on user feedback.
---
<!--sgpt-->**We're [Earthly](https://earthly.dev/). Want to simplify and speed-up your software builds with containerization? Especially if you're into GitHub Actions, Earthly is the sidekick you didn't know you needed for your CI workflows. [Check us out](/).**

GitHub Actions [reusable workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows) are particularly helpful in modern software projects. Reusable workflows act as blueprints for CI/CD pipelines, allowing developers to quickly scaffold processes and accelerate their software delivery significantly.

In this guide, you'll learn more about reusable workflows, what they offer, the challenges associated with them, and some best practices you should keep in mind to make the best use of reusable workflows.

## What Are Reusable Workflows?

Reusable workflows are predefined templates in GitHub Actions used for orchestrating various tasks and processes within your software development lifecycle. Instead of creating each new workflow from scratch every time, you can create reusable workflows as templates. These templates encapsulate actions, steps, and configurations that can be easily shared and reused across different repositories or projects. They're like LEGO building blocks for your development process.

The key to reusable workflows is to fine-tune them to provide as many steps out of the box as possible while being generic enough to be reused across multiple projects. Once you've perfected that, you can effortlessly call them across multiple projects, ensuring consistency in your pipelines and saving a ton of time.

Creating reusable workflows is simple. You just need to choose the `workflow_call` trigger in the workflow you wish to reuse. Here's what the trigger would look like in the workflow file:

~~~{.yaml caption=""}
on:
  workflow_call
~~~

Next, in the caller workflow (where you wish to call this reusable workflow), you need to use the `uses` keyword when defining a job in the workflow:

~~~{.yaml caption=""}
jobs:
  my_job_1:
    runs-on: ubuntu-latest
    steps:
    - uses: <your-profile-or-org-username>/<repo-name>/
    <reusable-workflow-name
~~~

Reusable workflows not only boost efficiency but also promote best practices by enabling teams to create and use standardized templates effortlessly. Some of the most common ways reusable workflows are used include the following:

* CI pipelines
* Code scanning and analysis
* Release management
* Documentation generation
* Dependency management
* Issue and pull request workflow

However, there are a few nuances you need to keep in mind when working with reusable workflows:

* **Extensibility can be limited in some cases.** It can be challenging to maintain a balance between making a reusable workflow flexible and keeping it manageable. Extending or modifying reusable workflows may require significant effort and careful consideration.
* **Version management is tiring but important.** While versioning your reusable workflows is a best practice, managing multiple versions and ensuring compatibility across repositories can become cumbersome.
* **Dependency management can be cumbersome.** Reusable workflows may have dependencies on specific versions of tools, libraries, or actions. Ensuring compatibility with different versions of these dependencies across applications in multiple repositories can be challenging.
* **Environment variables set in the context of the caller workflow do not get passed to the reusable workflow.** Instead, you need to pass them as input arguments to the reusable workflow. Similarly, environment variables set from inside reusable workflows are not propagated to the calling workflow. You need to use output arguments in such cases.
* **You can only nest up to four levels.** You can nest reusable workflows (*ie* call a reusable workflow inside another reusable workflow). However, you can only nest up to four levels.
* **Workflows count restriction.** You can only call a maximum of twenty reusable workflows from a workflow file. This includes nested workflows as well, so make sure to isolate reusable workflows wherever possible.

## Best Practices for Reusable Workflows in GitHub Actions

Now that you understand what reusable workflows are and how they work, here are a few best practices you can make use of to get the most out of reusable workflows.

### Parameterize Your Workflows

Since your reusable workflows are going to be used across repositories, it only makes sense to parameterize them (*ie* use input parameters with them to allow the calling workflow to pass in custom data when calling them). You should also define output parameters if the reusable workflow needs to pass data back to the calling environment.

As discussed previously, the environment of the calling workflow and the called workflow (*ie* the reusable workflow) are not shared. This means using input and output arguments is your only way of communicating with the reusable workflows.

Following is an example workflow that defines two input arguments and one output argument:

~~~{.yaml caption=""}
name: Add Numbers Workflow

on:
  workflow_call:
    inputs:
      number1:
        description: 'First number'
        required: true
        type: number
        default: 0
      number2:
        description: 'Second number'
        required: true
        type: number
        default: 0
    outputs:
      sum:
        description: 'Sum of the two numbers'
        value: ${{ jobs.add-numbers.outputs.sum }}
        

jobs:
  add-numbers:
    name: Add two numbers
    runs-on: ubuntu-latest

    outputs:
      sum: ${{ steps.calculate.outputs.sum }}
    
    steps:
      - id: set-up-env
        name: Set up environment
        run: |
          echo "NUMBER1=${{ inputs.number1 }}" >> $GITHUB_ENV
          echo "NUMBER2=${{ inputs.number2 }}" >> $GITHUB_ENV
          
      - name: Calculate sum
        id: calculate
        run: |
          sum=$((NUMBER1 + NUMBER2))
          echo "%{sum}"
          echo "SUM=${sum}" >> $GITHUB_OUTPUT
~~~

Notice how this code sets a default value for the input arguments. This is a good practice as it allows your reusable workflow to start up without error, even in the case of missing input arguments. Additionally, the input and the output arguments carry a short description using the `description` node. This helps your team members understand what these arguments are meant to do.

### Document Your Workflows

When working with more than one reusable workflow across repositories, it can become cumbersome to remember what each workflow does and how it works. To avoid the mental exercise of inferring what a workflow does from its YAML code, you should consider documenting your workflows.

This documentation should be clear and include instructions on how to use them, what inputs they require, and what outputs or artifacts they produce. Also, consider adding comments within the workflow file to explain the purpose and functionality of each step. This goes a long way in helping the other people who use your workflow to understand how it works.

### Use Composite Actions

Similar to reusable workflows, GitHub Actions also offers a feature to help you reuse a bunch of workflow steps known as [composite actions](https://docs.github.com/en/actions/creating-actions/about-custom-actions#composite-actions). This feature allows you to create your custom actions by packaging multiple workflow steps into one callable action.

This is quite similar to how reusable workflows work. However, the key difference is how they are called. While reusable workflows take up an entire job in your calling workflow, composite actions can be run as a single step in a job in your calling workflow, allowing you to compose the job as you'd like.

You can leverage composite actions when designing workflows (both regular and reusable) that contain overlapping steps to isolate them and make the code more easily manageable.

### Consider a Dedicated Workflows Repository

While setting up reusable workflows in your target repository and reusing them in other workflows are standard ways supported by GitHub Actions, it also supports reusing workflows from other repositories in the same user account or organization. You can make use of this feature to better organize your reusable workflows.

If you're planning to set up multiple reusable workflows in your organization, it might be a good idea to set up a common workflow repository. This allows you to better track the development of reusable workflows, reuse them in a standard fashion across your organization, and version them for easier access.

### Version Your Reusable Workflows

As you make updates or improvements to your reusable workflows, consider using versioning to track changes. This allows users to choose a specific version of the workflow when incorporating it into their repository, ensuring compatibility and stability.

If you're using a dedicated workflow repository, this becomes easier. Create releases for each stable version of your workflow. Other team members can reference the versions by the release tags when calling them in their workflows. This also works with commit SHAs, but releases provide you with a cleaner version tag so it's easier to read and understand.

### Test Your Reusable Workflows

Just like any other form of software, reusable workflows can have bugs and other errors. It's good practice to test your workflows whenever possible. The upside to reusable workflows is that they work quite similarly to functions in programming as they take in a set of input values and return a set of output values. You can create test workflows to test your reusable workflows by passing in a set of input arguments and expecting a set of output values, similar to unit tests.

You can also make use of [matrix strategies](https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs) supported by GitHub Actions to easily trigger multiple invocations of the workflow being tested for a large number of input argument sets.

Here's an example test workflow that uses the matrix strategy for the `add.yaml` workflow you saw earlier:

~~~{.yaml caption="add.yaml"}
name: Test workflow

on: 
  workflow_dispatch:

jobs:
  test:
    strategy:
        matrix:
          number1: [1, 2, 3, 4, 5, 6, 7]
          number2: [7, 6, 5, 4, 3, 2, 1]
    uses: krharsh17/reusable-workflows/.github/workflows/add.yaml@main
    with:
      number1: ${{ matrix.number1 }}
      number2: ${{ matrix.number2 }}   
~~~

This workflow runs the `add.yaml` workflow for all possible combinations of `number1` and `number2` from the arrays defined in the `matrix` node. This allows you to test your workflow across a wide range of input values to see if it works correctly in all possible situations. Since reusable workflows depend on input and output arguments, it's relatively simple to test them via the matrix strategy, as shown here.

Here's what a test run looks like:

<div class="wide">
![Test runs]({{site.images}}{{page.slug}}/wQk0gvc.png)
</div>

You can also set up `act` to test workflows locally by simulating a GitHub Actions Runner environment on your local machine and saving some of your remote GitHub Actions usage.

### Follow Naming Conventions

Use clear and descriptive names for your workflows and workflow files. Choose names that convey the purpose and function of the workflow, making it easier for users to understand and select the appropriate workflow for their needs.

Within the workflows, try to name each job and step as descriptively as possible. You can also consider prefixing the names of reusable workflows with a common term to help your team members quickly identify reusable workflows from all workflows in a repository.

### Consider Platform Compatibility

When designing reusable workflows, be mindful of platform dependencies and compatibility. Ensure that your workflows work across different operating systems and versions of the tools and dependencies they rely on.

If possible, don't use dependencies (third-party actions) that do not run on all environments. If you have to, make sure the platform compatibility of the reusable workflow is clearly defined in its documentation so that your team members aren't left to figure out why the workflow keeps failing.

### Continuously Improve and Refine

Encourage feedback from users of your reusable workflows and iterate on them based on their needs and suggestions. Continuously improving your workflows based on user feedback helps make your workflows more robust, flexible, and user-friendly.

## Conclusion

Reusable workflows make it convenient to isolate reusable logic from your CI/CD pipelines and reuse them across multiple repositories and pipelines. However, they can get quite tricky to track and manage if you aren't careful with them.

If writing pipelines in this way is starting to seem cumbersome, then take a look at [Earthly](/). It can be used within GitHub Actions to over encapsulation and a way to organize more complex builds.

{% include_html cta/bottom-cta.html %}
