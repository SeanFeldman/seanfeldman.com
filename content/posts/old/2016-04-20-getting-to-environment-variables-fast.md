---
title: Getting to Environment Variables Fast
slug: getting-to-environment-variables-fast
date: '2016-04-20T05:38:00'
updated: '2016-04-20T05:48:08.674524+00:00'
draft: false
author: Sean Feldman
---
I tend to keep connection strings, security tokens, and other secrets in the environment variable. This is handy when you commit your code to a public repository and want to make sure that your storage account connection string is not shared worldwide. It's also convenient because all those variables can be accessed in almost any hosting environment (VM, Cloud Service, WebJob, Azure Function, you name it). The downside - getting to those environment variables fast to modify those.

Usually, I'd be doing Computer --> Properties --> Advanced System Properties to get where I need. When RDPed into a VM or a Cloud Service instance that's just slow. Luckily, there's a way to get to the same place much faster.

```
Win-R (to open a run command window)
sysdm.cpl ,3
```

And done. Works like a charm. No more clicks and navigates in a slow worker role instance.
Happy fast environment variables editing!
