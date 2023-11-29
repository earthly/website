---
title: "Kube-Bench"
categories:
  - Tutorials
toc: true
author: Anurag Kumar

internal-links:
 - CLI
 - Kube-Bench
 - Kubernetes
 - cluster
excerpt: |
    Learn how to benchmark your Kubernetes cluster against CIS benchmarks using Kube-Bench. This tutorial provides step-by-step instructions on installing and configuring Kube-Bench, running benchmarks via CLI, fixing WARN and FAIL benchmarks, and automating the process using Kubernetes jobs and cronjobs.
last_modified_at: 2023-07-19
---
**This article discusses Kubernetes security benchmarking. Kube-bench secures Kubernetes clusters, while Earthly ensures robust and reliable CI pipeline builds. [Check it out](/).**

## What Is CIS?

CIS security is a community driven and non-profit organization that aims at improving security around the internet. It is the one that creates and updates CIS controls and CIS benchmarks. You can read more about the [CIS](https://www.cisecurity.org/about-us)

## What Are CIS Benchmarks?

CIS benchmarks are best practices around your IT system. Kubernetes CIS benchmarks are industry-accepted system hardening procedures. CIS Kubernetes benchmarks are reviewed by Kubernetes community as well as security experts.

## **How You Can Benchmark Your Cluster Against CIS Benchmarks?**

There are two ways in which you can benchmark your cluster against CIS benchmarks

1. Kube-bench CLI
2. Kubernetes Jobs & CronJobs
We will talk about this in detail in the blog.

## Spinning Your Kubernetes Cluster

For the purpose of this blog, I'm using [minikube](/blog/k8s-dev-solutions), and you can refer to minikube [installation](https://minikube.sigs.k8s.io/docs/start/)

If you're running kind then you can perform the same thing, but you've to exec into the control plane container. In order to create your cluster using kind refer to the [docs](https://kind.sigs.k8s.io/docs/user/quick-start/) kind assumes your [docker](/blog/docker-slim) container as Kubernetes nodes, so in order exec into your kind controlplane container use

~~~{.bash caption=">_"}
docker exec -it <container-name> /bin/bash
~~~

## Installing Kube-Bench

We will use [GitHub](/blog/ci-comparison) releases to install kube-bench. Go to the GitHub releases [page](https://github.com/aquasecurity/kube-bench/releases/tag/v0.6.8) Download kube-bench according to your system. I'm using Linux amd64, so I will be going with that.

~~~{.bash caption=">_"}
curl -LO https://github.com/aquasecurity/kube-bench/releases/download/v0.6.8/kube-bench_0.6.8_linux_amd64.tar.gz
~~~
  
After this, you have to create one directory where the default config files of kube-bench will reside.

~~~{.bash caption=">_"}
sudo mkdir -p /etc/kube-bench
~~~

Now after this you need to untar the kube-bench files in this above directory.

~~~{.bash caption=">_"}
sudo tar -xvf kube-bench_0.6.8_linux_amd64.tar.gz -C /etc/kube-bench
~~~

Last thing that you need to do is to move the kube-bench binary to /usr/local/bin

~~~{.bash caption=">_"}
sudo mv /etc/kube-bench/kube-bench /usr/local/bin
~~~

You have successfully installed and configured kube-bench, and we are ready to move ahead. To verify the installation, use the command `kube-bench version`

<div class="wide">

![kube-bench installation]({{site.images}}{{page.slug}}/Imgur.gif)\

</div>

## A Hands-on Guide to Kube-Bench

### Running Kube-Bench via Cli

Previously, We had installed kube-bench, and it's time to try it out. To use kube-bench, you just have to run kube-bench run Now what will happen in the background is kube-bench will run all the checks that's there in the CIS benchmarks. After running all the checks, it will give you a formatted output of FAIL, WARN, and PASS benchmarks.

Before analysing the output of the previous command, let's try to understand what are the components of the Kubernetes cluster that kube-bench benchmarks. Essentially, kube-bench will benchmark your configurations of the followings.

1. Control Plane Components
2. Etcd
3. Control Plane Configurations
4. Worker Nodes
5. Policies

## How to Fix the Warn and Fail Benchmarks?

![Fix]({{site.images}}{{page.slug}}/fix.jpg)\

We will use one example of each WARN and FAIL in order to understand how to fix these. If you want quick and immediate solution, then you can look at the output right after the completion of each section's benchmark.

When you will look at the output of the previous command, then in the first section you will see something like this.

~~~{.bash caption=">_"}
[WARN] 1.2.12 Ensure that the admission control plugin AlwaysPullImages
is set (Manual)

[WARN] 1.2.13 Ensure that the admission control plugin SecurityContextDeny
is set if PodSecurityPolicy is not used (Manual)

[PASS] 1.2.14 Ensure that the admission control plugin ServiceAccount is 
set (Automated)

[PASS] 1.2.15 Ensure that the admission control plugin NamespaceLifecycle 
is set (Automated)

[PASS] 1.2.16 Ensure that the admission control plugin NodeRestriction 
is set (Automated)

[PASS] 1.2.17 Ensure that the --secure-port argument is not 
set to 0 (Automated)

[FAIL] 1.2.18 Ensure that the --profiling argument is set to 
false (Automated)

[FAIL] 1.2.19 Ensure that the --audit-log-path argument is set (Automated)

[FAIL] 1.2.20 Ensure that the --audit-log-maxage argument is set to 30 
or as appropriate (Automated)

[FAIL] 1.2.21 Ensure that the --audit-log-maxbackup argument is set to 
10 or as appropriate (Automated)
~~~

> **Note** :
> This is just one section that I have taken to illustrate how to solve WARN and FAIL checks. The output can be different for you.

Let's first understand how to understand the output of the kube-bench run command.

### Output Format of the Kube-Bench

The general output format looks something like this. We have 5 sections as mentioned earlier that we target using kube-bench. Each section starts with info describing the component it's benchmarking. e.g. consider the first section.

~~~{.bash caption=">_"}
[INFO] 1 Control Plane Security Configuration

[INFO] 1.1 Control Plane Node Configuration Files
~~~
  
The first section is all about controlplane configuration and all the manifests associated with controlplane.

Then You will get a complete list of **PASS**, **FAIL** and **WARN** checks.

kube-bench also gives you remediation recommendations right below the checks of each section. Below is an example.

~~~{.bash caption=">_"}
== Remediations master ==

1.1.9 Run the below command (based on the file location on your system)/
 on the control plane node.

For example, chmod 644 <path/to/cni/files>
~~~
  
And at the end you will get a summary of all the checks within one section. e.g. here is an example of the first section

~~~{.bash caption=">_"}
== Summary master ==
43 checks PASS
9 checks FAIL
10 checks WARN
0 checks INFO
~~~
  
If you want more detailed look then you can set the verbosity while executing the command

~~~{.bash caption=">_"}
$ kube-bench run -v 5
~~~

To get the output in [JSON](/blog/convert-to-from-json) you can execute the following

~~~{.bash caption=">_"}
$ kube-bench run --json | jq
~~~

## CIS Kubernetes Benchmark Guide

![Guide]({{site.images}}{{page.slug}}/guide.jpg)\

When you visit the CIS website, then you'll get a handbook that lists all the benchmarks and their remediation in detail. When you're not sure about why a particular benchmark is failing, then this is the reference you should follow.

If you look at the first section, then the content is structured in four parts.

1 Control Plane Components
    1.1 Control Plane Node Configuration Files
    1.2 API Server
    1.3 Controller Manager
    1.4 Scheduler

### Running Kube-Bench as Kubernetes Jobs

Now, in the previous part we have learnt about running kube-bench via the command line utility but when we want to run our kube-bench jobs after a fixed interval of time for example on a period of 10 days then doing it manually will be tedious. Although, we can automate it using the Linux Jobs but in this blog we will use Kubernetes jobs to run kube-bench. First, we will set Kubernetes job to run kube-bench and then in the immediate next section, we will configure the job to run every week with the help of Kubernetes cronjobs. The difference between jobs and cronjobs is that with cronjobs, you can configure a job to run a repeating task on a regular schedule.

If you look at the [GitHub](/blog/ci-comparison) repo of kube-bench then you will see a [job.yaml](https://github.com/aquasecurity/kube-bench/blob/main/job.yaml) file in the parent directory. This is the manifest you need to run your kube-bench as Kubernetes jobs.

On your cluster, you just need to apply this manifest.

~~~{.bash caption=">_"}
$ kubectl apply -f https://raw.githubusercontent.com/aquasecurity/\
kube-bench/main/job.yaml
job.batch/kube-bench created

$ kubectl get jobs,pods
NAME                   COMPLETIONS   DURATION   AGE
job.batch/kube-bench   1/1           4s         28s

NAME                   READY   STATUS      RESTARTS   AGE
pod/kube-bench-s268f   0/1     Completed   0          28s

$ kubectl logs $(kubectl get pods -o name)
[INFO] 1 Control Plane Security Configuration
[INFO] 1.1 Control Plane Node Configuration Files
...
...
~~~

**Note:** You need to have the configuration files in place, then only the logs will show up in a correct manner.

### Setting Kube-bench To Run Every Monday

In some organizations, there can be a regular time-frame where you need the security scanning. It can be daily/weekly/monthly, depending on the compliance your organization is adhering to. In this section, we will use Kubernetes cronjobs to run our jobs every Sunday at midnight. Let's look at the manifest below and apply this to our Kubernetes cluster. With the following [manifest](https://gist.github.com/kranurag7/dbe36952b476d1e600857fd89028e54b) you can benchmark your Kubernetes cluster every two minutes. If you want to change this the timing, then change it in the spec.schedule section. You can use this [website](https://crontab.guru) in order to make your job easy.

### Kube-Bench For Cloud Specific K8s Cluster

Although kube-bench runs on any Kubernetes cluster, some big cloud provider have their own security benchmarks. Chances are you would have noticed it during the installation of the kube-bench. You can read more about [AWS EKS](https://www.eksworkshop.com/intermediate/300_cis_eks_benchmark/) CIS benchmarks here. Similarly, you can read about [google GKE](https://cloud.google.com/kubernetes-engine/docs/concepts/cis-benchmarks) & [azure AKS](https://docs.microsoft.com/en-us/azure/aks/cis-kubernetes) CIS benchmarks. So, if you're running your Kubernetes workloads on any of these managed offerings, then you should run the respective cloud specific CIS benchmarks as well. You can check all the cloud specific benchmarks in the /etc/kube-bench/cfg directory.

~~~{.bash caption=">_"}
$ cd /etc/kube-bench/cfg
$ tree .
.
|-- ack-1.0
|   |-- config.yaml
|   |-- controlplane.yaml
|   |-- etcd.yaml
|   |-- managedservices.yaml
|   |-- master.yaml
|   |-- node.yaml
|   `-- policies.yaml
|-- aks-1.0
|   |-- config.yaml
|   |-- controlplane.yaml
|   |-- managedservices.yaml
|   |-- master.yaml
|   |-- node.yaml
|   `-- policies.yaml
|-- cis-1.20
|   |-- config.yaml
|   |-- controlplane.yaml
|   |-- etcd.yaml
|   |-- master.yaml
|   |-- node.yaml
|   `-- policies.yaml
|-- cis-1.23
|   |-- config.yaml
|   |-- controlplane.yaml
|   |-- etcd.yaml
|   |-- master.yaml
|   |-- node.yaml
|   `-- policies.yaml
|-- cis-1.5
|   |-- config.yaml
|   |-- controlplane.yaml
|   |-- etcd.yaml
|   |-- master.yaml
|   |-- node.yaml
|   `-- policies.yaml
|-- cis-1.6
|   |-- config.yaml
|   |-- controlplane.yaml
|   |-- etcd.yaml
|   |-- master.yaml
|   |-- node.yaml
|   `-- policies.yaml
|-- config.yaml
|-- eks-1.0.1
|   |-- config.yaml
|   |-- controlplane.yaml
|   |-- managedservices.yaml
|   |-- master.yaml
|   |-- node.yaml
|   `-- policies.yaml
|-- gke-1.0
|   |-- config.yaml
|   |-- controlplane.yaml
|   |-- etcd.yaml
|   |-- managedservices.yaml
|   |-- master.yaml
|   |-- node.yaml
|   `-- policies.yaml
|-- gke-1.2.0
|   |-- config.yaml
|   |-- controlplane.yaml
|   |-- managedservices.yaml
|   |-- master.yaml
|   |-- node.yaml
|   `-- policies.yaml
|-- rh-0.7
|   |-- config.yaml
|   |-- master.yaml
|   `-- node.yaml
`-- rh-1.0
    |-- config.yaml
    |-- controlplane.yaml
    |-- etcd.yaml
    |-- master.yaml
    |-- node.yaml
    `-- policies.yaml
~~~
  
There are benchmarks for large cloud providers Kubernetes offerings like GKE, EKS, AKS etc. If you're running your Kubernetes workloads in any one of them, then you can benchmark your cluster and configurations using kube-bench. In order to run gke-1.2.0 benchmark, you will execute the following command.

~~~{.bash caption=">_"}
$ kube-bench --benchmark gke-1.2.0
~~~

This will give you all the warnings, pass & failed checks with respect to your GKE cluster.

## Conclusion

Using kube-bench in production allows you to benchmark your Kubernetes cluster against CIS benchmarks effectively, helping you avoid misconfigurations. Following CIS benchmarks ensures you abide by best practices for running Kubernetes. This guide should equip you to understand and utilize kube-bench for benchmarking your cluster.

If you're looking to further enhance your Kubernetes workflows, consider giving [Earthly](https://www.earthly.dev/) a try. It offers efficient and reproducible builds, adding another layer of optimization to your development process.

{% include_html cta/bottom-cta.html %}