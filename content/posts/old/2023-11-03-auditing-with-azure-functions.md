---
title: Auditing with Azure Functions
slug: auditing-with-azure-functions
date: '2023-11-03T17:29:00'
updated: '2023-11-06T17:24:39.046842+00:00'
draft: false
author: Sean Feldman
---
In the previous two posts about [recoverability][1], I focused on the rainy day scenarios where intermittent failures require retries and backoffs. This post will focus on the happy day scenario, where everything works as expected. So what's the issue then?

A successful message processing is not the only outcome that's required. More often than not there's also an audit trail that's requried. Imagine processing purchase orders. Not only you want to know nothing has failed. You might also want to have the confidence in a form of an audit trail that consists of those processed messages.

With Azure Functions Isolated Worker SDK, this becomes an extremely easy feature to implement. You could implement it as a standalone middleware but I chose to combine it with the revoverability middleware to keep the picture complete.

```
public async Task Invoke(FunctionContext context, FunctionExecutionDelegate next)
{
	try
	{
	    await next(context);
```

```
await Audit(message, context);
	}
	catch (AggregateException exception)
	{
	    // Recoverability, omitted for clarity
	}
}
```

The implementation for auditing is just sending a message to the queue chosen to be the audit queue. Similar to the centralized error queue.

```
private async Task Audit(ServiceBusReceivedMessage message, FunctionContext context)
{
    var auditMessage = new ServiceBusMessage(message);
    auditMessage.ApplicationProperties["Endpoint"] = context.FunctionDefinition.Name;
    await using var serviceBusSender = serviceBusClient.CreateSender("audit");
    await serviceBusSender.SendMessageAsync(auditMessage);
}
```

Notice the custom header `"Endpoint"`. This is intentional to keep track of the endpoint/function that has successfully processed the message that got audited. While there is additional information that could be propagated with the audited message, this is enough for a basic audit trail.

[1]: https://weblogs.asp.net/sfeldman/recoverability-with-azure-functions-delayed-retries
