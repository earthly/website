---
title: Get Earthly
layout: page
tabs: 
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
---

{% include tabs.html tabs=page.tabs id="os" %}

### Verify installation

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
