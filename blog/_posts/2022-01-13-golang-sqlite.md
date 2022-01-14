---
title: "SQLite and GoLang"
categories:
  - Tutorials
toc: true
author: Adam
sidebar:
  nav: "activity-tracker"
internal-links:
 - just an example
---
### Writing Article Checklist

- [ ] Write Outline
- [ ] Write Draft
- [ ] Fix Grammarly Errors
- [ ] Read out loud
- [ ] Write 5 or more titles and pick the best on
- [ ] First two paragraphs: What's it about? Why listen to you?
- [ ] Create header image in Canva
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
- [ ] Run mark down linter (`lint`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `link-opp` and find 1-5 places to incorporate links to other articles
- [ ] Add Earthly `CTA` at bottom `{% include cta/cta1.html %}`
- [ ] Raise PR

Welcome back. I'm an experienced developer, learning golang by building an activity tracker. Last time I built a [command line client]() to connect to the [Json Service]() but today is all about database persistence.

My goal for today is to add a SQLite backend to the service so that my work outs aren't lost if the service goes down. And once I have that in I will be able to add the `--list` command, which I skipped before – it's the type of feature that works is really simple to do with SQL.

## Steps

## Install SQLite

My first step is to install SQLite and SQLite-utils. 

``` bash
 brew install sqlite3
 brew install sqlite-utils
 ```
 <figcaption>I'm on Mac OS, but you can find these in your package manager of choice.</figcaption>

<div class="notice--info">

**ℹ️ Fun Tool: sqlite-utils**

`sqlite-utils` is a handy tool for working with sqlite databases at the command line. It makes it simple to query for results or insert records from your terminal. 

One thing in particular its good at is creating a database schema based on a CSV or JSON schema. So if I start up the service and get a sample JSON doc:

```
> curl -X GET -s localhost:8080 -d '{"id": 1}' | jq '.activity'
{
  "time": "2021-12-09T16:34:04Z",
  "description": "bike class",
  "id": 1
}
```

Then I can use `sqlite-utils` to create a database and table based on this JSON document's structure:

```
$ curl -X GET -s localhost:8080 -d '{"id": 1}' | \
 jq '.activity'  | \
 sqlite-utils insert activities.db activities  - 
```

That gives me a good starting point for creating my table – I can never remember the `CREATE TABLE` syntax – and then I can use `sqlite-utils` again to return the schema it created:

```
sqlite-utils schema activities.db
CREATE TABLE [activities] (
   [id] INTEGER
   [time] TEXT,
   [description] TEXT,
);
```

I'm going to show the way to create a schema manually sqlite3 below, but its helpful to know you can have a tool create the schema for you.
</div>

## SQLite3 Create Database

SQLite databases are stored in files with the `.db` extension. I can create one with the schema I want using the sqlite3 command line tool like this:

```
sqlite3 activities.db
SQLite version 3.32.3 2020-06-18 14:16:19
Enter ".help" for usage hints.
sqlite> sqlite> CREATE TABLE [activities] (
   ...> id INTEGER NOT NULL PRIMARY KEY,
   ...> time DATETIME NOT NULL,
   ...> description TEXT
   ...> );
```

<div class="notice--info">

**ℹ️ SQLite, Data Types, and `database/sql`**

You may notice that I'm storing time as `DATETIME` whereas sqlite-utils suggested `TEXT` for that column. In SQLite, there are reasons to prefer one over the other, depending upon the case. SQLite is an amazing database but it has an unusual stance on types: it doesn't [really care](https://www.sqlite.org/datatype3.html) about static types. In fact, Richard Hipp, the creator doesn't even like the term static types, he prefers rigid types, which he thinks are often [a mistake](https://www.sqlite.org/flextypegood.html).[^1]

Because of this stance, there is no staticly verified `TIME` or `DATETIME` type in SQLite. Only `INTEGER`, `REAL`, `TEXT`, and `BLOB`. If you set the type as `DATETIME`, it is still stored as `TEXT` on disk and you can insert anything into it:

```
sqlite> insert into activities values 
 ...> (NULL,"not a date","christmas eve bike class");
sqlite> select * from activities;
1|not a date|bike class
```

Why then am I using `DATETIME`? Well, It's because I'm going to be using `database/sql` in my service and it uses the column types to infer the type of conversions that are valid. In other words, I need it to be `DATETIME` so that I can convert it into a `time.Time` when we jump into our GoLang service.

</div>

## Populating the SQLite Database

I'm going to add some sample data in the database.
```
sqlite> insert into activities values (NULL,"2021-12-09T16:34:04Z","christmas eve bike class");
sqlite> insert into activities values (NULL,"2021-12-09T16:56:12Z","cross country skiing is horrible and cold");
sqlite> insert into activities values (NULL,"2021-12-09T16:56:23Z","sledding with nephew");
```

I can see the data like this:

```
sqlite> select * from activities;
1|2021-12-09T16:34:04Z|christmas eve bike class
2|2021-12-09T16:56:12Z|cross country skiing is horrible and cold
3|2021-12-09T16:56:23Z|sledding with nephew
```

Commands in `sqlite3` start with a dot `.` so I exit like this:

```
sqlite> .exit
```

By the way, I rarely actually select data using the sqlite3 client. Instead I like to use `sqlite-utils` which has a nice table output view:

```
sqlite-utils activities.db "select * from activities" --table
  id  time                  description
----  --------------------  -----------------------------------------
   1  2021-12-09T16:34:04Z  christmas eve bike class
   2  2021-12-09T16:56:12Z  cross country skiing is horrible and cold
   3  2021-12-09T16:56:23Z  sledding with nephew
```
It also has a dump command, which is helpful if I want a text backup of my database contents to version control.
```
sqlite-utils dump activities.db > data.sql
```

```
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

```

With my database in place, I can now start in on changes to the service.

## GoLang SQLite Setup

To use sqlite3 from golang, I need a database driver. I'm going to use [`go-sqlite3`](https://github.com/mattn/go-sqlite3) which I can install like this:

```
go get github.com/mattn/go-sqlite3
```

*Installing go-sqlite3 requires `gcc` and `CGO_ENABLED=1`, both of which we ready to go on my macbook. However, I will have to make some changes to the CI process to ensure a c compiler is present.*

## GoLang SQL Example Repository

Previously `server.Activities` contained a slice of `api.Activity`. Now I'm going to update it to contain a pointer to a `sql.DB`. This will be my database handle. That is it will be how I store and retrieve the activity records. Here is a diff:

//todo: adjust colors

~~~{.diff caption="internal/server/activity.go"}
 type Activities struct {
	mu         sync.Mutex
-	activities []api.Activity
+	db *sql.DB
}
~~~

`sql.DB` is not sqlite specific. It is can represent a connection to any relational database with a driver. Let's connect to it. 

For this round I'm going to hard code my file path:

~~~
const file string = "activities.db"
~~~

I can then initialize my db handle using open:

```
db, err := sql.Open("sqlite3", file)
```

If I run this, I get this helpful error message:

```
sql: unknown driver "sqlite3" (forgotten import?)

```

`database/sql` doesn't know about `github.com/mattn/go-sqlite3` and it's helpfully telling me that I probably need to import it. 



~~~{.diff caption="internal/server/activity.go"}
import (
	"database/sql"
	"errors"
	"log"
	"sync"

	api "github.com/adamgordonbell/cloudservices/activity-log"
+	 _ "github.com/mattn/go-sqlite3"
)
~~~

After doing that, things seem to work. It seems a little bit magical for an import to change execution but the reason is that `db.Open` looks into a map of drivers (`drivers[driverName]`) for the driver matching `sqlite3` and the initialization of `github.com/mattn/go-sqlite3` calls `sql.Register` and adds itself to that driver map. Also, the error message told me exactly what to do, which was nice.

### Create Table 

I'd like my service to be able to bootstrap the database itself if one doesn't exist. After all once of the nice things about sqlite is how quickly a database can be created. For now, I'm going to initialize things by using a `CREATE TABLE IF NOT EXISTS` statement. This way I can keep my existing data if I have it, but if I don't I'll start from scratch. 

~~~{.go caption="internal/server/activity.go"}
const create string = `
		CREATE TABLE IF NOT EXISTS activities (
		id INTEGER NOT NULL PRIMARY KEY,
		time DATETIME NOT NULL,
		description TEXT
		);`
~~~

I'll execute that with `db.Exec`, meaning my whole database handle constructor looks like this:

~~~{.go caption="internal/server/activity.go"}
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
<figcaption>Intialize the db like this (code is here)</figcaption>

## Golang Insert bla

I can now use my `sql.db` handle to insert data and get back primary key. The most concise way to do this is using `db.Exec` like this:
```
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
```

//ToDo: is this even a good idea? The prepared statment is thrown away

However, it does take time for SQLite to parse the insert string when sent this way. It probably doesn't matter for this case, since the number of inserts I'm doing is pretty low, but I'm going to use a prepared statement for insert.

Doing so means first preparing a statement `insStmt`, like this:
```
insStmt, err := c.db.Prepare("INSERT INTO activities VALUES(NULL,?,?);")
	if err != nil {
		return 0, err
	}
	defer insStmt.Close()
```

And then using it to execute my insert:

```
res, err := insStmt.Exec(activity.Time, activity.Description)
	if err != nil {
		return 0, err
	}
```
The whole thing, slightly simplified looks like this:
```
func (c *Activities) Insert(activity api.Activity) (int, error) {
	insStmt, err := c.db.Prepare("INSERT INTO activities VALUES(NULL,?,?);")
	if err != nil {
		return 0, err
	}
	defer insStmt.Close()

	res, err := insStmt.Exec(activity.Time, activity.Description)
	if err != nil {
		return 0, err
	}

	var id int64
	if id, err = res.LastInsertId(); err != nil {
		return 0, err
	}
	return int(id), nil
}
```

And I can test it with curl:

## Prepared statements

//todo: make these examples better and consistent across the tutorial
```
 curl -X POST -s localhost:8080 -d \    '{"activity": {"description": "christmas eve bike class", "time":"2021-12-09T16:34:04Z"}}'
{"id":5}
```
And I can see that it's ending up in the db:
```
sqlite-utils activities.db "select * from activities" --table
  id  time                       description
----  -------------------------  -----------------------------------------
   1  2021-12-09 16:34:04+00:00  christmas eve bike class
   2  2021-12-09 16:56:12+00:00  cross country skiing is horrible and cold
   3  2021-12-09 16:56:23+00:00  sledding with nephew
   4  not a date                 christmas eve bike class
   5  2021-12-09 16:34:04+00:00  christmas eve bike class
```


## Golang Select Row.Scan
Now that I can insert, its time for retrieve. 

I could use db.query for my retrieval by id.

```
da code
```
To do so I would need to check the row count returned and handle the specific case of getting zero rows back.

```
da code
```

Instead I can use  db.QueryRow:
```
	row := c.db.QueryRow("SELECT * FROM activities WHERE id=?", id)
```

## GoLang SQL row.Scan

Then I do the mapping:
```

```
, and things can go badly like this





[^1]:
  I disagree with Richard on this but he is a more talented engineer than me, so I suspect he has some strong reasoning behind his stance.