---
title: Service Bus Message to Blob
slug: asb-message-to-blob
date: '2022-02-28T06:26:31.331946+00:00'
updated: '2022-02-28T06:26:31.316316+00:00'
draft: false
tags:
- AzureServiceBus
- Functions
author: Sean Feldman
---
About 5+ years ago I blogged about [turning messages into audit blobs][1]. Back then, it was for Storage Queue messages and the early Azure Functions implementation that required portal configuration. Since then, Storage Queues has been replaced by Azure Service Bus and Azure Functions has gained the ability to declare everything through the code. And not only that but also in two different ways, using

1. In-Process SDK
1. Isolated Worker SDK (out-of-process)

The concept hasn't changed much but the the code did become somewhat simpler.

**In-Process SDK**

```
public static class MessageTriggeredFunction
{
    [FunctionName(nameof(MessageTriggeredFunction))]
    public static async Task Run(
        [ServiceBusTrigger("myqueue", Connection = "ServiceBusConnectionString")]string payload,
        string messageId,
        [Blob("messages/{messageId}.txt", FileAccess.Write, Connection = "StorageAccountConnectionString")] Stream output)
    {
        await output.WriteAsync(Encoding.UTF8.GetBytes(payload));
    }
}
```


**Isolated Worker SDK**

```
public class MessageTriggeredFunctionIsolated
{
   [Function(nameof(MessageTriggeredFunctionIsolated))]
   [BlobOutput("messages/{messageId}.txt", Connection = "StorageAccountConnectionString")]
   public string Run(
       [ServiceBusTrigger("myqueue", Connection = "ServiceBusConnectionString")] string payload,
       string messageId)
  {
            return payload;
  }
}
```

The two snippets will result in the same outcome - a message will trigger the function and cause a blob to be generated and named as `message-id.txt` where `message-id` will be the physical message id.

[1]: https://weblogs.asp.net/sfeldman/azure-functions-to-make-audit-queue-and-auditors-happy
