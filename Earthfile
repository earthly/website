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
  ARG NETLIFY_STAGING_SITE_ID
  ARG NETLIFY_STAGING_AUTH_TOKEN 

  FROM node:18-alpine3.15
  RUN npm i -g netlify-cli && apk add --no-cache jq curl
  RUN echo "$NETLIFY_STAGING_SITE_ID"
  RUN echo "$NETLIFY_STAGING_AUTH_TOKEN"

  # IF [ "$DESTINATION" = "PROD" ]
  #   COPY ./blog/+build/_site/* ./blog
  #   COPY ./website/+build/_site/* ./website
  # ELSE
  #   COPY (./blog/+build/_site --FLAGS="--future")  ./blog 
  #   COPY (./website/+build/_site --FLAGS="--future") ./website
  # END

  # ## Content needs to be combined into /build for netlify to pick up
  # RUN mkdir -p ./build/blog
  # RUN cp -rf ./blog/* ./build/blog
  # RUN cp -rf ./website/* ./build 

  # IF [ "$DESTINATION" = "PROD" ]
  #   RUN "PROD_DEPLOY"
  #   RUN cd build && netlify deploy --dir=. --prod
  # ELSE
  #   RUN echo "Preview Throw Away Deploy"
  #   RUN cd build && netlify deploy --site "$NETLIFY_STAGING_SITE_ID" --auth "$NETLIFY_STAGING_AUTH_TOKEN" --dir=.
  # END 