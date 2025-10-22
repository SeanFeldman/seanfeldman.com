---
title: Azure Service Bus - OnMessage API
slug: azure-service-bus-onmessage-api
date: '2016-03-18T05:08:28.539994+00:00'
updated: '2016-03-18T05:08:28.524362+00:00'
draft: false
author: Sean Feldman
---
When it comes to receiving messages with ASB, there are plenty of options:

 - `QueueClient` to receive messages from queues 
 - `SubscriptionClient` to receive messages from subscriptions 
 - `MessageReceiver` to receive messages from queues or subscriptions (which is convenient since doesn't require particular receiver type per entity type)

All support Receive/ReceiveAsync for a single message receiving operation. Though usually, when you receive messages you receive those throughout your entire application life and need a message pump. While it sounds not a complicated task, many aspects need to be taken into consideration when building a message pump. What's nice with ASB is that you don't have to. It's given to you with `OnMessage` API.

`OnMessage` API is an asynchronous process that receives messages in an event-driven message pump.
When calling OnMessage, the client starts an internal message pump that continuously polls the queue or subscription. This message pump consists of an infinite loop that issues a Receive() call. If the call times out, it issues the next Receive() call. `OnMessage` accepts a callback that passes in the message that is received and needs to return a task. Also, OnMessageOptions is passed it defining the following:

 1. AutoComplete - if set to `true`, once callback is completed, the message is automatically completed. If set to false, you need to complete (`CompleteAsync`) the message yourself.
 2. AutoRenewTimeout - if processing is taking longer than the lock duration, ASB will issue lock time extension w/o increasing the delivery count.
 3. MaxConcurrentCalls - the number of concurrent calls to the callback ASB will make.

Equipped with this options, creation of a message pump is a breeze:

```
var receiver = await messageFactory.CreateMessageReceiverAsync("test");
var options = new OnMessageOptions 
{
  AutoComplete = true,
  AutoRenewTimeout = TimeSpan.FromMinutes(1), // for lock duration 30 secs
  MaxConcurrentCalls = concurrencyLevel
};
```

```
// callback
receiver.OnMessageAsync(async (message) =>
{
  // processing message
}, options);
```

What's the benefit of this approach:

 1. No need to worry about creating the pump
 2. Auto-completion
 3. Auto-extension of lock duration if operation is taking longer
 4. Easy control over concurrency
 5. Bonus: error handling

How does the error handling working? By subscribing to the `OnMessageOptions.ExceptionReceived` event, we get notified whenever `OnMessage` is failing to receive a message _or_ message processing is failing in the message pump code.

With this information, you can quickly build message pump and handle exception while receiving or processing messages. Whenever the message is completed, it will be marked as such, if it's failing, ASB will abandon it and will try to receive again later.
