---
title: Azure Service Bus Plugins
slug: asb-plugins
date: '2017-07-03T22:19:00'
updated: '2017-07-13T21:49:59.242050+00:00'
draft: false
tags:
- AzureServiceBus
author: Sean Feldman
---
[![Plugins][1]](https://weblogs.asp.net/sfeldman/asb-plugins)
For a very long time Azure Service Bus client [WindowsAzure.ServiceBus/](https://www.nuget.org/packages/WindowsAzure.ServiceBus/) was a black box. When it came to the customization of the message payload, it would allow choosing on serialization, and that's pretty much it. Message IDs were always generated as random Guids and were required to be overwritten to comply with project requirements. Needed to secure the payload? You'd need to have that code to operate on the data before it would become BrokeredMessage payload.
These are the hardships of the old client though. With the new client, [Microsoft.Azure.ServiceBus](https://www.nuget.org/packages/Microsoft.Azure.ServiceBus/) things are different. With support for extensibility, the new client offers a simple incoming and outgoing pipelines. These pipelines take plugins that have a relatively simple API but can help immensely with message customization when it's sent or received. This is what a [plugin skeleton](https://github.com/Azure/azure-service-bus-dotnet/blob/master/src/Microsoft.Azure.ServiceBus/Core/ServiceBusPlugin.cs) looks like (at the time of writing, this is still in preview):
```
public abstract class ServiceBusPlugin
{
  public abstract string Name { get; }
  public virtual bool ShouldContinueOnException => false;
  public virtual Task<Message> BeforeMessageSend(Message message)
  {
      return Task.FromResult(message);
  }
  public virtual Task<Message> AfterMessageReceive(Message message)
  {
      return Task.FromResult(message);
  }
}
```
In the [previous post](https://weblogs.asp.net/sfeldman/hello-microsoft-azure-servicebus), I've already talked about [MessageIdPlugin](https://github.com/Azure/azure-service-bus-dotnet-plugins/blob/dev/src/Microsoft.Azure.ServiceBus.MessageIdPlugin/readme.md) and [KeyVaultPlugin](https://github.com/Azure/azure-service-bus-dotnet-plugins/blob/dev/src/Microsoft.Azure.ServiceBus.KeyVaultPlugin/readme.md). In this post, I'd like to extend the topic by demonstrating another power that plugins bring to the game.
## Sending large messages
\*How large message can be?\*
Today it's 256KB/1MB including headers.
\*Isn't that a solved problem already? That's what [Claim Check pattern](http://www.enterpriseintegrationpatterns.com/patterns/messaging/StoreInLibrary.html) is for.\*
While claim check pattern is indeed the way to go, it is distracting from the actual code you most likely trying to get out - sending messages. Remember, another level of indirection can solve a problem. For sending and receiving large messages that could be a claim check plugin. A message exceeding maximum size would be saved to a blob, reference attached to the message, and upon receive payload would be read back and associated with the message. More than that, a plugin could determine based on some custom logic at what point a message should be "offloaded" to a blob or not. Criteria could be payload size or message type for example.
## Meet ServiceBus.AttachmentPlugin
And that's exactly what [ServiceBus.AttachmentPlugin](https://www.nuget.org/packages/ServiceBus.AttachmentPlugin/) is. Harvesting the power of OSS extensibility and NuGet packaging it implements Claim Check pattern plugin for the new ASB client.
To use the plugin, a connection string to Storage account is required. With Storage connection string, the plugin can be configured and used
### Configuration and registration
```
var sender = new MessageSender(connectionString, queueName);
var config = new AzureStorageAttachmentConfiguration(storageConnectionString);
var plugin = new AzureStorageAttachment(config);
sender.RegisterPlugin(plugin);
```
### Sending
```
var payload = new MyMessage { ... }; 
var serialized = JsonConvert.SerializeObject(payload);
var payloadAsBytes = Encoding.UTF8.GetBytes(serialized);
var message = new Message(payloadAsBytes);
```
### Receiving
```
var receiver = new MessageReceiver(connectionString, entityPath, ReceiveMode.ReceiveAndDelete);
receiver.RegisterPlugin(plugin);
var msg = await receiver.ReceiveAsync();
// msg will contain the original payload
```
Configuration applies the defaults, which [can be overriden](https://github.com/SeanFeldman/ServiceBus.AttachmentPlugin#configure-blobs-container-name).
[Visual](https://aspblogs.blob.core.windows.net:443/media/sfeldman/2017/asb-plugins/flow.PNG) of a sample message sent with the plugin.
## Seeing is believing
```
Install-Package ServiceBus.AttachmentPlugin -Pre
```
Found issues or have suggestions? Raise those [here](https://github.com/SeanFeldman/ServiceBus.AttachmentPlugin/issues).
[1]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2017/asb-plugins/plugins.jpg
