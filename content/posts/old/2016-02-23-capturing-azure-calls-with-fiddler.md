---
title: Capturing Azure calls with Fiddler
slug: capturing-azure-calls-with-fiddler
date: '2016-02-23T07:50:21.291314+00:00'
updated: '2016-02-23T07:50:21.210220+00:00'
draft: false
author: Sean Feldman
---
When working with Azure Service Bus or Storage Queues, Fiddler help in troubleshooting errors that could happen while talking to the remote service. Particularly useful when there's a mismatch between .NET client library that wraps RESTful API and remote service. Using Fiddler, you can trace the traffic going back and forth. Communication happens over HTTPS and sometimes Fiddler can refuse to show the values. When that happens, you no longer troubleshoot your Azure Service usage, but Fiddler configuration. Luckily, the fix as easy as resetting certificates used by Fiddler.
1. Tools > Fiddler Options.
1. Select HTTPS.
1. Generate certificates using CertEnroll engine.
1. Under Actions, select `Reset Certificates`.
Once all popups with prompts are accepted (press OK), you can see the traffic to Azure services back again.
![enter image description here][1]
[1]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2016/fiddler.png
