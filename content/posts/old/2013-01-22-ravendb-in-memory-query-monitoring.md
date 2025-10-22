---
title: RavenDB In Memory Query Monitoring
slug: ravendb-in-memory-query-monitoring
date: '2013-01-22T04:03:00'
updated: '2013-01-22T04:03:00'
draft: false
tags:
- RavenDB
- TDD
author: Sean Feldman
---


RavenDB has a great way to monitor what’s happening between client and server. I found it very helpful when trying to figure out what’s happening, or just understand how things work (such as querying).

When doing unit testing, the pattern is to leverage in-memory store to speed things up. Unfortunately, when that’s the case, there’s exposed communication happening between unit tests (client) and in-memory store (server).

There are a few possible solutions folks have suggested, but one that really made my day was… custom logger. This is a fantastic way to tap into what’s happening and see it all (Thank you [Matt Johnson](https://groups.google.com/d/msg/ravendb/ANEIBix4pTY/smUjE5jk78IJ) for help).

Now there’s no more blindness and magic. Everything is revealed. Happiness.


