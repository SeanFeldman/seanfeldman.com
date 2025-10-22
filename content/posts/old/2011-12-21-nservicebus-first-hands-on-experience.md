---
title: NServiceBus - First Hands-On Experience
slug: nservicebus-first-hands-on-experience
date: '2011-12-21T03:28:00'
updated: '2011-12-21T03:28:00'
draft: false
author: Sean Feldman
---


I previously blogged on [afterthoughts](http://weblogs.asp.net/sfeldman/archive/2011/12/06/nservicebus-course-afterthought.aspx) on NServiceBus course. Equipped with new powerful knowledge I have approached on of the TODO tasks on my plate – decouple email notification service from the main web application.

First, the problem with the code that needed to be resolved. A customer is submitting content that has to be approved. Once content was submitted, an email is generated to notify approver. Approver either rejects or accepts the content, and notification is sent to the customer. Simple. Yet the original implementation has email notification logic residing within the application. What happens when application explodes or SMTP is down? Out of luck, sorry.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Windows-Live-Writer/NServiceBus-for-a-Newbie_BD80/image_thumb.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Windows-Live-Writer/NServiceBus-for-a-Newbie_BD80/image_2.png)

What should it be?

Personally, I think email notification service should be completely separated from the application. A bus should connect application and services and be the reliable mechanism for transportation of system messages (white envelope on the picture). In case email notification service is not available, messages are not lost, and email are not failing to reach their destination. Application can work with notification service being down or temporarily not available. Once service is available, messages are delivered to the service and it is service responsibility to fire emails to approver and customer. In case SMTP is not working, there’s a single point of failure, which is easy to troubleshoot. When using NServiceBus, queues are transactional, which means system messages are not removed until there’s a successful processing or message was retried defined number of times and moved to the failed queue. The biggest advantage of this approach, is the fact that no system message is lost, application is still running, and once service failure is addressed, system messages can be re-submitted (commands replayed). In worse case scenario, pull out messages manually and send a piece of paper with doves :) Or maybe not, but you got the drift.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Windows-Live-Writer/NServiceBus-for-a-Newbie_BD80/image_thumb_1.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Windows-Live-Writer/NServiceBus-for-a-Newbie_BD80/image_4.png)

## Weak Points

I have used NServiceBus 2.6 since 3.0 is still in Beta and it wouldn’t be wise to apply a beta in production… There are several points of weakness I run into:

1. Configurations – yacks. It is not complex, but tedious, and time wasting. I wish there’d be a tool not just to spit out a default configuration one time only, but a tool that actually allows to update and existing solution configuration (NServiceBus folks, here’s a feature request).
2. Multiple assembly references – to build the project I had to use different NuGet packages for NSB. I’d rather see a single NuGet package instead of multiple ones that are way too confusing. Once packages are in place, referencing multiple assemblies is awkward. Maybe next version this will be resoled.
3. Scattered documentation – documentation is there, but it’s not in a single spot. User group, release notes, NServiceBus site, StackOverflow. I guess this is a typical problem of any software project and not unique to NSB only.
4. User group – I just don’t like the interface and functionality of Yahoo user group. Not being able to receive notification for specific thread – drives me insane.

## 

SOA Done Right?

I am not sure if using NServiceBus will answer all the questions, but so far a lot of them got covered for me:

* Reliability
* Sub-systems decoupling
* Single Responsibility
* Single point of failure
* Versioning

Next step for myself would be to attend [Udi’s Advanced Distributed Systems Design course](http://www.nservicebus.com/AdvancedDistributedSystemsDesignCourse.aspx). Till then, more experiments with NSB.


