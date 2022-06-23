---
title: "Code From Anywhere: Dev Containers and Github Codespaces"
categories:
  - Tutorials
toc: true
author: Josh

internal-links:
 - just an example
---

## Prerequisites
For this tutorial you'll need the following:

- VSCode
- Github Account
- Working knowledge of Docker and docker-compose
- Github Organization with billing enabled (For Codespaces portion only)

## What are Dev Containers?
Dev Containers are a VS Code feature that allows you to define a development environment with a Docker or docker-compose file and then run your project in that environment with the click of a button. Because VS Code can run in the browser, Dev Containers, along with Github Codespaces, also allow you to develop in the cloud from almost anywhere. They're great for standardizing development across a team. They can also make working on several repos at once much easier because each repo can have its own specific environment for development.

We recently started using Dev Containers for our Jekyll blog here at Earthly. We have a lot of different plugins and dependencies to make things like linting, spell check, and image importing much easier. The problem is, a lot of this was originally set up on an Intel Mac. Now that the team has grown, there are developers using M1s, Linux, and Windows, and so as you can imagine, a lot of our teammates who just want to write a simple blog entry were getting stuck just trying to get the blog working locally. Not only did Dev Containers with Codespaces solve this issue for us, it made development in general much easier and more portable. 

For this tutorial I thought I'd work with a [sample Django project](https://github.com/jalletto/circle_ci_python_example) I set up for a [previous article](https://earthly.dev/blog/circle-ci-with-django/). It has a few dependencies and also relies on a Postgresql database. Feel free to follow along with that repo, but just know that very little of what we cover will be unique to Python or Django, so you should be able to follow along with your own project as well.

## The Files

All Dev Container set ups start with a `.devcontainer/devcontainer.json`. In here you can set environment variables unique to the dev environment, install additional resources, include any VS Code plugins that might be necessary or helpful, run commands after the container is done spinning up and much more. MAYBE ADD SOMETHING ABOUT customizations and dot files?

Since a Dev Container is just a Docker container, you can define it the same way you define any container, in a Dockerfile or using a docker-compose file or a combination of both. You can also pull an existing image. Most set ups will use some combination of `devconatiner.json` and a Dockerfile

## Getting Set Up

VS Code provides a lot of template projects to help you get started with Dev Containers, and though you can just as easily create these files yourself, I recommend starting with a template and then adding and deleting to customize your set up from there. To view the optional template press `cmd + shift + p` and then type `Remote-Containers: Add Development Container Configuration Files`.

![remote containers options]({{site.images}}{{page.slug}}/remote-containers.png)

After you click here you'll have a few options depending on your repo. VS Code will suggest pre-defined templates based on what kinds of files it finds in your project. For example, there's no Django template, but the the first suggesting for me was `Python3 with Postgresql`, which is exactly what I needed. After this you are given the option to add additional features like Homebrew, Docker, the AWS Cli and many more. These options just get added to your `devconatiner.json`, so if you don't know what you'll need don't worry, it's easy to add them later. I didn't need anything else so I left these out and clicked OK. 

If you're following along with the Django app, you should have three new files.

- `.devconatiners/devcontainer.json `
- `.devconatiners/Dockerfile`
- `.devconatiners/docker-compose.yml`

Let's take a quick look at each one.

### devconatiner.json

```json
{
	"name": "Python 3 & PostgreSQL",
	"dockerComposeFile": "docker-compose.yml",
	"service": "app",
	"workspaceFolder": "/workspace",

	// Configure tool-specific properties.
	"customizations": {
		// Configure properties specific to VS Code.
		"vscode": {
			// Set *default* container specific settings.json values on container create.
			"settings": { 
				"python.defaultInterpreterPath": "/usr/local/bin/python",
				"python.linting.enabled": true,
				"python.linting.pylintEnabled": true,
				"python.formatting.autopep8Path": "/usr/local/py-utils/bin/autopep8",
				"python.formatting.blackPath": "/usr/local/py-utils/bin/black",
				"python.formatting.yapfPath": "/usr/local/py-utils/bin/yapf",
				"python.linting.banditPath": "/usr/local/py-utils/bin/bandit",
				"python.linting.flake8Path": "/usr/local/py-utils/bin/flake8",
				"python.linting.mypyPath": "/usr/local/py-utils/bin/mypy",
				"python.linting.pycodestylePath": "/usr/local/py-utils/bin/pycodestyle",
				"python.linting.pydocstylePath": "/usr/local/py-utils/bin/pydocstyle",
				"python.linting.pylintPath": "/usr/local/py-utils/bin/pylint",
				"python.testing.pytestPath": "/usr/local/py-utils/bin/pytest"
			},
			
			// Add the IDs of extensions you want installed when the container is created.
			"extensions": [
				"ms-python.python",
				"ms-python.vscode-pylance"
			]
		}
	},

	// Use 'forwardPorts' to make a list of ports inside the container available locally.
	// This can be used to network with other containers or the host.
	"forwardPorts": [8080],

	// Use 'postCreateCommand' to run commands after the container is created.
	// "postCreateCommand": "pip install --user -r requirements.txt",

	// Comment out to connect as root instead. More info: https://aka.ms/vscode-remote/containers/non-root.
	"remoteUser": "vscode"
}

```
This file is the base file for our Dev Container. This file gets read first, before the container is spun up. For now most of what is defined in here is specific to how we want VS Code to be set up, including adding some settings specific to Python, and including two extensions. The only thing we want to update in this file is the `forwardedPorts` section. Django's webserver runs on port 8000. This will forward port 8000 in the container to `localhost:8000` on our machine and allow us to open our Django app in the browser. 

### Dockerfile

```Dockerfile

ARG VARIANT=3-bullseye
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
   && rm -rf /tmp/pip-tmp

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

```
The most important thing in the Dockerfile is the `COPY` and `RUN` commands that install our Python packages. In Python, packages are listed in a `requirements.txt` file and downloaded with a package manager called pip.

Notice how we don't need to copy in the other files in project after we download our packages. After the container get's created, VS Code will make a shallow clone of our repo inside the container for us.

### dockerComposeFile

```yml
version: '3.8'

services:
  app:
    build:
      context: ..
      dockerfile: .devcontainer/Dockerfile
      args:
        VARIANT: "3"
        NODE_VERSION: "none"

    volumes:
      - ..:/workspace:cached

    command: sleep infinity

    network_mode: service:db

  db:
    image: postgres:latest
    restart: unless-stopped
    volumes:
      - postgres-data:/var/lib/postgresql/data
    hostname: postgres
    environment:
      POSTGRES_DB: my_media
      POSTGRES_USER: example
      POSTGRES_PASSWORD: pass
      POSTGRES_HOST_AUTH_METHOD: trust
    ports:
      - 5432:5432

volumes:
  postgres-data: null

```
Not all projects will have a `docker-compose.yml`, but because we wanted to have PostgreSQL, one was generated for us.
The only thing I added here was the `environment` section under `db` with some variables specific to how my app connects to Postgres.

## Running Your Dev Container

Now you can run `cmd + shift + P` and type `Remote-Containers: Open Folder in Container`. Everything will disapear for a minute while the containers spin up. Once your back up pull up your terminal and you're now inside your dev container! All the files in your project should be available in the default directory `/workspace`.

![My local machine is a Mac. But you can see here I'm running in a Linux container.]({{site.images}}{{page.slug}}/container-terminal.png)

As long as you forwarded the correct port in your `devcontainer.json`, you should be able to run your app as you normally would. In my case, I'll first need to run my database migrations.

```Python
python manage.py migrate
```
And then I can start my server.

```Python
python manage.py runserver
```
Now I can go to `http://127.0.0.1:8000/media/` to see my app's only page.

## Codespaces
Dev Containers let you run any project in a Docker container. You can do this locally, as we've seen, or you can do it remotely in the cloud using Github's Codespaces. Codespaces is a cloud computing service that lets you run a Dev Container on remote hardware and access it from almost anywhere. 

### Enabling Codespaces

Because Codespaces is a billed service (there is currently no free option), you'll need to have an [organization](https://docs.github.com/en/organizations/collaborating-with-groups-in-organizations/about-organizations) set up with a credit card to use them. 

To enable Codespaces for your organization, go to your orgs settings page. On the left, scroll down to Codespaces and click general.
Here you can choose to active Codespaces with a number of options for who can use them. You can turn them on for everyone in your org, select certain members or allow anyone in your org and anyone you invite to a repo as a collaborator to use them. Just make sure whoever has access is trusted as [compute time can add up quickly](https://docs.github.com/en/billing/managing-billing-for-github-codespaces/about-billing-for-codespaces).

![Turn On Code Spaces in Your Org Settings]({{site.images}}{{page.slug}}/turn-on-codespaces.png)

### What About Forks?

Codespaces are tied to organizations. If someone outside your organization forks your repo, they won't have the ability to use any Codespaces tied to your account. They can, however, use your Dev Container set up to run a Codespace in their own organization billed to their own credit card.

### Setting Up Codespaces

Once Codespaces is enabled for your organization, you'll be able to click the green `Code` button at the top right of any repo. You should see a tab on right for Codespaces.

![Creating a Codespace]({{site.images}}{{page.slug}}/create-codespace.png)

You can click the button to create a Codespace right away with the default settings, or you can click the arrow next to the button and select "Configure and Create Codespace". 

![Configure a Codespace]({{site.images}}{{page.slug}}/configure.png)

This will take you to a new page where you can select a different branch and a machine type. Once you have everything configured the way you want it click "create Codespace". You'll be taken to a screen similar to the one below. 

![Your container is spinning up.]({{site.images}}{{page.slug}}/creating.png)

You can wait for Codespaces to open up a VS Code right in your browser, or you can click the button to have it open in your local version of vscode. I found working in the browser to be a pretty good experience. The biggest problem was that I didn't have access to all of my shortcuts I'm so used to. For that one reason I usually choose to open a Codespace locally. If you do choose to use VS Code in the browser, be sure to choose dark mode right away or someone from StackOverflow will be dispatched to your home to break your legs.

If you already have a Dev Container set up like we did in the last section, then that will be used to create your Codespace environment in the cloud. 

But don't worry if you haven't taken any steps to configure a Dev Container yet. Github will spin up their default containerfor you. This default container does its best to be a catch all, so it has many different languages and packages built into it. For some quick edits or certain projects, it may be all you need. But to get the most out of Codespaces, you'll want to take the time to set up a Dev Container specific to your project.

### Stopping Your Codespace

Codespaces cost money. When you're finished using them, remember to shut them off. Simply closing VS Code will not do the trick. Remember this is a container running in the cloud. You can stop the code space by clicking the work Codespaces in the bottom left corner of your VS Code window or by pressing `cmd + shift + P` and typing stop until you see "Codespaces: Stop Current Codepsace", which you can click to turn it off.

![]({{site.images}}{{page.slug}}/stoping.png)
![]({{site.images}}{{page.slug}}/stop.png)

If you're ever unsure if you have any Codespaces running, you can see all your Codespaces by clicking on your profile pic in the upper right of the Github menu bar and navigating to Your Codespaces.

![]({{site.images}}{{page.slug}}/personal-cs.png)

### A Few Last things

- 
- Yes, you can start a Codepsace from your phone. No, it is not usable in any way.

{% include cta/cta1.html %}

- [ ] Fix Grammarly Errors
- [ ] First two paragraphs: What's it about? Why listen to you?
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
- [ ] Run mark down linter (`lint`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `link-opp` and find 1-5 places to incorporate links to other articles
- [ ] Add Earthly `CTA` at bottom ``
- [ ] Raise PR

- you can set constriants for codespaces org -> codespace -> general
- billing https://docs.github.com/en/billing/managing-billing-for-github-codespaces/about-billing-for-codespaces
- You'll need an organization
- Code spaces cost money