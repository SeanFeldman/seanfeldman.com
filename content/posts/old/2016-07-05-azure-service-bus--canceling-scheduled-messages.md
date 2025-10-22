---
title: Azure Service Bus - Canceling Scheduled Messages
slug: azure-service-bus--canceling-scheduled-messages
date: '2016-07-05T20:58:00'
updated: '2017-06-19T14:43:51.595629+00:00'
draft: false
tags:
- AzureServiceBus
author: Sean Feldman
---
When Marty went back to 1955, he had no idea how to make it back. Using Azure Service Bus `BrokeredMessage` property `ScheduledEnqueueTimeUtc` to schedule a message in the future would feel the same when the need to cancel the scheduled message would arise. Congratulations, you've scheduled a message. Sorry, there's no way to call it off until it happens. Gladly, the Doc (read ASB team) has introduced a new feature in the latest 3.3.1 version that allows to schedule a message and cancel it on demand, before becoming visible/available.

Before version 3.3.1 the way to schedule future messages was by updating `BrokeredMessage.ScheduledEnqueueTimeUtc` property, setting it to some date/time in the future.

```
var message = new BrokeredMessage();
message.ScheduledEnqueueTimeUtc = DateTime.UtcNow.AddSeconds(300);
await sender.SendAsync(message).ConfigureAwait(false);
```

The problem with this approach is that whenever a scheduled message needs to be canceled prior to becoming visible, it was not possible. Despite the property `SequenceNumber` being assigned by the broker on the sent `BrokeredMessage` (on the server), any attempt to access its value would result in `InvalidOperationException`. Therefore, any messages scheduled in the future and no longer needed would be "stuck" on the broker until the later time.

With version 3.3.1 `QueueClient` or `TopicClient` can be used to schedule a message and cancel it later.

```
var sequenceNumber = await queueClient.ScheduleMessageAsync(message, DateTimeOffset.UtcNow.AddSeconds(300)).ConfigureAwait(false);
await queueClient.CancelScheduledMessageAsync(sequenceNumber).ConfigureAwait(false);
```

The new API doesn't set the scheduled date/time on the message itself, but rather invokes `ScheduleMessageAsync()` method passing the message in and returning sequence number assigned by the broker right back. This sequence number can be used later to cancel the message at any point in time. Even when scheduled time has not arrived yet. No more messages that sit on the broker if not needed. 

A few things to note:

1. Lower level `MessegeSender` doesn't support this functionality. This makes work with messages of both command and event types more challenging. Hopefully, ASB team will add it.
1. API doesn't allow scheduling or canceling multiple messages.
1. <strike>Sequence number returned by `client.ScheduleMessageAsync()` is not assigned to the `BrokeredMessage.SequenceNumber`. Could be a bug in the client library.</strike> `SequenceNumber` is assigned on the broker and the only way to discoverer it w/o receiving the message was to peek at the queue to see all the messages, which would include those set for delivery in the future. Thanks to John Taubensee from the ASB team for spotting light on this item.

Happy time travelling with your messages!
