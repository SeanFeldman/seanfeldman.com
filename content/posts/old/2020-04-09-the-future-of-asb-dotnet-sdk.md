---
title: The future of Azure Service Bus .NET SDK
slug: the-future-of-asb-dotnet-sdk
date: '2020-04-09T04:35:00'
updated: '2020-04-15T04:20:14.027647+00:00'
draft: false
tags:
- AzureServiceBus
- AzureSDK
- .NET
author: Sean Feldman
---
<center>
![The Azure Service Bus SDK for .NET is one of the oldest Azure SDKs][1]
</center>

## The past and the current of the SDK

The Azure Service Bus SDK for .NET is one of the oldest Azure SDKs. Its first public appearance as a NuGet package [`WindowsAzure.ServiceBus`](https://www.nuget.org/packages/WindowsAzure.ServiceBus/0.5.0) goes back to 2011. Back then, it was for .NET Framework and closed source. The package had an excellent mileage and is still used on multiple projects even today. And then the .NET Core and Standard have landed. Times have changed, open-source has become much more mainstream and accepted. The Azure Service Bus .NET SDK has moved into the brand new world with a successor package, [`Microsoft.Azure.ServiceBus`](https://www.nuget.org/packages/Microsoft.Azure.ServiceBus/). Started in early 2017, it showed up, causing some havoc to the brownfield projects. These projects were forced to face a complete rewrite due to the nature of the disruptive changes introduced by the new package. Once the dust has settled, the old and the new SDK nomenclature has established, and slowly projects have embraced the new SDK. There was a balance in the Force.

"I felt a great disturbance in the Force"
―Obi-Wan Kenobi

They say change is the only constant. Yet again, it was time for the .NET Azure Service Bus SDK to change. This time the change was not about .NET Standard or open source. It was bigger than that. The SDK has joined a new family - Azure SDKs family. What family?

## Azure SDKs

A few words on the Azure SDKs first. In the past, various Azure service teams were responsible for the client SDKs. Those SDKs would be for .NET, Java, and other languages the teams could support. Not always consistent. Not very idiomatic, and not necessarily all the popular programming languages. A decision was taken to consolidate client SDKs developments with a single group, Azure SDK group, that would focus on the popular languages, building idiomatic client-side SDKs for the Azure services with a few goals: consistency, simplicity, best practices, and so forth. Most of the Azure services SDKs are request-response based over HTTP, and that's where the focus was spent first. Eventually, it was messaging services turn. While EventHubs SDK was first, the real complex SDK, Azure Service Bus, the first preview has landed. Lo and behold, [`Azure.Messaging.ServiceBus`](https://www.nuget.org/packages/Azure.Messaging.ServiceBus/7.0.0-preview.1) version 7.

## Excuse me?!

Yes. There's some explaining to be done.

First, the project has moved home. It's no longer https://github.com/Azure/azure-service-bus-dotnet, rather https://github.com/Azure/azure-sdk-for-net/. Well, rather https://github.com/Azure/azure-sdk-for-net/tree/master/sdk/servicebus as it's a mondo repository with roughtly 100 various .NET SDKs sharing the repo. Don't confuse it with the broker repository, https://github.com/Azure/azure-service-bus, which doesn't contain the source code for the Service Bus service. Instead, it's used as a public issue tracker for broker related issues. Not client SDK. Capiche? It's okay if you feel slighly confused. Microsoft is good at making things confusing. But also eventually sorting those out. Not a 100% track record, but it's decent.

Second, there were some executive decisions made to position the new-new SDK in the right place. 

Full disclaimer: I'm very critical of some of these decisions. Time will show wherever I was just an old man yelling on the kids to get off my lawn or actually predicted some of the challenges the .NET SDK for Service Bus will experience.

## Executive decisions

The package name. All the [new Azure SDKs](https://azure.github.io/azure-sdk/releases/latest/dotnet.html) follow the naming convention that prescribes `Azure` prefix. Hence the new package name, `Azure.Messaging.ServiceBus`. Argueably, this is a sane decision given that the previous package, `Microsoft.Azure.ServiceBus` is not dead. At least not yet.

The code base is a brand new code base. Or, simply put, it's a complete re-write. Do not expect to find a full feature parity. Not yet. There are going to be many breaking changes and I can sense the tention in the air. Especially for those who have already gone through a complete re-write in the last couple of years. Brace yourselves, you'll go through another one. On the positive note, some of these changes will be very welcomed. Support for `CancellationToken`s, safe batching, Memory<T> support, and some more of the .NET goodies. But enogh with the spoilers. More about that in my next post.

The version start from...7. WTF?! Well, yes. It's a brand new package. Entirely re-written code base. And it starts with version 7. Traditionally it would be version 1, but the decision described in this [GitHub issue](https://github.com/Azure/azure-sdk-for-net/issues/10959) is beyond my understanding and I will read it to the readers to decide wherever I was just arguing for the sake of the argument or there was a merit in staring the version from 1. As of today, the legacy package, `WindowsAzure.ServiceBus` is still on top, so the assumption that version will bring the new-new package up, at least for now, is not quite working. BTW, your'e welcome to chime in if like me your head is spinning from this decision. Or if you'd like to show some support for it 😉

## How do we call all these Service Bus SDKs?

Old, new, and new-new? No, that's confusing. Gen1, gen2, and gen3? That'd be great, but that's not how it started. The Azure SDK team has decided to call all previous implementation `Track 1`, covering `Microsoft.Azure.ServiceBus` with that name. The new `Azure.Messaging.ServiceBus` is naturally `Track 2`. Leaving `WindowsAzure.ServiceBus` the true developer enumerated name `Track 0` which I've coined at this point. In my future post, I'm going to refer to them as`Track 0` (`WindowsAzure.ServiceBus`), `Track 1` (`Microsoft.Azure.ServiceBus`), and `Track 2` (`Azure.Messaging.ServiceBus`).

## Summary

The king is not yet dead, but a successor is emerging. It will take some time till it becomes a viable replacement, but a preview is out and you can take it for a spin. Make sure to provide your feedback and engage with the Azure SDK team at https://github.com/Azure/azure-sdk-for-net/issues. 

In the next posts I'll be covering more of the new Service Bus SDK, some design changes, and the exciting changes coming to the Track 2 library.


[1]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2020/the-future-of-asb-dotnet-sdk/crystal-ball.jpg
