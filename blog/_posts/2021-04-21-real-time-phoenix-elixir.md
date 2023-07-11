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
excerpt: Learn how to build a real-time crowdfunding application using the Phoenix Framework and Elixir. Discover the power of Phoenix LiveView and how to leverage PubSub to broadcast updates to all users in real time.
---

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
-----------+----------+----------+------------+------------+-----------------------
 postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 | ...

```

## Setting Up Phoenix

Now that you have the necessary dependencies, go ahead and install the Phoenix application generator and create your first Phoenix app. The Phoenix generator is distributed as a `mix archive` and can be installed by running the following command:

```bash
> mix archive.install hex phx_new 1.5.8
```

### Mix Archives

Mix archives are essentially `.zip` files of an Elixir project following the [Erlang Archive Format](http://erlang.org/doc/man/code.html). Simply put, archives give us a way to distribute projects and use them as a regular command tool.

### Creating a New Project

Now that the Phoenix archive is installed locally if you run `mix help`, you should see a new set of mix commands available in your system:

```bash
mix phx                   # Prints Phoenix help information
mix phx.digest            # Digests and compresses static files
mix phx.digest.clean      # Removes old versions of static assets
mix phx.gen.cert          # Generates a self-signed certificate for HTTPS testing
mix phx.gen.channel       # Generates a Phoenix channel
mix phx.gen.context       # Generates a context with functions around an Ecto schema
mix phx.gen.embedded      # Generates an embedded Ecto schema file
mix phx.gen.html          # Generates controller, views, and context for an HTML resource
mix phx.gen.json          # Generates controller, views, and context for a JSON resource
mix phx.gen.live          # Generates LiveView, templates, and context for a resource
mix phx.gen.presence      # Generates a Presence tracker
mix phx.gen.schema        # Generates an Ecto schema and migration file
mix phx.gen.secret        # Generates a secret
mix phx.new               # Creates a new Phoenix v1.5.4 application
mix phx.new.ecto          # Creates a new Ecto project within an umbrella project
mix phx.new.web           # Creates a new Phoenix web project within an umbrella project
mix phx.routes            # Prints all routes
mix phx.server            # Starts applications and their servers
```

Running `mix phx.new` from any directory will create a new Phoenix application. But before you dive in, it's crucial that you understand the options available when making a Phoenix project. Let's take a look by running the following command:

```bash
> mix help phx.new

...

  • --live - include Phoenix.LiveView to make it easier than ever to build
    interactive, real-time applications
  • --umbrella - generate an umbrella project, with one application for
    your domain and a second application for the web interface
  • --app - the name of the OTP application
  • --module - the name of the base module in the generated skeleton
  • --database - specify the database adapter for Ecto. One of:
    • postgres - via https://github.com/elixir-ecto/postgrex
    • mysql - via https://github.com/elixir-ecto/myxql
    • mssql - via https://github.com/livehelpnow/tds

    Please check the driver docs for more information and requirements.
    Defaults to "postgres".

  • --no-webpack - do not generate webpack files for static asset building.
    When choosing this option, you will need to manually handle JavaScript
    dependencies if building HTML apps
  • --no-ecto - do not generate Ecto files
  • --no-html - do not generate HTML views
  • --no-gettext - do not generate gettext files
  • --no-dashboard - do not include Phoenix.LiveDashboard
  • --binary-id - use binary_id as primary key type in Ecto schemas
  • --verbose - use verbose output
  
...

```

Let's pay attention to the first option, `--live`. As mentioned at the beginning of this tutorial, you'll be building a fundraising application, so make sure to set up your Phoenix application to allow for real-time functionality from the get-go:

```bash
> mix phx.new --live phoenix_fund

...
* creating phoenix_fund/lib/phoenix_fund_web/router.ex
* creating phoenix_fund/lib/phoenix_fund_web/telemetry.ex
* creating phoenix_fund/lib/phoenix_fund_web.ex
* creating phoenix_fund/mix.exs
* creating phoenix_fund/README.md
...

* creating phoenix_fund/assets/static/robots.txt

Fetch and install dependencies? [Yn] 
* running mix deps.get
* running mix deps.compile
* running cd assets && npm install && node node_modules/webpack/bin/webpack.js --mode development

```

`mix phx.new` will create the basic skeleton for your new Phoenix LiveView app and download all the dependencies on the Elixir and Node.js side of things.

Next, provision your database and start the local Phoenix server:

```bash
> mix ecto.create && mix phx.server
```

If everything is working correctly, you should be able to visit [localhost:4000](http://localhost:4000) and see the default Phoenix livewire homepage:

![Out of the box installation]({{site.images}}{{page.slug}}/0N5VpNv.png)

Now the app generated has the default Phoenix styling and setup, but let's add a little polish for this exercise. You're going to add [TailwindCSS](https://tailwindcss.com/) and some pre-made boilerplate CSS.

1. First, add the following dependencies to your `assets/package.json` file, to install Tailwind and the necessary node libraries:

```json
...
  "devDependencies": {
...
    "postcss": "^8.1.10",
    "postcss-import": "^13.0.0",
    "postcss-loader": "^4.1.0",
    "postcss-nested": "^4.2.1",
    "tailwindcss": "^2.0.1",
...
    }
```

2. Next, make sure to install your new dependencies:

```bash
npm install
```

3. Copy [the webpack and Tailwind configuration from this gist](https://gist.github.com/amacgregor/1369927cb4555803fa359c5ad9104fa9) into your assets directory:

```
assets/tailwind.config.js
assets/webpack.config.js
assets/postcss.config.js
```

4. Copy [these CSS files](https://gist.github.com/amacgregor/66c7fd76b55332c77bbdb21c5f62940b) into the following locations:

```
assets/css/app.css
assets/csss/custom.css
```

5. Finally change your application to use regular CSS instead of Sass by updating the `assets/js/app.js` to:

```
import "../css/app.css"
```

## Adding Your Auction Route

Now that you have a project up with the base styling, you can start working on adding the routes and logic to show the auctions. Open your `lib/phoenix_fund_web/router.ex` file and look for the following chunk of code:

```elixir
  scope "/", PhoenixFundWeb do
    pipe_through :browser

    live "/", PageLive, :index
  end
```

This is the scaffold code that was generated when you generated the application. You want to add a new route for your actions, and you can do that easily by using the `live` macro:

```elixir
 ...
 live "/auction", AuctionLive
```

It's important to highlight that `AuctionLive` is not a Phoenix controller. Rather, it's a long-running LiveView process in charge of managing and tracking the state for that particular route.

Go ahead and define your new module under `lib/phoenix_fund_web/live/auction_live.ex`. By convention, the LiveView modules are placed under the `live` directory.

```elixir
defmodule PhoenixFundWeb.AuctionLive do 
 use PhoenixFundWeb, :live_view
 
 def mount(params, session, socket) do
  {:ok, assign(socket, :raised, 0)}
 end
end
```

This is the core of a LiveView module. `mount/3` is the entry point for each LiveView, and it will be invoked twice:

- Once on the initial page load
- Once to establish a live socket

It expects three parameters:

- `params`: A map of string keys with the query params
- `session`: The connection session
- `socket`: The LiveView socket struct

In your `mount/3` function, assign the initial status for your LiveView so it can be rendered. Next, define a `render/1` function that will render your LiveView HTML.

```elixir
defmodule PhoenixFundWeb.AuctionLive do 
...
  def render(assigns) do
    ~L"""
       <h1>Cabinet of Curiosities</h1>
       <div id="auction">
           <div class="meter">
             <span style="width: <%= @raised %>%">
               $<%= @raised %> USD
             </span>
           </div>
        </div>
    """
  end
end
```

For now, you'll provide the HTML directly on your function. Note that the `~L` is a special syntax called a sigil; it's used to represent Live EEx content.

Start your Phoenix server and let's try to load [/auction](http://localhost:4000/auction). If everything was set up correctly, you should see the following:

![Auction View]({{site.images}}{{page.slug}}/6gnnM9k.png)

Excellent! Your new route is now being rendered by your LiveView. Now it's time to make it do something useful by adding a couple of buttons to allow people to donate.

```elixir
```elixir 
defmodule PhoenixFundWeb.AuctionLive do 
...
  def render(assigns) do
    ~L"""
       <h1>Cabinet of Curiosities</h1>
       <div id="auction">
           <div class="meter">
             <span style="width: <%= @raised %>%">
               $<%= @raised %> USD
             </span>
           </div>
           
        <button phx-click="donate-1"> $1 </button>
           <button phx-click="donate-5"> $5 </button>
           <button phx-click="donate-10"> $10 </button>
           <button phx-click="donate-100"> $100 </button>
        </div>
    """
  end
end
```

The page should look as follows:

![Buttons added]({{site.images}}{{page.slug}}/kI2Zchu.png)

However, if you try to click any of your new buttons, you're going to get an error like so:

```
{% raw %}
[error] GenServer #PID<0.935.0> terminating
** (FunctionClauseError) no function clause matching in PhoenixFundWeb.AuctionLive.handle_event/3
    (phoenix_fund 0.1.0) lib/phoenix_fund_web/live/auction_live.ex:26: PhoenixFundWeb.AuctionLive.handle_event("donate-5", %{"value" => ""}, #Phoenix.LiveView.Socket<assigns: %{flash: %{}, live_action: nil, live_module: PhoenixFundWeb.AuctionLive, raised: 34}, changed: %{}, endpoint: PhoenixFundWeb.Endpoint, id: "phx-FmnbLK6vHaXG9gIk", parent_pid: nil, root_pid: #PID<0.935.0>, router: PhoenixFundWeb.Router, view: PhoenixFundWeb.AuctionLive, ...>)
    (phoenix_live_view 0.13.0) lib/phoenix_live_view/channel.ex:102: Phoenix.LiveView.Channel.handle_info/2
    (stdlib 3.14) gen_server.erl:689: :gen_server.try_dispatch/4
    (stdlib 3.14) gen_server.erl:765: :gen_server.handle_msg/6
    (stdlib 3.14) proc_lib.erl:226: :proc_lib.init_p_do_apply/3
Last message: %Phoenix.Socket.Message{event: "event", join_ref: "4", payload: %{"event" => "donate-5", "type" => "click", "value" => %{"value" => ""}}, ref: "39", topic: "lv:phx-FmnbLK6vHaXG9gIk"}
State: %{components: {%{}, %{}, 0}, join_ref: "4", serializer: Phoenix.Socket.V2.JSONSerializer, socket: #Phoenix.LiveView.Socket<assigns: %{flash: %{}, live_action: nil, live_module: PhoenixFundWeb.AuctionLive, raised: 34}, changed: %{}, endpoint: PhoenixFundWeb.Endpoint, id: "phx-FmnbLK6vHaXG9gIk", parent_pid: nil, root_pid: #PID<0.935.0>, router: PhoenixFundWeb.Router, view: PhoenixFundWeb.AuctionLive, ...>, topic: "lv:phx-FmnbLK6vHaXG9gIk", transport_pid: #PID<0.929.0>}
{% endraw %}
```

## Handling Events

As you can see from the error, the Auction LiveView doesn't currently know how to handle an event. As part of your button code, you added `phx-click`; this is a **binding** that sends a particular event like `donate-1` back to your LiveView.

Your next step is adding a new definition of `handle_event/3` for each one of your events. Go ahead and add the first function definition to the handle of the $1 donation button event:

```elixir
defmodule PhoenixFundWeb.AuctionLive do 
...
  def handle_event("donate-1", _, socket) do
    raised = socket.assigns.raised + 1
    {:noreply, assign(socket, :raised, raised)}
  end
end
```

The `handle_event/3` function takes three parameters:

- The name of the event, in this case `donate-1`
- The `metadata` about the event, that you can safely ignore for now
- The `socket`, which, if you remember, holds the state of your LiveView process

Inside your `handle_event/3`, you're doing two things:

- Retrieving the current `raised` value from the `socket.assigns` and increment it by `1`
- Assigning the new value back to the socket

If you reload your page and click on the $1 donation button, you should see the value correctly incrementing.

![Button working]({{site.images}}{{page.slug}}/WA1gHtv.gif)

Make sure to add the following code to handle the remaining events:

```elixir
defmodule PhoenixFundWeb.AuctionLive do 
...
  def handle_event("donate-5", _, socket) do
    raised = socket.assigns.raised + 5
    {:noreply, assign(socket, :raised, raised)}
  end

  def handle_event("donate-10", _, socket) do
    raised = socket.assigns.raised + 10
    {:noreply, assign(socket, :raised, raised)}
  end

  def handle_event("donate-100", _, socket) do
    raised = socket.assigns.raised + 100
    {:noreply, assign(socket, :raised, raised)}
  end  
end
```

## Understanding the LiveView Life Cycle

![LiveView Life Cycle]({{site.images}}{{page.slug}}/rk4dJHg.png)

Let's recap what you've done so far to better understand the LiveView life cycle:

1. Your application receives a request for a LiveView route.
2. Your app will invoke that view `mount/2` function and set the initial socket state.
3. Next, it will call `render/1` to render the static HTML to send back to the client.
4. Opening a LiveView socket will pass the rendered HTML.
5. The socket will remain open to receive events and handle updates on the LiveView process state.

It is in this life cycle where one of the more powerful and interesting features of LiveView lies. As mentioned, LiveView is listening to your socket for updates but _it will only rerender the portions of the page that needed updating_. In the case of this tutorial, the meter is the only piece that gets an update.

This is one of the key features that makes Phoenix and LiveView extremely well suited for real-time applications.

## Broadcasting With PubSub

So far, you've built an app that can leverage Phoenix LiveView to allow users to donate in real time, but so far, there's a caveat: updates are not shared across users or even tabs. Wouldn't it be nice to get the donations to show in real time for everyone who has the page open?

Next, you'll leverage [PubSub](https://github.com/phoenixframework/phoenix_pubsub) to broadcast real-time updates to all LiveView clients, not just the one that triggers the event.

> "Publish-subscribe is a messaging pattern where senders of messages, called publishers, do not program the messages to be sent directly to specific receivers, called subscribers, but instead categorize published messages into classes without knowledge of which subscribers, if any, there may be. Similarly, subscribers express interest in one or more classes and only receive messages that are of interest, without knowledge of which publishers, if any, there are." –[Wikipedia](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern)

In short, PubSub is a messaging pattern that will allow us to implement real-time asynchronous communication with any clients listening for events in our application. In the case of this tutorial, that will be every user with a fundraising page open.

### Configure Phoenix PubSub

First, you need to configure your app endpoint to use the `Phoenix.PubSub.PG2` adapter. Add the following configuration to your `lib/phoenix_fund/application.ex`:

```elixir
{Phoenix.PubSub, [name: PhoenixFund.PubSub, adapter: Phoenix.PubSub.PG2]},
```

### Subscribing to a Topic

Next, tell your LiveView process to subscribe to a specific topic when the LiveView mounts. You can leverage `Phoenix.PubSub.subscribe/3` for that:

```elixir
defmodule PhoenixFundWeb.AuctionLive do
  use PhoenixFundWeb, :live_view
  
  @topic "auction"

  def mount(params, session, socket) do
   PhoenixFundWeb.Endpoint.subscribe(@topic)
    {:ok, assign(socket, :raised, 0)}
  end
...
end
```

You'll use a generic `auction` topic, as you're only dealing with a single auction.

### Broadcasting to All Subscribers

Your next step is to modify each of your `handle_event/3` definitions to broadcast. The updated code looks like:

```elixir
  def handle_event("donate-1", _, socket) do
    raised = socket.assigns.raised + 1
    PhoenixFundWeb.Endpoint.broadcast_from(self(), @topic, "donate_event", raised)
    {:noreply, assign(socket, :raised, raised)}
  end

  def handle_event("donate-5", _, socket) do
    raised = socket.assigns.raised + 5
    PhoenixFundWeb.Endpoint.broadcast_from(self(), @topic, "donate_event", raised)
    {:noreply, assign(socket, :raised, raised)}
  end

  def handle_event("donate-10", _, socket) do
    raised = socket.assigns.raised + 10
    PhoenixFundWeb.Endpoint.broadcast_from(self(), @topic, "donate_event", raised)
    {:noreply, assign(socket, :raised, raised)}
  end

  def handle_event("donate-100", _, socket) do
    raised = socket.assigns.raised + 100
    PhoenixFundWeb.Endpoint.broadcast_from(self(), @topic, "donate_event", raised)
    {:noreply, assign(socket, :raised, raised)}
  end
```

You're using the `Phoenix.PubSub.broadcast_from/4` function, which allows you to broadcast a message describing a new socket state to all the LiveView clients that are subscribed to a topic. Notice that you're not triggering the click event on the other clients, just letting them know that the socket state has changed.

Finally, now that you're broadcasting the socket updates, you need to tell your LiveView process how to handle the incoming broadcasts. For this, add a `handle_info/2` that will pattern match against the broadcast struct:

```elixir
  def handle_info(%{topic: @topic, payload: raised}, socket) do
    {:noreply, assign(socket, :raised, raised)}
  end
```

If you start up your application and open two browser windows side by side, you should see the donation meter updating on all windows as soon anyone clicks any of the donation buttons.

![Broadcast in real time]({{site.images}}{{page.slug}}/tiqB8O5.gif)

## In Summary

As you've learned, Phoenix offers a powerful set of libraries, making it relatively easy to create real-time applications with very little code and, even more surprisingly, no JavaScript at all. With LiveView, you can create fully fledged real-time features using only server-side code, and when you add Phoenix PubSub, you can open those same features to all app users in real time.

Of course, we've only begun to scratch the surface here of what you can do with Phoenix, LiveView, and PubSub. If you want to keep going with this project, I would recommend tackling adding persistence next, and the ability to create multiple auctions with [Ecto](https://hexdocs.pm/ecto/getting-started.html).

Both Ecto and the Phoenix project use [Earthly](https://earthly.dev) for defining their continuous integration process, so examining [those](https://github.com/elixir-ecto/ecto/blob/master/Earthfile) [projects](https://github.com/phoenixframework/phoenix/blob/master/Earthfile) can be a great way to learn more about Earthly.

### Additional Resources

- [The Pragmatic Studio: Phoenix LiveView Course](https://pragmaticstudio.com/phoenix-liveview)
- [_Programming Phoenix LiveView_](https://pragprog.com/titles/liveview/programming-phoenix-liveview/)
- [Full source code](https://github.com/amacgregor/phoenix_fund)
