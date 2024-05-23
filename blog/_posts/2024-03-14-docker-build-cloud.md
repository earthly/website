---
title: "Saving an Hour a Day with Docker Build Cloud"
toc: false
author: Damaso Sanoja

internal-links:
 - saving an hour a day with docker build cloud
 - save an hour daily with docker build cloud
 - docker build cloud saving an hour daily
 - work efficiently with docker build cloud
excerpt: |
    Docker Build Cloud is a service that speeds up Docker builds by up to 39 times compared to local builds, allowing software developers to save valuable time and enhance productivity. It leverages on-demand cloud resources and team-wide caching to reduce build times and supports building images for different platforms.
categories:
  - Cloud
---
**The article examines Docker Build Cloud's features. Earthly Satellites is an improvement upon this idea which can shrink your image build time. [Check it out](https://cloud.earthly.dev/login).**

As a software developer, you're probably familiar with the slow nature of Docker builds. These local builds can consume anywhere from an hour to several hours of your day. The slow pace of these builds not only delays project schedules but also hinders your ability to iterate quickly, forcing you to find a faster, more streamlined build process.

Enter [Docker Build Cloud](https://www.docker.com/products/build-cloud/), a solution designed to transform how you build Docker images. In this article, you'll learn all about Docker Build Cloud and how it works. By the end of the article, you'll be well-equipped to save valuable time in your development cycle and enhance your overall productivity and efficiency.

## Understanding Docker Build Cloud

Docker Build Cloud is a groundbreaking service aimed at speeding up Docker builds by [up to 39 times](https://www.docker.com/blog/highlights-from-dockercon-2023) compared to conventional local builds.

Build Cloud works similarly to local [BuildKit instances](https://docs.docker.com/build/architecture/#buildx), but with a key distinction in how it executes: when you initiate a build with Build Cloud, the build data is securely transmitted to a remote [builder](https://docs.docker.com/build/builders/) using end-to-end encryption. After the remote builder finishes the build tasks, it sends the output back to your chosen destination, be it your local Docker image store or an online image registry.

<div class="wide">
![Docker Build Cloud profile, courtesy of Damaso Sanoja]({{site.images}}{{page.slug}}/1DJqqY1.png)
</div>

This approach focuses on utilizing on-demand cloud resources. When a build job is received, Docker Build Cloud dynamically allocates cloud-based BuildKit instances to handle the build tasks.

A key feature of Docker Build Cloud's architecture is team-wide caching. This innovative caching solution allows all team members to share cached build layers across projects. That means that when one team member builds an image, the resulting layers are cached on the cloud, and subsequent builds by any team member can reuse these cached layers if the build context hasn't changed. This dramatically reduces build times. Additionally, since Build Cloud natively supports multiplatform builds, this advantage extends to any image type, regardless of the underlying platform.

Another advantage of Docker Build Cloud is that it supports building images for different platforms, such as AMD64 and ARM64, and you don't need multiple native builders or slow emulators. Moreover, builds run on managed infrastructure, ensuring that each build [operates in isolation](https://docs.docker.com/build/cloud/) on a dedicated Amazon EC2 instance with a dedicated EBS volume for the build cache. This setup guarantees that there are no shared processes or data between cloud builders, maintaining strict end-to-end encryption and security.

In essence, Docker Build Cloud is not just a tool but a transformational shift in how Docker image builds are approached. It elevates development productivity by streamlining the build process and leveraging cloud resources to vastly reduce build times. Docker Build Cloud also fosters collaboration, significantly reducing duplicate efforts and ensuring that everyone is working in the latest build environment so that builds are both fast and consistent.

## Implementing Docker Build Cloud

Now that you understand the benefits of Docker Build Cloud, it's time to dive into its implementation. This section shows you how to set up Docker Build Cloud and build images. It also introduces some tips for optimizing your Docker Build Cloud setup so you get the most out of its capabilities.

### Setting Up Docker Build Cloud

To start using Docker Build Cloud, you need to link a payment method to your [Docker account](https://hub.docker.com/signup), even if you plan to only use the free tier.

If you visit [https://build.docker.com/](https://build.docker.com/), you'll see a screen asking which profile you want to use for Build Cloud:

<div class="wide">
![Choosing a profile]({{site.images}}{{page.slug}}/YVd5CWV.png)
</div>

After selecting a profile, you'll be shown the available plans. For this guide, the free **Starter** plan is sufficient, but you should choose the plan that best fits your needs.

After choosing a plan, you'll see a pop-up notification telling you that you need to add a valid credit card for account verification:

<div class="wide">
![Adding a valid credit card to your Docker account]({{site.images}}{{page.slug}}/hKGdjqR.png)
</div>

Once you add your card, you'll be directed to the Docker Build Cloud dashboard:

<div class="wide">
![Docker Build Cloud dashboard]({{site.images}}{{page.slug}}/Ryzkgd6.png)
</div>

From the main dashboard, you can check the remaining build minutes in your plan, upgrade your Docker Build Cloud plan, and create cloud builders. To create a builder, simply click the **Create a Cloud Builder** button. A pop-up window will appear, asking you to give the builder a name:

<div class="wide">
![Creating a new cloud builder]({{site.images}}{{page.slug}}/15NB7Xt.png)
</div>

Name your builder (here, it's named `mastodon`) and click **Create**.

After creation, you'll be directed to the **Cloud Builders** screen, where you can view all your available builders:

<div class="wide">
![Cloud Builders list]({{site.images}}{{page.slug}}/CVUhKL8.png)
</div>

Select the builder you just created, and instructions for installing a cloud [build driver](https://docs.docker.com/build/drivers/) on your local machine and integrating it with CI/CD processes will appear:

<div class="wide">
![Docker Build Cloud setup instructions]({{site.images}}{{page.slug}}/H6VRqTX.png)
</div>

Begin by executing the first two steps. Follow the on-screen commands, which are already populated with your Docker organization and builder name for ease of use. After completing these steps, you can use Docker Build Cloud from your CLI.

Alternatively, because Docker Desktop includes Build Cloud as a preinstalled feature, when you log in to Docker Desktop with your user or organization credentials, you can directly access Build Cloud from the **Builders** tab.

Then, since you've created a cloud builder, you can find it under the **Available builders** section. You'll see instructions for connecting the builder via the CLI, but you can skip this step since you've already completed it. Simply click the **Connect to builder** button to start using Build Cloud through Docker Desktop:

<div class="wide">
![Accessing Build Cloud via the Builders tab in Docker Desktop]({{site.images}}{{page.slug}}/VJNRxL9.png)
</div>

Once connected, you can use the menu to use the builder, stop it, or disconnect from it:

<div class="wide">
![Builder menu options]({{site.images}}{{page.slug}}/3bH6tap.png)
</div>

The final step in the setup process is to integrate Build Cloud with your existing CI/CD pipelines and tools. Choosing your builder on [https://build.docker.com/](https://build.docker.com/) only provides detailed instructions for [GitHub Actions](https://github.com/features/actions) and [CircleCI](https://circleci.com/), but [additional integration guidance is available](https://docs.docker.com/build/cloud/ci/) for [GitLab](https://about.gitlab.com/), [Buildkite](https://buildkite.com/), and [Jenkins](https://www.jenkins.io/).

Now that you have everything you need to start using Build Cloud from the CLI or from Docker Desktop, it's time to start leveraging its power by building some images.

### Building Docker Images with Docker Build Cloud

This section compares Build Cloud with the traditional `docker build` command that you're probably very familiar with. This demonstration uses a basic Flask application:

~~~{.python caption=""}
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'
~~~

This app is written in Python and creates a basic web application that responds with "Hello, World!" when accessed. To create the Docker image for this app, you can use the following Dockerfile:

~~~{.Dockerfile caption="Dockerfile"}
FROM python:3.13.0a3-bookworm
WORKDIR /app
RUN pip install flask==2.3
COPY . /app
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
~~~

Selecting the base image `python:3.13.0a3-bookworm` over a lighter alternative, such as one based on Alpine, is a deliberate decision to increase the workload for the Docker build process. Once you save both files, you can start building Docker images.

#### Building a Local Image

Building a local image establishes a baseline that allows you to compare your traditional workflow with Docker Build Cloud. For that reason, run the following command to build the image without using Build Cloud:

~~~{.bash caption=">_"}
docker buildx build -t <YOUR_DOCKER_USERNAME>/sample-flask-app:local .
~~~

This command builds a Docker image from the Dockerfile and tags it as `local` to indicate that it's a local version of the `sample-flask-app` image under the `<YOUR_DOCKER_USERNAME>` repository.

#### Building an Image Using Docker Build Cloud

Now, switch to Docker Build Cloud to [build the same image](https://docs.docker.com/build/cloud/usage/) using the following code:

~~~{.bash caption=">_"}

docker buildx build --builder cloud-<YOUR_DOCKER_USERNAME>-<YOUR_BUILDER_NAME> --tag <YOUR_DOCKER_USERNAME>/sample-flask:cloud .
~~~

This command initiates the build and is essentially the same as the previous one. The main difference is where and how the build is processed, which is determined with the `--builder` flag.

The only reason you don't specify the `--builder` flag when building the image locally is because you're using the default builder. If you want to set Docker Build Cloud as the default builder (and save you from typing `--builder` every time), you can use the following command:

~~~{.bash caption=">_"}
docker buildx use cloud-<ORG>-<BUILDER_NAME> --global
~~~

Keep in mind that if you do so, each time you build an image, your build will be processed on the cloud. This might impact your billing.

#### Comparing Your Results

<div class="wide">
![Docker Build Cloud vs. local build]({{site.images}}{{page.slug}}/nGmeBWS.png)
</div>

This screenshot shows your results, in which the container image took 5.3 seconds to build using the default (local) BuildKit instance and 1.6 seconds using Docker Build Cloud. In other words, the image was built 3.3 times faster.

Before drawing conclusions, remember that your results may vary depending on your hardware and/or internet connection. Regardless, for such a simple image, the results are promising, especially considering that no optimization has been implemented yet.

### Optimizing Docker Build Cloud Performance

As the complexity of Docker images increases, they require more computing resources to build. That's why adopting best practices and effective strategies to [enhance Docker build performance](https://docs.docker.com/build/cloud/optimization/) is so important.

Consider using `.dockerignore` files to exclude unnecessary files from your build context, choosing slim base images to reduce final image size, leveraging multistage builds to minimize redundancy and speed up builds, and fetching files directly in your build from remote locations rather than including them in your build context.

If the results of Build Cloud do not meet your expectations, consider [upgrading your plan](https://www.docker.com/products/build-cloud/#pricing), as doing so gives you access to instances with more CPU power, RAM, cache storage, and parallel builds.

That said, none of these optimizations address the main limitation of Docker Build Cloud, which is that it cannot be leveraged to build artifacts beyond Dockerfiles.

[Earthly](https://earthly.dev/) is a CI/CD framework that expands Docker's capabilities and makes remote builds super simple. It offers [Earthly satellites](https://docs.earthly.dev/earthly-cloud/satellites), which provide an innovative approach to build optimization.

Earthly satellites are remote runner instances that facilitate remote caching, allow for a simplified syntax in build scripts, enable parallel execution of build stages, and manage build artifacts more effectively than Docker alone. A noteworthy application of this approach is seen in the [case of ExpressVPN](https://earthly.dev/blog/incremental-rust-builds/), which dramatically cut CI build times by utilizing Earthly's caching features and remote runners. This example highlights the potential for significant efficiency gains in CI processes through thoughtful optimization and the adoption of advanced building tools like Earthly.

## Conclusion

In this article, you learned how Docker Build Cloud—with its cloud-based infrastructure, native multiplatform support, and team-wide caching—can help you achieve significantly lower build times. However, you also learned that Docker Build Cloud cannot be used to build artifacts beyond Dockerfiles. That's where Earthly satellites can help.

Earthly satellites can help you unlock the full potential of your CI/CD pipeline with remote runner instances designed for efficiency and scalability. Start optimizing your build processes today and experience groundbreaking speed and reliability in your deployments.

{% include_html cta/bottom-cta.html %}
