FROM ruby:2.7
RUN apt-get update 
RUN apt-get install sudo
RUN sudo apt-get install build-essential
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/Linuxbrew/install/master/install.sh)"

ENV PATH="/home/linuxbrew/.linuxbrew/bin:${PATH}"
RUN apt-get install gcc cmake imagemagick -y 
RUN gem install bundler -v "~>1.0" && gem install bundler jekyll
RUN apt-get install python3-matplotlib libvips-dev python3-pip npm pandoc -y
RUN pip3 install pandocfilters
RUN npm install -g markdownlint-cli
RUN brew install vale sponge gawk
