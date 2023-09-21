---
title: "Using `npm` Workspaces for Monorepo Management"
categories:
  - Tutorials
toc: true
author: Aniket Bhattacharyea
editor: Ubaydah Abdulwasiu

internal-links:
 - just an example
---

In the ever-evolving world of software development, managing complex projects with multiple interconnected components can be a daunting task. However, monorepos provide an efficient organizational strategy by offering a unified repository that houses all related projects in one place.

With a bird's-eye view of all related projects, code sharing and collaboration across teams become seamless, fostering a cohesive development environment. Monorepos also ensure synchronized releases and reduce versioning issues across projects.

[npm 7](https://www.npmjs.com/package/npm/v/7.0.7) introduced [npm workspaces](https://docs.npmjs.com/cli/v9/using-npm/workspaces?v=true), which provide monorepo management capabilities. In this article, you'll learn all about npm workspaces and how to set up and implement one.

## What Are npm Workspaces?

[npm](https://www.npmjs.com/) is a popular package management tool for JavaScript. In 2020, npm introduced the much-awaited [workspaces feature](https://docs.npmjs.com/cli/v7/using-npm/workspaces), which gives you the ability to manage multiple packages from one single top-level package. With workspaces, you can develop and manage multiple independent packages and create dependencies between them.

For example, if you have `package-a` and `package-b` in a single top-level package with workspaces enabled, running `npm install` will symlink `package-a` and `package-b` directories inside a root-level `node_modules` directory. Then you can use `package-a` in `package-b` and vice versa without worrying about manually linking dependencies with `npm link`. This simplifies the management of a monorepo significantly.

> Note that the term *workspace* can refer to the root-level package as well as the individual packages under the root-level package.

To enable workspaces, you need to add the `workspaces` key to your root-level `package.json`. This key should list all the directories containing the workspaces:

```json
{
	...,
	"workspaces": [ "./package-a", "./package-b" ]
}
```

Once this is defined, you can use the `--workspace` flag in `npm` commands to run the commands in a particular workspace and the `--workspaces` flag to run the commands in all workspaces like this:

```bash
npm install date-fns --workspace package-a # Install date-fns into package-a
npm uninstall lodash --workspace package-b # Uninstall lodash from package-b
npm run build --workspaces # Run build in all workspaces
```

### Pros of npm Workspaces

The following are some of the advantages of using npm workspaces:

#### Simple and Easy to Use

With npm workspaces, you don't need to install third-party build tools such as [Nx](https://nx.dev/) or [Turborepo](https://turbo.build/). Instead, configuring workspaces is as simple as adding the `workspaces` key in `package.json`. The existing npm commands work the same, making it a very straightforward tool with almost no learning curve.

#### Efficient Dependency Management

Using npm workspaces, you can install all the dependencies at the root-level workspace as long as all the workspaces are using the same version. If different workspaces use different versions of the same dependency, it gets installed in individual workspaces. At the same time, the individual workspaces are symlinked to the root-level `node_modules` directory. This ensures you don't waste space by installing the same dependency multiple times. It also helps you synchronize dependency versions throughout different packages.

### Cons of npm Workspaces

Even though npm workspaces make monorepo management more accessible, it still has a few downsides:

#### Lack of Features

npm workspaces lack many features that you'd expect from a powerful build tool. For instance, it doesn't have a build introspection tool like [`nx graph`](https://nx.dev/core-features/explore-graph), and it lacks any way to define how tasks may depend on each other, like Turborepo. If you want to make sure `package-a` is built before `package-b`, there's no way to configure this with workspaces, and you have to manually build `package-a` before building `package-b` (and this has to be done every time `package-a` changes).

Additionally, there's no equivalent to Nx's affected mechanism where you can run tests and builds for only the packages affected by the most recent change. With npm workspaces, you must figure out the impact of the changes on your own or run tests and builds in all workspaces, which wastes time and resources.

#### Lack of Integration with Tools and Frameworks

Another disadvantage is that npm workspaces don't have native integration with frameworks like [React](https://react.dev/), [Vue](https://vuejs.org/), or [Vite](https://vitejs.dev/). This means you must manually create packages with these frameworks and configure them to integrate with npm workspaces. Compare this to a tool like Nx, which can create apps with different frameworks that work out of the box with one simple command.

Additionally, npm workspaces also don't have integration with IDEs, and you have to use the CLI to use it.

## Build a Monorepo with npm Workspaces

To follow along with this tutorial, you need to install the latest version of [Node.js](https://nodejs.org/en) and [npm](https://npmjs.com). The npm workspace was introduced in npm version 7, so make sure you have the latest version of npm installed by running `npm -v`:

```bash
npm -v
```

If the npm version is earlier than 7, install the latest version of npm with the following command:

```bash
npm install -g npm@latest
```

> This article was written with Node.js v20.3.0 and npm v9.6.7.

### Create the Workspace

Create a new directory named `npm-workspaces-demo` and initiate an npm package:

```bash
mkdir npm-workspace-demo && cd npm-workspace-demo
npm init -y
```

To use npm workspaces, you don't need to follow a certain directory structure; you're free to structure your workspace as you see fit. For this tutorial, create two directories: `apps` to hold the React apps and `packages` to hold the shared package:

```bash
mkdir apps packages
```

Move into the `apps` directory and create two React apps with Vite: `app1` and `app2`:

```bash
cd apps
npm create vite@latest app1 -- --template react-ts
npm create vite@latest app2 -- --template react-ts
```

Edit the `package.json` file of `app1` and change the name field to the following:

```json
{
	"name": "@npm-workspace-demo/app1",
	...
}
```

Even though it's not mandatory, scoping the packages with `@npm-workspace-demo` ensures no conflict with existing packages in the npm registry.

Do the same in the `package.json` of `app2`:

```json
{
	"name": "@npm-workspace-demo/app2",
	...
}
```

Finally, move into the `packages` directory and create another React app named `components`:

```bash
npm create vite@latest components -- --template react-ts
```

Then create a directory named `components` inside `packages/components/src` and create a file `Header.tsx` in this directory with the following code:

```tsx
import React from 'react'

export interface HeaderText {
  text: string
}
export const Header = ({ text }: HeaderText) => {
  return <div className="text">{text}</div>
}
```

This code simply defines a `Header` component that displays a text.

Next, create an `index.ts` file in the same directory and export the `Header` and `HeaderText` components:

```tsx
export { Header } from './Header'
export { type HeaderText } from './Header'
```

Your shiny new `Header` component is ready. However, before you can use it, you need to compile the TSX into JavaScript before importing it into your React apps. To tell Vite how to do that, open the `vite.config.ts` file in `packages/components` and replace the existing code with the following:

```ts
import { resolve } from 'node:path'

import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'
import dts from 'vite-plugin-dts'
import tsConfigPaths from 'vite-tsconfig-paths'
import * as packageJson from './package.json'


export default defineConfig((configEnv) => ({
  plugins: [
	react(),
	tsConfigPaths(),
	dts({
  	include: ['src/components/'],
	}),
  ],
  build: {
	lib: {
  	entry: resolve('src', 'components/index.ts'),
  	name: 'Components',
  	formats: ['es', 'umd'],
  	fileName: (format) => `components.${format}.js`,
	},
	rollupOptions: {
  	external: [...Object.keys(packageJson.peerDependencies)],
	},
  },
}))
```

The `dts` function compiles the type information from `src/components`, and the `build` function compiles the components into UMD and ES formats. The file `src/components/index.ts` is used as the entry point to tell Vite which components to compile. Finally, the `peerDependencies` field in `package.json` is passed to `rollup` to tell it which external libraries are needed for the build.

Open the `tsconfig.json` file in `packages/components` and write the following code:

```json
{
  "compilerOptions": {
	"target": "ESNext",
	"useDefineForClassFields": true,
	"lib": ["DOM", "DOM.Iterable", "ESNext"],
	"allowJs": false,
	"allowSyntheticDefaultImports": true,
	"strict": true,
	"forceConsistentCasingInFileNames": true,
	"module": "ESNext",
	"moduleResolution": "Node",
	"resolveJsonModule": true,
	"isolatedModules": true,
	"noEmit": true,
	"jsx": "react-jsx",
	"declaration": true,
	"skipLibCheck": true,
	"esModuleInterop": true ,
	"declarationMap": true,
	"allowImportingTsExtensions": true,
	"baseUrl": ".",
	"paths": {
  	"components": [ "src/components/index.ts" ]
	},
	"typeRoots": [
  	"node_modules/@types",
  	"src/components/index.d.ts"
	]
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

This enables the TypeScript compiler to know what files to compile to JavaScript.

Replace the contents of `tsconfig.node.json` in the same directory with the following to configure the compiler options for Vite:

```json
{
  "compilerOptions": {
	"composite": true,
	"module": "ESNext",
	"moduleResolution": "Node",
	"allowSyntheticDefaultImports": true,
	"resolveJsonModule": true,
  },
  "include": ["vite.config.ts","package.json"],
}
```

Finally, open `package.json` in the same directory and add the following entries to the JSON object:

```json
"files": [
	"dist"
],
"exports": {
	".": {
    	"import": "./dist/components.es.js",
    	"require": "./dist/components.umd.js"
	},
}
"main": "./dist/components.umd.js",
"module": "./dist/components.es.js",
"types": "./dist/index.d.ts",
```

This simply tells npm which files to export. After the components are compiled, the resulting JavaScript file is stored in `dist/components.<format>.js`, which is imported into the React apps.

Rename the `dependencies` key to `peerDependencies` and change the `name` field to include the scope:

```json
{
	"name": "@npm-workspace-demo/components",
	...
}
```

Finally, open the `package.json` file of the root workspace and add the following entry:

```json
{
	...,
	"workspaces": ["./packages/*", "./apps/*"]
}
```

This tells npm that everything under the `packages` and `apps` directories is an npm workspace. Note that the workspace's name is inferred from the `name` field of the corresponding `package.json` file.

Now run `npm install` in the root of the project to install the dependencies of all the workspaces.

> Note that there is no `node_modules` directory inside the individual workspaces after the installation of the dependencies.

As mentioned previously, the dependencies of all the workspaces are stored in the root-level `node_modules` directory and linked from there as long as all the workspaces use the same version of the dependencies. If different workspaces use different versions of a particular dependency, it will be installed in the individual workspaces with the appropriate versions.

For the `components` library to compile, you need to install a few dependencies. You can use the `--workspace` flag of `npm` to run npm commands scoped to a specific workspace.

Run the following command to install `vite-plugin-dts` and `vite-tsconfig-paths` into the `components` workspace:

```bash
npm install vite-plugin-dts vite-tsconfig-paths --workspace @npm-workspace-demo/components
```

Build the `components` library:

```bash
npm run build --workspace @npm-workspace-demo/components
```

And install it into `app1` and `app2`:

```bash
npm install @npm-workspace-demo/components --workspace @npm-workspace-demo/app1
npm install @npm-workspace-demo/components --workspace @npm-workspace-demo/app2
```

It's time to use the component in the React apps and make sure the setup works as expected.

Open `apps/app1/src/App.tsx` and replace the code with the following:

```tsx
import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { Header } from "@npm-workspace-demo/components"

function App() {

  return (
	<div className="App">
  	<Header text="Hello World from app1" />
	</div>
  )
}

export default App
```

Here, the `Header` component is imported from `@npm-workspace-demo/components`. Note that the syntax is the same as what you'd write for a module installed from the npm registry.

Do the same thing for `app2.` This time, change the text to `Hello World from app2`:

```tsx
import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { Header } from "@npm-workspace-demo/components"

function App() {

  return (
	<div className="App">
  	<Header text="Hello World from app2" />
	</div>
  )
}

export default App
```

### Run the Apps

At this point, you've finished interlinking the apps and the architecture looks roughly like this: 

![The architecture of the project courtesy of Aniket Bhattacharyea](https://i.imgur.com/YH3Jk8h.png)

Run `app1` and make sure that it works:

```bash
npm run dev --workspace @npm-workspace-demo/app1
```

![Screenshot of app1](https://i.imgur.com/j6sKizL.png)

And then make sure `app2` works as well:

```bash
npm run dev --workspace @npm-workspace-demo/app2
```

![Screenshot of app2](https://i.imgur.com/aTosrRc.png)

You can find the complete code for this tutorial on [GitHub](https://github.com/heraldofsolace/npm-workspaces-demo).

## Conclusion

npm is one of the most commonly used Node.js package managers, and the workspaces feature marks its entry into the field of monorepos. With workspaces, you can manage multiple Node.js packages in one single repo and run npm tasks in individual projects from the main project, making it an easy-to-use monorepo management tool.

Even though npm workspaces are an excellent option for small monorepos, it's not mature enough to use in large, complex monorepos. The lack of defining task dependencies, result caching, and affected mechanism makes it an inferior choice to other tools like Nx or Turborepo when it comes to managing a complex js monorepo with a large number of projects and/or a lot of interdependencies. And if you need to incorporate other languages or backend services, an NPM based solution will be a limitation. For monorepos builds that support NPM and many other tools, take a look at [Earthly](http://earthly.dev). It can help keep your monorepo builds fast as your code base grows.

## Outside Article Checklist

- [ ] Create header image in Canva
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
  - Would any images look better `wide` or without the `figcaption`?
- [ ] Run mark down linter (`lint`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `link-opp` and find 1-5 places to incorporate links
- [ ] Add Earthly `CTA` at bottom `{% include_html cta/bottom-cta.html %}`
