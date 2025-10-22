---
title: Azure Service Bus SDK - Sending ServiceBusMessage(s)
slug: sb-servicebussender
date: '2020-05-04T05:50:00'
updated: '2021-07-26T23:29:45.981074+00:00'
draft: false
tags:
- AzureServiceBus
- AzureSDK
- .NET
author: Sean Feldman
---
![Azure SDK - Service Bus - ServiceBusSender][1]

<div style="color: #CCCCCC;font-family:  Arial, Helvetica, sans-serif;">
Note: SDK Track 2 is still a preview and subject to API changes.
</div>
<br>

Table of contents

 1. [The future of Azure Service Bus .NET SDK][2]
 2. [ServiceBusClient][3]
 3. ServiceBusSender
 4. [ServiceBusReceiver][4]
 5. [Safe Batching][5]

## What's a message?

Throughout the time, the Azure Service Bus message has changed a lot.

In Track 0, it was a `BrokeredMessage` that included both the data and the disposition operations. One drawback that was found with that implementation was the difference with regards to the disposition operations when it came to the protocol: SBMP vs AMQP.

In Track 1, a message has become just a `Message`. A message was a collection of properties and no disposition methods. All the operations were moved to the entity clients/message receiver to adhere to the single AMQP protocol, which requires disposition operations to be performed on the link used to receive the message.

In Track 2, things are changing again. In the right way, this time. A message is no longer just a message. It has a semantic meaning, describing message intent, a message sent, or a message received. For an outgoing message, `ServiceBusMessage` is the message type. `ServiceBusMessage` includes solely the properties that can be found on an outgoing message. Nothing related to the incoming messages. This separation of concerns will help to differentiate between incoming and outgoing messages as the type is intent revealing.

All the properties found on the `ServiceBusMessage` are identical to the subset of the properties from Track 1 `Message`. Except for two minor yet essential differences.

The two properties that have different types are:

 1. `ScheduledEnqueueTime`
 2. `Body`

Why are these two different? Azure SDK was following the best practices and tasked to optimize the code to take advantage of the latest improvements in .NET space.

### `ScheduledEnqueueTime`

The property represents time and is no longer of type `DataTime` but rather `DateTimeOffset`. `DateTimeOffset` is designed for date and time, plus the offset from UTC.

### `Body`

The property represents the payload and is no longer an array of bytes but rather `ReadOnlyMemory<T>`. Represents a contiguous region of memory which accepts byte array as well.

## Sending a message

To send a message, we need to go through the entry point which is `ServiceBusClient`:

```csharp
await using var client = new ServiceBusClient(connectionString, serviceBusClientOptions);
```
Once the client is obtained, a `ServiceBusSender` can be created. Sender creation is done with the client acting as a factory:

```csharp
var sender = client.CreateSender("queue-or-topic"); // entity needs to exist
```
*Note: `ServiceBusSenderOptions` is optional and currently only useful when sending messages transactionally using Send-Via feature. Will be covered in a later post.*

And sending a message:

```csharp
var message = new ServiceBusMessage(Encoding.UTF8.GetBytes("hello"));
await sender.SendAsync(message, cancellationToken);
```
And here's the excellent news - Track 2 has finally added support for `CancellationToken` with the receive operation (spoiler alert, not only sending operation).

And finally, when the sender is no longer required, it can be disposed:

```csharp
await sender.DisposeAsync();
```
With this, messages can be sent to queues and topics. Next is receiving messages.


[1]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2020/sb-servicebussender/sending.jpg
[2]: https://weblogs.asp.net/sfeldman/the-future-of-asb-dotnet-sdk
[3]: https://weblogs.asp.net/sfeldman/sb-servicebusclient
[4]: https://weblogs.asp.net/sfeldman/sb-servicebusreceiver
[5]: https://weblogs.asp.net/sfeldman/sb-servicebusreceiver/sb-safebatching
