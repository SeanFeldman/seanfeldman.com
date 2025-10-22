---
title: The secret brotherhood of the message counts
slug: the-secret-brotherhood-of-message-counts
date: '2017-04-04T19:10:00'
updated: '2017-06-09T03:04:29.570663+00:00'
draft: false
tags:
- AzureServiceBus
author: Sean Feldman
---
[![Shhhh][1]][2]

When working with Azure Service Bus, message count is expected to report how many messages are found in the queue. Only if life was that simple. In the real world, things a bit more complicated. 

Let's assume there's a queue, named `queue` which receives messages. Whenever a message fails to be processed more than `MaxDeliveryCount` times, it is assumed to be a poisonous message and is moved to what's called a dead-letter queue (or simply DLQ). Here's a first not-so-secret member of the brotherhood. DLQ path for `queue` would be expressed as `queue/$DeadLetterQueue`. ASB client has a convenience API ([`client.FormatDeadLetterPath(path)`][3]) to get the name of the DLQ for any given queue.

When a message is sent using [SendVia feature][4] or a message is [auto-forwarded][5] between entities, ASB is using an additional queue called Transfer queue, utilized behind the scenes. Its value highly depends on the throughput a queue is experiencing at any given moment.

![enter image description here][6]

This queue has a <strike>name</strike> path: `queue/$Transfer`.

So so far, for _any_ queue, there are actually 3 queues:

 1. `queue`
 2. `queue/$DeadLetterQueue`
 3. `queue/$Transfer`

Wait. There's more. Whenever a message going through the Transfer queue is failing, it is moved to the Transfer DLQ. It _is_ a queue that can be accessed . Messages found in the Transfer DLQ are all the messages that have failed to be transfered. Its path is always `queue/$Transfer/$DeadLetterQueue`. There's a [convenience method][7] to construct the Transfer DLQ queue name as well.

So by now, we've discovered that there's are four queues for any given queue:

 1. `queue`
 2. `queue/$DeadLetterQueue`
 3. `queue/$Transfer`
 4. `queue/$Transfer/$DeadLetterQueue`

With this information, ASB\`s `MessageCountDetails` makes more sense. Looking at the portal, the numbers start to make sense as well.

![enter image description here][8]

In this case, there are:

  - 2 messages ready to be processed in the `queue` (1) 
  - 998 messages scheduled for the future (can be peeked but not received) (1a)
  - No DLQed messages
  - No messages being transferred at the moment
  - 11,735 message that didn't make the transfer, rest their soul in peace

Together, these counts can tell a story of what happened to the messages in a queue. It also can reveal more secrets about messages that vanished into the Transfer DLQ. On that in the [follow-up post][9].


[1]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2017/queue-brotherhood/secret.jpeg
[2]: https://weblogs.asp.net/sfeldman/the-secret-brotherhood-of-message-counts
[3]: https://docs.microsoft.com/en-us/dotnet/api/microsoft.servicebus.messaging.queueclient
[4]: https://docs.microsoft.com/en-us/azure/service-bus-messaging/service-bus-transactions#transfers-and-send-via
[5]: https://docs.microsoft.com/en-us/azure/service-bus-messaging/service-bus-auto-forwarding
[6]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2017/queue-brotherhood/MessageCount.gif
[7]: https://docs.microsoft.com/en-us/azure/service-bus-messaging/service-bus-dead-letter-queues#dead-lettering-in-forwardto-or-sendvia-scenarios
[8]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2017/queue-brotherhood/portal.png
[9]: https://weblogs.asp.net/sfeldman/monitoring-all-dead-letter-queues-yes-multiple
