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
                <code class="Home-product-Earthfile-code on-download-listen">sudo /bin/sh -c 'wget https://github.com/earthly/earthly/releases/latest/download/earthly-linux-amd64 -O /usr/local/bin/earthly && chmod +x /usr/local/bin/earthly && /usr/local/bin/earthly bootstrap --with-autocomplete'</code>
            </div>

            <div class="Home-product-note" markdown="1">
            `sudo` is used for:
              * placing the `earthly` binary in `/usr/local/bin/` and marking it as executable
              * installing auto-completion for your shell
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
                <code class="Home-product-Earthfile-code on-download-listen">brew install earthly && sudo earthly bootstrap</code>
            </div>

    tab3:
        name: windows
        title: Windows (WSL 2)
        source: source3
        content: |
            ### Pre-requisites

            * [WSL 2](https://docs.microsoft.com/en-us/windows/wsl/install-win10)
            * [Docker Desktop with WSL2 backend](https://docs.docker.com/docker-for-windows/wsl/)
            * [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

            ### Installation

            Under `wsl`, run the following to install `earthly`.

            <div class="Home-product-Earthfile">
                <header class="Home-product-Earthfile-header">
                    <div class="Home-product-Earthfile-header-chromeDecoration">
                    </div>
                    Terminal
                </header>
                <code class="Home-product-Earthfile-code on-download-listen">sudo /bin/sh -c 'wget https://github.com/earthly/earthly/releases/latest/download/earthly-linux-amd64 -O /usr/local/bin/earthly && chmod +x /usr/local/bin/earthly && /usr/local/bin/earthly bootstrap  --with-autocomplete'</code>
            </div>

            <div class="Home-product-note" markdown="1">
            `sudo` is used for:
              * placing the `earthly` binary in `/usr/local/bin/` and marking it as executable
              * installing auto-completion for your shell
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
            Add the [Earthly Earthfile package](https://packagecontrol.io/packages/Earthly%20Earthfile) via Package Control:

            1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac) to bring up the Command Palette, and select **Install Package control** (if you haven't already installed Package Control).
            2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac) again, select "Package Control: Install Package" and select **Earthly Earthfile** to install.
---

{% include tabs.html tabs=page.os id="os" bodyclass="fullborder" %}

<p>
<div class="on-download-show-wrap">
<div class="on-download-show">
<div class="on-download-show-content">
<p class="on-download-show-content-quote">
<div markdown="1">

#### 📢 Get involved 📢

Thank you for giving Earthly a shot. Come and be part of the Earthly movement!

<!-- Twitter button code -->
<script>window.twttr = (function(d, s, id) {
  var js, fjs = d.getElementsByTagName(s)[0],
    t = window.twttr || {};
  if (d.getElementById(id)) return t;
  js = d.createElement(s);
  js.id = id;
  js.src = "https://platform.twitter.com/widgets.js";
  fjs.parentNode.insertBefore(js, fjs);

  t._e = [];
  t.ready = function(f) {
    t._e.push(f);
  };

  return t;
}(document, "script", "twitter-wjs"));</script>

<!-- Social buttons -->
<p class="get-involved-social">
<a class="github-button" href="https://github.com/earthly/earthly" data-size="large" data-show-count="true" aria-label="Star earthly/earthly on GitHub">Star</a>
<a class="twitter-share-button" href="https://twitter.com/intent/tweet?text=I%27m%20trying%20out%20%F0%9F%8C%8D%20%40EarthlyTech%2C%20a%20fully%20containerized%20build%20tool%0A%0AIt%27s%20like%20Makefile%20and%20Dockerfile%20had%20a%20baby%20%F0%9F%8D%BC%0A%0AWish%20me%20luck!%0A%0A&url=https%3A%2F%2Fearthly.dev" target="_blank" data-size="large">Tweet</a>
<!-- <a class="twitter-follow-button" href="https://twitter.com/EarthlyTech" target="_blank" data-show-count="false" data-size="large">Follow @EarthlyTech</a> -->
</p>
</div>
</p>
</div>
</div>
</div>
</p>

For alternative installation options see the [alternative installation page in the Earthly docs](https://docs.earthly.dev/docs/misc/alt-installation). To install Earthly from source, see the [contributing page in GitHub](https://github.com/earthly/earthly/blob/main/CONTRIBUTING.md).

## Verify installation

<p>
    <div class="Home-product-Earthfile">
        <header class="Home-product-Earthfile-header">
            <div class="Home-product-Earthfile-header-chromeDecoration">
            </div>
            Terminal
        </header>
        <code class="Home-product-Earthfile-code">earthly github.com/earthly/hello-world:main+hello</code>
    </div>
</p>

This command executes the target `hello` from the repository [`github.com/earthly/hello-world`](https://github.com/earthly/hello-world) on the branch `main`.

## Syntax highlighting

{% include tabs.html tabs=page.ide id="ide" bodyclass="fullborder" %}

## Installing Earthly in CI

See the [CI integration guide](https://docs.earthly.dev/guides/ci-integration).

## Next steps

To learn how to use Earthly, try

* [The getting started guide](https://docs.earthly.dev/guides/basics).
* [An introductory video](https://www.youtube.com/watch?v=B7Q7S2lpshw)
* [The full documentation](https://docs.earthly.dev/)

Need some inspiration to get started with your project? Check out [examples on GitHub](https://github.com/earthly/earthly/tree/main/examples).
