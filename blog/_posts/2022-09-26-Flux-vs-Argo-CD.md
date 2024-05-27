---
title: "Comparison: Flux vs Argo CD"
toc: true
author: David Szakallas

internal-links:
 - Flux
 - Argo CD
 - DevOps
 - GitOps
 - Kubernetes
topic: ci
excerpt: |
    In this article, the author compares two popular GitOps tools, Flux and Argo CD. They discuss various aspects such as reconciliation, source tracking, configuration, Helm support, scaling out, permissions and access control, and more. The article provides insights into the similarities and differences between the two tools, helping readers make an informed decision based on their specific needs.
last_modified_at: 2023-08-17
categories:
  - Deployment
---
**The article compares Flux and Argo CD. Earthly enhances CI/CD security with isolated build environments, unlike Argo CD. [Check it out](https://cloud.earthly.dev/login).**

Since February we have been working on adopting Kubernetes and cloud-native technologies for our cell simulation platform at [Turbine.ai](https://turbine.ai).
Part of my job entailed figuring out how to onboard developers who didn't practice DevOps before.

Companies I've worked at during the past 7 years have all used Kubernetes in some way; and the last one, Turbine.ai, adopted it with my lead. It's been quite a journey for me
since I first encountered the technology in 2015, not long after securing my first full time role as a software engineer at a SaaS startup.
Back in those days, the only cloud vendor that had a managed public K8s offering was Google Cloud Platform (GKE). The tech was fresh and all backend engineers at our company were pretty hyped about migrating to GKE from Heroku.

Later that year, I moved to a role more aligned with my aspirations of working on distributed data processing pipelines with Apache Spark and had little exposure to K8s for
over a year and a half. My path eventually lead back to the container orchestrator when I started working with the machine learning team, running ML workflows in our cloud environment. I recall manually installing and upgrading Apache Airflow (which was the only service I operated) with Helm, all from my development laptop. If the templates rendered the release was good to go.

Fast-forward to my next role where we operated an internal data platform with a more mature development lifecycle. I encountered GitOps for the first time here,
as backend teams were using Argo CD to deploy their applications. It was a radical quality of life improvement over what I'd been practicing previously. Automatic change detection, a nice GUI, alerts on failures and a unified delivery approach for all applications instead of pile of deployment scripts. What's not to love?

Then, I was hired by Turbine.ai, which is a cool biotech startup. In the simulation team, we decided to move our workflow orchestrator to K8s, with expectations that other services will follow suit gradually. However, there was a problem. Backend developers weren't generally practicing DevOps in the company, and even a simple configuration change in a web app deployment often involved a sysadmin in the loop. Moving to K8s can be daunting for such newcomers, as they have to learn how to rebuild their existing applications according to cloud native application development principles
such as [12 factor app](https://12factor.net); learn the fundamentals of K8s alongside with its limitations and idiosynchronicities, pick up new tools and infrastructure components, etc. Moreover, the [cloud native landscape](https://landscape.cncf.io) is vast and rapidly changing, so the best way to do X might be completely different than it was two years ago.

So, long story short, I was afraid that if we didn't offer a smooth developer experience, DevOps would be too much pain to do, which would lead to backlash. GitOps is a method that can largely simplify infrastructure operations for developers, and I managed to convince our team that we should deliver it as part of the milestone marking k8s general availability for the rest of the teams. But what is GitOps and how can it help?

## What Is GitOps?

The term was coined by Weaveworks with the following definition found on [gitops.tech](https://gitops.tech):

> GitOps is a way of implementing Continuous Deployment for cloud native applications. It focuses on a developer-centric experience when operating infrastructure,
by using tools developers are already familiar with, including Git and Continuous Deployment tools. The core idea of GitOps is having a Git repository that always
contains declarative descriptions of the infrastructure currently desired in the production environment and an automated process to [make](/blog/makefiles-on-windows) the production environment
match the described state in the repository. If you want to deploy a new application or update an existing one, you only need to update the repository - the automated
process handles everything else. It's like having cruise control for managing your applications in production.

Making git the single source of truth for cluster state has many benefits. Without completeness:

1. Offers observability and time-travel with the full change history recorded. This simplifies rollbacks and helps developers move with confidence.
1. Enables modifying the application's configuration and source code with a unified approach (even in a single changeset)
1. Simplifies the sharing and reuse of common configuration patterns (eg. with ordinary file editing / templating tools)
1. Enables the adoption of already existing DevOps/CI practices to infrastructure, such as static validation, tests, manual approvals, automated vulnerability scans, etc.
1. Git is the industry standard for source control, everyone should use it already

After this short introduction, now it's time to get on with our topic: comparing Argo CD and Flux, two popular GitOps tools. If you are completely new to GitOps, you'll certainly want to learn more before going ahead. If this is the case, [gitops.tech](https://gitops.tech) is a good place to continue. You can also find plenty of videos on YouTube.

## Introducing the Two Contenders

||<a href="https://fluxcd.io" ><img alt="Flux logo" class="image image--md" src="{{site.images}}{{page.slug}}/flux.png"/> </a>|<a href="https://argoproj.github.io/cd"><img alt="Argo CD logo" class="image image--md" src="{{site.images}}{{page.slug}}/argo.png"/></a>|
|-|-|-|
|initial release|Flux2: Jun 25, 2020<br>Flux (succeeded): Jun 27, 2017|Mar 18, 2018|
|license|![License on GitHub](https://img.shields.io/github/license/fluxcd/flux?style=for-the-badge)|![License on GitHub](https://img.shields.io/github/license/argoproj/argo-cd?style=for-the-badge)|
|maturity|CNCF Incubating Project<br>LF Project<br>[CNCF End User Tech Radar Continuous Delivery, June 2020: Adopt](https://radar.cncf.io/2020-06-continuous-delivery)<br>![GitHub Repo stars](https://img.shields.io/github/stars/fluxcd/flux2?style=for-the-badge) |CNCF Incubating Project<br>LF Project<br>[CNCF End User Tech Radar DevSecOps, September 2021: Adopt](https://radar.cncf.io/2021-09-devsecops)<br>![GitHub Repo stars](https://img.shields.io/github/stars/argoproj/argo-cd?style=for-the-badge)|
|enterprise offering| [Weave GitOps Enterprise](https://www.weave.works/product/gitops-enterprise/) | [Akuity](https://akuity.io) |

Both Flux and Argo CD are very popular with an active community. Flux defines itself as "a set of continuous and progressive delivery solutions for Kubernetes that are open and extensible",
whereas Argo CD is "a declarative, GitOps continuous delivery tool for Kubernetes". Based exclusively on this, one might conclude that there's no clear distinction in their mission statement, however as we dive deeper, we will see that they take a different approach and offer a slightly different feature set.

Argo CD is part of [Argo](https://argoproj.github.io), an umbrella project comprising of multiple productivity focused tools, and is currently incubating under the CNCF. Jesse Suen, creator of the Argo project, [told in Kubernetes Podcast #172](https://kubernetespodcast.com/episode/172-argo/) about the origins of Argo CD: "we needed to build a delivery tool for developer teams (at Intuit - ed) and we heavily focused on things like the user experience and the UI, and GitOps happened to be the mechanism we chose to do the delivery aspect of it". He claims that Argo CD is more developer-experience-centric, whereas Flux is more operator centric. There has been an attempt to merge the two projects, but in the end the Flux team went with a different approach which became the GitOps Toolkit (Flux2).

Flux predates Argo CD and has been around since 2017. I explore the second major version of Flux, which resolves many shortcomings, offers better observability, ease of integrating, composability, and extensibility over the first, which is now in maintenance mode. Flux 2 is comprised of GitOps Toolkit components, k8s operators that reconcile GitOps resources of different kinds. For example, the [source controller](https://fluxcd.io/docs/components/source/) is responsible for source repositories, the helm controller - Helm releases, etc.

This article follows with the comparison of the two frameworks organized by core aspects, such as how they carry out reconciliaton, what tools they support, etc. Bear in mind that I do not attempt a full comparison, for the sake of conciseness and because of my limited research, covering the core functionalities and our use cases. I still believe that it could prove useful for many.

## Kubernetes Cluster Reconciliation

_Reconciliation_ or _synchronization_ (_sync_) is the act of modifying the [cluster](/blog/kube-bench) state to match the description stored in git.

Both platforms support automated sync, i.e they can reconcile the cluster state automatically after a change in GitOps; and manual sync where the action is triggered directly by a human or some external service agent.

<div class="notice--info">
As it was previously mentioned, Flux is componentized. Reconciliation specifics may vary between components. I am using Kustomization in the examples here, but the concepts should work similarly for all sync-able GitOps resources. Caveats will be discussed in detail in the tool-specific sections later.
</div>

## Manual Sync

### Argo CD

With Argo CD, you declaratively specify manual sync by setting `syncPolicy: {}` on the `Application` GitOps resource. This way, Argo CD will detect changes, show them on the UI, etc, but will not take action to reconcile them. Instead, synchronization can be manually triggered on the web UI (which is very straightforward for beginners) or the CLI with [`argocd app sync`](https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd_app_sync/).

### Flux

Using Flux, automatic reconciliation is the norm, but you can opt-out of it by 'suspending' the GitOps resource. This can be done declaratively by setting [`suspend: true`](https://fluxcd.io/docs/components/kustomize/kustomization/#reconciliation).

To do manual sync on-demand on a suspended GitOps resource, set the `reconcile.fluxcd.io/requestedAt` annotation to the current time:

~~~{.bash caption=">_"}
kubectl annotate --field-manager=flux-client-side-apply --overwrite \
kustomization/podinfo reconcile.fluxcd.io/requestedAt="$(date +%s)"
~~~

It's worth noting that running `flux reconcile` against a suspended resource will **not** trigger the reconciliation. Requiring a manual edit to the cluster state for this override was [an intentional design choice](https://github.com/fluxcd/flux2/issues/959). Essentially, on-demand, manual synchronization doesn't have a declarative setting, so Flux doesn't wish to support it via its CLI either.

<div class="notice--info">
Another way to trigger reconciliation is to temporarily `flux resume` the resource. One can argue that this is an imperative action too. The difference is that `suspend` has a declarative setting, so the command effectively edits an in-cluster resource, similarly to e.g `kubectl scale deployment`. Admittedly, this still hurts auditability, since the GitOps state is overridden (at least until the next reconciliation).
</div>

## GitOps Source Tracking

Source tracking controls how changes are detected in the GitOps resource. Both [Argo CD](https://argo-cd.readthedocs.io/en/stable/user-guide/tracking_strategies/#git) and [Flux](https://fluxcd.io/docs/components/source/gitrepositories/#reference) can be configured to track a branch, a tag pattern, or a fixed commit hash in git.

## Cluster Drift Reconciliation (Self Heal)

With source tracking the cluster will follow the desired state in git, but what if someone carries out a manual edit to the cluster? Cluster drift reconciliation (self heal in Argo lingo) entails resyncing the cluster state after a change outside GitOps control, e.g a manual edit with `kubectl`. It can ensure that the cluster adheres to the declared state (eventually). Both Argo CD and Flux support this feature with caveats.

Argo CD provides this as an optional feature, which requires automatic sync to be [enabled](https://github.com/argoproj/argo-cd/issues/4414), and it disables rollbacks.

In Flux, support varies by GitOps resource kind. For Kustomizations, cluster drift is reconciled by default, and the only way to opt-out is to annotate individual resources. On the other hand, Flux does not support this feature for Helm releases at all. (We'll see more on these in the Helm section.) Flux does not distinguish by trigger cause, consequently 'self-heal' won't be carried out if the resource is ignored or the owning GitOps resource is suspended.

## Garbage Collection (Pruning)

_Garbage collection_ controls what happens to resources getting untracked in source control. Both tools take a [similar](https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/#automatic-pruning) [approach](https://fluxcd.io/docs/components/kustomize/kustomization/#garbage-collection), exposing a setting whether they should be deleted or kept. You can also prevent garbage collection of specific resources with an annotation ([Argo](https://argo-cd.readthedocs.io/en/stable/user-guide/sync-options/#no-prune-resources), [Flux](https://fluxcd.io/docs/components/kustomize/kustomization/#garbage-collection)).

## Sync Windows

There are cases when you don't want to allow resource updates, only during a specific maintenance window.

Using Argo CD, this can be achieved with
[sync windows](https://argo-cd.readthedocs.io/en/stable/user-guide/sync_windows/). Using sync windows, automatic or all syncs can be denied except for a certain time frame.

Flux doesn't offer this feature, although a design has already been [proposed](https://github.com/fluxcd/flux2/discussions/870). Currently, it can be achieved with a CronJob that resumes the resource for the duration of the maintenance window.

## Selective Sync

Argo CD supports selective (or partial) syncs, i.e only selected resources get synced. Similarly to an ordinary manual sync, this can be done from the web UI or the CLI. However, selected syncs are not recorded in history and hooks are not run.

In Flux there's no mechanism for this, however if your only use case is to ignore certain resources during reconciliation you can label them ([Flux](https://fluxcd.io/docs/components/kustomize/kustomization/#reconciliation)).

## Hooks

Argo CD sync behavior can be customized with [hooks](https://argo-cd.readthedocs.io/en/stable/user-guide/resource_hooks/). If you are familiar with [Helm hooks](https://helm.sh/docs/topics/charts_hooks/), this is the same thing in essence, e.g allows you to deploy resources in a specific order, run a job (such as a database migration) or trigger a notification after the deployment. Argo CD also understands Helm hooks.

Flux doesn't provide hooks in general, but an individual tool (such as Helm) might provide their own.

## Summary

||Flux|Argo CD|
|-|-|-|
|Automated sync|✅|✅|
|Manual sync|✅|✅|
|Cluster drift reconciliation (Self heal)|⚠️|✅|
|Garbage collection (Pruning)|✅|✅|
|Sync windows|⛔|✅|
|Selective reconciliation|⛔|✅|
|Sync hooks|⚠️ Helm support|✅|

## Kustomize

[Kustomize](https://kustomize.io) is a utility for customizing application configuration in a template-free way, and is a core K8s tool shipping with `kubectl`. Both Argo CD and Flux supports Kustomize.

Argo CD relies on a [tool detection](https://argo-cd.readthedocs.io/en/stable/user-guide/tool_detection/) mechanism,
which checks the directory contents and uses kustomize if it finds a `kustomization.yaml`, `kustomization.yml`, or `Kustomization`.

Bear in mind that tool-specific settings will override the implicit behavior, which can be surprising at first.

~~~{.yaml caption="kustomization.yaml"}
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  ...
spec:
  ...
  source:
    ...

    # Tool -> plain directory
    directory:
      recurse: false
...
~~~

The above snippet will make Argo CD detect a plain directory even in the presence of a `kustomization.yaml`. The same applies to Helm charts.

With Flux, the kustomize-controller operator and its `kustomize.toolkit.fluxcd.io/Kustomization` CRD is used to manage applications configured with Kustomize.

<div class="notice--warning">

Don't mistake `kustomize.toolkit.fluxcd.io/Kustomization` for `kustomize.config.k8s.io/Kustomization`! The first one defines the GitOps resource managed by Flux's kustomize-controller, while the latter is the actual manifest used by kustomize.
</div>

## Configuration

Flux supports defining strategic merge and [JSON](/blog/convert-to-from-json) patches, overriding images and the namespaces in the `kustomize.toolkit.fluxcd.io/Kustomization` [resource](https://fluxcd.io/docs/components/kustomize/kustomization/#override-kustomize-config). Argo CD is less flexible, you have to place your edits in the overlays of your kustomization (with [a few exceptions](https://argo-cd.readthedocs.io/en/stable/user-guide/kustomize/#kustomize)). This might be a problem for certain repo layouts, e.g where kustomizations of an app live in a separate repo which is owned by a different team, and adding a new kustomization there is not preferable / feasible. If you are familiar with Helm, it's not hard to see how this will cause a bigger problem there, but about that later. As an additional customization, Flux supports [variable templating and substitution](https://fluxcd.io/docs/components/kustomize/kustomization/#variable-substitution).

## Summary

||Flux|Argo CD|
|-|-|-|
|Configured with CRDs|✅|✅|
|Inline configuration in the GitOps resource|✅|⛔|
|Variable substitution|[✅](https://fluxcd.io/docs/components/kustomize/kustomization/#variable-substitution)|⛔|
|Automated sync|✅|✅|
|Manual sync|✅|✅|
|Cluster drift reconciliation (Self heal)|✅|✅|
|Garbage collection|✅|✅|

## Helm

[Helm](https://helm.sh/) is a popular package manager for Kubernetes applications.

## Configuration

### Helm `values`

Helm charts can be configured with [values](https://helm.sh/docs/chart_best_practices/values/). With Flux it is possible to provide a [`values` block](https://fluxcd.io/docs/components/helm/helmreleases/#values-overrides) with the desired configuration in the `HelmRelease` resource. (Similarly to Kustomization, where you provide patches). Additionally, the contents can come from ConfigMap or Secret resources deployed in the cluster, which will be merged in the same manner the Helm CLI does it for values files.

Unfortunately, specifying values inline or inside the [cluster](/blog/kube-bench) is not supported by Argo CD. Instead, the files have to be placed alongside the chart in its repo (in case the source is git) or packaged with it (in case a Helm repository is used). This method works for bespoke applications, however it is quite problematic for those off the shelf.

Helm is essentially a package manager for charts. Many off the shelf (OTS) charts are available for open-source projects and can be downloaded from the internet. So there's a misalignment between Helm and Argo CD as an OTS chart cannot possibly contain the configuration for its users, which makes the above values file resolution mechanism useless for anything beyond reading default values. To work around this issue, one can create a wrapper, placed in git, that refers to the original as a [chart dependency](https://helm.sh/docs/topics/charts/#chart-dependencies), and include the custom value files there. Although this is much better than copy-pasting the entire chart, it still results in boilerplate and complicates versioning.

### Kustomize Helm Releases

There are cases when you would like to run Kustomize on Helm's rendered output. For example, when the chart isn't flexible enough and you have to override some configuration not supported by the chart, you could apply it as a patch with Kustomize. Flux supports Kustomize as a [postRenderer](https://fluxcd.io/docs/components/helm/helmreleases/#post-renderers), and can be used for this purpose. Argo CD doesn't have this feature, however you can create a [custom rendering plugin](https://github.com/argoproj/argocd-example-apps/tree/master/plugins/kustomized-helm) for it.

## Source Tracking

Tracking changes in Helm releases with GitOps is more complicated than Kustomize. This is because there's an additional notion of charts, handled differently by Argo CD and Flux.

### Helm Charts in Helm Registries

Helm uses [SemVer](https://semver.org/) for versioning. Helm charts are expected to be immutable, similarly to other software packages. This means, **whenever the template is changed, the chart version must be bumped**.

For charts in Helm registries, both [Flux](https://fluxcd.io/docs/components/helm/helmreleases/#helm-chart-template) and [Argo CD](https://argo-cd.readthedocs.io/en/stable/user-guide/tracking_strategies/#helm) support specifying SemVer ranges, so you may receive updates on new package versions. For example using a range of `>=4.0.0 <5.0.0`, your cluster will automatically receive updates for major version 4.

### Helm Charts in Git

Source tracking of Helm charts works similarly to Kustomizations using both platforms, i.e they can be configured so that reconciliation tracks commits on a branch, a tag pattern, or is fixed to a commit hash.

However, there is a very important property in Flux that you should be aware of. Under the hood, Flux packages the Helm chart contained in the git repository and caches it for internal consumption by HelmReleases. By default (i.e with the `ChartVersion` reconcile strategy), it assumes that **the chart is unchanged unless the version is different in `Chart.yaml`, no matter the git revision**. In other words, **it assumes immutable packages**, even for git sources. This means that if you don't want surprises, you should bump the Chart version on each revision that changes a template.

This behavior can be changed however by setting the [reconcile strategy](https://fluxcd.io/docs/components/helm/api/#helm.toolkit.fluxcd.io/v2beta1.HelmChartTemplateSpec) to `Revision`. This will configure Flux to append build metadata containing the git commit SHA to the version, thus reflecting every commit in a new package version.

<div class="notice--info">
Note that the reconcile strategy only affects the packaging of charts stored in git, changes to GitOps configuration (e.g the `values` block) will be reconciled as usual.
</div>

## Chart Dependencies

Both tools support [chart dependencies](https://helm.sh/docs/topics/charts/#chart-dependencies), which are charts too and may come
from different repositories altogether, so care must be taken to allow only trusted sources. Both platforms provide a way for limiting trust.

You [shouldn't use](https://www.weave.works/blog/profile-layering-for-helm-encourages-self-service-for-kubernetes) chart dependencies to define runtime ordering between applications. As detailed in the referenced article, when Helm installs the charts it renders all the chart objects, sorts all the Kubernetes objects by `Kind`, and then installs each `Kind`. This can prevent collections of charts from installing cleanly, as some charts might depend on previously installed charts with all their `Kind`s running. Ideally, chart dependencies should be used for [libraries](https://helm.sh/docs/topics/library_charts/), as a way to extract common patterns to keep your application charts [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself).

<div class="notice--warning">

## Reconciliation Caveat in Flux

Argo CD provides self healing for Helm releases. Flux [does **not**](https://github.com/fluxcd/flux2/discussions/2812).

This limitation of Flux is problematic enough for apps. However, it is even worse when you try to use Helm for managing GitOps resources (in a multi-level hierarchy), because e.g if someone suspends the reconciliation of an app by adding `suspend: true` to its owning GitOps resource, which is in turn owned by a `HelmRelease`, the drift will never be corrected in the child, and will linger there indefinitely. This can be problematic as entire hierarchies can drift away. Therefore, **my advice is to use Helm only for leaf GitOps resources** (i.e those that directly manage application resources), until drift correction is implemented for Helm.
</div>

## Summary

||Flux|Argo CD|
|-|-|-|
|Configured with CRDs|✅|✅|
|Cluster drift reconciliation (Self heal)|⛔|✅|
|OTS chart support|✅|⚠️ The OTS chart has to be wrapped in a local chart if you wish to override with values outside the chart|
|Replace default values.yaml with custom values.yaml(s) shipped **with** the chart|✅|⚠️ Only for charts hosted in git.|
|Inline values in the GitOps resource|✅|⛔ See [issue on GitHub](https://github.com/argoproj/argo-cd/issues/2789) for workarounds.|
|Upgrade chart stored in git on template change without changing chart version|✅ Using the [`Revision` reconcile strategy](https://fluxcd.io/docs/components/source/helmcharts/#artifact-example).|✅|
|Receive auto-updates from versioned charts using semver version ranges|✅|✅|
|Helm chart dependencies|✅|✅|
|Helm hooks support|✅|✅|
|Rollback on failed Helm upgrade|✅|⚠️ Rollback cannot be performed against an application with automated sync enabled.|
|Apply Kustomizations to Helm releases|✅|⚠️ Via a custom rendering plugin. See [this example](https://github.com/argoproj/argocd-example-apps/tree/master/plugins/kustomized-helm).|

## Scaling Out

GitOps frameworks should provide appropriate abstractions to support adoption in large organizations.

### Recursion

> "What is the tortoise standing on?" "You're very clever, young man, very clever," said the old lady. "But it's turtles all the way down!" -- conversation between scientist and old lady in Stephen Hawking's Brief History of Time

In this context, recursion means applying GitOps techniques to manage GitOps resources. For example, think of a team managing an application having multiple deployments (e.g in different environments). To keep their GitOps resources free of duplication they decide to extract common configuration with the use of kustomize patches. A straightforward way to do this is to create a parent GitOps resource that uses Kustomize to generate the inferior GitOps configurations.

In Argo CD, this can be achieved with the [App of Apps pattern](https://medium.com/dzerolabs/turbocharge-argocd-with-app-of-apps-pattern-and-kustomized-helm-ea4993190e7c), which lets us define an `Application` resource that contains child `Application`s (and `AppProject`s). Argo CD watches the root application as well as synchronizes any application it generates. (By the way, the referenced article also points out how to do Kustomized Helm.) The child apps need not reside in the same cluster as their parent. By using the Apps of Apps pattern we can use the same techniques for generating GitOps resources as app resources, which makes it feasible to template or kustomize `Application`s, consequently, avoid duplication.

Similarly in Flux, we can define GitOps resources recursively. Having dedicated CRDs for sources, sync-able resources, notifications, makes it even more flexible than Argo CD.

## Dependency Ordering

Applications depend on each other, and we should be able to express that to some degree. As initial approach, one can distinguish between infrastructure applications providing core functionalities such as ingress, secret management,
RBAC, cert management, service mesh, etc; and product applications. For example if you use the popular service mesh [linkerd](https://linkerd.io/), it must be in place before any applications come up, because it injects sidecars into application pods starting up. Having a way to stall the installation of product applications until the infra is ready spares us the chore of dealing with such race-conditions and other problems.

With Flux's [`dependsOn`](https://fluxcd.io/docs/components/kustomize/kustomization/#kustomization-dependencies), we can prevent an application to be synced unless its dependencies are in the Ready state, in other words, to guarantee installation ordering. Unfortunately, this feature is missing from Argo CD [but it is proposed](https://github.com/argoproj/argo-cd/issues/7437).

<div class="notice--warning">
Note that currently Flux doesn't allow a Kustomization to depend on a HelmRelease and vice versa.
</div>

## Permissions and Access Control

It makes sense to organize applications based on ownership to simplify permission setup. VCS based permission management can be put into place, e.g.
[CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) can be used to control write permissions based on globs within a [monorepo](/blog/monorepo-vs-polyrepo).
A higher degree of confidentiality can be achieved if each team gets their own repo, as even read can be forbidden for outsiders. The GitOps platform can offer additional features for access control.

With Argo CD, the `AppProject` is used to specify that an application belongs to a [project](https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/#projects), which makes use of Argo CD's [own user management](https://argo-cd.readthedocs.io/en/stable/operator-manual/user-management/) and permission system; enabling us to allow/deny

- Access to sources.
- Deploying resource kinds.
- Access for users
- Deploying to target clusters.

Flux doesn't offer its own user management like Argo CD does. Instead, platform administrators should use Kubernetes RBAC and policy driven validation to establish security. Flux has a multi-component design, and integrates with many other systems. Having different components and CRDs such as git repositories, charts, notifications, etc, helps separate concerns, thus facilitates setting up fine-grained policies. Platform admins can [enforce service account impersonation](https://fluxcd.io/docs/components/helm/helmreleases/#role-based-access-control) to minimize privileges.

## Everything Is A CRD

> Everything is on cob! The whole planet is on a cob! -- Rick Sanchez, Rick, and Morty - S02E10 The Wedding Squanchers

While Argo CD offers only two major CRDs, Application, and AppProject, Flux has separate CRDs for each concept such as Kustomization (kustomize-controller), HelmRelease, HelmChart (helm-controller), HelmRepository, GitRepository (source-controller), Alert, Event (notification-controller), etc. This allows for a cleaner design, which precipitates in details such as:

- Using Flux, notification configuration is [placed in CRDs](https://fluxcd.io/docs/components/notification/), whereas for Argo CD, it is [placed in ConfigMaps](https://argocd-notifications.readthedocs.io/en/stable/triggers/) in the Argo CD deployment's namespace. Access to that namespace is often restricted to the platform administrator.
- Using Flux, private repository credentials stored in a Secret should be referenced in [Flux's GitRepository](https://fluxcd.io/docs/components/source/gitrepositories/#secret-reference), whereas for Argo CD, they should be [placed in Secrets](https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/#repository-credentials) in the Argo CD deployment's namespace. Reusing the same credential for multiple repos requires a rather [strange technique](https://argo-cd.readthedocs.io/en/stable/user-guide/private-repositories/#credential-templates). Not only Flux's method is much more conventional and flexible, access to Argo CD's namespace is often restricted to the platform administrator.
- Analogously to repository credentials, cluster credentials (in a multi-cluster scenario) are set up [directly in the CRDs](https://fluxcd.io/docs/components/kustomize/kustomization/#remote-clusters--cluster-api) in Flux, whereas for Argo CD, its a [Secret in its own namespace](https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/#clusters)

## Polyrepo Support

Both platforms support multiple git repos.

## Multi-Cluster Deployment

Both platforms support syncing remote cluster targets.

Argo CD offers a dedicated ApplicationSet resource for templating Applications targeting multiple clusters. With Flux, you
can use conventional tooling (such as kustomize overlays) to [generate GitOps manifests](https://github.com/fluxcd/flux2-kustomize-helm-example) for the separate targets.

## Summary

||Flux|Argo CD|
|-|-|-|
|Recursion|✅|✅|
|Own user management system|⛔|✅|
|Own permission system|⛔|✅|
|Installation ordering|⚠️|⛔|
|Everything is a CRD|✅|⛔|
|Polyrepo support|✅|✅|
|Multi-cluster support|✅|✅|

## Conclusion

In this article, we explored GitOps frameworks, focusing mainly on core capabilities, leaving out features like multi-tenancy, RBAC, notifications, image automation, etc. We found that Argo CD and Flux are comparably efficient, with each having its pros and cons. After careful deliberation, at Turbine.ai we chose Flux due to its superior support for OTS Helm charts and operational simplicity.

Also as you prioritize your organization's specific needs when choosing between these platforms, you might also want to consider supercharging your build automation. If that's the case, give [Earthly](https://cloud.earthly.dev/login) a try!

It could be a valuable addition to your GitOps practices.

{% include_html cta/bottom-cta.html %}
