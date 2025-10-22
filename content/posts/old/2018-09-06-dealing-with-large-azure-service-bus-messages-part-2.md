---
title: Dealing with large Azure Service Bus messages (part 2)
slug: dealing-with-large-azure-service-bus-messages-part-2
date: '2018-09-06T21:33:12.030677+00:00'
updated: '2018-09-06T21:33:11.952558+00:00'
draft: false
tags:
- Azure
- AzureServiceBus
author: Sean Feldman
---
This is a follow-up post discussing [how to deal with large messages](https://weblogs.asp.net/sfeldman/dealing-with-large-azure-service-bus-messages-part-1).
This time, I'm looking at [implementing Claim Check pattern](https://www.serverless360.com/blog/deal-with-large-service-bus-messages-using-claim-check-pattern) in a simple manner, using Azure Storage Queues, which is powering Azure Service Bus  [ServiceBus.AttachmentPlugin](https://www.nuget.org/packages/ServiceBus.AttachmentPlugin/) implementation.
