VERSION 0.7 
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
  FROM node:18-alpine3.15

  BUILD ./blog/+lint

  RUN npm i -g netlify-cli && apk add --no-cache jq curl

  # Anything but "PROD" deploys to staging site
  ARG DESTINATION="STAGING"
  # Date is only used to bust the cache and get around this issue
  # https://github.com/earthly/earthly/issues/2086
  ARG DATE

  # Work around for netlify DNS issue
  HOST api.netlify.com 3.130.174.239

  IF [ "$DESTINATION" = "PROD" ]
    COPY (./blog/+build/_site --DATE="$DATE") ./blog
    COPY ./website/+build/_site ./website
  ELSE
    COPY (./blog/+build/_site --FLAGS="--future" --DATE="$DATE")  ./blog
    COPY (./website/+build/_site --FLAGS="--future") ./website
  END

  # ## Content needs to be combined into /build for netlify to pick up
  RUN mkdir -p ./build/blog
  RUN cp -rf ./blog/* ./build/blog
  RUN cp -rf ./website/* ./build

  IF [ "$DESTINATION" = "PROD" ]
    RUN --no-cache echo "PROD_DEPLOY"
    RUN --no-cache \
        --secret NETLIFY_SITE_ID \
        --secret NETLIFY_AUTH_TOKEN \
        cd build && netlify deploy --site "$NETLIFY_SITE_ID" --auth "$NETLIFY_AUTH_TOKEN" --dir=. --prod
  ELSE
    RUN --no-cache echo "Preview Throw Away Deploy"
    RUN --no-cache \
        --secret NETLIFY_STAGING_SITE_ID \
        --secret NETLIFY_STAGING_AUTH_TOKEN \
        cd build && netlify deploy --site "$NETLIFY_STAGING_SITE_ID" --auth "$NETLIFY_STAGING_AUTH_TOKEN" --dir=.
  END