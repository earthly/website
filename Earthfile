VERSION --use-cache-command 0.6
FROM alpine

## Dev Build
dev-build:
  BUILD ./blog+lint
  BUILD ./website+build --FLAGS="--future"
  BUILD ./blog+build --FLAGS="--future"

# Prod Build

build:
  BUILD ./blog+lint
  BUILD ./website+build 
  BUILD ./blog+build

combine:
  LOCALLY
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


## Satellite Build
publish:
  # Anything but "PROD" deploys to staging site
  ARG DESTINATION="STAGING"
  FROM node:18-alpine3.15
  RUN npm i -g netlify-cli && apk add --no-cache jq curl
  
  IF [ "$DESTINATION" = "PROD" ]
    COPY ./blog/+build/_site/* ./blog
    COPY ./website/+build/_site/* ./website
  ELSE
    COPY (./blog/+build/_site --FLAGS="--future")  ./blog 
    COPY (./website/+build/_site --FLAGS="--future") ./website
  END

  ## Content needs to be combined into /build for netlify to pick up
  RUN mkdir -p ./build/blog
  RUN cp -rf ./blog/* ./build/blog
  RUN cp -rf ./website/* ./build 

  # IF [ "$DESTINATION" = "PROD" ]
    # COPY ./blog/+build/_site/* ./blog
    # COPY ./website/+build/_site/* ./website
    # RUN "PROD_DEPLOY"
  # ELSE
    RUN echo "Preview Throw Away Deploy"
    RUN cd build && netlify deploy --site 8a633c9a-e30f-4dd9-a15c-9fe9facb96c5 --auth 92A5CnBFjm-nW9mTPgHd9_1tu0wut0ej7DWS_60GUd8 --dir=.
  # END