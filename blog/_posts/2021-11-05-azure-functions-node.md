---
title: "Azure Functions Deployment for Node.js Developers"
categories:
  - Tutorials
toc: true
author: Mohammed Osman
sidebar:
  nav: "deployment-strategies"
internal-links:
 - azure functions
 - azure
related: true 
excerpt: |
    Learn how to deploy Azure functions using Node.js with this tutorial. Discover the benefits of serverless computing and how it can simplify your application deployment process.
last_modified_at: 2023-08-17
---
**This article explains how to deploy Azure Functions. Earthly ensures consistent and reproducible builds in your CI/CD pipeline. [Check it out](https://cloud.earthly.dev/login).**

Deploying an application once meant provisioning a virtual machine, ensuring security protocols were in place, and installing the required frameworks—a complicated series of steps that led to unnecessary processing charges when the applications were idle.

Now, though, cloud computing has advanced to the point where you can rely on serverless computing for your platform and other deployment infrastructure and just focus on writing code.

This tutorial will introduce you to Azure functions, the Microsoft flavor of serverless computing. You'll learn how to create Node.js applications using VS Code, create Azure functions in Microsoft Azure, and finally deploy the application to Azure using the CI / CD pipeline in Azure DevOps.

## The Case for Serverless Functions

There are multiple benefits to using serverless functions in general, and Azure functions in particular.

First, you'll have less responsibility for maintaining your system. Your cloud provider will handle all infrastructure and platform concerns, allowing you to focus on what you do best: writing business logic.

Second, you'll improve your computing resources utilization since you can configure your Azure functions to run on demand and pay only for what you use. Compare that to the virtual machines scenario, where the bill keeps going up as long as you have a running VM.

These two characteristics make Azure functions suitable for specific use cases such as short running jobs, simple APIs, and other orchestration-based business workflows.

## How to Deploy an Azure Function Using Node.js

Now that you know the "what" and the "why" behind Azure functions, you can move on to the "how." These are the steps to implement an Azure function using Node.js.

### Prerequisites

Before you develop and deploy your Azure function, you need a few prerequisites.

- _Azure subscription:_ Azure, of course, is part of Microsoft Cloud. A subscription costs money, but you can use a [free trial](https://azure.microsoft.com/en-us/free/) for this tutorial.

- _Azure DevOps subscription_: Azure DevOps is a Microsoft solution for implementing [DevOps](https://azure.microsoft.com/en-us/overview/what-is-devops/). It enables you to plan, collaborate, build, and deploy your projects. You'll use it to create your build and release pipelines. There's also a [free trial](https://azure.microsoft.com/en-us/pricing/details/devops/azure-devops-services/) available for this service. Choose **start** from **Azure Pipelines** under **Individual Services**.

- _VS Code (Visual Studio Code):_ VS Code is a lightweight code editor made by Microsoft for different operating systems. You can enrich it by using [extensions](https://code.visualstudio.com/docs/editor/extension-marketplace) for different platforms and programming languages. You'll use it to develop your Azure function. Find the compatible version with your OS to [download](https://code.visualstudio.com/Download).

- _Node.js:_ Node.js is an open-source JavaScript environment that enables you to build web apps. You'll need it to develop your Azure function. [Download](https://nodejs.org/en/download/) the version that works with your OS. I created this tutorial with version 8.9.3.

- _GitHub:_ Use a GitHub repository to store your source code. If you don't have an account, [head over to GitHub](https://github.com/) to create one.

### Creating Sample Function App Using VS Code

In this step, you'll create a sample Azure function app and push it to a GitHub repository.

First create a new folder for your function app project. You can use the command line to create a folder with the name `myfunctionapp` folder under `C:/` drive. Then launch VS Code in that folder.

 ```
cd c:/
mkdir myfunctionapp
cd myfunctionapp
code .
```

Install the Azure functions development extension in VS Code. This extension enables you to create, manage, and deploy Azure functions from VS Code. Remember, VS Code is a lightweight editor that you'll need to enrich with extensions. Navigate to [this link](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions) and hit **Install**. The browser will prompt you to launch VS Code; accept it to install.

Install Azure Functions Core Tools. This enables you to develop and test Azure functions on your local computer. In the VS Code top menu, click **Terminal**, then **New Terminal**. Type the command:

 ```
npm install --global azure-functions-core-tools@3 --unsafe-perm true --save-dev
 ```

Create a sample Azure function using VS Code.

- Click on **Azure Extensions** on the left menu at VS Code (it looks like the Azure icon).
- Under the **Functions** menu, click on **Create New Project.** Select the **`myfunctionapp`** folder as your project folder.
- You'll get a prompt to choose the programming language. Select JavaScript (Node.js is based on JavaScript).
- You'll get a prompt for the project template. Select **HTTP trigger**.
- Enter a name for your Azure function. Use `nodejs-function-app-<yourname>`.
- Choose the authorization level as **Anonymous**.
- If you switch to the code view, you'll notice that VS Code automatically created the scaffolding for the function app project:

<figure style="width: 350px">
  <img src="{{site.images}}{{page.slug}}/6770.png" alt="Project structure">
  <figcaption>Project structure</figcaption>
</figure>

- In `index.js`, you can find the logic of the Azure function. It receives a query string and returns a response.
- To test the function locally, hit F5 (or go to **Debug > Start Debugging** ). You should see the listening application URL in the terminal output. It should resemble the following:

 ```
http://localhost:<SomePort>/api/<yourfunctionapp>
 ```

Send an HTTP request using your browser to:

```
http://localhost: <SomePort>/api/<yourfunctionapp>?name=<yourname>
```

You should get a welcome message.

Now push the code to GitHub so that you can use it to implement build and release pipelines.

- In VS Code, click on the source control icon on the left.
- Type a message for your commit, for example: "My first Azure Function App." Commit the changes by clicking the commit icon (it looks like a tick).
- To push your changes to GitHub, click the publish icon in the bottom left. VS Code will prompt you to log in to GitHub. Accept the prompt.
- Next, it will prompt you to publish to either a private or public GitHub repository. Choose the public repository for simplicity.

Checkpoint: At this stage, your code should be published to the GitHub repository.

### Creating Function App Using Azure Portal

Now, switch to Azure to create the required function to deploy your app.

- Sign in to the Azure portal.
- Click **Create a resource**.
- In the search box, type **Function App**. Azure Function and Function App are the same. Click **Create**.
- Enter your Azure subscription.
- Create a new resource group (for example, "myfunctionapp-rg").
- Choose a function app name (for example, "nodejs-function-app-<yourname>"). The Azure function name should be unique across Azure.
- Choose the publish type. Choose Code. You can create a function app Docker container by using a repeatable build tool such as [_Earthly_](https://cloud.earthly.dev/login).
- Choose the runtime as **Node.js**, then runtime version as **14 LTS**.
- Choose the closest Azure region to you. Aim to store your function apps geographically close to your customers to ensure high performance.
- Click on **Next: Hosting**.
- Choose your storage account (required for Azure functions code storage).
- Choose the operating system as **Linux**.
- Choose your plan type as **Consumption (Serverless)**. It is a lightweight plan that only charges you when your functions are running. You can read about other plan types [in Microsoft's documentation](https://docs.microsoft.com/en-us/azure/azure-functions/functions-scale?WT.mc_id=Portal-WebsitesExtension).
- Click **Review + create**. You'll get a summary of your settings. Validate them.
- Hit **Create** to create the Azure function. In a few minutes, your deployment should be complete.

Checkpoint: At this stage, you should have your code pushed to GitHub and your Azure function created in Azure.

### Creating CI/CD Pipeline

Now you'll create a build and release pipeline that pulls your Azure function code from GitHub, builds it, and deploys it to Azure.

- Navigate to Azure DevOps. If it's your first time launching Azure DevOps, you'll get a prompt to create a new organization. Go ahead and do that.
- You'll get a prompt to create a new project. You can name it "My First Function App." Keep it private and click **Create**.
- Click **Pipelines > Pipelines** on the left, then click **Create Pipeline**.
- Click **GitHub** since this is where you stored your code. Azure DevOps will redirect you to GitHub because it requires authorization to access your code. Click **Authorize AzurePipelines**.
- Choose your code repository in GitHub. You called it `myfunctionapp`. Azure DevOps will analyze your codebase to suggest a suitable pipeline template.
- Click **Node.js Function App to Linux on Azure**.
- You'll get a prompt to choose your Azure subscription. Choose yours and click **continue**.
- Choose the function app you created in Azure. It was "nodejs-function-app-<yourname>".
- Click **Validate and configure**. Azure DevOps will create a pipeline YAML file that contains your setup configuration.
- Click **Save and run**. Azure DevOps will commit the pipeline YAML file to your codebase in GitHub. Choose a commit name and then click **Save and run** again.

It will start running the build and deployment stages of your pipeline. The execution of the build and deployment stages is on an Azure-hosted agent. After the pipeline finishes execution, you should see the following in Azure DevOps:

![Successful deploy in Azure DevOps]({{site.images}}{{page.slug}}/6480.png)

Microsoft recently started limiting Azure-hosted agent usage for new Azure DevOps organizations. If you are following this tutorial and have created a new Azure DevOps organization, you are likely to get the following error:

> No hosted parallelism has been purchased or granted. To request a free parallelism grant, please fill out the following form: [https://aka.ms/azpipelines-parallelism-request](https://aka.ms/azpipelines-parallelism-request).

Fill out the form to ask Microsoft to enable Azure-hosted agent usage for your Azure DevOps organization.

Checkpoint: You should now have your code pushed to GitHub, your Azure function created in Azure, and your code built and deployed to the Azure function.

### Test and Verify

Test your Azure function by browsing to the following HTTP endpoint:

```
https://nodejs-function-app-<yourname>.azurewebsites.net/api/nodejs-function-app-<yourname>?name=<yourname>
 ```

You should get this response:

 ```
Hello, <yourname>. This HTTP triggered function executed successfully.
 ```

## Conclusion

Congratulations on implementing your first serverless function! Now you know how to help your business save on computing costs and reduce time to market on new developments.

Of course, Azure functions development is a big topic. If you are interested in learning more, check out the [Microsoft documentation](https://docs.microsoft.com/en-us/azure/azure-functions/functions-scale?WT.mc_id=Portal-WebsitesExtension). Keep in mind that there is no free lunch. While Azure functions make it easy for you to develop applications quickly and cheaply, you'll lose flexibility in controlling your infrastructure, so be sure to weigh your options carefully.

To further assist your build process, try [Earthly](https://cloud.earthly.dev/login). This free automation tool helps you execute your builds in containers. It works with multiple platforms and offers flexible caching and parallelism, so you can quickly build, test, and [deploy](/blog/deployment-strategies) your projects.

{% include_html cta/bottom-cta.html %}
