# Earthly Website

# deploy
 * merge to main deploys in netlify

 # dev environment
 ## Build
 ```
 cd src
 bundle exec jekyll build
 ```

 ## serve
 ```
 earthly +docker
 earthly +run
 ```
 navagate to localhost:4001

