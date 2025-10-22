---
title: Azure Service Bus Premium - Message Size
slug: azure-service-bus-premium-message-size
date: '2016-04-14T04:57:00'
updated: '2016-04-14T21:48:30.947857+00:00'
draft: false
tags:
- ASB
author: Sean Feldman
---
Messaging is about small messages. You should keep your messages relatively small. If you have fat messages, you're doing it wrong. All valid statements, until you look closer at the [Azure Service Bus Quotas](https://azure.microsoft.com/en-us/documentation/articles/service-bus-quotas/) information. The ones that are sometimes hard to digest would be:

1. Message size for a queue/topic/subscription entity - 256KB
2. Maximum header size - 64KB

It means up to 192KB for the payload. For the most scenarios, 192KB is a lot of data for a payload. If your message is slightly over that size, you're out of luck and will have to look into implementing a claim check pattern. Unfortunately, that mean the message is handled by more than a single service (Azure Service Bus and Azure Storage). Till recently that was the only option. Facing size limit, this is where you might reconsider Azure Service Bus Standard tier and trade your old ride for a new one: Premium Tier.

[Premium tier](https://azure.microsoft.com/en-us/documentation/articles/service-bus-premium-messaging/) was added to handle addresses scale, performance, and availability. Now it can also handle messages large than 1MB. To be more specific, up to 1MB (according to the tests I've done).

   
```csharp
var namespaceManager = NamespaceManager.CreateFromConnectionString(connectionString);
```
	var queueName = "test";
	if (!await namespaceManager.QueueExistsAsync(queueName))
	{
		await namespaceManager.CreateQueueAsync(queueName);
		Console.WriteLine("Queue created");
	}
	else
	{
		Console.WriteLine("Queue existed");
	}
	var factory = await MessagingFactory.CreateAsync(namespaceManager.Address, namespaceManager.Settings.TokenProvider);
	var sender = await factory.CreateMessageSenderAsync(queueName);

```csharp
// send a payload of 512KB
```
	var msg1 = new BrokeredMessage(new string('A', 512 * 1024));
	msg1.TimeToLive = TimeSpan.FromMinutes(2);

	Console.WriteLine("Sending batch");
	await sender.SendAsync(msg1);

![enter image description here][1]

**Note**: the maximum size I've managed to send was 1,013KB

![enter image description here][2]


[1]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2016/1MB-02.png
[2]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2016/1MB-03.png
