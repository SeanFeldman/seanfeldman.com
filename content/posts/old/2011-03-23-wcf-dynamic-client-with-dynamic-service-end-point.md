---
title: WCF Dynamic Client with Dynamic Service End Point
slug: wcf-dynamic-client-with-dynamic-service-end-point
date: '2011-03-23T04:29:00'
updated: '2011-03-23T04:29:00'
draft: false
author: Sean Feldman
---


First reaction would be why?

Allow me present the problem: Application has regular WCF service and RESTful service implemented with ASP.NET MVC controller (we could implement RESTful service with WCF, but then the challenge would not exist…).

Invocation of RESTful service done with WebClient object requires requires URI. This URI is easy to store in appSettings of the configuration file. But then on the same client, to access WCF service, address is specified within the client endpoint configuration.

Solution is the following:

```

```
  1: <appSettings>

```
```
  2:     <add key="ServicesBaseAddress" value="http://localhost/Services/"/>

```
```
  3:     <add key="ServiceName" value="WCFService"/>

```
```
  4:     <add key="RESTServiceName" value="Controller/Action"/>

```
```
  5:   </appSettings>
```

```

WCF Client configuration:

```

```
  1: <client>

```
```
  2:   <endpoint name="WCFService" address="" binding="basicHttpBinding" bindingConfiguration="SomeService_Binding" contract="WcfBaseAddressSpike.Server.ISomeService">

```
```
  3: 	<identity>

```
```
  4: 	  <dns value="localhost"/>

```
```
  5: 	</identity>

```
```
  6:   </endpoint>

```
```
  7: </client>/
```

```

WCF dynamic client creation:

```
var uri = new Uri(new Uri(ConfigurationManager.AppSettings["ServicesBaseAddress"]), ConfigurationManager.AppSettings["ServiceName"]);
var channel = new ChannelFactory<ISomeService>("WCFService").CreateChannel(new EndpointAddress(uri));
var response = channel.Ping();
```

RESTful service invocation:

```
 var uri = new Uri(new Uri(ConfigurationManager.AppSettings["ServicesBaseAddress"]), ConfigurationManager.AppSettings["RESTServiceName"]);
 var response = new WebClient.DownloadString(uri);
```

Source files [Source files](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/WcfBaseAddressSpike_2A4A1B2E.zip)


