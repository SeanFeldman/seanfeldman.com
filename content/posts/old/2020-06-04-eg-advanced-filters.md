---
title: Event Grid advanced filters and value pooling
slug: eg-advanced-filters
date: '2020-06-04T05:16:56.022719'
updated: '2020-06-04T05:16:56.007088+00:00'
draft: false
tags:
- EventGrid
author: Sean Feldman
---
![filter][1]

Event Grid subscriptions filtering offers advanced filtering that allows data payload attributes filtering. Or filtering on the payload. This is a feature you cannot have with Azure Service Bus, for example. If you'd like to achieve the same functionality with Service Bus, you'd need to promote data from the payload into the headers. But back to Event Grid.

There is a maximum of 5 advanced filters per subscription. This might seem not much, but it's actually quite a lot. Advanced filtered are evaluated using AND logic among themselves. Within each advanced filter, the evaluation of multiple values is done using OR logic. Except there's a caveat. The documentation is outdated and the portal does not reflect the real power of these filters - the number of values advanced filters can evaluate are not [restricted to 5](https://docs.microsoft.com/en-us/azure/event-grid/event-filtering#limitations) values per filter. Rather, the <strong>number</strong> of those values is a pool shared by all 5 advanced filters.

![portal][2]

This means a single advanced filter can have up to 25 values if there are no other advanced filters on the subscription. Unfortunately, the only way to accomplish that today is to use ARM template or the management SDK to provision subscriptions with pulled values for advanced filters. The service team will update both the portal and the documentation. Until then, it's another hidden gem of Azure.

![pooled values][3]


[1]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2020/eg-advanced-filters/filter.jpg
[2]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2020/eg-advanced-filters/bug.jpg
[3]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2020/eg-advanced-filters/pooled.filters.jpg
