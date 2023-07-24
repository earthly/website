# Earthly Website & Blog

## How To Build in Earthly and Run in Docker

### Run Blog in Docker

Build docker image for blog:

```
> earthly ./blog+run
```

Then browse to http://0.0.0.0:4002/blog/

### Run Website in Docker

You can run the website locally, and use it to preview changes as you go.

```
> earthly ./website+run
```

Then browse to http://0.0.0.0:4001/
 
## Alternative Run

By default the Earth files use a prebuilt image. To skip this and build the image yourself use `--CACHE_IMAGE="NO"`

```
> earthly ./blog+run --CACHE_IMAGE="NO"
```

Or

```
> earthly ./website+run --CACHE_IMAGE="NO"
```

To update the base image, makes changes in the earthfile and then run [this workflow](https://github.com/earthly/website/actions/workflows/base-image-build.yaml).

## Linting

The blog has several linting steps. They run in CI, but you can also run them locally using `earthly +blog-lint`.

These linting errors can also be seen directly in VS Code if you install them natively (See Install Dependencies below ) and install vs-code extension `markdownlint` and `vale`.

Also the helper function `lint` exists which will correct some of the lint problems itself and return any it can't correct (see helper functions below).

## Run Blog Native on MacOS

Volume mounts on a mac can be slow, until such time as [watch mode](https://docs.google.com/document/d/18VIcpWBmQ8HcNlmtlZtc84mvJA87_QZePZZY1ZPLI90/edit) exists it can be worth it to run Jekyll natively.

### Install Dependencies

For blogging locally:

```
 brew update
 brew upgrade ruby-build
 brew install rbenv
 rbenv install 2.7.0
 rbenv global 2.7.0
 brew install vips
 brew install pandoc
 brew install dateutils 
```

Then, in `/blog/` run `bundle install`.

For linting locally (and in vs code):

```
 brew install vale
 brew install sponge
 brew install gawk
 brew install gnu-sed

 npm install -g markdownlint-cli@0.32.0
```

`gnu-sed` works different than the version of `sed` that comes with mac by default, so you need to add the line below to your `.bashrc` or `.zshrc` to get your system to use it.

```bash
# For Intel Mac
 export PATH="/usr/local/opt/gnu-sed/libexec/gnubin:$PATH"

# For M1 Mac
export PATH=/opt/homebrew/opt/gnu-sed/libexec/gnubin:$PATH
```

# Image compression

If you want to resize images for the blog, and recompress them using functions in `functions` on a mac install these:

**Warning: these take a while and install a lot of dependencies**

```
brew install pngquant
brew install jpegoptim
brew install imagemagick
``

## Helper Bash Functions

There are helper functions in `util/functions`. Once sourced, `list` lists them.

```bash
> source ./util/functions
functions assume they are run from repo root
run "list" for a list of helpers
```

```
> list
function             description
----------------     -----------------------------------------------------------------
clear-images()       Clear images for latest post
link-opp()           List places you could link to other posts
lint()               Run Linter
list-images
new-post()           Eg. new-post multi-word-slug
set-author-image()   Eg. set-author-image first-last.jpg
set-header()         Set latest-image as header using $IMAGE_DOWNLOADS
set-image()          Save latest-image using $IMAGE_DOWNLOADS
imgur(){             Download images from imgur from post and update post
start-blog(){        Start up blog on localhost:4002/blog
start-website(){     Start up website on localhost:4001
-----------------------------------------------------------------------------------------
```

## Build Site (Blog and Website)

Build this site into a folder of static files:

```
earthly +build
```

Results will be output to `build` and future dated posts will not be included.
To include future dated posts use:

```
earthly +dev-build
```

## How To Deploy

Anything merged into main is deployed using `earthly +build` in GitHub actions.

## FAQS

Question: A page is not updating - what did I do wrong?
Answer: Clear the cache with `earthly +clean`
