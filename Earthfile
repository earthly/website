VERSION 0.6
FROM alpine

## Dev Build
dev-build:
  BUILD ./blog+blog-lint
  BUILD --build-arg FLAGS="--future" ./website+website-build 
  BUILD --build-arg FLAGS="--future" ./blog+blog-build

# Prod Build
build:
  BUILD ./blog+blog-lint
  BUILD ./website+website-build 
  BUILD ./blog+blog-build

## Utils
clean:
  LOCALLY
  RUN rm -rf build website/_site website/.sass-cache website/.jekyll-metadata website/.jekyll-cache
  RUN rm -rf build blog/_site blog/.sass-cache blog/.jekyll-metadata blog/.jekyll-cache

## Files needed by blog and website that are in root dir need to be exported here 
## And reimported in blog and website earthfiles 
export:
  WORKDIR /base
  COPY .vale.ini .
  COPY .github .github
  COPY ./blog/.markdownlint.json .
  SAVE ARTIFACT /base
