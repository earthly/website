# Earthly Website & Blog

## Helper Bash Functions
There are helper functions in `util/functions`. Once sourced, `list` lists them.

```bash
> source ./util/functions
functions assume they are run from repo root
run "list" for a list of helpers
```

```
> list
function        	 description
----------------	 -----------------------------------------------------------------
clear-images()   	 Clear images for latest post
link-opp()       	 List places you could link to other posts
lint()            	 Run Linter
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

## Dependencies

To run locally you need the following dependencies:

* Ruby 
* Jekyll
* Pandoc (blog only)

You can use `start-blog` or `start-website` to start or run in docker (see below).

## Run Website in Docker

You can run the website locally, and use it to preview changes as you go.  Use `earthly` to do this, or repeat the steps earthly executes manually.

Build docker image for website:

```
> earthly +website-docker 
```

Run docker image with a volume mount:

```
> earthly +website-run
```

or

```
> docker run -p 4001:4001 -v $(pwd)/website:/site earthly-website
```

Then browse to http://0.0.0.0:4001/


## Run Blog in Docker

Build docker image for blog:

```
> earthly +blog-docker
```

Run docker image with a volume mount

```
> earthly +blog-run
```

or

```
docker run -p 4002:4002 -v $(pwd)/blog:/site earthly-blog
```

Then browse to http://0.0.0.0:4002/blog/

## Run Blog Native on MacOS

### Install Dependencies

```
 brew update
 brew upgrade ruby-build
 rbenv install 2.7.0
 rbenv global 2.7.0
 ruby -v
 brew install vips
 brew install pandoc
```

### Run

```
> source ./util/functions
> start-blog

```

## Build Site (Blog and Website):

Build this site into a folder of static files:

```
earthly +build
```

Results will be output to `build` and future dated posts will not be included.
To include future dated posts use:

```
earthly +dev-build
```

## How to Deploy

Anything merged into main is deployed using `earthly +build` in GitHub actions.

## FAQS

Question: A page is not updating - what did I do wrong?
Answer: Clear the cache with `earthly +clean`
