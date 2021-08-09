5 Useful jq Commands to Parse JSON on the CLI
JSON has become the de facto standard data representation for the web. It’s lightweight, human-readable (in theory) and supported by all major languages and platforms. However, working on the CLI with JSON is still hard using traditional CLI tooling.

Lucky, there is jq, a command-line JSON processor. jq offers a broad range of operations to transform and manipulate JSON based data structures from the command line. Looking at the documentation however reveals an overwhelmingly huge number of options, functions and things you can do with jq. This blog post shows 5 useful jq commands that you really need to know.

The GitHub Events API as Example
Most jq examples contain trivial JSON and data structures. That’s why the examples in this blog post will make use of the publicly available GitHub events API to parse some complex and nested JSON data. To get a feeling of the data we’re now digesting feel free to open the events endpoint in your browser:

To try out the commands shown in this blog post fetch a snapshot of the endpoint (as it’s output is constantly changing) and work on the file. That allows you to experiment with the jq commands while you can still inspect the data in a text editor. To do so, let’s create a file called events.json from the endpoint:

# store the most recent 30 events on GitHub to a file
$ curl https://api.github.com/events > events.json
We’ll be using the events.json file as example throughout this blog post. If you want to experiment I’d suggest you do this too, so that not on every execution your data changes. Of course, you’re free to directly pipe the output of the curl directly to jq.

Exploring the Data Structure
If you’re lucky to have access to the API or data format documentation like we do now, this is the perfect time to familiarize yourself with the format. If not, have a look at the JSON keys and what value they typically contain.

For the GitHub events API you can have a look at the detailed documentation. It’s important to first understand the high-level structure. For the events that is:

id: Each event has an identifier. Typically any data set has some kind of identifying key.
type: Used to classify events.
actor: Someone must have triggered the event.
repo: All events belong to a repository.
payload: And the event finally contains specific payload.
Now let’s explore the data we have at hand with jq.

1) Extract a Specific Element From an Array
To familiarize with unknown data it usually makes sense to look at one specific data point, in our case a single event. With the array selector you can show exactly one element in a JSON array:

# Look at the third array element
$ cat events.json | jq '.[2]'
{
  "id": "12417731482",
  "type": "DeleteEvent",
  "actor": {
    "id": 37642427,
    "login": "hdamico",
    "display_login": "hdamico",
    "gravatar_id": "",
    "url": "https://api.github.com/users/hdamico",
    "avatar_url": "https://avatars.githubusercontent.com/u/37642427?"
  },
  "repo": {
    "id": 228452889,
    "name": "rootstrap/rs-code-review-metrics",
    "url": "https://api.github.com/repos/rootstrap/rs-code-review-metrics"
  },
  "payload": {
    "ref": "release/2020.05.22",
    "ref_type": "branch",
    "pusher_type": "user"
  },
  "public": true,
  "created_at": "2020-05-22T21:30:48Z"
}
Negative indices actually allow to retrieve the last element of the data set. That means that .[-1] refers to the last element and .[-2] to the second last element of the data set. Using the array operator, arrays can also be sliced by using the colon in an index: .[3:7] will return the subset if the array starting from index 3 (inclusive) all until index 7 (exclusive).

These commands are very powerful in the beginning to familiarize with a data set and see the similarities and differences between individual objects.

2) Extract a Specific Key for All Elements
Once we identified an interesting key, we can examine how that specific key looks like for all elements of an array. To do so, we can leverage the map operator to map each array element to a different representation:

# extract the repository name for each event
$ cat events.json | jq 'map(.repo.name)'
[
  "rootstrap/rs-code-review-metrics",
  "Dmitriy-Podanev/Dependency-Injection",
  ...
  "jesielviana/programacao-para-internet-i",
  "supertester00/Galileo"
]
We can also extract multiple keys for each array element by using the map function in combination with object construction:

# extract the type and repository name for all events
$ cat events.json | jq 'map({type: .type, reponame:.repo.name})'
[
  {
    "type": "CreateEvent",
    "reponame": "Dmitriy-Podanev/Dependency-Injection"
  },
  ...
]
The syntax basically describes a new JSON object of the form {<key>: <filter>, ...} where <key> is the name of the key to appear in the output and <filter> is any valid jq expression. By using the map operator we limit the results we get displayed to the data that we are really interested in. Personally, I use this often when I have lots of elements that I want to compare to each other. For example, what is the payload structure for all events of type PushEvent?

3) Filter By Specific Value
Limiting the result set by applying a filter helps in navigating through a large data set. To filter with jq we can make use of the select(boolean_expression) function, which takes an expression as argument that needs to return True for elements that should be kept. As an example, let’s try to determine the number of commits that happened in each push event, so first we need to apply the filter and then extract the relevant information.

# first, apply the filter to select all elements that have the `type` property equal to `PushEvent`
$ cat events.json | jq '.[] | select(.type=="PushEvent")'

# then limit the output to the event type and the numbrer of commits
$ cat events.json | jq '.[] | select(.type=="PushEvent") | {type:.type, commits:(.payload.commits|length)}'
Keep in mind that the select does not change the data structure, it merely filters out elements. You may then pipe the filter results to any other jq experssion to continue processing. Note that the expression uses two equal signs == as comparison operator - using just one equal sign will not produce an error as it is a plain assignment, so it will not filter your data.

4) Extracting All JSON Paths
Getting all the JSON paths that are available in the data can give you a head start in understanding what data is available across all elements. Lucky, jq has a built-in paths() function to do exactly that. The paths function turns a JSON document into a representation of all the paths available, so for example we would get [0, 'repo', 'name'] for the repo.name property of the first element.

Without further ado, let’s dive into how to extract all the keys:

# first, in case the root element is an object and not an array, turn it into an array (so future commands work)
$ cat events.json | jq 'select(objects)|=[.]'

# get all paths to all scalar attributes (i.e. the leaf nodes of the JSON tree structure)
$ cat events.json | jq 'select(objects)|=[.] | map( paths(scalars) )'

# as we're not interested in array element indices, let's replace all numeric path elements with `[]`
$ cat events.json | jq 'select(objects)|=[.] | map( paths(scalars) ) | map( map(select(numbers)="[]"))'

# finally, join the paths to a single string and find all unique values
$ cat events.json | jq 'select(objects)|=[.] | map( paths(scalars) ) | map( map(select(numbers)="[]") | join(".")) | unique'
[
  "created_at",
  "id",
  "payload.action",
  "payload.before",
  "payload.commits.[].author.email",
  "payload.commits.[].author.name",
  # ...
The output gives a nice overview of all the keys available in the given data set. The format of the keys is easy to process also for follow-up commands, for example to grep if a key containing commit is available.

5) Deep Text Search
When complex data structures are in place with lots of elements available it becomes increasingly complex to find elements with a certain textual match on the CLI. Traditionally, one would use grep or sed, however the tools are unaware of the hierarchical structure and even if they have a match, it is very hard to trace back the element the match belongs to. We can leverage jq to deeply traverse the data and report the keys that match a specific text along with their respective keys. Let’s look at this example to search for merge in the GitHub events API response:

# first store a reference to the complete data set - we'll need this later 
$ cat events.json | jq '. as $data | .'

# now with `..` traverse the whole tree applying the path() function to retrieve the location 
$ cat events.json | jq '. as $data | [path(..)]'

# we want to select only paths that are scalars (i.e. leaf nodes) and that match the regexp "merge"
$ cat events.json | jq '. as $data | [path(..| select(scalars and (tostring | test("merge", "ixn")))) ]'

# now that we have all the paths with matches, lets map them to an object with the key being a string representation of the key
$ cat events.json | jq '. as $data | [path(..| select(scalars and (tostring | test("merge", "ixn")))) ] | map({ (.|join(".")): "static" })'

# using the getpath function we can pop in the original value at the path (i.e. the scalar containing the match)
$ cat events.json | jq '. as $data | [path(..| select(scalars and (tostring | test("merge", "ixn")))) ] | map({ (.|join(".")): (. as $path | .=$data | getpath($path)) })'

# finally reduce all key-value matches to a single object
$ cat events.json | jq '. as $data | [path(..| select(scalars and (tostring | test("merge", "ixn")))) ] | map({ (.|join(".")): (. as $path | .=$data | getpath($path)) }) | reduce .[] as $item ({}; . * $item)'
Now if we execute the query on our sample GitHub API event data we can see a result similar as follows, with each key being the precise location of the match and the value being the match itself:

$ cat events.json | jq '. as $data | [path(..| select(scalars and (tostring | test("merge", "ixn")))) ] | map({ (.|join(".")): (. as $path | .=$data | getpath($path)) }) | reduce .[] as $item ({}; . * $item)'
{
  "3.payload.pull_request.body": "Bumps [rollup](https://github.com/rollup/rollup) from 2.6.1 to 2.12.1.\n<details>.....",
  "3.payload.pull_request.head.repo.merges_url": "https://api.github.com/repos/riklewis/purifycss/merges",
  "3.payload.pull_request.base.repo.merges_url": "https://api.github.com/repos/riklewis/purifycss/merges",
  "8.payload.pull_request.body": "Bumps [gatsby](https://github.com/gatsbyjs/gatsby) from 2.21.33 to 2.22.17.\n<details>.....",
  "8.payload.pull_request.head.repo.merges_url": "https://api.github.com/repos/n6g7/redux-saga-firebase/merges",
  "8.payload.pull_request.base.repo.merges_url": "https://api.github.com/repos/n6g7/redux-saga-firebase/merges",
  "20.payload.pull_request.head.repo.merges_url": "https://api.github.com/repos/donaldwasserman/demo-outlook-addin/merges",
  "20.payload.pull_request.base.repo.merges_url": "https://api.github.com/repos/donaldwasserman/demo-outlook-addin/merges"
}
In our example, two pull request bodies contained the word merge, as well as obviously the merges_url property. Depending on what you are looking for, the search can quickly point you to the right spot where the data is in the JSON file.

Conclusion
This blog post has shown some basic and advanced jq commands to explore and thrive with JSON on the command line. jq is very powerful and a reliable companion as soon as there is the first bit of JSON data on the CLI. What jq commands do you find useful?