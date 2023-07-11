---
title: "Using a Cache to Improve Bazel Build Times"
categories:
  - Tutorials
toc: true
author: Rose Chege
editor: Bala Priya C

internal-links:
 - Cache
 - Bazel
 - Local Caching
 - Remote Caching
excerpt: Learn how to improve your Bazel build times by using a cache. This article explains the benefits of caching, the different types of caches, and how to set up a local or remote cache with Bazel.
---

[Bazel](https://bazel.build) is a tool that helps you automate the process of building and testing. For instance, with Bazel, you can automate the process of creating executables for [monorepo build systems](https://earthly.dev/blog/bazel-build/).

One notable feature of Bazel is the ability to use a cache. A cache speeds up the build process and reduces build times, especially for large projects with many dependencies. Moreover, a [Bazel](/blog/monorepo-with-bazel) cache stores the build artifacts from previous builds, which means you don't have to rebuild files that have already been built since they're available in the cache.

A Bazel cache can either be [local](https://github.com/bazelbuild/bazel/issues/5139) or [remote (shared)](https://bazel.build/remote/caching). A local cache is stored on the same computer where Bazel is running. It improves the performance of Bazel by avoiding the need to rebuild artifacts that haven't changed since the last build on that machine.

A remote Bazel cache is stored on a separate machine, typically accessed over a network. This approach improves Bazel's performance by allowing multiple computers to share the same build artifacts, which means you don't have to rebuild them on each machine. This is important if multiple machines are used to build the same application but the cache is too large to fit on a single computer.

In this article, you'll learn how to set up a local and a remote cache to improve Bazel build performance. You'll also understand the pros and cons of caching information.

## Why You Need Bazel Caching

![Graphics]({{site.images}}{{page.slug}}/not.png)\

As mentioned, a cache speeds up the build process and reduces build times. By storing build artifacts in a cache, Bazel ensures that the same artifacts are used each time a build is executed, even if the environment or dependencies change. This helps prevent build failures or inconsistencies due to changes in the build environment.

For example, if you change a small part of your project, Bazel uses the cached results from previous builds and quickly rebuilds only the sections of your project affected by the change.

Bazel caching is essential to using Bazel efficiently because it significantly improves the performance and reliability of Bazel builds. However, it's always best to find a balance between cache builds since cache granularity lets you set the units of data stored in a cache.

In the next section, you'll learn about the optimal cache granularity you need, which depends on the workload you're running.

### Bazel Cache Granularity

[Cache granularity](https://docs.bazel.build/versions/0.19.1/migrate-maven.html#3-create-more-build-files-optional) refers to the level of detail at which the cache stores build outputs. It determines how Bazel breaks down the build process into individual steps and how it stores the results of each step in the cache.

Bazel supports three levels of granularity for the cache:

1. **File granularity (fine-grained)**: At this level, the cache stores the outputs of individual source files. If a source file is modified, only the outputs of that file will be invalidated in the cache, and Bazel will rebuild it.
2. **Directory granularity (medium-grained)**: At the directory level, the cache stores the outputs of all files in a directory. If any file in a directory changes, the cached outputs of all files in that directory are invalidated, and all files will be rebuilt.
3. **Package granularity (coarser-grained)**: At this level, the cache stores the outputs of all files in a package. If any file in a package is modified, the outputs of all files in that package are invalidated in the cache, and consequently, all the files in the package will be rebuilt.

Bazel uses a *fine-grained cache* by default. This means it stores individual action results (such as compiling a single file) in the cache, avoiding repeating actions. You can choose to use the coarser-grained cache, which stores the results of larger groups of actions together. This can be useful when dealing with large builds that have many actions because it reduces the amount of data stored in the cache and improves [cache hit rates](https://bazel.build/remote/cache-remote).

To configure the granularity of the cache, add the `--cache_granularity` flag in your `.bazelrc` file. Valid values for this flag include `fine`, `medium`, and `binary`, which correspond to the `fine-grained`, `medium-grained`, and `coarser-grained` cache levels, respectively.

For example, to use a `medium-grained` cache, add the following to your `.bazelrc` file:

~~~{ caption=".bazelrc"}
build --cache_granularity=medium
~~~

## Comparing Local vs. Shared (Remote) Caching with Bazel

![Graphics]({{site.images}}{{page.slug}}/compare.png)\

As discussed earlier, a Bazel build cache is stored either locally or remotely. Each of these approaches has its advantages and disadvantages, which you'll review in more detail later.

### Local Caching

The major advantages of using local caching include the following:

- **Faster access to build artifacts**: Your artifacts are stored on your local computer. This means that they can be accessed more quickly and do not need to be transferred over the network.
- **Increased reliability**: There's no need for an internet connection to access build artifacts.
- **Local caching is more secure**: Because build artifacts are only stored on the local machine, you can't access them over the network.

However, local caching has the following limitations:

- **Limited storage space**: Local caching takes up more disk space on the local computer. This is problematic if the computer has limited storage capacity, especially if you're building large projects.
- **Sharing limitations**: With local caching, build artifacts are only stored locally. You can't share them with other team members or across different computers. This is a huge setback when multiple team members work on the same Bazel built project.

### Shared (Remote) Caching

The major advantages of using shared caching include the following:

- **Unlimited storage space**: Build artifacts are stored on a remote server, meaning storage space is flexible and scaled based on the team's demand.
- **Increased efficiency**: Build artifacts are shareable across different team members, improving collaboration and reducing build times.

However, there are some potential drawbacks to using remote caching, including the following:

- **Slower access to build artifacts**: With shared caching, build artifacts are stored on a remote server and accessed more slowly than when stored locally.
- **Requires additional security levels**: Because build artifacts are accessible over the network, they're vulnerable to security threats.
- **Requires a stable internet connection.**

Overall, the decision to use local or shared caching with Bazel will depend on your project's specific needs and requirements.

## How to Set Up a Shared Build Cache Using Bazel

Now that you know why you need [Bazel](/blog/monorepo-with-bazel) caches and what the difference between shared and local caching is, let's discuss different approaches to setting up a [Bazel shared cache](https://coggle.it/diagram/XX4osbstyM-W9fld/t/bazel-remote-caching) and storing build artifacts and outputs in a centralized location.

### Remote Cache With a Google Cloud Storage Bucket

One option to set up a remote cache is to use a [Google Cloud Storage bucket](https://cloud.google.com/storage/docs/creating-buckets), a storage location in the cloud. By using a GCP bucket as a remote cache, Bazel will help improve the performance of your builds and make it easier to share artifacts among team members.

To use a GCP bucket as a remote cache for Bazel, you'll need to follow these steps:

1. Create a GCP bucket to use as the remote cache. This is done using the [Google Cloud console](https://cloud.google.com/storage/docs/cloud-console), the [gsutil command line tool](https://cloud.google.com/storage/docs/gsutil), or [gcloud storage buckets](https://cloud.google.com/sdk/gcloud/reference/storage/buckets).
2. Set up the credentials for accessing the GCP bucket. You should set up a service account and grant permission access to the bucket.
3. Configure Bazel to use the GCP bucket as the remote cache. You can achieve this by adding the following lines to your `.bazelrc` file:

~~~{ caption=".bazelrc"}
build --remote_cache=gs://[BUCKET_NAME]
build --google_credentials=[PATH_TO_CREDENTIALS_FILE]
~~~

Alternatively, you can use the `--remote_cache` flag in your Bazel commands to specify the URL of your GCP bucket as the remote cache location.

For example, to build a Bazel target using a GCP bucket as the remote cache, use the following command:

~~~{.bash caption=">_"}
bazel build --remote_cache=gs://my-gcp-bucket/path/to/cache my_target
~~~

This command will use the GCP bucket `my-gcp-bucket` at the specified path as the remote cache for the build. Then Bazel will store the build artifacts in the cache and retrieve them from the cache as needed.

### Remote Cache Using Amazon S3

Like a GCP bucket, an [Amazon Simple Storage Service (S3) bucket](https://aws.amazon.com/s3/) works as a remote cache for Bazel. To use an S3 bucket, follow these steps:

1. Create an S3 bucket to use as the remote cache. To do so, you can use the [Amazon S3 console](https://docs.vmware.com/en/VMware-Carbon-Black-Cloud/services/carbon-black-cloud-user-guide/GUID-4DEF3EF2-9415-42A7-82F0-34B41A8035F0.html), the [Amazon Web Services (AWS) CLI](https://docs.aws.amazon.com/cli/latest/reference/s3api/create-bucket.html), or the [Amazon S3 API](https://docs.aws.amazon.com/AmazonS3/latest/API/Welcome.html).
2. Set up the credentials for accessing the Amazon S3 bucket. Create an AWS Identity and Access Management (IAM) user and grant it the necessary permissions to access the bucket.
3. Configure Bazel to use the S3 bucket as the remote cache by adding the following lines to your `.bazelrc` file:

~~~{ caption=".bazelrc"}
build --remote_cache=https://s3.amazonaws.com/[BUCKET_NAME]
build --remote_instance_name=[INSTANCE_NAME]
~~~

Use the Bazel build and test commands as usual, and Bazel will automatically cache the build outputs or retrieve build artifacts from the S3 bucket.

### Remote Cache Using Remote Build Execution

Bazel supports using [remote build execution (RBE)](https://bazel.build/remote/rbe) to build and test applications remotely. This is useful when building and testing on multiple machines or when using a remote cache to speed up build times. To use RBE with a remote cache, you need to set up a remote execution instance and configure Bazel to use it. You can do this by adding the following lines to your `.bazelrc` file:

~~~{ caption=".bazelrc"}
build --remote_executor=<host>:<port>
build --remote_cache=<host>:<port>
~~~

Replace `<host>` and `<port>` with the hostname and port of your remote execution instance, respectively. Then use the build and test commands as usual, and Bazel will automatically use the remote cache and remote execution instance for your builds.

Using RBE and a remote cache extends build times because build output needs to be transmitted over the network to the remote cache. However, it significantly speeds up incremental builds since the remote cache saves the outcomes of earlier builds rather than recreating them.

### Clearing the Cache

To clear the Bazel cache, you can use the `bazel clean` command with the `--expunge` flag. This will remove all files from the Bazel cache for both the build and test outputs. Here is an example of how to clear the Bazel cache:

~~~{.bash caption=">_"}
bazel clean --expunge
~~~

<div class="notice--big--primary">
Using `--expunge` permanently deletes the files in the Bazel cache. You cannot recover them. Use this command only if you want to delete all the files in the Bazel cache.
</div>

Alternatively, you can use the `bazel clean` command without the `--expunge` flag to remove only the build and test outputs from the Bazel cache. This command won't delete the build and test logs. You can then recover the files in the cache by running the Bazel build or test commands again. Here's an example of how to use the `clean` command without the `--expunge` flag:

~~~{.bash caption=">_"}
bazel clean
~~~

### Disabling the Cache

To disable the [Bazel](/blog/monorepo-with-bazel) cache, use the `--noinmemory_cache` or `--noremote_cache` flags along the [Bazel](/blog/bazel-build) commands. This will prevent Bazel from using the in-memory or remote cache, respectively.

Following is an example of how to use the `--noinmemory_cache` flag when running the `bazel build` command:

~~~{.bash caption=">_"}
bazel build --noinmemory_cache [TARGETS]
~~~

And here is an example of how to use the `--noremote_cache` flag when running the `bazel test` command:

~~~{.bash caption=">_"}
bazel test --noremote_cache [TARGETS]
~~~

Disabling the Bazel cache can significantly increase your build and test times. However, all files must be rebuilt again by Bazel, even if they've already been built and are stored in the cache.

### Testing Without the Cache

It's possible to use [Bazel](/blog/bazel-build) without a cache; however, this may result in slower build times. To use Bazel without a cache, you need to specify the `--nocache` flag when running the Bazel commands. Here are examples:

~~~{.bash caption=">_"}
bazel build --nocache //path/to/package:target
~~~

~~~{.bash caption=">_"}
bazel test --nocache //path/to/package:target
~~~

Remember that using the `--nocache` causes Bazel to rebuild the necessary dependencies from scratch. You can use the cache unless there is a specific reason not to, such as the following:

- A cache contains outdated or invalid data, and you want to force Bazel to rebuild all dependencies from scratch.
- A rebuild of all necessary components is required based on changes to build configurations or dependencies that must be fully reflected in the build.
- For debugging reasons, you need the full output of the build process.

## Conclusion

Using remote cache for Bazel significantly improves your builds' performance and reliability, making storing and accessing build artifacts from multiple machines and locations easy.

In this guide, you learned about the concept of [Bazel](/blog/bazel-build) cache builds. After reading, you should be able to set up the local and remote cache to improve Bazel build performance. For more information, check out [this guide for any command-line reference](https://bazel.build/reference/command-line-reference) you may need.

{% include_html cta/bottom-cta.html %}
