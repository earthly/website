---
title: "How to validate and clean your YAML files using Kubeval and ValidKube"
toc: true
author: Boemo Wame Mmopelwa

internal-links:
 - YAML
 - Kubeval
 - ValidKube
 - Linux
excerpt: |
    Learn how to validate and clean your YAML files using Kubeval and ValidKube. These tools help you spot misconfigurations and remove clutter from your files, ensuring the security and health of your Kubernetes cluster.
last_modified_at: 2023-07-19
categories:
  - Orchestration
---
**The article focuses on Kubeval's importance in validating Kubernetes manifests. Earthly strengthens CI pipelines through reproducible builds, which complements Kubeval's functions. [Learn more about Earthly](https://cloud.earthly.dev/login).**

[Kubeval](https://www.kubeval.com/) is a [command line tool](/blog/golang-command-line) that validates Kubernetes manifests and YAML files using the Kubernetes API schema. Behind the scenes, Kubeval compares API schemas with objects provided in your YAML file to find any errors. Cleaning and validating your files is imperative because it helps you to spot misconfigurations that can introduce flaws to your cluster. All you have to do is run the Kubeval command which specifies your YAML file. Kubeval is a free and open-source project developed by [instrumenta](https://instrumenta.dev/).

Kubeval is an important tool if you are writing YAML files on a daily basis. You should use it to validate your files before applying them to your cluster. In this tutorial, you will learn how to validate your YAML files using Kubeval and ValidKube which is a web tool that cleans YAML files.

## We Will Cover the Following Points in This Article

1. How to install Kubeval on Linux
2. Validating files using Kubeval
3. Validating files using a specific schema
4. Skipping and ignoring commands
5. How to clean your files using Validkube
6. Conclusion

## Installing Kubeval on Linux

Use the following command to install Kubeval on your Linux machine:

~~~{.bash caption=">_"}
wget https://github.com/instrumenta/kubeval/releases/latest/download \
/kubeval-linux-amd64.tar.gz
tar xf kubeval-linux-amd64.tar.gz
sudo cp kubeval /usr/local/bin
~~~

If you're not using a Linux distribution you can check the Kubeval [docs](https://www.kubeval.com/installation/) for information on how to install the CLI on [Windows](/blog/makefiles-on-windows) or macOS.

Once the download is complete, you can confirm Kubeval has been installed successfully by using the following command:

~~~{.bash caption=">_"}
kubeval --version
~~~

You will get the following output message that shows the Kubeval version:

~~~{.bash caption="output"}
Version: 0.15.0
Commit: df50ea7fd4fd202458002a40a6a39ffbb3125bad
Date: 2020-04-14T09:32:29Z
~~~

If you get stuck while using Kubeval, use the following command to get all available Kubeval commands:

~~~{.bash caption=">_"}
 kubeval --help
~~~

## Validating Yaml Files Using Kubeval

Kubeval allows you to validate Kubernetes objects or resources stated in a YAML file. In this tutorial, you will learn to validate files by validating a ClusterRole. Create a file called `secret-reader.yaml` and add the following contents:

~~~{.yaml caption="secret-reader.yaml"}
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  namespace: organization
  name: secret-reader
rules:
- apiGroups: [""] # "" indicates the core API group
  resources: ["secrets"]
  verbs: ["get", "watch", "list"]
~~~

The above `ClusterRole` gives the user the right to get, watch and list secrets. Use the following command to validate the file:

~~~{.bash caption=">_"}
kubeval secret-reader.yaml
~~~

You will get the following output:

~~~{.bash caption="output"}
←[32mPASS←[0m - secret-reader.yaml contains a valid ClusterRole \
(organization.secret-reader)
~~~

Underneath the hood, Kubeval compared the `secret-reader.yaml` file to this [Jsonschema](https://github.com/garethr/kubernetes-json-schema/blob/master/v1.11.2/clusterrole-rbac-v1alpha1.json). As you can see, we provided it a valid file, so the scan passed with no errors or insecurities.

Now, let's use a YAML file that has missing metadata and see if Kubeval will spot the error. Here is the full file with the error:

~~~{.yaml caption="secret-reader.yaml"}
apiVersion: v1
kind: Service
spec:
  externalTrafficPolicy: Local
  ports:
  - name: http
    port: 80
    protocol: TCP
    targetPort: 80
  selector:    
    app: nginx
  type: NodePort

~~~

Use the following command to validate the above YAML file.

~~~{.bash caption=">_"}
kubeval service-ingress.yml
~~~

You will get the following output that shows that the missing key error has been detected:

~~~{.bash caption="output"}
←[31mERR ←[0m - service-ingress.yml: Missing 'metadata' key
~~~

When Kubeval gives you scan results that have errors, don't execute the YAML file, rather correct it using [ValidKube](https://validkube.com/) or [Kubescape](https://earthly.dev/blog/kubescape/). In this way, you will secure your cluster and prevent errors that could cost you hours to fix.

To correct the previous issue, add the metadata key that Kubeval had indicated as missing. The metadata segment in a Kubernetes resource file contains the name of the object, namespace, and other details. Here is the complete service YAML file that has metadata:

~~~{.yaml caption="secret-reader.yaml"}
apiVersion: v1
kind: Service
metadata:
  name: my-service
  namespace: newmetric
  labels:
    app: nginx
spec:
  externalTrafficPolicy: Local
  ports:
  - name: http
    port: 80
    protocol: TCP
    targetPort: 80
  selector:    
    app: nginx
  type: NodePort
~~~

If you scan the above contents using Kubeval again you will get the following output:

~~~{.bash caption="output"}
←[32mPASS←[0m - service.yaml contains a valid Service (newmetric.my-service)

~~~

## Converting Kubeval Results to Json and Tap Format

If you are more familiar with JSON or TAP, Kubeval allows you to output the results in [JSON](/blog/convert-to-from-json) or TAP format. This will help you analyze results better since you understand the JSON format much better.

Use the following command to get the validation results in JSON format:

~~~{.bash caption=">_"}
 kubeval secret-reader.yaml -o json
~~~

You will get the scan results in JSON format:

~~~{.json caption="output"}
[
        {
                "filename": "secret-reader.yaml",
                "kind": "ClusterRole",
                "status": "valid",
                "errors": []
        }
]
~~~

Use the following command to get the validation results in TAP format:

~~~{.bash caption=">_"}
kubeval secret-reader.yaml -o tap
~~~

You will get the following output:

~~~{.bash caption="output"}
1..1
ok 1 - secret-reader.yaml (ClusterRole)
~~~

## Validating Files Using a Specific Kubernetes Version

Kubeval has the `--kubernetes-version` flag which allows you to choose a specific version of a Kubernetes schema. For example:

~~~{.bash caption=">_"}
kubeval --kubernetes-version 1.16.1 service-ingress.yml
~~~

You can also use the [OpenShift JSON Schemas](https://github.com/garethr/openshift-json-schema) to validate your YAML files. Use the following flag to specify the version of OpenShift schema you want to use:

~~~{.bash caption=">_"}
kubeval --openshift -v 1.5.1   service-ingress.yml
~~~

## How To Ignore Missing Schemas

The `--ignore-missing-schemas` flag should be used when validating resources using Custom Resource Definitions(CRDs). Currently, Kubeval relies on schemas generated from the Kubernetes API. This means it's not possible to validate resources using CRDs. Kubeval currently supports schemas created by the Kubernetes API only.

~~~{.bash caption=">_"}
kubeval --ignore-missing-schemas service-ingress.yml
~~~

You will get the following output:

~~~{.bash caption="output"}
←[33mWARN←[0m - Set to ignore missing schemas
←[31mERR ←[0m - service-ingress.yml: Missing 'metadata' key
~~~

## How to Clean Your Files Using Validkube

After validating your files using Kubeval, it is important to remove clutter from the YAML files using [Validkube](https://validkube.com/) which is an online web tool that uses [Kube-neat](https://github.com/itaysk/kubectl-neat) to clean your files. You don't have to install anything to use it, all you have to do is copy and paste your files on [ValidKube](https://validkube.com/).

Let's clean the following [deployment](/blog/deployment-strategies) object using ValidKube:

~~~{.yaml caption="secret-reader.yaml"}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  namespace: example
  labels:
    app: nginx
spec:
  replicas: "Wrong"
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        args: []
        ports:
        - containerPort: 80
        resources: {}
~~~

Go to the [ValidKube website](https://validkube.com/) and paste the above content. Click on the "Clean" button to remove clutter from the deployment file:

<div class="wide">

![ValidKube dashboard]({{site.images}}{{page.slug}}/EIwWrGZ.jpg)

</div>

You will get the following results that show a clutter-free YAML file. The ` resources: {} `field has been removed since it was making the YAML file longer and it was not assigned any values. Also, the "" around `Wrong` were removed for the value of replicas.

~~~{.yaml caption="secret-reader.yaml"}
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: nginx
  name: nginx-deployment
  namespace: example
spec:
  replicas: Wrong
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - image: nginx:1.14.2
        name: nginx
        ports:
        - containerPort: 80
~~~

## Conclusion

In this tutorial, we covered using Kubeval and ValidKube for file validation and YAML clean up in Kubernetes. Using these tools will bolster your Kubernetes security, simplify tasks, and catch cluster errors. They help uncover hidden flaws in your manifests which can significantly improve your cluster's health over time. Remember, in Kubernetes, security isn't an afterthought but a priority.

Also if you're also looking for consistent build automation in your development process, you might want to give [Earthly](https://cloud.earthly.dev/login) a shot. It could be the tool you need to streamline your builds and ensure consistency across different environments.

{% include_html cta/bottom-cta.html %}
