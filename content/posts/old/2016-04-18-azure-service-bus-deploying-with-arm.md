---
title: Azure Service Bus - Deploying with ARM
slug: azure-service-bus-deploying-with-arm
date: '2016-04-18T05:21:00'
updated: '2016-04-18T05:22:25.038545+00:00'
draft: false
tags:
- ASB
author: Sean Feldman
---
Azure Service Bus still can't be created at the new portal, aka Ibiza. To create Azure Service Bus namespace and create entities, one has to do in manually at the old portal.  That wouldn't be so bad, but the lack of controlling what Resource Group the new namespace will belong to is a slight impediment for those that like their resources to be at the right places.

Luckily, there's an option to deploy ASB resources using ARM templates. And there are also [a few templates][1] to demonstrate how to do it. Unfortunately, those templates utilize `Switch-AzureMode` cmdlet that is no longer supported.

I've put together a sample to demonstrate how a template can be used and what are the commands that were needed to be executed to be able to deploy ASB resources using ARM template. 

First, like many others, I have more than a single subscription. To be able to deploy, I would need to specify what subscription to use for deployment. To select a subscription,  first, there's need to login to be able to access that information. This is achieved by using `Add-AzureRmAccount`. Notice the `AzureRm` part? That's what all the ARM commands are using nowadays. Could be subject to change. Just like `Switch-AzureMode`. A popup will show up to enter your Azure credentials.

![enter image description here][2]

Once you've been authenticated, the following will be presented

```csharp
Environment           : AzureCloud
Account               : your.email.address@domain.name
TenantId              : yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy
SubscriptionId        : xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
CurrentStorageAccount :
```
Next step is to select what subscription to use for deployment.

```csharp
Set-AzureRmContext -SubscriptionId xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```
Once the operational context is set, a new resource group can be created. You can skip this test if you already have a resource group to use.

```csharp
New-AzureRmResourceGroup -Name ASB-RG -Location "West US"
```
The convention of `-RG` might look redundant here.What can I say, old habits die hard. Either way, the output of the command is worth evaluation.

```csharp
ResourceGroupName : ASB-RG
Location          : westus
ProvisioningState : Succeeded
Tags              :
ResourceId        : /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/ASB-RG
```
1. Resource group name is `ASB-RG`
1. Location is West US region
1. Resource ID include subscription ID (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)

Final step is to create the needed resources (ASB namespace) and the entities. A few things to note. First, I'm deploying a template from a file and not a link, therefore `-TemplateFile` is used. Second, I'm giving deployment a name to read back the object, but it's really not necessary.

```csharp
New-AzureRmResourceGroupDeployment -Name my-deployment -ResourceGroupName ASB-RG -TemplateFile C:\templates\asb.json
```
It takes a while to provision a new namespace with the entities. Command will ask for the parameters we need to supply. It's possible to provide those via an external file, but I have skipped that part.

```csharp
cmdlet New-AzureRmResourceGroupDeployment at command pipeline position 1
Supply values for the following parameters:
(Type !? for Help.)
serviceBusNamespaceName: asb-rg-ns
serviceBusTopicName: asb-rg-topic
serviceBusSubscriptionName: asb-rg-sub
```
The output after a while looks like the following:

```csharp
DeploymentName          : my-deployment
ResourceGroupName       : ASB-RG
ProvisioningState       : Succeeded
Timestamp               : 2016-04-18 04:07:10
Mode                    : Incremental
TemplateLink            :
Parameters              :
                          Name             Type                       Value
                          ===============            =========================  ==========
                          serviceBusNamespaceName    String                     asb-rg-ns
                          serviceBusTopicName        String                     asb-rg-topic
                          serviceBusSubscriptionName String                     asb-rg-sub
                          serviceBusApiVersion       String                     2015-08-01
Outputs                 :
                          Name                          Type                       Value
                          ===============               =========================  ==========
                          namespaceConnectionString     String                     Endpoint=sb://asb-rg-ns.servicebus.windows.net/;SharedAccessKey
                          Name=RootManageSharedAccessKey;SharedAccessKey=<shared-access-key>
                          sharedAccessPolicyPrimaryKey  String                     <shared-access-primary-key>
DeploymentDebugLogLevel :
```
Details of asb.json can be found on the Azure documentation site with [detailed explanation][3] about parameters and options.

Should you wish to read more on deploying with ARM templates, [Using Azure PowerShell with Azure Resource Manager article][4] can provide good information.

Final result - `ASB-RG` resource group with `asb-rg-ns` messaging namespace.

![enter image description here][5]

And all the entities are in place as well.

![enter image description here][6]

Happy automated deployments!

[1]: https://azure.microsoft.com/en-us/documentation/articles/service-bus-arm-namespace-topic/#resources-to-deploy
[2]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2016/arm-01.png
[3]: https://azure.microsoft.com/en-us/documentation/articles/service-bus-arm-namespace-topic/#resources-to-deploy
[4]: https://azure.microsoft.com/en-us/documentation/articles/powershell-azure-resource-manager/
[5]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2016/arm-02.png
[6]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2016/arm-03.png
