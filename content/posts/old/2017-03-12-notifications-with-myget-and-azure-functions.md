---
title: Notifications with MyGet and Azure Functions
slug: notifications-with-myget-and-azure-functions
date: '2017-03-12T23:09:00'
updated: '2017-03-12T23:19:36.843410+00:00'
draft: false
tags:
- Azure
- Functions
- NuGet
author: Sean Feldman
---
[![enter image description here][1]][2]
If you're doing .NET development, you're probably familiar with NuGet packages. You might have also heard about MyGet service that offers an excellent package management. But have you looked at the additional things MyGet can provide? In this post, I'll focus on one of those hidden gems - webhooks.
\*\*Scenario\*\*
Scenario to implement is a requirement to receive notification about pre-release package builds added to MyGet feed for a specific nuget package.
MyGet has support for webhooks per feed. These webhooks are available in several flavors, depending on your taste. These webhooks can be invoked for various events for the feeds you nuget have. Interested to know when a package is pushed/added/deleted/listed/pinned? No problem. Choose your method of notification and off you go. You're free to choose your flavor from Twilio, Slack, Microsoft Team, HipChat, Twitter, HTTP post and email. If you need the ingredients list, look no further than [MyGet documentation](http://docs.myget.org/docs/reference/webhooks).
In my scenario, I'd like to be notified about daily updates taking place on the feed I'm working with to know if there were changes to a specific package I'm interested in. I'm a lazy developer and opted into Azure Functions with plain HTTP Posts.
The first step is to provide MyGet webhook with the URL to post notifications to. If you don't have one, don't worry. I will get into how to address it later in the post. The second step is to specify Content-Type of the webhook. 'application/json' will do the job. Third and the last step is to select the event you're interested in. For the scenario I'm implementing, 'Package Added' is what I'm after.
![enter image description here][3]
Once webhook is configured, it can be tested. MyGet allows to "ping" webhook with a test dummy JSON payload to mimic an event that would trigger webhooks.
```
{"Identifier":"a835cebf-28e3-4f0a-9b2a-c163d18e281a","Username":"highcoconsulting",
 "When":"2017-03-12T20:03:22.9159969Z","PayloadType":"PingWebHookEventPayloadV1","Payload":{}}
```
There's only one problem. MyGet feed sends notifications for any package found in the feed. It doesn't differentiate between versions either. That makes a requirement a bit more challenging. In a scenario like this Azure Functions can help to implement custom logic required to narrow notifications down.
\*\*Azure Function\*\*
Azure Function could be just filtering out the calls by MyGet and forward the filtered results to your original webhook handler. Alternatively, it could do the notification as well. I'll leave this decision to the readers and just show how filtering could be implemented.
Create a function under "API & Webhooks" category (a generic webhook function). Since we've specified for MyGet to send data in JSON format, we can safely deserialize the payload into a dynamic object.
```
var jsonContent = await req.Content.ReadAsStringAsync().ConfigureAwait(false);
dynamic data = JsonConvert.DeserializeObject(jsonContent);
```
Next is to determine the event type and filter out anything that is not "package added" event.
```
if (data?.PayloadType != null && data.PayloadType == "PackageAddedWebHookEventPayloadV1")
```
Note that each MyGet webhook event has an exact payload type.
Next is to peek into payload to detect the package name. Remember, the scenario was only supposed to notify a specific package (let's assume it's called "PackageX").
```
if  (data?.Payload?.PackageIdentifier == "PackageX")
```
If the package identifier is right, then the version retrieval is what's next
```
if (IsPrereleasedVersion(data?.Payload?.PackageVersion))
```
In case the version is matching the criteria of a pre-released version, notification can take place. Et voilà!
Knock knock. Who's there? A notification!
![enter image description here][4]
[1]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2017/notifications-myget-azure-functions/head.PNG
[2]: https://weblogs.asp.net/sfeldman/notifications-with-myget-and-azure-functions
[3]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2017/notifications-myget-azure-functions/webhook.PNG
[4]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2017/notifications-myget-azure-functions/package.PNG
