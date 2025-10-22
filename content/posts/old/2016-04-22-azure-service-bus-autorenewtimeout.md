---
title: Azure Service Bus - AutoRenewTimeout
slug: azure-service-bus-autorenewtimeout
date: '2016-04-22T06:16:00'
updated: '2017-06-16T20:59:28.226255+00:00'
draft: false
author: Sean Feldman
---
I was reading a [question][1] on StackOverflow where the requirement was to "Lock a Service-Bus Queue and prevent others from accessing it." Quite often when dealing with competing consumers and `PeekLock` mechanism it feels odd. What do you mean I'm in the middle of processing my message and it will re-appear on the queue?! Why do I need to worry about some `LockDuration`?! The answer is simple. The server allows the receiver to handle the message and completes it within `LockDuration` time. If the operation takes longer, the server will no longer respect the original lock token as it will be replaced by another receiver that got the message. 

This is great when message processing is under 1 min. But what if message processing takes longer. In case message processing does take longer, the message will re-appear on the queue. This can be controlled by increasing `LockDuration`. Even then, the maximum amount of time is only 5 minutes. What will happen if message processing exceeds 5 minutes? You've guessed it right; the message will be unlocked and handled by another receiver.

There are two options to address this:

 1. Manual lock renewal
 2. Automatic lock renewal

### Manual Lock Renewal

`BrokeredMessage` allows renewing an already obtained lock that was given when message was received.

```
var brokeredMessage = queueClient.Receive();
brokeredMessage.RenewLock();
```

It surely looks simple. What's not so trivial is the timing of when lock renewal should be issued. Not mention that lock renewal time management would pollute the code with an additional concern. Let's look at a better option.

### Automatic lock renewal

In one of the previous posts, I have covered the [OnMessage API][2]. One of the `OnMessageOptions` was `AutoRenewTimeout`. What this does is automatically renew message lock without increasing the delivery count up maximum to the time of `AutoRenewTimeout`. For example, setting it to 10 minutes will allow us to surpass the maximum 5 minutes of the `LockDuration` and allow message processing to take up to 10 minutes. Auto lock renewal will not be issued if callback takes longer than 10 minutes. 

Let's dive into a sample:
   
```
static async Task Go(NamespaceManager nsManager, MessagingFactory mf)
{
    var connectionString = Environment.GetEnvironmentVariable("ConnectionString");
    var nsManager = NamespaceManager.CreateFromConnectionString(connectionString);
    var mf = MessagingFactory.CreateFromConnectionString(connectionString);
```

```
if (!await nsManager.QueueExistsAsync("test").ConfigureAwait(false))
    {
        var desc = new QueueDescription("test")
        {
            LockDuration = TimeSpan.FromSeconds(45),
        };
        await nsManager.CreateQueueAsync(desc).ConfigureAwait(false);
    }
    var msg1 = new BrokeredMessage(new string('A', 5));
    msg1.MessageId = DateTime.Now.ToString();
    var sender = await mf.CreateMessageSenderAsync("test").ConfigureAwait(false);
    await sender.SendAsync(msg1).ConfigureAwait(false);
    var receiver = await mf.CreateMessageReceiverAsync("test");
    var options = new OnMessageOptions 
    {
        AutoComplete = false, // let us complete the message
        AutoRenewTimeout = TimeSpan.FromMinutes(10)
    };
    //callback
    receiver.OnMessageAsync(async (message) =>
    {
        var sw = new Stopwatch();
        Console.WriteLine("Callback started for message id " + message.MessageId);
        Console.WriteLine("delaying for 8 minutes");
        await Task.Delay(TimeSpan.FromMinutes(8));
        var body = message.GetBody<string>();
        Console.WriteLine($"processing id: {message.MessageId} body: {body}");
        Console.WriteLine("delivery count: " + message.DeliveryCount);
```

```
await message.CompleteAsync();
```

```
Console.WriteLine("Callback stopped");
    }, options);
    Util.ReadLine();
}
```

For this test code, a queue called `test` with `LockDuration` 45 seconds is used. The message received in the callback is handled for over 5 minutes and completed after 8 minutes.

Fantastic, we can obtain message lock for longer than 5 minutes! Just don't go crazy. You should strive to have shorter processing and not lock message for a long time. If you do, review what you're trying to do. Remember that processing that is stalled will be holding up the message until `AutoRenewTimeout` time is expired. Which at times is not a great idea.

Happy long processing!


**Update 2017-06-16**

Since this post there were still questions about guarantees on this operation. Due to the fact that this is ASB client initiated renewal, it's no different from `brokeredMessage.RenewLock();`. If operation fails after all the retries ASB client has in place, the lock won't be re-acquired and message will become visible. I.e. `AutoRenewTimeout` is **not** a guaranteed on the broker operation.


[1]: http://stackoverflow.com/questions/36705199/lock-a-service-bus-queue-and-prevent-others-from-accessing-it/36731132
[2]: http://bit.ly/onmessageapi
