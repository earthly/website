---
title: Get Earthly
layout: page
os:
  tab1:
    name: linux
    title: Linux
    source: source1
    active: 1
    content: |
      ### Pre-requisites

      * [Docker](https://docs.docker.com/install/) or [Podman](https://github.com/containers/podman/blob/main/docs/tutorials/podman_tutorial.md)
      * [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

      ### Installation

      <div class="Home-product-Earthfile">
          <header class="Home-product-Earthfile-header">
              <div class="Home-product-Earthfile-header-chromeDecoration">
              </div>
              Terminal
          </header>
          <code class="Home-product-Earthfile-code">sudo /bin/sh -c 'wget https://github.com/earthly/earthly/releases/latest/download/earthly-linux-amd64 -O /usr/local/bin/earthly && chmod +x /usr/local/bin/earthly && /usr/local/bin/earthly bootstrap --with-autocomplete'</code>
      </div>

      <div class="Home-product-note" markdown="1">
      `sudo` is used for:
        * placing the `earthly` binary in `/usr/local/bin/` and marking it as executable
        * installing auto-completion for your shell

      For Podman:
        * Rootless Podman is [not officially supported](https://docs.earthly.dev/docs/guides/podman#rootless-podman). Run podman with `sudo`
      </div>

  tab2:
    name: mac
    title: Mac
    source: source2
    content: |
      ### Pre-requisites
      * [Homebrew for Mac](https://brew.sh/)
      * [Docker for Mac](https://docs.docker.com/docker-for-mac/install/) or [Podman](https://github.com/containers/podman/blob/main/docs/tutorials/podman_tutorial.md)
      * [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

      ### Installation

      <div class="Home-product-Earthfile">
          <header class="Home-product-Earthfile-header">
              <div class="Home-product-Earthfile-header-chromeDecoration">
              </div>
              Terminal
          </header>
          <code class="Home-product-Earthfile-code">brew install earthly/earthly/earthly && earthly bootstrap</code>
      </div>

      <div class="Home-product-note" markdown="1">
      For shell auto-completion:
        * Homebrew may require [additional configuration](https://docs.brew.sh/Shell-Completion) in your profile
      
      For Podman:
        * Ensure [Podman Machine](https://docs.podman.io/en/latest/markdown/podman-machine.1.html) is running before running bootstrap
        * Rootless Podman is [not officially supported](https://docs.earthly.dev/docs/guides/podman#rootless-podman). Learn how to [switch to rootful mode](https://docs.podman.io/en/latest/markdown/podman-machine-set.1.html#rootful)
      </div>

  tab3:
    name: windows
    title: Windows (WSL 2)
    source: source3
    content: |
      ### Pre-requisites

      * [WSL 2](https://docs.microsoft.com/en-us/windows/wsl/install-win10)
      * [Docker Desktop with WSL2 backend](https://docs.docker.com/docker-for-windows/wsl/) or [Podman with WSL2 backend](https://github.com/containers/podman/blob/main/docs/tutorials/podman-for-windows.md)
      * [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

      ### Installation

      Under `wsl`, run the following to install `earthly`.

      <div class="Home-product-Earthfile">
          <header class="Home-product-Earthfile-header">
              <div class="Home-product-Earthfile-header-chromeDecoration">
              </div>
              Terminal
          </header>
          <code class="Home-product-Earthfile-code">sudo /bin/sh -c 'wget https://github.com/earthly/earthly/releases/latest/download/earthly-linux-amd64 -O /usr/local/bin/earthly && chmod +x /usr/local/bin/earthly && /usr/local/bin/earthly bootstrap  --with-autocomplete'</code>
      </div>

      <div class="Home-product-note" markdown="1">
      `sudo` is used for:
        * placing the `earthly` binary in `/usr/local/bin/` and marking it as executable
        * installing auto-completion for your shell

       For Podman:
        * Rootless Podman is [not officially supported](https://docs.earthly.dev/docs/guides/podman#rootless-podman). Run podman with `sudo`
      </div>

ide:
  tab1:
    name: vscode
    title: VS Code
    source: source1
    active: 1
    content: |
      Add [Earthfile Syntax Highlighting](https://marketplace.visualstudio.com/items?itemName=earthly.earthfile-syntax-highlighting) to VS Code.

      ```
      ext install earthly.earthfile-syntax-highlighting
      ```

  tab2:
    name: vim
    title: Vim
    source: source2
    content: |
      Visit [earthly.vim on GitHub](https://github.com/earthly/earthly.vim) for details.

  tab3:
    name: emacs
    title: Emacs
    source: source3
    content: |
      If you are using `use-package`:

      ```elisp
      (use-package earthfile-mode
        :ensure t)
      ```

      Alternatively, install via `package-install`:

      ```
      M-x package-install RET earthfile-mode RET
      ```

  tab4:
    name: st
    title: Sublime Text
    source: source4
    content: |
      Add the [Earthly Earthfile package](https://packagecontrol.io/packages/Earthly%20Earthfile) via Package Control:

      1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac) to bring up the Command Palette, and select **Install Package control** (if you haven't already installed Package Control).
      2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac) again, select "Package Control: Install Package" and select **Earthly Earthfile** to install.

  tab5:
    name: intellij
    title: IntelliJ
    source: source5
    content: |
      Earthly plugin available in the [IntelliJ Marketplace](https://plugins.jetbrains.com/plugin/20392-earthly).

---

<link rel="stylesheet" href="/assets/css/subpage.css">

{% include tabs.html tabs=page.os id="os" bodyclass="fullborder" %}

For alternative installation options see the [alternative installation page in the Earthly docs](https://docs.earthly.dev/docs/misc/alt-installation). To install Earthly from source, see the [contributing page in GitHub](https://github.com/earthly/earthly/blob/main/CONTRIBUTING.md).

<h2 class="
      mt-14
      mb-8
      text-3xl
      font-extrabold
      leading-none
      tracking-tight
      text-gray-900
      lg:text-3xl
      xl:text-4xl
      lg:mt-20
    ">Verify installation</h2>

<p class="-mt-4">
    <div class="Home-product-Earthfile">
        <header class="Home-product-Earthfile-header">
            <div class="Home-product-Earthfile-header-chromeDecoration">
            </div>
            Terminal
        </header>
        <code class="Home-product-Earthfile-code">earthly github.com/earthly/hello-world+hello</code>
    </div>
</p>

This command executes the target `hello` from the repository [`github.com/earthly/hello-world`](https://github.com/earthly/hello-world).

<h2 class="
      mt-14
      mb-5
      text-3xl
      font-extrabold
      leading-none
      tracking-tight
      text-gray-900
      lg:text-3xl
      xl:text-4xl
      lg:mt-20
    ">Syntax highlighting</h2>

{% include tabs.html tabs=page.ide id="ide" bodyclass="fullborder" %}

<h2 class="
      mt-14
      text-3xl
      font-extrabold
      leading-none
      tracking-tight
      text-gray-900
      lg:text-3xl
      xl:text-4xl
      lg:mt-20
    ">Installing Earthly in CI</h2>

See the [CI integration guide](https://docs.earthly.dev/guides/ci-integration).

<h2 class="
      mt-14
      text-3xl
      font-extrabold
      leading-none
      tracking-tight
      text-gray-900
      lg:text-3xl
      xl:text-4xl
      lg:mt-20
    ">Next steps</h2>

To learn how to use Earthly, try

- [The getting started guide](https://docs.earthly.dev/guides/basics).
- [An introductory video](https://www.youtube.com/watch?v=B7Q7S2lpshw)
- [The full documentation](https://docs.earthly.dev/)

Need some inspiration to get started with your project? Check out [examples on GitHub](https://github.com/earthly/earthly/tree/main/examples).
