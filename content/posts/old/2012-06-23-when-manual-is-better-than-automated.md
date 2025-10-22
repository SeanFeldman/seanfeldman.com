---
title: Automate or Not
slug: when-manual-is-better-than-automated
date: '2012-06-23T01:30:00'
updated: '2012-06-23T01:30:00'
draft: false
tags:
- Automation
author: Sean Feldman
---


When system is built, no one wants to baby sit after its up and running. Therefore, there is a strong desire to automate everything, including error handling. But sometimes automation is not suitable for every error, and here is a good example.

An email signup service that I have created is using a 3rd party service to discover city, region, and country from city name only.  Easy and intuitive for customers, head ache free to maintain (no need to keep data source up-to-date). All good and nice till I got an error reported by someone on the team – instead of City the system reported “junk” (see screenshot).

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_548BBCBA.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_37D247A5.png)

After debugging a little, it was simply bad data coming back from the 3rd party service (which I have to admit was extremely reliable and accurate for the most part). So what do you do? Initial response in the team was “lets code it so that when a city has a comma and space, we strip it along with the rest. I.e., when “Calgary, Alberta” is received for a city name, we strip the “, Alberta” portion. Sounds like a great idea, can be automated and be done.

But wait a second, there’s also a different issue as well, sometimes system reports Region (aka state / district / province) incorrectly (“AB Alberta” rather than “Alberta”). It is not affecting production right away. So would it be correct to apply the same “fix logic”? At the same time, it could be “City, Regions, Country” returned in a field for City only. Does it make sense to automate the process of fixing the problem (considering that it happens rarely)? Or, perhaps, it’s worth to automate alerts about malformed data, but leave data clean-up to a person?

We have decided to do the minimum required – automate alerts for data that looks odd, and leave fixing to a person that actually deals with subscriptions.


