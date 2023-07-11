---
title: 'Building a Real-Time Application in the Phoenix Framework with Elixir'
categories:
  - Tutorials
toc: true
author: Allan MacGregor
internal-links:
    - phoenix
    - elixir
    - liveview
excerpt: |
    Learn how to build a real-time crowdfunding application using the Phoenix Framework and Elixir. Discover the power of Phoenix LiveView and how to leverage PubSub to broadcast updates to all users in real time.
---
<!--sgpt-->**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. This article is about building a real-time application in the Phoenix Framework with Elixir. Earthly is a powerful build tool that can greatly enhance your development workflow when working with Elixir and Phoenix. [Check us out](/).**

The Elixir language, along with the [Phoenix framework](https://phoenixframework.org/), has been growing in popularity at a quick pace, and with good reason. Phoenix offers productivity levels comparable to frameworks like Ruby on Rails while being one of the [fastest web frameworks](https://github.com/mroth/phoenix-showdown/blob/master/RESULTS_v3.md) available.

If you're currently working with a web framework like Ruby on Rails or even Laravel, you should definitely give Phoenix some attention due to the performance gains it promises. Additionally, Phoenix also has the capability to build highly responsive real-time applications.

## Introducing Phoenix LiveView

[Phoenix LiveView](https://github.com/phoenixframework/phoenix_live_view) is a relatively new library added to the Phoenix stack. Developers can build rich, real-time user experience with purely server-rendered HTML.

Phoenix LiveView adds bi-directional communication via WebSockets between the server and the client, without needing dedicated JavaScript code on the frontend. This allows you to implement real-time functionality on your applications with ease.

## Explaining Today's Tutorial

For this tutorial, we are going to be building a crowdfunding application that will leverage the real-time capabilities of Phoenix LiveView. Our application will allow users to support a funding goal in real-time and see the funding goal update as other users also commit to a specific amount. We'll call it Phoenix Fund.

The goal of this application is not to build a fully-featured crowdfunding platform but to get your feet wet with LiveView:

- How LiveView views works and renders
- How Phoenix leverages WebSockets for communication
- How to implement real-time updates on your application
- How the LiveView life cycle works

Here's a sample of how the final application will work:

![The Crowdfunding App]({{site.images}}{{page.slug}}/q0L1xth.gif)

## Pre-Build Setup

For this tutorial, make sure you have a good working Elixir environment. The easiest way to do this is to follow the [official Elixir instructions](https://elixir-lang.org/install.html), which will give you a couple of options for:

- Local installation on Linux, Windows, and macOS
- Dockerized versions of Elixir
- Package manager versions setups

I would recommend focusing on the local install for this tutorial, as it might be the easiest one to get started. Additionally, you will need to have [npm](https://www.npmjs.com/) installed locally and a running version of PostgreSQL.

### npm

You can easily install Node.js from their [official instructions](https://nodejs.org/en/), but in most cases, it's possible your system might already have Node preinstalled.

### Postgres
<!-- markdownlint-disable MD029 -->
[Postgres](https://www.postgresql.org/) can be a little tricky to install depending on the operating system you're using. For this tutorial, you can leverage Docker and get a local version running by taking the following steps:

1. Create a folder to persist the DB data.

```bash
> mkdir ${HOME}/phoenix-postgres-data/
```

2. Run a Docker container with the Postgres image.

```bash
$ docker run -d \
 --name phoenix-psql \
 -e POSTGRES_PASSWORD=Phoenix1234 \
 -v ${HOME}/phoenix-postgres-data/:/var/lib/postgresql/data \
 -p 5432:5432 \
 postgres
```

3. Validate that the container is running.

```bash
> docker ps

CONTAINER ID   IMAGE      COMMAND                  CREATED         STATUS        PORTS                                  NAMES
11cbe1d2bc2f   postgres   "docker-entrypoint.s…"   6 seconds ago   Up 5 seconds  5432/tcp, 0.0.0.0:5432->5432/tcp       phoenix-psql
I can
that was
```

4. Validate PostgreSQL is up and running.

```bash
> docker exec -it phoenix-psql bash

root@11cbe1d2bc2f:/# psql -h localhost -U postgres

psql (13.2 (Debian 13.2-1.pgdg100+1))
Type "help" for help.

postgres=# \l
                                 List of databases
   Name    |  Owner   | Encoding |  Collate   |   Ctype    |   Access privileges