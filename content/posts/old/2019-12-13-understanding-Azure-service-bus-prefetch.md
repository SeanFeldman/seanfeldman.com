---
title: Understanding Azure Service Bus Prefetch
slug: understanding-Azure-service-bus-prefetch
date: '2019-12-13T21:13:00'
updated: '2019-12-13T13:13:56.050358+00:00'
draft: false
tags:
- AzureServiceBus
author: Sean Feldman
---
Working with a remote broker can be a challenge at times. The latency caused by the roundtrip to the broker to fetch a single message can exceed the processing time of that message. To help with this problem, Azure Service Bus (ASB) offers a prefetching option to retrieve messages before they are requested. This option is available with all three clients capable of retrieving messages: `MessageReceiver`, `QueueClient`, and `SubscriptionClient`. When a message is requested, and this option is turned on, the ASB client retrieves more messages. The additional messages are kept in a memory buffer until the user code requests the next message. Except for this time, the client will not fetch it from the broker but rather from the in-memory buffer. That beats the latency and improves the overall throughput of the application or the system performing message processing.

Prefetch is configured on the client-side. For .NET SDK that is specified by providing the PrefetchCount to one of the clients, as mentioned earlier. Note that the exact number of prefetched messages is not always the same as the requested number. If the broker has fewer messages to pass, it will not wait for the requested number of messages to materialize on the broker to be prefetched. It will send whatever is available.

Prefetch feature reduces the average latency per message and drives the throughput up, but it is not enabled by default. And there’s a good reason why by default prefetch is set to none. Safety.

Let’s have a look at the two modes ASB messages can be processed: `ReceiveAndDelete` and `PeekLock`.

## Prefetch with ReceiveAndDelete mode

With `ReceiveAndDelete` mode, messages are processed in at-most-once mode. When a message is retrieved from the broker to the client, the message is immediately removed from the broker w/o the client’s acknowledgement. And that’s risky. 

What happens to the pre-fetched messages in this mode? If the application crashes, the in-memory buffer is gone. And so are the pre-fetched messages that were still in that buffer. And that’s dangerous. Unless it’s tolerable and acceptable to lose a few messages for the sake of speed. Though you were warned.

## Prefetch with PeekLock mode

Unlike the first mode, PeekLock is a safer mode by default. A message is never deleted from the broker until the client has confirmed its successful processing or has explicitly instructed on a different course of action. Such an action would be explicit dead-lettering, deferral, or cancellation. Though there’s a condition, a message has to be processed and actioned within a pre-defined time known as `MaxLockDuration`. That’s a lease time; each message gets on the broker for a client to get finished with it. When a client takes longer than that time, the lease is no longer respected and the message is given to another client. This pattern is also known as a competing consumer. 

The challenge with the competing consumer pattern combined with ASB’s lease lock is that sometimes message processing can take longer than the duration of the lease. And that has consequences – message processing by multiple competing consumers. 

Why is this a problem? There are a few issues:

 1. When a message cannot be completed within the lease time (`MaxLockDuration`), the work that is performed is unnecessary.
 1. 2.	The additional work would need to be reverted, or some de-duplication would need to take place to ensure the same data is not stored twice, for example.

So, what would be the right approach in this receive mode? A balance. A balance between the number of messages prefetched, max lease time configured, and the longest time it takes to process a single message. And even then, sometimes there are edge cases. Thanks to the brokered message properties, some of those edge cases can be mitigated. Upon arrival on the client-side, each message is “stamped” with a few system properties. One of those properties is `LockedUntilUtc`. Or until when the lease is valid. This property can be used to “gatekeep” from the unnecessary processing of those messages that arrive too late or just before the lease is about to expire and due to processing times will not have a chance to be completed successfully (read w/o LockLostException).

A word of caution, the time for `LockedUntilUtc`, represents the broker time. Clients can be impacted by a clock skew and throw calculations off by a split of a second. Nothing is perfect. 🤷‍♂‍

## Summary

If you’ve never used pre-fetch, check it out. Not only you’ll be equipped with a robust feature, but also improve the throughput and shave those milliseconds off. Log and measure. Use it wisely.
