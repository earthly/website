VERSION 0.6
FROM alpine

## Dev Build
dev-build:
  BUILD ./blog+lint
  BUILD ./website+build --FLAGS="--future"
  BUILD ./blog+build --FLAGS="--future"

# Prod Build
build:
  LOCALLY
  BUILD ./blog+lint
  BUILD ./website+build 
  BUILD ./blog+build

  ## Content needs to be combined into /build for netlify to pick up
  RUN mkdir -p ./build
  RUN cp -rf ./blog/build/* ./build
  RUN cp -rf ./website/build/* ./build

build-base-images:
  BUILD ./blog+base-image-all
  BUILD ./website+base-image-all  

## Files needed by blog and website that are in root dir need to be exported here 
## And reimported in blog and website earthfiles 
export:
  WORKDIR /base
  COPY .vale.ini .
  COPY .github .github
  COPY ./blog/.markdownlint.json .
  SAVE ARTIFACT /base

clean:
  LOCALLY
  BUILD ./blog+clean
  BUILD ./website+clean
  RUN rm -rf build
