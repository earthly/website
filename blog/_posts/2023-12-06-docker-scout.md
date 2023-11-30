---
title: "What Is Docker Scout and How to Use It"
categories:
  - Tutorials
toc: true
author: Damaso Sanoja

internal-links:
 - just an example
last_modified_at: 2023-09-08
---

[Docker Scout](https://docs.docker.com/scout/quickstart/) is an innovative tool that simplifies securing Docker images by analyzing their contents and generating a detailed report of any vulnerabilities detected during the process. Docker Scout's key features include inspecting for [common vulnerabilities and exposures](https://www.redhat.com/en/topics/security/what-is-cve) (CVE), providing security recommendations, and seamless integration with continuous integration, continuous delivery (CI/CD) workflows, helping you discover and remediate vulnerabilities during development.

In this tutorial, you'll learn all about Docker Scout, including how to use the Docker Scout CLI and UI and how to seamlessly integrate it into your CI/CD workflows.

## Docker Scout vs. Docker Scan

If you're familiar with [Docker Scan](https://github.com/docker/scan-cli-plugin), consider Docker Scout as an upgrade that offers a more comprehensive approach to Docker image analysis. Docker Scout goes deeper into the contents of the images, generating an exhaustive report on the packages and their possible vulnerabilities.

Additionally, unlike Docker Scan, Docker Scout is integrated into Docker Desktop. This means you can view and pull images from Artifactory repositories directly through the user interface and review vulnerability information and remediation recommendations.

## When Should You Consider Using Docker Scout?

Adding a new tool to the development workflow takes time and effort, so it makes sense for your team to evaluate whether it's worth it. The following are some scenarios where your company should consider using Docker Scout:

* **Compliance with security regulations:** Companies that provide services to US government agencies should use Docker Scout since they need to demonstrate [FedRAMP](https://www.fedramp.gov) compliance, which [expressly requires scanning container images](https://www.fedramp.gov/assets/resources/documents/Vulnerability_Scanning_Requirements_for_Containers.pdf) before deploying them to production.
* **Malicious code execution:** Images can contain untrusted or malicious code. Without scanning, this code could be executed unknowingly, leading to potential system compromise, data corruption, and lateral movement attacks that can [compromise the integrity of your entire development pipeline](https://www.businessinsider.com/solarwinds-hack-explained-government-agencies-cyber-security-2020-12).
* **Unpatched vulnerabilities:** Without scanning for CVE, [developers may use outdated images with known vulnerabilities](https://snyk.io/learn/docker-security/top-5-vulnerabilities/). Hackers can exploit these, leading to unauthorized access, a data breach, or service disruption to your company's customers, leading to loss of reputation and money.

## Docker Scout in Action

The best way to evaluate a tool is to see it in action, which is what you'll do here. Go ahead and make sure you [install the most recent version of Docker Desktop](https://www.docker.com/products/docker-desktop/). This tutorial uses Docker Desktop v4.24.2 for Apple silicon.

Docker Desktop provides a convenient UI for Docker Scout and the corresponding command line interface, `scout-cli`. Alternatively, you can install just `scout-cli` on a headless system by following [these instructions](https://github.com/docker/scout-cli).

### The docker scout quickview Command

To start experimenting with Docker Scout, launch Docker Desktop, fork, and then clone [this GitHub repository](https://github.com/docker/scout-demo-service.git) to your local machine.

The repository consists of an example project written in Node.js that contains known vulnerabilities. Navigate to the directory and build the application image using `docker build`, replacing `<DOCKER_HUB_ORG>` with your Docker Hub username or organization:

```shell
cd scout-demo-service
docker build -t <DOCKER_HUB_ORG>/scout-demo:v1 .
```

The output should look like this:

```shell
...
What's Next?
  View a summary of image vulnerabilities and recommendations → docker scout quickview
```

Follow the suggestion in the last line and run the [`docker scout quickview`](https://github.com/docker/scout-cli/blob/main/docs/scout_quickview.md) command:

![docker scout quickview output](https://i.imgur.com/wAeIhZF.png)

You can also view this information using Docker Desktop:

![docker scout quickview output on Docker Desktop](https://i.imgur.com/0kT5gL1.png)

As the name suggests, the `docker scout quickview` command shows a high-level overview of the container image and is a good starting point to figure out if the image has vulnerabilities. In this case, some have been found, and you can dig deeper by running a CVE scan.

### The docker scout cves Command

Basically, a CVE scan analyzes a software artifact for known vulnerabilities. [`docker scout cves`](https://github.com/docker/scout-cli/blob/main/docs/scout_cves.md) is the CLI command that performs this scan:

```shell
docker scout cves local://<DOCKER_HUB_ORG>/scout-demo:v1
```

This time, the output offers more information, including CVE IDs and a [CVSS](https://nvd.nist.gov/vuln-metrics/cvss) score and CVSS vector for each vulnerability. The following is only a partial output:

![docker scout cves output](https://i.imgur.com/FrN1qD1.png)

A convenient way to manage so much information or even filter it is through Docker Desktop:

![docker scout cves output on Docker Desktop](https://i.imgur.com/ILCtj0Q.png)

From there, you have different views, such as images, packages, and vulnerabilities, that help you analyze all the data in the way that you prefer. However, analyzing the vulnerabilities is only one part of the equation. Since the real goal is to remediate the vulnerabilities, this is where Docker Scout recommendations are helpful.

### The docker scout recommendations Command

One of the key features of Docker Scout is the recommendations it provides to fix every CVE, ultimately saving you time. All you have to do is run the command [`docker scout recommendations`](https://github.com/docker/scout-cli/blob/main/docs/scout_recommendations.md), like this:

```shell
docker scout recommendations local://<DOCKER_HUB_ORG>/scout-demo:v1
```

The following is a partial output that shows recommendations for one of the CVEs:

![docker scout recommendations output](https://i.imgur.com/ERzW99o.png)

Alternatively, you can use the `--only-refresh` or `--only-update` flags to show only base image refresh or update recommendations.

Similar to the previous commands, you can also review the recommendations using Docker Desktop. To do this, simply select **Recommendations for base image**:

![Docker Scout recommendations for base image](https://i.imgur.com/W1e0spJ.png)

A pop-up window will show you a list of recommendations to refresh or update the base image:

![Refresh or update the base image](https://i.imgur.com/vD4Zn4J.png)

You can navigate using the tabs and review each of the recommendations individually:

![Review each Docker Scout recommendation individually](https://i.imgur.com/IHEVTDC.png)

Then, you can apply the suggested changes and remediate each vulnerability.

For instance, you could edit the `Dockerfile` and update the Alpine image to version 3.17, as suggested by Docker Scout. Then, you'll need to rebuild the image:

```shell
docker build -t <DOCKER_HUB_ORG>/scout-demo:v2 .
```

Once ready, you can scan the new version for vulnerabilities in Docker Desktop:

![Scan the new version for vulnerabilities](https://i.imgur.com/FK7L3TX.png)

No further base image issues have been found.

As you can see, Docker Scout provides valuable insights that streamline the process of remediating vulnerabilities in container images. However, while it's great to have a CLI and an intuitive UI to perform these tasks, it isn't efficient to manually scan each container for vulnerabilities. That's why it's recommended that you integrate Docker Scout into your CI/CD pipeline.

### Integrating Docker Scout into CI/CD Pipelines

The Docker Scout documentation explains in detail how to [automate container image scans](https://docs.docker.com/scout/integrations/#continuous-integration) using popular CI integration platforms such as GitHub Actions, GitLab, Microsoft Azure DevOps Pipelines, CircleCI, and Jenkins.

For instance, if you want to [integrate Docker Scout with GitHub Actions](https://docs.docker.com/scout/integrations/ci/gha/), use the same example repository from before and navigate to the `.github/workflows` directory to create the GitHub action:

```shell
cd .github/workflows
```

Next, create a YAML file with a GitHub action for Docker Scout. In this example, it will be called `github-actions-demo.yml`, but you can use whatever name you prefer:

```shell
nano github-actions-demo.yml
```

At this point, you can create an action with the steps you need. In the following example, the GitHub action will trigger automatically when you create a pull request (PR). It builds and scans Docker images for vulnerabilities and then publishes the results to GitHub:

```yaml
name: Docker

on:
  push:
    tags: [ "*" ]
    branches:
      - 'main'
  pull_request:
    branches: [ "**" ]
    
env:
  # Use docker.io for Docker Hub if empty
  REGISTRY: docker.io
  IMAGE_NAME: ${{ github.repository }}
  SHA: ${{ github.event.pull_request.head.sha || github.event.after }}
  # Use `latest` as the tag to compare to if empty, assuming that it's already pushed
  COMPARE_TAG: latest

jobs:
  build:

    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
      pull-requests: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
        with:
          ref: ${{ env.SHA }}
          
      - name: Setup Docker buildx
        uses: docker/setup-buildx-action@v2.5.0
        with:
          driver-opts: |
            image=moby/buildkit:v0.10.6

      # Login against a Docker registry except on PR
      # https://github.com/docker/login-action
      - name: Log into registry ${{ env.REGISTRY }}
        uses: docker/login-action@v2.1.0
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ secrets.DOCKER_USER }}
          password: ${{ secrets.DOCKER_PAT }}

      # Extract metadata (tags, labels) for Docker
      # https://github.com/docker/metadata-action
      - name: Extract Docker metadata
        id: meta
        uses: docker/metadata-action@v4.4.0
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          labels: |
            org.opencontainers.image.revision=${{ env.SHA }}
          tags: |
            type=edge,branch=$repo.default_branch
            type=semver,pattern=v{{version}}
            type=sha,prefix=,suffix=,format=short
      
      # Build and push Docker image with Buildx (don't push on PR)
      # https://github.com/docker/build-push-action
      - name: Build and push Docker image
        id: build-and-push
        uses: docker/build-push-action@v4.0.0
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Analyze for critical and high CVEs
        id: docker-scout-cves
        if: ${{ github.event_name != 'pull_request_target' }}
        uses: docker/scout-action@v1
        with:
          command: cves, recommendations
          image: ${{ steps.meta.outputs.tags }}
          sarif-file: sarif.output.json
          summary: true
      
      - name: Upload SARIF result
        id: upload-sarif
        if: ${{ github.event_name != 'pull_request_target' }}
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: sarif.output.json
```

In this code, some preliminary tasks are performed to pave the way for vulnerability scanning with Docker Scout, including checking the repository code, configuring Docker `buildx`, authenticating to the Docker registry, pulling metadata, and building/pushing the Docker image. Then, from line 76 onwards, you'll notice two actions related to Docker Scout:

1. `Analyze for critical and high CVEs` achieves its goal by using `command: cves, recommendations`, equivalent to the commands `docker scout cves` and `docker scout recommendations` you ran in the CLI.
2. `Upload SARIF result` is responsible for uploading the results to GitHub for easier analysis.

Once the GitHub action is ready, go to your GitHub repository, click the **Settings** tab, and then go to **Secrets and variables > Actions** in the sidebar. There, create two secrets and one environmental variable:

* The `DOCKER_USER` secret corresponds to your Docker Hub username.
* The `DOCKER_PAT` secret corresponds to your Docker Hub [personal access token](https://docs.docker.com/security/for-developers/access-tokens/).
* The `REGISTRY` variable corresponds to your Docker Hub namespace.

Now that your local and remote repositories are ready, you can create a new branch, make dummy changes, and push them to GitHub:

```shell
git checkout -b docker-scout-test
git add .
git commit -m "testing Docker Scout"
git push --set-upstream origin docker-scout-test
```

Then, [create a new PR on GitHub](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request#) that will trigger the GitHub action:

![PR on GitHub](https://i.imgur.com/kUaAoDW.png)

The scan results will be published once the process is completed. The following screenshot was taken after changing the Alpine image back to an unsafe version:

![Unsafe version of Alpine image](https://i.imgur.com/i1Nr5cZ.png)

As you can see, it shows the same vulnerabilities as Docker Desktop: 2 critical, 16 high, 7 medium, and 1 unspecified:

![Vulnerabilities](https://i.imgur.com/48vncnS.png)

To learn more about integrating Docker Scout with GitHub Actions, check out the [`scout-action` repository](https://github.com/docker/scout-action).

## Conclusion

In this tutorial, you learned about what Docker Scout is and its importance in identifying and remedying vulnerabilities. You also learned about its usage and how to integrate it into your favorite CI/CD pipeline. With this knowledge, you're better equipped to optimize your development environment, bolster your security posture, and streamline your workflow.

## Outside Article Checklist

- [ ] Create header image in Canva
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
  - Would any images look better `wide` or without the `figcaption`?
- [ ] Run mark down linter (`lint`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `link-opp` and find 1-5 places to incorporate links
- [ ] Add Earthly `CTA` at bottom `{% include_html cta/bottom-cta.html %}`
