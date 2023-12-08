---
title: You're using docker-compose wrong
categories:
  - Articles
author: Vlad
sidebar:
  nav: "docker"
internal-links:
   - docker compose
excerpt: |
    Learn how to avoid common mistakes when using docker-compose for integration testing and development environments. Discover the cardinal sins to avoid and best practices to follow for a smoother Docker experience.
last_modified_at: 2023-07-14
---
**In this article, you'll discover common Docker Compose errors. Struggling with docker-compose in your CI workflows? Earthly simplifies your integration testing with consistent builds. [Learn how](https://cloud.earthly.dev/login).**

<!-- vale HouseStyle.H2 = NO -->
Tell me if this sounds familiar? You were introduced to docker-compose either by choice or by force. You've been using it for a while, but you find it clunky. I'm here to tell you, you are probably using it wrong.

Ok, that might be an exaggeration. I don't think there's actually a 100% right or wrong way to use it: home-grown build and dev setups tend to have all kinds of [weird](/blog/dont-be-weird) requirements and so the standard doesn't always match the needs. Please take the article with the appropriate skepticism if your situation doesn't quite fit.

I, myself, have been guilty of each of these in the past and I might be in the future as well!!

In any case, here is a rundown of some of the cardinal sins that I found myself making while using docker-compose.

In this article, I'll be focusing on use-cases related to **integration testing** and using docker-compose as a **development environment**. For production use, I think docker-compose is usually ill-suited.

## Problem #1: You're using the host network

One of the first things new-comers find cumbersome is the use of [Docker networks](/blog/docker-networking). It's yet another layer of knowledge to add to your repertoire after you get used to the basics of **docker build** and **docker run** … and frankly, why do you even need to understand these Docker networks? Everything works fine via the host network, right? Wrong!

Using the host network means that you have to reserve specific ports for the various microservices that you use. If you happen to bring up two stacks that collide on ports, tough luck. If you want to bring up two versions of the same stack, tough luck. You want to test the behavior of a certain service when it has multiple replicas? Tough... luck!

By default, docker-compose spins up its containers on a separate network called **\<project-name\>\_default** (where **\<project-name\>** is by default the name of the directory). So really, you don't need to do anything special in order to take advantage of Docker networks.

This network gives you a number of benefits right off the bat:

- It's a network more isolated from your host network - so it's less likely that the specifics of your system environment will cause the compose setup to behave differently. You have access to the internet, but any ports that you wish to be accessible from the host need to be declared with a port bind.
- If a service starts listening on 0.0.0.0 (the way containers should), then a host network setup will open up that port on your WLAN. If you use a Docker network, it'll only expose that port to that network.
- You can talk between services by using their compose names as host names. So if you have a service called **db** and within it there's a service listening on port **5432** , then you can access it from any other service via **db:5432**. This is typically more intuitive than **localhost:5432**. And because there is no risk of localhost port clashing, it has a greater chance to be more consistent when used across different projects.
- Most ports don't need to be opened up to the host too - which means that they are not competing on global resources, should you need to increase the replication via [**--scale**](https://docs.docker.com/compose/reference/up/).

## Problem #2: You're binding ports on the host's 0.0.0.0

I've seen it everywhere, you've seen it everywhere, everybody saw it everywhere: binding ports as **8080:8080**. At first glance, this looks innocuous. But the devil is in the details. This extremely common port bind is not just forwarding a container port to the localhost - it forwards it to be accessible on every network interface on your system - including whatever you use to connect to the internet.

This means that it's very likely that your development containers are constantly listening on your WLAN - when you're home, when you're in the office, or when you're at McDonald's. It's always accessible. This can be dangerous. Don't do that.

"But Vlad, I use **ufw** , my ports aren't accessible by default".

That may be true - but if you use this docker-compose setup as a team, one of your teammates might not have a firewall on their laptop.

The fix is very easy: Just add **127.0.0.1:** in front. So for example **127.0.0.1:8080:8080**. This simply tells docker to only expose the port to the loopback network interface and nothing else.

## Problem #3: You're using sleep to coordinate service startup

I have a confession to make. I'm 100% guilty of this.

The main reason this is such a complicated issue is that there is no support from Docker or Docker Compose to address this. Version 2.1 of the docker-compose format used to have a **depends\_on** option called **condition** which could be set to **service\_healthy**. And also, each service could have a **healthcheck** command which could tell docker-compose what "healthy" means. Well, this is [no longer available in Version 3.0](https://docs.docker.com/compose/compose-file/#depends_on) and [no replacement](https://stackoverflow.com/questions/47710767/what-is-the-alternative-to-condition-form-of-depends-on-in-docker-compose-versio) is offered for it.

Docker's docs basically [recommend](https://docs.docker.com/compose/startup-order/) that your service is made resilient to other services not being around for a while because that's what might happen in production anyway, if there's a short network bleep, or if a service restarts. Can't argue with that logic.

Where it gets a bit more cumbersome is when you run an integration test and the routines meant for initializing the test environment (for example pre-populating the database with some test data) end up not being resilient to starting before the other service is ready. So the argument about "it should be resilient in production anyway" doesn't quite apply here, because the code to populate the DB with test data is never used in production.

For such cases, you need something that waits for services to be ready. Docker recommends using [wait-for-it](https://github.com/vishnubob/wait-for-it), [Dockerize](https://github.com/jwilder/dockerize) or [wait-for](https://github.com/Eficode/wait-for). Note, however, that a port being ready isn't always a sign that the service is ready to be used. For example, in an integration test using a certain SQL DB with a certain schema, the port becomes available when the DB is initialized, however, the test might only work after a certain schema migration has been applied. You may need application-specific checks on top.

## Problem #4: You're running the DB in docker-compose, but the test on the host

Here is a situation: you want to run some unit tests but those tests depend on some external services. Maybe a database, maybe a Redis, maybe another API. Easy: let's put those dependencies in a docker-compose and have the unit test connect to those.

That's great - but note that your tests aren't exactly just unit tests anymore. They are now [integration tests](/blog/unit-vs-integration). Besides the nomenclature, there is an important distinction to take into account now: you'll need to account for a setup of the test environment and a teardown. Usually, it's best for the setup/teardown to be performed outside of the test code - main reason being that there may be multiple distinct packages depending on these external services. But YMMV.

If you do end up separating test setup and teardown, you could go the extra mile and containerize your integration test. Hear me out!

Containerized tests mean:

- You are on the same Docker network, so the connectivity setup is the same you would use for running your service in compose anyway. Configuration becomes cleaner.
- You may be able to reuse the code used to wait for other services to be ready in your setup/teardown.
- The integration test does not depend on any other local system configuration or environment setup, such as say… your JFrog credentials, or any build dependencies. A container is isolated.
- If another team needs to run your tests against an updated version of a service the tests depend on, you can just share the integration testing image - no need for them to compile or to set up a build toolchain.
- If you end up with multiple separate integration test containers, you can typically run all of them at the same time in parallel.

A tip for using containerized integration tests is to use a separate docker-compose definition for them. For example, if most of your services exist in **docker-compose.yml** , you could add **docker-compose.test.yml** with integration test definitions. This means that **docker-compose up** brings up your usual services, while **docker-compose -f docker-compose.yml -f docker-compose.test.yml up** starts your integration tests. For a full example on how to achieve this, see this excellent [docker-compose integration testing](https://github.com/george-e-shaw-iv/integration-tests-example) repository from Ardan Labs.

Ok, ok - calling this out as being wrong isn't entirely fair. There are many situations where not containerizing is preferable. As a simple example, many languages have deep IDE integrations which make inserting a container between the language and the IDE pretty much impossible. There are many valid productivity reasons not to do this.

## Conclusion

Docker Compose can be an amazing tool for local development purposes. Although it has a few gotchas, it usually brings a lot of productivity benefits to many engineering teams, especially when used in conjunction with integration tests.

If you're looking for more flexibility in defining containerized tests than docker-compose alone can provide, take a [look](https://github.com/earthly/earthly/blob/0f48f14/examples/integration-test/Earthfile#L38-L44) at [integration test support](https://docs.earthly.dev/guides/integration) in [Earthly](https://cloud.earthly.dev/login).
<!-- vale HouseStyle.H2 = YES -->
