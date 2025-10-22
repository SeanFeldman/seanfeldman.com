---
title: EventProcessorHost Inject Dependencies
slug: eventprocessorhost-inject-dependencies
date: '2016-03-16T05:04:00'
updated: '2016-03-16T06:03:14.754370+00:00'
draft: false
author: Sean Feldman
---
Processing with Azure EventHubs can be significantly simplified if using [`EventProcessorHost`](https://msdn.microsoft.com/library/microsoft.servicebus.messaging.eventprocessorhost.aspx). EventProcessorHost is using Azure Storage account to track last read locations (pointers) in event hub partitions. 

![enter image description here][1]

In order to start a host, `eventHubName`, `eventHubConnectionString`, and `storageConnectionString` need to be passed in (`eventProcessorHostName` could be a `GUID` or anything else).

```csharp
var eventProcessorHost = new EventProcessorHost(eventProcessorHostName, eventHubName, EventHubConsumerGroup.DefaultGroupName, eventHubConnectionString, storageConnectionString);
```
Once a host is created, a processor needs to be specified. A processor is a class implementing `IEventProcessor` contact which will allow to open and close processor, and process events data.

```csharp
eventProcessorHost.RegisterEventProcessorAsync<SimpleEventProcessor>();
```
While this is working great, there's no simple way to inject dependencies into the processor you define using registration demonstrated above. Gladly, there's a factory registration that allows registering `IEventProcessorFactory` implementation.

```csharp
eventProcessorHost.RegisterEventProcessorFactoryAsync(new EventProcessorFactory(dependency))
```
Where `EventProcessorFactory` is defined as follow:

```csharp
class EventProcessorFactory : IEventProcessorFactory
{
    private readonly IDependency dependency;
    public EventProcessorFactory(IDependency dependency)
    {
        this.dependency= dependency;
    }
    public IEventProcessor CreateEventProcessor(PartitionContext context)
    {
        return new SimpleEventProcessor(dependency);
    }
}
```
And now we can define our `SimpleEventProcessor` processor with any dependencies that we want. 

Happy processing!


[1]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2016/event-processor-host.png
