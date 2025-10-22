---
title: Azure Functions
slug: azure-functions
date: '2016-04-04T05:58:00'
updated: '2016-04-04T05:59:10.621753+00:00'
draft: false
tags:
- Azure NServiceBus
author: Sean Feldman
---
When Azure Functions were announced at the Build2016 conference, I had to see what is it. Part of my curiosity was fueled by the same thought I had for WebJobs when those where announced first. To be more specific, an [alternative hosting environment for NServiceBus][1] in the Azure cloud. I'll share my personal conclusions in a little bit. However, first, what are Azure Functions?

Azure Functions are lightweight functions that are executed as a response to various events. An HTTP call, a new blob in Azure Storage, a new message on a storage queue, web hook invocation, etc. Sounds very similar to what WebJobs are doing. Indeed. It is because Functions *are* implemented on top of the WebJobs, running on top of [Kudu project][2]. Big difference between the two is how they are running. To run WebJobs, Azure Hosting Plan is required, executed 24/7. Azure Functions while can be executed on an existing Hosting Plan, can also run using Dynamic Hosting Plan. Runs the functions when those are triggered. Hence, the charge is based on the amount of memory function is using, times time it was running. 

To start with Azure functions, you can either start at https://functions.azure.com or through the portal. Documentation is available through https://azure.microsoft.com/en-us/services/functions/. [Core concepts][3] document is recommended to understand the basics. You'll find yourself playing with the actual bits easier after that.

Editing scripts is conveniently easy. Starting from pre-existing templates allows you to move fast. The feature is still in beta, so expect some rough edges. The editor is not bad, and it will only get better (IntelliSense should be coming soon, making editing experience much smoother). Integration of the editor with the streaming logs and sample data makes it easy to develop functions, experimenting and tweaking it fast. A neat feature is saving. Hitting CTRL-S will save your function.

![enter image description here][4]

Another thing to keep in mind - Azure Functions are implemented on top of WebJobs. Therefore, the SCM portal can be used to inspect, modify, and deploy Functions. When creating Functions, they are stored under `Function App`. In my case, `Function App` is called "function-sean". SCM portal is always https://function-app-name.scm.azurewebsites.net. Et voilà, we've got to the SCM portal under which Functions are running.

All Azure Functions run with a web application, so just like WebJobs they'll be found under site/wwwroot. Each Function will have a folder of its own. I've deployed two functions, hence two folders.
![enter image description here][5]

The official documentation talk about 2 files (function.json and run.csx), but there are additional files, which make the portal experience much richer.

![enter image description here][6]

TestOutput.json is the Output pane from the last execution at the portal.
![enter image description here][7]

Run.csx is the function itself. This is a C# script file. You can run .csx in Visual Studio 2015 Update 1 or later by opening [C# Interactive window][8]. It is a C# REPL, which also can load a file (`#load` command). I assume Visual Studio tooling will be updated soon to allow functions creation using a new project template.

Now back to hosting NServiceBus endpoints. Personally, I do not think Azure Functions would make a good host. Functions are intended to be a quick response to an event. They should not run all the time. When are triggered, should execute fast. The whole point is to save on resources utilization and pay per execution, and not to have something that is constantly running. Nature of NServiceBus would require loading, scanning for messages and handlers, hence making this a lengthy operation that is not suited for Functions. However, there is a use case where Functions can be extremely helpful: native integration. Native integration, while doesn't have a dependency on NServiceBus assemblies, does require transport assemblies. For example, when using Azure Service Bus, native integration would still have to reference Azure Service Bus client assembly to create and send a `BrokeredMessage` (see [example][9]). What if your integration is with an environment where ASB client library is not available or running on a platform/language that is not supported? This is where Azure Functions will be helpful. You could create a function that accepts a REST call via HTTP and convert raw JSON data into a native `BrokeredMessage`, pushing it on a queue and delivering to an endpoint.

Note: as of now, Azure Functions do not have support for ASB bindings (`in` and `out`), but it is coming [shortly][10]. Till then, this can be solved by referencing ASB NuGet package. Also, when creating Service Bus namespace, it is only using Notification Hub, not the messaging.

To sum it up, Azure Functions are a nice was to write economically safe event based triggers. They can scale-out (maximum of 4 concurrent executions with Dynamic Hosting Plan). With the pay-per-use model, it will make it attractive for certain scenarios where a full-fledged WebJob is just too much. 

[1]: https://weblogs.asp.net/sfeldman/nservicebus-with-azure-webjobs
[2]: https://github.com/projectkudu/kudu
[3]: https://azure.microsoft.com/en-us/documentation/articles/functions-reference/#core-concepts
[4]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2016/functions-01.png
[5]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2016/functions-02.png
[6]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2016/functions-03.png
[7]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2016/functions-04.png
[8]: https://github.com/dotnet/roslyn/wiki/Interactive-Window
[9]: http://docs.particular.net/samples/azure/native-integration-asb/
[10]: https://github.com/projectkudu/AzureFunctions/issues/273
