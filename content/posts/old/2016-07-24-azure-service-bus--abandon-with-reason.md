---
title: Abandon with Reason
slug: azure-service-bus--abandon-with-reason
date: '2016-07-24T21:07:00'
updated: '2016-07-24T21:20:36.057011+00:00'
draft: false
author: Sean Feldman
---
In some cases, when a message should be abandoned, Azure Service Bus offers `BrokeredMessage.Abandon()` API. The message is abandoned immediately; delivery count is increased, and message re-appears on the broker. In case `MaxDeliverCount` is exceeded, the message is moved to the designated dead letter queue. Whenever a message is moved to a dead letter queue, it is stamped with two standard properties: `DeadLetterReason` and `DeadLetterErrorDescription`. Here's an example of how to get a message dead lettered and stamped with these two properties
```
void Main()
{
    MainAsync().GetAwaiter().GetResult();
}
static async Task MainAsync()
{
    var connectionString = Environment.GetEnvironmentVariable("AzureServiceBus.ConnectionString");
    var namespaceManager = NamespaceManager.CreateFromConnectionString(connectionString);
    var queueName = "test";
    if (!await namespaceManager.QueueExistsAsync(queueName))
    {
        var queueDescription = new QueueDescription(queueName) { 
            MaxDeliveryCount = 2
        };
        await namespaceManager.CreateQueueAsync(queueDescription);
        Console.WriteLine("Queue created");
    }
    else
    {
        Console.WriteLine("Queue existed");
    }
    var factory = await MessagingFactory.CreateAsync(namespaceManager.Address, namespaceManager.Settings.TokenProvider);
    var sender = await factory.CreateMessageSenderAsync(queueName);
    var msg1 = new BrokeredMessage("test-1");
    await sender.SendAsync(msg1);
    var receiver = await factory.CreateMessageReceiverAsync(queueName);
    var msg1back = await receiver.ReceiveAsync();
    await msg1back.AbandonAsync();
    msg1back = await receiver.ReceiveAsync();
    await msg1back.AbandonAsync();
}
class TestMessage { }
```
As a result of this code, the queue called "test" will have a dead lettered message, with the two properties populated as following:
- \*\*DeadLetterReason\*\*: MaxDeliveryCountExceeded
- \*\*DeadLetterErrorDescription\*\*: Message could not be consumed after 2 delivery attempts.
Great information, except it doesn't help us to understand the real issue for which the message was rejected and abandoned, to begin with. For that, there's a better way to abandon messages. Always abandon with a reason. `BrokeredMessage` provides an overload `Abandon(IDictionary()`. Use this overload to abandon messages while providing the reason. After all, you never know when it will be the last time that the message was attempted. Below is a slightly modified code to achieve the same, except this time there's a custom property called "Reason" to indicate \_why\_ the message was abandoned.
```
await msg1back.AbandonAsync(new Dictionary<string, object> { { "Reason", "Blah"} });
```
After running the code with the modified abandon code, custom properties will contain the reason in addition to the properties stamped by the broker when the message got moved to the DLQ.
- \*\*Reason\*\*: Blah
- \*\*DeadLetterReason\*\*: MaxDeliveryCountExceeded
- \*\*DeadLetterErrorDescription\*\*: Message could not be consumed after 2 delivery attempts.
## Warning: Custom Properties Only
Be aware that abandon can only affect custom properties and not the standard properties. For example, let's say you're trying to abandon a message and set the standard property Label while doing so.
```
await msg1back.AbandonAsync(new Dictionary<string, object> { { "Reason", "Blah" }, { "Label", "ABC" });
```
What will happen is that there will be a custom property "Label" added to the rest of the custom properties, and it will contain the value "ABC", leaving the standard property "Label" untouched. The custom properties will contain the following:
- \*\*Reason\*\*: Blah
- \*\*Label\*\*: ABC
- \*\*DeadLetterReason\*\*: MaxDeliveryCountExceeded
- \*\*DeadLetterErrorDescription\*\*: Message could not be consumed after 2 delivery attempts.
So the next time you abandon a message, don't burn all the bridges. Leave a reason behind.

