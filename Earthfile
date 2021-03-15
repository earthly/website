FROM ruby:2.7-alpine
WORKDIR /site

deps:
    RUN apk add --no-cache build-base gcc bash cmake git
    RUN apk --update add imagemagick
    RUN gem install bundler -v "~>1.0" && gem install bundler jekyll


update:
  FROM +deps
  COPY website .
  RUN rm Gemfile.lock
  RUN bundle install
  RUN bundle update
  SAVE ARTIFACT Gemfile.lock AS LOCAL src/Gemfile.lock

jekyll-install:
    FROM +deps
    COPY website/Gemfile .
    COPY website/Gemfile.lock .
    RUN bundle install --retry 5 --jobs 20

build:
  FROM +jekyll-install
  COPY website .
  RUN RUBYOPT='-W0' bundle exec jekyll build
  SAVE ARTIFACT _site AS LOCAL build/site

deploy:
  FROM +build
  RUN echo "Here we should deploy the contents of build/site to S3 or wherever prod earthly.dev is served from"

docker:
    FROM +jekyll-install
    CMD RUBYOPT='-W0' bundle exec jekyll serve --incremental -H 0.0.0.0 -P 4001
    SAVE IMAGE earthly-website

run:
  LOCALLY
  BUILD +docker
  RUN docker run -p 4001:4001 -v $(pwd)/website:/site earthly-website

clean:
  LOCALLY
  RUN rm -r build website/_site website/.sass-cache website/.jekyll-metadata website/.jekyll-cache || True

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
