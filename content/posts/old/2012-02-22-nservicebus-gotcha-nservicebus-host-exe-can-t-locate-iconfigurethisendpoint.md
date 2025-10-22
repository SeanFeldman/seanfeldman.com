---
title: NServiceBus Gotcha - NServiceBus.Host.exe Can’t Locate IConfigureThisEndpoint
slug: nservicebus-gotcha-nservicebus-host-exe-can-t-locate-iconfigurethisendpoint
date: '2012-02-22T00:59:00'
updated: '2012-02-22T00:59:00'
draft: false
tags:
- NServiceBus
author: Sean Feldman
---

> Unhandled Exception: System.InvalidOperationException: No endpoint onfiguration found in scanned assemblies. This usual ly happens when NServiceBus fails to load your assembly contaning IConfigureThisEndpoint. Try specifying the type explicitly in the NServiceBus.Host.exe.config using the appsetting key: EndpointConfigurationTypeScanned path: C:\SearchFeedingService\   
>    at NServiceBus.Host.Program.ValidateEndpoints(IEnumerable`1 endpointConfigurationTypes)   
>    at NServiceBus.Host.Program.GetEndpointConfigurationType()   
>    at NServiceBus.Host.Program.Main(String[] args)

First I googled [stackoverflow](http://stackoverflow.com/questions/6095043/the-dreaded-no-endpoint-configuration-found-in-scanned-assemblies-nservicebus). Handy, but was not my case as I had only one implementation of IConfigureThisEndpoint, same .NET version, and everything was packaged. Then I found [this post](http://frankmao.com/2010/10/08/my-nservicebus-demo/), which helped a lot – I had to explicitly tell NSB what type implements IConfigureThisEndpoint. Not sure why this was happening.

**Update:** The issue was a result of bad packaging… A newer version of StructureMap.dll was packaged (not the version expected by NSB). So the exception, as mentioned in other posts, is masquerading the real problem.


