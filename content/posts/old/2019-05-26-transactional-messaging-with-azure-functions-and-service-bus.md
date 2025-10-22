---
title: Transactional messaging with Azure Functions and Service Bus
slug: transactional-messaging-with-azure-functions-and-service-bus
date: '2019-05-26T21:17:00'
updated: '2019-05-26T21:23:01.542525+00:00'
draft: false
tags:
- AzureServiceBus
- AzureFunctions
author: Sean Feldman
---
## Azure Functions basics

Azure Functions design is a modular design. It consists of
- Mandatory trigger
- Function logic
- Optional one or more output bindings

![Function general design][1]

Triggers and output bindings can be of different types. For example, a trigger could be an Azure Service Bus message, while an output binding could be a Storage Blob. The flexibility to mix and match is extremely powerful but has a price. And that price is the necessity to keep triggers and output bindings independent of each other, having no connection or relation whatsoever. In almost all combinations of triggers and output bindings, it's expected to be the case with one exception when both the trigger and the output binding are of Service Bus type.

First, what's a typical function with Service Bus input and output would look like?

```
public static class ServiceBusTriggeredFunction
{
    [FunctionName("queue-in")] 
    public static async Task Run(
        [ServiceBusTrigger("queue-in", Connection = "ConnectionString")]Message message,
        [ServiceBus("queue-out", Connection = "ConnectionString")]IAsyncCollector<string> collector,
        ILogger logger)
    {
        logger.LogInformation("Sending a message out");
        await collector.AddAsync($"Processed message with ID {message.MessageId}");
        logger.LogInformation("Done");
    }
}
```


So what's the problem?

Most of the time, this design is working just fine. But sometimes, there are issues. One of those issues are those pesky intermittent failures. For example, the incoming message that couldn't be completed. Looking at the sample above, the collector is given a string, which is turned into a message that is immediately dispatched. 

When an incoming message arrives

![incoming.messages][2]

The function is triggered, and an outgoing message is emitted via the collector.

![processing.1][3]

Notice the "Done" statement was not logged yet. The outgoing message will be created while the incoming message is still in the queue-in.

![incoming.and.outgoing.messages][4]

But then, the incoming message is failing to be completed. Because of that, it will be re-delivered to the function and reprocessed. This can happen several times.

![enter image description here][5]

And as long as that happens (2 failures in this example), output messages are generated. 

![incoming.and.more.outgoing.messages][6]

In the cloud world, these "duplicates" are not unexpected. One of the options to handle a situation such as this is to implement idempotent processing of the outgoing messages to ensure duplicates are disregarded. But is there a different way?

There is — transactional message processing.

## Transactional messaging with Service Bus

Service Bus' transactional processing allows sending the outgoing message(s) along with the completion of the incoming message in an atomic operation, ensuring all messages either succeed or get reverted. For that to work, the collector needs to send messages via the input queue. Which is not possible by design.

It would work if the Service Bus trigger and output binding would share the same connection and would be possible to define the "send-via" entity for the output binding. Unfortunately, that would mean coupling between the two components, which are by design shouldn't be.

Gladly, there's a way. Any function can be injected with additional dependencies SDK can supply. For Service Bus trigger it's the [message metadata][7], a.k.a properties or headers. There's an additional, undocumented option. The `MessageReceiver` used to retrieve the incoming message is also available to be injected in the function. A true hidden gem! Message receiver contains the connection string, which is necessary to create a message sender that would participate in the transaction. With that, the function will be able to send the message and it won't be dispatched to the output queue unless the incoming message is successfully completed. 

```
public static class AsbConnectedFunction
{
    [FunctionName("queue-in")]
    public static async Task Run(
        [ServiceBusTrigger("queue-in", Connection = "ConnectionString")]Message message,
        ILogger logger,
        MessageReceiver messageReceiver)
    {
        using (var scope = new TransactionScope(TransactionScopeOption.RequiresNew, TransactionScopeAsyncFlowOption.Enabled))
        {
            var messageSender = new MessageSender(messageReceiver.ServiceBusConnection, "queue-out", "queue-in");
```

```
var outgoingMessage = new Message(Encoding.UTF8.GetBytes($"Processed message with ID {message.MessageId}"));
```

```
logger.LogInformation("Sending a message out");
            await messageSender.SendAsync(outgoingMessage);
            logger.LogInformation("Done");
```

```
await messageReceiver.CompleteAsync(message.SystemProperties.LockToken);
```

```
scope.Complete();
        }
    }
}
```

Note: completing manually a message in the function will cause function host to throw an exception when it tries to do the same. 

![exception][9]

To disable function auto-completion of the incoming message, turn [`autoComplete` flag][8] off in `host.json`.

Sending a message to the `queue-in` and setting a breaking point at the completion command, will reveal that even though the outgoing message was dispatched, it does not appear to be in the `queue-out`. Not until the incoming message is completed.

Sending the message with successful incoming message completion

![incoming.messages][10]

results in a single message dispatched. In case there are errors, the outgoing message is discarded and the function is invoked again. Yet there's only one message dispatched to the `queue-out`.

![atomic.messages][11]

That's a powerful option that is missing from Azure Functions when working with Azure Service Bus. Remember that transaction processing is slower than non-transactional and should be employed where it necessary and required.

## What's next?

Transactional message processing with Service Bus in Functions is a great hidden feature. To my personal taste, the need to manually create a sender and wrap the logic in a transaction scope is clunky and less than optimal. I would rather like to see the code less about the infrastructure and the inner workings of Service Bus and more about business. Imagine function code being expressed with POCOs and solely focus on the business logic in the following way:

```
public class GenericAsyncHandler : IHandleMessages<RegisterOrder>
```
	{
		public awaut Task Handle(RegisterOrder message, IMessageHandlerContext context)
		{
			// process order registration
			await context.Publish(new OrderRegistered { OrderId = message.OrderId });
		}
	}

Wait for a second, this is extremely similar to the  [NServieBus handlers][12] paradigm. Or is it? 

Interested to take your Functions to the next level and transform from a collection of utility methods into a manageable code? Stay tuned!

[1]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2019/asb-transaction-function/00.function.design.png
[2]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2019/asb-transaction-function/02.incoming.messages.png
[3]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2019/asb-transaction-function/processing.1.png
[4]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2019/asb-transaction-function/03.incoming.and.outgoing.messages.png
[5]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2019/asb-transaction-function/processing.2.png
[6]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2019/asb-transaction-function/04.incoming.and.more.outgoing.messages.png
[7]: https://docs.microsoft.com/en-us/azure/azure-functions/functions-bindings-service-bus#trigger---message-metadata
[8]: https://docs.microsoft.com/en-us/azure/azure-functions/functions-bindings-service-bus#hostjson-settings
[9]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2019/asb-transaction-function/exception.png
[10]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2019/asb-transaction-function/02.incoming.messages.png
[11]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2019/asb-transaction-function/05.atomic.messages.png
[12]: https://docs.particular.net/nservicebus/handlers/
