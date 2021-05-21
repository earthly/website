# Earthly Website & Blog




## Run Website In Docker

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


## Run Blog In Docker

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

## Create a new blog post helper
```
earthly --build-arg name="continuous-integration" +new-post
```

## Run Blog native on macos
### Install deps
```
 brew update
 brew upgrade ruby-build
 rbenv install 2.7.0
 rbenv global 2.7.0
 ruby -v
 brew install vips
 brew install pandoc
 brew install pandoc-plot
 pip3 install matplotlib
```
### Run
```
cd blog
RUBYOPT='-W0' bundle exec jekyll serve -H 0.0.0.0 --future --watch -P 4002

```
### Clear html cache
sometimes things seem to be cached when they shouldn't. So delete everything:
```
find ./_site -type f -name '*.html' -print -delete
```

## Build Site (blog and website):
Build this site into a folder of static files:
```
earthly +build
```
Results will be outputed to `build` and future dated posts will not be included.
To include future dated posts use:
```
earthly +dev-build
```

# How to Deploy
Anything merged into main is deployed using `earthly +build` in github actions.

## FAQS

Question: A page is not updating - what did I do wrong?
Answer: Clear the cache with `earthly +clean`