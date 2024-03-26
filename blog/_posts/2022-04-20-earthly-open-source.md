---
title: Earthly Switches to Open-source
featured: true
categories:
 - News
tags:
- license
- news
- open-source
author: Vlad
internal-links:
  - earthly open-source
topic: earthly
funnel: 3
topcta: false
excerpt: |
    Earthly, a CI/CD framework, has announced that it is switching to an open-source license, allowing for greater community involvement and integration with various CI/CD vendors. The decision was made after considering user feedback and the benefits of an open model for both users and the business.
last_modified_at: 2023-07-24
---

*TLDR We are switching from a source-available license, to an open-source license for Earthly.*

We started Earthly with the mission of bringing better builds to the world and to become the standard CI/CD framework that allows pipeline development locally and running on any CI.

Oftentimes, to be able to deliver on a mission, you also need a way to sustain that mission long-term. For us this meant raising capital from investors and building a sustainable business around it. To protect the interests of the business, we need to create a moat[^1]. Thus, some time ago we decided to use the source-available license [Business Source License](https://mariadb.com/bsl11/) (BSL), which is like an open-source license, but with one exception: it prevents anyone from creating a competing product and also commercializing it.

On our journey to make Earthly the standard framework for CI/CD pipelines, we realized that Earthly would not be as successful long-term if we don't make it an open-source standard. **Today, we are proud to announce that Earthly switches to an open-source license, [Mozilla Public License Version 2.0](https://www.mozilla.org/en-US/MPL/2.0/).**

Following user feedback, advice from open-source industry CEOs and conversations with our network of advisors, we decided that a switch to a more open model is best for both the community and also for the business. Here is how our thinking evolved.

[^1]: A company's moat refers to its ability to maintain the competitive advantages that are expected to help it fend off competition and maintain profitability into the future.

## Understanding the Motivation Behind Source-Available

The first observation we made was that source-available licenses (and sometimes open-source copy-left licenses[^2]) are more predominantly used for databases. More and more this seems like a more widely accepted model in that world. We asked ourselves why that is and we spoke to a few of the leaders of database companies. Here is what we found:

* As expected, the main reason for using a more restrictive license is to prevent the competition from offering your product as a service. It helps to protect yourself from "hyperscalers" - the tech giants of the world that are able to use a platform play (i.e. the monopoly game) to attract users to their offering much easier than yours.
* You generally want to open-source the pieces that require deep code integration. This helps prevent vendor lock-in concerns on the user's side, but it also allows the community you're targeting: developers, to help out with ironing out any inefficiencies in your product. Developers will become contributors and help make a better platform for everyone, especially in the areas that are very close to their own code. After all, what most contributors do is scratch their own itch.
* In some cases, the DB is source-available, while the syntax is based on another open-source project. This helps make the part that has deep code integration stay fully open, alleviating the concerns mentioned in the point above. An example is Cockroach DB - the DB is source-available, but the syntax of the queries is Postgres-compatible - a widely known and loved open-source dialect for SQL. This makes the actual DB work on a plug-and-play model for the most part, making it easy to swap out - and arguably harder to protect from hyperscalers.
* Most non-DB projects often create a **Developer Experience** play as well, which creates large communities, which in and of their own are a tremendous moat. And it's a moat despite the project being open-source. An example would be Terraform: a far nicer API over any cloud vendor. The author of the project will always be in the best position to help support the community and for that reason, all the value flows upstream to the original project. Being as open as possible encourages this flow. In contrast, in the case of DBs it is much more typical for the value to come from production environment efficiency improvements and less so from improved developer experience locally - which makes the community-as-moat play less relevant (not completely irrelevant, but sensibly less so). For this reason, again, there need to be better mechanisms to protect database products specifically from a business perspective, hence the choice of source-available.
* Databases are already budgeted for. Getting a hundred high-paying customers is enough for many database companies to be successful. For other developer products, the unit economics don't work quite the same way, and community and scale of individual users becomes much more important. Hence it's better to optimize for growth.
* A lesser reason (but still relevant), is that in some isolated cases the DBs have used open-source in their early life to create growth and awareness, and now at maturity, they have switched to a source-available to switch focus from growth to monetization. The switch was extremely disruptive for the community given that it was done so late in their life (after so many depended on the license being open-source) and has prompted the community to show up with angry comments and pitchforks. I will not name names :-), but this kind of fiasco has given source-available a worse name than it deserves.

Overall, we believe that source-available models are net good when used in the right situations. Normalizing them is a fight worth fighting. Putting the power of innovation in the hands of the small guys and preventing monopoly bullying is in the best interest of the user in the end because it encourages innovation.

However, as our thinking evolved, we now believe that *for Earthly specifically*, it's not the best choice.

[^2]: Copy-left licenses like GPL and AGPL are somewhat similar to source-available in spirit, even though they are [OSI-approved](https://opensource.org/licenses). Copy-left is used as a poison pill for anyone trying to copy and build a competing product by the fact that it forces the competitor to release the code back as open-source. All while the owner of the project can still create closed-source modifications to the project to sneak in unique advantages - the owner is allowed to because they own copyright (assuming a [CLA](https://en.wikipedia.org/wiki/Contributor_License_Agreement) is in place - like there usually is in such cases). For similar reasons, there are several databases that use a copy-left license - it makes it hard for the competition to support differentiating features, while the original author can still have closed-source differentiators.

## User Feedback

Earthly's growing user base is mostly okay with the BSL license, but there were a few cases where it seemed like a point of friction for our users. Some online license feedback we could dismiss as trolling but other interactions were genuine concerns from sophisticated prospective users.

<div class="align-center">
 {% picture {{site.pimages}}{{page.slug}}/adam-1.png --picture --img width="400px" --alt {{ the only downside is that it's not open source }} %}

 {% picture {{site.pimages}}{{page.slug}}/adam-2.png --picture --img width="400px" --alt {{ Logically I have to treat Earthly the way I would treat any other investment in proprietary software }} %}
<figcaption>Twitter conversation with Adam Jacob</figcaption>
</div>

[Adam Jacob](https://twitter.com/adamhjk) is the founder of Chef and System Initiative and he has been thinking about this topic for over a decade - [he even wrote a book](https://sfosc.org/). The 1:1 conversation that ensued after the Twitter interactions was extremely enlightening: [this twitter thread](https://twitter.com/adamhjk/status/1514628721793150977) summarizes it pretty well.

In another example, a prospective user had a hard time understanding whether BSL would be ok in his organization.

<div class="align-center">
 {% picture {{site.pimages}}{{page.slug}}/chris.png --picture --img width="400px" --alt {{ I'm unsure of how to proceed }} %}
<figcaption>Twitter conversation with Chris Lieb</figcaption>
</div>

We were able to convince Chris in the end. But he still had to jump through a few organizational hoops and you can say it's a lucky case: he reached out and we were able to clarify BSL for him. But not every prospective user is as determined as Chris.

The above is only a sample of the interactions, and again, the vast majority of our users were ok with BSL, and of those who initially weren't most ended up being ok with BSL after an explanation. But there was onboarding friction, and some users were against BSL altogether, or just didn't have the patience to look into it and just gave up.

In some cases, highly popular, foundation-owned, projects like some Apache projects and some CNCF projects wanted to take a look at Earthly, but the license was simply a non-starter for them.

Although we've had a ton of growth in a very short amount of time and although it's very difficult to perform an A/B test of the different licenses to measure growth difference, there is anecdotal evidence that led us to believe that in our case source-available has limited some growth.

## It Cannot Be a Standard Unless it's Open

Beyond that, there is the wider architectural perspective. We want to make the Earthly syntax a unifying framework on top of any CI/CD vendor. By that definition, a more open project will not only help our users integrate better with the various CI/CD vendors out there, and thus making Earthly better for everybody, but it will also consequently create a stronger community, which helps the mission from the business perspective too.

There is some analogy to be drawn about the Postgres / CockroachDB case - the syntax (the Postgres SQL dialect) is open-source, which helps foster a flourishing community ecosystem full of various vendors, community tools, integrations, and interoperability. If the syntax weren't an open standard, Cockroach wouldn't have had an ecosystem to plug a commercial product into.

As we were discussing with our network of advisors, [Chad Metcalf](https://twitter.com/metcalfc) (former Chief Architect at Docker, and an Earthly investor) said:

> If Dockerfile and Compose are analogous wouldn't the syntax becoming a standard be better in the long run? **It cannot be a standard unless it's open**. The more Earthfiles in the world the better. [...] Make it easy to fork you. But they cannot call it Earthly. The logo, the CLI name, all of that is yours. All of that work goes back to you.

In addition, the parts that are deeply integrated into the user's code are better when they are open-source. Developers are more comfortable making deep integrations with another ecosystem in such cases, as open-source prevents vendor lock-in concerns and helps justify a long-term invasive investment in the technology.

## The Future

We have made this decision with careful consideration and although there are some risks, we believe that the benefits, for both our users and for us as a business, outweigh the drawbacks significantly. We also made this decision knowing that once opened up it would be unfair to ever go back and constrain it ever again. So here we make a pledge to forever keep Earthly open-source from now on.

As we are happy to embrace open-source whole-heartedly for the Earthly project and the Earthfile syntax, we will continue to pursue a commercialization strategy that relies on open-core and an Earthly-as-a-service CI/CD freemium product, which will have proprietary components[^3].

[^3]: Some might question whether we should open up the cloud offering too. We have considered that and for now we don't have enough conviction to commit to that direction. The only company that was successful in leveraging that model is RedHat. Whereas the open-core model has significantly more data points: HashiCorp, GitLab, DataBricks, Confluent, Chef, Redis and many others. That's not to say the model cannot work or that we wouldn't explore this at a later time - we just find it hard to commit to that direction now for such an important decision that we wouldn't be able to reverse later (it would be unfair to the community to ever reverse such a decision).

## Conclusion

By internal metrics Earthly has grown 10.4x year-over-year, and although we're gaining momentum, we believe we're merely at the beginning of the journey. Companies such as ExpressVPN, Workday, Roche, Bluecore, Namely, and many others rely on Earthly every day.

Open-sourcing Earthly is the best decision for both the Earthly community and for us as the company. We're grateful for the help, support, and feedback our users have given Earthly throughout our lifetime in return and this decision is largely because of you.

In addition we would like to thank the following individuals for their help in advising on this matter. They may or may not agree with the conclusions, but their input was instrumental in educating us about the landscape and the implications: Adam Jacob (CEO System Initiative, formerly founder Chef), Chad Metcalf (GitPod, formerly Chief Architect Docker), Florian Leibert (468 Capital, formerly CEO Mesosphere), Davis Treybig (Innovation Endeavors), Amir Shevat (Innovation Endeavors), Matt Klein (creator Envoy Proxy), Spencer Kimball (CEO Cockroach Labs), Cristian Strat (CEO Runloop), Arjun Narayan (CEO Materialize), Salil Deshpande (Uncorrelated Ventures), Michael Howard (CEO MariaDB) and Sakib Dadi (Bessemer Venture Partners).

As Earthly turns two this month, we're looking forward to an even brighter and more open future. If you're new to Earthly, come [give Earthly a shot](https://earthly.dev/get-earthly) and develop CI/CD pipelines locally that run in any CI. Also, [we're hiring](https://earthly.dev/hiring)!
