---
title: cURL to Scrape Data
slug: curl-to-scrape-data
date: '2012-09-20T13:43:00'
updated: '2012-09-20T13:43:00'
draft: false
tags:
- Automation
author: Sean Feldman
---


I ran into a situation today when one of our microsites that was developed by a 3rd party is no longer… manageable. To be less politically correct, we don’t have access to the data anymore. Nothing significant, but annoying. The only way to see the data was through the web site. Yet data was paged, with about 40 pages. This is where curl was really helpful. Apparently, you can [parameterize URLs](http://www.codediesel.com/tools/6-essential-curl-commands/) (thanks to Sameer’s post) passed into the command, as well as the output. Here’s an example:

curl.exe -o **page#1.html** http://dummy.com/show?page=**[1-40****]** 

Where page#1.html will be populated by the current index and index is set from 1 to 40. Awesome trick!


