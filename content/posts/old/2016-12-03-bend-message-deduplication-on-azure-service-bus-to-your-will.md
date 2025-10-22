---
title: Bend Message Deduplication on Azure Service Bus to Your Will
slug: bend-message-deduplication-on-azure-service-bus-to-your-will
date: '2016-12-03T09:35:00'
updated: '2016-12-04T21:33:10.792433+00:00'
draft: false
tags:
- AzureServiceBus
author: Sean Feldman
---
[![Do not duplicate][1]](https://weblogs.asp.net/sfeldman/bend-message-deduplication-on-azure-service-bus-to-your-will)

Duplicates detection functionality provided by Azure Service Bus can automatically remove duplicate messages sent to a queue or topic. Deduplication is always based on the value of the MessageId property. No other property can participate in deduplication. 

In the real world, message deduplication can often depend on things that are part of the message payload itself. Let's say we process orders*. Deduplication would rather be based on the order ID and not message ID. There are a few creative solutions that allow custom deduplication. For example, perform deduplication outside of ASB broker by manually inspecting message payload and marking it as a duplicate. For example, using Azure Functions and Storage tables\**. While approach like this one works, it has several drawbacks: 

 - Unnecessary intermediate steps
 - Performance decrease
 - No ability to take advantage of highly optimized and performant native deduplication

_What's the solution?_

Use native deduplication!

_Wait, but isn't native deduplication limited to solely message ID?_

Glad you've asked. Absolutely. It is. Though let's look at the `MessageId` property of the `BrokeredMessage`. It's a read/write property, meaning we **can** set it to custom values. 

_Custom value you said?_ 

Let's read a bit more of the ASB documentation on deduplication.

> [To enable duplicate detection, each message has to have a unique MessageId property that by default stays the same no matter how many times the message is read from a queue.](https://docs.microsoft.com/en-us/azure/service-bus-messaging/service-bus-fundamentals-hybrid-solutions)

Solved! To deduplicate order messages on `OrderId`, we'll assign brokered message `MessageId` property the value of `OrderId`. Done. Now order messages will be deduplicated on order IDs\***.

_Hold your horses! What if I need to deduplicate based on several values from a message?_

Same as with order id. Combining all property values and assigning as `MessageId`. Except that there might be a size issue.

Size issue?! Yes. `BrokeredMessage.MessageId` is limited to 128 characters. Would that be a deal breaker if generated ID needs to be more than 128 characters? Not at all. As a matter of fact, the entire payload could be used for deduplication. Here's an example:

```csharp
var payload = serializerOfYourChoice.Serialize(payloadObject);
var msg1 = new BrokeredMessage(payload);
msg1.MessageId = CreateDeterministicIdFromHash(payload);
msg1.Label = "1st";
await sender.SendAsync(msg1).ConfigureAwait(false);
var msg2 = new BrokeredMessage(payload);
msg2.MessageId = CreateDeterministicIdFromHash(payload);
msg2.Label = "2nd";
await sender.SendAsync(msg2).ConfigureAwait(false);
```
The sample creates a GUID like ID by making an object hash using serialized object. For example, using JSON.Net you could get the serialized object and pass it to `CreateGuidLikeIdFromHash` to provide the deterministic ID that is based on a hash. As result of this snippet, there will be only one message received when a queue has deduplication enabled. 

`CreateGuidLikeIdFromHash`  method could be implemented in the following way:

```csharp
static string CreateDeterministicIdFromHash(string input)
{
    var inputBytes = Encoding.Default.GetBytes(input);
    // use MD5 hash to get a 16-byte hash of the string
    using (var provider = new MD5CryptoServiceProvider())
    {
        var hashBytes = provider.ComputeHash(inputBytes);
        return new Guid(hashBytes).ToString();
    }
}
```
[**Update**: as Clemens Vasters [pointed out][2] correctly, MD5, or any other cryptography hashes, should not be used for non-cryptographic purposes. [Data.HashFunction library][3] offers number of non-cryptographic hashes that can be used instead.]

Et voilà. Now you can leverage native ASB deduplication using your custom data from the message itself without unnecessary intermediaries or performance impact. 

Stay deduplicated!

\* as pointed out by one of the readers, order might not be the best example. Keep in mind, this is just to serve an example, not solve world's problems :)

\** deduplication with Azure Functions [sample](http://microsoftintegration.guru/2016/09/20/use-azure-function-to-deduplicate-messages-on-azure-service-bus) by Michael Stephenson

\*** `RequiresDuplicateDetection` needs to be set to `true` along with `DuplicateDetectionHistoryTimeWindow` set to the time span duplicates detection is taking place per message


[1]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2016/deduplication/deduplication.keys.jpg
[2]: https://twitter.com/clemensv/status/805499155351240706
[3]: https://github.com/brandondahler/Data.HashFunction
