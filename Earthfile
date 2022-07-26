VERSION 0.6
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
  
  ## Content needs to be combined into /build for netlify to pick up
  RUN mkdir -p ./build
  IF [ "$DESTINATION" = "PROD" ]
    COPY ./blog+build/site/* ./build
    # COPY ./website+build/_site/* ./build
  ELSE
    COPY (./blog+build/_site/* --FLAGS="--future")  ./build 
    # COPY (./website+build/_site/* --FLAGS="--future") ./build
  END
  RUN FALSE


          #   if [ "$CI_ACTION_REF_NAME" == "main" ] && [ "$REPO" == "" ]; then
          #   echo "Main Build - deploying to prod!"
          #   netlify deploy --dir=. --prod
          #   OUTPUT=$(netlify deploy --dir=.)
          #   echo "NETLIFY_URL=https://earthly.dev" >> $GITHUB_ENV
          # else
          #   echo "Preview Throw Away Deploy"
          #   OUTPUT=$(netlify deploy --site 8a633c9a-e30f-4dd9-a15c-9fe9facb96c5 --auth ${D%???}-${M%???}_${C%?????} --dir=.)
          #   echo "NETLIFY_URL=$(echo $OUTPUT | grep -Eo '(http|https)://[a-zA-Z0-9./?=_-]*(--)[a-zA-Z0-9./?=_-]*')" >> $GITHUB_ENV
          # fi