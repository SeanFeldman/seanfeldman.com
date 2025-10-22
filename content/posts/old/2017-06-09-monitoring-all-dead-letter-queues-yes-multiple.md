---
title: Monitoring all Dead Letter Queues. Yes, multiple.
slug: monitoring-all-dead-letter-queues-yes-multiple
date: '2017-06-09T02:49:00'
updated: '2017-06-11T03:01:54.202244+00:00'
draft: false
tags:
- ASB
author: Sean Feldman
---
[![enter image description here][1]][2]
In my previous post [The secret brotherhood of the message counts](http://bit.ly/msgbrotherhood) I talked about sub-queues any Azure Service Bus queue has. For a `queue` those where:
1. `queue/$DeadLetterQueue`
2. `queue/$Transfer`
3. and `queue/$Transfer/$DeadLetterQueue`
In this post, I'm going to focus on the importance of monitoring TDLQ (Transfer DLQ).
## Great success: the message was not delivered.
Imagine the following scenario:
![scenario][3]
A proess is handling a message from `source` queue. During processing, several messages are created and dispatched to various destinations `dest-a`, `dest-b`, and `dest-c`. With transaction and send-via it all works just great. This is what it looks like before message is processed and after:
\*\*\*before\*\*\*
Messages in queue `source`: 1
Messages in queue `dest-a`: 0
Messages in queue `dest-b`: 0
Messages in queue `dest-c`: 0
\*\*\*after\*\*\*
Messages in queue `source`: 0
Messages in queue `dest-a`: 1
Messages in queue `dest-b`: 1
Messages in queue `dest-c`: 1
Now imagine for a second that one of the destination queues is piling up messages that are not dequeued frequently. For the sake of example, let it be `dest-b`. Messages will build up until the point where the queue will reach its maximum size. What will happen then?
\*\*\*before\*\*\*
Messages in queue `source`: 1
Messages in queue `dest-a`: 0
Messages in queue `dest-b`: 0
Messages in queue `dest-c`: 0
\*\*\*after\*\*\*
Messages in queue `source`: 0
Messages in queue `dest-a`: 1
Messages in queue `dest-b`: \*\*0\*\*
Messages in queue `dest-c`: 1
Wait a second. What just happened here? No exceptions, no errors, but the message is not delivered?
## Guaranteed delivery. Not guaranteed destination.
No need to panic. The messages for the destination queues are staged during the transaction and are kept on the broker. They are transferred to the destination queue by the broker. If the broker cannot deliver a message to its destination, it will not fail. Rather it will safely move the message to the send-via queues' TDLQ. By doing so, Azure Service Bus ensures that even if the destination is not capable of receiving the message at the moment, the message won't be lost. Instead, it will be safely stored in TDLQ. And since TDLQ can be accessed, it can be monitored and operated on. Therefore message can be actioned if needed.
To simulate this scenario, one queue `dest-b` could be simply disabled. The result of our scenario would be the following:
![tdlq-ed message][4]
## Are you insane?! Do I need to check TDLQ for every transaction?
No. I am not saying that. You do not need (and even should not) check TDLQ after each and every transaction completion. What you \_should\_ do is have a process in place [to monitor](https://weblogs.asp.net/sfeldman/centralized-dead-letter-queue-with-azure-service-bus) your TDLQs by ops and alert if something is there. Just like you would monitor for the regular DLQs. Remember, this is an \*edge case\*, not a norm. But just because it's rare, doesn't mean it won't happen.
[1]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2017/monitoring-all-dead-letter-queues-yes-multiple/00.transaction.header.jpg
[2]: https://weblogs.asp.net/sfeldman/monitoring-all-dead-letter-queues-yes-multiple
[3]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2017/monitoring-all-dead-letter-queues-yes-multiple/00.transaction.logical.PNG
[4]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2017/monitoring-all-dead-letter-queues-yes-multiple/01.transaction.tdlq.PNG
