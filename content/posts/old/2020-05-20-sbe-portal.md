---
title: Service Bus Explorer in Azure Portal
slug: sbe-portal
date: '2020-05-20T04:05:00'
updated: '2020-05-20T05:43:11.805728'
draft: false
tags:
- AzureServiceBus
author: Sean Feldman
---

![Service Bus Explorer for Azure Portal][1]

If you ever used the Service Bus Explorer (SBE) tool, you can appreciate how handy it is to be able to explore the namespace, inspect individual entities, and perform CRUD operation. It's also extremely handy to be able to perform operations that involve messages. For a long time, the tool was only available for Windows users and there was a long-standing [feature request][2] to make the tool cross-platform. The tool is an open-source project and is entirely driven by the volunteered effort. For a long time, the tool was compensating for what Microsoft didn't provide. And, I must admit, was doing a great job, considering its open-source nature and completely voluntary contributions. Until today.
What has changed today? Today, the Azure portal has officially launched Service Bus Explorer in Azure portal. While the name is very similar, do not confuse the two. This is a very early preview with somewhat basic functionality, but a minimum viable product and is a step in the right direction. A very welcomed and long-anticipated addition. But why is it some important? For a few reasons:
1. It's a Microsoft backed tool with a support guarantee
2. It's a web-based tool right in the portal, meaning can be run anywhere.
3. This tool, similar to Storage Explorer, has a chance to potentially become a standalone tool solving the cross-platform ask.
## How do I access the tool?
Right now the only way to see the tool is to navigate to one of the entities (Queues or Topics section in the Entities section of the Service Bus blade).
![enter image description here][3]
## So what can the tool do now?
### Queues
Queues can be created and deleted
![create queues][4]
It also can be modified. I found it a bit awkward to do that not under 'Service Bus Explorer' section, but rather under 'Properties'.
![update queue][5]
This is probably years of using the other SBE tool is talking 🙂
The next big thing is the message operations. This is where it finally closes the gap. For queues, messages can be sent, received, and peeked.
Sending messages allows quick population of custom/user properties as well as system properties by ticking off 'Expand Advanced Properties'. There you'll find Message ID, Label, To, Reply-To, Correlation ID, Schedule time and TTL.
![send a message][6]
Peeking messages can be done from either the queue or its dead-letter queue.
![peek a message][7]
\*\*Note\*\*: only up-to 32 messages can be peeked at the moment. I hope this restriction will be removed as it's possible to peek more than just 32.
Selecting a single message from the peeked messages list allows closer message inspection, revealing custom headers and broker-set properties.
![message properties][8]
Receiving is always done for a single message. Received message can be either from the queue or its dead-letter queue and is \*\*ALWAYS\*\* performed using `ReceiveAndDelete` mode.
![receive a message][9]
\*\*Note\*\*: only a single message can be received at this point. Hopefully, this will change and it will be possible to control the number of messages to be retrieved.
### Topics
Topics can be created, modified, and deleted in a similar way to the queues. And now, with the SBE for the portal messages can be published to the topics as well.
To publish a message to a topic, there's got to be at least one subscription. Once a subscription is created (see down the post), messages can be posted to the topic. Publishing is identical to the sending a message to a queue.
Peeking and receiving are different though. Whenever messages are picked or received from a topic (which is logically invalid), a subscription is required. And that's because messages should be received and peeked from the subscriptions under the topic, not the topic directly.
![receive a message][10]
### Subscriptions
Subscriptions are entities that belong to the topics. Creation, modification, and management of subscription is done under the topics section.
A subscription creation allows providing all the parameters.
![create a subscription][11]
And under individual subscriptions, there's an option to manage the filters.
### Subscription filters/rules
The 'Overview' section of each subscription entity shows also the list of the filters.
![filters][12]
The `$Default` filter, which is by default created with each subscription, will always be there for each new subscription.
When creating a filter, the SBE allows SQL and [Correlation filters][13], with a nice touch of SQL filter validation.
![create a filter][14]
\*\*Note\*\*: filter action cannot be modified at this point.
Existing filters can be inspected \_and\_ modified.
For Correlation filters, the UI provides a drop-down for the correlation properties and entry fields for the custom header/value pairs.
![correlation filter][15]
While in preview, this is an exciting addition to the portal and a great addition to the Azure Service Bus tooling, which was missing for a long time. I'm looking forward to GA-ing of the SBE as well as additional functionality added over the time. It's not on par with any of the other 3rd party tools. And I date to say it doesn't try to replace those. But it's a heck of help to all the developers that need to perform basic operations on the entities and messages. And this tool is going to receive a warm welcome.
[1]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2020/sbe-portal/sbe.png
[2]: https://github.com/paolosalvatori/ServiceBusExplorer/issues/286
[3]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2020/sbe-portal/entities.png
[4]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2020/sbe-portal/queue-create.png
[5]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2020/sbe-portal/queue-update.png
[6]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2020/sbe-portal/queue-send.png
[7]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2020/sbe-portal/queue-peek.png
[8]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2020/sbe-portal/message-properties.png
[9]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2020/sbe-portal/message-receive.png
[10]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2020/sbe-portal/subscription-receive.png
[11]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2020/sbe-portal/subscription-create.png
[12]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2020/sbe-portal/filters.png
[13]: https://weblogs.asp.net/sfeldman/asb-subs-with-correlation-filters
[14]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2020/sbe-portal/filter-create.png
[15]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2020/sbe-portal/filter-correlation.png
