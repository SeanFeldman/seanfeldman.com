---
title: What you pay is what you get
slug: what-you-pay-is-what-you-get
date: '2018-07-03T17:20:00'
updated: '2018-07-09T15:55:09.021902+00:00'
draft: false
tags:
- AzureServiceBus
author: Sean Feldman
---
**Update 2017-07-09**: it appears none of the documentation was updated yet. ASB team is aware and it's [tracked here](https://github.com/Azure/azure-service-bus/issues/212).

"What you pay is what you get."
<br>This age-old wisdom applied to cloud services even more than anywhere. Take Azure Service Bus for example. The service offers 3 tiers that provide a different level of service and commitment.

 - Basic
 - Standard
 - Premium

I'm not going to focus on all there here. General information is available on the [pricing page](https://azure.microsoft.com/en-gb/pricing/details/service-bus/). What I am going to focus is on the distinction between the two most dominant tiers: Standard and Premium.

## Standard Tier

Standard tier is a very economical tier offering an unlimited number of namespaces for a monthly flat fee of about $10 USD. The tier offers all the standard features you'd get on Premium, minus the new features that are developed solely for Premium such as [IP filtering](https://blogs.msdn.microsoft.com/servicebus/2018/06/27/ip-filtering-for-event-hubs-and-service-bus/) or [Geo-DR](https://docs.microsoft.com/en-us/azure/service-bus-messaging/service-bus-geo-dr). It has neither throughput nor latency SLA. 

An immediate reaction could be "how come?". Well, if you think about it, it makes a lot of sense.
First, you're paying a fraction of what it costs to build, run, and maintain these features.
Second, you're able to create multiple namespaces and pay no extra besides the number of operations and connections. Though those namespaces are not coming from void, they are still provisioned on some hardware, consuming CPU, memory, bandwidth, and storage. So someone has to pay for it. As we all know, there are no free lunches. So you pay for it. You pay in SLA and performance. First, you cannot get a promised message throughput or latency. You're in a shared environment, and when resources under stress, you'll be throttled. Yes, that [`ServerBusyException`](https://docs.microsoft.com/en-us/dotnet/api/microsoft.azure.servicebus.serverbusyexception?view=azure-dotnet) can and will be thrown at you.

<center>
![enter image description here][1]<br>
<div>Namespace provisioning on Standard tier</div></center>

"This is bad" you must be thinking. How can I run my production on a standard tier with no proper SLA, throttling, and all these issues? Let me pose a different question - would you run your mission-critical system on a resource that is shared and not promised 100% of the time? Most likely not. So what's the answer? Premium tier.

## Premium Tier

[Premium tier](https://docs.microsoft.com/en-us/azure/service-bus-messaging/service-bus-premium-messaging) was explicitly designed to provide dedicated resources. It provides more predictable performance through higher throughput and lower latency. It does not suffer from the "noisy neighbor" problem affecting Standard tier. It provides an ability to scale workload up and down through a number of Messaging Units (MUs) depending on the scale you required. Moreover, it's designed to support your production-grade systems. Not to mention that it can carry around messages larger than 256KB. One megabyte to be precise.

<center>
![enter image description here][2]<br>
<div>Experimenting with sends</div></center>

"It's way too expensive" is what I always here as a first reaction after people read up on the [Premium tier cost](https://azure.microsoft.com/en-gb/pricing/details/service-bus/) and play with [Azure calculator](https://azure.microsoft.com/en-ca/pricing/calculator/). While it's not a cheap offer, you have to ask yourself a simple question: how important for your business to have this service up and running, performing predictably? If it's not a must, then stick with Standard. Alternatively, perhaps look at even cheaper service such as [Storage Queues](https://docs.microsoft.com/en-us/azure/storage/queues/storage-queues-introduction). Otherwise, think for a second time invested into handling throttling, noisy neighbors, throughput limitations, and decide if the Premium is worth the investment rather than spending that on your custom code to overcome all those headaches.

I'm okay to pay that for production, but there are testing and QA namespaces. That will quickly add up.
No one said you have to use Premium for absolutely everything. You can run your lower environments on standard tier while benefitting from the Premium for production. Also, in case you've missed the news, which was not that hard to miss, **the charge for Premium is no longer per day, but per hour**. You could try sping up a Premium namespace for testing, and tear it down a few minutes later. That is much more economical and in the best spirit of cloud charging.

## Epilogue

As developers we often want services to be as cheap as possible, if not free at all. We want to charge for our work and expect to get the best from what we consume. Azure Service Bus offers several options. Two out of those are definite candidates for different types of workloads. With per-hour billing, Premium is becoming even more affordable. Dynamic resource provisioning is an excellent approach for environments that are not required 24/7. With ARM templates, Azure CLI, and other tools available nowadays, statically provisioned resources are not required. Tests, especially automated, can take advantage of spinning up and tearing down resources such as Service Bus namespaces. At the rate of ~90 cents per MU per hour, testing on Premium tier is by far a much better option to have an idea what production will look like.

When it comes to production, understand your needs. If you need a short ride and not bothered with a bumpy ride, a beaten cab will do. If you're in for a more extended trip and want the peace of mind and adequate service, a limo is likely a better option. 


[1]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2018/asb-what-you-pay/asb.containers.namespaces.jpg
[2]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2018/asb-what-you-pay/sends.JPG
