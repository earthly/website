---
title: "Introducing Self-Hosted Earthly Satellites"
categories:
  - news
toc: true
author: Gavin

internal-links:
 - introduction to earthly satellites
 - earthly satellites
 - what are earthly satellites
excerpt: |
    Announcing Self-Hosted Earthly Satellites. Remote build runners that bring the power of Earthly's consistent, fast builds to your own infrastructure.
---

I remember the first application that I self-hosted, [BugTracker.NET](https://ifdefined.com/bugtrackernet.html). It's ancient now, but this was in 2009. I had just landed my second job out of undergrad. I went from being an incredibly underpaid computer programmer focusing on one of Microsoft's now-legacy ERP systems, Dynamics AX, and development on top of Microsoft SQL Server to being a system administrator for that same ERP system for a new company at more than double the pay.

When I landed in this new role, they didn't have a bug/feature tracking system. They had a helpdesk ticketing system that the infrastructure team used, but it was insufficient for what I needed, and the licensing scheme didn't allow end-users to enter tickets themselves. I didn't have the budget for a bug/feature tracking system either, and I wasn't going to get it. The company was investing $2M over two years into the ERP system I was responsible for implementing. This was a huge spend for them. There was no chance I was getting another $10K or whatever the price was going to be for a bug/feature tracking system. So I went searching for solutions to my problem, and BugTracker.NET was the best option I found.

### Self-Hosting Wasn't Easy, but It Provided Real Value

I was extremely familiar with open source software by this point. I'd been installing Linux on every PC I pieced together from garage sale finds since I was 13 or 14 (I Frankenstein'd together a lot of PCs from salvaged parts). I had never self-hosted anything at that point though, and I'd never brought an open source tool into a company I had worked for. I needed it though. The business needed it too, they just didn't know it.

So I set it up. I spun up a VM, configured IIS, installed all the prerequisites, created a new database in one of our non-production SQL Server instances, and installed BugTracker.NET. It wasn't exactly straightforward, and it required a lot of resources we happened to have "lying around" (e.g. a server available with extra space for the VM, extra license keys for Windows Server, and a barely used, non-production SQL Server instance), but I got it working within a day.

We used self-hosted BugTracker.NET for the following three years I was at this company (they probably used it after I left). It became the de facto standard for bug/feature tracking outside of the infrastructure team. It solved an important problem for us and provided incredible value to the business. After that, I was sold on self-hosting. Sure it was a pain to get everything configured, but it was worth it.

After Docker came out, the number of applications I personally self-hosted ballooned. Docker lowered the barrier to entry for self-hosting a lot. I didn't have to spin up a VM and configure a web server for each application. Now I just have one web server running with Docker installed. Self-hosting an application is as easy as creating a new database in one of my Postgres instances, launching a container with the application's image, and adding it to the server's reverse proxy. This has allowed me to experiment with a lot of self-hosted applications. Right now, I have one VPS where I self-host [Firefly III](https://www.firefly-iii.org/), [Bitwarden](https://bitwarden.com/), [Nextcloud](https://nextcloud.com/), and [Plex](https://www.plex.tv/), all with Docker.

### Self-Hosting Is Problem-Solving

Self-hosting, for me, centers around one thing: problem-solving with software. I have something I want to do or an issue I keep running into. I find open source software that does what I need and self-host it. My problem is solved.

Sometimes the problems you need to solve go beyond the capabilities of the software though. Sometimes the problem is that I have multiple options and don't know which piece of software to use. Self-hosted software (along with SaaS free tiers) makes trying things out and making a decision easier. Or maybe the problem is that I can't have a piece of software operating in a vendor's cloud, it needs to be in mine, whether for purposes of security or for hardening production environments. In that case, self-hosted is almost the only option.

## Announcing Self-Hosted Earthly Satellites

![Announcing]({{site.images}}{{page.slug}}/announce.png)\

Here at Earthly, I'm a marketer, but the way I choose to market is to focus on the problems we can help our users and customers solve. I know a lot of you out there have a VPS running Plex or a homelab, and I want you to be able to use Earthly Satellites and see how awesome it is. And – maybe I'm not supposed to say this part out loud – if some of you self-host Earthly Satellites for a side project, you'll like it, and you might bring it into work (and that's where we get paid).

We are announcing the availability of self-hosted Earthly Satellites. Earthly Satellites are remote build runners that work natively with Earthly. They are also the primary service included with Earthly Cloud. Up to now, Earthly Satellites were only available as a fully managed service hosted in Earthly's infrastructure. This lets you bring Earthly Satellites into your ecosystem, have them run on your infrastructure, and still use the same Earthly Cloud UI and native Earthly CLI integration that our managed and hosted Satellites offer. So your build execution, build artifacts, and even your code never leave your hardware or your ecosystem.

### Why Choose Self-Hosted Earthly Satellites?

![why]({{site.images}}{{page.slug}}/why.png)\

* _Enhanced Security_:  We know that the more complex your application's infrastructure is, the more likely it is that you need CI/CD to run next to production. This is the primary use case for self-hosted Satellites. In addition, if having a highly available application is important to your company, you'll likely want to keep your production environment as isolated as possible. This lets you reduce the variables you don't control that can cause your app to stutter.
* _Customizable Performance_:  With self-hosted Satellites, you can customize instances for specific hardware and network configurations. So you can make sure each instance has whatever resources your builds need in a much more specific way than with our hosted Satellite sizes. If you need more cache storage, you can add more cache storage without upgrading to a larger machine.
* _Use Cloud Vendor Credits_:  Since self-hosted Satellites are in your environment using your cloud infrastructure, you can use the credits you already have with your cloud vendor to pay for compute. This frequently makes getting approval to use a tool easier and, depending on the discount you have with your cloud vendor, could be less expensive than using hosted Satellites.
* _Full Control_:  You can manage and update your self-hosted Satellites according to your schedule and requirements. If your business has its own scheduled maintenance windows, you can update your self-hosted Satellites then and not be beholden to our SaaS maintenance windows.
* _Automatic TLS Key Management_:  We automatically manage and rotate TLS keys for hosted Satellites. It's a basic requirement that Earthly Satellites has always satisfied. Self-hosted Satellites are no different. Your and everyone on your team's TLS keys will be automatically generated and rotated just like they are for hosted Satellites. So you never have to think about encryption with your builds nor the process that everyone on your team has to follow to get it right. It's done for you automatically.
* _Seamless Integration_:  Self-hosted Satellites integrate seamlessly with Earthly and Earthly Cloud. When you launch a self-hosted satellite, it automatically registers with Earthly Cloud and is ready to run builds from the command line. If you want to run a build on a self-hosted satellite, you use the same commands that you would on an Earthly-hosted satellite.
* _Consistent, Fast Builds that Work with Any CI_:  With self-hosted Satellites, you still get all the benefits you expect from Earthly:  write once, run anywhere builds that work the same on your laptop as they do in CI; ridiculous build speed from Earthly's automatic caching and parallel execution; and compatibility with any CI.

### Getting Started with Self-Hosted Earthly Satellites

![starting]({{site.images}}{{page.slug}}/started.png)\

Launching a self-hosted satellite is as easy as running the public Docker image. A few environment variables are needed to link the satellite with your Earthly Cloud account. The satellite will use these values to automatically register it with the Earthly Cloud control plane. Note that Earthly Cloud will never connect to your satellite directly. So the host and port of your satellite can be private to your internal network or VPC.

Here is a minimal command to start a self-hosted satellite:

~~~{.bash caption=">_"}
docker run --privileged \
    -v satellite-cache:/tmp/earthly:rw \
    -p 8372:8372 \
    -e EARTHLY_TOKEN=[your_token] \
    -e EARTHLY_ORG=[your_earthly_cloud_org] \
    -e SATELLITE_NAME=[your_satellite_name] \
    -e SATELLITE_HOST=[your_satellite_hostname_or_ip] \
    earthly/satellite:v0.8.3
~~~

The following environment variables are required:

* `EARTHLY_TOKEN` - a persistent auth token obtained by running `earthly account create-token [token-name]` from the Earthly CLI.
* `EARTHLY_ORG` - the name of your organization created in [Earthly Cloud](https://cloud.earthly.dev/).
* `SATELLITE_NAME` - a name you choose to identify the satellite instance.
* `SATELLITE_HOST` - Hostname or IP address of your satellite for the Earthly CLI to connect (note that users will select the satellite by name when running builds).

Once your satellite is launched and has finished registering with the Earthly Cloud control plane, it can be selected and managed using typical Earthly Satellite commands from the CLI. For example, to select the satellite for persistent use in subsequent builds:
`earthly sat select [your_satellite_name]`

Or, to invoke a build once on the satellite, without having it persistently selected:
`earthly --sat [your_satellite_name] +your-target`

_For the complete guide, visit [the Self-Hosted Satellites page in our documentation](https://docs.earthly.dev/earthly-cloud/satellites/self-hosted) ._

## Start Self-Hosting Earthly Satellites Today

![today]({{site.images}}{{page.slug}}/today.png)\

[Sign up for Earthly Cloud](https://cloud.earthly.dev/login) to start self-hosting your own Earthly Satellites. They are even available on our free tier, so you can start with self-hosted Satellites now at no cost ([visit our Pricing page](https://earthly.dev/pricing#compute-pricing) for more details about pricing for self-hosted Satellites). Try out self-hosted Earthly Satellites, and let us know how they work for you.

{% include_html cta/bottom-cta.html %}
