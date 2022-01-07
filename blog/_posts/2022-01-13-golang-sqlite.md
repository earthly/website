---
title: "Put Your Best Title Here"
categories:
  - Tutorials
toc: true
author: Adam

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

## Draft.dev Article Checklist

- [ ] Add in Author page
- [ ] Create header image in Canva
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
  - Would any images look better `wide` or without the `figcaption`?
- [ ] Run mark down linter (`lint`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `link-opp` and find 1-5 places to incorporate links
- [ ] Add Earthly `CTA` at bottom `{% include cta/cta1.html %}`

## Steps


* Create sqlite db

 brew install sqlite3
 brew install sqlite-utils
 
 # trick for creating table
 we can start the service, make a call to get the jsonL
 ```
 curl -X POST -s localhost:8080 -d \
'{"activity": {"description": "christmas eve bike class", "time":"2021-12-09T16:34:04Z"}}'
 curl -X GET -s localhost:8080 -d '{"id": 1}' 
{"activity":{"time":"2021-12-09T16:34:04Z","description":"christmas eve bike class","id":1}}
 ```
Then we can use `sqlite-utils` to create a database and table based on this JSON document:
```
curl -X GET -s localhost:8080 -d '{"id": 1}' | jq '.activity'  |  sqlite-utils insert activities.db activities  - 
```
After this, sqlite-utils can tell show us the schema it created:
```
sqlite-utils schema activities.db
CREATE TABLE [activities] (
   [id] INTEGER
   [time] TEXT,
   [description] TEXT,
);
```
## real way

Create the database
```
sqlite3 activities.db
SQLite version 3.32.3 2020-06-18 14:16:19
Enter ".help" for usage hints.
sqlite> sqlite> CREATE TABLE [activities] (
   ...> id INTEGER NOT NULL PRIMARY KEY,
   ...> time TEXT,
   ...> description TEXT
   ...> );
```
You may notice that I'm storing TIME as text. SQLite is an amazing database, but Richard made it in TCL originally and it has a somewhat unusual stance on types for a SQL database. That being that it doesn't really care for static types.  There is no static TIME or Date type in sqlite. Only INTEGER / REAL / TEXT and BLOB.

Don't worry it can still has functions that can handle dates and timestamps, they just parse from TEXT on each call.

Insert some data:
//ToDo: need better examples
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
By the way, I rarely actually select data in the sqlite3 client. Instead I like to use `sqlite-utils` which has a nice table output view:
```
sqlite-utils activities.db "select * from activities" --table
  id  time                  description
----  --------------------  -----------------------------------------
   1  2021-12-09T16:34:04Z  christmas eve bike class
   2  2021-12-09T16:56:12Z  cross country skiing is horrible and cold
   3  2021-12-09T16:56:23Z  sledding with nephew
```
We can keep all this in a script like so:
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

## Go SQLite setup

* install driver

//todo: Explain whatever this does
```
go get github.com/mattn/go-sqlite3
go install github.com/mattn/go-sqlite3 -- needed? not sure
```

``` diff
- type Activities struct {
+ type InMemory struct {
	mu         sync.Mutex
	activities []api.Activity
}
```