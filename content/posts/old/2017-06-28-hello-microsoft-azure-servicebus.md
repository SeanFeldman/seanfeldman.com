---
title: Hello Microsoft.Azure.ServiceBus
slug: hello-microsoft-azure-servicebus
date: '2017-06-28T05:04:11.959335+00:00'
updated: '2017-06-28T05:04:11.943737+00:00'
draft: false
tags:
- AzureServiceBus
author: Sean Feldman
---
[![hello][1]][2]

If you've missed the news, a [new Azure Service Bus client](https://twitter.com/jtaubensee/status/811303987156832256) is emerging on the horizon.

![tweet][3] 

This client is a significant development under the umbrella of multiple changes taking place in the Microsoft camp. A few of those are:

 - Open Source support
 - Public collaboration
 - Investment into documentation
 - Client customization

Open Source support is a big one. In the past, the WindowsAzure.ServiceBus client we've learned to love and hate was closed source. While decompiling was possible, that is far from optimal experience trying to understand the code and the decisions behind it. The code for the current client will stay closed, and probably good that it will. Some skeletons shouldn't be out of the closet. 

With the new client, the code is public on [GitHub](https://github.com/Azure/azure-service-bus-dotnet). No more fiddling with reflection tools. Can provide a better implementation? Send a PR. Found a bug? Raise an issue and tie it to PR. Connect discussions to the code. Have more eyes on the code and discussions that are happening. A real public collaboration. The type of cooperation that will promote superior results.

It would be unfair to talk about all of this excitement without calling out the elephant in the room. Documentation. Great strides were made to address a long-standing deficit. Guidance articles were added, and API documentation is refreshed. Here starts a long journey towards a much better documentation that this service needs and deserves. With the open source code and collaboration in a public repository, knowledge is not only shared but also documented. The importance while not immediately realized will manifest itself in many occasions down the road. Discussions and design/implementation choices explained and captured. No guidance or API documentation can do that.

And what it be if not the new and exciting possibilities. The new client will be simpler and "cleaner." Up-to-date with the modern times on the async side of things. API design refreshed and updated to reflect lessons learned over time. For example, one of the exciting changes coming to the new client is the [extensibility API](https://github.com/Azure/azure-service-bus-dotnet/issues/106). While it doesn't sound a lot, it brings a whole world of new opportunities into the client world with the OCP principle observed. Want to secure your messages using KeyVault service? Add [KeyVault plugin](https://github.com/Azure/azure-service-bus-dotnet-plugins) and have messages encrypted. Want to control message ID generation? You guessed it right. Want to add more customizations to the incoming/outgoing pipelines? Build your plugins and get that custom functionality you always wanted the client to have.

And if I managed to awake your curiosity, get the [client NuGet package](https://www.nuget.org/packages/microsoft.azure.servicebus) and go for it! Ready for more? Contribute some code. Find a bug and raise an issue. Be in charge of the client future and have fun.


[1]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2017/hello-microsoft.azure.aervicebus/00-title-3.PNG
[2]: https://weblogs.asp.net/sfeldman/hello-microsoft-azure-servicebus
[3]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2017/hello-microsoft.azure.aervicebus/00-tweet.PNG
