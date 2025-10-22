---
title: Processing Azure Services EventGrid events with NServiceBus
slug: processing-azure-services-eventgrid-events-with-nservicebus
date: '2018-07-24T06:28:00'
updated: '2018-07-25T05:15:12.238474'
draft: false
tags:
- EventGrid
- Azure
author: Sean Feldman
---
<center>
[![enter image description here][1]][2]
</center>

In the previous post [Processing Azure EventGrid events with NServiceBus][3], I showed how to process custom events emitted to EventGrid using NServiceBus.

In this post, I’ll focus on events emitted by EventGrid for Azure services such as Blob Storage and Resources. Note that there are other Azure resource providers that can raise EventGrid events which could be processed in the same manner.

To make processing simpler, I’ve extracted the logic for message conversion and contracts into its package, [NServiceBus.AzureEventGrid.StorageQueues]( https://www.nuget.org/packages/NServiceBus.AzureEventGrid.StorageQueues). 

To enable EventGrid message processing, NServiceBus endpoint configured to use Azure Storage Queues transport should invoke the following configuration API:

```
var transport = endpointConfiguration.UseTransport<AzureStorageQueueTransport>();
transport.EnableSupportForEventGridEvents();
```

## What Services support EventGrids events?

 - Resource Groups
 - Azure Subscriptions
 - Blob Storage
 - Service Bus
 - Event Hubs
 - IoT Hubs
 - Media Services
 - Container Registry

## Subscribing to Storage Blob events

```
storageid=$(az storage account show --name eventgridasq --resource-group EventGrid-ASQ-RG --query id --output tsv)
queueid="$storageid/queueservices/default/queues/queue"
```

Note: this is Bash script. For Windows AZ CLI the syntax is slightly different, `$storageid=(az storage...)`.

```
az eventgrid event-subscription create \
  --resource-id $storageid \
  --name asq-blob-subscription \
  --endpoint-type storagequeue \
  --endpoint $queueid
```

Azure Event Grid event schema for Blob storage defined [here](https://docs.microsoft.com/en-us/azure/event-grid/event-schema-blob-storage) is defined in the package mentioned above and can be subscribed to using the standard NServiceBus syntax. Below is an example of handling Storage Blob `Microsoft.Storage.BlobCreated` event:


```
public class BlobCreatedHandler : IHandleMessages<BlobCreated>
{
  static ILog log = LogManager.GetLogger<BlobCreated>();
```

```
public Task Handle(BlobCreated message, IMessageHandlerContext context)
  {
    log.Info($"EventGrid.eventType: {context.MessageHeaders[Headers.EnclosedMessageTypes]}");
    log.Info($"URL: {message.Url}");
    log.Info($"API: {message.Api}");
    log.Info($"BlobType: {message.BlobType}");
    log.Info($"ContentType: {message.ContentType}");
    log.Info($"ContentLength: {message.ContentLength}");
    return Task.CompletedTask;
  }
}
```

Creating a blob with “This is a test.” content 

<center>
![blob][4]
</center>

will produce the following output:

2018-07-14 11:24:25.560 INFO  Microsoft.Storage.BlobCreated URL: https://eventgridasq.blob.core.windows.net/eventgrid-post/file.txt<br>
2018-07-14 11:24:25.585 INFO  Microsoft.Storage.BlobCreated API: PutBlob<br>
2018-07-14 11:24:25.592 INFO  Microsoft.Storage.BlobCreated BlobType: BlockBlob<br>
2018-07-14 11:24:25.598 INFO  Microsoft.Storage.BlobCreated ContentType: text/plain<br>
2018-07-14 11:24:25.602 INFO  Microsoft.Storage.BlobCreated ContentLength: 15

Update the blob with an additional character will cause `BlobCreated` event to fire again with an updated length:

2018-07-14 11:25:40.547 INFO  Microsoft.Storage.BlobCreated URL: https://eventgridasq.blob.core.windows.net/eventgrid-post/file.txt<br>
2018-07-14 11:25:40.556 INFO  Microsoft.Storage.BlobCreated API: PutBlob<br>
2018-07-14 11:25:40.562 INFO  Microsoft.Storage.BlobCreated BlobType: BlockBlob<br>
2018-07-14 11:25:40.569 INFO  Microsoft.Storage.BlobCreated ContentType: text/plain<br>
2018-07-14 11:25:40.576 INFO  Microsoft.Storage.BlobCreated ContentLength: **16** 

Once a blob is deleted, `Microsoft.Storage.BlobDeleted` will be fired

2018-07-14 11:33:21.228 INFO  BlobDeletedHandler URL: https://eventgridasq.blob.core.windows.net/eventgrid-post/file.txt<br>
2018-07-14 11:33:21.234 INFO  BlobDeletedHandler API: DeleteBlob<br>
2018-07-14 11:33:21.238 INFO  BlobDeletedHandler BlobType: BlockBlob<br>
2018-07-14 11:33:21.242 INFO  BlobDeletedHandler ContentType: text/plain<br>

<center>
![enter image description here][5]
</center>

## Processing Resource Group events

```
storageid=$(az storage account show --name eventgridasq --resource-group EventGrid-ASQ-RG --query id --output tsv)
queueid="$storageid/queueservices/default/queues/queue"
```

```
az eventgrid event-subscription create \
  --resource-group EventGrid-ASQ-RG \
  --name rg-subscription \
  --endpoint-type storagequeue \
  --endpoint $queueid
```

## The devil is in details

Every service has nuances associated with the events it emits. Look into documentation to understand how those generated. For example, Service Bus will emit events per entity until there’s an active receiver or no receive operation happened for two minutes as per [documentation]( https://docs.microsoft.com/en-us/azure/service-bus-messaging/service-bus-to-event-grid-integration-concept).

## What if a service doesn’t expose EventGrid events?

If you’d like to see more Azure services to emit EventGrid events, raise your request with the appropriate product groups responsible for the services you’re interested in.

## Summary

EventGrid offers a powerful event-driven ability. It’s still very new and as with anything new has a few rough edges. As time goes and more services are onboard, EventGrid will become a vital fabric of many Azure-based solutions. And potentially beyond Azure as well.
The code is available on [GitHub](https://github.com/SeanFeldman/EventGridWithNServiceBus).


[1]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2018/eventgrid-with-nsb/header2.png
[2]: https://weblogs.asp.net/sfeldman/processing-azure-services-eventgrid-events-with-nservicebus
[3]: https://weblogs.asp.net/sfeldman/processing-azure-eventgrid-events-with-nservicebus
[4]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2018/eventgrid-with-nsb/blob.png
[5]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2018/eventgrid-with-nsb/metrics.png
