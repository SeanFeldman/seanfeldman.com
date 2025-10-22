---
title: Reporting with NHibernate?…
slug: reporting-with-nhibernate
date: '2010-02-25T07:51:00'
updated: '2010-02-25T07:51:00'
draft: false
tags:
- NHibernate
author: Sean Feldman
---


About over a year+ we had a little application that was leveraging NHibernate for a simple domain. Along all the requirements, one was to generate a pre-defined report with a few simple filters on it. Initial thought was to leverage the same domain we’ve worked out and build report based on that. It was obviously not the best solution there, but once we got the profiling, it was obviously the worse one we could come up with. Re-hydrating entities for reporting was a little bit of a waste. So what would be an alternative without re-investing a lot? We ended up re-using same NHibernate, but in a slightly different manner.

NHibernate has an option to execute raw SQL queries, option exposed through *ISession.CreateSQLQuery(sql\_statement)*. The returned *ISQLQuery* object exposes functionality *SetResultTransformer(IResultTransformer)* that can be used to (quoting NHibernate documentation) “”change” the shape of query result”. Let’s look into it.

To start-off, we’ll define our Report Data transformer, based on the ReportDataDto

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_22F5BEB6.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_40D442B7.png)

This DTO is going to present what the report has to show – post ID, post title, and first 50 characters for a post body as a preview, followed by ellipsis. ERD derived from the domain entities is a bit more reach with attributes, and has association, which for the given report we intentionally want to remove.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_4B2A8879.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_423AF63A.png)

Also, we want to have a meaningful name for body preview in the DTO, and that will be an alias change, that we’ll have to capture in result transformer.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_32BD05CD.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_185A8205.png)

(*IReportDataDtoTransformer* is extending NHibernate’s *IResultTransformer*)

At this point we are done with "“changing” the shape of results". All we need is to get the results. This is a sample only, therefore query will be embedded within the code, where normally it would be externalized with or without parameters, depends on requirements.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_43C65512.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_02298815.png)

Execution of this query is literally execution of the SELECT statement defined in SQL statement. No entities are created, but simple dumb DTOs. No state management, no overheads, plain data in objects form for reporting purpose.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_50C2C5D4.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_5368F0D4.png)

This is definitely one of the ways to accomplish the task, and not the only. It is not suitable for complex and dynamic report, but efficient and quick for static ones. Our new college, Dragosh, has proposed to look into read-only NHibernate session and leverage LINQ 2 NHibernate to accomplish the same result, but using entities. I haven’t looked into that, but definitely worth experimenting.


