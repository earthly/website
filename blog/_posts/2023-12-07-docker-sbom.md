---
title: "How to Generate Your SBOM from Docker Images"
categories:
  - Tutorials
toc: true
author: James Walker

internal-links:
 - just an example
last_modified_at: 2023-09-08
---

A software bill of materials (SBOM) is a manifest that lists all the dependencies and third-party components included in your application's codebase. It gives you visibility into your software supply chain, allowing you to verify that your application only uses secure and updated dependencies.

In this article, you'll learn more about what SBOMs are and why they're important in the context of containerized apps that use Docker. Then, you'll learn how to generate a SBOM for your Docker images using the experimental `docker sbom` command.

## What Is a SBOM?

In physical manufacturing industries, a product's bill of materials (BOM) states the components required to produce it. For example, building a new desktop computer requires a processor, some memory modules, and a case; in turn, those components will need metal, plastic, and other materials.

A SBOM fulfills a similar role for software products. It lists the dependencies in your stack to give you a complete overview of your supply chain. The details included in a SBOM can vary, but frequently include:

- Open source and third-party programming language packages
- Operating system (OS) packages
- Version and licensing information
- Links to any known vulnerabilities that affect each package
- Package authorship and download location references

This information can be used to inform vital internal security efforts—such as identifying compromised packages and removing them from your stack—but it's also suitable for distribution to customers, partners, and compliance auditors who need to understand how your software is built.

## Why Should You Generate a SBOM for Docker Images?

Docker has simplified software development by making it easy to package and deploy applications using containers. However, containers present a "black box" problem because it's difficult to inspect their contents. They include all the packages inherited from their [base image chain](https://docs.docker.com/build/building/base-images), as well as any extra OS packages and programming language dependencies you install in your own `Dockerfile`. The final package list can even change without your knowledge when the base image is updated.

You can gain visibility into your Docker images by producing SBOMs for them. An image's SBOM will list every component of the image, including both the OS packages in its file system and the packages that your app directly depends on.

When a new zero-day vulnerability like [Log4j](https://www.ncsc.gov.uk/information/log4j-vulnerability-what-everyone-needs-to-know) is reported, you can consult your container's SBOM to determine whether it's affected. Similarly, publishing the SBOM to your customers allows *them* to verify that your software is safe to use.

## How to Generate a SBOM for Your Docker Image

You can generate SBOMs for your container images using the [`docker sbom`](https://docs.docker.com/engine/sbom) command. It provides integrated capabilities for viewing and exporting SBOMs without having to install any other tools.

### Enable and Run the docker sbom Command

`docker sbom` is an experimental feature. It already includes useful functionality today, but the command might change or be removed in the future. How you access `docker sbom` depends on the Docker edition that you're using:

- If you're using [Docker Desktop](https://www.docker.com/products/docker-desktop), then the `docker sbom` command has been available by default since [Docker Desktop v4.7.0](https://docs.docker.com/desktop/release-notes/#470), which was released in July 2022.
- If you're using the [Docker Engine](https://docs.docker.com/engine/install) standalone daemon on Linux, then you'll need to manually add the [Docker SBOM CLI plugin](https://github.com/docker/sbom-cli-plugin) before you can use the feature.

You can check whether the command is already available on your system by running:

```bash
docker sbom --version
```

You're good to go if your output looks like this:

```bash
sbom-cli-plugin 0.6.1, build 02cf1c888ad6662109ac6e3be618392514a56316
```

If the feature is unavailable, you'll see a `'sbom' is not a docker command` error message. You should manually install the plugin by first downloading the installation script:

```bash
curl -sSfl https://raw.githubusercontent.com/docker/sbom-cli-plugin/main/install.sh -o install-docker-sbom.sh
```

Then, make the installation script executable:

```bash
chmod +x install-docker-sbom.sh
```

Run the installation script:

```bash
./install-docker-sbom.sh
```

Your output will look like this:

```
[info] fetching release script for tag='v0.6.1'
[info] using release tag='v0.6.1' version='0.6.1' os='linux' arch='amd64'
[info] installed /home/james/.docker/cli-plugins/docker-sbom
```

Finally, check that `docker sbom` is available. Try running `docker sbom --version` to confirm that the plugin was installed successfully. Your output should look like this:

```
sbom-cli-plugin 0.6.1, build 02cf1c888ad6662109ac6e3be618392514a56316
```

### Generate a SBOM

You can generate and view an image's SBOM by passing the image's tag to the `docker sbom` command, like this:

```bash
docker sbom nginx:latest
```

The command starts by pulling the image for [Syft](https://github.com/anchore/syft), the underlying SBOM generator that `docker sbom` wraps. The image you're scanning is then pulled and parsed to identify which packages it contains. The results are displayed in a table in your terminal:

```
Syft v0.46.3
 ✔ Pulled image            
 ✔ Loaded image            
 ✔ Parsed image            
 ✔ Cataloged packages      [150 packages]
NAME                       VERSION                         TYPE         
adduser                    3.134                           deb           
apt                        2.6.1                           deb           
base-files                 12.4+deb12u1                    deb           
base-passwd                3.6.1                           deb           
bash                       5.2.15-2+b2                     deb
```

Each row in the table describes a single package in your container image. The records include the package's name, installed version, and the type of package that it is. The row below represents a Debian package installed in the operating system:

```
bash                       5.2.15-2+b2                     deb
```

Using this information, you can rapidly identify which packages are present in your container. When a new vulnerability is published, viewing the SBOM lets you check whether you're using an affected version.

### Format the SBOM Output

`docker sbom` defaults to the human-readable table output shown in the previous example, but several [alternative options](https://docs.docker.com/engine/sbom/#output-formatting-and-saving-outputs) are available. Here are some you should be familiar with:

- `cyclonedx-xml`: [CycloneDX](https://cyclonedx.org), an [OWASP Foundation](https://owasp.org) project, is a standardized format for expressing SBOM data. CycloneDX XML reports are supported by [several third-party tools](https://cyclonedx.org/tool-center).
- `github-json`: The GitHub JSON format is a GitHub-specific option for integrating SBOMs with your repositories. However, GitHub is moving to support [standardized formats](https://github.blog/2023-03-28-introducing-self-service-sboms/), so `github-json` is rarely used.
- `spdx-json`: [SPDX](https://spdx.dev) (Software Package Data Exchange) is another standardized specification for the contents of SBOMs. It's led by the [Linux Foundation](https://www.linuxfoundation.org/) and supported by industry vendors including AWS, Google, and Microsoft. Reports generated in this JSON-based format can be used with [many supply chain security tools](https://spdx.dev/use/tools/open-source-tools).
- `text`: This is an alternative human-readable format that displays packages in a list.

Use the `--format` flag to specify the format to use for your SBOM:

```bash
docker sbom nginx:latest --format spdx-json
```

An SPDX JSON report contains much more information about the detected packages and their sources:

```json
{
 "SPDXID": "SPDXRef-DOCUMENT",
 "name": "nginx-latest",
 "spdxVersion": "SPDX-2.2",
 "creationInfo": {
  "created": "2023-11-01T20:07:53.905499809Z",
  "creators": [
   "Organization: Anchore, Inc",
   "Tool: syft-v0.46.3"
  ],
  "licenseListVersion": "3.17"
 },
 "dataLicense": "CC0-1.0",
 "documentNamespace": "https://anchore.com/syft/image/nginx-latest-6cba1524-4bee-404b-a4d5-8eba1a376577",
 "packages": [
  {
   "SPDXID": "SPDXRef-1f8a9173774c4709",
   "name": "adduser",
   "licenseConcluded": "GPL-2.0 AND GPL-2.0+",
   "downloadLocation": "NOASSERTION",
   "externalRefs": [
	{
 	"referenceCategory": "SECURITY",
 	"referenceLocator": "cpe:2.3:a:adduser:adduser:3.134:*:*:*:*:*:*:*",
 	"referenceType": "cpe23Type"
	},
	{
 	"referenceCategory": "PACKAGE_MANAGER",
 	"referenceLocator": "pkg:deb/debian/adduser@3.134?arch=all&distro=debian-12",
 	"referenceType": "purl"
	}
   ],
   "filesAnalyzed": false,
   "licenseDeclared": "GPL-2.0 AND GPL-2.0+",
   "originator": "Person: Debian Adduser Developers <adduser@packages.debian.org>",
   "sourceInfo": "acquired package info from DPKG DB: /usr/share/doc/adduser/copyright, /var/lib/dpkg/info/adduser.conffiles, /var/lib/dpkg/info/adduser.md5sums, /var/lib/dpkg/status",
   "versionInfo": "3.134"
  },
(truncated)
```

This report is suitable to be saved and distributed alongside your container images. It allows users to be sure of what they're running, similar to how food labels give you detailed information on the ingredients you're eating.

### Save the SBOM Output

Regardless of the format you select, `docker sbom` defaults to printing your report's output to your terminal. You can save it to a file instead by setting the `--output` flag:

```bash
docker sbom nginx:latest --format spdx-json --output nginx-sbom.json
```

The initial progress information will still be emitted to your console, but the report will be separately written to the specified file.

### Generate SBOMs for a Different Platform

Most popular Docker images are now multiarch. A tag such as `nginx:latest` can point to several different architecture variants, such as AMD64 and ARM64, and Docker automatically selects the correct one for your system.

`docker sbom` respects this behavior by generating the SBOM for the variant that matches the architecture and platform you're currently using. You can get the SBOM for a different variant by using the `--platform` flag, where the available values depend on those supported by the image:

```bash
docker sbom nginx:latest --platform arm64
```

### Exclude Specific Container Paths

Occasionally, you might want to generate a partial SBOM for some of the paths within a container. For example, you might only want to see the packages that are directly referenced by your application as programming dependencies, without the output being polluted by the container's OS packages.

The `--exclude` flag lets you omit specific paths from the SBOM scan. It supports [glob patterns](https://man7.org/linux/man-pages/man7/glob.7.html) and can be repeated multiple times.

The following example excludes all common OS package locations:

```bash
docker sbom nginx:latest --exclude /lib --exclude /var
```

Now only one package has been detected, as the noise from the primary system directories has been removed:

```
Syft v0.46.3
 ✔ Loaded image       	 
 ✔ Parsed image       	 
 ✔ Cataloged packages  	[1 packages]
NAME 	VERSION  TYPE    	 
libintl  0.21 	java-archive
```

Excluding paths you know to be irrelevant will make your scans more performant and cut down on visual noise in reports.

## Conclusion

In this article, you explored how SBOMs allow you to enhance software supply chain security by cataloging the third-party packages included in your application.

Supply chain security is topical in the wake of major incidents such as [SolarWinds](https://www.ncsc.gov.uk/collection/ncsc-annual-review-2021/the-threat/solarwinds) and [Log4j](https://www.ncsc.gov.uk/information/log4j-vulnerability-what-everyone-needs-to-know). In both of these cases, problems in a third-party package meant organizations had to urgently check if they were affected. Having an SBOM makes this task much easier by giving you a single reference point that lists every package with its version.

SBOMs are particularly important for containerized applications because the packages included in a container can change each time it's rebuilt if the base image has been updated. It can also be tricky to inspect the contents of container file systems, making it harder to know which packages are present.

Generating a SBOM for your images using `docker sbom` allows you to easily access this information and then distribute it to your clients and customers. This increases trust in your software, lets you efficiently address new zero-day vulnerabilities, and could [even be a requirement](https://www.isaca.org/resources/news-and-trends/industry-news/2023/why-are-regulations-demanding-sbom-adoption) when tendering for future software delivery contracts.

## Outside Article Checklist

- [ ] Create header image in Canva
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
  - Would any images look better `wide` or without the `figcaption`?
- [ ] Run mark down linter (`lint`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `link-opp` and find 1-5 places to incorporate links
- [ ] Add Earthly `CTA` at bottom `{% include_html cta/bottom-cta.html %}`
