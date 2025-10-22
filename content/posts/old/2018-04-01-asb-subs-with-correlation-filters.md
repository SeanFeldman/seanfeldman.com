---
title: Azure Service Bus Subscriptions with Correlation Filters
slug: asb-subs-with-correlation-filters
date: '2018-04-01T15:56:33.546090+00:00'
updated: '2018-04-01T15:56:33.514822+00:00'
draft: false
tags:
- AzureServiceBus
author: Sean Feldman
---
<center>
[![filter][1]][2]
</center>

Azure Service Bus pub/sub is implemented using topics and subscriptions. Messages are published to topics and copied over to subscription queues with matching criteria. Criteria are declared using Rules. Each rule has a Filter. Filters help the broker decide if a message sent to a topic will be copied over to a subscription or not. Let’s dive into the world of filters to understand how they work.
There are three types of filters supported by the broker:

 1. Boolean filters
 2. SQL filters
 3. Correlation filters

## Boolean filters

These filters (`TrueFilter` and `FalseFilter`) are not the most sophisticated. They are literally "catch-all" or "catch nothing" options. The `TrueFilter` is the default when nothing else is defined. It’s handy when implementing a wiretap to analyze all messages flowing through a topic.

## SQL filters

Just as the name indicates, SQL filters allow SQL language-based expressions to define criteria used to filter to identify messages that will be copied over to subscription. If you’re interested in the syntax, see [documentation]( https://docs.microsoft.com/en-us/azure/service-bus-messaging/service-bus-messaging-sql-filter). One thing I’ll mention is the idea of scope, which denotes the type of property; user-defined properties prefixed with `user` and system defined properties prefixed with `sys`.

With SQL filters it’s possible to create very complex rules for filtering messages out. Keep in mind that the more complex these rules are, the higher performance tall will be on the broker will have to apply these rules to every message. An example of a SQL rule:

```csharp
sys.Label LIKE '%bus%'` OR `user.tag IN ('queue', 'topic', 'subscription')
```
## Correlation filters

Unlike Boolean and SQL filters, this group is used to perform matching against one or more user and system properties in a very efficient way. Paraphrasing [official documentation]( https://docs.microsoft.com/en-us/dotnet/api/microsoft.servicebus.messaging.correlationfilter):

> The CorrelationFilter provides an efficient filter that deal with equality only. As such, the cost of evaluating filter expression is minimal and almost immediate w/o extra compute required

The only challenge with this filter, it’s not quite clear how to use it. There are two constructors

 1. Default (empty) constructor
 2. Constructor taking a single argument

The second constructor with a single `string` argument initiates a correlation filter to use the passed in value to be the criteria for `CorrelationId`. The first constructor is a mystery. Well, not quite. Empty correlation filter can be used to assign other system and user properties that can be used for filtering. For system properties `ContentType`, `MessageId`, `ReplyTo`, `ReplyToSessionId`, `SessionId`, `To`, and `CorrelationId` can be assigned values to filter on. What about user-defined properties? That’s nwhere it’s a little unclear if you follow the documentation, which hopefully will get updated soon.

To specify user-defined properties for correlation filter, a property `Properties` of type ` IDictionary <string, object>` is exposed. Keys for this dictionary are the user-defined properties to look up on messages. Values associated with keys are the values to correlate on. Here’s an example.

```csharp
var filter = new CorrelationFilter();
filter.Label = "blah";
filter.ReplyTo = "x";
filter.Properties["prop1"] = "abc";
filter.Properties["prop2"] = "xyz";
```
Created filter will have the following criteria:

```csharp
sys.ReplyTo = 'x' AND sys.Label = 'blah' AND prop1 = 'abc' AND prop2 = 'xyz'
```
And you’ve guessed it right. When correlating on multiple properties, logical AND will be used so that all properties have to have the expected values for the filter to be evaluated as truthy.

In case you wondered how user-defined properties are populated, here's an example:

```csharp
message.Properties["prop1"] = "abc";
```
## Conclusions

Filtering messages can be done in several ways. Evaluate what filter to create and don’t default to SQL filter just because it’s easier to create. If filters can be simple enough to be expressed with correlation, prefer `CorrelationFilter` over `SqlFilter`. And remember, no matter what filter is used, filters cannot evaluate message body, but you can always promote from message body to properties/headers.


[1]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2018/asb-filters/filter.png
[2]: https://weblogs.asp.net/sfeldman/%20%20%20asb-subs-with-correlation-filters
