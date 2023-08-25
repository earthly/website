---
title: "Create Automated CI/CD Builds Using GitHub Actions and DockerHub"
categories:
  - Tutorials
toc: true
sidebar:
    nav: github-actions
author: Rose Chege
editor: Mustapha Ahmad Ayodeji
last_modified_at: 2023-06-26
internal-links:
 - CI/CD
 - Github Actions
 - DockerHub
 - Automation
excerpt: |
    
---
**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster. This article is about GitHub Actions, if you'd like to see how Earthly can improve your GitHub Actions builds then [check us out](/earthly-github-actions).**

To streamline your development workflow, in this tutorial, we will explore the power of GitHub Actions in automating CI/CD builds. Specifically, we will focus on leveraging GitHub Actions to automate Docker builds and facilitate seamless deployments to DockerHub. Join us as we construct an automated CI/CD pipeline using GitHub Actions and DockerHub.

## Prerequisites

To follow along with this article, it is essential to have the following:

- [Node.js](https://nodejs.org/en/) installed on your computer.
- [Docker](https://www.docker.com/) installed on your computer.
- GitHub and DockerHub accounts.
- Basic knowledge of working with Docker.
- Basic knowledge of how to use GitHub.
- Familiarity editing YAML files.

## Creating the Application and a Dockerfile to Build the Application Image

To get started, you need an application to put into a Docker image. In this guide, you will develop a simple Node.js application with a single endpoint that just print `Hello World` to the screen. Alternatively, if you have an application you have already developed, you can use it along and achieve the same objective this guide aims for.

The simple Node.js application will be created as follows:

From your preferred working directory, initialize the application:

~~~{.bash caption=">_"}
npm init -y
~~~

Install [express](https://expressjs.com/) for setting up the web server:

~~~{.bash caption=">_"}
npm install express
~~~

Create an `app.js` file to host the application logic as follows:

- Import the necessary packages:

~~~{.js caption="app.js"}
const express = require('express');
~~~

- Define the express instance and the port for the application:

~~~{.js caption="app.js"}
const app = express();
const PORT = process.env.PORT || 4000;
~~~

- Define a default testing route:

~~~{.js caption="app.js"}
app.get('/',(req,res) => {
    res.status(200);
    res.send("Hello World!!");
});
~~~

- Start the application:

~~~{.js caption="app.js"}

app.listen(PORT, () => console.log(`App listening on port ${PORT} `));
~~~

The whole code in the *apps.js* looks as shown below:

~~~{.js caption="app.js"}
const express = require('express');

const app = express();
const PORT = process.env.PORT || 4000;

app.get('/',(req,res) => {
    res.status(200);
    res.send("Hello World!!");
});

app.listen(PORT, () => console.log(`App listening on port ${PORT} `));
~~~

- In the `package.json` add a script for running the application:

~~~{.js caption="package.json"}
"start":"node app.js"
~~~

You can test your application and ensure it works as expected by starting the development server using the following command:

~~~{.js caption="app.js"}
npm run start
~~~

From your browser, go to `http://localhost:4000` to check if the application works as expected.

<div class="wide">
![A simple Node.js app showing Hello World]({{site.images}}{{page.slug}}/FjB1m1G.png)
</div>

To run this application with Docker, you need to provide the correct command for packaging it. To do this, you can use a Dockerfile, which specifies the instructions to build a Docker image. Once the image is built, it contains everything required to run the application, including the code, runtime, libraries, and settings. This results in a Docker container image that can be used to run the application on any Docker-supported platform.

In your application directory, create a file named `Dockerfile`. In this `Dockerfile`, add the commands for building the image step by step as follows:

Specify the base image to use, in this case, the node version:

~~~{.dockerfile caption="Dockerfile"}
FROM node:19
~~~

Define the working directory, where the application will reside inside the Docker:

~~~{.bash caption=">_"}
WORKDIR /usr/src/app
~~~

Copy `package.json` to the working directory:

~~~{.bash caption=">_"}
COPY package*.json .
~~~

Run the `npm install` command to install the application dependencies on Docker:

~~~{.bash caption=">_"}
RUN npm install
~~~

Copy the rest of the application files to Docker, i.e., `app.js`:

~~~{.bash caption=">_"}
COPY . .
~~~

Expose the port the application will run on:

~~~{.bash caption=">_"}
EXPOSE 4000
~~~

Define the command to run the application. This is the same command that Node.js runs on when creating the application locally:

~~~{.bash caption=">_"}
CMD = ["npm","run", "start"]
~~~

Your complete code in the Dockerfile should be as shown below:

~~~{.dockerfile caption="Dockerfile"}
FROM node:19
WORKDIR /usr/src/app
COPY package*.json .
RUN npm install
COPY . .
EXPOSE 4000
CMD = ["npm","run", "start"]
~~~

>If you are using a different application, ensure your `Dockerfile` reflects the instruction needed to dockerize your application.

Build the Docker image to check if these instructions work correctly on Docker:

~~~{.bash caption=">_"}
docker build . --tag node_app 
~~~

And run the application on docker:

~~~{.bash caption=">_"}
docker run -it -p 4000:4000 node_app
~~~

The results should remain the same as when you tested the application locally. Otherwise, recheck the above steps and ensure that you entered the code correctly.

## Creating a Github Repository and Pushing the Application to Github

GitHub actions require you to host your application code on a remote repository, including the `Dockerfile` containing the Docker commands. A GitHub repository stores your code and related files.

[Create a GitHub repository](https://docs.github.com/en/get-started/quickstart/create-a-repo) to add all your code and add you project so far to it.

If you're not familiar with Git then I recommend using a Git client with a graphical user interface (GUI), such as GitHub Desktop to make working with Git repositories on GitHub easier. Here's a brief overview of how to use GitHub Desktop to push code changes to your remote GitHub repository:

- Open GitHub Desktop and log in using your GitHub account
- Select the repository you have created on your GitHub page and open it with GithHub Desktop:

<div class="wide">
![Open repository with GitHub Desktop]({{site.images}}{{page.slug}}/z3eCRBz.png)
</div>

- Clone the repository:

<div class="wide">
![Clone a GitHub repository]({{site.images}}{{page.slug}}/FM0FobH.png)
</div>

- Add your application code in the local cloned repository
- Review the changes on GitHub Desktop, add a commit message summarizing your changes and click the Commit button:

<div class="wide">
![Adding files using GitHub Desktop]({{site.images}}{{page.slug}}/ddRx6uU.png)
</div>

- Click the Publish button to push your code to the remote GitHub repository:

<div class="wide">
![Pushing changes to GitHub]({{site.images}}{{page.slug}}/ATE8WYC.png)
</div>

## Setting Up DockerHub

The GitHub action that you will set up will push the application image to the DockerHub repository. Therefore, you must have the correct access token for GitHub Actions to access your DockerHub account. In the DockerHub account portal, you will create an access key for GitHub to connect to your DockerHub account. You can create a new access key as follows:

Navigate to your account **setting**, **security** and click on the **New Access Token**:

<div class="wide">
![Create a new DockerHub access token]({{site.images}}{{page.slug}}/WZEzcDF.jpg)
</div>

Specify the access token description and permission:

<div class="wide">
![Generate a new DockerHub access token]({{site.images}}{{page.slug}}/aoHh73M.jpg)
</div>

Copy the access token:

<div class="wide">
![Copy DockerHub access token]({{site.images}}{{page.slug}}/bQ5oYZj.jpg)
</div>

>Once the key is ready, it should be copied immediately and saved securely because it will be provided only once and cannot be retrieved, and it will not be stored on DockerHub. The key will be required for the upcoming steps.

## Creating a GitHub Actions Workflow

With all the application code available remotely, you can create a GitHub Actions workflow that will automate the build process and save the build artifacts to DockerHub.

### Connecting GitHub Actions With DockerHub

To set up a workflow, GitHub must communicate with DockerHub using the DockerHub access token (that you just created) and your DockerHub username. Your DockerHub access token is a confidential information, and you need to add it as a secret environment variable on GitHub. The workflows will execute this access token and username as secret environment variables on GitHub.

To add the secret environment variables, navigate to the repository you created on Github

In your repository, navigate to **Settings**, **Secrets and Variables**, and **Actions** sections as follows:

<div class="wide">
![Creating GitHub Actions environment variables]({{site.images}}{{page.slug}}/jdGYMqh.jpg)
</div>

Click on the **New repository secret** button:

<div class="wide">
![Adding GitHub Actions environment variables]({{site.images}}{{page.slug}}/fPge5wm.jpg)
</div>

Create a `DOCKERHUB_USERNAME` variable and add your DockeHub username as the value:

<div class="wide">
![New GitHub Actions environment variables]({{site.images}}{{page.slug}}/YdIyEoC.png)
</div>

Create a `DOCKERHUB_TOKEN` variable and add the access token you created earlier as the value. You should have the following results:

<div class="wide">
![Docker access token and username as GitHub secret environment variables]({{site.images}}{{page.slug}}/Dz4Y51v.jpg)
</div>

### Implementing the GitHub Actions Workflow

GitHub Actions workflow includes creating the processes that trigger [events, jobs, and steps](https://docs.github.com/en/actions/learn-github-actions/understanding-github-actions) that set up a workflow. The docker image will be built and deployed to the DockerHub when you push the code to the main branch of the GitHub repository. Therefore, the GitHub Actions workflow needs to initiate a push event on the main branch of the Github repository you hosted your application code.

To setup the workflow, you need to create the workflow file. You can create one as shown below:

Click on the **Actions**` tab in your repository and click the **set up a workflow yourself**:

<div class="wide">
![Creating a GitHub Action workflow]({{site.images}}{{page.slug}}/FfMgwbq.jpg)
</div>

On the resulting editor, add the following workflow to the `main.yml` file as follows:

Define the build trigger:

~~~{.yml caption="main.yml"}
name: node_app

on: # specify the build to trigger the automated ci/cd
    push:
        branches:
            - "main"
~~~

GitHub Actions will name this configuration `node_app`. The code specifies the trigger as a push event (changes) to your application code's `main` branch on the GitHub repository you created.

Define the job that indicates the steps to checkout the code and build the Docker images:

~~~{.yml caption="main.yml"}
jobs:
    build:
        name: Build Docker image
        runs-on: ubuntu-latest # specify the build machine
        steps:
~~~

GitHub Actions uses `jobs` to define one or more tasks that your CI/CD pipeline will run. In the code above, the `build` specifies the steps and it also specifies the machine type that the steps will run on using the [`runs-on`](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idruns-on) keyword. The value of `ubuntu-latest` indicates an ubuntu machine as the pipeline environment. The `steps` will define a list of stages to be executed in sequence to fulfill the pipeline objectives.
This steps are as follows:

Define the steps that will checkout the code:

~~~{.yml caption="main.yml"}
- # checkout to the repository on the build machine
    name: Checkout
    uses: actions/checkout@v3
~~~

The `uses: actions/checkout@v3` syntax clones your Github repository to the `ubuntu-latest` build machine. This will make the code available to the subsequent steps in executing the job.

Define the step to sign in to DockerHub with the credentials in the GitHub Action environment variable secrets:

~~~{.yml caption="main.yml"}
- # login to Docker Hub using the secrets provided
    name: Login to Docker Hub
    uses: docker/login-action@v2
    with:
        username: ${{ secrets.DOCKERHUB_USERNAME }}
        password: ${{ secrets.DOCKERHUB_TOKEN }}
~~~

The `uses: docker/login-action@v2` syntax allows GitHub Action to log in to your DockerHub registry based on the `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` you added as GitHub Actions environment variables.

Define the step that setup the Docker Buildx:

~~~{.yml caption="main.yml"}
- # create a build kit builder instance
    name: Set up Docker Buildx
    uses: docker/setup-buildx-action@v2
~~~

The `uses: docker/setup-buildx-action@v2` syntax creates a [Docker Buildx builder](https://docs.docker.com/engine/reference/commandline/buildx_build/) instance. It uses a [`docker buildx`](https://docs.docker.com/engine/reference/commandline/buildx/) command that builds Docker images to your desired architectures.

Define the step that build and push the docker image to DockerHub. The workflow will build the image based on the `Dockerfile` commands and tag the images. It will finally push and deploy the built image to your DockerHub as follows:

~~~{.yml caption="main.yml"}
- # build the container image and push it to Docker Hub with \
 # the name clockbox.
    name: Build and push
    uses: docker/build-push-action@v4
    with:
        context: .
        file: ./Dockerfile
        push: true
        tags: ${{ secrets.DOCKERHUB_USERNAME }}/clockbox:latest
~~~

The `uses: docker/build-push-action@v4` syntax will execute your Dockerfile, push the resulting image to your DockerHub registry, and tag it as `${{ secrets.DOCKERHUB_USERNAME }}/clockbox:latest`.

The whole workflow code is as shown below:

~~~{.yml caption="main.yml"}
name: node_app

on: # specify the build to trigger the automated ci/cd
    push:
        branches:
            - "main"

jobs:
    build:
        name: Build Docker image
        runs-on: ubuntu-latest # specify the build machine
        steps:
            - # checkout to the repository on the build machine
                name: Checkout
                uses: actions/checkout@v3
            - # login to Docker Hub using the secrets provided
                name: Login to Docker Hub
                uses: docker/login-action@v2
                with:
                  username: ${{ secrets.DOCKERHUB_USERNAME }}
                  password: ${{ secrets.DOCKERHUB_TOKEN }}
            - # create a build kit builder instance
                name: Set up Docker Buildx
                uses: docker/setup-buildx-action@v2
            - # build the container image and push it to Docker \
                # Hub with the name clockbox.
                name: Build and push
                uses: docker/build-push-action@v4
                with:
                  context: .
                  file: ./Dockerfile
                  push: true
                  tags: ${{ secrets.DOCKERHUB_USERNAME }}/clockbox:latest
~~~

## Testing the Builds with GitHub Actions

To deploy the workflow, click on **Start commit**, add a commit message, and submit:

<div class="wide">
![The start commit button]({{site.images}}{{page.slug}}/9feGKlX.png)
</div>

Navigate to the `Actions` tab to view the job and the build status.

<div class="wide">
![Checking the workflow]({{site.images}}{{page.slug}}/7QUay3g.jpg)
</div>

After committing from the previous step, the build should start automatically:

<div class="wide">
![The GitHub Action build image stage]({{site.images}}{{page.slug}}/xSiA3A1.png)
</div>

Once The GitHub workflow executes all the steps, the build will be completed as follows:

<div class="wide">
![The build steps and status]({{site.images}}{{page.slug}}/fvHxnna.png)
</div>

From your DockerHub dashboard, you should be able to view the image that has just been deployed:

<div class="wide">
![The Docker Image on DockerHub]({{site.images}}{{page.slug}}/UYadTPj.png)
</div>

## Conclusion

GitHub Actions and DockerHub integration streamline your development process. Automating your builds and deployments pipelines creates team efficiency while reducing errors and increasing productivity.

This article has shown you how to create an automated CI/CD build with GitHub and DockerHub. In this article, you have learned:

- How to dockerize an application with Docker
- How to create and deploy an application from GitHub Actions
- How to automatically build and push a Docker image DockerHub with GitHub action.

The code used in this tutorial can be found in this [GitHub repository](https://github.com/Rose-stack/node_app). And if you're looking to continue building out your GHA workflows, consider using [Earthly](https://earthly.dev). Earthly runs everywhere, including GitHub Actions and can improve the reliability of your CI/CD pipelines. It works great with [GitHub Actions](/earthly-github-actions) and docker.

{% include_html cta/gha-cta1.html %}
