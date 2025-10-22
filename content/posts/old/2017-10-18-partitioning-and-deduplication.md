---
title: Partitioning and de-duplication
slug: partitioning-and-deduplication
date: '2017-10-18T03:19:00'
updated: '2017-10-18T03:39:49.070476+00:00'
draft: false
tags:
- AzureServiceBus
author: Sean Feldman
---
Recently, I've received a comment on an older post about [message de-duplication](https://weblogs.asp.net/sfeldman/bend-message-deduplication-on-azure-service-bus-to-your-will) that was somewhat peculiar. 

> An important note here - watch out for partitioning. I basically ran the same code, but de-duping did not work and I couldn't understand why. Turns out that because I created the queue manually through the portal with partitioning enabled, and it screwed up the de-duping.

To recap, here's what we have:

 - A queue is created with native de-duplication enabled.
 - It's partitioned.
 - A message with a calculated `MessageId` is sent to the queue.
 - A message duplicate with the same `MessageId` is sent to the queue.
 - Expected behavior: duplicate to be detected and removed
 - Actual behavior: the message and its duplicate are found on the queue.

This makes no sense, right? Indeed it doesn't.

You know how the instinct to blame something "obvious" kicks in first? The portal is already <strike>horrible</strike> not the best. It would be easy to blame it for another issue and move on. And that's exactly what I did at first. Except it feels wrong to cast blame on something that might not be at fault and make a scapegoat of it.

So let's assume it's _not_ the tool's fault and review the basics of the Azure Service Bus.

## [Duplication Message Detection][1]

> Enabling duplicate detection helps keep track of the application-controlled `MessageId` of all messages sent into a queue or topic during a specified time window. If any new message is sent carrying a `MessageId` that has already been logged during the time window, the message is reported as accepted (the send operation succeeds), but the newly sent message is instantly ignored and dropped. No other parts of the message other than the `MessageId` are considered.

Simple and clear. As long as message IDs are repeated within a specfied time window, the broker will discard the later received copies.

## [Partitioned Entities][2]

> Each partitioned queue or topic consists of multiple fragments. Each fragment is stored in a different messaging store and handled by a different message broker. 

This is the important part: each fragment is handled by a **different broker**.

> When a message is sent to a partitioned queue or topic, Service Bus assigns the message to one of the fragments. The selection is done randomly by Service Bus or by using a partition key that the sender can specify.

A partition key can be influenced by `SessionId`, `PartitionId, or `MessageId`.

>  If the queue or topic has the `QueueDescription.RequiresDuplicateDetection` property set to true and the `BrokeredMessage.SessionId` or `BrokeredMessage.PartitionKey` properties are not set, then the **`BrokeredMessage.MessageId` property serves as the partition key**. (Note that the Microsoft .NET and AMQP libraries automatically assign a message ID if the sending application does not.) In this case, **all copies of the same message are handled by the same message broker**. This enables Service Bus to detect and eliminate duplicate messages. If the `QueueDescription.RequiresDuplicateDetection` property is not set to true, Service Bus does not consider the MessageId property as a partition key.

This is important! To get messages de-duplicated properly when sent to a partitioned entity, a message ID is used to calculate the partition key. The documentation also clearly states that the .NET Framework client is **by default** setting the message ID.

What that means for the Azure Service Bus full framework client is that even without specifying the message ID, it will be assigned by the client. And since there's no partition key specified, the message ID (randomly assigned by the client) will be used to derive the partition key value. I.e. message IDs will be different. Therefore partition keys will be different. As a result, messages will be sent to different fragments, resulting in duplicates. 

<center>
![ASB][3]
<br/>(Service Bus Architecture diagram, source: [Microsoft docs][4])
</center>

**Moral of the story**: always assign a message ID that is deterministic for all the duplicates.

But that's not everything. At least not all the possible ways to mess things up.

In case a partition key is specified, it will be used **as-is** to determine the fragment to send messages to. Which will, again, result in messages going to different fragment and from there we know duplicates will be unavoidable.

**Moral of the story**: do not specify different partition keys for messages that can be duplicates.

And with the new kid on the block, Azure Service Bus .NET Standard client, the behavior should be identical. Except it's not. It's better. The new client does not mandate message ID to be assigned. Whenever a message without a message ID or a partition key is attempted to be sent to a partitioned entity that has duplicate detection turned on, an exception is thrown.

> Batching brokered messages with distinct SessionId, PartitionKey, or MessageId  is not supported for an entity with partitioning and duplicate detection enabled. 

Beside the obviously confusing error message which is a [broker minor issue][5], this is a much better outcome then just to have a partition key being assigned from some random message ID. 1:0 in favor of the new Azure Service Bus client!


[1]: https://docs.microsoft.com/en-us/azure/service-bus-messaging/duplicate-detection
[2]: https://docs.microsoft.com/en-us/azure/service-bus-messaging/service-bus-partitioning
[3]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2017/partitioning-and-de-duplication/asb.architecture.png
[4]: https://docs.microsoft.com/en-us/azure/service-bus-messaging/service-bus-architecture
[5]: https://github.com/Azure/azure-service-bus/issues/103
