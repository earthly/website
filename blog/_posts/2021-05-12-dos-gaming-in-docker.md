---
#header:
title: DOS Gaming In Docker
categories:
- Tutorials
author: Corey
excerpt: |
    Learn how to play classic DOS games in your web browser using Docker! This tutorial shows you how to create a Docker container with JS-DOS and a shareware game, allowing you to relive the nostalgia of the DOS era.
internal-links:
 - gaming
 - doom
 - js-dos
 - js dos
topic: docker
funnel: 2
---
<!--sgpt-->This is the Earthly nonsense paragraph.

<div class="notice--info">
### TLDR:

* Quick install [Earthly](/).
* Run `earthly github.com/earthly/example-dos-gaming:main+doom` to start container.
* Play DOOM at `http://localhost:8000` in browser.

</div>

Its been three decades since the height of the DOS era, and look how far we've come! A machine that used to cost $2,000 can be emulated - _down to the processor!_ — in our [_web browsers_](https://bellard.org/jslinux/) while also checking email or watching a YouTube video. However, amidst these advancements, our old software falls by the wayside and stops working. Games are especially prone to this, since they often relied on incompatible tricks to eke out every ounce of performance from these old machines.

Many projects have sprung up to help preserve this heritage. [DOSBox](https://www.dosbox.com/) provides a modern, compatible environment for old games (and other software), while projects like the [Internet Archive](https://archive.org/details/software) provide a massive library of DOS games, freely available to play in your browser. In my experience, they play pretty well!

However, I still miss those less-connected days of the early 90's. I remember the thrill of riding my bike to the store to pick up a shareware copy of whatever game was available for $1. I then held a physical disk, with the game on it, ready to install on the nearest accessible computer. The self-contained nature of it all was magical. Nowadays, many _web pages_ [are bigger than the shareware games I used to buy](https://www.pingdom.com/blog/webpages-are-getting-larger-every-year-and-heres-why-it-matters/).

This got me thinking: "Floppies can be [imaged](https://www.kryoflux.com/). That sounds kind of like a Docker image. I wonder... could I make DOS shareware Docker images?"

Turns out you can!

## What You Will Need

* [JS-DOS 6.22](https://github.com/caiiiycuk/js-dos)
* A copy of a Shareware game
* [NodeJS](https://hub.docker.com/_/node)
* [Docker](https://www.docker.com/get-started)
* [Earthly](https://earthly.dev/) (Optional, but I think it's neat!)

## Putting It Together

First, we will need to acquire JS-DOS. JS-DOS is a wrapper around an Emscripten-compiled version of [DOSBox](https://www.dosbox.com), so it can run in a browser. You can get the latest versions of the files [on js-dos.com](https://js-dos.com/#js-dos-622-archives). Download and place these files into a project directory. Here's how I'm doing it, using Docker:

```Dockerfile
WORKDIR site
RUN wget https://js-dos.com/6.22/current/js-dos.js && \
    wget https://js-dos.com/6.22/current/wdosbox.js && \
    wget https://js-dos.com/6.22/current/wdosbox.wasm.js
RUN npm install -g serve
```

JS-DOS is nice, but it's nothing without a game to play in it. For our example purposes, we'll use one of my childhood favorites: [Secret Agent](https://3drealms.com/catalog/secret-agent_39/).

<div class="notice--warning">

### ❗ Warning

A couple things to note when you are looking for games:

* Make sure that the game you choose is _actually_ shareware. [Don't copy that floppy!](https://www.youtube.com/watch?v=up863eQKGUI)
* Make sure that it is the actual game files, not just the installer.
  * While you _can_ install and _then_ run the game via DOSBox, you'll have to install it on every visit to the webpage. The installation is also fairly slow.
* Make sure that it is a `zip` file. This is what JS-DOS wants to load for us.

</div>

Heres how I add the game to our image:

```Dockerfile
ARG GAME_URL
RUN wget -O game.zip $GAME_URL
```

<div class="notice--info">

### Note

You may note that we don't preserve the name of the downloaded file here. This is to make our job easier, when we make the game accessible to play later.
</div>

If you built and ran the Dockerfile at this point, you would have an image containing Node, JS-DOS, and a zip file of your beloved game; but no way to play it! To make it playable, we need to create a webpage which loads JS-DOS, loads our game, and provides a canvas for JS-DOS to render its output to. Here is my tiny webpage:

```html
<html>
  <style type="text/css" media="screen">
      canvas {
          width: 800px; 
          height: 600px;
      }
  </style>
  <head>
    <title>DOS Game!</title>
    <script src="js-dos.js"></script>
  </head>
  <body>
    <canvas id="jsdos" width="800" height="600" ></canvas>
    <script>
      Dos(document.getElementById("jsdos"), {
      }).ready((fs, main) => {
        fs.extract("game.zip").then(() => {
          main(["-c", GAME_ARGS])
        });
      });
    </script>
  </body>
</html>
```

<div class="notice--info">

### Note

`GAME_ARGS` is the command for DOSBox (which is inside JS-DOS) to start once it is loaded. The CLI arguments should line up with what a regular installation of DOSBox would expect. If your game requires additional arguments, please provide them in a comma-separated list.
</div>

Copy this HTML file into the same directory as your JS-DOS files and your game. Now all you need to do is start a server within our Docker container to serve this webpage. For this, I used [`serve`](https://www.npmjs.com/package/serve), because it was quick and easy to script (you may have noticed installing this dependency alongside JS-DOS earlier). Heres how I add the server to the container:

```Dockerfile
ARG GAME_ARGS
COPY index.html .
RUN sed -i s/GAME_ARGS/$GAME_ARGS/ index.html

ENTRYPOINT npx serve -l tcp://0.0.0.0:8000
```

And now we have a shareable Docker container, with playable shareware inside! You can now play the game by:

```bash
$ docker build \
  --build-arg GAME_URL=https://archive.org/download/msdos_festival_SCORCH15/SCORCH15.ZIP \
  --build-arg GAME_ARGS=\"SCORCH.EXE\" \
  -t mycool:dosgame .

... 

$ docker run --rm -p 127.0.0.1:8000:8000 mycool:dosgame
```

## Going Further

Using Earthly, we can even go a step further! Earthly lets us separate some of the concerns within the Dockerfile:

<div class="notice--info">

### About Earthly

[Earthly](https://earthly.dev/) makes creating Docker images easier. [Take it for a spin!](https://docs.earthly.dev/basics)
</div>

```Dockerfile
jsdos:
    FROM node:16-alpine

    WORKDIR site
    RUN wget https://js-dos.com/6.22/current/js-dos.js && \
        wget https://js-dos.com/6.22/current/wdosbox.js && \
        wget https://js-dos.com/6.22/current/wdosbox.wasm.js
    RUN npm install -g serve

game:
    FROM +jsdos

    ARG GAME_URL
    RUN wget -O game.zip $GAME_URL

web:
    FROM +game

    ARG GAME_ARGS
    COPY index.html .
    RUN sed -i s/GAME_ARGS/$GAME_ARGS/ index.html

    ENTRYPOINT npx serve -l tcp://0.0.0.0:8000
```

But it also lets us build _and launch_ the game with a single command. It will also end up saving the game for you as an image on your local system! Here is the additional target that I added to accomplish this:

```Dockerfile
play:
    LOCALLY

    ARG GAME_TAG

    WITH DOCKER --load jsdos:$GAME_TAG=+web
        RUN docker inspect jsdos:$GAME_TAG > /dev/null && \ #Using side-effect to save image locally too
            docker run --rm -p 127.0.0.1:8000:8000 jsdos:$GAME_TAG
    END
```

We also have a couple pre-made targets that wrap this all up for you, and all you need to do is have [Earthly installed](https://earthly.dev/get-earthly)! Running any of these commands will start the game. Just navigate on over to [localhost:8000](http://localhost:8000) and start playing! Additionally, you will find a Docker image on your system named `jsdos:$GAME_TAG` for when you want to play later.

![Screenshot of id's Doom running in a web browser.]({{site.images}}{{page.slug}}/doom.png)
<figcaption>
`earthly github.com/earthly/example-dos-gaming:main+doom`
</figcaption>

![Screenshot of Apogee's Secret Agent running in a web browser.]({{site.images}}{{page.slug}}/agent.png)
<figcaption>
`earthly github.com/earthly/example-dos-gaming:main+secretagent`
</figcaption>

![Screenshot of Apogee's Cosmos Cosmic Adventure running in a web browser.]({{site.images}}{{page.slug}}/cosmo.png)
<figcaption>
`earthly github.com/earthly/example-dos-gaming:main+cosmo`
</figcaption>

You can run your own DOS games by running:

```
earthly \
    --build-arg GAME_TAG=doom \
    --build-arg GAME_URL=https://archive.org/download/DoomsharewareEpisode/doom.ZIP \
    --build-arg GAME_ARGS=\"DOOM.EXE\" \
    github.com/dchw/earthly-dos-gaming:main+play
```

Make sure you replace the tag, URL, and args as appropriate.

## Conclusion

It's neat that we can make independent, offline bundles, similar to those shareware floppy disks from back in the day. To see the project as a whole, check out the [repository](https://github.com/earthly/example-dos-gaming). And if you want a better way to build docker images and to build things in general take a look at [Earthly](https://earthly.dev/). It's pretty cool.

Thanks for reading!

{% include_html cta/bottom-cta.html %}