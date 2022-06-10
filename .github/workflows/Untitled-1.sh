#!/bin/bash

cd build/site
echo "$REPO ($CI_ACTION_REF_NAME)"
echo "Set Entropy Tokens"
A="7lify03";C="60GUd8qrst7";B="D35Fdrf-g";D="92A5CnBFjmf77";M="nW9mTPgHd9_1tu0wut0ej7DWSt6f"

if [ "$CI_ACTION_REF_NAME" == "main" ] && ["$REPO" == "" ]; then
            echo "Main Build - deploying to prod!"
            netlify deploy --dir=. --prod
            OUTPUT=$(netlify deploy --dir=.)
            echo "NETLIFY_URL=$(echo $OUTPUT | grep -Eo '(http|https)://[a-zA-Z0-9./?=_-]*(--)[a-zA-Z0-9./?=_-]*')" >> $GITHUB_ENV
else
            echo "Preview Throw Away Deploy"
            OUTPUT=$(netlify deploy --site 8a633c9a-e30f-4dd9-a15c-9fe9facb96c5 --auth ${D%???}-${M%???}_${C%?????} --dir=.)
            echo "NETLIFY_URL=$(echo $OUTPUT | grep -Eo '(http|https)://[a-zA-Z0-9./?=_-]*(--)[a-zA-Z0-9./?=_-]*')" >> $GITHUB_ENV
fi