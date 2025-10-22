---
title: Azure Service Bus with Managed Service Identity
slug: azure-service-bus-with-managed-service-identity
date: '2018-01-26T06:19:00'
updated: '2018-02-01T05:58:04.260770+00:00'
draft: false
tags:
- AzureServiceBus
- AAD
author: Sean Feldman
---
<center>
[![image][1]][2]
</center>

[Managed Server Identity (MSI)*](https://docs.microsoft.com/en-us/azure/active-directory/msi-overview) is a feature of Azure Active Directory (AAD) to allow applications in Azure authenticate to cloud services without managing credentials in your code. 

Integration with MSI presents an excellent opportunity to remove credentials from your code and no longer manage those pesky connections string. What's even better, no more SAS keys to refresh in case those are re-generated. Azure Service Bus documentation has a [quick tutorial](https://docs.microsoft.com/en-ca/azure/service-bus-messaging/service-bus-managed-service-identity) with a linked [sample](https://github.com/Azure/azure-service-bus/tree/master/samples/DotNet/Microsoft.ServiceBus.Messaging/ManagedServiceIdentity), which is not as detailed as I'd like it to be. So here's a more comprehensive walkthrough.

What's required?

1. Azure Service Bus namespace with a queue. The namespace has to be in US East, US East 2, or West Europe. These are currently the only supported regions. The queue can be upfront using a tool like ServiceBus Explorer or similar or created via code. The latter is only possible using the old client (WindowsAzure.ServiceBus) and not the new one (Microsoft.Azure.ServiceBus). 

2. Azure WebApp in any Azure region. You're in luck if it's one of those where ASB supports MSI preview. And if not, you can still proceed. Your messages will just travel a bit longer.

For the same of this tutorial, I'll use web application named `msi-asb-post` a namespace called `msi-asb-post` (FQDN `msi-asb-post.servicebus.windows.net`).

With all resources ready to go, next step is to configure the web application to use MSI and allow it to access Azure Service Bus namespace. 

MSI needs to be turned on for the web application under Managed service identity.

<center>![enter image description here][3]</center>

Allow web application to access Azure Service Bus namespace using MSI. Select Access control (IAM) under the namespace and add a new permission by clicking +Add. Add Permission screen will show up. Select "Owner" for the Role, leave "Assign access to" as-is, and for the third input box called "Select", type in the name of the web application (msi-asb-post is the name for my example). UI should find MSI identity for the web application and show it on the list. Select the name and click Save. At this point, App Service `msi-asb-post` has access to the Azure namespace `msi-asb-post`.

<center>![enter image description here][4]</center>

*Tip: you can verify if the right web application is selected by inspecting resource path that is trancated by hovering over.  
`/subscriptions/<subscription-id-guid>/resourcegroups/<resource-group-id>/providers/Microsoft.Web/sites/<web-app-name>`*

At this point, the code is ready to be executed. Do not to try it locally, as you'll have no AAD and an authentication exception will be thrown. Instead, deploy to the web application and run it here. You can connect your debugger to the web application if you'd like to step through.

Most noticeable few lines of code are the ones that instruct ASB client to retrieve SAS token from MSI:

```
var messagingFactorySettings = new MessagingFactorySettings
{
  TokenProvider = TokenProvider.CreateManagedServiceIdentityTokenProvider(ServiceAudience.ServiceBusAudience),
  TransportType = TransportType.Amqp
};
```

There's also a broker known issue that can be worked around with the following line of code until the issue is fixed.

```
messagingFactorySettings.AmqpTransportSettings.EnableLinkRedirect = false;
```

If you're using this code in your POC, subscribe to the [tracking issue](https://github.com/Azure/azure-service-bus/issues/136) to remove this workaround once it's fixed on the broker.

**Note**: it's a good and responsible practice to leave TODO with tracking issue. Do not leave a note for future w/o ability to follow up on something that can be tracked back later. Otherwise, the workaround is sealed and will make it into production.

Once executed, the following web page will show up.

<center>![enter image description here][5]</center>

1. FQDN to be used should be the namespace created
2. `msi-asb-post.servicebus.windows.net` (your namespace name would replace `msi-asb-post` part).
3. Queue name of the queue you've created earlier
4. `test` is the queue name I've chosen.
5. Data to send. This is going to be the payload of the outgoing message.
6. I'll be sending two messages. `123` for the first message and `Hello from sender` for the second message
7. Send button to send a single message
8. Receive button to receive a single message.
9. The expected output of message payload and it's sequence number (your sequence numbers will be different based on how many messages were sent to the queue).

With MSI you start preparing your applications for what's coming - credentials worry free deployments. Happy messaging!

\* *MSI is still in preview and not available for all services in all regions yet.*

**Update 2018-01-31**: as of now, the new client (Microsoft.Azure.ServiceBus) does not support MSI.

[1]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2018/msi-asb/00.private.jpg
[2]: https://weblogs.asp.net/sfeldman/azure-service-bus-with-managed-service-identity
[3]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2018/msi-asb/01.msi.webapp.png
[4]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2018/msi-asb/02.permissionpng.png
[5]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2018/msi-asb/03.execution.png
