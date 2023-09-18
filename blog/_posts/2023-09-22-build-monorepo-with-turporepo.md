---
title: "Using Turborepo to Build Your First Monorepo"
categories:
  - Tutorials
toc: true
author: Aniket Bhattacharyea
editor: Muhammad Badawy

internal-links:
 - using turborepo
 - turborepo to build your first monorepo
 - building your first monorepo
 - turborepo
 - first monorepo with turborepo
---

In recent years, monorepos have seen a boom in popularity. Many real-life software projects consist of smaller, individual components that often depend on each other.

For instance, you might have an app with its own [Vue](https://vuejs.org/) frontend and [Node.js](https://nodejs.org/en/) backend, or two different [React](https://react.dev/) applications sharing a common collection of components. Traditionally, each individual component gets its own repo, but as the number and complexity of components grow, managing them individually becomes a challenge. Monorepos solve this issue by putting all related components in the same repository.

A monorepo allows you to have all related projects in one place, providing visibility over all of them. If you commit new changes to one project, you can easily visualize how this affects the other projects. Additionally, with monorepos, it's easier to share code, collaborate on projects, and synchronize releases of different projects.

However, monorepos require specialized [build tools](https://earthly.dev/blog/monorepo-tools/) that are capable of handling multiple interdependent projects. One such tool is [Turborepo](https://turbo.build/repo). In this article, you'll learn all about Turborepo and how to create and manage a monorepo with it.

## What Is a Monorepo?

With traditional polyrepo architecture, each individual component of a project is stored in separate repos. While this makes it easier to develop, test, and deploy individual components, it may become convoluted as the number of components and the dependencies between them grow.

For instance, if you have twenty different components across twenty different repositories and twenty different teams working on them, it's likely that each team will introduce its own tooling and styles, creating a management nightmare. Since the projects are isolated, it's also possible to introduce breaking changes since the developers don't have visibility over how their changes affect other projects.

By consolidating all the projects in a single monorepo, you can have a bird's eye view of all the projects in one place as well as centralized tooling, style guides, and tests. You can also easily manage the impact of changes and improve synchronization between projects.

## What Is Turborepo?

Turborepo is a fast, high-performance build system for JavaScript and TypeScript projects. It's a tool- and framework-agnostic build system that can integrate with package managers, such as [npm](https://www.npmjs.com/), [Yarn](https://yarnpkg.com/), and [pnpm](https://pnpm.io/), and provides a build system that can improve build times by [40 to 85 percent](https://turbo.build/repo/docs/core-concepts/caching#hitting-the-cache).

Even though it's aimed mainly at monorepos, it can be added to any JavaScript or TypeScript project to improve the build process.

### Pros of Turborepo

Even though Turborepo is relatively young compared to other mature tools, such as [Nx](https://nx.dev), Turborepo has quite a few advantages that make it a superb choice for monorepos:

#### Fast Builds

The selling point of Turborepo is its speed. Turborepo uses a combination of caching, multitasking, and pruning to speed up builds by as much as 85 percent.

Turborepo utilizes [caching](https://turbo.build/repo/docs/core-concepts/caching) to remember previously built items, avoiding unnecessary rebuilding if nothing has changed. It uses content-based hashing, which means it looks at the file contents to figure out what has changed rather than just the timestamp.

Turborepo can [schedule tasks parallelly](https://turbo.build/repo/docs/core-concepts/monorepos/running-tasks#turborepo-can-multitask), which optimizes the build by making full use of the CPU cores. Lastly, with [pruning](https://turbo.build/repo/docs/reference/command-line-reference/prune), Turborepo can generate a sparse/pruned subset of the monorepo with only what's needed to build a specific target.

#### Remote Caching

Turborepo uses [Vercel](https://vercel.com) for remote caching. After linking your monorepo with a Vercel project, Turborepo can push artifacts and logs to the remote cache, which you or other team members can access by linking their local copies with the same Vercel project. This means if someone on your team builds the project, everyone can share the build results and won't have to build again. This cements Turborepo's motto of "Never do the same work twice."

#### Flexible Task Configuration

With Turborepo, you can define tasks such as `build`, `test`, and `lint` in a file named `turbo.json`. You can define each task's dependencies and how to cache the results. Turborepo can then figure out optimal scheduling of the tasks that make full use of the multitasking capabilities of Turborepo.

By defining dependencies, you can always be sure your tasks run in the order they need to.

#### Integration With Existing Package Managers

Turborepo extends the capabilities of the workspaces feature available in existing package managers such as npm, Yarn, or pnpm; meaning Turborepo is tool-agnostic and doesn't get in the way of your existing tools.

#### Build Introspection Tools

When using the `turbo run` commands, you have the option to include the `--graph` field, which allows you to generate a visualization of the dependencies between tasks with [Graphviz](https://graphviz.org/). This feature provides a visual overview of the execution order of tasks, helping you understand the task relationships more intuitively. Additionally, you can generate a PNG, JPEG, or PDF file of the graph for easy sharing or reference.

### Cons of Turborepo

While Turborepo brings immense value by boosting the build speed of a monorepo, it also has a few downsides that can end up being dealbreakers for some developers. Take a look at some of these disadvantages:

#### Lack of Integration with Frameworks and Tools

Unlike Nx, Turborepo doesn't integrate intuitively with frameworks such as Next.js or Vue. That means if you want to add a new project to your workspace, you need to manually configure it with the framework of your choice. In comparison, with Nx, you can create apps or libraries with different frameworks with just a single command.

Additionally, Turborepo doesn't integrate with tools such as [Firebase](https://firebase.google.com/), which can make things more time-consuming to set up. Moreover, it only supports JavaScript and TypeScript projects, so if your monorepo has components in other languages, such as Go or Rust, you won't be able to use Turborepo.

#### Developer Experience

Because Turborepo is very young, it doesn't provide a cohesive developer experience. Apart from the lack of built-in support for frameworks, Turborepo also doesn't offer any plugins or extensions for IDEs or editors. Additionally, the CLI tool is immature, with only a few commands and limited customization options.

Overall, Turborepo is an excellent tool for JavaScript or TypeScript monorepos with interdependent tasks, as it offers significant performance improvements through multitasking and caching. However, for more complex projects that involve multiple languages or dependencies, it may not be the best choice.

## Build a Monorepo With Turborepo

Now that you know more about Turborepo's pros and cons, it's time to learn how to configure a monorepo with Turborepo. In this hypothetical scenario, you'll have a blogging service with a monorepo containing the following projects:

1. A React app named `admin`.
2. A Vue app named `blog`.
3. An [Express](https://expressjs.com/) app named `backend`.
4. A TypeScript library named `types`.

The `backend` project runs a server from which both `admin` and `blog` fetch data. The `types` library exports common TypeScript types that all three apps use:

<div class="wide">
![Architecture diagram of the monorepo courtesy of Aniket Bhattacharyea]({{site.images}}{{page.slug}}/lA9Y1xn.png)
</div>

To follow along, you need to install the latest Node.js. You also need to install pnpm. While you can use npm or Yarn, the Turborepo team recommends using pnpm. This article was written using Node.js v20.3.0 and pnpm 8.6.2.

The entire code for this tutorial is available on this [GitHub repo](https://github.com/heraldofsolace/turborepo-demo).

### Create the Monorepo

To begin, you need to create a directory to hold the monorepo and initialize pnpm in it:

~~~{.bash caption=">_"}
mkdir turborepo-demo && cd turborepo-demo
pnpm init
~~~

Because Turborepo doesn't have a fixed directory structure, you can choose whatever structure you prefer.

In this tutorial, you'll create the applications (frontends and backends) under the `apps` directory and libraries and packages under the `packages` directory. Use the following command to create the directory structure:

~~~{.bash caption=">_"}
mkdir apps
mkdir packages
~~~

Now, navigate to the `apps` directory. This is where you create the React frontend, the Vue frontend, and the Express backend. Start by creating the Vue frontend by running the following command:

~~~{.bash caption=">_"}
pnpm create vue@latest
~~~

You are then asked a few questions. Please respond to each question as follows:

* **Project name:** `blog`
* **Add TypeScript?:** Yes
* **Add JSX Support?** Yes
* **Add Vue Router . . . ?:** No
* **Add Pinia . . . ?:** No
* **Add Vitest . . . ?:** No
* **Add an End-to-End Testing Solution?:** No
* **Add ESLint . . . ?:** Yes
* **Add Prettier . . . ?:** Yes

<div class="wide">
![Creating a Vue app]({{site.images}}{{page.slug}}/X7quTia.png)
</div>

This creates a Vue app in the `blog` directory.

Next, create the React app with the following command:

~~~{.bash caption=">_"}
pnpm create vite@latest
~~~

Use `admin` as the project name and choose `React` as the framework. Select `TypeScript` as the variant:

<div class="wide">
![Creating the React app]({{site.images}}{{page.slug}}/cglxvrE.png)
</div>

Now, your React app is ready in the `admin` directory.

Next, you need to create a directory named `backend` and initialize a `pnpm` project:

~~~{.bash caption=">_"}
mkdir backend
cd backend
pnpm init
~~~

The `backend` folder holds the Express app that you'll create later.

Navigate back to the root of your monorepo and create a `types` directory inside the `packages` directory. Use the following command to create the directory structure as well as initialize `pnpm`:

~~~{.bash caption=">_"}
mkdir packages/types
cd packages/types
pnpm init
cd ../..
~~~

The next step is to set up `pnpm` workspaces. Create a file named `pnpm-workspace.yaml` at the root of the monorepo with the following content:

~~~{.yaml caption="pnpm-workspace.yaml"}
packages:
  - "packages/*"
  - "apps/*"
~~~

This configuration tells `pnpm` that all the directories under `packages` and `apps` are `pnpm` workspaces.

Run `pnpm install` to install the dependencies in all the workspaces.

Then install Turborepo globally in the repo:

~~~{.bash caption=">_"}
pnpm install turbo --global
~~~

> **Note:** If you want to commit the repo to Git, make sure to add the `.turbo` directory to your `.gitignore` file so that it's excluded from being committed.

### Create the `types` Package

Once you've installed Turborepo in the repo, it's time to install TypeScript in the `types` package:

~~~{.bash caption=">_"}
pnpm add --save-dev typescript --filter types
~~~

Create a `src` directory inside `packages/types` and create an `index.ts` file in the `src` directory. Then write the following code in the `index.ts`:

~~~{.ts caption="index.ts"}
export type Blog = {
    id: string;
    title: string;
    content: string;
}
~~~

This code defines a `Blog` type with ID, title, and content fields. This type is exported so that other packages in the monorepo can use this type.

Create a `tsconfig.json` file in the `types` directory with the following code:

~~~{.js caption="tsconfig.json"}
  {
      "compilerOptions": {
        "baseUrl": ".",
        "target": "es2017",
        "lib": ["dom", "dom.iterable", "esnext"],
        "allowJs": true,
        "skipLibCheck": true,
        "strict": true,
        "forceConsistentCasingInFileNames": true,
        "noEmit": true,
        "esModuleInterop": true,
        "module": "esnext",
        "moduleResolution": "node",
        "resolveJsonModule": true,
        "isolatedModules": true,
        "jsx": "preserve"
      },
      "include": ["./src"]
    }

~~~

This file tells the TypeScript compiler to compile TypeScript files in the `src` directory.

Finally, you need to tell the Node.js engine how to import this file. For that, edit `packages/types/package.json`. Change the `main` key to `./src/index.ts` and add a `type` key with the value `./src/index.ts`. Finally, modify the `scripts` key as follows:

~~~{.ts caption="index.ts"}
"scripts": {
    "type-scheck": "tsc"
}
~~~

The `package.json` file should look something like this:

~~~{.js caption="package.json"}
  {
    "name": "types",
    "version": "1.0.0",
    "description": "",
    "main": "./src/index.ts",
    "types": "./src/index.ts",
    "scripts": {
      "type-check": "tsc"
    },
    "keywords": [],
    "author": "",
    "license": "ISC",
    "devDependencies": {
      "typescript": "^5.1.6"
    }
  }
~~~

> **Note:** Your dependency's versions may be different.

### Create the `backend` App

Now it's time to create the backend. Run the following command in the workspace root to install the dependencies in the `backend` package:

~~~{.bash caption=">_"}
pnpm add express cors --filter backend
pnpm add --save-dev typescript esbuild \
tsx @types/{express,cors} --filter backend
~~~

Next, install the `types` package that you previously created. To install packages from the same workspace, you can use the `package-name@workspace` syntax:

~~~{.bash caption=">_"}
pnpm add --save-dev types@workspace --filter backend
~~~

Create a `src` directory inside `apps/backend` and create a file `index.ts` inside it with the following code:

~~~{.ts caption="index.ts"}
import express from 'express';
import cors from 'cors';

import { Blog } from 'types';

const app = express();
const port = process.env.PORT || 8000;

app.use(cors({ origin: '*' }));

app.get('/blogs', (req, res) => {
  const blogs: Blog[] = [
    { id: '1', title: 'Blog 1', content: 'Content 1' },
    { id: '2', title: 'Blog 2', content: 'Content 2' },
    { id: '3', title: 'Blog 3', content: 'Content 3' },
    { id: '4', title: 'Blog 4', content: 'Content 4' },
  ];
  res.json({ blogs });
});

app.listen(port, () => console.log(`Listening on http://localhost:${port}`));
~~~

This code creates an Express server at port 8000 and returns a dummy list of blogs when the endpoint `/blogs` is visited.

> Note that you're importing `Blog` from the `types` package as if it were a standard Node.js package. pnpm takes care of the linking for you.

Finally, modify `apps/backend/package.json` and modify the `scripts` key as shown here:

~~~{.js caption="package.json"}
"scripts": {
      "test": "echo \"Error: no test specified\" && exit 1",
      "dev": "tsx watch src/index.ts",
      "build": "esbuild src/index.ts --bundle --platform=node \
      --outfile=dist/index.js --external:express --external:cors",
      "start": "node dist/index.js"
    },

~~~

Here, you're defining how to build the backend and how to run a development server for it. These scripts will later be used by Turborepo as part of its pipeline.

### Create the Frontends

Now it's time to code the frontends to send requests to the backend. Start by installing the `types` package to both `admin` and `blog` by using the following command:

~~~{.bash caption=">_"}
pnpm add --save-dev types@workspace --filter admin
pnpm add --save-dev types@workspace --filter blog
~~~

Then install [Axios](https://axios-http.com) in both packages:

~~~{.bash caption=">_"}
pnpm add axios --filter admin
pnpm add axios --filter blog
~~~

Open `apps/admin/src/App.tsx` and replace the code with the following:

~~~{.tsx caption="App.tsx"}
import { useEffect, useState } from 'react'
import { Blog } from 'types'
import './App.css'
import axios from 'axios'

function App() {
  const [ blogs, setBlogs ] = useState<Blog[]>([])

  useEffect(() => {
    axios.get('http://localhost:8000/blogs').then((res) => {
      // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
      setBlogs(res.data.blogs as Blog[])
    }).catch((err) => {
      console.log(err)
    })
  }, [])

  return (
    <>
    {blogs.map((blog: Blog) => (
      <div key={blog.id}>
        <h1>{blog.title}</h1>
        <p>{blog.content}</p>
      </div>
    ))}
    </>
  )
}

export default App
~~~

This code fetches the list of blogs from the backend and displays them on the HTML page.

Now you'll create a blog page in the Vue app. Open `apps/blog/src/App.vue` and replace the existing code with the following:

~~~{.vue caption="App.vue"}
<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios'
import { type Blog } from 'types'

const blogs = ref<Blog[]>([])

axios.get('http://localhost:8000/blogs').then(res => {
  blogs.value = res.data.blogs
})
</script>

<template>
  <main>
    <div v-for="blog in blogs" :key="blog.id">
      <h2>{{ blog.title }}</h2>
      <p>{{ blog.content }}</p>
    </div>
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
}
</style>
~~~

This code is similar to the React version and does the exact same thing—fetches the list of blogs from the backend and lists them in the HTML page.

### Set Up Turborepo

To set up Turborepo, create a `turbo.json` file in the root of the workspace:

~~~{.js caption="turbo.json"}
{
    "$schema": "https://turbo.build/schema.json",
}
~~~

For `turbo` to run tasks, you need to define the tasks. Although you're free to define your own tasks, a typical project usually needs `build`, `test`, `lint`, `dev`, and `deploy` tasks.

#### `build` Task

The `build` task is responsible for building the whole monorepo. In order to build the monorepo, you need to start by building the `admin`, `blog`, and `backend` projects. The `build` tasks of `admin`, `blog`, and `backend`, in turn, depend on `types` being built. So Turborepo first builds the `types` package and then builds the other three simultaneously since they're independent.

Edit `turbo.json` to add the `build` pipeline as follows:

~~~{.js caption="turbo.json"}
{
    "$schema": "https://turbo.build/schema.json",
    "pipeline": {
        "build": {
            "dependsOn": ["^build"],
            "outputs": ["dist/**"]
        },
    }
}
~~~

The `dependsOn` key tells Turborepo which tasks should be finished before this task can run. The caret symbol (*ie* `^`) denotes that a workspace's `build` task depends on the `build`task of its `dependencies` and `devDependencies` being completed first. The `outputs` key tells Turborepo which directories to cache.

#### `test` Task

The `test` pipeline is responsible for running tests in the workspace.

Add the following in `turbo.json` to define the `test` pipeline:

~~~{.js caption="turbo.json"}
{
    ...
    "pipeline": {
        ...,
        "test": {
          "dependsOn": ["build"],
          "inputs": ["src/**/*.tsx", "src/**/*.ts", "test/**/*.ts", \
          "test/**/*.tsx"]
        },
    }
}
~~~

The `test` task depends on the `build` task being finished. Note that the caret is absent this time, which means the `build` task of the whole workspace is being referred to. This means whenever `test` is executed, `build` is also executed in the workspace, which, in turn, executes the `build` task in each dependency.

The `inputs` key tells TurboRepo that the tests should be rerun whenever the specified files are modified. The `test` task is loaded from the cache if none of the specified files are modified.

#### `lint` Task

The `lint` task should run linters on the packages. This task has no dependencies and should be able to run whenever needed. So you need to use an empty object:

~~~{.js caption="turbo.json"}
{
    ...
    "pipeline": {
        ...,
        "lint": {},
    }
}
~~~

#### `dev` Task

The `dev` task starts development builds in each package. Since this should never be cached, you must set `cache: false`. Additionally, since the development servers are persistent, meaning they never exit on their own, you need to set `persistent: true`. This makes sure no other task can depend on the `dev` task:

~~~{.js caption="turbo.json"}
{
    ...
    "pipeline": {
        ...,
        "dev": {
          "cache": false,
          "persistent": true
        }
    }
}
~~~

#### `deploy` Task

The `deploy` task should be used to deploy the final code(s) to the servers or package registries. This task requires `build`, `test`, and `lint` to be finished:

~~~{.js caption="turbo.json"}
{
    ...
    "pipeline": {
        ...,
        "deploy": {
          "dependsOn": ["build", "test", "lint"]
        },
    }
}
~~~

### Build With Turborepo

Once the tasks are defined, you can run them with the `turbo run` command. Check the apps out with the `dev` command:

~~~{.bash caption=">_"}
turbo run dev
~~~

Open [http://localhost:5173](http://localhost:5173) to see the React app in action. It should list the blogs as seen here:

<div class="wide">
![The React app in action]({{site.images}}{{page.slug}}/M6fsMgv.png)
</div>

Then open [http://localhost:5174](http://localhost:5174) to see the Vue app:

<div class="wide">
![The Vue app in action]({{site.images}}{{page.slug}}/JyLcQKI.png)
</div>

Stop the `dev` task by pressing **Ctrl + C** and run the `build` task:

~~~{.bash caption=">_"}
turbo run build
~~~

Turborepo runs the `build` tasks in all the packages and caches the results. You can see that it took around two seconds (the exact time may vary):

<div class="wide">
![The result of the `build` task]({{site.images}}{{page.slug}}/XyJv714.png)
</div>

Rerun the same command (*i.e.* `turbo run build`). This time, it's instant since the results are loaded from the cache. `turbo` also replays the last log since the logs are also cached:

<div class="wide">
![The `build` task is cached]({{site.images}}{{page.slug}}/oPyFhf3.png)
</div>

You can generate a graph of the tasks and save it to a PNG by running the following:

~~~{.bash caption=">_"}
turbo run build --graph=tasks.png
~~~

<div class="wide">
![The `build` graph]({{site.images}}{{page.slug}}/fB1xGP3.png)
</div>

## Conclusion

Turborepo is a young contender in the world of build tools. Its speed and optimization powers make it a fantastic choice for building JavaScript and TypeScript monorepos.

In this article, you learned the pros and cons of Turborepo and saw how to use Turborepo in a monorepo for building and running tasks. If you have JavaScript or TypeScript projects that you want to speed up, give Turborepo a try! If your projects include the use of other languages, Turborepo won't be a fit, but you might want to take a look at [Earthly](https://earthly.dev/). Earthly can speed up your builds and work with other tools including Turborepo and NX.

{% include_html cta/bottom-cta.html %}

## Outside Article Checklist

* [ ] Create header image in Canva
* [ ] Optional: Find ways to break up content with quotes or images