---
title: "How Blue-Green Deployments Work in Practice"
categories:
  - Articles
toc: true
sidebar:
  nav: "deployment-strategies"
author: Taurai Mutimutema
internal-links:
 - blue green
excerpt: |
    Learn how blue/green deployments can eliminate downtime and errors when updating applications, and discover best practices and tools to streamline the process.
---
**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. This article is about blue/green deployments. Earthly is a powerful build tool for streamlining a deployment processes. [Check us out](/).**

Remember when systems would go offline to implement changes and updates? Sometimes you still get emails from applications with notifications of downtime, apologizing in advance for any interruption. That's a costly and outdated way of maintaining applications that are constantly evolving.

These days, blue/green deployments address the downtime and embarrassing errors that are commonly associated with taking an application offline for updates.

This guide explains blue/green deployments and shares best practices for running them seamlessly. You'll also discover industry-leading tools and techniques to reduce the friction of deploying new application versions continuously.

## What to Know Before Using Blue/Green Deployment

The term *blue-green* describes the concept of two production environments hosting two versions of the same application. The duality allows one environment to work as a staging environment while traffic accesses the stable rendition of the app in the production environment.

In practice, the two environments used for blue/green transitions share a few resources and a single underlying database. This reduces the cost and complexity of managing two applications.

## How Blue/Green Deployments Work

Let's take a step-by-step example to understand how a blue/green deployment process looks like from start to finish.

The first step to running a blue/green deployment scheme for your organization involves duplicating your production environment. You'll need to provision the same specifications and resources for both blue and green environments to minimize any application runtime errors caused solely by environmental changes. At any given time, only one of these - let's say blue - is live to the users. Usually, a router or a load balancer is responsible for directing traffic to the live environment. The non-live environment - green in this example - acts as the staging server and can only be accessed through a private network.

When you're ready to release a new update, you deploy the new version to the green environment and perform the final testing. Once you are sure it works as intended, you can switch the traffic from the blue environment to the green one. Once all the traffic has been switched, the green server becomes the production server and the blue server becomes the staging server.

The blue server can now be used for testing and deploying the next release following the same procedure, or it can be used to rollback to the previous version by simply switching traffic back to the blue environment.

### Managing Data During Blue/Green Changeovers

Now you have a clear picture of how blue/green deployment works. But what about the database? It's highly likely that at some point of time, you need to make changes to the database schema. How does the blue/green process look like in that case? And how do you handle rollbacks?

You could run two different production databases for the two environments, but synchronizing data between two databases with possibly different schema is an extremely complex process and out of the scope of this article. The easier way to use a single versioned database and some tweaks to the deployment process.

Versioning the database can be done with tools like [FlyWay](https://flywaydb.org/) or by using a framework like Ruby on Rails that support database versioning natively. In this approach all your database changes are annotated with a version identifier. As an example, imagine your `users` table has a non-nullable column `birthday` that is used to track the age of users and you want to replace this column with a non-nullable `age` column that will store the age directly. For a typical deployment, you would add the `age` column, run a backfill script to populate the `age` column from `birthday` and delete the `birthday` column, and then deploy the updated code that references the new `age` column. These approach will, however, not work in a blue/green scenario, because while you're testing your new code, the live environment will still be referencing the old `birthday` column and will stop working.

To solve this and also to be able to rollback in need, you'll need multiple deployments. Let's say, your database at version `v1` uses the `birthday` column. The first step is to create a new version `v2` of the database that simply adds the `age` column as a **non-nullable** column, without touching the `birthday` column. Then, change your code to reference both the `age` and `birthday` columns. This code should store data in both `age` and `birthday` columns, but for reading data it should try the `age` column first and if it's `null`, it should fallback to `birthday`. This ensures that any new data has both the columns set so that rollback can be performed without any issue. This code should be deployed to the green environment and follow the usual procedure to become the live environment.

Rolling back at this point can be done using the usual procedure, since both the `birthday` and `age` column are present in the database.

In the next release, you can upgrade the database to version `v3` that simply fills in the `age` column from the `birthday` column and drops the `not null` constraint from the `birthday` column. The code can now be changed to drop all references to `birthday` altogether. Once this code is live, rollback is still possible as usual, since the previous version uses both the columns.

Finally, the database can be upgraded to `v4` where you simply drop the `birthday` column and add the `not null` constraint to the `age` column.

### CI/CD and Blue/Green Deployments

Automated deployment has to be the norm before you implement a blue/green strategy in order to remove complexities with the changeover process.

Continuous delivery makes it possible for the application branch in the staging environment to take form seamlessly. Developers add code and integrate it automatically to the previous version with automated tests and lint error removal during static code analysis. However, deployment is left to an ultimate check and green-light process by your engineers.

Continuous deployment takes the process further by automating the deployment and changeover processes. Typically, this workflow comprises small batch-processing events and the creation of build-files with new dependencies. Then there's an automated test of the new build for compatibility with the staging environment and finally, pushing all approved changes as ready for a blue/green switch.

The key to running a successful blue/green deployment is ensuring the replicability and stability of both environments. As the application evolves, either of them could become the production and traffic destination. Keeping that in mind, one of the crucial areas to optimize your transitions around is handling requests made during the blue-to-green (or reverse) transition. In a nutshell, "in-flight" request management is left to the load balancer to delay and route accordingly as soon as the new production environment is stable.

Some cloud service providers mitigate this delay by running an [environment preboot](https://devcenter.heroku.com/articles/preboot). This is an effective way of enhancing the load balancer traffic routing action as the environment "warms up" in anticipation of incoming requests.

Even with preboot and an intuitive load balancer, there may still be errors encountered during the switch. For these situations, you should institute an automatic and instant rollback to the previous version of the application.

### Use Cases for Blue/Green Deployments

Blue/green deployments are particularly useful when **maintaining time-sensitive applications**. Yes, every application should stay online persistently, but if you stand to lose money each time an update takes your systems offline, then you should consider the environment duality path.

Sometimes you find yourself wishing you had **a quick (non-disruptive) rollback option**. You can hit that all-important rewind button on system updates by reverting to the old application version. You simply divert traffic to your staging environment.

Application feature flagging and **regional segregation of traffic** are also easy to implement with an active blue/green setup. The router can direct traffic to a fitting version of the application, or even call features and services in a different environment when needed.

No matter how much effort you make to ensure that your staging and production environment are identical, there will always be minor discrepancies. An application that passes the tests in the staging environment can still run into edge cases when pushed to production. With blue/green deployment, you essentially get the ability to "test in production." Since both the environments are actual production environments, you can easily verify your applications behavior before making it live.

## The Challenges of Blue/Green Deployments

As mentioned, the initial setup for blue/green deployments can be an arduous process. So before you set out on this path, there are a few challenges you need to stay ahead of if you're going to ever achieve successful blue/green deployments.

- **The cost of two production environments.** The two environments are not negotiable. Let stakeholders know where the inflated resource costs are coming from before the idea gets shot down.
- **Increased complexity.** While it makes for smooth transitions (eventually), blue/green deployments introduce a new degree of difficulty in maintaining applications. This risk burdens developers more than other stakeholders.
- **Advanced database handling.** Blue/green deployments require an intricate database management strategy, particularly for transitions. With incremental changes deployed daily, you'll need to address this challenge frequently.

## Conclusion

Blue/green deployments are a clever way to push new application versions without disrupting the end-user experience. Essentially, you need two environments that interchangeably step in as the production version residence and traffic destination. All of this is facilitated by a load balancer.

As simple as blue/green deployments appear on the surface, the actual build process can deter engineers. Double the maintenance workload, a more complex database migration procedure, and the need to quickly resolve errors during an environment switch can all add up to some serious hindrances.

However, the benefits and seamless application versioning experience often outweigh the costs and complexities associated with blue/green deployments. Also, a solid, repeatable build – which can be achieved with tools like  [Earthly](https://earthly.dev/) – can help ease the complexities of a blue/green deployment cycle.

{% include_html cta/bottom-cta.html %}
