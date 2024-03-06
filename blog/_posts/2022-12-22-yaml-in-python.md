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
last_modified_at: 2023-10-18
---
**This article explains how to handle YAML files in Python. Earthly streamlines Docker image builds. [Check it out](https://cloud.earthly.dev/login).**

<iframe width="560" height="315" src="https://www.youtube.com/embed/FfbGrSDXtHU?si=gn5YQnyO7qKPcna2" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

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
---
apiVersion: v1
kind: persistentVolume
metadata:
  name: mysql-pv
  labels:
    type: local
spec:
  storageClassName: hostpath
capacity:
  storage: 2Gi
accessModes:
- ReadWriteOnce
hostpath:
  path: /mnt/data

~~~

## Writing YAML to a File in Python

![Writing YAML to a File in Python]({{site.images}}{{page.slug}}/XUdOKxs.png)\

Now that you've learned how to create YAML documents from Python objects, let's learn how to write them into a file for future use.

The `dump()` function optionally accepts a file object as one of its arguments. When you provide this optional file object argument, the `dump()` function will write the produced YAML document into the file.

Let's define a Python function `write_yaml_to_file()` that converts a Python object into YAML and writes it into a file.

~~~{.python caption="script.py"}
def write_yaml_to_file(py_obj,filename):
    with open(f'{filename}.yaml', 'w',) as f :
        yaml.dump(py_obj,f,sort_keys=False) 
    print('Written to file successfully')
write_yaml_to_file(data, 'output')
~~~

Upon calling the `write_yaml_to_file()` function with the `data` dictionary as the argument, the YAML file will be created in the working directory, as shown below:

<div class="wide">
![Viewing *data* dictionary in *yaml* format in the file *output.yaml* ]({{site.images}}{{page.slug}}/YF5c7y0.png)
</div>

Similarly, you can call the `write_yaml_to_file()` function with `data2` as the argument to convert it to YAML and store it into a YAML file.

~~~{.python caption="script.py"}
def write_yaml_to_file(py_obj,filename) :
    with open(f'{filename}.yaml', 'w',) as f :
        yaml.dump_all(py_obj,f,sort_keys=False)
    print('written to file successfully')
write_yaml_to_file(data2, 'output2')

~~~

<div class="wide">

![Viewing (*data2*) list of dictionaries in *yaml* format in a file (*output2.yaml*)]({{site.images}}{{page.slug}}/XoFh6F9.png)

</div>

## Reading YAML in Python

The *yaml* module comes with a function that can be used to read YAML files. This process of YAML files with PyYAML is also referred to as loading a YAML file.

### How to Read YAML Files With `safe_load()`

The `safe_load()` function is used to read YAML files with the PyYAML library. The other loader you can use but is not recommended is the `load()` function.

<aside>
💡 The `safe_load()` function is used to read YAML from unreliable and untrusted sources. The `load()` function is not reliable, especially when it is used to load a supposedly malicious script. The authors recommend using the `safe_load()` function instead. However, both functions have Python objects as their return type.
</aside>

The function `read_one_block_of_yaml_data` will open a *yaml* file in read mode, load its contents using the `safe_load()` function, and print out the output as a dictionary of dictionaries.

~~~{.python caption="script.py"}
def read_one_block_of_yaml_data(filename):
    with open(f'{filename}.yaml','r') as f:
        output = yaml.safe_load(f)
    print(output) 
    
read_one_block_of_yaml_data('output')
~~~

~~~{.yaml caption="Output"}
{'Name': 'John Doe', 'Position': 'DevOps Engineer', \
'Location': 'England', 'Age': '30', 'Experience': \
{'GitHub': 'Software Engineer', 'Google': 'Technical Engineer', \
'Linkedin': 'Data Analyst'}, 'Languages': {'Markup': ['HTML'],\
 'Programming': ['Python', 'JavaScript', 'Golang']}}
~~~

You can also read the contents of a YAML file, copy, and write its contents into another file. The code below will read a file *output.yaml* and write the content of that file, into another file *output3.yaml*.

~~~{.python caption="script.py"}
def read_and_write_one_block_of_yaml_data(filename,write_file):
    with open(f'{filename}.yaml','r') as f: 
        data = yaml.safe_load(f)
    with open(f'{write_file}.yaml', 'w') as file:
        yaml.dump(data,file,sort_keys=False)
    print('done!') 

read_and_write_one_block_of_yaml_data('output', 'output3')
~~~

You should have the following output:

<div class="wide">

![Viewing contents of read yaml *output.yaml* in file `output3.yaml`]({{site.images}}{{page.slug}}/O8N1jqh.png)

</div>

For reading *yaml* with multiple blocks of YAML data, you'll use the `safe_load_all()` function and convert the output to a list:

~~~{.python caption="script.py"}
def read_multiple_block_of_yaml_data(filename):
    with open(f'{filename}.yaml','r') as f:
        data = yaml.safe_load_all(f)
        print(list(data)) 
read_multiple_block_of_yaml_data('output2')
~~~

The output below shows the result as a list of dictionaries:

~~~{caption="Output"}
[{'apiVersion': 'v1', 'kind': 'persistentVolume', 'metadata': \
{'name': 'mongodb-pv', 'labels': {'type': 'local'}}, 'spec': \
{'storageClassName': 'hostpath'}, 'capacity': {'storage': '3Gi'}, \
'accessModes': ['ReadWriteOnce'], 'hostpath': {'path': '/mnt/data'}}, \
{'apiVersion': 'v1', 'kind': 'persistentVolume', 'metadata': \
{'name': 'mysql-pv', 'labels': {'type': 'local'}}, 'spec': \
{'storageClassName': 'hostpath'}, 'capacity': {'storage': '2Gi'}, \
'accessModes': ['ReadWriteOnce'], 'hostpath': {'path': '/mnt/data'}}]
~~~

If you try to load the data as it is, without converting it to a list, you'll get a generator object and a memory location and not the contents of the *yaml* file:

~~~{caption="Output"}
<generator object load_all at 0x7f9e0e0b6880>
~~~

<aside>
If you'd like to learn more about generators in Python and how they work, you can check out the [docs on Python generator expressions](https://docs.python.org/3/reference/expressions.html#generator-expressions)
</aside>

Similarly, you can also write the loaded data into another file:

~~~{.python caption="script.py"}
with open(f'{filename}.yaml','r') as f:
        data = yaml.safe_load_all(f)
        loaded_data = list(data)
with open('output4.yaml', 'w') as file:
        yaml.dump_all(loaded_data,file, sort_keys=False)
print('done!') 
~~~

And you have the complete function as follows:

~~~{.python caption="script.py"}
def read_multiple_block_of_yaml_data(filename,write_file):
    with open(f'{filename}.yaml','r') as f:
        data = yaml.safe_load_all(f)
        loaded_data = list(data)
    with open(f'{write_file}.yaml', 'w') as file:
        yaml.dump_all(loaded_data,file, sort_keys=False)
    print('done!') 

read_multiple_block_of_yaml_data('output2','output4')
~~~

<div class="wide">

![Reading and writing multiple blocks of yaml data]({{site.images}}{{page.slug}}/nghXeJI.png)

</div>

## Modifying YAML in Python

![Modifying YAML in Python]({{site.images}}{{page.slug}}/1Loo6M7.png)\

You can modify the contents of a YAML file using the `yaml` module with PyYAML. All you have to do is ensure the function takes in the following arguments: a YAML file to read and the key with the new value.

As an example, you'll replace the `data` dictionary `Age` key to have a value of `30` instead of `26`. The code below will create a function `read_and_modify_one_block_of_yaml_data` that takes in any YAML file as an argument. Then, it will read that file and modify the `Age` key to have a value of `30` and output the modified data.

~~~{.python caption="script.py"}
def read_and_modify_one_block_of_yaml_data(filename, key, value):
    with open(f'{filename}.yaml', 'r') as f:
        data = yaml.safe_load(f)
        data[f'{key}'] = f'{value}' 
        print(data) 
    print('done!')
    
read_and_modify_one_block_of_yaml_data('output', key='Age', value=30)
~~~

~~~{caption="Output"}
{'Name': 'John Doe', 'Position': 'DevOps Engineer', 'Location': \
'England', 'Age': '30', 'Experience': {'GitHub': 'Software Engineer', \
'Google': 'Technical Engineer', 'Linkedin': 'Data Analyst'}, \
'Languages': {'Markup': ['HTML'], 'Programming': \
['Python', 'JavaScript', 'Golang']}}
done!
~~~

You can optionally write the modified data into another file. The code below writes the modified data into another file *output5.yaml*.

~~~{.python caption="script.py"}

 def read_and_modify_one_block_of_yaml_data(filename,write_file, key,value):
    with open(f'{filename}.yaml', 'r') as f:
        data = yaml.safe_load(f)
        data[f'{key}'] = f'{value}'
        print(data)
    with open(f'{write_file}.yaml', 'w') as file:
        yaml.dump(data,file,sort_keys=False)
    print('done!') 
    
read_and_modify_one_block_of_yaml_data('output', \
'output5', key='Age', value=30)
~~~

Once executed successfully, you should have the following output:

<div class="wide">

![Modifying yaml data with one block of yaml data]({{site.images}}{{page.slug}}/Vx75ygy.png)\

</div>

To illustrate further, you can modify the *output2.yaml* file also. The code below, will modify the first block of YAML data and edit the `accessMode` to be both 'ReadAccessModes' and 'ReadOnlyMany' and write it to a file *output6.yaml*

~~~{.python caption="script.py"}

def read_modify_save_yaml_data(filename,index,key,value,write_file):
    with open(f'{filename}.yaml','r') as f:
        data = yaml.safe_load_all(f)
        loaded_data = list(data)
        loaded_data[index][f'{key}'].append(f'{value}')
    with open(f'{write_file}.yaml', 'w') as file:
        yaml.dump_all(loaded_data,file, sort_keys=False)
    print(loaded_data) 
    
read_modify_save_yaml_data('output2', 0, 'accessModes', \
'ReadOnlyMany', 'output6')
~~~

Once this code is executed, you should have the following output:

<div class="wide">

![Viewing modified *yaml*]({{site.images}}{{page.slug}}/1zYum42.png)\

</div>

## How to Convert YAML to JSON in Python

You can convert YAML to another data-serialization format like JSON.

Firstly, you'll need to import the `json` module from the Python standard library:

~~~{.bash caption=">_"}
import json 
~~~

Now, run the code below to convert a YAML document to a JSON object and save it in a file called `output.json`.

~~~{.python caption="script.py"}
def convert_yaml_to_json(yfile, jfile):
    with open(f'{yfile}.yaml', 'r') as f:
        yaml_file = yaml.safe_load(f)
    with open(f'{jfile}.json', 'w') as json_file:
        json.dump(yaml_file, json_file, indent=3)
    print('done!')
convert_yaml_to_json('output','output')
~~~

<aside>
The `json.dump()` function converts a Python object (YAML in this case) into a [JSON](/blog/convert-to-from-json) object. It takes in the following arguments: the Python object you want to convert, the JSON file you'd like to write it to, and an optional `index` value to specify how you want the JSON object to be formatted.
</aside>

Once converted successfully, you should have an `output.json` file in your working directory:

<div class="wide">

![new-3.png]({{site.images}}{{page.slug}}/WJ7ZS6j.png)\

</div>

## Conclusion

In this tutorial, you've learned how to handle YAML using Python and the PyYAML library. You've worked with functions like `safe_load()`, `safe_load_all()`, `dump()`, and `dump_all()` to manipulate YAML data and even convert it to JSON with Python's `json` library.

As you continue to explore and expand your Python skills, you might find yourself in need a CI process. If that's the case, give [Earthly](https://cloud.earthly.dev/login) a try. It's a great tool for automating Python builds and can significantly streamline your workflow.

Now, why not take your newfound knowledge a step further? Try converting [JSON to CSV](https://earthly.dev/blog/convert-to-from-json/) next.

{% include_html cta/bottom-cta.html %}
