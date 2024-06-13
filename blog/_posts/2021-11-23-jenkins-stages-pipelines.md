---
title: "Jenkins Deployment Stages and Pipelines"
toc: true
author: Joel Olawanle
sidebar:
  nav: "deployment-strategies"
internal-links:
 - jenkins
 - jenkins pipeline
 - jenkinsfile
excerpt: |
    Learn how to automate your software development using Jenkins's deployment stages and pipeline tools. This article will guide you through the process of setting up Jenkins, creating a Jenkinsfile, and utilizing stages to automate your software deployment.
last_modified_at: 2023-08-17
categories:
  - deployment
---
**This article explains the Jenkins Pipeline automation process. Earthly streamlines the build process for Jenkins Pipeline users. [Check it out](https://cloud.earthly.dev/login).**

The software release cycle has developed over time, from the days of moving code from one machine to another to see if it works (which was frequently error-prone), to the present day, where automated techniques ensure that software programs may be deployed quickly at any time.

[Continuous deployment](/blog/deployment-strategies) is a software engineering strategy that involves automating the delivery of software features on a regular basis. Jenkins is a popular open-source continuous integration tool. It's written in Java and it can help you automate a variety of software development tasks. In Jenkins, you can create pipelines which are a sequence of tasks that processes a set of input data.

In this article, you will learn more about how Jenkins's deployment stages and pipeline tools can be used to help automate software development. You will learn how to leverage Jenkins's deployment phases and Pipeline features to help automate your software development. You'll leave with a better grasp on what a Jenkins Pipeline is and you'll know how to set up Jenkins and the Pipeline plug-in.

## What Is Jenkins Pipeline?

A `Pipeline` in Jenkins is a series of tasks or events that are interconnected in a logical order to help develop CI/CD. In other words, a Jenkins Pipeline is a collection of code-based instructions for continuous delivery that employs automation techniques to get software from version control into the hands of end users.

![Collection of Jenkins states]({{site.images}}{{page.slug}}/HrpJY8p.png)

A continuous delivery Pipeline in Jenkins is represented by the above diagram, which incorporates states, such as build, test, and deploy.

The Jenkins Pipeline is stored in a Jenkinsfile. This permits multiple users to edit and execute the Pipeline process. It also allows you to pause the Pipeline operation and have it continue once the user provides input. If your server has to unexpectedly restart, the Pipeline will be automatically restarted.

## Implementing Jenkins Pipeline

In this tutorial, you will make use of a [Node.js and React application](https://github.com/olawanlejoel/node-js-react-npm-app). When you run your project with `npm start`, a web page that reads "Welcome to React" will be generated. Ensure that you fork this repository, as it will be used in this article. After reading this article, you should have a fundamental grasp of how to use Jenkins Pipeline.

### Make Sure You Have the Prerequisites

Before installing Jenkins, you will need to make sure your computer meets the minimum hardware requirements of 256 MB RAM and 1 GB of hard drive space (however, if you will be running Jenkins as a Docker container, note that 10 GB is the recommended minimum). Furthermore, visit [this page](https://www.jenkins.io/doc/book/scaling/hardware-recommendations) for a complete list of hardware recommendations.

Since Jenkins is built on Java, you'll also need either Java 8 or Java 11 Runtime Environments. For more information, visit the [Java Requirements](https://www.jenkins.io/doc/administration/requirements/java) page.

### Install Jenkins and the Pipeline Plug-in

Once you have completed the prerequisites, you will install Jenkins on your local workstation. This is a tutorial for a Windows installation, but you can refer to the [Jenkins manual](https://www.jenkins.io/doc/book/installing/) for other operating systems, such as macOS and Unix; the steps are almost identical.

To start, you'll need to [download Jenkins](https://jenkins.io/download/), being sure to get the LTS (long-term support) version.

![Download Jenkins]({{site.images}}{{page.slug}}/62VN3d3.png)

Next, you'll run the downloaded WAR file and run it with Java using the command below:

```
java -jar D:\Software_Tools\jenkins.war
```

Ensure you replace `D:\Software_Tools\jenkins.war` with the location of the Jenkins download on your local machine.

Once this is complete, navigate to `localhost:8080`. To get started from here, you'll need to unlock Jenkins. The password can be found in one of two places.

1. You can find it in your terminal:

![Unlock Jenkins password]({{site.images}}{{page.slug}}/xa5nqab.png)

<!-- markdownlint-disable MD029 -->
2. You can, alternatively, find the `initialAdminPassword` file in the directory visible on localhost port 8080.
<!-- markdownlint-enable MD029 -->

![Unlock Jenkins tab]({{site.images}}{{page.slug}}/hI6mYjD.png)

After you've provided your password on the Jenkins login page, you'll be prompted to install the project's required plug-ins. You can either pick **Install suggested plugins** to install the plug-ins from the default list or select **Select plugins to install** to select the specific plug-ins you wish to install.

![Install suggested plugins]({{site.images}}{{page.slug}}/e7c8pYx.png)

For the sake of this tutorial, select **Install suggested plugin**. Installation could take up to one to four minutes, but once complete, the **Create First Admin User** tab will appear:

![Create admin user]({{site.images}}{{page.slug}}/6RqWGxV.png)

Fill out each of the boxes with the account information you would like and then press **Save and Continue**. Once submitted successfully, a tab will appear asking you for URL data.

This URL is used to set the default configuration path for Jenkins. Choosing to keep it as it is may help to prevent any confusion later on. However, if another program is running on port 8080, you can either stop that program from using the port or change the port number.

To change the port, search for the `httpPort` in `<Jenkins-installation-folder >\Jenkins\jenkins.xml` and change it from 8080 to any port number you'd like. Once you've completed this, Jenkins deployment is complete, and your Jenkins configuration is ready.

![Jenkins is ready!]({{site.images}}{{page.slug}}/pO32H9a.png)

> **Note:** Assuming you selected **Install suggested plugins**, then the Pipeline plug-in will have already been installed by default.

However, you'll also want to install one additional plug-in. Go to **Manage Jenkins** and select **Manage Plugins**.

<div class="wide">
![Manage Plugins in Jenkins]({{site.images}}{{page.slug}}/rtZBk5C.png)
</div>

To view all available plug-ins, navigate to **Available**. Then search for **Blue Ocean** and click **Install without restart**. Once this plug-in has been successfully installed, you may proceed.

### Register a Pipeline

Pipelines can be established using [Blue Ocean](https://www.jenkins.io/doc/book/pipeline/getting-started/#through-blue-ocean), [the classic UI](https://www.jenkins.io/doc/book/pipeline/getting-started/#through-the-classic-ui), or [in SCM](https://www.jenkins.io/doc/book/pipeline/getting-started/#defining-a-pipeline-in-scm). For the purposes of this tutorial, you will use SCM, which allows you to manually generate a `Jenkinsfile` that you can commit to your project's source code repository.

To begin, you'll want to log in or return to your Jenkins dashboard and select **New Item** from the top-left menu.

![Jenkins dashboard]({{site.images}}{{page.slug}}/hBOatjE.png)

You will need to enter an **item name** into the field, which will serve as the name for your new Pipeline project.

> **Note:** Jenkins creates directories on the disk using this item name. To avoid issues with scripts that don't properly handle spaces in directory paths, avoid using spaces in item names.

To open the Pipeline setup page, make sure the **General** tab is selected. Then scroll down and choose **Pipeline** before clicking **OK** at the bottom of the page.

<div class="wide">
![Creating a Pipeline]({{site.images}}{{page.slug}}/4IdD6q0.png)
</div>

Next, you can write an optional description if you'd like. Then click the **Pipeline** tab at the top of the page and scroll down to the **Pipeline** section.

In the **Definition** field, choose the **Pipeline script from SCM** option. In the **SCM** field, choose the type of source control system for the repository containing your `Jenkinsfile`. If you're following along with all the specifics for this tutorial, you will choose **Git**.

Ensure you add your **Repository URL** in its field, as well as your branch name in the **branches to build** section. In this particular case, I'll use the default `*/master`. Alternatively, if you're using a local repository, you can input the path on your own system starting with a forward slash (/), such as `/home/cloned-git-repos/my-git-repo.git`.

Finally, make sure you enter the location (and name) of your `Jenkinsfile` in the **Script Path** field before clicking the **Apply and Save** button. This field's default value assumes that your `Jenkinsfile` is named "Jenkinsfile" and is located in the root of the repository.

### Create a Jenkinsfile

A `Jenkinsfile` is a text file that is checked into source control and contains the definition of a Jenkins Pipeline.

After you've successfully applied and saved the Pipeline configurations, you'll build your `Jenkinsfile` in the repository's root directory.

You can do this locally and then push to your repository, but for this guide, I'll generate the file directly on GitHub in the root directory so that Jenkins can easily locate it, just as you set it when you configured your Pipeline.

![Creating Jenkinsfile on GitHub]({{site.images}}{{page.slug}}/ULvtuCb.png)

### Modify the Jenkinsfile to Utilize Stages

A Jenkinsfile can be created as a [scripted](https://www.jenkins.io/doc/book/pipeline/syntax/#scripted-pipeline) or [declarative](https://www.jenkins.io/doc/book/pipeline/syntax/#declarative-pipeline) Pipeline.

The **scripted** Pipeline was the first syntax of Jenkinsfile, allowing you to write the entire Jenkinsfile setup using Groovy script with no predetermined structure. This can be tough to get started with—here's an example:

```
node {
    stage('Build') {
        echo 'Building....'
    }

    //other groovy scripts'
}
```

However, for the sake of this tutorial, I'll utilize the **declarative** Pipeline, which is a recent feature that's easier to get started with because it has a predefined structure, such as below:

```
pipeline {

    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building..'
            }
        }
    }
}
```

`pipeline` is a mandatory attribute in the above code and must be at the top, replacing `node` for scripted pipelines; `agent` `any` instructs Jenkins to use any available executor.

`stages` is also a necessary attribute that contains all the stages you'll utilize for this project; it's where the actual work takes place. There are several stages, but this tutorial will just use three: build, test, and deploy.

Here is what each stage looks like:

```
stage('Build') {
    steps {
        echo 'Building..'
    }
}
```

`steps` provides a set of stages that you want the project to go through, and once that's done, you can test it out by running the build. For example, you can put it into the Jenkinsfile you've just made using this command:

```
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building..'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}
```

Now you can run the build to test whether it's functioning once you push/commit this to your repository. To accomplish this, use the Blue Ocean plug-in you installed earlier. On the left side of your dashboard, click **Open Blue Ocean**.

![Jenkins dashboard]({{site.images}}{{page.slug}}/hBOatjE.png)

Then click the **run** button, which will run the full Jenkinsfile and do all the procedures you instructed for each stage. For the purposes of this guide, it will simply echo the texts we asked it to echo in the `Jenkinsfile`, letting you know it was successful.

<div class="wide">
![Jenkins builds successful]({{site.images}}{{page.slug}}/Le6cAps.png)
</div>

## Conclusion

In this article, you have seen how to leverage Jenkins's deployment phases and Pipeline features to help automate your deployments by constructing a Jenkinsfile, which is significantly easier than completing a manual deployment.

Finally, take a look at [Earthly](https://cloud.earthly.dev/login), a continuous integration tool that may be used to supplement Jenkins's continuous deployment features.

Earthly is a container [build automation](/blog/introducing-earthly-build-automation-for-the-container-era) solution that allows you to run all your builds in containers. Regardless of how Earthly runs—whether on your CI or on your local computer—there is a degree of assurance that the build will run the same way. This allows for faster iteration of the build scripts as well as easier debugging in the event that something goes wrong.

<div class="wide">
![Why Earthly?]({{site.images}}{{page.slug}}/HtxHSQ2.png)/
</div>

Earthly is designed to be used on your development computer as well as in continuous integration. It can be installed on top of existing CI systems (like Jenkins, [Circle CI](https://docs.earthly.dev/examples/circle-integration), or [GitHub Actions](https://docs.earthly.dev/examples/gh-actions-integration)). It serves as a layer between language-specific tools (such as Maven, Gradle, npm, pip, and go build) and the CI build standard. For more information, learn how to [integrate Earthly with Jenkins](https://docs.earthly.dev/ci-integration/vendor-specific-guides/jenkins).

{% include_html cta/bottom-cta.html %}
