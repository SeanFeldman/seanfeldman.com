---
title: 'Azure Service Bus Message: Wanted Dead or Alive'
slug: azure-service-bus-message-wanted-dead-or-alive
date: '2017-04-07T06:27:00'
updated: '2017-04-07T06:29:50.972948+00:00'
draft: false
tags:
- AzureServiceBus
- NServiceBus
author: Sean Feldman
---
[![enter image description here][1]][2]
Running NServiceBus on Azure sometimes can be challenging. Take for example the Azure Service Bus transport. Every queue has additional queues that could contain either dead-lettered messages as a result of repeated failing processing of the poisonous messages or [unsuccessful transfer][3].
With multiple endpoints and their queues, you want to be able to monitor your system and know when things are going south. Particular Platform offers a monitoring tool, [Service Control][4] that is designed specifically for this purpose. Except it monitors endpoints for successfully processed and failed processing messages. Not quite the whole story for the ASB’s dead-letter queues, isn’t it?
Gladly, there’s an option of [Custom Checks][5]. These checks allow periodic execution of certain tests and can report results back to the mothership, SP dashboard.
To implement a custom check, Custom Checks NuGet package needs to be a referenced. For NServiceBus version 6, the package is `ServiceControl.Plugin.Nsb6.CustomChecks`. With the package in place, plugin requires ServiceControl input queue.
```
endpointConfiguration.CustomCheckPlugin("particular.servicecontrol");
```
And the check class itself:
```
public class MonitorDeadletterQueue : CustomCheck
{
    NamespaceManager namespaceManager;
    const string endpointName = "Samples.Azure.ServiceBus.Endpoint2";
    public MonitorDeadletterQueue() : base(id: $"Monitor {endpointName} DLQ", category: "Monitor DLQ", repeatAfter: TimeSpan.FromSeconds(10))
    {
        var connectionString = Environment.GetEnvironmentVariable("AzureServiceBus.ConnectionString");
        namespaceManager = NamespaceManager.CreateFromConnectionString(connectionString);
    }
    public override async Task<CheckResult> PerformCheck()
    {
        var queueDescription = await namespaceManager.GetQueueAsync(endpointName).ConfigureAwait(false);
        var messageCountDetails = queueDescription.MessageCountDetails;
        if (messageCountDetails.DeadLetterMessageCount > 0)
        {
            return CheckResult.Failed($"{messageCountDetails.DeadLetterMessageCount} dead-lettered messages in queue {endpointName}.");
        }
        return CheckResult.Pass;
    }
}
```
Once implemented, DLQ custom check periodically executes and provides the status. As long as there are no dead-lettered messages, there will be no alerts.
![enter image description here][6]
However, the moment there are dead-lettered messages, the dashboard will light up.
![enter image description here][7]
In this scenario, there was indeed a dead-lettered message in the queue.
![enter image description here][8]
Once inspected and addressed, the message can be removed from the DLQ, and SP will go back to normal.
![enter image description here][9]
Or at least till the next dead-lettered message 😊
Now you can track down those dead-lettered villains an pick up your bounty.
[1]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2017/asb-message-wanted-dead-or-alive/Wanted-Dead-or-Alive.jpg
[2]: https://weblogs.asp.net/sfeldman/azure-service-bus-message-wanted-dead-or-alive
[3]: https://weblogs.asp.net/sfeldman/the-secret-brotherhood-of-message-counts
[4]: https://particular.net/servicepulse
[5]: https://docs.particular.net/servicecontrol/plugins/custom-checks#periodic-check
[6]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2017/asb-message-wanted-dead-or-alive/passed.PNG
[7]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2017/asb-message-wanted-dead-or-alive/failed.PNG
[8]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2017/asb-message-wanted-dead-or-alive/dlq.PNG
[9]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2017/asb-message-wanted-dead-or-alive/cleared.PNG
