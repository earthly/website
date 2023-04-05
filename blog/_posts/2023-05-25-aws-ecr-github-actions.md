---
title: "Deploy Applications to AWS ECR with a GitHub Actions CI/CD Pipeline"
categories:
  - Tutorials
toc: true
author: Rose Chege

internal-links:
 - just an example
---

CI/CD automates the application development pipeline. It eliminates manual deployments from your initial code commit to production deployment integrations. Deploying applications using GitHub Actions as CI/CD pipeline provides a streamlined, secure approach to managing application releases. 

Its practice allows teams to build, test, and deploy applications quickly and reliably. This article will help you learn how to deploy applications to AWS ECR using GitHub actions workflow.

## The Role of CI/CD and GitHub Actions

CI allows your teams to merge code changes into the shared repository. Each code change is integrated into the main branch of a shared source code repository. Each code commit triggers a CI process to automatically test and build the new changes. CD will then package the application changes and deploy them to your provisioned infrastructure environments.

### GitHub Actions for CI/CD

[GitHub Actions](https://docs.github.com/en/actions) is a perfect tool for automating your development workflows, such as CI/CD. GitHub allows you to host your application code. Any team member can contribute changes to a shared GitHub repository. The changes are merged and accepted as part of the main code. You need a pipeline that will test, build and create a new deployment for these changes. GitHub Actions allows you to set a channel that will automatically trigger such tasks.

## Docker Deployments with AWS ECR

You require a packaged application that is easily portable throughout the pipeline. Docker provides a consistent and isolated environment for building, testing, and deploying applications. It allows you to create Docker images that package an application and its dependencies into a single portable artifact. This makes it easier to trigger changes across different stages of the pipeline.

To manage a Docker image, you need infrastructures allowing you to store and retrieve images while maintaining application scalability. AWS provides [ECR](https://aws.amazon.com/ecr/) as a fully managed container registry service to deploy your application using Docker.

Let’s dive in and create a GitHub Actions workflow that will automate deployments to [AWS ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html).

### Prerequisites

Before proceeding with this guide, you require the following:

- [Docker Engine](https://docs.docker.com/get-docker/) installed on your computer.
- [AWS CLI](https://aws.amazon.com/cli/) installed.
- [Git](https://git-scm.com/downloads) installed and [configured with GitHub](https://docs.github.com/en/get-started/quickstart/set-up-git).
- Basic knowledge of working with AWS and GitHub.

Check the code used in this guide in [this GitHub repository](https://github.com/Rose-stack/nodes-app).

## Setting up the AWS IAM

To allow GitHub Actions to communicate with AWS, you’ll need an [AWS IAM user account](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html) to manage access to AWS resources. You can achieve it using AWS CLI.  It Provides commands for interacting with various AWS services, such as ECR.

To create an IAM user, run the following command in your terminal:

```bash
aws iam create-user --user-name your_username
```

Replace `your_username` with your preferred username of choice.

Give the created user access to the AWS Management Console by creating a login profile:

```bash
aws iam create-login-profile --user-name your_username --password your_password
```

Replace`your_username` with your preferred username and `--password` with your preferred password.

This user requires a user group. In this example, give the user the Admins privilege for simplicity purposes:

```bash
aws iam create-group --group-name your_group_name
```

Replace `your_group_name` with your preferred group name such as `Admins`.

Add the above user to the group to IAM:

```bash
aws iam add-user-to-group --user-name your_username --group-name your_group_name
```

Replace `your_username` with your username and `your_group_name` with the group's name.

To give programmatic access to the user, you will need to create the access keys below:

```bash
aws iam create-access-key --user-name your_username
```

Replace `your_username` with your preferred user name.

From above, you will get an output with an `AccessKey` and the `Secret access key`. Copy these keys and save them somewhere. You will require them to send calls to AWS programmatically using GitHub Actions later in this guide.

For the user to be able to programmatically create a deployment to ECR, you will need to add a policy for that and give access to the ECR resources.

To add the policy:

- Login to your AWS Management Console.
- Under IAM > Users, locate the user you created and navigate to it.
- On the permissions tab, click on `Add Inline Policy` as follows:

![](https://imgur.com/9PB8QEH)

On the resulting page under the JSON tab, paste in the following rules to give full access to `ecr` and `cloudtrail`. This will grant us full access to container images within these services.

 
![](https://imgur.com/AI7eqgV)

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ecr:*",
                "cloudtrail:LookupEvents"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "iam:CreateServiceLinkedRole"
            ],
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "iam:AWSServiceName": [
                        "replication.ecr.amazonaws.com"
                    ]
                }
            }
        }
    ]
}
```

Review the above policy and enter the name of the policy; create the policy, and it will be added to your user.
 
![](https://imgur.com/hSYnLji)

## Creating a GitHub Repository

[GitHub Actions](https://docs.github.com/en/actions/quickstart) requires a repository for hosting and sharing the code. It will trigger its workflow based on your current code on a GitHub repository. Navigate to your [GitHub account](https://github.com/) and create the GitHub Repository online.

This Repository will host a simple sample [Node.js application](https://nodejs.org/en/docs/guides/getting-started-guide/). First, create the application locally as follows:

From your terminal, initialize a Node.js application:

```bash
npm init -y
```

Install express to create a simple web server:

```bash
npm install express
```

Create an `app.js` to handle the application logic:

```js
# app.js
const express = require('express');
const app = express();
const PORT = process.env.PORT || 4000;

app.get('/',(req,res) => {
    res.status(200);
    res.send("Hello World!!");
});

app.listen(PORT, () => console.log(`App listening on port ${PORT} `));
```

Add a script for starting the application on `package.json`:

```js
"start":"node app.js"
```
###  Creating Application Dockerfile

Docker will use this application and build an image that has the application code and dependencies. GitHub action will then ship the image to ECR. Therefore, you need the correct Docker command for building the application image. On the Node.js application folder, create a `Dockerfile` with instructions for building the Docker image as follows:

```dockerfile
FROM node:16 
# use node 16 image

WORKDIR /usr/src/app # set the working directory

COPY package.json . 
# copy package json to the directory
RUN npm install 
# install the dependencies
COPY . . 
# copy the files

EXPOSE 4000 
# open up port 4000

CMD ["node","app.js"] # cmd command
```

Create a `.dockerignore` to ignore the `node_modules` and npm log file on Docker while building the image. This reduces the image size by instructing Docker not to copy any unnecessary files and folders:

```dockerfile
# .dockerignore
node_modules
npm-debug.log
```

Likewise, the code will be pushed to GitHub. Therefore create a `.gitignore` to avoid shipping `node_modules` to GitHub as such:

```js
# .dockerignore
node_modules
```

Once the application is ready, it's time to use the repository you just created. First, initialize a local GitHub repository:

```bash
git init .
```

Add the project files and folders to the repository:

```bash
git add .
```

Then commit them using the following command:

```bash
git commit -am "fix: initial commit"
```

To publish the code you’re the remote repository, add the remote GitHub Repository URL you just created:

```bash
git remote add origin <remote_origin_url>
```

Finally, push the code to the online GitHub Repository:

```bash
git push origin <branch_name>
```

## Setting up AWS ECR

You will require an [ECR](https://aws.amazon.com/ecr/) to store the image the GitHub Action will build and deploy. Navigate to your AWS Management Console, and from the dashboard section, search for [Elastic Container Registry](https://aws.amazon.com/ecr/), then click on **Create a repository**.

![](https://imgur.com/wnC3tR4)

Ensure you have selected **Private**, enter the name of the repository, and create Repository:

![](https://imgur.com/vWGHWIK)

## Configure GitHub with AWS ECR

For your workflow to work, you must configure the permissions for GitHub Actions to access ECR. From the project's GitHub repository page, click on Settings. From this page, click on **Secrets and Variables** as follows:

![](https://imgur.com/3nvIsQm)

Then click on **New Repository Secret** and add the values for `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_REGION` (based on your AWS account: For example, us-east-1, ap-south-1, eu-central-1, etc.) as below:

![](https://imgur.com/t10Zyir)

You should have two keys added as follows:
 
![](https://imgur.com/AwaxYcD)

## Writing the Workflow YAML File

The most important part is to create a workflow that will trigger builds and deployments. This will create, connect the pipeline and ensure every process works as expected. Let’s discuss how to create a GitHub Actions workflow that deploys our sample  Node.js application to ECR.

The first step is to set up when the workflow should be triggered. In this case, a change to the main branch should always automatically triggers the workflow as follows:

```yaml
# deploy.yml
name: Deploy Node.js App to ECR # name

on:
  push: 
   branches: # the branch to be deployed
      - 'main'

jobs:
    build:
        name: Build Image
        runs-on: ubuntu-latest
        steps:
            - name: Check out code
              uses: actions/checkout@v2
```

This will create a name for the workflow and specifies that the workflow should be triggered on a push to the main branch.

The defined job `build` defines the series of steps that should be executed sequentially. Based on the above example, the first step that will be triggered is to check out the code from the repository using the `actions/checkout` action so that the workflows can access it.

Once the workflow has the code repository ready, you can configure AWS credentials programmatically to trigger communication with AWS as follows:

```yaml
# deploy.yml
- name: Configure AWS credentials
  uses: aws-actions/configure-aws-credentials@v1
  with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ secrets.AWS_REGION }}
```

Note that the above secrets are the keys you added to your GitHub repository secrets. Once the workflow has access to AWS, it can then log in to Amazon ECR and get ready to store the application image as follows:

```yaml
# deploy.yml
- name: Login to Amazon ECR
  id: login-ecr
  uses: aws-actions/amazon-ecr-login@v1
```

The workflow has now connected all the different stages of the pipeline. It can now trigger the build and deploy the image to ECR. Below is how the GitHub workflow will build, tag, and push the Docker image to Amazon ECR:

```yaml
# deploy.yml
- name: Build, tag, and push image to Amazon ECR
  env:
    ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
    ECR_REPOSITORY: simple_nodejs_app
    IMAGE_TAG: nodejs_simple_app
  run: |
    docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
    docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
```

In the above code example, ensure you replace `simple_nodejs_app` with the name of your ECR repository.

To execute the above workflow, on the project's GitHub repository page, navigate to the **Actions** menu and **set up a workflow yourself**:
 
![](https://imgur.com/7f6mg71)

### The Final Workflow

Name your workflow `deploy.yml` on the input section, and add your workflow code, ensuring you follow the indentation as follows:

```yaml
# deploy.yml
name: Deploy Node js App to ECR # name

on:
  push: 
   branches: # the branch to be deployed
      - 'main'
    
jobs:

    build:
        
        name: Build Image # build name
        runs-on: ubuntu-latest # build os

        steps: # sequence of tasks to be executed

            - name: Check out code # Check  the Dockerfile to build the docker image
              uses: actions/checkout@v2
            
            - name: Configure AWS credentials # Programmatic authentication to aws
              uses: aws-actions/configure-aws-credentials@v1
              with:
                    aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
                    aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
                    aws-region: ${{ secrets.AWS_REGION }}

            - name: Login to Amazon ECR
              id: login-ecr
              uses: aws-actions/amazon-ecr-login@v1

            - name: Build, tag, and push image to Amazon ECR # copying the code from repo i.e. Dockerfile, versioning the docker image, and pushing it to ECR.
              env:
                ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
                ECR_REPOSITORY: simple_nodejs_app
                IMAGE_TAG: nodejs_simple_app
              run: |
                docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
                docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
```

## Deploying to AWS ECR

To deploy your workflow, you only need to hit the `Start commit` as follows:

![](https://imgur.com/7vNrG0d)

Once you have committed, a workflow should be started automatically.

![](https://imgur.com/XBwYXnx)

Go ahead and refresh your ECR repository, and your application image will be deployed as follows:
 
![](https://imgur.com/jfi5YV3)

## Conclusion

Deploying applications to AWS ECR with a GitHub Actions CI/CD creates a reliable pipeline that automates Docker builds and deployment cycles. This guide helped you learn how to deploy an application to AWS ECR using a GitHub Actions CI/CD pipeline. I hope you found the GitHub Actions workflow useful while leveraging automation to AWS resources. To further improve your [CI/CD pipelines](https://earthly.dev/blog/ci-vs-cd/), leverage other AWS services, such as [CodePipeline](https://aws.amazon.com/codedeploy/) and [CodeDeploy](https://aws.amazon.com/codepipeline/), and streamline your pipeline infrastructure.

## Outside Article Checklist

- [ ] Create header image in Canva
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
  - Would any images look better `wide` or without the `figcaption`?
- [ ] Run mark down linter (`lint`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `link-opp` and find 1-5 places to incorporate links
- [ ] Add Earthly `CTA` at bottom `{% include_html cta/cta2.html %}`
