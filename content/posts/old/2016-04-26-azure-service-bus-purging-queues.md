---
title: Azure Service Bus - Purging Queues
slug: azure-service-bus-purging-queues
date: '2016-04-26T05:49:00'
updated: '2016-04-29T16:22:10.685260+00:00'
draft: false
tags:
- ASB
author: Sean Feldman
---
Testing code that involves queues always has some utility code that is responsible for test cleanup. The cleanup is often implemented as a queue purge operation. For example, MSMQ allows to delete all messages in a queue by calling a `Purge()` command on a queue.
```
MessageQueue queue = new MessageQueue(".\\exampleQueue");
queue.Purge();
```
Simple. Convenient. Not possible with Azure Service Bus.
There are a few options to handle situations when the purge operation is needed. None of those options is perfect, but is a workable solution until native implementation is provided (vote for the suggestion on [UserVoice][1]).
## Drain messages
Draining messages is receiving all of the messages found. Execution time will depend on a number of messages found in a queue. To make if faster, multiple message receivers can be used. To make it less chatty, receiving mode should be set to `ReceiveAndDelete` rather than to `PeekLock`. This will reduce the latency and number of operations.
## Receive in batches
Batching will help with getting as many messages as possible in a single operation. It will be subject to the quotas imposed by the service tier being used.
## Use async
Not need to explain that async operations are much more preferred with IO-based operations. When receiving messages in batches, make sure to use `ReceiveBatchAsync()` and not its synchronous counterpart.
```
var mf = MessagingFactory.CreateFromConnectionString(connectionString);
```
var receiver = await mf.CreateMessageReceiverAsync("queue", ReceiveMode.ReceiveAndDelete);
while (true)
{
var messages = await receiver.ReceiveBatchAsync(batchSize);
if (!messages.Any())
{
break;
}
};
## Additional options
### Message TimeToLive
When sending messages, if possible, set `TimeToLive` to expire those messages prior to receiving them back. For example, assuming your test suit takes 10 minutes to run, have messages TTL set to 10 minutes. Make sure you don't set `EnableDeadLetteringOnMessagExpiration`. That will cause your DLQ to fill up fast.
### Message stamping
Last, but not the least, try stamping your messages with a test run if possible. Messages can be invisible and regular draining will not remove those. For your test run, for example, you could generate messages with a unique header that would contain a test run ID. Test run ID would be unique per your test session. When receiving messages, discard those messages that don't have the matching test run ID.
[1]: https://feedback.azure.com/forums/216926-service-bus/suggestions/6154597-queue-purge
