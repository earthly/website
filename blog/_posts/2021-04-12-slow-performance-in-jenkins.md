---
title: 'Addressing Slow Performance in Jenkins'
categories:
  - Tutorials
toc: true
author: Milan Bhardwaj
internal-links:
    - jenkins
topic: ci
excerpt: |
    Learn how to address slow performance in Jenkins and significantly improve the performance of your continuous integration workflow. This guide provides tips and strategies for overcoming common Jenkins performance issues without necessarily upgrading your hardware.
last_modified_at: 2023-07-14
---
**In this article, we dive into optimizing Jenkins for better performance. If Jenkins slowdowns frustrate you, Earthly can boost your CI builds and help you conquer those stubborn performance issues. [Learn more](/).**

There's nothing more frustrating than a sluggish continuous integration system. It slows down feedback loops and prevents code from reaching production quickly. While quick fixes like using a bigger CI server can buy you time, you ultimately have to invest in maintaining the performance of your continuous integration workflow.

Jenkins is one of the most popular CI/CD tools out there, but its users often [experience lagging and responsiveness issues over time](https://issues.jenkins.io/browse/JENKINS-56243?page=com.atlassian.jira.plugin.system.issuetabpanels%3Aall-tabpanel). In this guide, I'll share an overview of some of the biggest Jenkins performance issues and some tips for significantly improving performance without necessarily upgrading your hardware.

## Why Is Jenkins Such a Popular Option for CI/CD?

Jenkins is a Java-based, open-source tool that is leveraged by [tens of thousands](https://www.businesswire.com/news/home/20181024005509/en/Jenkins-Community-Achieves-Record-Growth-Driven-by-Major-Innovation) of developers on hundreds of thousands of installations, making it the most popular automation server. This widespread use means that it's easy to find support and tips for Jenkins, but that's not the only reason it's so widely used.

Jenkins brought a lot of interesting paradigms to CI workflows, including:

- **Faster deployment.** Gone are the days when a build was tested and deployed once after all the developers committed their code. With Jenkins' automated CI/CD pipeline, whenever a developer commits code, it's built and tested throughout the day across multiple cycles.
- **[Scalable master-agent architecture](https://www.jenkins.io/doc/book/scaling/architecting-for-scale/).** When it comes to managing distributed builds at scale, Jenkins can be a good choice. Jenkins' primary server is the master that schedules build jobs and assigns them to agents (formerly, slaves) for execution. This pattern allows you to run Jenkins on one or hundreds of servers to speed up your builds.
- **Thousands of plugins:** Being an open-source platform, Jenkins provides a plethora of plugins for continuous integration built by other developers. This allows you to extend the base functionality without writing or maintaining much extra code in-house.

## Overcoming Common Jenkins Performance Issues

Over time, increased build frequency, multiple jobs running in parallel, and increasing build complexity can lead to performance issues in Jenkins. Your experience will likely vary based on your use case, but some common issues include:

- "Hangups" where the build seems "stuck" on a specific step each time it runs.
- Hitting memory limits on individual machines or the master node.
- CPU bottlenecks that slow down specific parts of a build.
- Bugs or inefficient code in plugins or scripts.

Since these issues can be caused by a wide variety of root causes, it's hard to generalize the solutions, but there are a few things that Jenkins users might want to look into. Here are some of the most universal ways you can improve your Jenkins build performance and limit the frequency of issues like those above.

### 1. Avoid Complex Groovy Script In Your Pipelines

The [Jenkins Groovy script console](https://www.jenkins.io/doc/book/managing/script-console/) is executed on the master node and directly uses master resources such as CPU and memory. Therefore, it's recommended that you reduce the number as well as the complexity of Groovy scripts in your pipelines and instead favor plugins that can be run on each agent directly.

The most common Groovy methods to avoid in Jenkins are JsonSlurper, Jenkins.getInstance, and HttpRequest. Jenkins has more suggestions for [scalable pipeline code and the operations to avoid on its blog](https://www.jenkins.io/blog/2017/02/01/pipeline-scalability-best-practice/).

### 2. Keep Builds Minimal at the Master Node

Jenkins' master node sits at the epicenter of the whole CI/CD process, where the application runs. Hence, the number of builds on the master node significantly affects resource usage. Keeping fewer builds on the master node will leave enough CPU and memory for agent nodes to schedule and trigger jobs.

You can use the "[Restrict where project can be run](https://stackoverflow.com/questions/13946929/ci-with-jenkins-how-to-force-building-happen-on-slaves-instead-of-master)" option in your job. While Jenkins will still run [a flyweight executor](https://support.cloudbees.com/hc/en-us/articles/360012808951-Pipeline-Difference-between-flyweight-and-heavyweight-Executors) on the master node, your heavyweight executors will run on the agent nodes.

Think of the master node as the brain of your Jenkins. Unlike agents, the master node can't be purged or replaced. So, to ensure optimum CI/CD functioning, consider doing some performance tuning on your Jenkins and free up the master node from unnecessary tasks. This will leave you with ample memory and CPU for effective scheduling and build triggers over agents.

### 3. Don't Bloat the Jenkins Master Installation

DevOps professionals often work across multiple teams and projects for CI/CD-related tasks. If that's your situation, take care not to burden a single Jenkins master. Instead, create multiple masters. Multiple masters will ensure project-specific resource allocation to masters, and you'll also avoid plugin collision.

Moreover, rather than setting up a long build that might fail anywhere in the cycle, remember to break your build into multiple smaller jobs.

### 4. Make Agent Management Effortless

While setting up Jenkins, it's important to set up the agents correctly. You want to make sure that when the time comes, you can add new agents or replace existing ones easily. To achieve this, consider creating a virtual machine image for the agent. You might also consider running Jenkins inside a [Docker container](https://devopscube.com/docker-containers-as-build-slaves-jenkins/) in a scalable cluster like Kubernetes or [Amazon EKS](/blog/how-to-setup-and-use-amazons-elastic-container-registry) where scaling agents is simple.

It's also a good idea to make agents generic and versatile; an agent should run multiple different jobs and utilize resources to the fullest extent.

### 5. Remove Older Builds

After a while, Jenkins builds can pile up, and disk consumption may get out of hand. Developers often overlook Jenkins' [Discard Old Builds](https://plugins.jenkins.io/discard-old-build/) option. Set metrics, such as the number of builds and days to keep builds and artifacts are under the Jenkins Log Rotation menu.

Rather than letting old builds accumulate and consume a file system, developers can enable _Discard Old Builds_ and enjoy automated resource usage cleanup once a Jenkins job finishes. You can also use the [G1 garbage collector](https://docs.oracle.com/javase/8/docs/technotes/guides/vm/gctuning/g1_gc.html) instead of Java 8's default [Parallel GC](https://docs.oracle.com/javase/8/docs/technotes/guides/vm/gctuning/parallel.html) since the former is a server-style garbage collector with a lower GC pause time.

Builds can also be removed [manually](https://superuser.com/a/1418896/92661) via the Jenkins command line or using a [cron job](https://opensource.com/article/17/11/how-use-cron-linux) that periodically cleans up old builds. You can find other options for discarding old build data [in this reference post](https://support.cloudbees.com/hc/en-us/articles/215549798-Deleting-Old-Builds-Best-Strategy-for-Cleanup-and-disk-space-management).

#### Prevent Resource Collision in Parallel Jobs

Jobs running in parallel might want exclusive access to ports or resources. This may cause a collision, fail a build and further slow down your Jenkins pipeline. For example, if you run multiple builds in parallel, there's a high chance they might collide while accessing a resource, say, Postgres's database port 5432.

Jenkins offers the [Throttle Concurrent Builds](https://plugins.jenkins.io/throttle-concurrents/) plugin to help regulate the number of concurrent builds on Jenkins nodes:

```
// Throttle a single operation
throttle(['test_1']) {
    node() {
        sh "sleep 100"
        echo "Done"
    }
}
```

You'll need to do some testing to see how many parallel builds your system can handle, but knowing how to set this limit and modify it will help you get started.

### 6. Lower Heap Size

Do you want to create CI/CD pipelines that are performance-oriented and never fail with a memory leak or out-of-memory errors? Pay attention to the _heap size_. As the number of Jenkins builds grows, the default heap size can be a limiting factor leading to out-of-memory errors if not attended to.

A majority of modern Java applications start with the maximum heap size configuration during startup. For Jenkins to run smoothly, lower the maximum heap size property to a maximum of [4 GB](https://docs.cloudbees.com/docs/admin-resources/latest/jvm-troubleshooting/#_heap_size) for starters. You can increase the heap size over time, depending on the Jenkins builds.

To set the heap size to 4 GB:

- Refer to `/etc/default/jenkins`
- Pass `JAVA_ARGS="-Xmx4096m"`

### 7. Avoid Plugin Overload

With over a thousand plugins available, Jenkins offers its users many capabilities for empowering their CI/CD pipelines. However, keep performance in mind when adding plugins and external services to your pipeline. Integrating Jenkins with external services will often slow down the Jenkins UI and lead to adverse effects, like dropped agents or disconnections.

In order to determine if a plugin is causing your builds to slow down, you can try running your builds with all or some plugins disabled. Gradually add each back to determine which is causing the bottleneck. Once you find the plugin (or combination of plugins) causing the performance issue, you have a few options:

1. **Find a replacement plugin** by searching the [Jenkins Plugin Index](https://plugins.jenkins.io/).
2. **See if Jenkins has added native support** for this feature by checking [the changelog](https://www.jenkins.io/changelog/). You may have to upgrade Jenkins to get the latest features, but this is generally a good idea for performance anyway.
3. **Replace the plugin with a custom script** bearing in mind that this could introduce new performance issues. Still, if you install a complex plugin, but only use one or two small features, a script might be more efficient.
4. **Remove the plugin** if you can live without it. Sometimes this is a worthwhile tradeoff.

## Tracking Jenkins Performance

As you start tuning your Jenkins performance, you might be interested in adding a plugin to help monitor and improve performance. For example, you can leverage the [Jenkins Monitoring plugin](https://plugins.jenkins.io/monitoring/) to get deep insights into your CI/CD pipeline, including:

- Errors and logs
- Charts for CPU, memory, and average system load
- Reports on HTTP sessions and HTTP response time
- Detailed statistics for build time and build steps
- Aggregated heap histogram for all nodes

![Jenkins Performance Monitoring Tool]({{site.images}}{{page.slug}}/mE6fSdy.png)

This can help you assess the effectiveness of your performance tweaks and guide you as you continue to improve your Jenkins installation.

## Wrapping It Up

Jenkins' responsiveness issues are common, especially when dealing with heavier builds. Broken Jenkins CI/CD pipelines can stall your development teams and create unnecessary dependencies. The tips discussed in this article should help you boost the performance of your Jenkins CI/CD pipeline significantly.

Looking to make your builds more repeatable? [Earthly](https://earthly.dev/) replaces clunky [bash scripts](/blog/understanding-bash) and Makefiles by giving you a single understandable, consistent definition for your CI/CD builds and it works great with Jekyll. Learn more [at Earthly.dev](https://earthly.dev/).