Mapserv
=======

Mapserv is planned to be a spatial query service. Clients send abstract query
trees encoded as [Thrift](http://incubator.apache.org/thrift/) messages to a
server. The server performs the query, and then sends the results back to the
client.

In principle, the client and server can be implemented however they want. The
current implementation (see "What's Done" notes below) consists of the following
parts:

* A Python server which uses a SQLite backend (with the [R*Tree
  extension](http://www.sqlite.org/rtree.html))
* A Python query DSL, which makes it simple to generate complex abstract query
  messages

The Python/SQLite server is just an experiment to get the service up and
running. This combination was chosen as it was the simplest server to get up and
running. Other possible backends could use the language of your choice (ideally
C++, Java, C#, or something else with good thread support), and any of the
following storage backends:

* [SQLite/R*Tree](http://www.sqlite.org/rtree.html)
* [MySQL/MyISAM](http://dev.mysql.com/doc/refman/5.1/en/spatial-extensions.html)
* [PostgreSQL/PostGIS](http://postgis.refractions.net/)
* A custom spatial index implementation (there are many floating around on the
  net, if you need some inspiration)

What's Done
===========

This project is in a pre-alpha phase. Here's what's currently implemented:

* A prototype of the thrift query spec (see `query.thrift`). This is still
  actively being modified. Note: Some SQLite-isms may have bled through into the
  query spec.
* The Python query DSL is usable (however, `UPDATE` statements have not yet been
  implemented).
* There is no server implementation yet.

Hacking
-------

If you want to hack on this project, it lives on GitHub at
[http://github.com/eklitzke/mapserv](http://github.com/eklitzke/mapserv).

There are some tests in the aptly named `tests` directory. You can run all of
the tests by running `make tests` (although they're run in a sort of strange
way, since each test file is run separately).
