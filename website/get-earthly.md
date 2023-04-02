---
title: Get started with Earthly
layout: page
os:
  tab1:
    name: linux
    title: Linux
    source: source1
    active: 1
    content: |

      <div class="Home-product-Earthfile relative">
          <header class="Home-product-Earthfile-header">
              <div class="Home-product-Earthfile-header-chromeDecoration">
              </div>
              Terminal
          </header>
          <code class="Home-product-Earthfile-code">sudo /bin/sh -c 'wget https://github.com/earthly/earthly/releases/latest/download/earthly-linux-amd64 -O /usr/local/bin/earthly && chmod +x /usr/local/bin/earthly && /usr/local/bin/earthly bootstrap --with-autocomplete'</code>


                  <div class="copy-item absolute pr-4 top-1 right-0 text-white z-10 cursor-pointer" data-clipboard-text="sudo /bin/sh -c 'wget https://github.com/earthly/earthly/releases/latest/download/earthly-linux-amd64 -O /usr/local/bin/earthly && chmod +x /usr/local/bin/earthly && /usr/local/bin/earthly bootstrap --with-autocomplete'">Copy</div>

      </div>

        <div class="mt-4" markdown="1">
       Pre-requisites
      * [Docker](https://docs.docker.com/install/) or [Podman](https://github.com/containers/podman/blob/main/docs/tutorials/podman_tutorial.md)
      * [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

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

      <div class="Home-product-Earthfile relative"> 
          <header class="Home-product-Earthfile-header">
              <div class="Home-product-Earthfile-header-chromeDecoration">
              </div>
              Terminal
          </header>
          <code class="Home-product-Earthfile-code">brew install earthly && earthly bootstrap</code>

          <div class="copy-item absolute pr-4 top-1 right-0 text-white z-10 cursor-pointer" data-clipboard-text="brew install earthly && earthly bootstrap">Copy</div>
      </div>


        <div class="mt-4 " markdown="1">
       Pre-requisites
      * [Homebrew for Mac](https://brew.sh/)
      * [Docker for Mac](https://docs.docker.com/docker-for-mac/install/) or [Podman](https://github.com/containers/podman/blob/main/docs/tutorials/podman_tutorial.md)
      * [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

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
    title: Windows
    subtitle: ( WSL 2 )
    source: source3
    content: |

      <div class="text-base text-gray-700 mb-1 -mt-1">
      Under <span class="font-semibold">wsl</span>, run the following to install earthly.
      </div>

      <div class="Home-product-Earthfile relative">
          <header class="Home-product-Earthfile-header bg-[#4B5563]">
              <div class="Home-product-Earthfile-header-chromeDecoration">
              </div>
              Terminal
          </header>
          <code class="Home-product-Earthfile-code">sudo /bin/sh -c 'wget https://github.com/earthly/earthly/releases/latest/download/earthly-linux-amd64 -O /usr/local/bin/earthly && chmod +x /usr/local/bin/earthly && /usr/local/bin/earthly bootstrap  --with-autocomplete'</code>

              <div class="copy-item absolute pr-4 top-1 right-0 text-white z-10 cursor-pointer" data-clipboard-text="sudo /bin/sh -c 'wget https://github.com/earthly/earthly/releases/latest/download/earthly-linux-amd64 -O /usr/local/bin/earthly && chmod +x /usr/local/bin/earthly && /usr/local/bin/earthly bootstrap  --with-autocomplete'">Copy</div>
      </div>


        <div class="mt-4 " markdown="1">
       Pre-requisites
      * [WSL 2](https://docs.microsoft.com/en-us/windows/wsl/install-win10)
      * [Docker Desktop with WSL2 backend](https://docs.docker.com/docker-for-windows/wsl/) or [Podman with WSL2 backend](https://github.com/containers/podman/blob/main/docs/tutorials/podman-for-windows.md)
      * [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
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


      <div class="font-mono">
      ext install earthly.earthfile-syntax-highlighting
      </div>

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

      <div class="mt-4 " markdown="1">
      1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac) to bring up the Command Palette, and select **Install Package control** (if you haven't already installed Package Control).
      2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac) again, select "Package Control: Install Package" and select **Earthly Earthfile** to install.
      </div>

  tab5:
    name: intellij
    title: IntelliJ
    source: source5
    content: |
      Earthly plugin available in the [IntelliJ Marketplace](https://plugins.jetbrains.com/plugin/20392-earthly).
---

<link rel="stylesheet" href="/assets/css/subpage.css">

<div class="get-started">

{% include tabs.html title="Install Earthly CLI" selectDescription="Select your OS:" tabs=page.os id="os" %}

<div class="text-base max-w-[800px] mt-2 text-gray-600 pl-2 font-normal">
For alternative installation options see the <a class="underline blue-link" href="https://docs.earthly.dev/docs/misc/alt-installation">alternative installation page in the Earthly docs</a>. To install Earthly from source, see the <a class="underline blue-link" href="https://github.com/earthly/earthly/blob/main/CONTRIBUTING.md">contributing page in GitHub</a>
</div>

<div class="border rounded-xl bg-gray-100 px-6 py-4 mt-6 mb-6">
    <div class="text-3xl pb-4">
        Verify installation
    </div>

<div>
    <div class="Home-product-Earthfile relative">
        <header class="Home-product-Earthfile-header">
            <div class="Home-product-Earthfile-header-chromeDecoration">
            </div>
            Terminal
        </header>
        <code class="Home-product-Earthfile-code">earthly github.com/earthly/hello-world+hello</code>

  <div class="copy-item absolute pr-4 top-1 right-0 text-white z-10 cursor-pointer" data-clipboard-text="earthly github.com/earthly/hello-world+hello">Copy</div>
    </div>
 
</div>

<div class="mt-4">
This command executes the target <span class="font-semibold">hello</span> from the repository <a class="underline  blue-link" href="https://github.com/earthly/hello-world">github.com/earthly/hello-world</a>.</div>

</div>

{% include tabs.html title="Add Syntax highlighting" selectDescription="Select your IDE:" tabs=page.ide id="ide" %}

<div class="border rounded-xl bg-gray-100 px-6 py-4 mt-6 mb-6" markdown="1">

  <div class="text-3xl">
    Next Steps
  </div>

  <div class="text-gray-500 mt-2 text-lg">Try Earthly CI, use Earthly with your existing CI, or learn more about Earthly through docs, and examples.</div>

  <div class="text-2xl mt-4 border-t pt-4 border-gray-300">
    Earthly CI
  </div>

  <div class="mt-2">
See the <a href="https://docs.earthly.dev/earthly-cloud/earthly-ci" class="underline blue-link  font-semibold">Earthly CI docs</a>
</div>

<a href="/signup/earthly-ci" class="try-button py-4 h-10 px-4 xl:px-6 items-center text-sm xl:text-base text-center text-white bg-[#2d7e5d] hover:bg-green-800 rounded-lg inline-flex">
                    Try Earthly CI
                </a>

  <div class="text-2xl mt-6 border-t pt-4 border-gray-300">
    Run Earthly in a traditional CI
  </div>
<div class="mt-2">
See the <a href="https://docs.earthly.dev/guides/ci-integration" class="underline  font-semibold blue-link">CI integration guide</a> to use Earthly in GitHub Actions, Circle CI, Jenkins, GitLab CI, and others.
</div>

 <div class="text-2xl mt-6 border-t pt-4 border-gray-300">Learn Earthly</div>

<div class="mt-2 mb-2">
To learn how to use Earthly, try:
</div>

- [The getting started guide](https://docs.earthly.dev/guides/basics).
- [An introductory video](https://www.youtube.com/watch?v=B7Q7S2lpshw)
- [The full documentation](https://docs.earthly.dev/)

 <div class="text-2xl mt-6 border-t pt-4 border-gray-300">Example projects</div>
 <div class="mt-2">
Need some inspiration to get started with your project? <div class="mt-2 pb-4">Check out <a class="blue-link underline font-semibold " href="https://github.com/earthly/earthly/tree/main/examples">examples on GitHub</a></div>
</div>

</div>

</div>
