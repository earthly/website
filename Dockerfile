# DOCKER_BUILDKIT=1 docker build . -t agbell/website-base:latest 
#agbell/website-base:latest 
FROM ruby:2.7
WORKDIR /site

RUN apt-get update 
RUN apt-get install gcc cmake imagemagick -y
RUN gem install bundler -v "~>1.0" && gem install bundler jekyll

# # diagrams and stuff
RUN apt-get install cabal-install -y
RUN cabal update
RUN cabal install pandoc-plot --force-reinstalls
RUN cp /root/.cabal/bin/* /usr/bin/

RUN apt-get install python3-matplotlib -y
RUN apt-get install libvips -y
