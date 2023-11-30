---
title: "Using GitHub Actions to Run, Test, Build, and Deploy Docker Containers"
categories:
  - Tutorials
toc: true
sidebar:
  nav: github-actions
author: James Olaogun
editor: Bala Priya C
internal-links:
 - Github Actions
 - Deployment
 - Testing
 - Build
 - Docker Container
excerpt: |
    Learn how to automate the process of developing, testing, building, and deploying Docker containers using GitHub Actions. This tutorial will guide you through the steps of creating a workflow, setting up a runner, running GitHub Actions locally, and setting up the build and test stages. Save time and improve the quality of your software with this powerful automation tool.
last_modified_at: 2023-07-11
---
**This article explains how to automate Docker using GitHub Actions. Earthly's caching mechanisms speed up your GitHub Actions pipeline. [Learn how](https://cloud.earthly.dev/login).**

GitHub Actions is a flexible tool that enables developers to automate a variety of processes, including developing, testing, and deploying, right from their GitHub repositories. The automation of Docker containers is no exception since GitHub Actions also enables developers to automate the process of developing containerized applications. As a result, developers can save time and focus on improving the overall quality of their software.

In this article, you'll learn how to use Github Actions to run, test, build, and deploy Docker containers using GitHub Actions.

## How to Run, Test, Build, and Deploy Docker Containers Using GitHub Actions

Before you begin this tutorial, you'll need the following:

- [GitHub account](https://github.com)
- Basic knowledge of Docker and Docker Compose
- Basic knowledge of YAML files

Once these prerequisites are met, it's time to begin. You'll start by creating a sample workflow, and then set a runner for the workflow. After that, you'll learn how to set up GitHub Actions locally and then how to set up the build and test stage. Finally, you'll execute the workflow by running the action.

### Create a Workflow

The first thing you need to do is create a workflow using GitHub Actions. This workflow defines the steps that GitHub Actions should take when triggered, including checking out the code, building a Docker container, running tests, and deploying the application.

To create a workflow, log into your GitHub account and navigate to the repo you want to automate. Select **Actions** from the navigation bar, which will take you to the **Actions** page:

<div class="wide">
![GitHub Actions]({{site.images}}{{page.slug}}/UWSEDSN.png)
</div>

At this point, you have two options: you can either select any of the workflow examples/templates or create a new one from scratch. Here, the **Deploy to Amazon ECS** example was chosen under the **Deployment** template. This workflow example essentially deploys a container to an [Amazon Elastic Container Service (Amazon ECS)](https://aws.amazon.com/ecs/):

<div class="wide">
![**Deploy to Amazon ECS** example template]({{site.images}}{{page.slug}}/J5BbN1U.png)
</div>

<div class="notice--info">
The GitHub workflow configuration is always in YAML format, and you'll see many of the following popular parent key-value pairs in your workflows:

- **`name`** defines a unique name for the workflow.
- **`on`** specifies the trigger for the workflow, such as when a push is made to the repository or a pull request is opened.
- **`jobs`** contains one or more jobs that make up the workflow.
- **`steps`** specifies a list of steps to run in a job.
- **`env`** defines [environment variables](/blog/bash-variables) that will be used in the workflow.
- **`runs-on`** specifies the type of runner to use for a job.

</div>

### Set Up a Runner

Once you've created your workflow, you need to set up a runner. A runner, in this context, is the environment or operating system that processes the actions when the workflow is executed. There are two types of runners in GitHub Actions: [self-hosted runners](https://docs.github.com/en/actions/hosting-your-own-runners/about-self-hosted-runners) and [GitHub-hosted runners](https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners).

To set up a runner, open your workflow YAML file. Following the **Deploy to Amazon ECS** workflow template, you should see the `jobs` key with a `deploy` child key, followed by the `runs-on` key. The `runs-on` key is what defines the runner to be used for executing the job. See the following code snippet as an example:

~~~{.yml caption=""}
jobs:
  deploy:
    name: Deploy
    runs-on: ubuntu-latest
    environment: production

    steps:
    - name: Checkout
      uses: actions/checkout@v3
…
~~~

In this code snippet, the runner is the `ubuntu-latest` runner, which is a GitHub-hosted runner provided by GitHub Actions. Aside from `ubuntu-latest`, there are several other GitHub-hosted runners, such as `windows-latest`, `macos-latest`, and `centos-8`, that you can use in GitHub Actions.

When the workflow is triggered, GitHub Actions will allocate an available runner of the specified type `ubuntu-latest`. The runner will then execute each step defined in the `steps` key, starting with the `Checkout` step. You can review the `steps` section in the **Deploy to Amazon ECS** as an example:

<div class="wide">
![*Deploy to Amazon ECS* steps section]({{site.images}}{{page.slug}}/teXRquk.png)
</div>

### Set Up GitHub Actions Locally

Considering the limited [build minutes](https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions#about-billing-for-github-actions) that GitHub Actions provides, it's recommended that you conduct a test run of the workflow locally as the workflow will fail to complete if the allotted build time is exceeded. Additionally, setting up GitHub Actions locally allows you to test your workflow locally before you push it to your GitHub repository. This helps ensure that your workflow is working as expected and will run successfully on a GitHub Actions runner.

To set up GitHub Actions locally, you need to first clone or pull the latest changes from your GitHub repository that contains the workflow you want to run locally. Then change the directory to the root directory of the code.

Then install [Act](https://github.com/nektos/act#installation) on your local machine. Act is a tool that will enable you to run your GitHub Actions locally. After the installation, connect your GitHub token to Act by logging into your GitHub account and navigating to **Settings > Developer settings > Personal access tokens (classic)**. You can either use an existing token if you still have access to it or generate a new token:

<div class="wide">
![**Personal access tokens** page]({{site.images}}{{page.slug}}/hKztz9s.png)
</div>

Copy the generated token and run the following command:

~~~{.bash caption=">_"}
act -s GITHUB_TOKEN={{YOUR_GITHUB_TOKEN}}
~~~

Make sure to replace `{{YOUR_GITHUB_TOKEN}}` with your generated token. If it is your first time running the command, you will be asked to select the default image you want to use with `act`. You can select the "medium" image.

<div class="notice--warning">

### ❗Act Problems?

`Act` can run simple GitHub Action workflow locally using a fairly large docker container. But not all features of GitHub Actions work well with `Act`.

An alternate approach covered in [other articles](/earthly-github-actions) is to write your workflow in an Earthfile. An Earthfile can be run locally or in any CI.

</div>

When finished, clone your GitHub repo with the workflow file if you haven't, and proceed to use Act to run your GitHub Actions locally by running the `act -n` command to [dry run](https://en.wikipedia.org/wiki/Dry_run_(testing)) the workflow. You should see the run log:

<div class="wide">
![Test workflow run log]({{site.images}}{{page.slug}}/ZT3S7It.png)
</div>

You can also run other commands, including the command that runs a specific job, lists all actions for all events, or runs a specific event. You can check out the [documentation](https://github.com/nektos/act#example-commands) to see a list of all the available commands.

### Set Up the Build Stage

Now that you've gotten your GitHub Actions to work locally, you can use it to debug and test your workflow locally, make any necessary changes to the workflow, and rerun it until you're satisfied with the results before pushing your code to GitHub.

Once each step defined in the `steps` key of your workflow file is tested and working as expected, you need to run your `docker-compose` file or build your Docker images. To do that, add a new value to the `steps` key with a `name`, `id`, and `run` key. It may also have an `env` key if the Docker image requires a passkey.

The `name` key can be `Build docker images`, the `id` key will have any unique string, and the `run` key will contain the build command as the value:

~~~{.yml caption=""}
{% raw %}
- name: Build docker images
  Id: build-image
  run: | 
    echo ---Building images and starting up docker---
    {{docker build [image-url] or docker-compose -f \
    [docker-compose file] up -d }}
    echo ---Containers up—
{% endraw %}
~~~

Following the **Deploy to Amazon ECS** workflow template that's been used here, the build step can be found on line 67:

~~~{.yml caption=""}
{% raw %}
- name: Build, tag, and push image to Amazon ECR
      id: build-image
      env:
        ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
        IMAGE_TAG: ${{ github.sha }}
      run: |
        # Build a docker container and
        # push it to ECR so that it can
        # be deployed to ECS.
        docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
        echo "image=$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG" >> \
        $GITHUB_OUTPUT
{% endraw %}
~~~

This template's build step uses the `env` key since `ECR_REGISTRY` requires a login and SHA key.

### Set Up the Test Stage

Once you're done setting up the build stage, the next thing you need to do is set up the test stage. Because the **Deploy to Amazon ECS** workflow template is primarily a deployment template, the test stage isn't factored into it. However, the test stage is the recommended phase since it helps you verify the functionality and connections of your applications (including the workflow file) before pushing to GitHub to run the workflow actions.

To set up the test stage, you can either create a test folder in your application or in a different folder outside your application, then develop all your test cases. Afterward, ensure your test folder is containerized in the same network as your application. If you're using [Docker Compose](/blog/youre-using-docker-compose-wrong), GitHub Actions will run the workflow in a user-defined network. And for communication to happen, your application and test folder must be in the same network. The network in this context is the Docker Compose network.

The purpose of this network is to provide a Docker network for the containers defined in the `docker-compose` file, allowing them to communicate with each other and with the host system. Containers in separate networks cannot communicate, which means that API test cases won't be able to get a response from the services in other networks. You can learn more about creating a `docker-compose` file with a network [in this article](/blog/docker-networking).

When you're done adding the test cases folder to the same container network, you need to add a new value to the `steps` key of your workflow file. The new value will contain a `name`, `id`, and `run` key:

~~~{.yml caption=""}
- name: Run test cases
   id: run-test-cases
  run: |
    echo --- Running test cases ---
    docker-compose -f {{docker-compose-file}} -p {{project-name}} \
    up --build --exit-code-from {{container-name}}
    echo --- Completed test cases ---
~~~

In this code, `{{docker-compose-file}}` is the name of your `docker-compose` file, `{{project-name}}` is the project name, and `[{{container-name}}` is the container name.

<div class="notice--big--primary">
As an alternative to using a `docker-compose` file, you can leverage [Earthly](https://cloud.earthly.dev/login), which lets you define your containers and their dependencies, as well as specify your entire build process, including testing and deployment, in one **Earthfile**.

In addition, Earthly allows you to define reusable builds that you can use across different machines, making it easier to collaborate and enabling you to run your builds anywhere.

Moreover, Earthly caches your build components, making the process efficient and fast. Check out the [official documentation](https://docs.earthly.dev/basics) to learn more about getting started with Earthly.
</div>

### Run the Action

After you've set up the test stage, the final step is to run the action. To do that, you need to push the changes made to your workflow file to your GitHub repository. The workflow will be triggered based on the branches you set it to monitor on the `on` key of your workflow file.

You can also monitor the progress of the workflow by visiting the **Actions** tab in your repository on GitHub and selecting a workflow that has previously been run or the currently running workflow:

<div class="wide">
![Workflow history]({{site.images}}{{page.slug}}/VQCqOYR.png)
</div>

## Conclusion

In this tutorial, you learned how to create a new workflow, edit an existing workflow, set up the runner for your workflow, and locally set up and work with GitHub Actions. At this point, you should be confident that you can build GitHub Actions for your projects and speed up the development processes.

And if you're looking to continue building out your GHA workflows, consider using [Earthly](https://cloud.earthly.dev/login). Earthly runs everywhere, including GitHub Actions and can improve the reliability of your CI/CD pipelines. It works great with [GitHub Actions](/earthly-github-actions) and docker.

{% include_html cta/gha-cta1.html %}
