---
title: "Top 5 Tools for Generating Your SBOM"
categories:
  - Tutorials
toc: true
author: James Walker

internal-links:
 - tools for generating sbom
 - generating sbom
 - top 5 tools to generate sbom
 - generate your sbom
excerpt: |
    This markdown content provides a checklist for writing and publishing an article, including steps such as outlining, drafting, proofreading, creating a header image, and adding internal links. It also includes a checklist for optimizing an article for external publication, including adding an author page, optimizing images, and incorporating external links.
---

Producing a software bill of materials (SBOM) is an increasingly important stage in the software development lifecycle (SDLC). SBOMs catalog the open source components used in your product, providing a reference to the version numbers, vendors, and licenses you depend on.

Possession of an SBOM is a critical step toward understanding your software supply chain security. Obtaining visibility into your system's composition allows you to make more informed risk assessments, such as after a new zero-day vulnerability is discovered. You can quickly consult your SBOM to determine whether you're using an affected package.

The problem is that actually generating an SBOM can be a daunting task. With multiple tools and standards available, you'll face several choices along the way.

In this article, you'll learn more about SBOMs and why you need one. You'll also review five of the most popular SBOM generators and learn how you can use them in your projects.

## SBOM Formats

While there's broad consensus that generating an SBOM is a best practice step you should include in your SDLC, there's less agreement about the exact contents of an SBOM and how it should be expressed.

There are currently three main SBOM file formats, each of which has a slightly different purpose:

- [Software Package Data Exchange](https://spdx.dev) (SPDX) is an SBOM format that's defined by the Linux Foundation. It's designed to encapsulate common data about a range of software artifact types, with fields for name, version, copyright, security issues, and licensing. Two output variants are available: tag-value, which puts each field on a new line in `Field: Value` format, and JSON for easier machine consumption.
- The [CycloneDX](https://cyclonedx.org) standard aims to encompass the entire software supply chain; in addition to SBOMs, it can express other bills of materials (*eg* machine learning BOM and operations BOM), as well as vulnerability reports. Development of the CycloneDX format is led by the [Open Worldwide Application Security Project](https://owasp.org/) (OWASP).
- [Software identification (SWID) tags](https://www.iso.org/standard/65666.html) are part of an ISO standard that uses embedded metadata to make software components reliably identifiable by inventory tools. This can be extracted to produce an SBOM. In practice, the use of SWID tags has remained relatively low, but you might see them mentioned when evaluating SBOM generators.

It's advisable to choose a tool that supports one or more of these options. This will ensure that your SBOM's consumers (such as customers, clients, and compliance auditors) can easily interpret its information. Standards also help you use your SBOMs with wider ecosystem tools, such as vulnerability scanners that can read an SBOM to report the known zero-days in your dependencies.

## The Top 5 SBOM Tools

![Top 5 Tools]({{site.images}}{{page.slug}}/five.jpg)\

The following five tools have been selected because they represent modern approaches to SBOM generation that work with multiple programming languages, frameworks, and deployment environments. For each tool, you'll learn about its core functionality, how well it integrates with other systems, and its support for the standards listed above.

### Syft by Anchore

[Syft](https://github.com/anchore/syft) is a CLI-based SBOM generation tool from [Anchore](https://anchore.com), a software composition analysis (SCA) provider. Syft can also be used programmatically via a Go library, allowing you to easily automate bulk SBOM generation tasks.

Syft can generate SBOMs for container images, file system paths, and compressed archives. It's [capable of detecting](https://github.com/anchore/syft#supported-ecosystems) the majority of package formats, including programming dependencies installed in C, C++, Dart, Go, Java, JavaScript, PHP, Python, Ruby, and Rust projects, among others. Syft also supports OS packages for Alpine (apk), Debian (dpkg), and the Linux kernel (ko/vmlinuz).

In addition to its own format, Syft supports the SPDX and CycloneDX SBOM standards. You can also sign your SBOMs with [in-toto](https://github.com/in-toto/attestation/blob/main/spec/README.md) to prove their authenticity. This means Syft's reports are ready to distribute and use with other tools, including Anchore's [Grype](https://github.com/anchore/grype) vulnerability scanner.

Syft's README file provides comprehensive documentation on the available features and how to use them. It's easy to get started with the tool, but if you require more support, commercial options are available from the Anchore team. This makes Syft suitable for all development scenarios, from personal hobby projects to large-scale team endeavors.

Here's a simple example that uses Syft to produce an SBOM for a container image:

~~~{.bash caption=">_"}
$ syft alpine:latest
 ✔ Loaded image            
 ✔ Parsed image            
 ✔ Cataloged packages      [15 packages]
NAME                    VERSION      TYPE
alpine-baselayout       3.4.3-r1     apk   
alpine-baselayout-data  3.4.3-r1     apk   
alpine-keys             2.4-r1       apk
~~~

The packages detected in the image are displayed in your terminal.

To obtain output in a particular format (for example, an SPDX JSON file), you can set the `-o` flag:

~~~{.bash caption=">_"}
$ syft alpine:latest -o spdx-json
{
 "SPDXID": "SPDXRef-DOCUMENT",
 "name": "alpine-latest",
 "spdxVersion": "SPDX-2.2",
 "creationInfo": {
  "created": "2023-11-17T07:38:01.434421982Z",
  "creators": [
   "Organization: Anchore, Inc",
   "Tool: syft-0.29.0"
  ],
  "licenseListVersion": "3.14"
 },
~~~

### Tern

[Tern](https://github.com/tern-tools/tern) performs software composition analysis to produce an SBOM that lists the packages detected in container images and Dockerfiles. To run it, you need either Python or Docker installed on your system.

Tern analyzes your image's layers to understand the type of image it is and the package managers that are used. The commands run during the image build (*ie* the [Dockerfile `RUN` instructions](https://docs.docker.com/engine/reference/builder/)) are executed in a separate environment so Tern can track the package changes that each instruction applies to the container's file system.

The analysis results are collated into an SBOM that's ready to consume and share. Tern defaults to its own format, but both the SPDX and CycloneDX standards are available as alternatives.

The ability to scan Dockerfiles directly—without first building the image they define—makes Tern a convenient choice for programmatic environments such as CI/CD platforms. It supports both operating system packages and programming language dependencies, although the inability to scan arbitrary file system paths prevents it from being used with other types of artifacts beyond your container images.

Tern is an open source, community-driven project. The documentation is detailed, but there's no other support available. The repository's [public roadmap](https://github.com/tern-tools/tern/blob/main/docs/project-roadmap.md) notes that limited development resources are currently available. This could be a drawback for teams that need to generate SBOMs for critical projects.

It's easiest to run Tern as a Docker image. Because Tern doesn't currently publish images to a public registry, you need to [clone the source repository](https://github.com/tern-tools/tern#getting-started-with-docker), build the image, and then start a container.

The following example assumes the image is available on your system under the `tern:latest` tag:

~~~{.bash caption=">_"}
$ docker run --rm tern:latest report -i alpine:latest
This report was generated by the Tern Project
Version: 2.12.1

Docker image: alpine:latest:
    Layer 1:
        info: Layer created by commands: /bin/sh -c #(nop) ADD file:756183bba9c7f4593c2b216e98e4208b9163c4c962ea0837ef88bd917609d001 in /
        info: Found 'Alpine Linux v3.18' in /etc/os-release.
        info: Retrieved package metadata using apk default method.

    File licenses found in Layer:  None
    Packages found in Layer:
    +------------------------+-------------+-------------------------------------------+------------+
    | Package                | Version     | License(s)                                | Pkg Format |
    +------------------------+-------------+-------------------------------------------+------------+
    | alpine-baselayout      | 3.4.3-r1    | GPL-2.0-only                              | apk        |
    | alpine-baselayout-data | 3.4.3-r1    | GPL-2.0-only                              | apk        |
    | alpine-keys            | 2.4-r1      | MIT                                       | apk        |
~~~

Set the `-f spdxjson` flag to get the report in SPDX JSON format instead of the default readable table:

~~~{.bash caption=">_"}
$ docker run --rm tern:latest report -i alpine:latest -f spdxjson
{
    "SPDXID": "SPDXRef-DOCUMENT",
    "spdxVersion": "SPDX-2.2",
    "creationInfo": {
        "created": "2023-11-17T07:53:45Z",
        "creators": [
            "Tool: tern-2.12.1"
        ],
        "licenseListVersion": "3.20"
    },
    "name": "Tern report for alpine",
    "dataLicense": "CC0-1.0",
    "comment": "This document was generated by the Tern Project: \
    https://github.com/tern-tools/tern",
    "documentNamespace": "https://spdx.org/spdxdocs/tern-report-2.12.1-alpine-d8e16344-0a45-4a50-999f-516864f9401f",
    "documentDescribes": [
        "SPDXRef-alpine-latest"
    ],
    "packages": [
        {
            "name": "alpine",
            "SPDXID": "SPDXRef-alpine-latest",
            "versionInfo": "latest",
            "supplier": "NOASSERTION",
            "downloadLocation": "NOASSERTION",
            "filesAnalyzed": false,
            "licenseConcluded": "NOASSERTION",
            "licenseDeclared": "NOASSERTION",
            "copyrightText": "NOASSERTION"
        },
~~~

### Kubernetes BOM

[bom](https://github.com/kubernetes-sigs/bom) is a project from the Kubernetes development team that was created to make it easier to produce SBOMs for Kubernetes itself. Currently, it's a general-purpose tool that's suitable for use with your work, and it's incubated by the Linux Foundation.

bom is capable of scanning container images, file system paths, and individual files. This makes it a versatile tool that applies to every major SBOM use case. Individual SBOMs can reference multiple sources, allowing you to produce a consolidated inventory for all of your assets.

bom emphasizes standardization and interoperability. For that reason, it *only* supports SPDX output (in either tag-value or JSON formats). As a result, the SBOMs you produce can always be readily shared and inspected using other ecosystem tools. bom also supports the generation of provenance attestation files using [in-toto](https://github.com/in-toto/attestation/blob/main/spec/README.md#in-toto-attestation-framework-spec), letting you prove SBOM authenticity.

bom can also be used to visualize the content of SBOMs. It includes features for viewing files, querying them, and obtaining a condensed overview of the often dense data they contain. bom therefore offers a more convenient SBOM consumption experience than some of the other tools on this list.

Because bom is led by the Kubernetes team, with the backing of the Linux Foundation, it holds strong potential for future development. However, there's currently no specific support available beyond the documentation provided in the project's README. bom also remains relatively unknown; it has fewer than 270 stars on GitHub, and at the time of writing, no new updates have been released in the last six months.

bom is distributed as a Go project, so you need Go on your system before you can use it. Then, run the following command to install bom:

~~~{.bash caption=">_"}
$ go install sigs.k8s.io/bom/cmd/bom@latest
~~~

To generate an SBOM for a container image, use the `bom generate` command:

~~~{.bash caption=">_"}
$ bom generate -i alpine:latest
INFO bom v0.5.1: Generating SPDX Bill of Materials
INFO Processing image reference: alpine:latest    
INFO Reference alpine:latest points to an index   
INFO Reference image index points to 7 manifests  
...
SPDXVersion: SPDX-2.3
DataLicense: CC0-1.0
SPDXID: SPDXRef-DOCUMENT
DocumentName: SBOM-SPDX-ed492ac9-10f7-4c5a-bdb1-1e36a692f023
DocumentNamespace: https://spdx.org/spdxdocs/k8s-releng-bom-5e248342-409c-41ec-b055-b85ef729548d
Creator: Organization: Kubernetes Release Engineering
Creator: Tool: bom-v0.5.1
LicenseListVersion: 3.20
Created: 2023-11-17T08:10:25Z
~~~

### SPDX SBOM Generator

Looking for an SPDX-standard-compliant SBOM generator? Then look no further. Previously referred to as Open SBOM Generator, [SPDX SBOM Generator](https://github.com/opensbom-generator/spdx-sbom-generator) provides a convenient CLI for generating SBOMs that are formatted as SPDX and contain all the data supported by the standard, including security references and license details.

There's programming language support for Go, Java, JavaScript, Python, PHP, and Rust, among others. The tool's pluggable architecture allows you to add your own modules as well, such as to detect custom package types used in your project.

The generator is currently only capable of scanning file system paths. For example, you can't use it to directly scan a container image without first exporting the image to an archive that you then extract. For many projects, this will make the tool less convenient to work with than some of the other options. There are also relatively few configuration options available—for example, you can't exclude subpaths or generate attestation files.

A compounding factor is the lack of development activity observed over the past year. The project has yet to release a stable version, and no releases have been published since July 2022. A September 2023 code commit [indicated that](https://github.com/opensbom-generator/spdx-sbom-generator/commit/4879a906f7e5d331570e6ad0986c4c896580caa6) the project is still under construction, but at the time of writing, there've been no further updates. Users are currently warned to expect breakages and stability issues when future versions arrive.

Binaries are available for download from the project's [GitHub page](https://github.com/opensbom-generator/spdx-sbom-generator#installation). As a result, SPDX SBOM Generator is one of the simplest tools to deploy, as there's no third-party software to install and configure.

Once downloaded, you can scan your projects to produce an SBOM. The example command below references a Rust project:

~~~{.bash caption=">_"}
$ ./spdx-sbom-generator -p /open-spdx-sbom-rust
INFO[2023-11-17T08:55:23Z] Starting to generate SPDX ...                
INFO[2023-11-17T08:55:24Z] Running generator for Module Manager: 
`cargo` with output `bom-cargo.spdx`
INFO[2023-11-17T08:55:25Z] Current Language Version cargo 1.74.0 
(ecb9851af 2023-10-18)
INFO[2023-11-17T08:55:25Z] Global Setting File                          
INFO[2023-11-17T08:55:27Z] Command completed successful for 
below package managers
INFO[2023-11-17T08:55:27Z] Plugin cargo generated output at bom-cargo.spdx
~~~

The generated file contains the SBOM in the default SPDX tag-value format:

~~~{.bash caption=">_"}
$ cat bom-cargo.spdx
SPDXVersion: SPDX-2.2
DataLicense: CC0-1.0
SPDXID: SPDXRef-DOCUMENT
DocumentName: open-spdx-sbom-rust-0.1.0
DocumentNamespace: http://spdx.org/spdxpackages/open-spdx-sbom-rust-0.1.0-b0fa3da4-4633-4715-a7ff-6508ec35f29d
Creator: Tool: spdx-sbom-generator-v0.0.15
Created: 2023-11-17T08:55:27Z


##### Package representing the open-spdx-sbom-rust

PackageName: open-spdx-sbom-rust
SPDXID: SPDXRef-Package-open-spdx-sbom-rust
PackageVersion: 0.1.0
PackageSupplier: Organization: open-spdx-sbom-rust
PackageDownloadLocation: NOASSERTION
FilesAnalyzed: false
PackageChecksum: SHA1: 9ac60f17409eed46b53d476599c57eb0ed64836f
PackageHomePage: NOASSERTION
PackageLicenseConcluded: NOASSERTION
PackageLicenseDeclared: NOASSERTION
PackageCopyrightText: NOASSERTION
PackageLicenseComments: NOASSERTION
PackageComment: NOASSERTION
~~~

### CycloneDX Generator (`cdxgen`)

CycloneDX also has its own SBOM generation tool, [CycloneDX Generator](https://github.com/CycloneDX/cdxgen) (cdxgen). This is a fully-featured solution that supports the production of SBOMs for both source directories and container images. It has a CLI and is specifically designed to integrate well with CI/CD pipelines.

CycloneDX Generator supports a [comprehensive array of programming languages](https://github.com/CycloneDX/cdxgen#supported-languages-and-package-format) and package types. It can also scan many types of configuration files (including Kubernetes manifests, Helm charts, GitHub Actions pipeline definitions, and OpenAPI schemas) and can even generate SBOMs for Windows virtual machines.

All output produced by the tool uses the CycloneDX format. This makes it interoperable with other ecosystem components that understand the CycloneDX specification. The companion [CycloneDX CLI](https://github.com/CycloneDX/cyclonedx-cli) is also capable of converting SBOMs between formats (including SPDX) and visualizing their content, in addition to signature verification and diff detection features.

The project is developed in Node.js and can be integrated with your own apps [as a library](https://github.com/CycloneDX/cdxgen#integration-as-library). This lets you easily create more complex automated workflows where SBOMs are generated as part of a script.

Owing to its OWASP backing, CycloneDX has the advantage of being one of the more active projects in the SBOM space. There's clear documentation, a regular release schedule, a community [Discord server](https://discord.gg/tmmtjCEHNV), and the option of enterprise support provided by [AppThreat](https://www.appthreat.com)—the tool's original creator. This makes CycloneDX suitable for use in large projects that require stability.

Since CycloneDX is developed in Node.js, it's easy to install using npm (though a Docker image is also available):

~~~{.bash caption=">_"}
$ npm install -g @cyclonedx/cdxgen
~~~

The following example uses CycloneDX to produce an SBOM for a container image:

~~~{.bash caption=">_"}
$ cdxgen -t docker alpine:latest -o sbom.json
~~~

The output file contains the SBOM in CycloneDX JSON format:

~~~{.bash caption=">_"}
$ cat sbom.json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.5",
  "serialNumber": "urn:uuid:2786ceda-824c-438f-8465-22bad297ee15",
  "version": 1,
  "metadata": {
    "timestamp": "2023-11-17T09:24:14.903Z",
    "tools": {
      "components": [
        {
          "group": "@cyclonedx",
          "name": "cdxgen",
          "version": "9.9.4",
          "purl": "pkg:npm/%40cyclonedx/cdxgen@9.9.4",
          "type": "application",
          "bom-ref": "pkg:npm/@cyclonedx/cdxgen@9.9.4",
          "author": "OWASP Foundation",
          "publisher": "OWASP Foundation"
        }
      ]
    },
    "authors": [
      {
        "name": "OWASP Foundation"
      }
    ],
    "component": {
      "name": "alpine",
      "version": "latest",
      "type": "container",
      "purl": "pkg:oci/alpine@sha256:eece025e432126ce23f223450a0326fbebde39cdf496a85d8c016293fc851978",
      "bom-ref": "pkg:oci/alpine@sha256:eece025e432126ce23f223450a0326fbebde39cdf496a85d8c016293fc851978"
    },
~~~

### Summary: Comparison Table

To recap, here's a quick comparison table for all the tools you've learned about here:

| | **Syft** | **Tern** | **Kubernetes bom** | **SPDX** | **CycloneDX** |
|-| ---- | ---- | ---- | ---- | ---- |
**Automatic/programmatic generation** | Yes, as a Go library | Yes, with Python extensions | No official support | Yes, using custom modules | Yes, as a Node.js library
**Container capabilities** | Yes | Yes (including Dockerfile scans) | Yes | Yes | No | Yes
**Supported components** | OS packages and programming language dependencies | OS packages and programming language dependencies | OS packages and programming language dependencies | Programming language dependencies only | OS packages, programming language dependencies, cache contents, API schemas, container and CI/CD configuration files
**Ease of deployment** | Easy; binary download or Docker image | Intermediate; requires Python or manual build of a Docker image | Intermediate; requires Go | Easy; binary download | Easy; use npm or Docker
**Integrations** | Seamlessly works with other Anchore tools and supports programmatic use with Go | Programmatic use with Python | No native integrations | No native integrations | Integrates with other CycloneDX CLIs and supports programmatic use via Node.js library
**Reporting and analysis** | Multiple output formats, including human-readable options and SPDX | Multiple output formats, including human-readable options and SPDX/CycloneDX | Outputs SPDX. Includes tools for querying and inspecting SBOM content. | Outputs SPDX. No options for querying content or producing human-readable output. | Outputs CycloneDX. Can be combined with the CycloneDX CLI for visualization and querying purposes.
**Support** | Commercial support available | No formal support available | No formal support available | No formal support available, and project is infrequently developed | Commercial support available
**Training resources** | Detailed README and examples | Detailed README and examples | Detailed README and examples | Detailed README and examples | Detailed README, examples, and documentation microsite

## Conclusion

In this article, you learned about five popular tools that you can use to produce SBOMs for your software projects. SBOMs list the components that your software depends on, helping interested parties (whether security teams or customers) to understand your product's composition. This helps you maintain your security posture by allowing rapid identification of potentially problematic packages.

Whether you choose [Syft](https://github.com/anchore/syft), [Tern](https://github.com/tern-tools/tern), [Kubernetes bom](https://github.com/kubernetes-sigs/bom), [SPDX SBOM Generator](https://github.com/opensbom-generator/spdx-sbom-generator), [CycloneDX Generator](https://github.com/CycloneDX/cdxgen), or another solution altogether, regularly generating SBOMs is a best practice step to reduce risks and stay informed about your supply chain security.

{% include_html cta/bottom-cta.html %}
