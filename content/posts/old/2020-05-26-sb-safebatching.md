---
title: Azure Service Bus SDK - Safe Batching
slug: sb-safebatching
date: '2020-05-26T03:38:00'
updated: '2020-05-26T04:12:05.247218+00:00'
draft: false
tags:
- AzureServiceBus
- AzureSDK
- .NET
author: Sean Feldman
---
![Azure SDK - Service Bus - Safe Batching][1]

<div style="color: #CCCCCC;font-family:  Arial, Helvetica, sans-serif;">
Note: SDK Track 2 is still a preview and subject to API changes.
</div>
<br>

Table of contents

 1. [The future of Azure Service Bus .NET SDK][2]
 2. [ServiceBusClient][3]
 3. [ServiceBusSender][4]
 4. [ServiceBusReceiver][5]
 5. Safe Batching

## Unsafe batching

In one of the previous posts, [Sending ServiceBusMessage(s)][6] I've mentioned the option to send a single message using `SendAsync()` API. Sometimes, sending a single message is not enough and multiple messages need to be sent. The same method provides an overload to send a collection of messages.

```
IEnumerable<ServiceBusMessage> messages = new 
List<messages>{ ... };
await sender.SendAsync(messages, cancellationToken);
```

This method is great when messages are pre-created and sent in a single operation. It's subject to a single message size restriction but other than that, it's straight forward. Except it's not.

Consider the following scenario: you've created multiple messages and about to send those, but as you do so, `MessageSizeExceededException` exception is thrown. Why is that? That's due to the fact that each message is smaller than the maximum message size. But combined together, multiple messages can exceed that limit and there's no way to validate the total size until an attempt to send those to the broker is made. And that's far from optimal. This is especially problematic when handling a continuous stream of data that needs to be converted to messages and sent out. How to know how messages would be within the right size boundaries? What if there's an outlier causing an assumed batch size to be invalidated?

In the past, for track 0 SDK, I've dealt with that by [estimating the batch size][7] and used padding percentage. While it worked, it wasn't very accurate and it's the biggest drawback was high inaccuracy with small messages. But hey, it worked well for the closed source SDK.

For track 1 SDK, this was no longer required as safe batching could be implemented in the SDK code.
I've started working on the [PR to add the feature](https://github.com/Azure/azure-service-bus-dotnet/pull/539) to the SDK and it was almost there, except things didn't go as I was hoping they'd go.

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Current status: building <a href="https://twitter.com/hashtag/Azure?src=hash&amp;ref_src=twsrc%5Etfw">#Azure</a> <a href="https://twitter.com/hashtag/servicebus?src=hash&amp;ref_src=twsrc%5Etfw">#servicebus</a> safe batching API for <a href="https://twitter.com/hashtag/azureservicebus?src=hash&amp;ref_src=twsrc%5Etfw">#azureservicebus</a> <a href="https://twitter.com/hashtag/netstandard?src=hash&amp;ref_src=twsrc%5Etfw">#netstandard</a> client. No more surprises at run-time. <a href="https://t.co/2kHD5mapSR">pic.twitter.com/2kHD5mapSR</a></p>&mdash; Sean Feldman (@sfeldman) <a href="https://twitter.com/sfeldman/status/1024902379475324928?ref_src=twsrc%5Etfw">August 2, 2018</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

Nonetheless, the idea was straight forward - build up a batch of messages in a controlled manner by converting those message to AMQP messages and counting their size towards total batch size.

![safe batching track 1][8]

## Safe batching

Wait, is that all to it? Yes. That's all. And the good news, track 2 SDK already has it. Let's have a look at the API.

First step is to create a sender. A sender is necessary not only to dispatch a batch of messages, but also to create the batch.

```
await using var client = new ServiceBusClient(connectionString, options);
await using var sender = client.CreateSender("myqueue");
```

The next step is to define batch creation options. Currently it only supports `MaxSizeInBytes`, which is necessary if you'd like to control the batch maximum size. If omitted, the maximum message size for the namespace tier/SKU will be used.

```
var batchOptions = new CreateBatchOptions
{
	MaxSizeInBytes = 100
};
```

With the options and sender, we can create a batch

```
using var batch = await sender.CreateBatchAsync(batchOptions, cancellationToken);
```

Note that `ServiceBusMessageBatch` is `IDisposable` and should be disposed of after used up.

Adding messages to the batch is done in a controlled manner, using `TryAdd(message)` method. Try-add is a well-established pattern to attempt an operation and indicate wherever it succeeded or not without a failure. The operation adds the message and returns `true` if the message's addition does not surpass the maximum batch size. Otherwise, `false` is returned and the message is not added to the batch, leaving it for the next batch. E.g.:
```
batch.TryAdd(message1);
batch.TryAdd(message2);
batch.TryAdd(message3);
```

`ServiceBusMessageBatch` also exposes the following properties to query it's size:

 1. Count - number of messages in a batch
 2. SizeInBytes - batch total size
 3. MaxSizeInBytes - maximum allowed batch size

And last but not the least, sending the batch

```
await sender.SendAsync(batch, cancellationToken);
```

## Conclusion

This small but extremely powerful feature solves the problem of unexpected surprises when trying to send a collection of messages to the broker. By using safe batching API, there's no more gambling wherever the send operation will succeed or fail.

[1]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2020/sb-safebatching/batch.jpg
[2]: https://weblogs.asp.net/sfeldman/the-future-of-asb-dotnet-sdk
[3]: https://weblogs.asp.net/sfeldman/sb-servicebusclient
[4]: https://weblogs.asp.net/sfeldman/sb-servicebussender
[5]: https://weblogs.asp.net/sfeldman/sb-servicebusreceiver
[6]: https://weblogs.asp.net/sfeldman/sb-servicebussender
[7]: https://weblogs.asp.net/sfeldman/asb-batching-brokered-messages
[8]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2020/sb-safebatching/code.png
