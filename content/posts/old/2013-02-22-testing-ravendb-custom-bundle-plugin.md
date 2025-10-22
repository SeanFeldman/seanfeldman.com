---
title: Testing RavenDB Custom Bundle/Plugin
slug: testing-ravendb-custom-bundle-plugin
date: '2013-02-22T18:28:00'
updated: '2013-02-22T18:28:00'
draft: false
tags:
- OSS
- RavenDB
- TDD
author: Sean Feldman
---


RavenDB is amazing. You don’t have to work with it for a long time to get that. What’s even more amazing is the extensibility and testability of it. This post is about the last two.

In my recent work I needed to have versioning of documents with very specific requirements that are not matching RavenDB built in [versioning bundle](http://ravendb.net/docs/server/extending/bundles/versioning). Default versioning bundle would generate revisions of all documents upon any change that occurs to a document. In my scenario, I needed only 1 revision at any given time, and revision should be generated only for the documents that have a Status field and its value is changing to “Published”. Very specific to the business requirement. After poking around, reading [documentation](http://ravendb.net/docs/server/extending/plugins), and bugging people on [user group](https://groups.google.com/forum/?fromgroups=#!topic/ravendb/kAruTZeTuZ4), I learned a few things about testing custom bundle/plugin RavenDB style.

## Testing

If you are doing unit testing, [RavenDB.Tests.Helpers](http://nuget.org/packages/RavenDB.Tests.Helpers) is your friend. Once nuget package is installed, your tests can inherit from *RavenTestBase* class that will wire a new embedded document store for you, optimized for testing, and allowing additional modification needed for testing scenario(s) (#3). For bundle/plugin testing, I needed to register all of my triggers (optionally, you could register one at a time, or all of the triggers found in assembly) in Raven’s configuration. The base class exposes *ModifyConfiguration* for that purpose (#1). In addition to that, RavenDB needs to be told that we are activating our bundle (#4). Logging (#2) was more for me to see what happens with RavenDB while test is running.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_3088503C.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_54DD5A8B.png)

## Custom Triggers

One this that I haven’t seen in documentation, but was helped with at the user group was the attributes needed for each custom trigger. *InheritedExport* and *ExportMetadata* are both needed. BundleName is the name that is registered with Raven’s configuration.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_2F43B75D.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_68C6C754.png)

## Enabling Bundle in RavenDB

In order to get custom bundle to work, it has to be copied into Plugins folder under RavenDB location and database setting has to be updated to let Raven know we want bundle to be activated.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_1C228AB1.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_75C0A765.png)

## Bundle in Action

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_5B140B4C.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_7FA598D0.png)

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_05140975.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_5EB22629.png)

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_23EA7D53.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_2B75ECC0.png)


