---
title: Dynamic WCF Proxy
slug: dynamic-wcf-proxy
date: '2009-09-23T01:22:00'
updated: '2009-09-23T01:22:00'
draft: false
tags:
- .NET
author: Sean Feldman
---


Our new system is entirely based of services (SOA solution). From the day one we had an issue with Visual Studio auto-magically generated proxies and management of those as system grew. Solution at that time was to create clients of the services dynamically, but the knowledge of WCF we had was a minimal. Now, 6+ months later, we finally getting to the point where I am comfortable and pleased with the solution. The interesting part is that WCF had that option all the time, we were not just educated enough to see it. Now we are.

The solution is to leverage *ChannelFactory* provided by WCF and create a client proxy from an end point defined in configuration file. Let me show the process from the client perspective:

 
```
var channel = new ChannelFactory<IWcfAppenderService>("WcfAppenderServiceEP").CreateChannel();
```

*channel* is our proxy. Reading carefully [Programming WCF Services](http://www.amazon.ca/Programming-WCF-Services-Juval-Lowy/dp/0596521308) book from Yuval Lowy (page 48), it is clear that a channel has to be closed, regardless of the state it’s found in after invocation (faulted or not).

```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: white; width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;"><span style="color: rgb(0, 0, 255);">using</span>(channel <span style="color: rgb(0, 0, 255);">as</span> IDisposable)</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: rgb(244, 244, 244); width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">          channel.Append(loggingEventDataDto);</pre>
```

.NET *using* statement does the work.

This is it. To simplify the whole thing, we could intercept method calls on channel with a transparent proxy of ours and wrap with *using* statements – that way a user does not have to remember to do it each time.

Configuration file for a client would contain the minimal required information:

```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: white; width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;"><span style="color: rgb(0, 0, 255);">&lt;</span><span style="color: rgb(128, 0, 0);">system.serviceModel</span><span style="color: rgb(0, 0, 255);">&gt;</span></pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: rgb(244, 244, 244); width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">  <span style="color: rgb(0, 0, 255);">&lt;</span><span style="color: rgb(128, 0, 0);">client</span><span style="color: rgb(0, 0, 255);">&gt;</span></pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: white; width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">    <span style="color: rgb(0, 0, 255);">&lt;</span><span style="color: rgb(128, 0, 0);">endpoint</span> <span style="color: rgb(255, 0, 0);">address</span><span style="color: rgb(0, 0, 255);">="http://localhost:4268/WcfAppenderService.svc"</span></pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: rgb(244, 244, 244); width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">        <span style="color: rgb(255, 0, 0);">binding</span><span style="color: rgb(0, 0, 255);">="wsHttpBinding"</span> </pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: white; width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">        <span style="color: rgb(255, 0, 0);">contract</span><span style="color: rgb(0, 0, 255);">="WcfAppender.Contracts.IWcfAppenderService"</span> </pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: rgb(244, 244, 244); width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">        <span style="color: rgb(255, 0, 0);">name</span><span style="color: rgb(0, 0, 255);">="WcfAppenderServiceEP"</span><span style="color: rgb(0, 0, 255);">&gt;</span></pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: white; width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">    <span style="color: rgb(0, 0, 255);">&lt;/</span><span style="color: rgb(128, 0, 0);">endpoint</span><span style="color: rgb(0, 0, 255);">&gt;</span></pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: rgb(244, 244, 244); width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">  <span style="color: rgb(0, 0, 255);">&lt;/</span><span style="color: rgb(128, 0, 0);">client</span><span style="color: rgb(0, 0, 255);">&gt;</span></pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: white; width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;"><span style="color: rgb(0, 0, 255);">&lt;/</span><span style="color: rgb(128, 0, 0);">system.serviceModel</span><span style="color: rgb(0, 0, 255);">&gt;</span></pre>
```

And the last missing part – contracts. A shared assembly with contracts would define all the service and data contracts. This is the only coupling between client and the server, which is logical, because contracts are coupling. [![image](http://weblogs.asp.net/blogs/sfeldman/image_thumb_4B012D64.png "image")](http://weblogs.asp.net/blogs/sfeldman/image_000B2BE4.png)

I am not done with my WCF adventures, but I can definitely point to a great book by Yuval Lowy as a reference for WCF.


