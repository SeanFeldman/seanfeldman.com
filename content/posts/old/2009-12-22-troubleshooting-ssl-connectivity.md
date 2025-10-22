---
title: Troubleshooting SSL Connectivity
slug: troubleshooting-ssl-connectivity
date: '2009-12-22T15:02:00'
updated: '2009-12-22T15:02:00'
draft: false
author: Sean Feldman
---


While integrating two clients and working on two way authentication, I had to troubleshoot SSL connectivity. Configuration file was my best tool I could use. There are a couple of things I used, and probably there’s a lot more I am not aware of.

#### ServicePointManager

*ServicePointManager* helps especially when validating server certificate, by allowing to review what are the errors and make a decision either to proceed or not. This is achieved through *ServerCertificateValidationCallback* event.

As well, I used configuration file to tweak a few things:

```

checkCertificateName="false"
                 expect100Continue="true"/>
```

Same thing can be done through code (either on *ServicePointManager* directly, or on request object, ServicePoint property).

#### System.Diagnostics

Logging is an absolute must when you get an exception, and details of exception are not sufficient enough. Luckily, System.Net (and more nested namespaces) support [logging that can be enabled](http://msdn.microsoft.com/en-us/library/ty48b824.aspx) (which reminds me to look under my nose and not to re-invent a wheel). After enabling these logs, I could get detailed trace of SSL communication which helped me a lot. To enable logs:

```

```
<sources>
  <source name="System.Net" tracemode="includehex" maxdatasize="1024">
    <listeners>
      <add name="System.Net"/>
    </listeners>
  </source>
  <source name="System.Net.Sockets">
    <listeners>
      <add name="System.Net"/>
    </listeners>
  </source>
  <source name="System.Net.Cache">
    <listeners>
      <add name="System.Net"/>
    </listeners>
  </source>
</sources>
<switches>
  <add name="System.Net" value="Verbose"/>
  <add name="System.Net.Sockets" value="Verbose"/>
  <add name="System.Net.Cache" value="Verbose"/>
</switches>
<sharedListeners>
  <add name="System.Net"
       type="System.Diagnostics.TextWriterTraceListener"
       initializeData="network.log" />
</sharedListeners>
<trace autoflush="true"/>
```


```

Hopefully, this helps someone as it helped me.


