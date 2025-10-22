---
title: Azure Service Bus SDK - Receiving ServiceBusReceivedMessage(s)
slug: sb-servicebusreceiver
date: '2020-05-11T05:28:30.470579'
updated: '2020-05-11T05:28:30.298718+00:00'
draft: false
tags:
- AzureServiceBus
- AzureSDK
- .NET
author: Sean Feldman
---
![Azure SDK - Service Bus - ServiceBusReceiver][1]

<div style="color: #CCCCCC;font-family:  Arial, Helvetica, sans-serif;">
Note: SDK Track 2 is still a preview and subject to API changes.
</div>
<br>

Table of contents

 1. [The future of Azure Service Bus .NET SDK][2]
 2. [ServiceBusClient][3]
 3. [ServiceBusSender][4]
 4. ServiceBusReceiver
 5. [Safe Batching][5]

## Sent message vs received message

Not all messages are born equal. A message sent starts its life on the client-side and has fewer attributes than a message that is received. Why is that? Well, a message that is sent has not been on the server-side. It hasn't been received and "leased". And as a result of that, it has no values for `SequenceNumber`, `DeliveryCount`, `LockToken`/`LockedUntil`, `DeadLetterReason` or any other value that would be set on the broker. But historically, that was not the case. Both, Track 0 and Track 1 took an approach of a canonical message that represented both messages, sent and received. With Track 2 that's changing. Message sent from the client-side, `ServiceBusMessage` is not the type received. Received messages are of the type `ServiceBusReceivedMessage`. It's an "extension" of the `ServiceBusMessage`, containing all the additional information broker (server-side) would set.

This change, while it is a small change, is designed to enforce cleaner code and separation of concerns when dealing with two types of messages (outgoing and incoming). At the moment of writing this post, it is impossible to create a `ServiceBusReceivedMessage`. It will be possible to create it for testing purposes, using a static factory for **testing** purposes. I also suspect there will be some way to create a copy/clone with modifications when the support for the incoming pipeline will be in place. Yet that is not implemented yet and will be a future post topic. For now, you can track the progress on the topic in the issue [here][6].

## Receiving a message

So, assuming there are messages waiting to be received, how to receive those?

As always, we need a Service Bus client to create a receiver. The receiver can also take an optional options parameter, used to specify receive mode and custom prefetch count.

```csharp
await using var client = new ServiceBusClient(connectionString, options);
var receiveOptions = new ServiceBusReceiverOptions
{
	PrefetchCount = 0,
	ReceiveMode = ReceiveMode.PeekLock
};
await using var receiver = client.CreateReceiver("myqueue", receiveOptions);
```
Once we've got the receiver, we can request a single message or multiple messages

```csharp
ServiceBusReceivedMessage message = await receiver.ReceiveAsync(cancellationToken);
IList<ServiceBusReceivedMessage> messages = await receiver.ReceiveBatchAsync(maxMessages, cancellationToken);
```
Note that `ReceiveBatchAsync()` method implies there's a batch received, in reality it's a best-effort operation to retrieve up-to `maxMessages` requested and not exactly that number of messages.

And another great addition in Track 2 is support for `CancellationToken` by all vital methods.

Now we can send and receive using Azure Service Bus future SDK. Exciting!

In the next post, I'll be looking at the feature that has almost made it to the Track 1 SDK and is finally here - safe batching. Until then, happy coding.

[1]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2020/sb-servicebusreceiver/receiving.jpg
[2]: https://weblogs.asp.net/sfeldman/the-future-of-asb-dotnet-sdk
[3]: https://weblogs.asp.net/sfeldman/sb-servicebusclient
[4]: https://weblogs.asp.net/sfeldman/sb-servicebussender
[5]: https://weblogs.asp.net/sfeldman/sb-servicebusreceiver/sb-safebatching
[6]: https://github.com/Azure/azure-sdk-for-net/issues/11986
