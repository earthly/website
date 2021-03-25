FROM ruby:2.7
WORKDIR /site

## Base Image
deps:
    RUN apt-get update 
    RUN apt-get install gcc cmake imagemagick -y
    RUN gem install bundler -v "~>1.0" && gem install bundler jekyll
    # diagrams and stuff
    RUN apt-get install cabal-install -y
    RUN cabal update
    RUN cabal install pandoc-plot --force-reinstalls
    RUN cp /root/.cabal/bin/* /usr/bin/
    RUN apt-get install python3-matplotlib -y
    RUN apt-get install libvips -y

## Website
website-update:
  FROM +deps
  COPY website .
  RUN rm Gemfile.lock
  RUN bundle install
  RUN bundle update
  SAVE ARTIFACT Gemfile.lock AS LOCAL website/Gemfile.lock

website-install:
    FROM +deps
    COPY website/Gemfile .
    COPY website/Gemfile.lock .
    RUN bundle install --retry 5 --jobs 20

website-build:
  FROM +website-install
  COPY website .
  RUN RUBYOPT='-W0' bundle exec jekyll build
  SAVE ARTIFACT _site AS LOCAL build/site


website-docker:
    FROM +website-install
    CMD RUBYOPT='-W0' bundle exec jekyll serve --incremental -H 0.0.0.0 -P 4001
    SAVE IMAGE earthly-website

website-run:
  LOCALLY
  BUILD +website-docker
  RUN docker run -p 4001:4001 -v $(pwd)/website:/site earthly-website

## Blog
blog-update:
  FROM +deps
  COPY blog .
  RUN rm Gemfile.lock
  RUN bundle install
  RUN bundle update
  SAVE ARTIFACT Gemfile.lock AS LOCAL blog/Gemfile.lock

blog-install:
  FROM +deps
  COPY blog/Gemfile .
  COPY blog/Gemfile.lock .
  RUN bundle install --retry 5 --jobs 20

blog-build:
  FROM +blog-install
  COPY blog .
  RUN RUBYOPT='-W0' bundle exec jekyll build --future
  SAVE ARTIFACT _site AS LOCAL build/site/blog

blog-docker:
  FROM +blog-install
  CMD RUBYOPT='-W0' bundle exec jekyll serve -H 0.0.0.0 --future -P 4002
  SAVE IMAGE earthly-blog

blog-interactive:
  FROM +blog-install
  RUN --interactive /bin/bash

blog-run:
  LOCALLY
  BUILD +blog-docker
  # RUN docker kill $(docker ps -q) # Don't ask
  RUN docker run -p 4002:4002 -v $(pwd)/blog:/site earthly-blog

## Utils

clean:
  LOCALLY
  RUN rm -r build website/_site website/.sass-cache website/.jekyll-metadata website/.jekyll-cache || True
  RUN rm -r build blog/_site blog/.sass-cache blog/.jekyll-metadata blog/.jekyll-cache || True

# doesn't work
shell: 
  LOCALLY    
  BUILD +docker
  RUN --interactive docker run -p 4001:4001 -v $(pwd)/website:/site -it --entrypoint=/bin/bash earthly-website

# get shell, but no volume mount
static-shell:
  FROM +jekyll-install
  COPY website .
  RUN --interactive /bin/bash


## Prod
deploy:
  BUILD +website-build
  BUILD +blog-build
  RUN echo "Here we should deploy the contents of build/site to S3 or wherever prod earthly.dev is served from"
