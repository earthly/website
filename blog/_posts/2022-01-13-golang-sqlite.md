---
title: "Golang SQLite `database/sql`"
categories:
  - Tutorials
toc: true
author: Adam
sidebar:
  nav: "activity-tracker"
internal-links:
 - sqlite
 - sqlite3
 - sqlite-utils
---
**Writing Article Checklist**

- [ ] Fix Grammarly Errors
- [ ] Read out loud
- [ ] First two paragraphs: What's it about? Why listen to you?
- [ ] Run mark down linter (`lint`)
- [ ] Raise PR

Welcome back. I'm an experienced developer, learning Golang by building an activity tracker. Last time I built a [command line client](/blog/golang-command-line/) to connect to the [Json Service](/blog/golang-http/) but today is all about database persistence using `database/sql`.

**If you curious about the basics of storing persistent data into a SQL database using Golang, this tutorial will be helpful for you.** I'm going to be using `sqlite3` and I'll add lots of heading for ease of skimming.

My goal for today is to add a SQLite backend to [the service](https://github.com/adamgordonbell/cloudservices) so that my workouts aren't lost if the service goes down. And once I have that in I will be able to add the `--list` command, which I skipped before – it's the type of feature that is really simple to do with SQL backend.

## Install SQLite

This first thing I need is to setup my dev environment. I need to install SQLite3 and SQLite-utils 

``` bash
 brew install sqlite3
 brew install sqlite-utils
 ```
 <figcaption>I'm on Mac OS, but you can find these in your package manager of choice.</figcaption>

<div class="notice--info">

**ℹ️ Fun Tool: sqlite-utils**

`sqlite-utils` is a handy tool for working with sqlite databases at the command line. It makes it simple to query for results or insert records from your terminal. 

One thing in particular `sqlite-utils` is good at is creating a database schema based on a CSV or JSON schema. So if I start up the service and get a sample JSON doc:

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

I'm to this sqlite3 schema creation manually below, but its helpful to know you can have a tool create a schema for you.
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

You may notice that I'm storing time as `DATETIME` whereas sqlite-utils suggested `TEXT` for that column. SQLite is an amazing database but it has an unusual stance on types: it doesn't [really care](https://www.sqlite.org/datatype3.html) about static types. In fact, Richard Hipp, the creator doesn't even like the term static types, he prefers rigid types, which he thinks are often [a mistake](https://www.sqlite.org/flextypegood.html).[^1]

Because of this stance, there is no statically verified `TIME` or `DATETIME` type in SQLite. Only `INTEGER`, `REAL`, `TEXT`, and `BLOB`. If you set the type as `DATETIME`, it is still stored as `TEXT` on disk and you can insert anything into it:

```
sqlite> insert into activities values 
 ...> (NULL,"not a date","christmas eve bike class");
sqlite> select * from activities;
1|not a date|bike class
```

Why then am I using `DATETIME`? Well, It's because I'm going to be using `database/sql` in my service and it uses the column types to infer the type of conversions that are valid. In other words, I need it to be `DATETIME` so that I can convert it into a `time.Time` when we jump into our Golang service.

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

To use sqlite3 from Golang, I need a database driver. I'm going to use [`go-sqlite3`](https://github.com/mattn/go-sqlite3) which I can install like this:

```
go get github.com/mattn/go-sqlite3
```

*Installing go-sqlite3 requires `gcc` and `CGO_ENABLED=1`, both of which we ready to go on my macbook. However, I will have to make some changes to the CI process to ensure a c compiler is present.*

Finally, let's jump into the GoLang code.

## Golang SQL Repository

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

### Database Connection Open

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

After doing that, things seem to work. 

<div class="notice--info">

**ℹ️ `database/sql` drivers**

It seems a little bit magical for an import to change execution but the reason is that `db.Open` looks into a map of drivers (`drivers[driverName]`) for the driver matching `sqlite3` and the initialization of `github.com/mattn/go-sqlite3` calls `sql.Register` and adds itself to that driver map. Also, the error message told me exactly what to do, which was nice.

</div>

### Initialize Database and Setup Schema

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

<figcaption>Initialize the db like this (code is on github)</figcaption>

## Golang Insert into Database

I can now use my `sql.db` handle to insert data and get back primary key. The most concise way to do this is using `db.Exec` like this:

~~~{.go caption="internal/server/activity.go"}
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

//todo: make these examples better and consistent across the tutorial
```
 curl -X POST -s localhost:8080 -d \    
 '{"activity": {"description": "christmas eve bike class", "time":"2021-12-09T16:34:04Z"}}'
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

Now that I can insert data into the database, its time to get some data back out. 

I can use db.query for my retrieval by id.

~~~{.go caption="internal/server/activity.go"}
row, err := c.db.Query("SELECT * FROM activities WHERE id=?", id)
if err != nil {
	return nil, err
}
~~~
<figcaption>I can get a single row with `Query` but there is a better way.</figcaption>

But doing this gives me back `sql.Rows`, a cursor that points to one to n rows. Using it I'll have to handle the possibility of multiple rows coming back — since that is impossible with my primary key based query I'd probably just assume I always get a single row back.

Thankfully, I can use `sql.QueryRow` which does just this:

> QueryRow executes a query that is expected to return at most one row.
> QueryRow always returns a non-nil value. Errors are deferred until
> Row's Scan method is called.
> if the query selects no rows, the *Row's Scan will return ErrNoRows.
> Otherwise, the *Row's Scan scans the first selected row and discards
> the rest.

My usage looks like this:

~~~{.go caption="internal/server/activity.go"}
	row := c.db.QueryRow("SELECT id, time, description FROM activities WHERE id=?", id)
~~~

To convert the database values into my struct `api.Activity` I used `row.Scan` ( or `row.Scan` for multiple rows). It copies columns from the row into the value pointed at by each of its arguments.

With that in place, my full sql select to struct code looks like this:

~~~{.go caption="internal/server/activity.go"}
func (c *Activities) Retrieve(id int) (api.Activity, error) {
	log.Printf("Getting %d", id)

	// Query DB row based on ID
	row := c.db.QueryRow("SELECT id, time, description FROM activities WHERE id=?", id)

	// Parse row into Activity struct
	activity := api.Activity{}
	var err error
	if err = row.Scan(&activity.ID, &activity.Time, &activity.Description); err == sql.ErrNoRows {
		log.Printf("Id not found")
		return api.Activity{}, ErrIDNotFound
	}
	return activity, err
}
~~~

<div class="notice--info">

**ℹ️ Understanding Scan**

`rows.Scan` has no problem handling cases where the column value is an integer and destination value is also an integer – it just copies the row value into the pointed at destination value.

But how can it convert the string returned by sqlite into a `time.Time`? After all 01/12/2022 means different things depending whether you expect `DD/MM/YYYY` or `MM/DD/YYY` and sqlite is actually storing this dates as strings on disk. It turns out that it handles more complex types by implementing the scanner interface, which looks like this:

```
```

The `time.Time` scan implementation of this looks this:

~~~{.go caption="database/sql/sql.go"}

type NullTime struct {
	Time  time.Time
	Valid bool // Valid is true if Time is not NULL
}
func (n *NullTime) Scan(value interface{}) error {
	if value == nil {
		n.Time, n.Valid = time.Time{}, false
		return nil
	}
	n.Valid = true
	return convertAssign(&n.Time, value)
}

~~~
And the relevant part of `convertAssign` looks like this:

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

In other words, `database/sql` is expecting any strings that are dates to be formatted like this: `2006-01-02T15:04:05.999999999Z07:00` and it's up to our sqlite driver `github.com/mattn/go-sqlite3` to get that string into the correct format.

`go-sqlite3` does this by keeping a list of datetime formats to try:

~~~{.go caption="mattn/go-sqlite3/sqlite3.go"}

// SQLiteTimestampFormats is timestamp formats understood by both this module
// and SQLite.  The first format in the slice will be used when saving time
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

So, as long as my dates strings are in one of these formats, everything will work correctly on retreival. And when inserting the first format in the list will be used to convert the other way.

</div>




```
da code
```



## Golang SQL row.Scan

Then I do the mapping:
```

```
, and things can go badly like this


<div class="notice--info">

**ℹ️ Prepared statements**

It takes time for SQLite to parse the strings of SQL I'm sending it. And since the sql never changes using prepared statements is a great option to consider.

To do so I would need to add them to my `Activities` struct and initialize them with the database handle init code.

~~~{.diff caption="internal/server/activity.go"}

type Activities struct {
	db     *sql.DB
	mu     sync.Mutex
+	insert, retrieve, list *sql.Stmt
}

func NewActivities() (*Activities, error) {
	db, err := sql.Open("sqlite3", file)
	if err != nil {
		return nil, err
	}
	if _, err := db.Exec(create); err != nil {
		return nil, err
	}
+	insert, err := db.Prepare("INSERT INTO activities VALUES(NULL,?,?);")
+	if err != nil {
+		return nil, err
+	}
	...
	return &Activities{
		db:     db,
+		insert: insert,
+		retrieve: retrieve,
+		list: list,
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

### What's Next

My current plan is to ... After that, I'm thinking about adding other features, but I'll keep those to myself for now.

If you want to be notified about the next installment, sign up for the newsletter:

{% include cta/embedded-newsletter.html %}



[^1]:
  I disagree with Richard on this but he is a more talented engineer than me, so I suspect he has some strong reasoning behind his stance.