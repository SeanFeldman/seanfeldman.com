---
title: ServiceBus Explorer tool
slug: servicebus-explorer-tool
date: '2016-03-04T07:42:00'
updated: '2016-03-04T07:43:09.942894+00:00'
draft: false
author: Sean Feldman
---
Tooling is an important part of the development experience. No matter how good a service you're using is, if there are no decent tools, you always have that disgruntled feeling about the entire experience. When developing against hosted services, tools are either coming from the service provider or a third party. 

For Azure Service Bus current options are somewhat limited. There are no tools provided by the ASB team itself. Hopefully, that will change one day. There are options such as Cerebrata Azure Management Studio. While the tool is excellent, specifically for Azure Service Bus it feels same as dining at a fancy restaurant with utensils where a knife is a Swiss army knife. Perfect for many things, but not so much for a very particular usage.

And that's where ServiceBus Explorer comes to the rescue. Build solely for the purpose of managing and working with Service Bus entities (queues, topics, event hubs, notification hubs, and relays). Being able to drill into nested entities, such as rules on subscriptions, look at your message properties (standard and custom), peek messages, save messages, run analytics, etc. Another interesting fact about ServiceBus Explorer is that [it's an OSS](https://github.com/paolosalvatori/ServiceBusExplorer). Whenever you find an issue and would like to [fix it](https://github.com/paolosalvatori/ServiceBusExplorer/issues/11), you can alway do so. Paolo Salvatori, the author of SBExplorer, is accepting PRs :)

![enter image description here][1]

If you do any work that requires Azure Service Bus, this is the tool you have to have in your toolbox to get the work done. If you haven't used it yet, do it.
The future you will thank you.


[1]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2016/service-bus-explorer.png
