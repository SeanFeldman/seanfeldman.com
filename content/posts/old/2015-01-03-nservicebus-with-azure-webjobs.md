---
title: NServiceBus with Azure WebJobs
slug: nservicebus-with-azure-webjobs
date: '2015-01-03T08:18:00'
updated: '2015-01-05T07:28:54.477565+00:00'
draft: false
author: Sean Feldman
---
## Azure WebSites and WebJobs
Azure WebSites have become a significant building component on Azure platform lately, with many features and tools built around it. WebJobs is one of the features, based on Kudu engine, that allows to run background tasks in Azure website. There's [plenty of information](http://azure.microsoft.com/en-us/documentation/articles/web-sites-create-web-jobs/) about Azure WebJobs and possibilities it opens for Azure WebSites. I'd like to highlight 2 interesting facts:
1. WebJobs aims to make developing, running, and scaling this easier
2. There is no additional cost to use Azure WebJobs
Scott Hanselman had a [very good post](http://www.hanselman.com/blog/IntroducingWindowsAzureWebJobs.aspx) on how he's using WebJobs to make development, running, and scaling easier.
Since Azure WebJobs are running under Azure WebSites, it is same VM(s) behind the scenes that both. Which results in no additional costs for running WebJobs. Nice side of this is is that WebJobs scale out with WebSite when later is scaled out from a single to multiple instances.
## NServiceBus
Where's [NServiceBus](http://particular.net/NServiceBus) in all of this? Great question. NServiceBus has [Azure transport support](http://docs.particular.net/nservicebus/windows-azure-transport). [Hosting NServiceBus in Azure](http://docs.particular.net/nservicebus/hosting-nservicebus-in-windows-azure) supports several scenarios:
1. Virtual Machines
2. Azure Websites
3. Cloud Services
4. Cloud Services - Shared Hosting (aka Dynamic Host)
1st, 3rd, and 4th scenarios allow you to run with with endpoints for front and back end. 2nd scenario does not. Or \*did not\* until Azure WebJobs.
## Azure WebJobs meet NServiceBus
WebJobs can be executed as continuous jobs without being triggered automatically as showed in vast majority of samples. Instead, WebJob `Host` can kick-off a long running task until it's cancelled (WebJob stopped or deleted). This can be used to self-host NServiceBus endpoint. NServiceBus takes out the manual and tedious work with low level queuing while allowing to dive into more complex scenarios for implementation. Not to mention the tooling that is available as a part of [Particular Platform](http://particular.net/service-platform).
Additional reasons are:
- Simple and fast deployment of Azure WebJobs (with or without WebSite)
- Ability to scale-out
- Low cost (website instances cover cost of WebJobs instances)
Note: it's worth mentioning that it doesn't cost a dime to run a free hosting plan of Azure WebSites. Combined with [free trial of NServiceBus](http://particular.net/platform-download-started) you get to develop, deploy, and run on Azure your application.
## Show me some code
Scenario I have decided to implement is fairly simple: [full duplex](http://docs.particular.net/nservicebus/full-duplex-sample). WebApp, front-end point, that send a `Ping` command to WebJob, back-end processing endpoint. WebJob in turn replies back with `Pong` command. At this point you can either skip to the [bits on GitHub](https://github.com/SeanFeldman/NServiceBus\_WebJob) or read some comments / steps that are not included in code. After all, code should be self explanatory, isn't it? :)
## Solution structure
`Contracts`: [Messages used for commands / events / replies](http://docs.particular.net/nservicebus/unobtrusive-mode-messages)
`Shared`: [Message conventions](http://docs.particular.net/nservicebus/unobtrusive-sample)
`WebApp`: Azure WebSite for front-end endpoint
`WebJob`: Azure WebJob for back-end endpoint
Starting point is `HomeController`, where we send a `Ping` command to back-end endpoint.

Later, within front-end endpoint, we're expecting to receive reply message `Pong`

Now back-end endpoint turn. First WebJob configuration

Trick with `Environment.GetEnvironmentVariable()` is to allow execution of WebJob locally yet point to real Azure Storage account credentials without committing those into repository. This is needed since WebJobs cannot be executed with local storage emulator. In order to run it locally, create an environment variable called '`AzureStorageQueueTransport.ConnectionString`' on your machine and assign it connection string to a storage account you've created. If you have MSDN subscription, use your [MSDN Azure benefits](http://azure.microsoft.com/en-us/pricing/member-offers/msdn-benefits). And if you're not, sign-up, use a free WebSite, and pay a cost of a coffee for storage transactions, which will be less than that if you don't run it 24x7.
Next is to kick off our self-hosted endpoint. `host.Call(typeof(Functions).GetMethod("Host"));`

When executed, through portal we can find this WebJob running as continuous job
![Back-end endpoint running as WebJob][1]
When drill in, you can see that each WebJob deployment is causing previous instance to stop, and new instance to spin up
![Instances over time][2]
Instance can be aborted, which will cause a new instance to start again. Note that we have a log parameter supplied by WebJob SDK. Unfortunately, it's very limited in its capacity, but the good news is that we'll be able to use NServiceBus built-in logging. Combined with [Azure preview portal](https://portal.azure.com/) and [Streaming Logs for Azure Websites](http://www.hanselman.com/blog/StreamingDiagnosticsTraceLoggingFromTheAzureCommandLinePlusGlimpse.aspx) it is possible to monitor logs on portal or inside Visual Studio.
![Host][3]
`Host` function is responsible to spin-up self-hosting for NServiceBus and run in infinitely until we receive request to cancel/stop.
I found preview portal very handy when working with diagnostics and WebJobs.
![diagnostics and WebJobs][4]
With self-hosted endpoint up and running, we can start wiring message handlers. `PingHandler` code receives `Ping` and replies with `Pong`.

Let's run it.
![Run it][5]
Next step to validate execution is to look at the logs. I chose to use portal
![Diagnostics][6]
Application logs reflect communication we had between endpoints
![Logs][7]
WebApp sending a `Ping`, which is processed by WebJob, that replies back with `Pong`.
Since audit was enabled, both messages are found in audit queue - standard NServiceBus behaviour
![Audit Queue][8]
## Summary
Two great technologies, Azure and NServiceBus, combined together allow some very interesting scenarios to be implemented. I see this as an extremely affordable option to enter cloud-based distributed application development and experiment without breaking the bank. [Next time][9] I'll take a slightly more complicated scenario that would involve long-running process.
[1]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2015/NSB\_WebJobs/WebJob01.PNG
[2]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2015/NSB\_WebJobs/WebJob02.PNG
[3]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2015/NSB\_WebJobs/WebJob03.PNG
[4]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2015/NSB\_WebJobs/Portal01.PNG
[5]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2015/NSB\_WebJobs/Run01.PNG
[6]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2015/NSB\_WebJobs/Portal02.PNG
[7]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2015/NSB\_WebJobs/Run02.PNG
[8]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2015/NSB\_WebJobs/Queues01.PNG
[9]: http://bit.ly/nsb\_webjobs\_videostore
