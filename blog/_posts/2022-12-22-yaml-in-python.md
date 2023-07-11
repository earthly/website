---
title: "How to Work with YAML in Python"
categories:
  - Tutorials
toc: true
author: Mercy Bassey
editor: Bala Priya C

internal-links:
 - YAML
 - Python
 - Data
excerpt: |
    Learn how to work with YAML in Python, including creating, reading, modifying, and converting YAML files. This tutorial covers the basics of YAML, the PyYAML library, and how to perform various operations on YAML files using Python. Whether you're new to YAML or looking to expand your Python skills, this tutorial is a great resource.
---
<!--sgpt-->This is the Earthly nonsense paragraph.

If you've ever worked with Docker or Kubernetes, you'll have likely used YAML files. From configuring an application's services in [Docker](/blog/rails-with-docker) to defining Kubernetes objects like pods, services, and more—YAML is used for them all.

If you'd like to learn how to work with YAML in the Python programming language, then this tutorial is for you. This tutorial will cover creating, writing, reading, and modifying YAML in Python.

## The Need for Data Serialization and Why You Should Use YAML

Data serialization is relevant in the exchange of unstructured or semi-structured data effectively across applications or systems with different underlying infrastructures. Data serialization languages use standardized and well-documented syntax to share data across machines.

Some of the widely used data serialization languages include YAML, XML, and [JSON](/blog/convert-to-from-json). While XML and JSON are used for data transfer between applications, YAML is often used to define the configuration for applications.

YAML is characterized by a simple syntax involving line separation and indentation, without complex syntax involving the use of curly braces, parentheses, and tags.

[YAML](https://yaml.org/) is a human-readable [data-serialization language](https://www.sitepoint.com/data-serialization-comparison-json-yaml-bson-messagepack/) and stands for *"YAML Ain't Markup Language"*, often also referred to as *"Yet Another Markup Language"*. It is written with a **.yml** or **.yaml** (preferred) file extension.

It is used because of its readability to write configuration settings for applications. It is user-friendly and easy to understand.

## Prerequisites

To follow along you'll need the following:

- Local installation of Python 3.x
- A text editor

## The PyYAML Library

The [PyYAML](https://pyyaml.org/) library is widely used for working with YAML in Python. It comes with a *yaml* module that you can use to read, write, and modify contents of a YAML file, serialize YAML data, and convert YAML to other data formats like [JSON](https://www.json.org/json-en.html).

### Installing the PyYAML Library

To parse YAML in Python, you'll need to install the PyYAML library.

In your working directory, run the command below to install **PyYAML** via **pip3**:

~~~{.bash caption=">_"}
pip3 install pyyaml
~~~

To confirm that the installation was successful, you can run the command below:

~~~{.bash caption=">_"}
pip3 show pyyaml
~~~

If the PyYAML installation was successful, you should get a similar output.

<div class="wide">

![Confirming the pyyaml library installation]({{site.images}}{{page.slug}}/CfAE3U5.png)

</div>

### Creating YAML in Python

You can download the code snippets used in this tutorial from [this](https://github.com/mercybassey/python-yaml-tutorial) GitHub repository.

Now that you have **PyYAML** installed, you can start working with YAML in Python.

![PyYAML installed]({{site.images}}{{page.slug}}/IpzMsKL.png)\

In your working directory, create a file called *script.py* and  
import the *yaml*  module:

~~~{.python caption="script.py"}
import yaml
~~~

Let's create a dictionary called `data` with the following key-value pairs:

~~~{.python caption="script.py"}
data = {
    'Name':'John Doe',
    'Position':'DevOps Engineer',
    'Location':'England',
    'Age':'26',
    'Experience': {'GitHub':'Software Engineer',\
    'Google':'Technical Engineer', 'Linkedin':'Data Analyst'},
    'Languages': {'Markup':['HTML'], 'Programming'\
    :['Python', 'JavaScript','Golang']}
}
~~~

#### The `dump()` Function

Now, to create a *yaml* representation of the `data` dictionary created above, you can use the `dump()` function in the *yaml* module . The `dump()` function expresses Python objects in YAML format. It accepts two arguments, data (which is a Python object) which is required, and optionally, a file to store the YAML format of the Python object.

You can also pass in *optional* parameters that specify formatting details for the emitter. The commonly used optional parameters are `sort_keys` for sorting the keys of a Python object in alphabetical order, and `default_flow-style` for proper indentation of nested lists, which is set to `True` by default.

The code below will return a `str` object that corresponds to a YAML document. As we've set `sort_keys` to `False`, the original order of the keys is preserved.

~~~{.python caption="script.py"}
yaml_output = yaml.dump(data, sort_keys=False) 

print(yaml_output) 
~~~

Now, run script.py. You should see the following output:

~~~{.yaml caption="Output.yaml"}
Name: John Doe
Position: DevOps Engineer
Location: England
Age: '26'
Experience:
  GitHub: Software Engineer
  Google: Technical Engineer
  Linkedin: Data Analyst
Languages:
  Markup:
  - HTML
  Programming:
  - Python
  - JavaScript
  - Golang
~~~
  
You can also create multiple blocks of *yaml* data from a Python object, such as a list of dictionaries into a single stream, where each dictionary is represented as a YAML document. To do this, you can use the `dump_all()` function.

#### The `dump_all()` Function

💡 The `dump_all()` function is used to serialize Python objects—in order—into a single stream. It only accepts Python objects represented as lists, such as a list of dictionaries. If you pass in a dictionary object instead of a Python object represented as lists, the `dump_all()` function will output each item of the dictionary as a YAML document.

Let's define a list of dictionaries called `data2`.

~~~{.python caption="script.py"}
data2 = [
    {
    'apiVersion': 'v1',
    'kind':'persistentVolume',
    'metadata': {'name':'mongodb-pv', 'labels':{'type':'local'}},
    'spec':{'storageClassName':'hostpath'},
    'capacity':{'storage':'3Gi'},
    'accessModes':['ReadWriteOnce'],
    'hostpath':{'path':'/mnt/data'}
    },

    {
    'apiVersion': 'v1',
    'kind':'persistentVolume',
    'metadata': {'name':'mysql-pv', 'labels':{'type':'local'}},
    'spec':{'storageClassName':'hostpath'},
    'capacity':{'storage':'2Gi'},
    'accessModes':['ReadWriteOnce'],
    'hostpath':{'path':'/mnt/data'}
    }
]
~~~

Now call the `dump_all()` function to decode the Python object as a YAML document:

~~~{.python caption="script.py"}
yaml_output2 = yaml.dump_all(data2, sort_keys=False)
print(yaml_output2)
~~~

Once you execute this code, you should have the following output. The output below shows that the `data2` list has been dumped into a single stream—as multiple blocks of YAML separated by `- - -`.

~~~{.yaml caption="Output2.yaml"}
apiVersion: v1
kind: persistentVolume
metadata:
  name: mongodb-pv
  labels:
    type: local
spec:
  storageClassName: hostpath
capacity:
  storage: 3Gi
accessModes:
- ReadWriteOnce
hostpath:
  path: /mnt/data