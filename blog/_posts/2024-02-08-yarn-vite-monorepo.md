---
title: "Building a Monorepo with Yarn and Vite"
categories:
  - js-tooling
  - monorepos
toc: true
author: Aniket Bhattacharyea

internal-links:
 - building a monorepo with yarn and vite
 - build a monorepo
 - how to build a monorepo with yarn and vite
 - yarn and vite for building a monorepo
excerpt: |
    This article explains how to build a monorepo using Yarn workspaces and Vite, allowing for easy collaboration and dependency management in JavaScript projects. It covers the setup process, creating apps with React and Vue, and enabling parallel execution of build scripts.
---
**The article provides a guide on setting up a monorepo with Yarn and Vite. If you're working in a monorepo, you might be interested in Earthly. Earthly significantly speeds up build times for complex projects. [Check it out](https://cloud.earthly.dev/login).**

In a real-world project, you'll often have many independent components that depend on each other. Organizing these components while keeping in mind the ease of development and deployment is a daunting task. Thankfully, with [monorepos](https://earthly.dev/blog/monorepo-tools/), all the related subprojects are contained within one single repository. This makes it easy for teams to collaborate and update the dependencies with new changes without the fear of breaking projects that rely on them.

In the JavaScript world, [Yarn](https://yarnpkg.com) is a well-known package manager. With the recent addition of the [workspaces](https://yarnpkg.com/features/workspaces) feature, Yarn can now be used as a monorepo build tool. With workspaces enabled, Yarn can identify workspaces in a project, efficiently install and manage dependencies, handle dependencies between subprojects, and enable parallel builds.

When it comes to frontend development, [Vite](https://vitejs.dev/) is a next-generation tool that's designed to streamline development using JavaScript and TypeScript. Vite simplifies the creation of development environments for popular frontend frameworks like Vue, React, and Svelte, offering fast server start and hot module replacement (HMR) out of the box.

In this article, you'll learn how to use Vite and Yarn workspaces to build a monorepo.

## What Is Vite?

Traditionally, ECMAScript modules (ESM) were not supported by any browsers. This means developers needed to use bundlers such as [webpack](https://webpack.js.org/), [Rollup](https://rollupjs.org/), or [Parcel](https://parceljs.org/) to bundle all the source modules into JavaScript files that the browsers could run. However, this approach has a few performance drawbacks. For instance, when starting the dev server for the first time, the bundler must crawl through all the source code to create the bundle. If you have a large project with a bunch of source modules, this process can be very lengthy. Additionally, when one of the modules changes, the bundle must be reconstructed to reflect the changes, which is another time-consuming process.

Vite aims to improve upon these factors. It intelligently utilizes the native ESM capabilities of modern browsers to provide a fast server start as well as HMR, which lets you instantly reload a changed module without affecting the rest of the modules.

Vite has out-of-the-box support for TypeScript, JSX, and CSS, as well as support for frameworks like Vue, React, and Svelte. Thanks to its plugin architecture, you can easily customize its functionalities.

## Creating a Monorepo with Yarn and Vite

In this article, you'll learn how to build a monorepo with Yarn workspaces and Vite. The monorepo here will represent an internal portal for a company. In this scenario, there's a portal that teams use, a separate portal for the managers, and another portal for admins. For simplicity, these portals only display a message, but you're welcome to expand upon the concepts shown in this tutorial and build something more complex.

To demonstrate the flexibility of Vite, you'll use both React and Vue, and the monorepo will have four subprojects:

1. A `teams` app made in React
2. A `managers` app made in React
3. A Vue app named `admins`
4. A React library named `common-ui` (both the `teams` and `managers` apps will have this library as a dependency)

<div class="wide">
![Architectural diagram courtesy of Aniket Bhattacharyea]({{site.images}}{{page.slug}}/qEZyGXY.png)
</div>

To follow along, make sure you have [Node.js 18+](https://nodejs.org/en) installed.

### Creating the Monorepo Structure

The first thing you need to do is enable Yarn by running `corepack enable`. Then, create a directory and initialize a Yarn project in it:

~~~{.bash caption=">_"}
mkdir yarn-vite-monorepo && cd yarn-vite-monorepo
yarn init -2
~~~

Next, you need to create the directory structure of the monorepo. The applications will go under the `apps` directory, and the library will go under the `packages` directory. Use the following command to create the `apps` and `packages` directories:

~~~{.bash caption=">_"}
mkdir apps packages
~~~

Then, add the `workspaces` field to the `package.json` file at the root of the project:

~~~{.js caption="package.json"}
{
    ...
    "workspaces": [
        "packages/*",
        "apps/*"
    ]
}
~~~

This field tells Yarn that all the directories under `apps` and `packages` should be considered workspaces.

### Creating the Apps

To create the apps, navigate into the `apps` directory:

~~~{.bash caption=">_"}
cd apps
~~~

Then, create two React apps (the teams and managers portals):

~~~{.bash caption=">_"}
yarn create vite teams --template react
yarn create vite managers --template react
~~~

Next, create the Vue app (the admins portal):

~~~{.bash caption=">_"}
yarn create vite admins --template vue
~~~

Once you've created all three portals, navigate to the `packages` directory:

~~~{.bash caption=">_"}
cd ../packages
~~~

And create a package named `common-ui`:

~~~{.bash caption=">_"}
yarn create vite common-ui --template react
~~~

Then, navigate to the root of the project and run `yarn`. This will install the dependencies for each of the workspaces. Note that there's no need to individually install dependencies for the workspaces. When you run `yarn` in a project with workspaces enabled, Yarn automatically installs dependencies for each workspace.

### Creating the Shared Library

To create the shared library, you'll be working in the `packages/common-ui` directory.

Delete all the files in the `src` directory, then create a new file named `banner.jsx` with the following code:

~~~{.jsx caption="banner.jsx"}
export default function Banner({ instanceName }) {
    return <h1>Welcome to the {instanceName} portal</h1>;
}
~~~

This is a simple React component that displays a message on the screen. This component will be used in both the `managers` and `teams` apps.

You need to export this React component so that it can be imported into the apps. Create a new folder named `lib` and add a file named `main.js` to this directory. Paste the following code into it:

~~~{.js caption="main.js"}
export { default as Banner } from '../src/banner'
~~~

This file simply exports the `Banner` component and acts as an entry point for the library.

Next, you need to let Vite know how to build this project as a shared library. Open the `vite.config.js` file and replace the existing code with the following:

~~~{.js caption="vite.config.js"}
import react from "@vitejs/plugin-react";
import { resolve } from "path";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react()],
  build: {
    lib: {
      entry: resolve(__dirname, "lib/main.js"),
      name: "common-ui",
      fileName: "common-ui",
    },
    rollupOptions: {
      external: ["react", "react-dom"],
      output: {
        globals: {
          react: "React",
          "react-dom": "React-dom",
        },
      },
    },
  },
});
~~~

The important part of this code is that the `build` entry tells Vite to build the library using `lib/main.js` as the entry point. The compiled file will be stored at `dist/common-ui.js` and `dist/common-ui.umd.cjs`.

Now, open the `package.json` file and add the following entries:

~~~{.js caption="package.json"}
{
    ...
    "files": [
        "dist"
    ],
    "main": "./dist/common-ui.umd.cjs",
    "module": "./dist/common-ui.js",
    "exports": {
        ".": {
        "import": "./dist/common-ui.js",
        "require": "./dist/common-ui.umd.cjs"
        }
    },
}
~~~

These entries export the compiled JavaScript files and are responsible for finding the component when you import it into the apps later.

Navigate to the root of the project and build the `common-ui` library:

~~~{.bash caption=">_"}
yarn workspace common-ui build
~~~

This command executes the `build` script in the `common-ui` workspace. The `build` script runs `vite build` and compiles the component using the previous configuration. You should get an output that looks like this:

~~~{.bash caption=">_"}
vite v5.0.11 building for production...
✓ 10 modules transformed.
dist/common-ui.js  21.20 kB │ gzip: 6.32 kB
dist/common-ui.umd.cjs  13.94 kB │ gzip: 5.44 kB
✓ built in 172ms
~~~

### Completing the React Apps

To finish setting up the React apps, you need to install the `common-ui` library as a dependency in the `teams` and `managers` apps. Since the `common-ui` library is part of the same monorepo, you'll use a [special syntax](https://yarnpkg.com/features/workspaces#cross-references) for referencing it.

Open the `package.json` file in both `apps/teams` and `apps/managers`, and add the following entry in the `dependencies` object:

~~~{.js caption="package.json"}
"common-ui": "workspace:^",
~~~

From the root of the project, run `yarn` to install the dependency.

You're now ready to use the exported component in your React apps. Open `teams/src/App.jsx` and replace the existing code with the following:

~~~{.jsx caption="App.jsx"}
import { Banner } from 'common-ui'

function App() {

  return (
    <>
      <Banner instanceName="Teams" />
    </>
  )
}

export default App
~~~

Note that you're importing `Banner` from `common-ui` just like a usual library. Yarn takes care of linking the dependency behind the scenes.

Open `managers/src/App.jsx` and replace the existing code with the following:

~~~{.jsx caption="App.jsx"}
import { Banner } from "common-ui"

function App() {

  return (
    <>
      <Banner instanceName="Managers" />
    </>
  )
}

export default App
~~~

You can now run the apps and see if they work. From the root of the project, start the `teams` app:

~~~{.bash caption=">_"}
yarn workspace teams dev
~~~

If you visit `http://localhost:5173` in your browser, you should see the following:

<div class="wide">
![The Teams portal]({{site.images}}{{page.slug}}/BdWvKfO.png)
</div>

Stop the server and run the `managers` app:

~~~{.bash caption=">_"}
yarn workspace managers dev
~~~

Visit `http://localhost:5173` again, and you should see the `managers` app:

<div class="wide">
![The Managers portal]({{site.images}}{{page.slug}}/rHGXP5J.png)
</div>

### Completing the Vue App

After completing the React apps, you need to finish the Vue app. Open `apps/admins/src/components/HelloWorld.vue` and replace the code with the following:

~~~{.vue caption="HelloWorld.vue"}
<script setup>

defineProps({
  instanceName: String,
})

</script>

<template>
  <h1>Welcome to the {{ instanceName }} portal</h1>

</template>
~~~

This code creates a component analogous to the `Banner` component.

Open `apps/admins/src/App.vue` and replace all the code with the following:

~~~{.vue caption="App.vue"}
<script setup>
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <HelloWorld instanceName="Admins" />
</template>
~~~

From the root of the project, start the `admins` app:

~~~{.bash caption=">_"}
yarn workspace admins dev
~~~

Visit `http://localhost:5173`. This time, you'll see the Vue app:

<div class="wide">
![The Admins portal]({{site.images}}{{page.slug}}/TKCrxbj.png)
</div>

**Note:** You don't necessarily need to run the `dev` scripts from the root of the project. You can also run a script from within a workspace that defines it using the `yarn run` command, just like a usual Yarn project. For example, you can run `yarn run dev` from within the `apps/admins` directory instead of running `yarn workspace admins dev` from the project's root.

### Enabling Parallel Execution

So far, you've run the apps individually. Similarly, if you want to build the apps, you can run the build scripts individually. But there's a better way! If you want to run the same Yarn script for all the workspaces, you can use the [`yarn workspaces foreach`](https://yarnpkg.com/cli/workspaces/foreach) command. This command runs the same script in each workspace.

For example, using the following code, you can run the `build` script for all the workspaces:

~~~{.bash caption=">_"}
yarn workspaces foreach --all -pt run build
~~~

You should see an output like this:

~~~{ caption="Output"}
[admins]: Process started
[common-ui]: Process started
[common-ui]: vite v5.0.11 building for production...
[common-ui]: transforming...
[common-ui]: ✓ 10 modules transformed.
[common-ui]: rendering chunks...
[common-ui]: computing gzip size...
[common-ui]: dist/common-ui.js  21.20 kB │ gzip: 6.32 kB
[common-ui]: dist/common-ui.umd.cjs  13.94 kB │ gzip: 5.44 kB
[common-ui]: ✓ built in 183ms
[common-ui]: Process exited (exit code 0), completed in 0s 496ms
[admins]: vite v5.0.11 building for production...
[admins]: transforming...
[admins]: ✓ 11 modules transformed.
[admins]: rendering chunks...
[admins]: computing gzip size...
[admins]: dist/index.html                  0.46 kB │ gzip:  0.29 kB
[admins]: dist/assets/index-m0DGwFy9.css   1.00 kB │ gzip:  0.54 kB
[admins]: dist/assets/index-pF6ixyOY.js   52.56 kB │ gzip: 21.23 kB
[admins]: ✓ built in 451ms
[admins]: Process exited (exit code 0), completed in 0s 835ms
[managers]: Process started
[teams]: Process started
[teams]: vite v5.0.11 building for production...
[teams]: transforming...
[teams]: ✓ 32 modules transformed.
[teams]: rendering chunks...
[teams]: computing gzip size...
[teams]: dist/index.html                   0.46 kB │ gzip:  0.30 kB
[teams]: dist/assets/index-T74ItOsL.css    0.92 kB │ gzip:  0.50 kB
[teams]: dist/assets/index-6R6vXPwk.js   143.74 kB │ gzip: 46.30 kB
[teams]: ✓ built in 565ms
[teams]: Process exited (exit code 0), completed in 0s 849ms
[managers]: vite v5.0.11 building for production...
[managers]: transforming...
[managers]: ✓ 32 modules transformed.
[managers]: rendering chunks...
[managers]: computing gzip size...
[managers]: dist/index.html                   0.46 kB │ gzip:  0.30 kB
[managers]: dist/assets/index-T74ItOsL.css    0.92 kB │ gzip:  0.50 kB
[managers]: dist/assets/index-l9QTZ6f4.js   143.74 kB │ gzip: 46.30 kB
[managers]: ✓ built in 596ms
[managers]: Process exited (exit code 0), completed in 0s 896ms
Done in 1s 735ms
~~~

The flags passed to this command are important. The `--all` flag runs the script in all workspaces. You can also use `--since` to only run the script in workspaces that have changed in the current branch compared to the `main` branch.

Using `--from` instead of `--all` lets you supply a glob pattern so that the script is run only in the workspaces that match the pattern. For example, the following command only runs the `build` script in workspaces that are in the `packages` directory:

~~~{.bash caption=">_"}
yarn workspaces foreach --from packages/* -Rpt run build
~~~

The `-p` flag enables parallel execution, and the `-t` flag tells Yarn to respect the topological order. In other words, with the `-t` flag, Yarn runs the `build` script in a workspace only after all its dependencies have been built. When used together with the `-p` flag, you can ensure that the build process is run in parallel whenever possible while ensuring the dependencies are built first.

If you look at the output of the first `yarn workspaces foreach` command, you'll notice that `admins` and `common-ui` start their build simultaneously:

~~~{ caption="Output"}
[admins]: Process started
[common-ui]: Process started
~~~

This is because `managers` and `teams` depend on `common-ui`, which means they can't be built until `common-ui` is built. However, since `admins` doesn't depend on any other workspace, it can be built in parallel with `common-ui`.

Once `common-ui` finishes building, the `managers` and `teams` apps can be built. Since they don't depend on each other, they're also built in parallel:

~~~{ caption="Output"}
[managers]: Process started
[teams]: Process started
~~~

In comparison, here the `-p` flag is omitted:

~~~{.bash caption=">_"}
$ yarn workspaces foreach --all -t run build
[admins]: Process started
[admins]: vite v5.0.11 building for production...
[admins]: transforming...
[admins]: ✓ 11 modules transformed.
[admins]: rendering chunks...
[admins]: computing gzip size...
[admins]: dist/index.html                  0.46 kB │ gzip:  0.29 kB
[admins]: dist/assets/index-m0DGwFy9.css   1.00 kB │ gzip:  0.54 kB
[admins]: dist/assets/index-pF6ixyOY.js   52.56 kB │ gzip: 21.23 kB
[admins]: ✓ built in 460ms
[admins]: Process exited (exit code 0), completed in 0s 808ms

[common-ui]: Process started
[common-ui]: vite v5.0.11 building for production...
[common-ui]: transforming...
[common-ui]: ✓ 10 modules transformed.
[common-ui]: rendering chunks...
[common-ui]: computing gzip size...
[common-ui]: dist/common-ui.js  21.20 kB │ gzip: 6.32 kB
[common-ui]: dist/common-ui.umd.cjs  13.94 kB │ gzip: 5.44 kB
[common-ui]: ✓ built in 172ms
[common-ui]: Process exited (exit code 0), completed in 0s 439ms

[managers]: Process started
[managers]: vite v5.0.11 building for production...
[managers]: transforming...
[managers]: ✓ 32 modules transformed.
[managers]: rendering chunks...
[managers]: computing gzip size...
[managers]: dist/index.html                   0.46 kB │ gzip:  0.30 kB
[managers]: dist/assets/index-T74ItOsL.css    0.92 kB │ gzip:  0.50 kB
[managers]: dist/assets/index-l9QTZ6f4.js   143.74 kB │ gzip: 46.30 kB
[managers]: ✓ built in 552ms
[managers]: Process exited (exit code 0), completed in 0s 832ms

[teams]: Process started
[teams]: vite v5.0.11 building for production...
[teams]: transforming...
[teams]: ✓ 32 modules transformed.
[teams]: rendering chunks...
[teams]: computing gzip size...
[teams]: dist/index.html                   0.46 kB │ gzip:  0.30 kB
[teams]: dist/assets/index-T74ItOsL.css    0.92 kB │ gzip:  0.50 kB
[teams]: dist/assets/index-6R6vXPwk.js   143.74 kB │ gzip: 46.30 kB
[teams]: ✓ built in 578ms
[teams]: Process exited (exit code 0), completed in 0s 837ms
Done in 2s 922ms
~~~

As you can see, the workspaces are built one after another.

### Creating Global Scripts

So far, you've learned about three different ways to run a script defined in one of the workspaces:

1. Using `yarn run <script-name>` from the workspace where the script is defined
2. Using the `yarn workspace <workspace-name> run <script-name>` command from the root of the project
3. Using `yarn workspaces foreach` from the root of the project, provided all the workspaces define a script with the same name

However, it's also possible to "promote" a script to a global script so that it can be run from anywhere in the project, using the typical `yarn run <script-name>` syntax. To create a global script, you must create a script that contains a colon (`:`) in its name.

Open the `package.json` file in the `packages/common-ui` directory and add the following script:

~~~{.bash caption=">_"}
"common-ui:build": "vite build"
~~~

This script defines the same `build` task but is now registered as a global script. You can run it from anywhere in the project:

~~~{.bash caption=">_"}
yarn run common-ui:build
~~~

**Note:** You don't necessarily need to use the workspace name as the prefix of the global script, but it's a good practice so that you don't accidentally end up defining two global scripts with the same name in two different workspaces. If that happens, none of them will be promoted to global scripts.

You can find the complete project on [GitHub](https://github.com/heraldofsolace/yarn-vite-monorepo-demo).

## Conclusion

In this article, you learned how to build a monorepo with [Yarn workspaces](https://yarnpkg.com/features/workspaces) and Vite and explored how this setup enables you to have projects with different frameworks in the same repo.

[Vite](https://vitejs.dev/) is a powerful and efficient frontend build tool that makes developing JavaScript and TypeScript apps fast and easy. With Vite, you get access to a super fast development server with HMR and the freedom to use any framework of your choice.

When you outgrow yarn workspaces and vite, or need to incorporate backend languages like Go, Rust, Python or even Ruby and Java, take a look at Earthly. It's a great build tool for monorepos and will help speed your development and build time. [Check it out](https://cloud.earthly.dev/login)

{% include_html cta/bottom-cta.html %}
