---
title: IIS 7 - Writing Log Files
slug: iis-7-writing-log-files
date: '2011-03-30T01:49:00'
updated: '2011-03-30T01:49:00'
draft: false
tags:
- Other
author: Sean Feldman
---


I have ran into a problem while using [NLog](http://nlog-project.org/) with web application – logs not created when application is deployed to IIS. Everything would indicate that this is permissions issue, except that I couldn’t figure out what account my web application was running under. Under II6 it was simple – IUSR, but with IIS 7 things have changed a little. Then I learned about [Application Pool Identities](http://learn.iis.net/page.aspx/624/application-pool-identities/). Very interesting, especially when locating an account **DefaultAppPool** resolves nothing, but **IIS AppPool\DefaultAppPool** does find **DefaultAppPool**. Either way, once I set write permissions for **DefaultAppPool** on the web application folder controlled by IIS, my problems were solved.

Moral of this story – when working with new things (IIS in this case), make sure you know read the manual. Just “clicking” it might be quite expensive (time wise).


