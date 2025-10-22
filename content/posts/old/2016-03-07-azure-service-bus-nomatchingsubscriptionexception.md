---
title: Azure Service Bus - NoMatchingSubscriptionException
slug: azure-service-bus-nomatchingsubscriptionexception
date: '2016-03-07T05:02:00'
updated: '2016-03-07T05:35:41.596032+00:00'
draft: false
author: Sean Feldman
---
Azure Service Bus has a rich pub/sub mechanism supporting multiple options.

For each topic, there might be multiple subscriptions. Each subscription can contain one or more rules. If one of the subscriber rules is evaluated as `true`, a message published on the topic is _copied_ to subscription, which is a queue on its own.

![enter image description here][1]

When no rule evaluates as `true`, a message will not be stored with subscription and will be discarded.

![enter image description here][2]

For most scenarios this is working fine, and that is the default behavior for Azure Service Bus. However, what if it is significant to make sure that events published have subscribers? Doesn't matter if messages will or will not be handled, but important to ensure that there are subscribers. Azure Service Bus can support this scenario among other options that by defaults are turned off. 

To ensure that there are subscribers for a topic, ASB provides a flag on topic, `EnableFilteringMessagesBeforePublishing`. Setting this flag to `true` will make sure that if there are no subscriptions for topic, a `NoMatchingSubscriptionException` exception will be thrown on the client sending an event.

```csharp
var topicDescription = new TopicDescription(topicPath)
{
  EnableFilteringMessagesBeforePublishing = true
};
```
Client code will be responsible for handling this exception. Therefore, think twice if that is a desired behavior on the sender side. If it is, then make sure to deal with the exception.

	var topicClient = TopicClient.CreateFromConnectionString(connectionString, topicPath);
	var msg = new BrokeredMessage(messageBody);
	try
	{	        
		await topicClient.SendAsync(msg);
	}
	catch (NoMatchingSubscriptionException ex)
	{
		logger.LogError(ex.Message);
	}

Running this code will result in the following message being logged (IDs and timestamp will be different):

```
There is no matching subscription found for the message with MessageId '47eda34d2a764b76b8363b7d85463b24'. TrackingId:aa0d3da1-9e75-478b-ae8f-cd60d195ed8b_G15_B9,TimeStamp:3/7/2016 5:28:38 AM
```
[1]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2016/topic-subscription.png
[2]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2016/topic-subscription-empty.png
