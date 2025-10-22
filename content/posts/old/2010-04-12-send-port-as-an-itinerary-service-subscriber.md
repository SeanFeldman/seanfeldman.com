---
title: Send Port as an Itinerary Service Subscriber
slug: send-port-as-an-itinerary-service-subscriber
date: '2010-04-12T18:15:00'
updated: '2010-04-12T18:15:00'
draft: false
tags:
- ESB
author: Sean Feldman
---


In order for a send port to subscribe, it has to filter messages dynamically, based on several Itinerary schema properties (as described in documentation). Properties and values are:

* IsRequestResponse = False
* ServiceName = *Some\_Service\_Name*
* ServiceState = Pending
* ServiceType = Messaging

Filtering is done on promoted property from Microsoft.Practices.ESB application. In order to use those promoted properties, first Microsoft.Practices.ESB application should be referenced. Basic knowledge for an experienced BizTalk developer, but wheel spinning time for someone new.


