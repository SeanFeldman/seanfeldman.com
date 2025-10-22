---
title: Azure EventGrid testing with Azure Relay
slug: azure-eventgrid-testing-with-azure-relay
date: '2018-02-28T07:25:00'
updated: '2018-02-28T19:35:55.456951+00:00'
draft: false
tags:
- Azure
- EventGrid
author: Sean Feldman
---
Azure Service Bus can now integrate with Azure Event Grid. Great [news][1]! Currently, it's only possible with Azure Service Bus premium tier, but soon standard tier will get the ability as well. Also, at the moment of writing this post, there's no way to directly integrate EventGrid events with Azure Service Bus to post messages whenever there's an event coming from EventGrid.
Non the less, the ability to connect EventGrid to Azure Functions opens up scenarios such as message processing without long polling by simplifying events consumption. [An example][2] would be an Azure Function that would be triggered whenever there'a new message and no listeners are registered. The Function would retrieve the message and will be able to hibernate again. Until the next message shows up. No long polling, no additional cost. The only problem I find with this approach is testing. To test that logic for EventGrid is working, one has to create an Azure Function. For some integration testing, creating a function sounds a little of an overhead. Using services like [RequestBin][3] to inspect HTTP requests is not ideal either. This is where Azure Relay (WCF Relay) can help.
Azure Relay? Ok. "But WCF?". I'm not a big fan of WCF either, but in this case, it helps tremendously with integration testing w/o a need for an external resource or manually inspecting Azure Function invocation.
First, there's a hidden [EventGrid Relay listener][4] Azure sample gem. It is simple and brilliant. Once the Azure relay is created, the code executes a self-hosted WCF service to receive calls over HTTPS. Once that is in place, an EventGrid subscription can be created with a webhook URL pointing to the previously created Azure Relay. Whenever there's an EventGrid event (initial subscription request or an event fired by resource provider, requests will be relayed to the local machine. This way testing can be performed locally w/o a need for Azure Functions or additional external services for HTTP request interception.
Note a few issues with the sample:
1. The current implementation in the sample has a bug - when a SAS token is used for authentication and passed in as a query string (`?code=SASToken`), SAS token has to be URL encoded to ensure special characters are not stripped away. E.g. a plus sign (+), which can happen with base64 encoded SAS token, would need to become %2B. And so on.
2. Azure EventGrid registration event is `Microsoft.EventGrid.SubscriptionValidationEvent` and not `Microsoft.EventGrid/SubscriptionValidationEvent`.
For working sample, refer to the [following PR][5] until the repository is updated.
[1]: https://azure.microsoft.com/en-us/blog/azure-service-bus-now-integrates-with-azure-event-grid/
[2]: https://docs.microsoft.com/en-us/azure/service-bus-messaging/service-bus-to-event-grid-integration-example
[3]: https://requestb.in
[4]: https://github.com/Azure-Samples/event-grid-relay-listener/
[5]: https://github.com/Azure-Samples/event-grid-relay-listener/pull/2
