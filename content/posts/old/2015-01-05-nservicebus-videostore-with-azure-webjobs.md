---
title: NServiceBus VideoStore with Azure WebJobs
slug: nservicebus-videostore-with-azure-webjobs
date: '2015-01-05T07:27:00'
updated: '2015-01-07T05:33:12.031093+00:00'
draft: false
author: Sean Feldman
---
In my [previous post][1] I have demonstrated how NServiceBus endpoint can be hosted in a WebJob. To extend that concept and demonstrate that you could host multiple endpoints, I have taken NServiceBus [VideoStore sample][2] application and converted non-web endpoints to be hosted int WebJobs. Bits, as usual, are on [GitHub][3].


## What VideoStore sample does?

This sample demonstrates an online ordering system for purchasing videos. Behind the scenes, there are a few endpoints. Sales endpoint is executing a long running process (aka [`Saga` in NServiceBus][4] world) called `ProcessOrderSaga`. This saga is executed for each submitted order. A few other endpoints (`Content Management`, `Customer Relations`, and `Operations`) are involved as well, using commands and [`Pub-Sub` mechanism][5].

`Sales` endpoint also implements "Buyers Remorse"  option, where an order can be cancelled within certain period of time after it has been posted.

## WebJob naming

When in Rome do as the Romans do. So is with WebJobs.

WebJobs are strict about names - letters and dashes only. Therefore all endpoint names in this sample where deployed with names updated to include dash `-` instead of dot `.` (Ex: `VideoStore.Sales` endpoint would become a `VideoStore-Sales` WebJob).
<table>
<tr>
<td><img src="https://aspblogs.blob.core.windows.net:443/media/sfeldman/2015/NSB_WebJobs_VideoStore/name1.PNG" width="200"/></td>
<td>=&gt;</td>
<td><img src="https://aspblogs.blob.core.windows.net:443/media/sfeldman/2015/NSB_WebJobs_VideoStore/name2.PNG" width="200"/></td>
</tr>
</table>

### Deployment 

WebJobs require a WebSite to be published under. There are two options to deploy:
1. Deploy as a WebJob (used this option for the post)
2. Link and deploy with a web project

MSDN has [documentation][8] on both methods. Worth mentioning that both options play nicely with automation and CI.

## All endpoints Deployed

Once all endpoints are deployed (4 of them), quick validation can be performed to ensure all webjobs are well and running.

![All endpoints][9]

Drilling into any endpoint should result in a running host. This is continuous WebJobs in action and it's used to self-host each endpoint.

![Endpoint host running][10]

Go ahead, toggle `Output` to see if endpoint has successfully loaded. If it didn't, then it would be the right time for logging.

![Endpoint is ready][11]

## Running

Great, endpoints are loaded and running.

First scenario is to submit an order and wait over 20 seconds to see order going through cycle of submitted, and finally completed.

![Success][12]

Second scenario is to cancel an order within 20 seconds after submission to void it.

![Cancelation][13]

## Testing and Debugging 

You can [test and debug][14] your endpoints hosted in WebJobs using Visual Studio tools for Azure. It is straight forward and easy. You can also run it all locally, though for WebJobs you will need to point to the real Azure Storage accounts since emulator won't be enough.

### Steps for debugging are

**Step 1** - Access Azure services through Visual Studio `Server Explorer` windows (`CTRL-ALT-S`), navigate to the WebSite hosting WebJobs, and select a WebJob for debugging.

![Server Explorer][15]

**Step 2** - Attach Debugger

![Server Explorer][16]

**Step 3** - Step through code 
Visual Studio will stop at the break points set in WebJob. I have selected 7 videos in my order, so 7 links should show up in completed order on the client side.

![Server Explorer][17]

**Step 4** - Results validation

![Server Explorer][18]

## Everything that ends well

NServiceBus hosting on Azure is extremely powerful and flexible. You can pick and choose based on your needs and budgets. IMO, WebJobs are great to run quick NServiceBus prototypes on Azure, eventually converting them into Cloud Services, with or without [`Dynamic Host`][19]. Take the sample for a spin, and share your thoughts/comments.


  [1]:http://bit.ly/nsb_webjob
  [2]:https://github.com/Particular/NServiceBus.Azure.Samples
  [3]:https://github.com/SeanFeldman/NServiceBus_VideoStore
  [4]:http://docs.particular.net/nservicebus/sagas-in-nservicebus
  [5]:http://docs.particular.net/nservicebus/how-pub-sub-works
  [6]:https://aspblogs.blob.core.windows.net:443/media/sfeldman/2015/NSB_WebJobs_VideoStore/name1.PNG
  [7]:https://aspblogs.blob.core.windows.net:443/media/sfeldman/2015/NSB_WebJobs_VideoStore/name2.PNG
[8]: http://azure.microsoft.com/en-us/documentation/articles/websites-dotnet-deploy-webjobs/
[9]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2015/NSB_WebJobs_VideoStore/endpoints1.PNG
[10]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2015/NSB_WebJobs_VideoStore/endpoints2.PNG
[11]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2015/NSB_WebJobs_VideoStore/endpoints3.PNG
[12]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2015/NSB_WebJobs_VideoStore/execution-success.PNG
[13]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2015/NSB_WebJobs_VideoStore/execution-cancelling.PNG
[14]: http://azure.microsoft.com/en-us/documentation/articles/websites-webjobs-resources/#debug
[15]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2015/NSB_WebJobs_VideoStore/debug1.PNG
[16]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2015/NSB_WebJobs_VideoStore/debug2.PNG
[17]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2015/NSB_WebJobs_VideoStore/debug3.PNG
[18]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2015/NSB_WebJobs_VideoStore/debug4.PNG
[19]: http://docs.particular.net/nservicebus/shared-hosting-nservicebus-in-windows-azure-cloud-services
