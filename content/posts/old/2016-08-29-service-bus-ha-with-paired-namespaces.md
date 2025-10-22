---
title: Service Bus HA with paired namespaces
slug: service-bus-ha-with-paired-namespaces
date: '2016-08-29T04:36:00'
updated: '2016-08-29T04:41:46.318971+00:00'
draft: false
tags:
- AzureServiceBus
author: Sean Feldman
---
Azure Service Bus is one of the oldest cloud services on Azure. As any service living in the cloud, it grows, iterates, and changes. Among various features that the service has, there's one that could deserve a little more attention: paired namespaces.

An application communicating over Azure Service Bus is usually utilizing a namespace. Services and sometimes even entire regions can go down. That makes a single namespace a single point of failure. A possible solution is to enable high availability of the service. This is where Service Bus client can help. It can do so by using two namespaces rather than one. A primary and a secondary namespaces. The client is using both namespaces to achieve high availability. The feature is called PairedNamespaces.

A quick recap of how it works
-----------------------------

The client is normally sending to a primary namespace. In case primary namespace is no longer available, Azure Service Bus client will automatically switch to the secondary namespace. While sending messages to the secondary namespace, the client will also continue pinging the primary namespace behind the scenes to see if the primary namespace availability has changed and it's up again.  Ping messages are short-lived messages configured to self destruct after 1 second. While primary namespace is not available, the sender will be sending the messages to the secondary namespace. The secondary namespace is solely used as storage until the primary namespace is back online. Once the primary namespace is back, messages from the secondary (temporary storage) namespace will be moved to the primary namespace.

The secondary namespace has a very rigid structure. The structure is always a queue with the following path `<primary-namespacename>/x-servicebus-transfer/<backlog-queue-index>`

![enter image description here][1]

Backlog queues are used to hold the messages and number of the queues is defined when paired namespaces are configured using [`MessagingFactory.PairNamespaceAsync(SendAvailabilityPairedNamespaceOptions)`](https://msdn.microsoft.com/library/azure/microsoft.servicebus.messaging.messagingfactory.pairnamespaceasync.aspx) method.

In short, the primary namespace goes down; no message is lost, and all send operations are redirected to the secondary namespace. Once the primary namespace is back, all backed up messages are moved from the secondary to the primary namespace, to the appropriate queues/topics. To determine the right destination, each message is stamped with a `x-ms-path` custom property, indicating the destination entity for the message.

![enter image description here][2]

Except there are a few small details that need to be taken into consideration.

To test a failover scenario, the primary namespace has to be down. There's no API failover exposed. Therefore a workaround is to trick the client to think that namespace is down by pointing the primary namespace domain to some invalid IP address using the `hosts` files. 
According to documentation:

> ["Failures that trigger the failover timer are any MessagingException in which the IsTransient property is false or a System.TimeoutException."](https://azure.microsoft.com/en-us/documentation/articles/service-bus-async-messaging/#paired-namespaces).

Unfortunately, this is not what's happening. During a send attempt, once primary namespace was not available and `failoverInterval` time elapsed, `MessagingCommunicationException` was thrown by the ASB client. Surprisingly, the exception is **marked as transient**. To get the code working and verify that failover took place, **the message had to be retired**. Once the send operation was retried, ASB client uses the secondary namespace, and everything worked as expected. It's unfortunate that the exception is marked as transient, where it shouldn't be. On the positive side, it's not a bad idea to retry the operation, even if default retry policy does it already. The retry will ensure the failed send operation gets executed against the secondary namespace. 


Sample sender code
------------------

```
static async Task MainAsync()
    { 
        var connectionString1 = "Endpoint=sb://primary-pairednamespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=[key]";
        var namespaceManager1 = NamespaceManager.CreateFromConnectionString(connectionString1);
        var messagingFactory1 = MessagingFactory.CreateFromConnectionString(connectionString1);
```

```
var connectionString2 = "Endpoint=sb://secondary-pairednamespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=[key]";
        var namespaceManager2 = NamespaceManager.CreateFromConnectionString(connectionString2);
        var messagingFactory2 = MessagingFactory.CreateFromConnectionString(connectionString2);
```

```
if (!await namespaceManager1.QueueExistsAsync("testing"))
        {
            await namespaceManager1.CreateQueueAsync("testing");
        }
```

```
var sendAvailabilityPairedNamespaceOptions = new SendAvailabilityPairedNamespaceOptions(
            secondaryNamespaceManager:namespaceManager2,
            messagingFactory: messagingFactory2,
            backlogQueueCount: 3,
            failoverInterval: TimeSpan.FromSeconds(10),
            enableSyphon: true);
```

```
await messagingFactory1.PairNamespaceAsync(sendAvailabilityPairedNamespaceOptions);
```

```
var sender1 = await messagingFactory1.CreateMessageSenderAsync("testing");
        var receiver1 = await messagingFactory1.CreateMessageReceiverAsync("testing");
        var messageId = 1;
```

```
while (true)
        {
            try
            {
                var message = new BrokeredMessage("testing") {MessageId = messageId++.ToString()};
                // Set a breakpoint here and modify hosts file to contain "8.8.8.8 primary-pairednamespace.servicebus.windows.net"
                await sender1.SendAsync(message);
                Console.WriteLine(".");
            }
            catch (Exception e)
            {
                var me = (MessagingException) e;
                Console.WriteLine(e.GetType());
                Console.WriteLine(me.Detail.ErrorCode);
                Console.WriteLine(me.Detail.ErrorLevel);
                Console.WriteLine(me.Detail.Message);
                Console.WriteLine(me.IsTransient);
            }
```

```
await Task.Delay(2000);
        }
    }
```

Conclusions
-----------

The feature was [documented](https://azure.microsoft.com/en-us/documentation/articles/service-bus-paired-namespaces/) and API was [detailed](https://azure.microsoft.com/en-us/documentation/articles/service-bus-async-messaging/). However, it is still not commonly used. Can't be right. How come a feature, allowing HA out of the box is so neglected? Would be a killer feature if not a few caveats.

###**Failover API and testability**

The failover API was baked into the native client and was not exposed. Changing hosts file is far from an ideal way of verifying the feature works.

###**Feature Design**

Lack of explicit contract when failover is about to happen. General `MessagingCommunicationException` could be replaced with a more intention revealing exception that would not require relying on the transient nature of the exception. Not to mention that in the test above it turned to be not quite as expected.

Additional substantial factor has to do with the fact that paired namespaces were designed with sender and receiver as two different parties. I.e., sender application vs receiver application where each part would perform one type of operation, but not both. To demonstrate what I'm talking about, add a receiving operation to the sender application. While failover will take place and send operation will be successful, the receive operations would fail. This is due to the fact that this is not an active-active HA, and entities required by the receiver only exist in the primary namespace and not the secondary namespace. Could have been addressed by the ASB client if receive operations would just return null messages when requested to fetch and the client was in failover mode. But again, design decisions are hard to get right. Especially on the first time.

###**Cost**
 
Each send operation would become several operations, tripling the cost of a message when failover is occurring:
1. Send to the secondary namespace to store when the primary namespace is down.
2. Retrieve from the secondary namespace when the primary namespace is back.
3. Re-send to the primary namespace.

Let's be honest, what's a higher cost when you can still send messages that are vital to your business? An acceptable cost.

Summary
-------

If you require high availability today and can partition your application act as solely sender or receiver, paired namespaces feature could be a good option to use. If that's not your scenario, you could implement a more of an active-active approach, where entities are created and maintained on one or more namespace.

Credits
-------

Special thank you To John Taubensee for help with testing this feature.


[1]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2016/pairednamespaces/paired-namespace-secondary-namespace.png
[2]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2016/pairednamespaces/paired-namespace-custom-property.png
