---
title: Choosing Topology with Azure Service Bus
slug: choosing-topology-with-azure-service-bus
date: '2016-03-28T19:51:03.594281'
updated: '2016-03-28T19:51:03.594281'
draft: false
tags:
- ASB
author: Sean Feldman
---
Last week at the [Calgary .NET usergroup][1] presentation on [Azure Service Bus][2] I was talking about different options the services provides. Along with that, have also noted the quotas and limits subject to tier and usage. There were good questions asked, and one of those question I'd like to highlight here - choosing what topology to use with Azure Service Bus.

When working with ASB, quotas and performance are the a few things to keep in mind when designing your topology. Below, is an example of *a topology*. 

![enter image description here][3]

Publisher(s) have a topic per event in the system. Subscriber(s) subscribe to the topics to receive published events. All is great. But is it? Let's dive into details.

![enter image description here][4]

Assuming we've got an input queue for regular messages (like commands) and subscribe to three distinct events (*EventA*, *EventB*, and *EventC*), we'll end up with four receivers. For a small to a medium size system, this is not that bad. Scaling subscribers out and having receivers with concurrency higher than one brings us beyond four connections to the namespace. And each namespace has a [limit][5] of 1000 connections per namespace when running with the default SBMP protocol. What will happen when some events and subscribers are getting high? The number of receivers will go up, and ASB servers will reject connections. Sadly, this is where the original topology no longer holds true, and a different topology is needed.

Thanks to multiple features of ASB, coming up with a required topology is not an issue. For the sample topology above, a feature of *Auto Forwarding* can be used to solve the issue of multiple receivers. Each subscriber when creating a subscription will need to specify a queue to auto-forward to. 

![enter image description here][6]

An additional benefit we get with this topology is that broker is forwarding natively event messages to the destination queue, decreasing chances of failures when trying to receive messages with multiple subscriptions.

Fantastic! Original topology is improved. We can rest. Or can we? What if we have a critical event in our system that we receive rarely, but when do, need to process it quickly? With the topology we have now, this event can sit behind other (more frequent) events and commands that all are going into the input queue. Back to the topology design :)

Hopefully, this example gives you enough food for thought on topologies. There's not one topology to rule them all. You'll have to find the topology that works for your needs and architecture. And when you do settle on one, keep refining it to adapt to the changes your application/system goes through.

[1]: http://www.meetup.com/Calgary-net-User-Group/events/229063004/
[2]: https://github.com/SeanFeldman/ASB-DotNet-YYC/
[3]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2016/topology-01.png
[4]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2016/topology-02.png
[5]: https://azure.microsoft.com/en-us/documentation/articles/service-bus-quotas/
[6]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2016/topology-03.png
