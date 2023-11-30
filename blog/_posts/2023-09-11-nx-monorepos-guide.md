---
title: "Getting Started with Nx Monorepos: A Beginner's Guide"
categories:
  - Tutorials
toc: true
author: Aniket Bhattacharyea
editor: Ubaydah Abdulwasiu

internal-links:
 - guide to nx monorepos
 - starting with nx monorepos
 - introduction to nx monorepos
 - nx monorepos for beginners
excerpt: |
    This article introduces Nx, a powerful build tool for managing monorepos. It explains the benefits of using Nx, such as seamless code sharing, efficient task management, caching, and extensibility, and provides a step-by-step guide on how to create and manage a monorepo with Nx.
last_modified_at: 2023-10-06
---
**This article explains how to manage monorepos using Nx. Earthly ensures reproducible builds for monorepo workflows, regardless of programming langauge. [Check it out](/).**

Imagine you have a collection of distinct but interrelated projects. For instance, you might have an app with its own [React](https://react.dev/) frontend and [Node.js](https://nodejs.org/en/) backend, or two different [Angular](https://angular.io/) applications sharing a common collection of components. Monorepos offer an effective solution to organize these distinct but interrelated projects into a single repository.

With a monorepo, all related projects can be housed in a single location, providing clear visibility over all your projects. When you make new changes to one project, you can easily assess how it impacts the others.

Monorepos facilitate seamless code sharing, collaborative work on projects, and synchronization of releases across different projects. However, managing multiple interdependent projects within a single repository requires a capable [build tool](https://earthly.dev/blog/monorepo-tools/), such as [Nx](https://nx.dev), to efficiently handle the intricacies.

If you're looking to learn more about Nx and how it works, this article is for you. You'll learn all about Nx, including its pros and cons. You'll also learn how to create and manage a monorepo with Nx.

## Monorepos and Monorepo Tools

![Monorepo Tools]({{site.images}}{{page.slug}}/monorepo-tools.png)\

A majority of software projects are made up of smaller, interlinked components. While it may be tempting to put them in separate repositories, it may become convoluted as the number of components and the dependencies between them grows.

If you have different components across different repositories and different teams working on them, each team will likely introduce its tooling and styles. Since the projects are isolated, it's also possible that one project will be updated with a change that breaks the projects that depend on it.

By consolidating all the projects in a single monorepo, you can have a bird's-eye view of all your projects in one place as well as centralized tooling, style guides, and tests. You can also easily manage the impact of changes and improve synchronization between projects.

Monorepos also introduce new complexities since you have multiple projects in a single repo. Building and testing projects require special attention since the projects may depend on each other. This is why monorepos require specialized [build tools](https://earthly.dev/blog/monorepo-tools/) that take the pain out of managing multiple projects. Some famous monorepo tools are [Bazel](https://bazel.build), [Turborepo](https://turbo.build/repo), and Nx.

Nx is a fast and extensible monorepo build tool from [Nrwl](https://github.com/nrwl) and is used by companies such as Walmart, FedEx, and Shopify to efficiently manage their monorepos. Originally designed for handling Angular monorepos, Nx has expanded its capabilities over time to encompass various JavaScript frameworks such as React, Node.js, and even languages outside JavaScript, such as Go, C#, and Rust.

In Nx, a monorepo is known as a workspace. Each workspace can have multiple (possibly interdependent) projects.

### Pros

Some of the advantages of Nx include the following:

#### Integration With Frameworks and Tools

As previously stated, Nx integrates with popular JavaScript frameworks, such as React, [Vue](https://vuejs.org/), Angular, [Express](https://expressjs.com/), and [Expo](https://expo.dev/); testing frameworks, such as [Jest](https://jestjs.io/) and [Cypress](https://www.cypress.io/); and bundlers, such as [Vite](https://vitejs.dev/) and [webpack](https://webpack.js.org/). Apart from these JavaScript technologies, Nx also offers support for frameworks in other languages, such as Flutter and .NET, as well as tools such as [Firebase](https://firebase.google.com/).

The modular plugin system of Nx means that you can only install support for languages that you require. This extensibility and a large selection of languages and frameworks make Nx a great choice for a variety of monorepo projects.

Nx also has official extensions for [VS Code and JetBrains IDEs](https://nx.dev/core-features/integrate-with-editors#integrate-with-editors) as well as a community-maintained plugin for [Neovim](https://github.com/Equilibris/nx.nvim). These extensions make it easy to configure and use Nx straight from the editor.

#### Tasks

Nx comes built-in with common tasks such as `serve`, `build`, and `test`, which are generally used to run a development server in all projects, build distributable copies of all projects, and run unit tests in all projects, respectively. It's also possible to add new tasks in `nx.json`, or you can [run tasks in parallel](https://nx.dev/concepts/task-pipeline-configuration#run-tasks-in-parallel) for maximum efficiency.

#### Caching and Affected Mechanism

Nx offers caching of dependencies and task results, with optional remote caching through [Nx Cloud](https://nx.app/). It has a generous free tier as well as a free tier for personal and open source software usage. Even if you don't opt into using Nx Cloud, by default, Nx uses a local computation cache that is saved for one week. This helps speed up building and testing by replaying tasks from the cache instead of running it from scratch.

Another noteworthy feature of Nx that enhances the efficiency of working with monorepos is the "affected" mechanism. With this mechanism, you can selectively build and test only those projects that have been impacted by the most recent changes.

#### Introspection Tools

With Nx, you have the option to visualize the projects within your monorepo using the `nx graph` command. This command generates a graphical representation of the projects and their interdependencies on an HTML web page. This visualization allows you to easily understand the architecture of your monorepo.

#### Extensibility

Nx demonstrates its extensibility with the use of plugins. These plugins enable seamless integration with additional frameworks and tools, expanding Nx's capabilities significantly. For instance, the [DDD](https://github.com/angular-architects/nx-ddd-plugin) plugin provides domain-driven design support.

In addition, Nx offers flexibility in how you use it. You can utilize Nx for both monorepos, managing multiple interdependent projects, as well as stand-alone projects. In the latter case, you can benefit from the preconfigured tooling and plugins provided by Nx, even with just a single project.

When it comes to monorepos, Nx offers two options: [package-based](https://nx.dev/concepts/integrated-vs-package-based#package-based-repos) and [integrated](https://nx.dev/concepts/integrated-vs-package-based#integrated-repos) repos. Each approach serves different project requirements and preferences.

Integrating Nx into an existing project [is a breeze](https://nx.dev/getting-started/intro#adding-nx-to-an-existing-project-or-monorepo), thanks to its user-friendly nature and adaptability.

### Cons

While Nx comes with numerous advantages, it's important to be aware of some of its drawbacks:

* Nx has limited language support. It doesn't support commonly used languages like Java or C++. Even though it supports languages like Go, it's predominantly used for JavaScript and TypeScript-based projects.
* Apart from the graph and affected mechanism, Nx has very little build introspection capabilities compared to something like Bazel or Earthly.
* Nx only offers extensions for VS Code, JetBrains, and Neovim, which can be frustrating if you're used to using another editor.

## Implementing Monorepos With Nx

Now let's create a monorepo consisting of the following projects:

1. Two React applications: `customer` and `admin`.
2. A React library named `common-components` that will have components shared by the previous two React applications.
3. A Node.js server named `backend`.
4. A TypeScript library named `functions` that will be used by `backend`.

<div class="wide">
![The architecture diagram]({{site.images}}{{page.slug}}/kzTuwx6.png)
</div>

To follow along, make sure you have [Node.js](https://nodejs.org/en) installed. This article uses Node.js 20.3.0.

### Create an Nx Workspace

You need to start by creating an Nx workspace with the following command:

~~~{.bash caption=">_"}
npx create-nx-workspace@latest
~~~

You'll be asked a few questions. Answer with the following:

* **Where would you like to create your workspace?:** Provide a name of the workspace: **`myorg`**. Nx will create a directory with the same name and store your projects there.
* **Which stack do you want to use?:** Pick **react** for this tutorial.
* **What framework would you like to use?:** You can select one of the React frameworks that Nx officially supports. To keep things simple, pick **none**.
* **Standalone project or integrated monorepo?:** Choose **integrated**. You can find the difference between a stand-alone project and an integrated monorepo in the [official Nx documentation](https://nx.dev/concepts/integrated-vs-package-based).
* **Application name:** Use **customer**, which will be the first app you'll create.
* **Which bundler would you like to use?:** Choose **vite**.
* **Default stylesheet format:** Choose **css**.
* **Enable distributed caching to make your CI faster:** Select **Yes**.

<div class="wide">
![Workspace creation]({{site.images}}{{page.slug}}/7ux7KbH.png)
</div>

Once the command finishes running, you'll have a directory named `myorg`. Navigate to that directory, as the rest of the tutorial will take place there.

In `apps/customer`, you'll find that you have a React project. You also have an end-to-end (E2E) test set up with Cypress in `apps/customer-e2e`.

Now it's time to create a second React app with the following command:

~~~{.bash caption=">_"}
npx nx g @nx/react:app admin
~~~

This creates another React app named `admin` in the `apps` directory as well as an E2E test in `apps/admin-e2e`.

Before you can create the Node.js backend, you need to install the Node.js plugin for Nx:

~~~{.bash caption=">_"}
npm install -D @nx/node
~~~

Run the following command to create a Node.js application in the `apps/backend` directory. Choose `express` as the framework of choice:

~~~{.bash caption=">_"}
npx nx g @nx/node:app backend
~~~

Then create a React library that will be used by the `customer` and `admin` applications:

~~~{.bash caption=">_"}
npx nx g @nx/react:lib common-components
~~~

Choose `jest` as the test runner and `vite` as the bundler. This creates a React library in `libs/common-components`.

Finally, create a JavaScript library named `functions` that will be used by the `backend` application:

~~~{.bash caption=">_"}
npx nx g @nx/js:lib functions
~~~

Choose `none` for both the test runner bundler.

At this point, you should have the following directory structure:

~~~{ caption=""}
|__ apps
|    |__ admin
|    |__ admin-e2e
|    |__ backend
|    |__ backend-e2e
|    |__ customer
|    |__ customer-e2e
|__ libs
|    |__ custom-components
|    |__ functions
~~~

You can explore the projects and their interdependencies by running the following command, which opens a new page in your browser:

~~~{.bash caption=">_"}
npx nx graph
~~~

Select **Show all projects** in the sidebar, and you'll see the following screen:

<div class="wide">
![The current graph]({{site.images}}{{page.slug}}/0jWiH4g.png)
</div>

As you can see, you have five projects and three E2E tests. The E2E tests have implicit dependencies on their corresponding projects. However, none of the projects are dependent on each other.

Create a new `Header` component in `common-components` that will be used in both `admin` and `customer` with the following command:

~~~{.bash caption=">_"}
npx nx g @nx/react:component header \
--project=common-components --export
~~~

Open `libs/common-components/src/lib/header/header.tsx` and replace the existing code with the following:

~~~{.ts caption="header.tsx"}
import styles from './header.module.css';

/* eslint-disable-next-line */
export interface HeaderProps {
  text: string;
}

export function Header(props: HeaderProps) {
  return (
    <header>{props.text}</header>
  );
}

export default Header;
~~~

You can use this component by installing it from "@myorg/common-components" (which you'll do soon). Initially, you need to install Axios, which will be used to make HTTP requests to the backend server.

Installing a library in an Nx workspace is different because you need to install the library globally instead of in the project directory.

> Have you noticed that none of your projects have `node_modules`? This is because Nx takes care of installing dependencies globally in a workspace.

Run the following command in the workspace:

~~~{.bash caption=">_"}
npm install axios cors
~~~

Open `apps/admin/src/app/app.tsx` and replace the existing code with the following:

~~~{.ts caption="app.tsx"}
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import styles from './app.module.css';

import { Header } from '@myorg/common-components';
import { useEffect, useState } from 'react';

import axios from 'axios';

export function App() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    axios.get('http://localhost:3000/admin').then((response) => {
      setMessage(response.data);
    });
  }, []);

  return (
    <div>
      <Header text="Welcome to admin!" />
      <p>{message}</p>
    </div>
  );
}

export default App;
~~~

This code makes a GET request to `http://localhost:3000/admin`, where the backend returns a message. This message is then displayed on the page using the `Header` component.

Repeat the same step with the `customer` app. Open `apps/customer/src/app/app.tsx` and add the following code:

~~~{.ts caption="app.tsx"}
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import styles from './app.module.css';

import { Header } from '@myorg/common-components';
import { useEffect, useState } from 'react';

import axios from 'axios';

export function App() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    axios.get('http://localhost:3000/customer').then((response) => {
      setMessage(response.data);
    });
  }, []);

  return (
    <div>
      <Header text="Welcome to customer!" />
      <p>{message}</p>
    </div>
  );
}

export default App;
~~~

This code is largely the same as the `admin` code, except this time, you make a request to `http://localhost:3000/customer`.

Now create a `currentDate` function in the `functions` project that will be used in the `backend`. This function simply returns the current date. For that, you use the `date-fns` library:

~~~{.bash caption=">_"}
npm install date-fns
~~~

Open `libs/functions/src/lib/functions.ts` and replace the existing code with the following:

~~~{.ts caption="functions.ts"}
import { format } from 'date-fns';

export function currentDate(): string {
  return format(new Date(), 'yyyy-MM-dd');
}
~~~

Finally, create the backend app at `apps/backend/src/main.ts`:

~~~
import express from 'express';
import { currentDate } from '@myorg/functions';
import cors from 'cors';

const host = process.env.HOST ?? 'localhost';
const port = process.env.PORT ? Number(process.env.PORT) : 3000;

const app = express();
app.use(cors({ origin: '*' }));

app.get('/customer', (req, res) => {
  res.send(`[ customer ] ${currentDate()}`);
});

app.get('/admin', (req, res) => {
  res.send(`[ admin ] ${currentDate()}`);
});

app.listen(port, host, () => {
  console.log(`[ ready ] http://${host}:${port}`);
});
~~~

This code creates a simple Express app with two routes: `/customer` and `/admin`. Both routes use the `currentDate` function imported from `@myorg/functions` and return the current date, along with an indication of `customer` or `admin`.

Run `npx nx graph` again and select **Show all projects**:

<div class="wide">
![The graph of the project]({{site.images}}{{page.slug}}/x9j04Dw.png)
</div>

This time, you can see that you have dependencies between the projects. Both `customer` and `admin` depend on `common-components`, and `backend` depends on `functions`.

To run the projects, start the `backend` project with the following command:

~~~{.bash caption=">_"}
npx nx serve backend
~~~

Then in another terminal, start the `admin` app:

~~~{.bash caption=">_"}
npx nx serve admin
~~~

Visit [http://localhost:4200](http://localhost:4200) and verify that you can see the admin page:

<div class="wide">
![The admin app]({{site.images}}{{page.slug}}/bPfAloT.png)
</div>

To run the `customer` app, stop the `admin` app and then start the `customer` app with the following:

~~~{.bash caption=">_"}
npx nx serve customer
~~~

<div class="wide">
![The customer app]({{site.images}}{{page.slug}}/DM95lio.png)
</div>

### The Affected Mechanism

Typically, almost all commits change only a small subset of your projects. This means it's a waste of time and resources to build and test every single project every time you make a new commit. To tackle this, Nx offers a mechanism called  ["affected" mechanism](https://nx.dev/concepts/affected). With this mechanism, only the projects that have been changed by a commit and the projects depending on this changed project are built and tested. See this in action:

Start by creating a commit to mark the current state:

~~~{.bash caption=">_"}
git add .
git commit -m "Initial commit"
~~~

Now, change the `common-components` project. Open `libs/common-components/src/lib/header/header.module.css` and add the following CSS code:

~~~{.css caption="module.css"}
header {
    color: red;
}
~~~

Check which projects have been affected by this change with the following command:

~~~{.bash caption=">_"}
npx nx affected:graph
~~~

Select **Show all projects**, and you'll see that the `customer`, `admin`, `common-components`, and their corresponding E2E tests are marked in red. This is because changing `common-components` also affects these projects:

<div class="wide">
![The affected projects are marked in red]({{site.images}}{{page.slug}}/lISgdEG.png)
</div>

Now you can run the tests for only the affected projects with the following command:

~~~{.bash caption=">_"}
npx nx affected -t test
~~~

The tests will fail since you haven't written tests for the modified code. Note that only the tests for the affected components were run:

<div class="wide">
![The tests were run for the affected projects only]({{site.images}}{{page.slug}}/lISgdEG.png)
</div>

All the code for this tutorial can be found in this [GitHub repo](https://github.com/heraldofsolace/nx-demo).

## Conclusion

Monorepos are becoming the norm for organizing multiple interrelated projects in a single repo. To make full use of a monorepo, you must use a build tool that is capable of efficiently handling a monorepo.

In this article, you explored a powerful tool called Nx. You learned about its pros and cons and saw how easy it is to build a monorepo with it. If your projects are predominantly in JavaScript or TypeScript, then you can't go wrong with Nx. If your projects include use of other languages, Nx can still work but you might want to take a look at [Earthly.](https://earthly.dev/)

{% include_html cta/bottom-cta.html %}
