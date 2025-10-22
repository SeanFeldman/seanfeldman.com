---
title: Azure Service Bus - Number of Messages in a Single Transaction
slug: azure-service-bus-number-of-messages-in-a-single-transaction
date: '2016-03-18T05:45:00'
updated: '2016-03-18T05:14:09.197892+00:00'
draft: false
author: Sean Feldman
---
Azure Service Bus will not accept a transaction with more than a 100 messages. Not even if you send a batch. It is still a subject to the maximum 100 messages. If you try to send more, the exception "Cannot send more than 100 messages in a single transaction." will be upon you. 

This limit is not documented, so keep that in mind :)
