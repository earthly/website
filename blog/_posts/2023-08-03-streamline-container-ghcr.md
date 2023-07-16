---
title: "How to Streamline Your Container Workflow with GitHub Container Registry"
categories:
  - Tutorials
toc: true
author: Mercy Bassey
editor: Ubaydah Abdulwasiu

internal-links:
 - just an example
---
<!--sgpt-->**We're [Earthly](https://earthly.dev/). We simplify and speed up software building with containerization. Earthly is a powerful tool that enhances your CI/CD workflows. [Check it out](/).**

**We're [Earthly](https://earthly.dev/). We make building software simpler and, therefore, faster by using containerization. If you're interested in a different approach to building and packaging software, then [check us out](/).**

If you have been using GitHub lately, you might have encountered the GitHub Container Registry. In this era of containerization, it has undeniably become a cornerstone of modern application development and deployment. Containers have transformed how developers package their applications and dependencies, ensuring consistency and portability across different environments.

To further enhance the container workflow, GitHub introduced its registry - [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry) (GHCR). This powerful tool integrates seamlessly with your GitHub repositories, providing a secure and efficient way to store, manage, and distribute container images.

Conversely, this article will explore the capabilities of the GitHub Container Registry and dive into best practices and integration strategies that can revolutionize a container workflow. By the end, you'll have the knowledge and insights to effectively leverage the GitHub Container Registry, taking your container workflow to new heights.

## Prerequisites

To follow along in this tutorial, you are required to have the following:

- A [GitHub account](https://docs.github.com/en/get-started/signing-up-for-github/signing-up-for-a-new-github-account) and a [GitHub repository](https://docs.github.com/en/get-started/quickstart/create-a-repo) already created -  this tutorial uses a GitHub repository called *hello-world-express-app*.
- Familarity with [Docker](https://docs.docker.com/get-started/) and Docker [Engine](https://docs.docker.com/engine/install/) or [Desktop](https://www.docker.com/) installed on your machine.
- A Kubernetes cluster that is already up and running.

## What is the GitHub Container Registry?

The GitHub Container Registry is a feature provided by GitHub that allows you to store, manage, and distribute container images directly within your GitHub repository. It offers seamless integration between source code and container images, streamlining the development and deployment processes. Using the GitHub Container Registry, you can leverage the power of containerization while harnessing the collaborative and version control capabilities of GitHub.
Other than the fact that it acts as a central repository for hosting and managing container images, it does the following:

- Eliminates the need for separate container registry services, providing a unified platform for source code and container artifacts.
- Provide simplicity and familiarity in the sense that, as a developer that is already using GitHub for version control and collaboration, adopting the GitHub Container Registry feels natural as it leverages the same familiar interface and workflows, making it easy to manage both code and container images within the same environment.
- Integrates well with GitHub repositories and workflows, so you can publish container images directly from your CI/CD pipelines, ensuring that the entire development lifecycle, from code changes to image deployments, can be managed within GitHub.
- Provides a secure and efficient way to store and manage your container images alongside your code repositories. This means you can push, pull, and delete container images directly from your repository, maintaining a single source of truth for your application artifacts.
- Integrate well with your CI/CD pipelines, like [GitHub Actions](https://docs.github.com/en/actions) in this case, thereby enabling automatic publishing and deployment of container images where you can build, test, and package your application code and then seamlessly push the resulting container images to the registry for further deployment.
- Provide robust access control features that allow you to manage permissions, ensuring that only authorized collaborators or teams can access and use your container images. It also allows you to maintain security and control over your software artifacts. And so much more.

## Configuring Access with GitHub Container Registry

Now that you understand the GitHub Container Registry and have seen how it seamlessly integrates with GitHub repositories and workflows, you are ready to take the next step and configure access to this powerful tool. By configuring access, you can fully leverage the capabilities of the GitHub Container Registry and start managing your container images effectively.

In this section, you will set up a personal access token, the authentication mechanism for accessing the GitHub Container Registry. This token ensures secure and controlled access to your container images, allowing you to push, pull, and manage them within your repositories.

You must create a personal access token on your GitHub account to achieve this. The personal access token is a secure authentication method to access the container registry.

To create a personal access token, follow these steps:

1. Navigate to your GitHub account settings.
2. From the left panel, go to the *Developer settings* section and select *Personal access tokens*.
3. In the *Tokens (classic)* drop-down menu, click on *Generate new token (classic)* to create a new token.
    
    ![Generating a new token on GitHub](https://imgur.com/q75SJBo.png)
    
  >  Note: If your account configures two-factor authentication, you’ll be prompted to enter your GitHub password to proceed.
    
4. Provide a descriptive name for the token and select the necessary scopes for registry access. For this tutorial, select the **`write:packages`** , **`delete:packages`**, and **`workflow`** scopes to enable registry-related actions.
    
    ![Configuring token scopes (write and delete packages and workflow)](https://imgur.com/e3CKQ1r.png)
    
    
5. Scroll down to the bottom of the page and click *Generate token* to create the token.
6. Once the token is generated, copy it and securely store it in a safe location for future use.
    
    ![Copying newly generated token](https://imgur.com/qbwCHjC.png)
    
    
Once you have your personal access token, you can authenticate with the GitHub Container Registry from your local machine. This authentication step ensures that you have permission to interact with the container registry, such as pushing and pulling container images.


> To set up the demo application for this tutorial, clone the repository `hello-world-express-app` from the GitHub account `mercybassey` using the command `git clone git@github.com:mercybassey/hello-world-express-app.git`. Open the cloned repository in your preferred code editor, update the remote origin to your repository using the following commands, and proceed with the tutorial using this application as an example.

```bash
git remote remove origin
git remote add origin <your_repository_url> 
 ```


You can authenticate your local machine with the GitHub Container Registry with the personal access token. Using the Docker CLI, execute the following command:

```bash
docker login ghcr.io -u <GITHUB_USERNAME> -p <PERSONAL_ACCESS_TOKEN>
```

Replace `GITHUB_USERNAME` with your GitHub username and `PERSONAL_ACCESS_TOKEN` with the personal access token you generated. This command authenticates your Docker CLI with the GitHub Container Registry, allowing you to interact seamlessly. Once you are logged in, you are expected to have the following output:

![Logging in to GHCR from local machine](https://imgur.com/lTWu1Y3.png)

This shows you are now authenticated with the GitHub Container Registry and ready to interact.

## Deploying Docker Images to GitHub Container Registry

Now that you have configured access to the GitHub Container Registry and established a connection between your local machine and the registry, it's time to explore how to deploy Docker images to the registry.

Deploying Docker images to the GitHub Container Registry follows a similar process to the traditional way of building and deploying Docker images. However, there are a few key steps specific to the GitHub Container Registry that you need to consider.

To begin, execute the following command to build the docker image for the express app:

```bash
docker build -t ghcr.io/GITHUB_USERNAME/IMAGE_NAME:TAG .
```

Here,   `GITHUB_USERNAME` is your GitHub username,  `IMAGE_NAME` is the desired name for your image; this tutorial uses the image name `hello-world`, and `TAG` represents the version or tag you want to assign to the image, which should be the latest in this case.

This should take some time, but once the build is finished, you can confirm if it is listed among the Docker images you have on your machine using the following command:

```bash
docker images
```

![Viewing docker images available locally](https://imgur.com/ncnzDOV.png)

Before pushing the Docker image to the GitHub container registry, you must confirm if this image works as expected. One way to achieve this is to run the image locally; execute the following command:

```bash
docker run -p 3000:3000 ghcr.io/GITHUB_USERNAME/IMAGE_NAME
```

You are expected to have the following output:

![Running the express-app docker image locally](https://imgur.com/di96ksX.png)

Now open up the following web address `http://localhost/3000](http://localhost/3000` with your preferred web browser to view the express app; if you see the below output, it is confirmed that the application works as expected. You can now push it to the GitHub container registry:

![Viewing the express app over the browser](https://imgur.com/tNaHCu7.png)

To push this image up to the GitHub container registry, execute the following command:

```bash
docker push ghcr.io/USERNAME/REPOSITORY/IMAGE_NAME:TAG
```

You also need to wait for the image to be pushed to the GitHub container registry; once this is done, head over to your GitHub account and click on the packages tab as shown below to view the image:

![Viewing docker image on GitHub](https://imgur.com/9w7uygZ.png)

The image above shows that the Docker image was pushed successfully to the GitHub container registry.


> When you want to deploy an already built docker image to the GitHub container registry, be sure to tag the image appropriately using the following command `docker tag <image-name> [ghcr.io/USERNAME/REPOSITORY/IMAGE_NAME:TAG](http://ghcr.io/USERNAME/REPOSITORY/IMAGE_NAME:TAG)` otherwise, you won’t be able to push the image to the GitHub container registry.


## Integrating GitHub Container Registry with GitHub Actions

Integrating the GitHub Container Registry with GitHub Actions opens up possibilities for automating container workflows. You can streamline your development and deployment processes by combining the power of GitHub Actions CI/CD capabilities with the seamless container image management provided by GitHub Container Registry. This section will explore how to leverage GitHub Actions to build, test, and publish container images to the GitHub Container Registry, enabling automated workflows that ensure your applications are always up-to-date and readily deployable.

The first thing to do is create a `.github/workflows` directory in the root directory of your project. Inside this directory, create a YAML file named `ghcr.yaml` (or any preferred name) to define your GitHub Actions workflow. This file will contain the necessary configuration to build, test, and deploy your containerized application using the GitHub Container Registry.

In this file, add the following code snippets:

```yaml
# .github/workflows/gchr.yaml 

name: Build and Push to GHCR

on:
  push:
    branches:
      - main 

jobs:
  build_and_push:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Build and Push the Image to GHCR
        run: |
          docker login ghcr.io -u <YOUR_GITHUB_USERNAME> -p ${{ secrets.PERSONAL_ACCESS_TOKEN}}
          docker build -t ghcr.io/<YOUR_GITHUB_USERNAME>/hello-world:latest .
          docker push ghcr.io/<YOUR_GITHUB_USERNAME>/hello-world:latest
```

The code snippet above sets up a workflow named `Build and Push to GHCR` triggered by push events on the `main` branch (you can specify your branch if needed). The workflow specifies a single job named `build_and_push` that runs on an Ubuntu environment and consists of the following steps:

1. **Checkout code**: This step uses the `actions/checkout@v3` action to fetch the source code of your repository.
2. **Build and Push the Image to GHCR**: This step performs the actual build and push process. It starts by doing the following:
    1. logging into the GitHub Container Registry using your specified username (`<GITHUB_USERNAME>`) and a personal access token stored in the repository secrets (accessed via `${{ secrets.PERSONAL_ACCESS_TOKEN }}`). 
    2. Builds the Docker image using the current directory (`.`**) and tags it as `ghcr.io/<GITHUB_USERNAME>/hello-world:latest`. 
    3. Pushes the built image to the GitHub container registry.

At the moment, this workflow will be triggered automatically when you make a commit to your remote repository. However, before proceeding, you must add your personal access token as a secret on your GitHub account. By following the steps below, you can securely store the token and make it accessible to the workflow:

1. Navigate to the main page of the repository housing your express app.
2. Click on the Settings tab on the right side of the repository navigation bar.
3. In the left sidebar, click **Secrets and Variables** and  select the *Action* option from the drop-down menu.
4. Click on the **New repository secret** button.
5. Enter a name for your secret, such as *PERSONAL_ACCESS_TOKEN*, and paste your access token into the `Secret` field.
6. Click the **Add secret** button to save the secret.

![Viewing repository secrets](https://imgur.com/mI3e4D4.png)

Now to trigger the GitHub actions pipeline, edit the `index.js` file in your root directory to say `Hello GCHR` instead of `Hello World` as shown below:

```javascript
# index.js
...

app.get('/', (req, res) => {
  res.send('Hello GCHR');
});

...
```

Now, commit this change to your repository to trigger the pipeline by executing the following Git commands sequentially:

```bash
git add .
git commit -m "Configured GitHub Actions"
git push origin main
```

After a successful push, head to your remote repository and click the *Actions* tab to view your pipeline. The image below shows the pipeline has started and is in progress:

![Viewing GitHub actions workflow in progress](https://imgur.com/iRVQ8nU.png)

After a while, you should have the following image showing that the pipeline has completely succeeded:

![Viewing GitHub actions workflow in a complete state](https://imgur.com/fHr2vRX.png)

Now head over to your GitHub profile page; click on the **packages** tab and click on your package:

![Viewing GitHub package](https://imgur.com/fHr2vRX.png)


Once you click on it, you should see a new page containing other details and actions for your image. And from the output below, you can confirm that the image was recently updated:

![Confirming recent update of the GitHub package](https://imgur.com/aFIQDIU.png)


Now that GitHub actions are configured, once you commit any change in your code and push it to your GitHub repository, the docker image for your application rebuilds and gets updated in the GitHub container registry.

## Integrating GitHub Container Registry with Kubernetes

You can take your experience with the GitHub Container Registry further by seamlessly integrating it with Kubernetes. This integration allows you to leverage the power of the GitHub Container Registry as the image registry for your Kubernetes deployments. This streamlines the deployment process and enhances your containerized application workflow. This section will walk you through the steps to integrate the GitHub Container Registry with Kubernetes, enabling you to easily deploy your applications using container images stored in your GitHub repository.

However, there is something to note; the visibility of container images in the GitHub Container Registry is tied to the visibility settings of the corresponding GitHub repository. If a GitHub repository is public, any container images associated with it will also be public. If the repository is private, the container images will also be private. In a case where the container image isn’t tied to any repository yet (in our case), it is private by default. To grant Kubernetes access to the container image, you must authorize it accordingly.  

To begin, generate a Kubernetes Secret with credentials to authenticate with the GitHub Container Registry. We can do this by running the command:

```bash
kubectl create secret docker-registry k8s-ghcr --docker-server=https://ghcr.io --docker-username=<YOUR_GITHUB_USERNAME> --docker-password=<YOUR_GITHUB_PERSONAL_ACCESS-TOKEN> --docker-email=<YOUR_GITHUB_EMAIL>
```
To view the secret created:
```bash
kubectl get secret
```

The commands above will create a Docker registry secret in Kubernetes. Here’s what each command stands for:

- `kubectl create secret docker-registry k8s-ghcr` shows that the secret to be created is a [docker-registry](https://jamesdefabia.github.io/docs/user-guide/kubectl/kubectl_create_secret_docker-registry/) secret named `k8s-ghcr`.
- `--docker-server=https://ghcr.io` specifies the Docker registry server as `https://ghcr.io`, the GitHub Container Registry (GHCR).
- `--docker-username=<YOUR_GITHUB_USERNAME>` sets the Docker registry username as your GitHub username.
- `--docker-password=<YOUR_GITHUB_PERSONAL_ACCESS-TOKEN>` sets the Docker registry password as your GitHub Personal Access Token. This token is used for authentication and authorization with the GHCR.
- `--docker-email=<YOUR_GITHUB_EMAIL>` sets the email associated with the Docker registry account as your GitHub email.

Once the secret is created, you should have the following output:

![Creating and viewing secret *k8s-ghcr*](https://imgur.com/dwYNV7X.png)


Now, create a file `express-app.yaml` and paste in the following configuration settings:

```yaml
# express-app.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-world-express-app
  labels:
    app: hello-world-express-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: hello-world-express-app
  template:
    metadata:
      labels:
        app: hello-world-express-app
    spec:
      containers:
      - name: hello-world
        image: ghcr.io/<YOUR_GITHUB_USERNAME>/<IMAGE_NAME>:TAG
        ports:
        - containerPort: 3000
      imagePullSecrets:
      - name: k8s-ghcr
```

The code snippet above will set up a ' hello-world-express-app' deployment with three replicas and expose it on port `3000` within the Kubernetes cluster. It will use the package or container from your GitHub Container Registry as the container image for the deployment and use the `k8s-ghcr` secret created earlier to authenticate access to the private container image.

To create and view this deployment, execute the following commands sequentially:

```bash
kubectl apply -f express-app.yaml
kubectl get deployments
kubectl get pods
```

You are expected to have the following output:

![Creating and viewing *hello-world-express-app*  deployments and pods](https://imgur.com/PCzVhBa.png)

Create a file `svc.yaml` and paste in the following code to expose the deployment:

```yaml
# svc.yaml
apiVersion: v1
kind: Service
metadata:
  name: hello-world-service
spec:
  selector:
    app: hello-world-express-app
  ports:
    - protocol: TCP
      port: 3000
      targetPort: 3000
```

The code above will create a service of type `ClusterIP` named `hello-world-service` for the `hello-world-express-app` deployment. It will listen on port `3000` and forward traffic to the Kubernetes pods port `3000`.

Execute the following commands sequentially to create, view, and test this service:

```bash
# Creates the service
kubectl apply -f svc.yaml

# view the service
kubectl get service

# Creates a pod named "curl" using the "radial/busyboxplus:curl" image to allow interactive shell access to resources.
kubectl run curl --image=radial/busyboxplus:curl -i --tty

# Sends an HTTP request to the specified <cluster-ip> and port 3000 using the curl container image 
curl http:<cluster-ip>:3000
```

If you have the following output, then you have successfully pulled a private image from the GitHub Container Registry with Kubernetes:

![Creating and viewing service *hello-world-service*](https://imgur.com/aiOtIWZ.png)


## Conclusion

You can now agree that integrating the GitHub Container Registry into your container workflow can streamline your development and deployment processes. By leveraging the power of GitHub Actions and Kubernetes, you can automate your workflows and ensure that your containerized applications are always up-to-date and readily deployable. You have seen how to:
- Push docker images to the GitHub container registry.
- Use GitHub actions for automatic deployment to GHCR. 
- Pull and use docker images from GHCR in a Kubernetes environment. 
With this newfound knowledge, you can use GCHR to its full potential and maximize the potential of your container-based workflows.


## Outside Article Checklist

- [ ] Create header image in Canva
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
  - Would any images look better `wide` or without the `figcaption`?
- [ ] Run mark down linter (`lint`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `link-opp` and find 1-5 places to incorporate links
- [ ] Add Earthly `CTA` at bottom `{% include_html cta/bottom-cta.html %}`
