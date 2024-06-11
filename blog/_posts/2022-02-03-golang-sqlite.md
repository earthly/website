---
title: "Golang SQLite `database/sql`"
toc: true
author: Adam
sidebar:
  nav: "activity-tracker"
internal-links:
 - sqlite
 - sqlite3
 - sqlite-utils
 - "database/sql"
excerpt: |
    Learn how to use Golang's `database/sql` package to work with SQLite databases. This tutorial covers topics such as installing SQLite, creating a database schema, populating the database, inserting and retrieving data, and more. If you're interested in learning how to persist data using SQLite in Golang, this article is for you.
last_modified_at: 2023-09-19
categories:
  - golang
---
**This article explains how to integrate SQLite with Golang. Earthly simplifies the automation and containerization of Golang SQLite builds. [Learn more about Earthly](https://cloud.earthly.dev/login).**

<!-- markdownlint-disable MD036 -->
Welcome back. I'm an experienced developer, learning Golang by building an activity tracker. Last time I made a [command-line client](/blog/golang-command-line/) to connect to the [JSON Service](/blog/golang-http/), but today is all about database persistence using `database/sql`.

**If you're curious about the basics of storing persistent data into a SQL database using Golang, this tutorial will be helpful for you.** I'm going to be using `sqlite3`, but I'll add lots of headings, so you can skip ahead if `sqlite` is not your thing.

My plan is to add SQLite persistence to [the backend service](https://github.com/earthly/cloud-services-example) so that my workouts aren't lost if the service goes down. And once I have that, I'll add the `--list` command to my command line client and add an end point for it. it's the type of feature that is simple to do with a SQL backend.

## Install SQLite

The first thing I need is to set up my dev environment. I need to install SQLite3 and SQLite-utils:

<div class="narrow-code">

~~~{.bash caption=">_"}
 brew install sqlite3
 brew install sqlite-utils
 ~~~

</div>

 <figcaption>I'm on Mac OS, but you can find these in your package manager of choice.</figcaption>

<div class="notice--info">

### Fun Tool: `sqlite-utils`

`sqlite-utils` is a handy tool for working with SQLite databases at the command line. It makes it simple to query for results or insert records from your terminal.

In particular `sqlite-utils` is good at is creating a database schema based on a CSV or JSON schema. So if I start up the service and get a sample JSON doc:

~~~{.bash caption=">_"}
> curl -X GET -s localhost:8080 -d '{"id": 1}' | jq '.activity'
{
  "time": "2021-12-09T16:34:04Z",
  "description": "bike class",
  "id": 1
}
~~~

Then I can use `sqlite-utils` to create a database and table based on this JSON document's structure:

~~~{.bash caption=">_"}
$ curl -X GET -s localhost:8080 -d '{"id": 1}' | \
 jq '.activity'  | \
 sqlite-utils insert activities.db activities  - 
~~~

That gives me a good starting point for creating my table – I can never remember the `CREATE TABLE` syntax – and I can use `sqlite-utils` to return the schema it created:

~~~{.bash caption=">_"}
> sqlite-utils schema activities.db
~~~

~~~{.sql caption="Output"}
CREATE TABLE [activities] (
   [id] INTEGER
   [time] TEXT,
   [description] TEXT,
);
~~~

I'm going to create this sqlite3 schema manually, but it's helpful to know you can use a tool to create a schema for you.
</div>

## SQLite3 Create Database

SQLite databases are stored in files with the `.db` extension. I can create one with the schema I want using the sqlite3 command line tool like this:

~~~{.bash caption=">_"}
sqlite3 activities.db
~~~

~~~{.sql caption="sqlite3"}
SQLite version 3.32.3 2020-06-18 14:16:19
Enter ".help" for usage hints.
sqlite> sqlite> CREATE TABLE [activities] (
   ...> id INTEGER NOT NULL PRIMARY KEY,
   ...> time DATETIME NOT NULL,
   ...> description TEXT
   ...> );
~~~

<div class="notice--info">

### SQLite, Data Types, and `database/sql`

You may notice that I'm storing time as `DATETIME` whereas sqlite-utils suggested `TEXT` for that column. SQLite is an amazing database but it has an unusual stance on types: it doesn't [really care](https://www.sqlite.org/datatype3.html) about static types. Richard Hipp, the creator, doesn't even like the term static types. He prefers to call them rigid types ( which he thinks are often [a mistake](https://www.sqlite.org/flextypegood.html).[^1])

Because of this stance, there is no statically verified `TIME` or `DATETIME` type in SQLite. Only `INTEGER`, `REAL`, `TEXT`, and `BLOB`. If you set the type as `DATETIME`, you can insert anything you want into it because it's stored as TEXT on disk:

~~~{.sql caption="sqlite3"}
sqlite> insert into activities values 
 ...> (NULL,"not a date","christmas eve bike class");
sqlite> select * from activities;
1|not a date|bike class
~~~

Why then am I using `DATETIME`? Well, It's helpful to document the type of the field, and also, I'm going to be using `database/sql` in my service, and its scan function may use the column types when converting row values.

</div>

## Populating the SQLite Database

I'm going to add some sample data to the database.

~~~{.sql caption="sqlite3"}
sqlite> insert into activities values 
(NULL,"2021-12-09T16:34:04Z","christmas eve bike class");
sqlite> insert into activities values 
(NULL,"2021-12-09T16:56:12Z","cross country skiing is horrible and cold");
sqlite> insert into activities values 
(NULL,"2021-12-09T16:56:23Z","sledding with nephew");
~~~

I can see the data like this:

~~~{.sql caption="sqlite3"}
sqlite> select * from activities;
1|2021-12-09T16:34:04Z|christmas eve bike class
2|2021-12-09T16:56:12Z|cross country skiing is horrible and cold
3|2021-12-09T16:56:23Z|sledding with nephew
~~~

Commands in `sqlite3` start with a dot `.` so I exit like this:

~~~{.sql caption="sqlite3"}
sqlite> .exit
~~~

By the way, I rarely select data using the sqlite3 client. Instead, I like to use `sqlite-utils` which has a nice table output view:

~~~{.bash caption=">_"}
sqlite-utils activities.db "select * from activities" --table
~~~

~~~{.ini .merge-code}
  id  time                  description
----  --------------------  -----------------------------------------
   1  2021-12-09T16:34:04Z  christmas eve bike class
   2  2021-12-09T16:56:12Z  cross country skiing is horrible and cold
   3  2021-12-09T16:56:23Z  sledding with nephew
~~~

You can also set `.mode box` in your [`.sqliterc`](https://sqlite.org/cli.html#changing_output_formats) to get a nicer output out of `sqlite3`.

`sqlite-utils` also has a dump command, which is helpful if I want a text backup of my database contents to version control.

~~~{.bash caption=">_"}
> sqlite-utils dump activities.db
~~~

~~~{.sql .merge-code}
BEGIN TRANSACTION;
CREATE TABLE [activities] (
id INTEGER NOT NULL PRIMARY KEY,
time TEXT,
description TEXT
);
INSERT INTO "activities" VALUES(1,'2021-12-09T16:34:04Z','christmas eve bike class');
INSERT INTO "activities" VALUES(2,'2021-12-09T16:56:12Z','cross country skiing is horrible and cold');
INSERT INTO "activities" VALUES(3,'2021-12-09T16:56:23Z','sledding with nephew');
COMMIT;
~~~

With my database in place, I can now start in on changes to the service.

## Golang SQLite Setup

To use sqlite3 from Golang, I need a database driver. I'm going to use [`go-sqlite3`](https://github.com/mattn/go-sqlite3) which I can install like this:

~~~{.bash caption=">_"}
go get github.com/mattn/go-sqlite3
~~~

*Installing go-sqlite3 requires `gcc` and `CGO_ENABLED=1`*

Finally, let's jump into the Golang code.

## Golang SQL Repository

Previously `server.Activities` contained a slice of `api.Activity`. Now I'm going to update it to contain a pointer to a `sql.DB`. This will be my database handle. It will be how I store and retrieve the activity records. Here is a diff:

~~~{.diff caption="internal/server/activity.go"}
 type Activities struct {
 mu         sync.Mutex
- activities []api.Activity
+ db *sql.DB
}
~~~

`sql.DB` is not SQLite-specific. It can represent a connection to any relational database with a driver. Let's connect to it.

### Database Connection Open

For this round I'm going to hard code my file path:

~~~{.go caption="internal/server/activity.go"}
const file string = "activities.db"
~~~

I can then initialize my db handle using open:

~~~{.go caption="internal/server/activity.go"}
db, err := sql.Open("sqlite3", file)
~~~

If I run this, I get this helpful error message:

~~~{.bash caption=">_"}
sql: unknown driver "sqlite3" (forgotten import?)
~~~

`database/sql` doesn't know about `github.com/mattn/go-sqlite3` and it's helpfully telling me that I probably need to import it.

~~~{.diff caption="internal/server/activity.go"}
import (
 "database/sql"
 "errors"
 "log"
 "sync"

 api "github.com/earthly/cloud-services-example/activity-log"
+  _ "github.com/mattn/go-sqlite3"
)
~~~

After doing that, things seem to work.

<div class="notice--info">

### `database/sql` Drivers

It seems a bit magical for an import to change execution, but the reason is that `db.Open` looks into a map of drivers (`drivers[driverName]`) for the driver matching `sqlite3`. And `sqlite3` gets in that map via the initialization of `github.com/mattn/go-sqlite3`. Also, the error message told me precisely what to do, which was nice.

</div>

### Initialize Database and Setup Schema

I want my service to bootstrap the database itself if one doesn't exist. After all, one of the nice things about SQLite is how quickly you can create a database. For now, I'm going to initialize things by using a `CREATE TABLE IF NOT EXISTS` statement. This way, I can keep my existing data if I have it, but I can recreate things if I don't.

~~~{.go caption="internal/server/activity.go"}
const create string = `
  CREATE TABLE IF NOT EXISTS activities (
  id INTEGER NOT NULL PRIMARY KEY,
  time DATETIME NOT NULL,
  description TEXT
  );`
~~~

I'll execute that with `db.Exec`, meaning my whole database handle constructor looks like this:

~~~{.go captionb="internal/server/activity.go"}
func NewActivities() (*Activities, error) {
 db, err := sql.Open("sqlite3", file)
 if err != nil {
  return nil, err
 }
 if _, err := db.Exec(create); err != nil {
  return nil, err
 }
 return &Activities{
  db: db,
 }, nil
}
~~~

<figcaption>Initialize the [database](https://github.com/earthly/cloud-services-example/blob/v3-sqlite/activity-log/internal/server/activity.go)</figcaption>

## Golang Insert Into Database

I can now use my `sql.db` handle to insert data and get back the primary-key. The most concise way to do this is using `db.Exec` like this:

~~~{.go captionb="internal/server/activity.go"}
func (c *Activities) Insert(activity api.Activity) (int, error) {
 res, err := c.db.Exec("INSERT INTO activities VALUES(NULL,?,?);", activity.Time, activity.Description)
 if err != nil {
  return 0, err
 }

 var id int64
 if id, err = res.LastInsertId(); err != nil {
  return 0, err
 }
 return int(id), nil
}
~~~

And I can test my insert code with curl:

~~~{.bash caption=">_"}
 curl -X POST -s localhost:8080 -d \    
 '{"activity": {"description": "christmas eve bike class", 
 "time":"2021-12-09T16:34:04Z"}}'
~~~

~~~{.bash .merge-code}
{"id":5}
~~~

A quick check with `sqlite-utils` shows that my results were written to the db:

~~~{.bash caption=">_"}
> sqlite-utils activities.db "select * from activities" --table
~~~

~~~{.texinfo .merge-code}
  id  time                       description
----  -------------------------  -----------------------------------------
   1  2021-12-09 16:34:04+00:00  christmas eve bike class
   2  2021-12-09 16:56:12+00:00  cross country skiing is horrible and cold
   3  2021-12-09 16:56:23+00:00  sledding with nephew
   4  not a date                 christmas eve bike class
   5  2021-12-09 16:34:04+00:00  christmas eve bike class
~~~

## Golang Select Row.Scan

Now that I can insert data into the database, its time to get some data back out.

I can use `sql.DB.query` for my retrieval by id:

~~~{.go captionb="internal/server/activity.go"}
row, err := c.db.Query("SELECT * FROM activities WHERE id=?", id)
if err != nil {
 return nil, err
}
~~~

<figcaption>I can get a single row with `Query`, but there is a better way.</figcaption>

But doing this gives me back `sql.Rows`, a cursor that points to possibly many rows.

Using it, I'll have to handle the possibility of multiple rows coming back — since that is impossible with my primary key based query I'd probably just assume I always get a single row back.

Thankfully, I can use [`sql.QueryRow`](https://github.com/golang/go/blob/2580d0e08d5e9f979b943758d3c49877fb2324cb/src/database/sql/sql.go#L1828), which does just this:

> QueryRow executes a query that is expected to return at most one row.
> QueryRow always returns a non-nil value. Errors are deferred until
> Row's Scan method is called.
> if the query selects no rows, the *Row's Scan will return ErrNoRows.
> Otherwise, the*Row's Scan scans the first selected row and discards
> the rest.

My usage looks like this:

~~~{.go captionb="internal/server/activity.go"}
row := c.db.QueryRow(`
    SELECT id, time, description 
    FROM activities 
    WHERE id=?`, id)
~~~

To convert the database values into my struct `api.Activity` I used `row.Scan` ( or `row.Scan` for multiple rows). It copies columns from the row into the value pointed at by each of its arguments.

With that in place, my full SQL select to struct code looks like this:

~~~{.go captionb="internal/server/activity.go"}
func (c *Activities) Retrieve(id int) (api.Activity, error) {
 log.Printf("Getting %d", id)

 // Query DB row based on ID
row := c.db.QueryRow(`
    SELECT id, time, description 
    FROM activities 
    WHERE id=?`, id)

 // Parse row into Activity struct
 activity := api.Activity{}
 var err error
 if err = row.Scan(&activity.ID, &activity.Time, &activity.Description); 
    err == sql.ErrNoRows {
  log.Printf("Id not found")
  return api.Activity{}, ErrIDNotFound
 }
 return activity, err
}
~~~

<div class="notice--info">

### Understanding Scan

`rows.Scan` has no problem handling cases where the column value is an integer and destination value is also an integer – it just copies the row value into the pointed at destination value.

But how can it convert the string returned by SQLite into a `time.Time`? After all `01/12/2022` means different things depending on whether you expect `DD/MM/YYYY` or `MM/DD/YYY`, and SQLite stores these dates as strings on disk.

It turns out that `Scan` handles more complex types by implementing the scanner interface, which looks like this:

~~~{.go caption="database/sql/sql.go"}
type Scanner interface {
 Scan(src interface{}) error
}
~~~

However, time values come in from the driver as `time.Time` and get mapped to other values using [`convertAssign`](https://github.com/golang/go/blob/master/src/database/sql/convert.go#L219) like this:

~~~{.go caption="database/sql/convert.go"}
case time.Time:
  switch d := dest.(type) {
  case *time.Time:
   *d = s
   return nil
  case *string:
   *d = s.Format(time.RFC3339Nano)
   return nil
  case *[]byte:
   if d == nil {
    return errNilPtr
   }
   *d = []byte(s.Format(time.RFC3339Nano))
   return nil
  case *RawBytes:
   if d == nil {
    return errNilPtr
   }
   *d = s.AppendFormat((*d)[:0], time.RFC3339Nano)
   return nil
  }
~~~

So if SQLite is storing dates and time as strings and `database/sql` is getting them as `time.Time` then where is the conversion taking place? And this does matter – if I import data from another source, I want to make sure it will get converted correctly.

Well, after a little digging into `go-sqlite3` and I found this:

~~~{.go caption="mattn/go-sqlite3/sqlite3.go"}

// SQLiteTimestampFormats is timestamp formats understood by both this module
// and SQLite. The first format in the slice will be used when saving time
// values into the database. When parsing a string from a timestamp or datetime
// column, the formats are tried in order.
var SQLiteTimestampFormats = []string{
 // By default, store timestamps with whatever timezone they come with.
 // When parsed, they will be returned with the same timezone.
 "2006-01-02 15:04:05.999999999-07:00",
 "2006-01-02T15:04:05.999999999-07:00",
 "2006-01-02 15:04:05.999999999",
 "2006-01-02T15:04:05.999999999",
 "2006-01-02 15:04:05",
 "2006-01-02T15:04:05",
 "2006-01-02 15:04",
 "2006-01-02T15:04",
 "2006-01-02",
}
~~~

So, that list of priority order formats drives the conversion process.

As long as my dates strings are in one of these formats, they will get correctly converted when I read them out. And when I'm inserting records, the first format in the list will be used to transform my `time.Time` to a database string.

</div>

## Retrieving Many Rows With `rows.Scan`

Now I can add my `-list` endpoint. It follows a similar pattern as Retrieve (`-get`) but using `db.Query`:

~~~{.go captionb="internal/server/activity.go"}
func (c *Activities) List(offset int) ([]api.Activity, error) {
 rows, err := c.db.Query(
  "SELECT * FROM activities WHERE ID > ? ORDER BY id DESC LIMIT 100", offset)
 if err != nil {
  return nil, err
 }
 defer rows.Close()

 data := []api.Activity{}
 for rows.Next() {
  i := api.Activity{}
  err = rows.Scan(&i.ID, &i.Time, &i.Description)
  if err != nil {
   return nil, err
  }
  data = append(data, i)
 }
 return data, nil
}
~~~

<div class="notice--info">

### Prepared Statements

It takes time for SQLite to parse the strings of SQL I'm sending it. And since the SQL never changes, using prepared statements is a great option to consider.

To do so, I would need to add them to my `Activities` struct and initialize them with the database handle init code.

~~~{.diff caption="internal/server/activity.go"}
type Activities struct {
 db     *sql.DB
 mu     sync.Mutex
+ insert, retrieve, list *sql.Stmt
}

func NewActivities() (*Activities, error) {
 db, err := sql.Open("sqlite3", file)
 if err != nil {
  return nil, err
 }
 if _, err := db.Exec(create); err != nil {
  return nil, err
 }
+ insert, err := db.Prepare("INSERT INTO activities VALUES(NULL,?,?);")
+ if err != nil {
+  return nil, err
+ }
 ...
 return &Activities{
  db:     db,
+  insert: insert,
+  retrieve: retrieve,
+  list: list,
 }, nil

}
~~~

And then I could use these statements to perform any SQL work, saving the parsing:

~~~{.go captionb="internal/server/activity.go"}
 res, err := insStmt.Exec(activity.Time, activity.Description)
 if err != nil {
  return 0, err
 }
~~~

I'd also have to remember to close these statements when my db handle was closed.

This seems like overkill for my activity tracker, so I'll avoid this for now. But I did find [this example](https://github.com/TechEmpower/FrameworkBenchmarks/blob/master/frameworks/Go/echo/src/main.go) helpful for understanding what using prepared statements would look like.

</div>

## Testing List

With that list method threaded through to `/list` I can start pulling out lists of items using curl:

~~~{.bash caption=">_"}
> curl -X GET -s localhost:8080/list -d '{"offset": 1}' | jq .
~~~

~~~{.json .merge-code}
[
  {
    "time": "2022-01-09T16:56:23Z",
    "description": "sledding with nephew",
    "id": 3
  },
  {
    "time": "2022-01-02T16:56:12Z",
    "description": "cross country skiing",
    "id": 2
  }
]
~~~

And then calling it with my command-line client:

~~~{.bash caption=">_"}
go run cmd/client/main.go --list
~~~

~~~{.ini .merge-code}
ID:3    "sledding with nephew" .     2022-01-9
ID:2    "cross country skiing "      2022-01-2
ID:1    "christmas eve bike class"   2021-12-24
~~~

And I can also use [Earthly](https://cloud.earthly.dev/login) to test my CI integration tests:

~~~{.bash caption=">_"}
> earthly -P +test
   +build | --> RUN go build -o build/activityserver cmd/server/main.go
   +build | # github.com/mattn/go-sqlite3
   +build | cgo: exec gcc: exec: "gcc": executable file not found in $PATH
~~~

Oh yeah, the SQLite driver! Our driver needs GCC to build and since our builds are running in a container, for repeatability, we need to add GCC to our build script.[^2]

~~~{.diff caption="Earthfile"}
VERSION 0.6
FROM golang:1.15-alpine3.13
WORKDIR /activityserver

+ # Install gcc compiler
+ RUN apk add build-base

deps:
    COPY go.mod go.sum ./
    RUN go mod download
+   RUN go get github.com/mattn/go-sqlite3
    SAVE ARTIFACT go.mod AS LOCAL go.mod
    SAVE ARTIFACT go.sum AS LOCAL go.sum

build:
    FROM +deps
    COPY . .
    RUN go build -o build/activityserver cmd/server/main.go
    SAVE ARTIFACT build/activityserver /activityserver
 ...
~~~

With these changes, my previously written containerized integration now tests from network request to the filesystem, including creating a new database.

Here it is in GitHub Actions:

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/1200.png --alt {{ Successful build on GitHub Actions }} %}
<figcaption></figcaption>
</div>

Now my activity service has a persistence layer, and I learned quite a bit about how `database/sql`, `sqlite3`, `sqlite-utils` and `github.com/mattn/go-sqlite3` work. Thank you for coming along on the journey with me. I didn't show all the code changes here, but you can find the [diff](https://github.com/earthly/cloud-services-example/commit/9398c7251af9ef3d61a3ac32a5535cb7e71985fb) and the [full code](https://github.com/earthly/cloud-services-example/tree/v3-sqlite) on GitHub.

## What's Next

Next, I'm planning to explore gRPC and protocol buffers, along with considering richer records and reporting options. Also if you're building with Golang, consider giving [Earthly](https://cloud.earthly.dev/login) a whirl for consistent and efficient builds.

And if you want to be notified about the next installment, sign up for the newsletter:

{% include_html cta/embedded-newsletter.html %}

[^1]: [`bbkane_`](https://www.reddit.com/user/bbkane_/) pointed out to me that SQlite now has a [STRICT mode](https://www.sqlite.org/stricttables.html). It doesn't support DateTime so far, but perhaps it one day will.
[^2]: There is a machine translated pure Go SQLITE implementation that saves you from needing GCC, although it is slower and probably less extensively tested. Thanks again `bbkane_`
