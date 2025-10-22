---
title: Processing Azure EventGrid events with NServiceBus
slug: processing-azure-eventgrid-events-with-nservicebus
date: '2018-07-14T17:46:00'
updated: '2021-05-31T16:32:28.144216+00:00'
draft: false
tags:
- EventGrid
- NServiceBus
author: Sean Feldman
---
[![enter image description here][2]][1]

## What’s EventGrid and why it’s important?

EventGrid helps with creation of event-based systems. The service manages routing of events from various source to the subscribers. Its high throughput and availability make it very appealing. Currently supports a few Azure Services but will change over time as the service is adopted by more and more other Azure services.

So, what makes it so important? Event-based development. No longer polling. Instead, it’s a push-based model where events are pushed to the subscribers. Think of Serverless applications. No longer need to poll for a storage blob or a queue. Instead, when a blob is created, or a message is received, an event is fired. If you have developed using NServiceBus in the past, event-driven development is not a new concept to you, and you’ll see that EventGrid and NServiceBus pub/sub are playing along nicely.

## EventGrid providers

<center>
![enter image description here][3]
</center>

## Publishing and subscribing to events

Services that already act as event providers (topics) do not require any additional work and can be subscribed to as-is. For custom events, one or more custom topics can be created. To create a custom topic and configure a Storage Queue subscriber, follow the steps provided by Microsoft [here]( https://docs.microsoft.com/en-us/azure/event-grid/custom-event-to-queue-storage).

Note: make sure your queue name will be NServiceBus endpoint’s input queue.

To verify your code is working, the following snippet can be used to publish to the custom topic. Inspect Storage queue to find events stored as messages.

```csharp
var topicEndpoint = "https://<custom-topic>.<region>-1.eventgrid.azure.net/api/events";
var topicKey = "<topic-key>";
var topicHostname = new Uri(topicEndpoint).Host;
var topicCredentials = new TopicCredentials(topicKey);
var client = new EventGridClient(topicCredentials);
await client.PublishEventsAsync(topicHostname, GetEventsList());
Console.Write("Published events to Event Grid.");
```
To create one or more events (EventGrid supports batches), a collection of `EventGridEvent` needs to be created. A single event has a well defined schema, where custom event data is stored as `Data` property and event type as `EventType` property.

```csharp
new EventGridEvent
{
```
	  Id = Guid.NewGuid().ToString(),
	  Data = new BlogPostPublished
	  {
		ItemUri = post
	  },
	  EventType = nameof(BlogPostPublished),
	  EventTime = DateTime.Now,
	  Subject = "Processing Azure Event Grid events with NServiceBus",
	  DataVersion = "1.0"
```csharp
});
```
Storage queue should contain all published events

![enter image description here][4]

## Receiving EventGrid events with NServiceBus endpoint

NServiceBus can consume custom Storage Queue messages. EventGrid events can be treated as native integration messages. To enable this integration, a [custom envelope unwrapper]( https://docs.particular.net/transports/azure-storage-queues/configuration#custom-envelope-unwrapper) has to be registered.

```csharp
var jsonSerializer = new Newtonsoft.Json.JsonSerializer();
transport.UnwrapMessagesWith(cloudQueueMessage =>
{
	using (var stream = new MemoryStream(cloudQueueMessage.AsBytes))
	using (var streamReader = new StreamReader(stream))
	using (var textReader = new JsonTextReader(streamReader))
	{
		var jObject = JObject.Load(textReader);
		using (var jsonReader = jObject.CreateReader())
		{
			//try deserialize to a NServiceBus envelope first
			var wrapper = jsonSerializer.Deserialize<MessageWrapper>(jsonReader);
			if (wrapper.MessageIntent != default)
			{
				//this was a envelope message
				return wrapper;
			}
		}
		//this was an EventGrid event
		using (var jsonReader = jObject.CreateReader())
		{
  			var @event = jsonSerializer.Deserialize<EventGridEvent>(jsonReader);
			var wrapper = new MessageWrapper
			{
				Id = @event.Id,
				Headers = new Dictionary<string, string>
				{
					{ "NServiceBus.EnclosedMessageTypes", @event.EventType },
					{ "NServiceBus.MessageIntent", "Publish" },
					{ "EventGrid.topic", @event.Topic },
					{ "EventGrid.subject", @event.Subject },
					{ "EventGrid.eventTime", @event.EventTime.ToString("u") },
					{ "EventGrid.dataVersion", @event.DataVersion },
					{ "EventGrid.metadataVersion", @event.MetadataVersion },
				},
				Body = Encoding.UTF8.GetBytes(JsonConvert.SerializeObject(@event.Data)),
				MessageIntent = MessageIntentEnum.Publish
```
		    	};
		    	return wrapper;
		    }
```csharp
}
});
```
To help NServiceBus understand what event type the message represents, a specific header `NServiceBus.EnclosedMessageTypes` needs to be assigned the value of the EventGrid event published. 

Note: handled EventGrid events need to be declared in your NServiceBus using declarative or convention option.

```csharp
public class BlogPostPublished : IEvent
{
    public string ItemUri { get; set; }
}
```
`EventGridEvent` is an EventGrid wrapper defined by the service schema

```csharp
public class EventGridEvent
{
    [JsonProperty(PropertyName = "id")]
    public string Id { get; set; }
    [JsonProperty(PropertyName = "topic")]
    public string Topic { get; set; }
    [JsonProperty(PropertyName = "subject")]
    public string Subject { get; set; }
    [JsonProperty(PropertyName = "data")]
    public object Data { get; set; }
    [JsonProperty(PropertyName = "eventType")]
    public string EventType { get; set; }
    [JsonProperty(PropertyName = "eventTime")]
    public DateTime EventTime { get; set; }
    [JsonProperty(PropertyName = "metadataVersion")]
    public string MetadataVersion { get; set; }
    [JsonProperty(PropertyName = "dataVersion")]
    public string DataVersion { get; set; }
}
```
At this point, an event handler can be defined

```csharp
public class BlogPostPublishedHandler : IHandleMessages<BlogPostPublished>
{
    static ILog log = LogManager.GetLogger<BlogPostPublishedHandler>();
    public Task Handle(BlogPostPublished message, IMessageHandlerContext context)
    {
        log.Info($"Received {nameof(BlogPostPublished)}: {message.ItemUri}");
        log.Info($"Topic: {context.MessageHeaders["EventGrid.topic"]}");
        log.Info($"Subject: {context.MessageHeaders["EventGrid.subject"]}");
        log.Info($"Event time: {context.MessageHeaders["EventGrid.eventTime"]}");
        return Task.CompletedTask;
    }
}
```
Resulting in

<div>
2018-07-14 10:09:14.975 INFO  BlogPostPublishedHandler Received BlogPostPublished: https://weblogs.asp.net/sfeldman/eventgrid-events-with-nservicebus<br>
2018-07-14 10:09:14.980 INFO  BlogPostPublishedHandler Topic: /subscriptions/<subscription-id>/resourceGroups/EventGrid-ASQ-RG/providers/Microsoft.EventGrid/topics/Events<br>
2018-07-14 10:09:14.984 INFO  BlogPostPublishedHandler Subject: Processing Azure Event Grid events with NServiceBus<br>
2018-07-14 10:09:14.986 INFO  BlogPostPublishedHandler Event time: 2018-07-14 16:08:48Z
</div>

## Handling specific events

When a new event type is published, the endpoint will receive it and attempt to process. In case NServiceBus endpoint is not aware of the event type, it will end up in the error queue. This is caused by EventGrid subscription by default subscribing to all published events. To fix this, EventGrid subscription needs to be updated to receive only specific types.

```csharp
az eventgrid event-subscription update \
--resource-id "/subscriptions/<subscription-id>/resourceGroups/eventgrid-asq-rg/providers/microsoft.eventgrid/topics/events" \
--name asq-subscription \
--included-event-types BlogPostPublished
```
Once the subscription is updated, the filter will be on and only specified event types (`BlogPostPusblished` in this case) will be passed on to the Storage queue.

```csharp
{
  "destination": {
    "endpointType": "StorageQueue",
    "queueName": "queue",
    "resourceId": "/subscriptions/<subscription-id>/resourceGroups/EventGrid-ASQ-RG/providers/Microsoft.Storage/storageAccounts/eventgridasq"
  },
  "eventDeliverySchema": "InputEventSchema",
  "filter": {
    "includedEventTypes": [
  "BlogPostPublished"
    ],
    "isSubjectCaseSensitive": null,
    "subjectBeginsWith": "",
    "subjectEndsWith": ""
  },
  …
}
```
</div>

## What's next?

Next would be taking advantage of EventGrid with custom topics or Azure services that can already emit EventGrid events. In the next blog post I'll show how easy it would be to subscribe to Storage Blob events.

Happy eventing!


[1]: https://weblogs.asp.net/sfeldman/processing-azure-eventgrid-events-with-nservicebus
[2]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2018/eventgrid-with-nsb/header.png
[3]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2018/eventgrid-with-nsb/image.png
[4]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2018/eventgrid-with-nsb/image-1.png
