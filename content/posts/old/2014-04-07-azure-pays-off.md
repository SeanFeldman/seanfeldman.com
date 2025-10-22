---
title: Azure Pays Off
slug: azure-pays-off
date: '2014-04-07T03:05:32'
updated: '2014-04-07T03:05:32'
draft: false
tags:
- Cloud
author: Sean Feldman
---


A year ago I have started looking and evaluating cloud options. AWS and Azure were two options. I have decided to go with Azure for a couple of reasons that are still valid today (even more than a year ago)

1. As an MSDN subscriber, I could leverage MSDN credits that are sufficient to learn
2. PaaS on Azure was very appealing while on AWS it seemed a little foreign and not as friendly as AWS`s IaaS offer (a year ago Azure`s IaaS was very poor, so for infrastructure purposes only I’d probably wouldn’t choose Azure back then)
3. Simplicity, or at least perception I had

As an MSDN subscriber you get a LOT. You get credits on Azure that you can use towards anything you want (PaaS, IaaS, developer services, etc.) You can run production on MSDN subscription, but you can learn. And learning is important. I would strongly recommend to go beyond a single MSDN subscription discount and get a Pay-as-you-Go subscription to test out things. You can read documentation, play with cost calculator, but nothing, I repeat NOTHING, will replace the actual usage where real people are hitting your service, storage and CDN transactions are happening, when you run your minimal viable product with scale out as needed, leveraging developer services. If you try to shave off that cost, you’ll never fully learn. After all, without errors there are no successes. If you try to minimize the risk to none, you better not get on cloud at all.

PaaS or SaaS? Or both? This is a question only you can answer. My answer to this is: it depends. Certain things will require IaaS, other things will require PaaS. And PaaS on Azure has changed over time. It used to be just Cloud Services with Web and Wroker roles and a very complex process of deployment. But now we also have Azure Web Sites (ironically AWS) that have simplified the process of deployment and introduced some great options such as continuous deployment from code repository, IIS always on, web sockets, web jobs, etc. Today, one can build a globally scaleable web application without resorting to complex Cloud Services (thanks to Traffic Manager that made AWS a first class citizen). For scenarios you’d like to have pure VMs, you can leverage Azure IaaS that has become even richer with recent announcements at Build 2014. Automate it, schedule it, scale it, do anything you want.

Azure is simple. Interface is simple. Powershell cmdlets are easy. Will it stay simple for long? [Azure new portal](http://portal.azure.com) is making an attempt to address growing complexity by making it visually aesthetic and pleasant, something to validate in future to come.

So did this investment pay off? Yes. On several fronts:

1. Application hosting cost – now we know what it cost us to run a web application X
2. Infrastructure / hosting cost reduction – no argument here, costs went significantly down
3. Scaling – we can scale out with ease (once proper architecture is implemented. Do not dream of taking your application “as-is” and have it in the cloud)
4. Less dependency on IT – IT now can concentrate on more important things than spinning up VMs or monitoring response time
5. Automation – this has been addressed so many times, and yet I’ll say this again, with Azure automation is so easy that it’s a sin not to take advantage of it. And once you’ve automated a process, you’ve documented it and ensured that others can understand “the magic”.

We’ve implemented PaaS with Cloud Services, Plain AWS, IaaS, and recently have completed a spike that involved all above with an alternative approach for Sitecore CMS (that in its core is not so cloud friendly). Preview is available at [http://ta-mcit.azurewebsites.net/](http://ta-mcit.azurewebsites.net/ "http://ta-mcit.azurewebsites.net/")  and hopefully launch to come soon. When that happens, I’ll brag a little more about how we did it.


