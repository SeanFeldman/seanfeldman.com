---
title: Manually Completing Service Bus Messages with Functions
slug: manually-completing-service-bus-messages-with-functions
date: '2022-09-06T06:27:00'
updated: '2022-09-06T06:33:10.572232+00:00'
draft: false
tags:
- AzureFunctions
- Azure
author: Sean Feldman
---
Message settlement with Azure Service Bus has undergone some changes over the past few iterations of the Service Bus SDK for .NET. In the latest SDK (Azure.Messaging.ServiceBus), the settlement is performed via the `ServiceBusReceivedMessage`. In the previous SDK, this was accomplished with the help of the `MessageReceiver` object.
Azure Functions In-Process SDK can disable message auto-completion by specifying `AutoComplete = false` on the `ServiceBusTrigger`. When auto-completion is disabled, the responsibility to complete (settle) the incoming message is on the function code. Except with the latest SDK, `MessageReceiver` is no longer an option. And while the equivalent, `ServiceBusReceiver`, seems to be the logical replacement, it is not. Instead, a particular type, `ServiceBusMessageActions`\*, must be injected and used to settle messages.
And what about Isolated Worker SDK? Well, not there yet. Hopefully, it [will be](https://github.com/Azure/azure-functions-dotnet-worker/issues/1008) soon.
\\* will require `Microsoft.Azure.WebJobs.Extensions.ServiceBus` NuGet package to be added
