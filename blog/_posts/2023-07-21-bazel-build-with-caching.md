---
title: "Using a Cache to Improve Bazel Build Times"
categories:
  - Tutorials
toc: true
author: Rose Chege

internal-links:
 - using a cache
 - improve bazel build times
 - bazel build times
 - cache to improve bazel build times
excerpt: |
    Learn how to improve your Bazel build times by using a cache. This article explains the benefits of caching, the different types of caches, and how to set up a local or remote cache with Bazel.
last_modified_at: 2023-07-28
---
**Explore the intricacies of Bazel caching options in this article. Learn how Earthly's built-in caching can boost your build efficiency and enhance Bazel's capabilities. [Learn more](/).**



[Bazel](https://bazel.build) is a tool that helps you automate the process of building and testing. For instance, with Bazel, you can automate the process of creating executables for [monorepo build systems](https://earthly.dev/blog/bazel-build/).

One notable feature of Bazel is the ability to use a cache. A cache speeds up the build process and reduces build times, especially for large projects with many dependencies. Moreover, a Bazel cache stores the build artifacts from previous builds, which means you don't have to rebuild files that have already been built since they're available in the cache.

A Bazel cache can either be [local](https://github.com/bazelbuild/bazel/issues/5139) or [remote (shared)](https://bazel.build/remote/caching). A local cache is stored on the same computer where Bazel is running. It improves the performance of Bazel by avoiding the need to rebuild artifacts that haven't changed since the last build on that machine.

A remote Bazel cache is stored on a separate machine, typically accessed over a network. This approach improves Bazel's performance by allowing multiple computers to share the same build artifacts, which means you don't have to rebuild them on each machine. This is important if multiple machines are used to build the same application but the cache is too large to fit on a single computer.

In this article, you'll learn how to set up a local and a remote cache to improve Bazel build performance. You'll also understand the pros and cons of caching information.

## Why You Need Bazel Caching

![Graphics]({{site.images}}{{page.slug}}/not.png)\

As mentioned, a cache speeds up the build process and reduces build times. By storing build artifacts in a cache, Bazel ensures that the same artifacts are used each time a build is executed, even if the environment or dependencies change. This helps prevent build failures or inconsistencies due to changes in the build environment.

For example, if you change a small part of your project, Bazel uses the cached results from previous builds and quickly rebuilds only the sections of your project affected by the change.

Bazel caching is essential to using Bazel efficiently because it significantly improves the performance and reliability of Bazel builds.

### Bazel Cache Granularity

Bazel uses two types of cache: local and remote. The local cache is stored on your machine and speeds up incremental builds by reusing previously built artifacts. It includes disk cache, which stores build outputs on disk, and memory cache, which stores build outputs in memory for faster access. In comparison, the remote cache is a service that stores and retrieves build outputs across multiple machines, allowing teams to share build artifacts efficiently.

That being said, neither local nor remote cache should be confused with cache granularity.

Cache granularity in Bazel refers to the level at which the cache works to store and retrieve build outputs. Bazel caching operates at a highly granular level, typically targeting individual components or modules within a build.

At the most granular level, Bazel uses [action-level caching](https://sluongng.hashnode.dev/bazel-caching-explained-pt-1-how-bazel-works). This means that each individual build action, such as compilation, linkage, or code generation, has its own cache entry. Bazel computes a hash of the action's inputs, which includes the command line, environment variables, and input files. If the cache contains an entry with the same hash, Bazel will reuse the cached output, avoiding the need to re-execute the action. This fine-grained caching enables fast partial rebuilds, as only the affected actions need to be re-executed.

In the case of remote caching, this granularity allows Bazel to reuse build outputs from other users' builds or previous builds, saving time and resources by avoiding repetitive tasks. When Bazel executes a build, it traverses the action graph and determines which actions need to be executed, creating spawns with strategies to utilize remote caching or remote execution. By working at such a granular level, Bazel caching enables efficient sharing of build outputs and optimizes the build process.

## Comparing Local vs. Shared (Remote) Caching with Bazel

![Graphics]({{site.images}}{{page.slug}}/compare.png)\

As discussed earlier, a Bazel build cache is stored either locally or remotely. Each of these approaches has its advantages and disadvantages, which you'll review below.

### Local Caching

The major advantages of using local caching include the following:

- **Faster access to build artifacts**: Your artifacts are stored on your local computer. This means that they can be accessed more quickly and do not need to be transferred over the network.
- **Increased reliability**: There's no need for an internet connection to access build artifacts.
- **Local caching is more secure**: Because build artifacts are only stored on the local machine, you can't access them over the network.

However, local caching can create the following limitations:

- **Limited storage space**: Local caching takes up more disk space on the local computer. This is problematic if the computer has limited storage capacity, especially if you're building large projects.
- **Sharing limitations**: With local caching, build artifacts are only stored locally. You can't share them with other team members or across different computers. This is a huge setback when multiple team members work on the same Bazel built project.
- **Limited compute resources**: as with storage, locally available computing resources are limited, which can be a problem in large projects.

### Shared (Remote) Caching

The major advantages of using shared caching include the following:

- **Unlimited storage space**: Build artifacts are stored on a remote server, meaning storage space is flexible and scaled based on the team's demand.
- **Increased efficiency**: Build artifacts are shareable across different team members, improving collaboration and reducing build times.
- **Scalability**: in the cloud, computing resources can be increased or decreased in real time, which provides great flexibility and scalability.

However, there are some potential drawbacks to using remote caching, including the following:

- **Network latency**: With shared caching, build artifacts are stored on a remote server. Depending on latency, this can result in slower times to access build artifacts.
- **Requires additional security levels**: Because build artifacts are accessible over the network, they're vulnerable to security threats.
- **Requires a stable internet connection.**

Overall, the decision to use local or shared caching with Bazel will depend on your project's specific needs and requirements.

## How to Set Up a Shared Build Cache Using Bazel

Now that you know why you need Bazel caches and the difference between shared and local caching, let's discuss different approaches to setting up a Bazel remote cache and storing build artifacts and outputs in a centralized location.

### Remote Cache With a Google Cloud Storage Bucket

One option to set up a remote cache is to use a [Google Cloud Storage bucket](https://cloud.google.com/storage/docs/creating-buckets), a storage location in the cloud. By using a GCP bucket as a remote cache, Bazel will help improve the performance of your builds and make it easier to share artifacts among team members.

To use a GCP bucket as a remote cache for Bazel, you'll need to follow these steps:

1. Create a GCP bucket to use as the remote cache. This is done using the [Google Cloud console](https://cloud.google.com/storage/docs/cloud-console), the [gsutil command line tool](https://cloud.google.com/storage/docs/gsutil), or [gcloud storage buckets](https://cloud.google.com/sdk/gcloud/reference/storage/buckets).
2. Set up the credentials for accessing the GCP bucket. You should set up a service account and grant permission access to the bucket.
3. Configure Bazel to use the GCP bucket as the remote cache. You can achieve this by adding the following lines to your `.bazelrc` file:

~~~{ caption=".bazelrc"}
build --remote_cache=https://storage.googleapis.com/your-bucket-name
build --google_credentials=/path/to/your/credentials.json
~~~

Now, Bazel will use the GCP bucket as a remote cache when building your project.

### Remote Cache Using Amazon S3

Like a GCP bucket, an [Amazon Simple Storage Service (S3) bucket](https://aws.amazon.com/s3/) works as a remote cache for Bazel. To use an S3 bucket, follow these steps:

1. Create an S3 bucket to use as the remote cache. To do so, you can use the [Amazon S3 console](https://docs.vmware.com/en/VMware-Carbon-Black-Cloud/services/carbon-black-cloud-user-guide/GUID-4DEF3EF2-9415-42A7-82F0-34B41A8035F0.html), the [Amazon Web Services (AWS) CLI](https://docs.aws.amazon.com/cli/latest/reference/s3api/create-bucket.html), or the [Amazon S3 API](https://docs.aws.amazon.com/AmazonS3/latest/API/Welcome.html).
2. Set up the credentials for accessing the Amazon S3 bucket. Create an AWS Identity and Access Management (IAM) user and grant it the necessary permissions to access the bucket.
3. Configure Bazel to use the S3 bucket as the remote cache by adding the following lines to your `.bazelrc` file:

~~~{ caption=".bazelrc"}
build --remote_cache=https://s3.amazonaws.com/[BUCKET_NAME]
build --remote_instance_name=[INSTANCE_NAME]
build --remote_upload_local_results=true
~~~

Use the Bazel build and test commands as usual, and Bazel will automatically cache the build outputs or retrieve build artifacts from the S3 bucket.

### Remote Cache Using Remote Build Execution

Bazel supports using [remote build execution (RBE)](https://bazel.build/remote/rbe) to build and test applications remotely. This is useful when building and testing on multiple machines or when using a remote cache to speed up build times. To use RBE with a remote cache, you need to set up a remote execution instance and configure Bazel to use it. You can do this by adding the following lines to your `.bazelrc` file:

~~~{ caption=".bazelrc"}
build --remote_executor=<host>:<port>
build --remote_cache=<host>:<port>
~~~

Replace `<host>` and `<port>` with the hostname and port of your remote execution instance. Then use the build and test commands as usual, and Bazel will automatically use the remote cache and remote execution instance for your builds.

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

It's possible to use Bazel without a cache; however, this may result in slower build times.
To disable the Bazel cache, use the `no-cache` or `no-remote-cache` flags. This will prevent Bazel from using the in-memory or remote cache, respectively.

Following is an example of how to use the `no-cache` when on a specific target:

~~~{ caption=".bazelrc"}
…
my_test(
  name = "my_test",
  tags = ["no-cache"],
)
…
~~~

And here is an example of how to use the `no-remote-cache` on a specific target:

~~~{ caption=".bazelrc"}
…
java_library(
    name = "target",
    tags = ["no-remote-cache"],
)
…
~~~

Disabling the Bazel cache can significantly increase your build and test time as all files must be rebuilt again by Bazel, even if they've already been built and are stored in the cache.

You can use the cache unless there is a specific reason not to, such as the following:

- A cache contains outdated or invalid data, and you want to force Bazel to rebuild all dependencies from scratch.
- A rebuild of all necessary components is required based on changes to build configurations or dependencies that must be fully reflected in the build.
- For debugging reasons, you need the full output of the build process.

## Conclusion

Using remote cache for Bazel significantly improves your builds' performance and reliability, making storing and accessing build artifacts from multiple machines and locations easy.

In this guide, you learned about the concept of Bazel cache builds. After reading, you should be able to set up the local and remote cache to improve Bazel build performance. For more information, check out [this guide for any command line reference](https://bazel.build/reference/command-line-reference) you may need.

{% include_html cta/bottom-cta.html %}
