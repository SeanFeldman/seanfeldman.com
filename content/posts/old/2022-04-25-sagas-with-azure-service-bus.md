---
title: Sagas with Azure Service Bus
slug: sagas-with-azure-service-bus
date: '2022-04-25T07:22:00'
updated: '2022-04-25T13:31:24.708063+00:00'
draft: false
tags:
- AzureServiceBus
author: Sean Feldman
---
## Introduction
Handling messages out of order is always tricky. The asynchronous nature of messaging makes it challenging. On top of that, systems in the real world are messy and unpredictable. That's why handling workflows always brings more complexity than just handling messages. To illustrate the challenge, I'll use a scenario where my workflow depends on two different services.
1. Payments
1. Shipping
To successfully complete an order, I'll need to handle a message from each service. `PaymentAccepted` from the Payments service and `ItemShipped` from the Shipping service. The order can be considered successfully completed only when the two messages are received. The absence of one of the messages would indicate a failed state and require a compensating action. The compensating action will depend on which one of the two messages has already been handled. I'll leave the details of the compensating action out of this post to keep it somewhat light.
## Setting the expectations
One of the assumptions I'll make is how we handle a given order. Both the payment and the shipping services would need to use a correlation ID to connect the things together. This could be an order ID that should be unique. Another assumption is how to handle messages out of order over time. This is where the [saga pattern](https://docs.microsoft.com/en-us/azure/architecture/reference-architectures/saga/saga). An important aspect to note is that it will require persisting the state because we'll deal with time. And while we could leverage an external storage/database service with Azure Service Bus, this is unnecessary, thanks to a feature called [Message Sessions](https://docs.microsoft.com/en-us/azure/service-bus-messaging/message-sessions). While Message Sessions is more commonly used for FIFO scenarios where the message processing order has to be the same as the message sending order, my choice of Message Sessions was not driven by that. An additional property of the Message Sessions feature that is frequently overlooked is the ability to have a state associated with a given session. The state is an arbitrary object kept on the broker and associated with the session ID. The state can event exist w/o any messages for the session being around. This session state can be accessed by the session ID and can hold up to a single message size of data.
## Implementation
With all this in mind, let's get to the implementation. Each of the two services, as mentioned above, will post a message. The messages will always indicate the order ID as a correlation ID and set the message's `SessionId` to this value. I'll use a specific GUID as the order ID and store it in a shared project under `Correlation.Id` to make the demo simple.
```
public static class Correlation
{
    public const string Id = "77777777-0000-0000-0000-000000000000";
}
```
To mimic the real world where messages can come out of order and at different times, the Shipping service will post a message with a delay.
```
await publisher.ScheduleMessageAsync(new ServiceBusMessage("Shipping OK")
{
    SessionId = Correlation.Id,
    ApplicationProperties = { { "MessageType", "ItemShipped" } },
}, DateTimeOffset.Now.Add(TimeSpan.FromSeconds(7)));
```
Notice the `MessageType` header. I'll use topics and subscriptions, filtering out messages based on the `MessageType` header. Similar code but without delay will be published an even from the Payments service.
```
await publisher.SendMessageAsync(new ServiceBusMessage("Payment OK")
{
    SessionId = Correlation.Id,
    ApplicationProperties = { { "MessageType", "PaymentAccepted" }  }
});
```
When these two are executed, `PaymentAccepted` will be delivered right away and `ItemShipped` after 7 seconds. And now to the saga implementation that will handle these messages coming out of order at different times and the option that not always both messages will make it.
## Saga implementation
As mentioned earlier, the saga will be implemented using Message Sessions. To process session messages, the SDK provides a `SessionProcessor`. To see messages flow in a way that is easier to digest, I'll set the number of sessions to handle to 1. Of course, we'd not want to handle a single session but instead multiple sessions in the real world.
```
var options = new ServiceBusSessionProcessorOptions
{
    MaxConcurrentSessions = 1,
    MaxConcurrentCallsPerSession = 1,
    SessionIdleTimeout = TimeSpan.FromSeconds(15)
};
var processor = client.CreateSessionProcessor(topicName: "orchestration", subscriptionName: "orchestrator", options);
```
Not that I'm using a topic and a subscription. You could also use a queue or some other topology. Here's how I've arranged my topology for this demo:
```
orchestration (topic)
│
└────orchestrator (subscription)
     │
     ├────ItemShipped (rule)
     │
     ├────PaymentAccepted (rule)
     │
     └────Timeout (rule)
```
Notice the `Timeout` rule. This will be needed whenever we are waiting for the arrival of the missing messages. Timeouts will be our postponing of saga execution until either all messages will be handled or we'll reach the condition where no more waiting can occur. Then, a compensating action has to be executed as we've given up.
A session has several lifecycle events that can take place. Those are:
```
processor.SessionInitializingAsync += args =>
{
    WriteLine($"Handling session with ID: {args.SessionId}");
    return Task.CompletedTask;
};
processor.SessionClosingAsync += args =>
{
    WriteLine($"Closing session with ID: {args.SessionId}");
    return Task.CompletedTask;
};
processor.ProcessErrorAsync += args =>
{
    WriteLine($"Error: {args.Exception}", warning: true);        
    return Task.CompletedTask;
};
```
And the important one, `ProcessMessageAsync`. Again, it's a bit overwhelming, so give it a quick look and head over to the explanation below.
```
processor.ProcessMessageAsync += async args =>
{
    // (1)
    var message = args.Message;
    var messageType = message.ApplicationProperties["MessageType"];
    WriteLine($"Got a message of type: {messageType} for session with ID {args.SessionId}");
    // (2)
    var sessionState = await args.GetSessionStateAsync();
    var state = sessionState is null
        ? new State()
        : sessionState.ToObject<State>(new JsonObjectSerializer())!;
    // (3)
    if (state.Completed)
    {
        WriteLine($"Completing the process for Order with correlation ID {message.SessionId}");
        var publisher = client.CreateSender("orchestration");
        await publisher.SendMessageAsync(new ServiceBusMessage($"Orchestration for Order with session ID {message.SessionId} is completed"));
    }
    Func<State, Task> ExecuteAction = messageType switch
    {
        // (4)
        "PaymentAccepted" => async delegate
        {
            state.PaymentReceived = true;
            await SetTimeoutIfNecessary(client, args, state, TimeSpan.FromSeconds(5));
        },
        "ItemShipped" => async delegate
        {
            state.ItemShipped = true;
            await SetTimeoutIfNecessary(client, args, state, TimeSpan.FromSeconds(5));
        },
        // (5)
        "Timeout" => async delegate
        {
            if (state.Completed || sessionState is null)
            {
                WriteLine($"Orchestration ID {args.SessionId} has completed. Discarding timeout.");
                return;
            }
            if (state.RetriesCount < 3)
            {
                await SetTimeoutIfNecessary(client, args, state, TimeSpan.FromSeconds(5));
            }
            else
            {
                WriteLine($"Exhausted all retries ({state.RetriesCount}). Executing compensating action and completing session with ID {args.SessionId}", warning: true);
                // Compensating action here
                await args.SetSessionStateAsync(null);
            }
        },
        _ => throw new Exception($"Received unexpected message type {messageType} (message ID: {message.MessageId})")
    };
    await ExecuteAction(state);
    static async Task SetTimeoutIfNecessary(ServiceBusClient client, ProcessSessionMessageEventArgs args, State state, TimeSpan timeout)
    {
        if (state.Completed)
        {
            WriteLine($"Orchestration with session ID {args.SessionId} has successfully completed. Sending notification (TBD).");
            await args.SetSessionStateAsync(null);
            return;
        }
        WriteLine($"Scheduling a timeout to check in {timeout}");
        var publisher = client.CreateSender("orchestration");
        await publisher.ScheduleMessageAsync(new ServiceBusMessage
        {
            SessionId = args.Message.SessionId,
            ApplicationProperties = { { "MessageType", "Timeout" } }
        }, DateTimeOffset.Now.Add(timeout));
        state.RetriesCount++;
        await args.SetSessionStateAsync(BinaryData.FromObjectAsJson(state));
    }
}
```
What this code is doing is the following:
1. Upon a received message, it looks at the message type and the session state.
1. Session state is the saga state. If one doesn't exist, a new state is initiated. Otherwise, it's deserialized into the POCO to be used for the logic. The state keeps the vital information for the decision-making that needs to survive over the time between the messages.
1. If the state indicates completion (both messages received), notify about the successful completion of the saga. The underlying session will be completed eventually.
1. If the message is `PaymentAccepted`, the state is updated to indicate this message has been handled. And right away, a timeout is set, if necessary.
1. If the message is `Timeout`, the state is checked for completion (meaning `PaymentAccepted` \_and\_ `ItemShipped` where received), or if the session state is null, telling the saga is over. If that's the case, the timeout message will be discarded as it has arrived after the saga has been completed. Otherwise, a simple number of retries will be checked to determine wherever the saga should continue waiting or not. This part is very custom, and I've decided to let the saga issue a timeout of 5 seconds for 3 times. You could do it exponentially or introduce different types of timeouts. \*\*But\*\* if the number of retries has been exceeded, we've never got one of the missing messages, and the saga has not been completed successfully. This is where a compensating action would occur, and the session state would be cleared. It's crucial to remove the session state to ensure it doesn't stay on the broker forever.
Here's a happy day scenario, when both messages make it to the topic:
```
[23:35:42] Handling session with ID: 77777777-0000-0000-0000-000000000000
[23:35:42] Got a message of type: PaymentAccepted for session with ID 77777777-0000-0000-0000-000000000000
[23:35:43] Scheduling a timeout to check in 00:00:05
[23:35:48] Got a message of type: Timeout for session with ID 77777777-0000-0000-0000-000000000000
[23:35:48] Scheduling a timeout to check in 00:00:05
[23:35:52] Got a message of type: Timeout for session with ID 77777777-0000-0000-0000-000000000000
[23:35:53] Scheduling a timeout to check in 00:00:05
[23:35:55] Got a message of type: ItemShipped for session with ID 77777777-0000-0000-0000-000000000000
[23:35:55] Orchestration with session ID 77777777-0000-0000-0000-000000000000 has successfully completed. Sending notification (TBD).
[23:35:57] Got a message of type: Timeout for session with ID 77777777-0000-0000-0000-000000000000
[23:35:57] Orchestration ID 77777777-0000-0000-0000-000000000000 has completed. Discarding timeout.
[23:36:13] Closing session with ID: 77777777-0000-0000-0000-000000000000
```
And this is what the execution looks like when one of the messages never arrives:
```
[01:15:16] Handling session with ID: 77777777-0000-0000-0000-000000000000
[01:15:16] Got a message of type: PaymentAccepted for session with ID 77777777-0000-0000-0000-000000000000
[01:15:16] Scheduling a timeout to check in 00:00:05
[01:15:21] Got a message of type: Timeout for session with ID 77777777-0000-0000-0000-000000000000
[01:15:21] Scheduling a timeout to check in 00:00:05
[01:15:26] Got a message of type: Timeout for session with ID 77777777-0000-0000-0000-000000000000
[01:15:26] Scheduling a timeout to check in 00:00:05
[01:15:31] Got a message of type: Timeout for session with ID 77777777-0000-0000-0000-000000000000
[01:15:31] Exhausted all retries (3). Executing compensating action and completing session with ID 77777777-0000-0000-0000-000000000000
[01:15:47] Closing session with ID: 77777777-0000-0000-0000-000000000000
```
## Recap
Modelling a process that is executing over time requires persistence. With Azure Service Bus we can leverage Message Sessions to keep the state along with the session's messages, adding timeout messages to provide some future checkpoints to determine wherever the compensating logic needs to be executed or not. with the session state, we can also inspect the state of the saga by querying for it with the session ID and the correlation ID to be used.
Full solution is available on [GitHub](https://github.com/SeanFeldman/Orchestration).
