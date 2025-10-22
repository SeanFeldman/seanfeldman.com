---
title: HttpListener and IIS to Listen to HTTPS Traffic Connections Simultaneously
slug: httplistener-and-iis-to-listen-to-https-traffic-connections-simultaneously
date: '2010-01-09T18:27:00'
updated: '2010-01-09T18:27:00'
draft: false
tags:
- .NET
author: Sean Feldman
---


HttpListener provided with .NET version 2.0 and up allow to build a custom HTTP server based application without need to have IIS installed on machine. This can be handy in some scenarios, where IIS cannot fit it. HttpListener can handle normal HTTP traffic, as well as HTTPS (secure). Once details that is hard to find online, is the fact that there’s a conflict between IIS and HttpListener to listen simultaneously to port 443 despite **different** prefixes being used. After digging for a while, the answer was found. Apparently, Windows 2003 is coming with IIS 6.0 and Windows XP comes with IIS 5.1. That little details does the difference (underlying implementation in HTTP.SYS looks like).

Hopefully this saves time to those that ran into case.


