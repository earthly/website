---
title: "Everything You Need to Know about Bazel Query"
categories:
  - Tutorials
toc: true
author: Rose Chege

internal-links:
 - Bazel
 - Query
 - Graph
 - Optimize
excerpt: |
    Learn all you need to know about Bazel queries in this article. Discover how Bazel queries can help you analyze your project's build graph, optimize build performance, and debug builds.
last_modified_at: 2023-07-19
---
**The article explains the advantages of using Bazel queries. Earthly enhances Bazel's dependency management with robust build automation. [Check it out](/).**

[Bazel](https://earthly.dev/blog/bazel-build/) is a build system that streamlines repetitive tasks to ensure build consistency. Thanks to features such as scalability, multilanguage platform support, [caching](https://earthly.dev/blog/bazel-build-with-caching/), remote executions, and Bazel queries, developers can use Bazel to reproduce deterministic builds and tests for their projects.

More specifically, Bazel queries simplify the process of searching and analyzing the build graph by examining project build files and dependencies. This helps developers gain a better understanding of their dependencies, optimize build performance, and debug builds.

This article will help experienced developers learn all they need to know about Bazel queries. To follow along with the use cases used in this tutorial, you need to have [Bazelisk](https://bazel.build/install) installed.

## Why You Need Bazel Queries

As your build expands and becomes more complex, you'll likely need interdependent components to maintain and update your codebases. However, ensuring every dependency is working as expected is challenging. Fortunately, Bazel queries can help by allowing you to analyze your `BUILD` files and dependencies, enhancing your understanding of the dependencies within a project's entire graph.

For instance, a project built with Bazel has all kinds of different elements (*ie* packages and targets). With a large codebase, keeping track of all these elements is difficult. However, Bazel queries check each element in your project structure and locate the necessary information. For example, if you want to change a shared library, you can trace the impacted project segment, and Bazel queries can find all the targets that depend on the library before you make any changes.

Bazel queries use dependency analysis to isolate [direct](https://bazel.build/concepts/dependencies) and [transitive](https://bazel.build/basics/dependencies) dependencies. Dependency analysis helps identify any deprecated and insecure dependencies, as well as direct dependencies with various transitive dependencies. This improves build performance by identifying slow targets and dependencies.

Looking through the query results can help you identify slow or redundant dependencies and possibly replace them with better, more appropriate dependencies to help improve build performance and reduce binary size. Additionally, Bazel queries let you query test suites. You can identify tests for a target and its dependents to ensure all relevant tests are run when making changes to your code.

## How Bazel Queries Work

![How]({{site.images}}{{page.slug}}/how.png)\

Bazel queries are composed using a specialized query language that lets you filter specific target dependencies based on unique criteria. The query language contains keywords, operators, and filters that can be used to execute the queries as domain-specific languages (DSL), typically with file paths, labels, and build attributes serving as the primary components.

### The Bazel Query Syntax

For Bazel to execute your DSL, it uses a query engine to evaluate the query expressions and generate the results. For instance, if you want to [find the dependencies](https://bazel.build/query/language#deps) of a given rule, you need to define the following query:

~~~{.bash caption=">_"}
bazel query "deps(//path/to:your_rule)"
~~~

The output of this query includes all direct and transitive dependencies of the target. If you have a target `//test-app`, your query syntax would look like this:

~~~{.bash caption=">_"}
bazel query "deps(//test-app)"
~~~

This basic example lets you find all the targets you need to build `//test-app`. However, its output also includes dependencies the `//test-app` target inherits. This means if another target, `//test-app/test-app2`, depends on `//test-app`, which in turn depends on `//test-app/test-app-dep`, the output of the query would include all three targets as dependencies of the main `//test-app` target:

~~~{.bash caption=">_"}
bazel query "deps(//test-app)"
//test-app/test-app2
//test-app/test-app-dep
~~~

### Query Operators, Functions, and Keywords

Bazel queries find the dependencies of a rule; identify packages, rules, and targets; and analyze file dependencies. Because of this, its syntax supports query operators, functions, and keywords to ensure you can run all the aforementioned operations. For instance, the following query uses the `kind` function to filter targets whose name ends with packages, rules, and targets in the dependencies list of the target `runner`:

~~~{.bash caption=">_"}
bazel query "kind("package", deps(":runner")) \
union kind("rule", deps(:runner)) union kind("target", deps(":runner))"
~~~

To find all `BUILD` files that are required to build a given Bazel rule, the following syntax uses a `buildfiles` function based on the Bazel package location:

~~~{.bash caption=">_"}
bazel query "buildfiles(//path/to:your_rule)" --output build
~~~

## Overview of Bazel Query Language Concepts

[Bazel Query Language (BQL)](https://docs-staging.bazel.build/5813/versions/3.7.0/query.html) follows a set of concepts to query your build graph. A build graph is a collection of target dependencies that represents the dependencies between the targets. BQL concepts allow you to write expressions that evaluate a partially ordered set of [targets or a graph of targets](https://bazel.build/extending/aspects) as the only data type.

In the case of the set, the [partial order of the targets](https://bazel.build/query/language#language-concepts) isn't important. The order of the elements in a query set doesn't affect its meaning. Instead, you need to focus on the partial order of targets in a graph.

Take a look at some key concepts you should keep in mind when working with BQL to write meaningful and optimized expressions:

### Implicit Dependencies

[Implicit dependencies](https://bazel.build/query/language#implicit-dependencies) are implicitly defined in `BUILD` files and are automatically generated. By default, Bazel returns all implicit dependencies to provide a complete list of dependencies required during build times. This means that executing a Bazel query takes into account both the explicit and implicit dependencies of a rule.

A large list of implicit dependencies can sometimes add an unexpected and unreasonable overhead in build times and performance. However, Bazel helps you disable implicit dependencies using the `--[no]implicit_deps` flag to only return direct/explicit dependencies listed in your `BUILD` file:

~~~{.bash caption=">_"}
bazel query --noimplicit_deps 'deps(//app:test_app)'
~~~

Keep in mind that you can only omit implicit dependencies from query results with the help of this flag. Bazel still uses implicit dependencies in its builds. It's a good idea to check implicit dependencies regularly and keep their number as few as possible to reduce build time and, possibly, build binary size.

### Soundness

Bazel queries are designed to ensure their results are always [sound](https://bazel.build/query/language#soundness). This means that the result of a Bazel query is always valid for all build [configurations](https://bazel.build/extending/config) that are defined in your project. This further means that while it's possible to have defined different features in various configurations of the project, a query expression returns the results on all those features.

This happens because the query phase occurs before configurations are introduced and evaluated in the build process. As a result, your query results might contain a larger number of elements than what you might end up with after you run the build with a particular configuration.

### Preservation of Graph Order

![Graph]({{site.images}}{{page.slug}}/graph.png)\

Bazel queries use [partial ordering constraints](https://bazel.build/query/language#results-ordering) to determine the order in which query results should be arranged. If you execute operators such as `allpaths`, `rdeps`, `somepath`, `deps`, `package:*`, and `dir`, Bazel query results use guaranteed ordering constraints inherited from their subexpressions.

For example, assume you have the following three targets in your `BUILD` files:

~~~{.bash caption=">_"}
//package1:test_target1 --> //package2:test_target2 --> \
//package3:test_target3
~~~

Let's say the following query finds the transitive closure of dependencies of `//package1:test_target1`:

~~~{.bash caption=">_"}
bazel query "deps(//package1:test_target1)"
~~~

The results look like this:

~~~{ caption="Output"}
//package1:test_target1
//package2:test_target2
//package3:test_target3
~~~

And let's say the query finds the dependencies of `//package2:test_target2`:

~~~{.bash caption=">_"}
bazel query "deps(//package2:test_target2)"\
~~~

Bazel still preserves and ensures the ordering constraints inherited from their subexpressions in the `BUILD` files. The targets are ordered based on the dependency graph:

~~~{ caption="Output"}
//package2:test_target2
//package3:test_target3
~~~

However, running these queries only affects the [ordering of results](https://bazel.build/query/language#results-ordering). It doesn't change the targets in the result set or how the query is computed.

Some operators, such as [union operators](https://bazel.build/query/language#tokens), don't have ordering constraints of their own, and they don't guarantee any specific [order for the targets in their result set](https://bazel.build/query/language#graph-order).

### Cycles in a Dependency Graph

BQL expects the build dependency graphs to be acyclic (*ie* free of any cycles/loops) and you should try to avoid cyclic dependencies. This is because cyclic dependency graphs can create deadlock situations. For instance, if target A is dependent on target B, and B is also dependent on A, one can't be built without the other, and as a result, neither may ever get built. The build operations might keep looping between the two targets in an infinite loop or throw unexpected results.

To help identify cyclic build graphs, the query results also contain warning messages. However, in most cases, it's still recommended to avoid cycles in your dependency graph.

### Sky Query

A [Sky Query](https://bazel.build/query/guide#reverse-dependencies) operates on a specified [universe scope](https://bazel-docs-staging.netlify.app/versions/master/cquery.html#universe_scope-comma-separated-list) to provide additional powerful query functions, such as `allrdeps` and `rbuildfiles`, that a typical query doesn't provide. To use them, you need to activate the Sky Query mode by passing either the `--infer_universe_scope` or  `--universe_scope` flag and the `--order_output=no` flag.

The following Sky Query finds all the reverse dependencies of a target within the given universal set:

~~~{.bash caption=">_"}
bazel query "allrdeps(//node/some_component:component_target)" \
--universe_scope=//node:parent_target --order_output=no
~~~

In this case, the `allrdeps` function finds all the reverse dependencies of `component_target` using the flag `--universe_scope` to instruct Bazel to preload the transitive closure of `parent_target` and evaluate the query within that scope. This allows you to find the reverse dependencies of a component across projects, which might not normally be possible through the `rdeps` function if the dependency was used outside of the scope that it was defined.

## Bazel Query Examples

Now that you know more about Bazel queries in general, take a look at a few examples that run queries in a project using this [basic Node.js app created with Bazel](https://earthly.dev/blog/build-nodejs-app-with-bazel/).

This Bazel workspace has a `//apps/node_web` Bazel target. If you want to find direct and transitive dependencies of the target, run the following code to find the `deps` query of a rule:

~~~{.bash caption=">_"}
bazel query "deps(//apps/node_web)"
~~~

<div class="notice--info">
Targets that `//apps/node_web` depend on are part of the result of this query, even though you didn't include their labels in your build query. It explains the Bazel query soundness concept.
</div>

<div class="wide">
![Dependencies]({{site.images}}{{page.slug}}/D1T2tGs.png)
</div>

To find the `BUILD` files containing the dependencies of `//apps/node_web`, the following query lists the packages in your Bazel workspace:

~~~{.bash caption=">_"}
bazel query "buildfiles(deps(//apps/node_web))" --output package
~~~

<div class="wide">
![`BUILD` files program]({{site.images}}{{page.slug}}/Qrasa3S.png)
</div>

If you have a package (*ie* `express`), you can check the existing packages that this particular package depends on:

~~~{.bash caption=">_"}
bazel query "@npm//express" --output package
~~~

<div class="wide">
![Package beneath another]({{site.images}}{{page.slug}}/0Z8Iw6k.png)
</div>

And you can find rules defined in a package:

~~~{.bash caption=">_"}
bazel query "kind(rule, @build_bazel_rules_nodejs//internal/runfiles:*)" \
--output label_kind
~~~

<div class="wide">
![Package rules]({{site.images}}{{page.slug}}/hsdiFZM.png)
</div>

In addition, you can find the reverse dependencies:

~~~{.bash caption=">_"}
bazel query "rdeps(..., //apps/node_web:index.js)" --output package
~~~

<div class="wide">
![Reverse dependencies]({{site.images}}{{page.slug}}/Xc8wkWW.png)
</div>

And you can select all rules with a particular value:

~~~{.bash caption=">_"}
bazel query "attr("tags", "[\[ ]node[,\]]", deps(//apps/node_web))"
~~~

<div class="wide">
![Value rules]({{site.images}}{{page.slug}}/0intLpl.png)
</div>

These are just a few examples of how to construct practical Bazel queries. Check out this [Bazel query guide](https://bazel.build/query/quickstart) to learn more query writing techniques.

## Conclusion

In summary, Bazel queries provide a potent tool for managing project dependencies. This tutorial has introduced their syntax and usage within your dependencies graph. Integrate Bazel queries in your builds to maximize their effectiveness in your development process.

And if you've enjoyed learning about Bazel queries and are looking for more ways to optimize your build processes, you might also enjoy exploring [Earthly](https://www.earthly.dev/). It's an alternative to Bazel that's easy to use. Check it out!

{% include_html cta/bottom-cta.html %}