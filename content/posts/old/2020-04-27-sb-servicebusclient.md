---
title: Azure Service Bus SDK - ServiceBusClient
slug: sb-servicebusclient
date: '2020-04-27T04:19:00'
updated: '2021-07-26T23:30:11.491335+00:00'
draft: false
tags:
- AzureServiceBus
- AzureSDK
- .NET
author: Sean Feldman
---
![Azure Service Bus SDK - ServiceBusClient][2]
Note: SDK Track 2 is still a preview and subject to API changes.

  

Table of contents
1. [The future of Azure Service Bus .NET SDK][3]
2. ServiceBusClient
3. [ServiceBusSender][4]
4. [ServiceBusReceiver][5]
5. [Safe Batching](6)
## Entry point
Back in the days of Track 0 to be able to work with the SDK, everything had to go through a factory class called `MessagingFactory`. The messaging factory was responsible for the construction of all the Service Bus constructs to perform any operation. These constructs where `QueueClient`, `SubscriptionClient`, `TopicClient`, `MessageSender`, and `MessageReceiver`. The messaging factory had dedicated factory methods per each construct. That's probably not the most important technical detail except that there was something additional that `MessageFactory` has provided. Connection pooling
> A connection pool is a cache of broker connections maintained so that the connections can be reused when future requests to the broker are required. Connection pools are used to enhance performance. Opening and maintaining a new connection for each construct is costly and wastes resources. In connection pooling, after a connection is created, it is placed in the pool, and it is used again so that a new connection does not have to be established. Connection pooling also cuts down on the amount of time a user must wait to establish a connection to the broker.

That has drastically changed in Track 2, where every construct was constructed directly by invoking a constructor and accepting either a connection string or a shared `ServiceBusConnection` object. When a connection string was used, a new connection would be established. The biggest drawback was the loss of the automatic connection pooling by default.
Trak 2 SDK is changing that again.
## Meet ServiceBusClient
Azure SDK guidelines prescribe a specific design for any service entry point using `Client` convention. For Azure Service Bus SDK, that's the `ServiceBusClient` class. This class is responsible for establishing the connection to the broker \_and\_ perform connection pooling for any entity-specific client created later. This will be covered in the next post.
`ServiceBusClient` can be constructed using a connection string or [`TokenCredential`][6], a credential capable of providing an OAuth token.
An additional optional parameter is `ServiceBusClientOptions`. The options object is used to configure the `ServiceBusClient` for its entire lifecycle. Those include options:
- `ServiceBusTransportType` - AMQP protocol over TCP (`AmqpTcp`) or WebSockets (`AmqpWebSockets`)
- `Proxy` - proxy to use when WebSockets are used
- `RetryOptions` - retry options specified using `ServiceBusRetryOptions`
Retry options provide a way to specify the default retry policy which needs to implement the `ServiceBusRetryPolicy` base class.
```
var options = new ServiceBusClientOptions
{
    TransportType = ServiceBusTransportType.AmqpTcp,
    RetryOptions = new ServiceBusRetryOptions(){
        Mode = ServiceBusRetryMode.Exponential,
        CustomRetryPolicy = new MyRetryPolicy()
    }
};
```
```
public class MyRetryPolicy : ServiceBusRetryPolicy
{
    public override TimeSpan? CalculateRetryDelay(Exception lastException, int attemptCount)
    {
        return TimeSpan.FromSeconds(10);
    }
```
```
public override TimeSpan CalculateTryTimeout(int attemptCount)
    {
        return TimeSpan.FromSeconds(30);
    }
}
```
Note: at this point, retry options set on the Service Bus client will be the options applied to every other client it creates.
```
await using var client = new ServiceBusClient(connectionString, options);
```
## Disposal
The `ServiceBusClient` implements `IDisposeAsync` and is responsible for resource cleanup. `.DisposeAsync()` has to be called when the client is no longer required and should be disposed of and was not created with a `using` keyword. This includes broker connection termination.
```
await sender.DisposeAsync();
```
And with this, we've concluded the entry point into the new Azure Service Bus SDK, a.k.a. Track 2. In the next post, we'll look at sending and receiving messages with the new client.
[2]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2020/sb-servicebusclient/start.jpg
[3]: https://weblogs.asp.net/sfeldman/the-future-of-asb-dotnet-sdk
[4]: https://weblogs.asp.net/sfeldman/sb-servicebussender
[5]: https://weblogs.asp.net/sfeldman/sb-servicebusreceiver
[6]: https://docs.microsoft.com/en-us/dotnet/api/azure.core.tokencredential?view=azure-dotnet
