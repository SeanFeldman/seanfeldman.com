---
title: Consuming ASMX Web Service With WCF
slug: consuming-asmx-web-service-with-wcf
date: '2009-10-02T06:23:00'
updated: '2009-10-02T06:23:00'
draft: false
tags:
- .NET
author: Sean Feldman
---


ASMX web services were a breakthrough when appeared on .NET platform. A lot of services were created to take advantage of web services technology.

Now, that WCF is replacing legacy web services, we still have a lot of legacy web services running and being used. Connecting to legacy web services from WCF can be achieved either by leveraging Visual Studio .NET auto-generated proxies, or by [creating dynamic channel](http://weblogs.asp.net/sfeldman/archive/2009/09/22/dynamic-wcf-proxy.aspx) I talked about before. Creating dynamic channel looks like a cleaner solution, but there are a few caveats:

1. Legacy web service does not always expose a known/published interface (quiet often just implementation and no contracts);

2. Configuration might be a little tweaky;

In order to overcome the 1st issue, we can “re-invent” the contract that a legacy web service “would” implement.

 
```
[XmlSerializerFormat]
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: rgb(244, 244, 244); width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">public interface ILegacyService</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: white; width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">{</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: rgb(244, 244, 244); width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">  [OperationContract]</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: white; width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">  Version GetVersion();</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: rgb(244, 244, 244); width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">}</pre>
```

Next we can generate a dynamic channel

```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: white; width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">var channel = <span style="color: rgb(0, 0, 255);">new</span> ChannelFactory&lt;ILegacyService&gt;().CreateChannel();</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: rgb(244, 244, 244); width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;"><span style="color: rgb(0, 0, 255);">using</span> (channel <span style="color: rgb(0, 0, 255);">as</span> IDisposable)</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: white; width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">  <span style="color: rgb(0, 0, 255);">return</span> channel.GetVersion();</pre>
```

Once we have channel – time to configure

```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: white; width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;"><span style="color: rgb(0, 0, 255);">&lt;</span><span style="color: rgb(128, 0, 0);">system.serviceModel</span><span style="color: rgb(0, 0, 255);">&gt;</span></pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: rgb(244, 244, 244); width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">  <span style="color: rgb(0, 0, 255);">&lt;</span><span style="color: rgb(128, 0, 0);">client</span><span style="color: rgb(0, 0, 255);">&gt;</span></pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: white; width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">    <span style="color: rgb(0, 0, 255);">&lt;</span><span style="color: rgb(128, 0, 0);">endpoint</span> <span style="color: rgb(255, 0, 0);">name</span><span style="color: rgb(0, 0, 255);">="SomeServiceEndPoint"</span></pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: rgb(244, 244, 244); width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">              <span style="color: rgb(255, 0, 0);">address</span><span style="color: rgb(0, 0, 255);">="http://some.where.com/LegacyService/LegacyService.asmx"</span></pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: white; width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">              <span style="color: rgb(255, 0, 0);">binding</span><span style="color: rgb(0, 0, 255);">="customBinding"</span></pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: rgb(244, 244, 244); width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">              <span style="color: rgb(255, 0, 0);">contract</span><span style="color: rgb(0, 0, 255);">="ILegacyService"</span></pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: white; width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">              <span style="color: rgb(255, 0, 0);">bindingConfiguration</span><span style="color: rgb(0, 0, 255);">="custom.binding.for.SomeService"</span><span style="color: rgb(0, 0, 255);">&gt;</span></pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: rgb(244, 244, 244); width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">    <span style="color: rgb(0, 0, 255);">&lt;/</span><span style="color: rgb(128, 0, 0);">endpoint</span><span style="color: rgb(0, 0, 255);">&gt;</span></pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: white; width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">  <span style="color: rgb(0, 0, 255);">&lt;/</span><span style="color: rgb(128, 0, 0);">client</span><span style="color: rgb(0, 0, 255);">&gt;</span></pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: rgb(244, 244, 244); width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">  <span style="color: rgb(0, 0, 255);">&lt;</span><span style="color: rgb(128, 0, 0);">bindings</span><span style="color: rgb(0, 0, 255);">&gt;</span></pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: white; width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">    <span style="color: rgb(0, 0, 255);">&lt;</span><span style="color: rgb(128, 0, 0);">customBinding</span><span style="color: rgb(0, 0, 255);">&gt;</span></pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: rgb(244, 244, 244); width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">      <span style="color: rgb(0, 0, 255);">&lt;</span><span style="color: rgb(128, 0, 0);">binding</span> <span style="color: rgb(255, 0, 0);">name</span><span style="color: rgb(0, 0, 255);">="custom.binding.for.SomeService"</span><span style="color: rgb(0, 0, 255);">&gt;</span></pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: white; width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">        <span style="color: rgb(0, 0, 255);">&lt;</span><span style="color: rgb(128, 0, 0);">textMessageEncoding</span> <span style="color: rgb(255, 0, 0);">messageVersion</span><span style="color: rgb(0, 0, 255);">="Soap12"</span> <span style="color: rgb(255, 0, 0);">writeEncoding</span><span style="color: rgb(0, 0, 255);">="utf-8"</span> <span style="color: rgb(0, 0, 255);">/&gt;</span></pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: rgb(244, 244, 244); width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">        <span style="color: rgb(0, 0, 255);">&lt;</span><span style="color: rgb(128, 0, 0);">httpTransport</span><span style="color: rgb(0, 0, 255);">/&gt;</span></pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: white; width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">      <span style="color: rgb(0, 0, 255);">&lt;/</span><span style="color: rgb(128, 0, 0);">binding</span><span style="color: rgb(0, 0, 255);">&gt;</span></pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: rgb(244, 244, 244); width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">    <span style="color: rgb(0, 0, 255);">&lt;/</span><span style="color: rgb(128, 0, 0);">customBinding</span><span style="color: rgb(0, 0, 255);">&gt;</span></pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: white; width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">  <span style="color: rgb(0, 0, 255);">&lt;/</span><span style="color: rgb(128, 0, 0);">bindings</span><span style="color: rgb(0, 0, 255);">&gt;</span></pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: rgb(244, 244, 244); width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">&nbsp;</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: white; width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;"><span style="color: rgb(0, 0, 255);">&lt;/</span><span style="color: rgb(128, 0, 0);">system.serviceModel</span><span style="color: rgb(0, 0, 255);">&gt;</span></pre>
```

One comment about ServiceContract attribute. When consuming a legacy web service, and it has a pre-defined namespace. Modification to “re-invented” service will include the required information (such as Namespace)

```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: white; width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">[XmlSerializerFormat]</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: rgb(244, 244, 244); width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">  [ServiceContract(Namespace = <a href="http://some.where.com/LegacyService" mce_href="http://some.where.com/LegacyService">http://some.where.com/LegacyService</a>)]</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: white; width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">  public interface ILegacyService </pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: rgb(244, 244, 244); width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">  {</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: white; width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">    [OperationContract]</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: rgb(244, 244, 244); width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">    Version GetVersion();</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; text-align: left; line-height: 12pt; background-color: white; width: 100%; font-family: 'Courier New',courier,monospace; direction: ltr; color: black; font-size: 8pt;">  }</pre>
```


