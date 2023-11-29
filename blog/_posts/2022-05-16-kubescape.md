---
title: "Using Kubescape to Scan Kubernetes"
categories:
  - Tutorials
toc: true
author: Boemo Wame Mmopelwa
internal-links:
 - kubescape
excerpt: |
    Learn how to improve the security of your Kubernetes cluster with Kubescape, a free tool that scans for non-compliant YAML files and image vulnerabilities. Find out how to install Kubescape on Windows, macOS, and Linux, and discover how to analyze the scan results to identify and fix security risks.
last_modified_at: 2023-07-19
---
**This article examines the Kubescape security tool's features. Earthly provides consistent and efficient build processes for developers securing Kubernetes with Kubescape. [Learn more about Earthly](/).**

Kubescape is a free tool that improves Kubernetes security by scanning clusters and detecting YAML files that are not compliant with security standards such as the [National Security Agency](https://www.nsa.gov/)(NSA) guidelines. It also scans for image vulnerabilities. After scanning and analyzing your cluster it will output your cluster's risk analysis into a report in PDF or JSON format.

In this tutorial, you will learn how to scan your Kubernetes cluster using Kubescape. In addition, you will learn how to analyze the Kubescape scan results.

## Prerequisites

You need to have installed [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/) and have a running cluster before starting this tutorial.

## How to Install Kubescape

The Kubescape is available on Windows, macOS, and Linux. This tutorial will give cover install on Windows, Linux, and MacOS.

## Installing Kubescape CLI on Windows

Use the following command to install Kubescape CLI on Windows using Powershell:

~~~{.bash caption=">_"}
$ iwr -useb https://raw.githubusercontent.com/armosec/kubescape/master/install.ps1 | iex
~~~

If you have downloaded Kubescape successfully without errors, you will get the following output:

~~~{.bash caption="Output"}
Installing Kubescape...
Finished Installation
~~~

There is a possibility that the installation process might fail because Powershell has not been enabled or you can get an error that says "the internet explorer engine is not available". To resolve the latter error, go ahead and download [internet explorer](https://en.softonic.com/download/internet-explorer-9-vista-32/windows/post-download). After you have installed the internet explorer start the Kubescape installation procedure; this time it will install successfully.

Also, change the execution policy and enable Powershell using the following command if you had an installation error:

~~~{.bash caption=">_"}
$ Set-ExecutionPolicy RemoteSigned -scope CurrentUser
~~~

## Installing Kubescape CLI on `macOS`

Use the following two commands to install Kubescape using Homebrew. If you don't have Homebrew, go ahead and download it from [brew](https://brew.sh/).
<!-- markdownlint-disable MD029 -->
1. Start by adding the Kubescape GitHub repository:

~~~{.bash caption=">_"}
$ brew tap armosec/kubescape
~~~

2. Install Kubescape:

~~~{.bash caption=">_"}
$ brew install kubescape
~~~

## Installing Kubescape CLI on Linux

Go ahead and download Kubescape CLI binary files from [GitHub](https://github.com/armosec/kubescape/releases). For now, Kubescape has only Ubuntu binary files.

## Successful Installation Confirmation and Using Kubescape -H Command

Use the following to check the Kubescape version:

~~~{.bash caption=">_"}
$ kubescape version
~~~

You will get the following output if Kubescape has been downloaded successfully:

~~~{.bash caption="Output"}
Your current version is: v2.0.152
~~~

Use the following command to get all the available commands:

~~~{.bash caption=">_"}
$ kubescape -h
~~~

You will get the following output:

~~~{.bash caption="Output"}
Based on NSA \ MITRE ATT&CK(r) and other frameworks specifications

Usage:
  kubescape [command]

Examples:

  # Scan command
  kubescape scan --submit

  # List supported frameworks
  kubescape list frameworks

  # Download artifacts (air-gapped environment support)
  kubescape download artifacts

  # View cached configurations
  kubescape config view


Available Commands:
  completion  Generate autocompletion script
  config      Handle cached configurations
  delete      Delete configurations in Kubescape SaaS version
  download    Download controls-inputs,exceptions,control,framework,artifacts
  help        Help about any command
  list        List frameworks/controls will list the supported frameworks and controls
  scan        Scan the current running cluster or yaml files
  submit      Submit an object to the Kubescape SaaS version
  version     Get current version
~~~

You can also get extra information on a certain command by adding the `-h` flag. For example:

~~~{.bash caption=">_"}
$ kubescape scan -h
~~~

You will get the following examples on how to use the above command:

~~~{.bash caption="Output"}
The action you want to perform

Usage:
  kubescape scan [flags]
  kubescape scan [command]

Examples:

  Scan command is for scanning an existing cluster or kubernetes manifest files based on pre-defind frameworks

  # Scan current cluster with all frameworks
  kubescape scan --submit --enable-host-scan --verbose

  # Scan kubernetes YAML manifest files
  kubescape scan *.yaml

  # Scan and save the results in the JSON format
  kubescape scan --format json --output results.json

  # Display all resources
  kubescape scan --verbose

  # Scan different clusters from the kubectl context
  kubescape scan --kube-context <kubernetes context>
~~~

## How to Scan Your Kubernetes Cluster Using Kubescape

Security compliance standards are a set of rules, guidelines, and procedures that show developers how to protect their clusters and production environments. Most of all, these security compliance standards are used to gauge the competency of organizations and individuals in securing their software.

Kubescape uses security compliance standards and security frameworks such as [`MITRE ATT&CK`](https://attack.mitre.org/) and [National Security Agency](https://www.nsa.gov/)(NSA) to analyze security risks and vulnerabilities found in your cluster. The `MITRE ATT&CK` framework is used to describe security and model threats; while the NSA has a list of recommendations that guide developers on how they can secure their clusters.

The `kubescape scan` command scans every Kubernetes object available in your cluster and helm charts installed on your cluster. It has the following flags:

- `--submit`: This flag sends the scan results to the Armo management portal.
- `--enable-host-scan`: This flag deploys the ARMO K8s host-sensor DaemonSet that collects valuable and unlimited information from your host machine about your cluster.
- `--verbose`: This flag displays all the resources scanned.``

Use the following command to scan your cluster:

~~~{.bash caption=">_"}
$ kubescape scan --submit --enable-host-scan --format-version v2 --verbose 
~~~

This scanning command will output all the security analyses of every object in your cluster. From the scan results, I have picked the deployment object's results which I will use to teach how to analyze the scan results in the next subsection.

## How to Analyze Kubescape Scan Results

The following table contains the risk analysis of the deployment object. The risk analysis has the following fields:

- Threat severity: This field measures how critical the threat is. There are three levels of a threat, which are: High, Medium, and Low.
- Control Name: This field states the name of the component or aspect being analyzed.
- Docs: This field contains the link that redirects you to a page that contains information about the risk and threat detected during the scan.
- Assistant remediation: This field contains changes that can be made to your YAML file or cluster in order to eliminate the threat.

<table>
  <tr>
   <td><strong> SEVERITY                                                                           </strong>
   </td>
   <td><strong>CONTROL NAME</strong>
   </td>
   <td><strong>DOCS   </strong>
   </td>
   <td><strong>ASSISTANT REMEDIATION</strong>
   </td>
  </tr>
  <tr>
   <td> High
   </td>
   <td> Resources CPU limit and request  
   </td>
   <td>https://hub.armo.cloud/docs/c-0050
   </td>
   <td>spec.template.spec.containers[0]
   .resources.limits.cpu=YOUR_VALUE
<p>
spec.template.spec.containers[0]
.resources.requests.cpu=YOUR_VALUE
   </td>
  </tr>
  <tr>
   <td>Medium  
   </td>
   <td> Automatic mapping of service account
<p>
CVE-2022-0492-cgroups-container-escape
<p>
Ingress and Egress blocked
<p>
 Non-root containers
   </td>
   <td><a href="https://hub.armo.cloud/docs/c-0034">https://hub.armo.cloud/docs/c-0034</a>
<p>
<a href="https://hub.armo.cloud/docs/c-0086">https://hub.armo.cloud/docs/c-0086</a>
<p>
<a href="https://hub.armo.cloud/docs/c-0030">https://hub.armo.cloud/docs/c-0030</a>
<p>
https://hub.armo.cloud/docs/c-0013
   </td>
   <td>spec.template.spec.automountServiceAccountToken=false
<p>
spec.securityContext.runAsNonRoot=true
<p>

<p>
spec.securityContext.runAsNonRoot=true
   </td>
  </tr>
  <tr>
   <td>Low
   </td>
   <td> K8s common labels usage
<p>
Label usage for resources
<p>
Resource policies
   </td>
   <td><a href="https://hub.armo.cloud/docs/c-0077">https://hub.armo.cloud/docs/c-0077</a>
<p>
https://hub.armo.cloud/docs/c-0076
<p>
https://hub.armo.cloud/docs/c-0009
   </td>
   <td>metadata.labels=YOUR_VALUE
<p>
spec.template.metadata.labels=YOUR_VALUE
<p>

<p>
spec.template.spec.containers[0].resources.limits.cpu=YOUR_VALUE
<p>

   </td>
  </tr>
</table>

Vulnerabilities that are classified as High should be fixed within a short period of time. Use the information from the Docs and Assistance Remediation columns to help you fix the vulnerability detected.

The `--verbose` flag has limitations as the displayed results can be overwhelming and lead to Powershell clearing the first details. To solve this issue, convert the scan results to PDF using the following command:

~~~{.bash caption=">_"}
$ kubescape scan --format pdf --output results.pdf
~~~

The scan results.pdf file will be saved in your clusters directory or the directory you are currently using when scanning the cluster. The results will look like this in PDF format:

<div class="wide">
![Cluster Scan Results]({{site.images}}{{page.slug}}/alUD1l1.jpg)
</div>

Kubescape allows you to scan the cluster using your desired security framework such as the NSA framework. All you have to do is state the name of the framework as shown below:

~~~{.bash caption=">_"}
$ kubescape scan framework nsa --submit --format pdf --output nsa.pdf
~~~

You will get the following output:

<div class="wide">
![NSA framework scan results]({{site.images}}{{page.slug}}/Ynxknex.jpg)
</div>

You can also specifically scan containers that have escalated and privilege rights; by adding the control which is "Privileged container":

~~~{.bash caption=">_"}
$ kubescape scan control "Privileged container" --format pdf --output privcontainer.pdf
~~~

You will get the following output:

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/6510.png %}
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/6540.png %}
</div>

## How to Scan a Specific YAML File

Since you now know how to scan a Kubernetes cluster using Kubescape, it's now time to scan a specific YAML file. I have created a YAML file called logger.yaml which contains the contents that are used to write logs to the standard output stream per second. I will scan this file using Kubescape. Here are the contents of the YAML file:

~~~{.yaml caption=""}
apiVersion: v1
kind: Pod
metadata:
  name: logger
spec:
  containers:
  - name: count
    image: busybox:1.28
    args: [/bin/sh, -c,
            'i=0; while true; do echo "$i: $(date)"; i=$((i+1)); sleep 1; done']
~~~

Use the following command to scan the above YAML file:

~~~{.bash caption=">_"}
$ kubescape scan logger.yaml --format pdf --output logger.pdf
~~~

You will get the following output:

![Scan results of logger.yaml]({{site.images}}{{page.slug}}/UN40COM.jpg)

## Conclusion

Threat visibility is essential in security analysis, keeping you informed of potential risks in your cluster. Regular scanning of clusters and YAML files aids in identifying immediate vulnerabilities. Once your environment passes the Kubescape scan with 0% risk, your cluster achieves compliance with NSA, MITRE, etc., paving the way for various compliance badges. These badges enhance your business reputation, attracting client trust due to the assurance of high security standards.

And once you've secured your Kubernetes with Kubescape, why not step up your build process next? Check out [Earthly](https://www.earthly.dev/), a tool that can streamline your build process.

{% include_html cta/bottom-cta.html %}