---
title: Centralized Dead Letter Queue with Azure Service Bus
slug: centralized-dead-letter-queue-with-azure-service-bus
date: '2016-06-25T08:47:50.708465+00:00'
updated: '2016-06-25T08:47:50.677193+00:00'
draft: false
tags:
- AzureServiceBus
author: Sean Feldman
---
Azure Service Bus provides a robust Dead Letter mechanism. Each queue (or subscription) has its dead letter queue (DLQ).
![enter image description here][1]
Messages ending up in DLQs are not necessarily poisonous, and potentially could be resolved by re-processing. That means DLQs should be monitored to allow dead lettered messages to be analyzed and re-processed if needed. The issue with this approach is monitoring and troubleshooting.
When a number of queues is significant, monitoring becomes a real headache.
When a message is moved to its DLQ, it's obvious what queue did it fail. But what about centralized DLQ? If dead lettered messages from various queues are moved into a centralized DLQ, knowing message origin is important to send it back for reprocessing.
Gladly, the recent version of ASB has added an additional standard property on the `BrokeredMessage` called [`DeadLetterSource`](https://msdn.microsoft.com/en-us/library/microsoft.servicebus.messaging.brokeredmessage.deadlettersource.aspx). When a dead lettered message is forwarded to another queue, it's stamped with the source queue name.
Below is an example of a `test` queue that has DLQed messages forwarded to a centralized `error` queue. Assuming we're sending a message that fails the maximum number of deliveries to the `test` queue.
![enter image description here][2]
The message will be DLQed and automatically moved by the broker to the `error` queue.
![enter image description here][3]
Now message can be inspected and failed source queue retrieved.
![enter image description here][4]
In case of subscriptions, `DeadLetterSource` works exactly the same way. I've set up a topic called `events` with a subscription called `sub`. Dead lettered messages on the subscription are forwarded to the centralized error queue `error`.
![enter image description here][5]
Once a message on `sub` fails more than allowed delivery count, it's moved to the error queue which was specified as a queue to forward to on dead lettering. Inspection of the forwarded message shows the following:
![enter image description here][6]
Happy centralized error handling!
[1]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2016/deadletterqueue/dlq-per-queue.png
[2]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2016/deadletterqueue/message-in-queue.png
[3]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2016/deadletterqueue/forwarded-message.png
[4]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2016/deadletterqueue/source-on-message.png
[5]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2016/deadletterqueue/subscription.png
[6]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2016/deadletterqueue/deadlettersource-event.png
