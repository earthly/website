---
title: "Top 7 Platform Engineering Tools"
toc: true
author: Alexandre Couëdelo

internal-links:
 - top platform engineering tools
 - platform engineering tools
 - mostly used platform engineering tools
 - best platform engineering tools
excerpt: |
    Platform engineering focuses on improving developer productivity through standardized tooling, automation, and best practices. This article highlights seven popular platform engineering tools, including Backstage for building developer portals, Terraform for infrastructure provisioning, and Kubernetes for container orchestration.
categories:
  - Platforms
---
**This article lists key platform engineering tools for developers. Earthly guarantees consistent builds in any environment. [Learn more about Earthly](https://cloud.earthly.dev/login).**

Platform engineering focuses on improving overall developer productivity through standardized tooling, automation, and best practices. It involves creating and managing a shared infrastructure and internal development platform (IDP) that software teams can use to develop, deploy, and operate their applications.

However, you can't expect developers to be experts in all the technologies involved in the software development process. A platform helps abstract or aggregate various tools under a unified set of interfaces.

![Platform engineering and tooling, courtesy of Alexandre Couëdelo]({{site.images}}{{page.slug}}/j3837Ob.png)

In this article, you'll learn about seven of the most popular tools that platform engineers use and the benefits that they provide.

## Backstage

![Backstage]({{site.images}}{{page.slug}}/backstage.png)\

Originally developed by Spotify as an IDP, [Backstage](https://backstage.io/) has evolved into an open source platform for building developer portals. Since its acceptance to the Cloud Native Computing Foundation (CNCF) in 2020, it's become increasingly popular. [Many companies](https://github.com/backstage/backstage/blob/master/ADOPTERS.md)—including Expedia, Netflix, and VMware—have built their developer platform on top of Backstage and created various plugins to extend its functionalities.

At its core, Backstage is a software catalog, or a repository listing applications, services, and tools that are developed and used in an organization. The catalog also captures relations between various applications to provide insights and documentation to developers. Additionally, various plugins extend the possibility of gathering and displaying information; for instance, you can integrate Backstage with your CI/CD so that each entity in the catalog gets details about build and deployment status.

Backstage's self-service IDP, a set of tools and automation that enable developers to quickly and independently perform typical configuration tasks, is anchored by its [software templates](https://backstage.io/docs/features/software-templates/) feature. Using this template system, developers can create reusable workflow configurations via the Backstage UI. All you have to do is select a template. The automation then kicks in and provisions the required resources, such as code repositories and infrastructure components, on demand.

Backstage is so popular that competitors like Cortex and Humanitec decided to offer Backstage plugins so you can use Backstage as a UI for their platforms.

### Backstage Pros and Cons

Backstage provides a centralized platform for developers that helps improve the developer experience. This platform organizes and simplifies access to documentation, services, tooling, and infrastructure services.

Spotify continues to drive the evolution of Backstage, with a dedicated team providing frequent updates and [premium plugins](https://backstage.spotify.com/marketplace/spotify/bundle/spotify-plugins-bundle/) at an additional cost.

However, while Backstage's plugins offer a high degree of flexibility and customization, the process of integrating plugins and customizing Backstage can be complex. Backstage is more of a framework to build an IDP than an off-the-shelf solution.

Additionally, because Backstage is centered around its software catalog, it takes time to customize the platform. For smaller teams, this extensive effort may not be worth it.

### When to Use Backstage

Backstage is a great tool for platform engineering and software development. Software catalogs like Backstage shine when you have a large number of applications (100+) distributed across multiple teams (10+). If your company isn't that big yet, Backstage may have too much configuration and maintenance overhead for your use case.

## Terraform

![Terraform]({{site.images}}{{page.slug}}/terraform.png)\

Created by HashiCorp in 2014, [Terraform](https://www.terraform.io/) is an open source infrastructure as code (IaC) tool. It simplifies the process of provisioning cloud infrastructure through the use of a high-level configuration language called HashiCorp Configuration Language (HCL).

Terraform's continued popularity has spurred the development of numerous integrations called [providers](https://developer.hashicorp.com/terraform/language/providers). With Terraform, you can configure cloud provisioning for any application or software as a service (SaaS) that offers an API, as long as a Terraform provider has been created by either the service itself or the community.

One of Terraform's key features is the concept of [state](https://developer.hashicorp.com/terraform/language/state), which reflects the current configuration of the infrastructure. By saving the state after provisioning the infrastructure, any subsequent changes can be inferred based on what needs to be modified. Instead of blindly applying a recipe to provision infrastructure, Terraform uses a two-stage approach:

1. **Plan:** Terraform computes a plan, which is a list of changes required to go from the current state to the desired state.
2. **Apply:** If the user is happy with the plan provided by Terraform, they can trigger the `apply` command to start the provisioning.

HCL captures the dependencies between the resources it defines. If resource A references resource B, then Terraform ensures that resource B is created before provisioning resource A. That way, you don't need to bother with an execution step, as Terraform handles all that for you.

Terraform also supports reusable infrastructure configurations called [modules](https://developer.hashicorp.com/terraform/language/modules). Operations teams can provide modules to reduce the configuration work required for developers to provision common systems.

### Terraform Pros and Cons

Terraform lets users define and provision infrastructure using a version-controlled declarative configuration language. This IaC approach makes infrastructure changes easily auditable and reproducible. However, while its declarative syntax is simple to learn and use, it's not a shortcut for managing infrastructure. You need to be familiar with the cloud/SaaS resources you want to provision.

Terraform supports a wide range of service providers (both cloud and on-premise), enabling users to manage a diverse set of infrastructure resources through a single tool. Additionally, Terraform's execution plans and resource dependency management provide predictability and safety, ensuring that the state of infrastructure deployments is reliable and repeatable.

It should be noted that while Terraform's state management is an ingenious way to manage infrastructure, it can become a challenge at scale. The more resources that are part of a state, the more intricate it becomes and the more time it takes to compute a plan.

### When to Use Terraform

Terraform is a good option for small and large projects. Its universal interface can help provision and configure your infrastructure and SaaS providers. However, keep in mind that you need to adapt your usage of the tools to the size of your infrastructure. As your infrastructure and teams grow, you'll need to build [modules](https://developer.hashicorp.com/terraform/language/modules) to help simplify common configuration tasks and divide your configuration into relatively small [states](https://developer.hashicorp.com/terraform/language/state).

## Kubernetes

![Kubernetes]({{site.images}}{{page.slug}}/kubernetes.png)\

[Kubernetes](https://kubernetes.io/) is an open source container orchestration system for automating software deployment, scaling, and management. It was originally designed by Google in 2014 and donated as the inaugural project to CNCF in 2015.

Currently, Kubernetes is the de facto container orchestration platform, most likely due to its configuration system, which allows for declarative management (using YAML) of its components. Once the configuration is applied to a Kubernetes cluster, the control plane continuously tries to achieve the desired state, reflecting the configuration you provided.

Kubernetes configurations can be version-controlled, enabling teams to apply the practice of IaC. Additionally, Kubernetes offers a CLI tool called [kubectl](https://kubernetes.io/docs/reference/kubectl/), which provides a powerful interface for managing resources.

### Kubernetes Pros and Cons

One of the main advantages of Kubernetes is that it automates the deployment, scaling, and management of containerized applications, addressing the complexity of managing containers at scale. It's also a modular platform that can be extended in several ways (such as with custom resources and operators, hooks, and plugins).

Kubernetes has robust community support and a vast ecosystem of tools and extensions. Most open source applications these days prove that recipes can be deployed to Kubernetes in minutes.

However, managing Kubernetes involves significant operational overhead. A production cluster requires a lot of additional application pieces, including configuration management (like Argo CD or Flux CD), secrets management, artifact management/registry, logs, metrics, traces, analytics, alerts, and more. This often requires dedicated teams to manage the cluster and its tooling. Nowadays, cloud providers offer alternatives with a much lower barrier to entry, such as [GCP Cloud Run](https://cloud.google.com/run?hl=en) and [AWS Fargate](https://aws.amazon.com/fargate/).

Additionally, Kubernetes's extensive range of features and configurations can be overwhelming, posing challenges for both developers adapting to its paradigm shift and operators selecting the appropriate tooling.

### When to Use Kubernetes

Kubernetes is a mature container orchestration platform, but it's not for everyone. It's best suited for companies with over twenty applications that need an elastic workload.

If you're a small company, the heavy lifting and responsibility of setting up and maintaining Kubernetes clusters could slow you down. Cloud providers provide plenty of low-barrier entry solutions, from serverless (such as AWS Lambda and GCP Cloud Functions) to fully managed container orchestration platforms (such as AWS Fargate and GCP Cloud Run).

## Prometheus

![Prometheus]({{site.images}}{{page.slug}}/prometheus.png)\

[Prometheus](https://prometheus.io/) is an open source systems monitoring and alerting toolkit originally built at SoundCloud in 2012 and later donated to the CNCF in 2016. Prometheus played a significant role in shaping the cloud-native landscape. Its data model for metrics was so popular that it became an independent standard called [OpenMetrics](https://openmetrics.io/).

At its core, Prometheus is a time series database capable of pulling and storing metrics from your application. These metrics can later be accessed and used via its comprehensive query language, [PromQL](https://prometheus.io/docs/prometheus/latest/querying/basics/).

The combination of Prometheus, [Grafana](https://grafana.com/), and [Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/) is one of the most popular open source monitoring stacks. Grafana offers metrics visualization and dashboards, while Alertmanager enables you to monitor events and perform real-time alerting.

### Prometheus Pros and Cons

Prometheus's data model and query language make it an effective choice for monitoring the state of infrastructure and applications and alerting on anomalies. Its architecture is capable of handling high volumes of metrics from various sources without [external storage](https://prometheus.io/docs/prometheus/latest/storage/) (no database or blob storage required), as the Prometheus nodes handle the storage on their local disk.

Because Prometheus helped shape the standards for application metrics, most tooling exposes Prometheus-style metrics. Additionally, you can find a wide variety of exporters that allow you to ingest external metrics into Prometheus, including GCP metrics and AWS CloudWatch.

Although Prometheus excels in efficiency and centralizing metrics—especially for long-term retention or with high-cardinality metrics—it can pose challenges without supplementary components like [Thanos](https://thanos.io/). Without such components, managing long-term retention or dealing with high-cardinality metrics would necessitate large and costly Prometheus instances.

Additionally, if you're looking for fast and efficient queries for time series metrics, you must carefully design your metrics or add additional mechanisms such as aggregation, compaction, and sampling. Without these mechanisms, you may experience slower queries and increased storage costs.

### When to Use Prometheus

Prometheus is ideal if you're getting started with metrics and event monitoring; it's easy to deploy a Prometheus instance and instrument your application to expose metrics.

Prometheus has a slight learning curve, but challenges only arise on the operation side when the amount of data ingested becomes significant (over ten GB a day).

## Logstash

![Logstash]({{site.images}}{{page.slug}}/logstash.png)\

[Logstash](https://www.elastic.co/logstash) is an open source data processing pipeline specially designed to handle logs and events from your applications. It was created by [Jordan Sissel](https://www.elastic.co/blog/welcome-jordan-logstash) in 2009 and later became a part of the [Elastic Stack](https://www.elastic.co/elastic-stack/).

Logstash can ingest data from multiple sources simultaneously, transform it, and then send it to a "stash" like Elasticsearch or even a database. It's primarily used in application log processing and analysis, but its flexible pipeline design allows it to process a vast array of data types, including metrics and events. This provides a unified tooling approach for data ingestion and transformation.

Logstash's versatility is a key component in data analysis and visualization workflows, where you can leverage its power to extract the aggregated data. You don't want to search through all your data every time you need to load a dashboard, nor do you want all your raw data stored forever. Preprocessing logs (or any data) with Logstash drastically improves query performance and decreases storage costs.

### Logstash Pros and Cons

One of the main advantages of Logstash is that it can ingest data from any source, transform it, and store it in a centralized location (like Elasticsearch or any database). It also supports a wide range of input, filter, and output plugins, allowing for the processing of diverse data formats and integration with various storage and analytics platforms.

Since Logstash is part of the Elastic Stack, it works seamlessly with Elasticsearch and Kibana, providing you with a complete suite of tools for searching, analyzing, and visualizing log data.

However, Logstash's configuration and pipeline management often seem complex for developers who are not familiar with data pipelines. Additionally, Logstash can be resource-intensive, particularly when processing large volumes of data or when many transformations are applied, which might require a dedicated workload (CPU and memory).

### When to Use Logstash

If you're an Elastic Stack user, then learning Logstash will help you improve dashboard and query performance and decrease storage costs.

However, Logstash has a steep learning curve, and you need to be familiar with both data pipelines and the infrastructure to support those pipelines. Logstash is powerful and flexible, but if you're not an Elastic Stack user, you might want to explore some other options.

## Jaeger

![Jaeger]({{site.images}}{{page.slug}}/jaeger.png)\

[Jaeger](https://www.jaegertracing.io/) is an open source distributed tracing system built by Uber in 2015 and inspired by Google's [Dapper](https://research.google/pubs/dapper-a-large-scale-distributed-systems-tracing-infrastructure/). Uber donated the project to the CNCF in 2017.

Jaeger provides client libraries for a wide range of programming languages, including Go, Java, and Python. These libraries are used to instrument your application, allowing you to record spans when a service processes a request, such as an HTTP request or database call. As the request moves from one service to another, context about the trace is passed along with the request via unique identifiers (like span ID and trace ID). Details like the operation name, duration, and metadata are collected, and the client libraries send this data to Jaeger (the collector). Once the trace data is stored, it can be queried and visualized through the Jaeger UI.

### Jaeger Pros and Cons

One of the advantages of Jaeger is that it provides distributed tracing to monitor and troubleshoot microservices-based distributed systems. This provides visibility into requests as they travel through the system.

Jaeger also helps identify performance bottlenecks and latency issues, making root cause analysis more efficient for distributed systems.

Keep in mind that Jaeger can generate a significant amount of tracing data, which can become a challenge to store and manage. You often have to use sampling traces (*ie* only capturing a small percentage of data) to keep the system manageable in terms of resources and storage.

### When to Use Jaeger

Jaeger is a simple tool that provides the bare minimum to visualize traces. It's easy to integrate into your application and provides a great starting point for trace monitoring. However, its UI is a bit outdated.

## SigNoz

![SigNoz]({{site.images}}{{page.slug}}/signoz.png)\

[SigNoz](https://signoz.io/) is an open source application performance monitoring (APM) and observability platform that was created in 2021 to solve observability fragmentation issues. To properly monitor your system, you typically need a wide range of tools or solutions.

SigNoz applies the [OpenTelemetry](https://opentelemetry.io/) standard to collect data from your system, offering a vendor-neutral way to gather telemetry data such as traces, metrics, and logs. After receiving the data, SigNoz processes and stores it using [ClickHouse](https://clickhouse.com/), an open source columnar database designed for analytics data. SigNoz also provides a web interface where you can visualize and analyze the collected data, allowing you to explore metrics and build dashboards.

The platform also includes an [alerting system](https://signoz.io/docs/userguide/alerts-management/) that allows users to configure alert rules based on metrics or log data so that they'll be notified when those rules are violated.

### SigNoz Pros and Cons

SigNoz provides a unified view of metrics, traces, and logs, offering full-stack observability on a single platform. [SigNoz even promises](https://signoz.io/blog/datadog-vs-prometheus/#a-better-alternative-to-datadog-and-prometheus---signoz) to replace Prometheus, Jaeger, and Logstash altogether.

Because it utilizes ClickHouse for data storage, it's designed for high performance and scalability and is capable of handling large volumes of data efficiently.

### When to Use SigNoz

SigNoz is a promising open source full-stack monitoring platform that has a lot of potential. Since it's a newer tool, it may not have the same level of maturity or as extensive an ecosystem of integrations and community support as more established tools.

## Conclusion

Platform engineering plays a crucial role in standardizing tooling, automation, and best practices to enable software teams to focus on developing, deploying, and operating their applications. In this article, you learned about seven of the most popular platform engineering tools currently on the market.

Picking the right tools can make all the difference when it comes to fostering a streamlined and efficient development lifecycle, enhancing collaboration, and ensuring the scalability and reliability of applications in the long run. While not every tool may be necessary for every organization, being aware of the different tools available and their roles in the industry is crucial.

{% include_html cta/bottom-cta.html %}
