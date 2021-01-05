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

            * [Docker](https://docs.docker.com/install/)
            * [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

            ### Installation

            <div class="Home-product-Earthfile">
                <header class="Home-product-Earthfile-header">
                    <div class="Home-product-Earthfile-header-chromeDecoration">
                    </div>
                    Terminal
                </header>
                <code class="Home-product-Earthfile-code">
                    <p>sudo /bin/sh -c 'wget https://github.com/earthly/earthly/releases/latest/download/earthly-linux-amd64 -O /usr/local/bin/earthly && chmod +x /usr/local/bin/earthly && /usr/local/bin/earthly bootstrap'</p>
                </code>
            </div>

    tab2:
        name: mac
        title: Mac
        source: source2
        content: |
            ### Pre-requisites

            * [Docker for Mac](https://docs.docker.com/docker-for-mac/install/)
            * [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

            ### Installation

            <div class="Home-product-Earthfile">
                <header class="Home-product-Earthfile-header">
                    <div class="Home-product-Earthfile-header-chromeDecoration">
                    </div>
                    Terminal
                </header>
                <code class="Home-product-Earthfile-code">
                    <p>brew install earthly</p>
                </code>
            </div>

    tab3:
        name: windows
        title: Windows (WSL 2)
        source: source3
        content: |
            ### Pre-requisites

            * [WSL 2](https://docs.microsoft.com/en-us/windows/wsl/install-win10)
            * [Docker Desktop WSL2 backend](https://docs.docker.com/docker-for-windows/wsl/)
            * [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

            ### Installation

            <div class="Home-product-Earthfile">
                <header class="Home-product-Earthfile-header">
                    <div class="Home-product-Earthfile-header-chromeDecoration">
                    </div>
                    Terminal
                </header>
                <code class="Home-product-Earthfile-code">
                    <p>sudo /bin/sh -c 'wget https://github.com/earthly/earthly/releases/latest/download/earthly-linux-amd64 -O /usr/local/bin/earthly && chmod +x /usr/local/bin/earthly && /usr/local/bin/earthly bootstrap'</p>
                </code>
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
        name: st
        title: Sublime Text
        source: source3
        content: |
            Visit [sublimetext-earthly-syntax on GitHub](https://github.com/earthly/sublimetext-earthly-syntax) for details.
---

{% include tabs.html tabs=page.os id="os" %}

For alternative installation options see the [installation page in the Earthly docs](https://docs.earthly.dev/installation). To install Earthly from source, see the [contributing page in GitHub](https://github.com/earthly/earthly/blob/main/CONTRIBUTING.md).

### Verify installation

<p>
    <div class="Home-product-Earthfile">
        <header class="Home-product-Earthfile-header">
            <div class="Home-product-Earthfile-header-chromeDecoration">
            </div>
            Terminal
        </header>
        <code class="Home-product-Earthfile-code">
            <p>earthly github.com/earthly/hello-world:main+hello</p>
        </code>
    </div>
</p>

### Syntax highlighting

{% include tabs.html tabs=page.ide id="ide" %}

### Installing Earthly in CI

See the [CI integration guide](https://docs.earthly.dev/guides/ci-integration).

### Next steps

To learn how to use Earthly, try

* [The getting started guide](https://docs.earthly.dev/guides/basics).
* [An introductory video](https://www.youtube.com/watch?v=B7Q7S2lpshw)
* [The full documentation](https://docs.earthly.dev/)
