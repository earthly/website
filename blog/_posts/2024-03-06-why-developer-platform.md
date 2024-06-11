---
title: "Why You Need a Developer Platform"
toc: true
author: James Walker

internal-links:
 - why you need a developer platform
 - developer platform
 - needing a developer platform
excerpt: |
    Developer platforms centralize internal tools and processes for software development, improving DevOps outcomes by automating tasks and reducing friction. They offer benefits such as accelerated software development, improved developer productivity, enhanced collaboration and communication, and reduced costs and risks.
categories:
  - platform
---
**The article discusses the significant influence of internal developer platforms. Earthly streamlines and speeds up builds. A great consideration for your developer experience play. [Learn more about Earthly](https://cloud.earthly.dev/login).**

Developer platforms centralize the internal tools and processes that developers use to build and deliver software. These platforms improve DevOps outcomes by providing automated mechanisms for developers to achieve their tasks.

More teams and organizations are launching their own internal developer platforms (IDPs) to reduce friction in their software delivery. Establishing an IDP takes time but offers substantial benefits, including improved productivity, easier collaboration, and less risky development. This article will explore these advantages and how they apply when building or buying an IDP solution.

## Addressing the Challenges of Modern DevOps

![Challenges]({{site.images}}{{page.slug}}/challenges.png)\

DevOps enhances software delivery by tightening feedback loops, encouraging cross-discipline communication, and automating key processes around testing, quality, and deployment. However, DevOps doesn't solve every challenge, nor does it tell you how to implement its concepts. Teams often struggle to understand where to start automating their work, or they run into difficulties when apps, team members, environments, and tools change because it's hard to enforce which technologies devs are using.

Developer platforms are a holistic solution for achieving DevOps ideals. Consolidating your toolchain around a shared internal platform makes it easier to integrate different processes and standardize them across developers. An IDP gives devs automated access to the resources they need, such as the ability to create a new test environment on demand or request access to inspect what's running in production.

You can do DevOps without an IDP, but it'll probably be much less efficient. IDPs remove the responsibility for managing infrastructure processes from individual devs, letting them concentrate on delivering new software. Engineers don't need to worry about how complex processes like deployments happen as they're implemented within the IDP. The platform's capabilities are usually maintained by a dedicated platform engineering team that exists to support DevOps requirements.

## How Developer Platforms Benefit DevOps Teams

Developer platforms provide many benefits that collectively enable DevOps teams to quickly deliver impactful work while experiencing fewer problems. This section covers some of the ways in which adopting an IDP will improve your team's engineering output.

### Accelerated Software Development

![Accelerated]({{site.images}}{{page.slug}}/accelerated.png)\

Developer platforms can have a transformational effect on software development velocity. They shorten the software development lifecycle (SDLC), tighten feedback loops, and remove work from developers by automating previously time-consuming processes that depend on multiple tools.

IDPs achieve this by providing functions that support developer autonomy and efficiency. Instead of having to wait for separate teams to apply actions, developers are empowered to achieve their aims themselves using self-service options available within the platform.

For example, creating a new staging environment is often a complex procedure with many steps involved. Traditionally, developers would have contacted an infrastructure team to request that new resources be provisioned, then asked ops for help in deploying an environment, and finally consulted a senior developer to learn how to seed the deployment with some test data. This sequence is long-winded, dependent on multiple stakeholders, and a potential source of inconsistencies between environments.

Making the process available in an IDP solves these challenges. Developers would be able to use the platform to automatically launch a new environment on demand, such as by clicking a button, running a CLI command, or even using an extension added to an IDE or chat app. Moreover, as everyone deploys using the same automated action, the IDP standardizes the workflow and prevents configuration discrepancies from occurring. This helps you scale as more apps and developers are added to your organization.

The throughput increase afforded by an IDP was observed by [Mercado Libre](https://platformengineering.org/blog/unveiling-the-secrets-of-a-successful-journey-mercado-libres-internal-developer-platform) after it implemented its own FURY platform. Introducing FURY unlocked exponential growth in the developer count, while the number of microservices seamlessly grew to over 24,000. The organization found that the "decrease in cognitive load and the gain in efficiency … have undoubtedly made every investment in a platform worthwhile."

### Improved Developer Productivity

Accelerating the SDLC results in developer productivity improvements too. Increasing the use of automation removes friction from processes, helping developers stay focused on meaningful work instead of being distracted by infrastructure management tasks.

In turn, this contributes to improved developer satisfaction. Devs are happiest when they have the tools they need to do their work without having to wait for others. A good platform supports developers so they can be more efficient, making them feel valued within the organization.

IDP automation and self-service capabilities are key to this effect as they promote autonomy. Devs can trigger tasks when they need them, even if they don't understand exactly how they work or which tools are being used. This also helps to democratize development by allowing each engineer to safely apply changes to any area of a project, including those that might fall outside their existing skills.

The actual productivity increase created by an IDP will naturally vary by organization. Some of the effects are quantifiable by looking at metrics such as the number of issues closed, pull requests approved, and deployments created; a successful IDP implementation should deliver increases to these values as developer time is freed up.

Other aspects are purely qualitative enhancements to your [developer experience](https://earthly.dev/blog/dx-three-ways) (DX): developers should feel less pressured, more empowered, and better equipped to obtain visibility into operations across the SDLC. These benefits don't always show up directly in your metrics but will have a positive impact on morale, motivation, and team retention, which further helps sustain development velocity.

One of the best examples of the productivity benefits of IDPs comes from Spotify, the original creator of the popular [Backstage](https://backstage.io/blog/2020/03/16/announcing-backstage) developer portal system. After creating and adopting Backstage internally across 280 teams and more than 2,000 backend services, Spotify observed a [55 percent decrease](https://backstage.io/blog/2020/03/16/announcing-backstage/?ref=faun#the-spotify-story) in new developer onboarding time, highlighting how platforms support developers to deliver more value faster.

### Enhanced Collaboration and Communication

Beyond productivity improvements at the individual level, developer platforms also help foster better collaboration within and between DevOps teams. Developer platforms make it easy to align the efforts of different teams and working groups, ensuring standard results even where complex multidiscipline processes are used.

Additionally, centralizing tools, processes, and documentation into a unified platform means that everyone's working with the same resources. All developers can access the assets they require and understand how neighboring teams are tackling problems, thus preventing information from becoming siloed.

IDPs also make it easy to integrate changes into workflows and then roll them out consistently across the whole organization. This reduces the number of operating procedures, security policies, and compliance rules that need to be directly communicated to each team, limiting the places where knowledge can fall between the cracks.

In some cases, IDPs don't even need to contain communication-specific functionality, as centralized docs and specs can be sufficient to achieve process improvements. During the development of its internal platform, [Zalando](https://www.youtube.com/watch?v=TjvwgOGi8mU) spent time writing standards for how different teams should work together using common practices, including authoring API guidelines and identity management expectations. Once a behavior is defined as part of your platform, everyone has a common spec to work against. You can then implement automated tooling later on to detect and prevent spec noncompliance.

Of course, IDPs can't do everything; indeed, this surfaces one of their potential weaknesses. For an IDP to be successful, all teams need to use it to achieve their aims, even where they may have previously reached for or built their own solutions. Obtaining acceptance from different teams is therefore a priority for any IDP implementation. This prevents fragmentation from occurring if some groups start creating their own tools that exist separately from the platform.

### Reduced Costs and Risks

Delivering software using an IDP reduces the costs involved in the SDLC. Instead of maintaining multiple environments and resources for developers to use, you can focus on supporting a single platform with optimized utilization and provisioning. The removal of manual process steps frees up developers to stay focused on feature development, reducing overall sprint durations and minimizing the cost to your organization.

Additionally, improving developer productivity and increasing throughput allow extra value to be delivered to customers, making you more competitive and reducing time to market. Cutting the hours spent manually connecting tools or waiting for processes to complete ensures all developers are occupied with meaningful work.

Standardizing development activities around automated platform-centric tasks also reduces the risk in the SDLC. Replacing manual workflows with automated ones provides stability and helps eliminate many common errors, such as inadvertently skipping a step or supplying an incorrect input to a command.

Moreover, IDPs make it easier to govern the entire SDLC using standard policies and frameworks. If you're subject to specific security, compliance, or regulatory requirements, you can implement guardrails in your platform that ensure continual enforcement across all teams and projects. This defends against accidental compliance breaches when developers use unapproved tools or accidentally push insecure code.

Developer platforms also make you more resilient to other types of risks, such as the productivity threats posed by staff absences. Centralizing processes into self-service platform actions means work can continue even when senior developers or adjacent teams are unavailable, making it less likely that you'll miss critical deadlines.

Teams that have adopted internal platforms can deploy up to four times faster than those without, according to [analysis by Humanitec](https://humanitec.com/blog/impact-of-internal-developer-platforms). Additionally, their change failure rate falls simultaneously—down to 4 percent from 15 percent for teams without a platform. When failures do occur, the mean time to recovery is just 1.3 hours with an IDP instead of six hours without, making it much less likely that SLAs will be breached. Ultimately, IDPs protect you from costly incidents and make it easier to deploy more frequently, giving you a competitive edge.

## Building vs. Buying a Developer Platform

There's no one-size-fits-all developer platform solution. Some teams assemble their own platforms from scratch, which incurs a high initial cost but enables a high degree of customization. Others favor prebuilt commercial solutions that enable immediate adoption, but these may be less adaptable to future change. Between these two approaches, open-source platforms such as [Backstage](https://github.com/backstage/backstage) provide a robust foundation for your own tools, giving you some of the benefits of both DIY and off-the-shelf approaches.

Here are some aspects to consider when choosing whether to build or buy an IDP.

### Advantages of Building an IDP

The following are a few advantages of building your own IDP:

- **Complete control over the platform's design and functionality:** You can implement your exact processes and integrate all the services you depend on.
- **Tailor-made for your workflows:** Engineering velocity is maximized as the platform works exactly the way your developers expect, reducing time spent reorienting around the platform.
- **Deep understanding of the platform's internals:** You can easily evaluate the scope of new feature additions and how they'll affect the processes already existing in your platform.

### Disadvantages of Building an IDP

The following are a few disadvantages of building your own developer platform:

- **Requires a significant upfront investment:** Creating your own IDP is resource-intensive, as you need the time, engineering availability, and expertise to integrate your services and launch the platform.
- **Ongoing maintenance and troubleshooting can be burdensome:** Any failures need to be diagnosed and investigated, which can be time-consuming and detract from development work. The platform also needs ongoing maintenance to ensure it stays secure, updated, and compatible with current developer requirements.
- **Potentially less scalable and adaptable to new tech:** Self-built IDPs can be tricky to scale with your organization as working methods change. If you decide to start building new apps with a different technology, then your platform could require substantial retooling to support the shift.

### Advantages of Buying a Prebuilt IDP

If you're interested in buying a prebuilt IDP, the following are a few of the advantages:

- **Provides immediate access to a robust solution:** Prebuilt IDPs are ready to use, letting you shorten the go-live time and immediately benefit from proven features that support your core workflows.
- **Low maintenance burden on internal teams:** Since the platform is maintained by an external vendor, you don't need to dedicate your teams to building or supporting it—potentially allowing more resources to be allocated to valuable development tasks.
- **Comprehensive documentation and support included:** Prebuilt IDPs come loaded with documentation, examples, and reference guides to help you get started. If there's a problem, then you can use the vendor's support services to get help when you need it.

### Disadvantages of Buying a Prebuilt IDP

While the benefits of buying a prebuilt IDP are tempting, you also need to consider the following disadvantages:

- **Potential lack of customization and flexibility:** Off-the-shelf platforms can be more difficult to customize to your requirements, especially if you work with unique combinations of technologies or have complex workflows.
- **Risk of vendor lock-in and limited control over the development direction:** Using a prebuilt IDP makes you dependent on the vendor to continue supporting the service. If the platform closes down or shifts direction, you might have no recourse except for a disruptive migration to an alternative service.
- **Can be challenging to integrate with existing services and systems:** Because prebuilt platforms are controlled by their vendors, it can be difficult to integrate them with unsupported external services. This can prevent you from accurately modeling your workflows and lead to multiple siloed systems being used.

### Building vs. Buying: How to Choose

![Choose]({{site.images}}{{page.slug}}/choose.png)\

The decision to build or buy should be based on the organizational context in which your IDP will be received. Building your own platform guarantees you can implement your exact workflow requirements and specific customization needs, but you need to be prepared for the complexity involved. If platform adoption is urgent, then selecting a prebuilt solution is a pragmatic way to reduce integration time and obtain immediate DevOps improvements.

Nonetheless, your planning should also account for your long-term strategy and development vision, as either type of IDP can affect your ability to execute in the future. A self-built platform is infinitely flexible but requires ongoing access to skilled internal teams; purchased options allow you to consistently focus on development work with minimal platform engineering investment but pose a constant threat of vendor lock-in.

Selecting a popular open-source platform like [Backstage](https://github.com/backstage/backstage)–seen by many as the original tool for building internal developer portals–is a third approach to consider. Not only can open-source mitigate or even eliminate cost and lock-in concerns, it also leaves you free to build your own extensions and bespoke components atop the platform.

You can evaluate prospective solutions across the following four priorities:

| Priority | Build or Buy? |
| ---- | ---- |
**Organizational maturity and technical expertise** | **Build:** Mature software organizations with access to skilled platform engineers will be able to exactly model their processes with minimal risk of being encumbered by the platform.
**Specific requirements and customization needs** | **Build:** Building your own platform allows you to accommodate your precise requirements, including unique aspects that are unlikely to be supported in prebuilt solutions.
**Time to market and urgency of implementation** | **Buy:** Prebuilt platforms are invariably faster to integrate and require fewer resources to get started.
**Long-term strategy and vision for the platform** | **Build:** Consider building if the platform will be essential to your future strategy and you're prepared to spend time maintaining it. **Buy:** Consider buying if you want the platform to be transparent, lack the resources to manually maintain it, or are unsure about your future commitment to DevOps and want to follow established best practices that are defined for you. Alternatively, use an open-source platform to get off the ground quickly, while retaining the option to fork the project and contribute custom functionality in the future.

## Conclusion: Use Developer Platforms to Amplify Software Delivery Efforts

In this article, you learned how developer platforms can address the challenges of modern DevOps by offering a centralized platform that automates key processes in the SDLC. By giving devs self-service access to the tools and procedures they need for their work, IDPs can accelerate throughput, enhance developer productivity and satisfaction, and prevent you from becoming dependent on risky manual tasks.

Whether you choose to build or buy a solution, launching an IDP requires an upfront investment to integrate it with your processes and train your developers. You'll also need to budget for the platform's ongoing maintenance to support the changing requirements of your DevOps teams. However, the long-term efficiency improvements enabled by successful adoption can easily offset these costs, making an IDP one of the most valuable assets for high-performing software organizations.

{% include_html cta/bottom-cta.html %}
