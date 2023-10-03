---
title: "npx vs. npm vs. pnpm: A Comparison for JavaScript Projects"
categories:
  - Tutorials
toc: true
author: Kumar Harsh

internal-links:
 - just an example
---

If you've worked with JavaScript-based projects, you've likely used [npm](https://www.npmjs.com/), [npx](https://docs.npmjs.com/cli/v7/commands/npx/), or [pnpm](https://pnpm.io) to manage your project's dependencies and scripts. Each of these tools offers a unique set of features that are suited to different types and scales of projects.

npm comes bundled with [Node.js](https://nodejs.org/en/) as the default package management tool, while npx is a tool for executing Node.js packages that comes bundled with npm. In contrast, pnpm is a third-party tool that you can install if you need finer control over your project's dependencies.

In this article, you'll learn all about npx, npm, and pnpm, including how they work and when to use them.

## What Is npm?

[npm](https://docs.npmjs.com/cli/) (which [is not an acronym](https://github.com/npm/cli#is-npm-an-acronym-for-node-package-manager)) is a widely used package management tool for Node.js and JavaScript projects. It was created in 2009 as an open source project to simplify the process of sharing and distributing code modules (packages) within the Node.js community. Over time, npm has become a central component of the JavaScript ecosystem, enabling the installation, management, and integration of third-party libraries, tools, and scripts.

npm comes prebundled with Node.js. To verify its installation, you can run `npm -v` in your command line interface.

Some of the prominent use cases of npm include the following:

* **Initialize projects:** You can initialize a new JavaScript-based project using `npm init` and follow the prompts to set project details. This creates a `package.json` file for you in the project directory with your chosen project details.
* **Manage dependencies and package versions:** You can install packages as dependencies in your project using the command `npm install <package-name>`. To install specific versions of the dependencies, you can use `npm install <package-name@version>`.
* **Run npm scripts:** In `package.json`, you can define custom scripts under the `scripts` field. npm allows you to run them using the command `npm run <script-name>`. For example, `"start": "node index.js"` in your `package.json` lets you run `npm run start` to start your application.
* **Publish npm packages:** If you're developing an npm package locally, you can make use of the `npm publish` command to publish it to the Node.js package registry and make it available for public use.

## What Is npx?

[npx](https://docs.npmjs.com/cli/v7/commands/npx/), a node package runner, is a command line tool introduced in npm version 5.2.0. It addresses the need to run packages and binaries from the command line without the need for global installations. npx was created to simplify the process of using tools that are not globally installed or that come bundled with packages, making it a valuable addition to the npm ecosystem.

npx comes automatically installed with npm (npm version 5.2.0 and above). To use npx, simply prefix a command with `npx`. For example, `npx create-react-app my-app` runs the `create-react-app` tool without having to install it globally.

Some of the prominent use cases of npx include the following:

* **Execute packages and binaries:** You can run packages and binaries from the command line without installing them globally. npx allows you to do that by prefixing the command with `npx` (*eg* `npx eslint file.js`).
* **Run local development tools:** With npx, you can execute locally installed development tools that aren't part of the global `PATH` of your system. Webpack is a common development tool that is not installed on the host system directly, but you can run it using npx like this: `npx webpack`.
* **Run code from GitHub:** npx enables you to run code directly from GitHub repositories using the command syntax `npx github:username/repo`.
* **Try out new packages and commands:** With npx, you can test new packages and commands without permanently installing them. You can use the popular [cowsay](https://cowsay.diamonds/) program without installing it using the following format: `npx cowsay Hello, npx!`.
* **Bypass global packages:** npx enables you to avoid conflicts and version issues by running tools directly from their package context. This means that running `npx eslint` ensures that the ESLint installation specific to your project is launched and used, even if there is a global ESLint installation that might be incompatible with your project.

The ability to avoid global package installations is helpful because it prevents your system from getting cluttered, allows you to easily install and run packages (especially for temporary use cases), and ensures that you can use the latest version of a package. However, it also introduces a network dependency into your development process, which is a factor worth considering before using npx in your development workflows.

## What Is pnpm?

[pnpm](https://pnpm.io/pnpm-cli) is a package manager for JavaScript projects that aims to improve upon the traditional package management approaches of npm and [Yarn](https://yarnpkg.com/). It was developed in response to the issues of disk space consumption and duplicate packages that can occur when using npm or Yarn.

pnpm uses a unique approach called [store linking](https://pnpm.io/faq#why-does-my-node_modules-folder-use-disk-space-if-packages-are-stored-in-a-global-store) to minimize disk usage and accelerate the installation and updates of packages.

To use pnpm, you need to install it globally using npm or Yarn:

```bash
npm i -g pnpm
```

After installation, you can use pnpm commands in your projects instead of npm commands.

Some of the prominent use cases of pnpm include the following:

* **Initializing projects:** You can initialize a new project using `pnpm init`, similar to `npm init`. This also generates a `package.json` file containing the metadata of the project as you described it when setting it up.
* **Managing dependencies and package versions:** One of the key use cases of pnpm is to enable installing packages using `pnpm add <package-name>`. When installing packages, you can specify versions like `@latest` or `@1.0.0`.
* **Running pnpm scripts:** Similar to npm, you can define and run scripts in your `package.json`. Instead of running `npm run start`, run `pnpm start`. Additionally, if pnpm finds no script with the name supplied to it, it will then execute the command directly as a shell script. This means that you can run `pnpm webpack` to run webpack in your project even if it's not defined as part of any script in your `package.json` file.

## Comparing npx, npm, and pnpm

As you've probably already concluded, npx is a utility tool for executing Node.js packages, setting up tools for one-time use, and bypassing globally installed packages. Meanwhile, npm and pnpm are full-fledged package management solutions for JavaScript-based projects.

### When to Use and Not Use npx

npx is a great solution to use for the following:

* **Running one-off commands:** npx shines when it comes to running one-off commands in repos, such as initializing a project using a remote-based initialization script (*ie* `create-react-app` or `vite-app`) or setting up local dev testing environment (*ie* running `webpack`).
* **Trying out new packages:** If you're looking to try out new packages without installing them in your local system (and potentially interfering with other projects on your system), npx can be a major help as it can help you execute packages without having to install them in your project or globally.
* **Running local dev tools:** npx can conveniently provide the environment and scope needed to run local dev tools in multiple kinds of projects.

In comparison, npx might not be a good tool to choose in the following situations:

* **Frequent (and global) commands/tools:** If you find yourself using a command/tool through npx frequently, you might be able to optimize your experience by setting up that tool locally and avoiding pulling it afresh every time with npx.
* **Continuous integration (CI) environments:** CI environments require a stable set of dependencies to run your build as intended. Relying on npx to fetch the latest version of a tool during the build adds performance overhead to your builds (due to the network dependency) and increases the chances of a broken build as the tool pulled during the build might have changes that you're unaware of. You can use versions with npx commands, but the network overhead still remains, so it's best not to use npx in CI if possible.
* **Performance-critical operations:** Similar to the CI point from before, npx relies on the network to pull in packages and scripts, so it's best not to depend on it for performance-critical tasks.

### When to Use and Not Use npm

npm is a great solution in the following situations:

* **When implementing dependency management:** Because it ships out of the box with Node.js, npm is the first dependency management tool you'll use to install everything for your project, even other dependency management tools. It's a simple and lightweight tool, which makes it an easy-to-use dependency management solution for smaller projects.
* **When working with Node.js projects:** If you're working on a Node.js project that doesn't involve too many third-party frameworks and dependencies, npm is easy to get started with. 
* **When you have to run a lot of npm scripts:** If you're working on a project that relies on a large number of npm scripts, npm may be a good solution for both dependency management and build lifecycle management in one place.

However, there are situations where npm may not be well-suited, including the following:

* **Simple frontend projects:** Frontend projects often have too many dependencies to manage compared to backend projects. In these situations, a solution like Yarn might be better as it can perform parallel installations, resulting in better speed and performance.
* **Project already using another package manager:** If your project already has a package manager, it's best to continue using that instead of mixing npm in it. You can check if your project uses a package manager by looking for `*-lock.json` files or if it's mentioned in any configuration files. Mixing two package managers can result in dependency version conflicts and your project breaking.
* **Low on disk space:** npm is notorious for hogging up disk space with its dependencies. If you're on a system that's low on storage, pnpm or Yarn's pnpm mode might be better as it can efficiently manage disk storage.
* **Large-scale monorepos:** npm is great for simple projects, but it doesn't provide any special provisions for managing large-scale monorepos. If your project houses multiple apps and each requires active dependency management, npm might be too much of a hassle for you. A solution like pnpm suits this use case better.

### When to Use and Not Use pnpm

pnpm is quite similar to npm in terms of functionalities. However, the key difference lies in how it manages the problem of disk space consumption and duplicate packages. If you're looking for a solution that uses less disk space than npm, pnpm is the way to go. In this section, you'll learn of a few more use cases in which pnpm is best suited:

* **Monorepos:** pnpm finds use in monorepos as it provides special commands and flags to help you install, link, and manage dependencies in monorepos efficiently. For a repo that has multiple apps and, thus, a large number of locally cached dependencies, pnpm does a great job at keeping disk usage low as well.
* **Secure environments:** Unlike npm, pnpm creates a flat `node_modules` by default, meaning the `node_modules` directory for projects that use pnpm contains only their direct dependencies; not all direct and transitive dependencies flattened out together in the same folder. This prevents your code from accessing arbitrary packages and, therefore, running into compatibility or security issues.

While pnpm sounds like the perfect upgrade to npm, it's important to understand that it's a powerful and complex tool, and you probably don't need it in most of your simpler Node.js projects. It finds its best use in monorepos.

## Conclusion

In this article, you learned about the three most popular project and script management tools in JavaScript: npx, npm, and pnpm.

If you're looking for something conventional and easy to get started with, npm is the way to go. But if you want to experiment with remote scripts and packages, npx is a great option. And if you're looking for something more serious with performance and resource optimizations, you'll want to check out pnpm.

Once you understand how to make the best use of these tools, you'll be able to navigate your JavaScript projects with ease.

{% include_html cta/bottom-cta.html %}

## Outside Article Checklist

- [ ] Create header image in Canva
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
  - Would any images look better `wide` or without the `figcaption`?
- [ ] Run mark down linter (`lint`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `link-opp` and find 1-5 places to incorporate links
