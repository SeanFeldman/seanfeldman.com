---
title: Updating Azure Functions Tools
slug: updating-azure-functions-tools
date: '2022-08-10T17:06:00'
updated: '2022-08-10T17:19:42.125413+00:00'
draft: false
tags:
- AzureFunctions
- VS.NET
- Rider
author: Sean Feldman
---
Azure Functions Tools is at the heart of providing local development for Azure Function. Whenever you use Visual Studio, Rider, VS Code, or anything else, you need it to be able to run your bits. For command line folks, the installation process is [outlined](https://github.com/Azure/azure-functions-core-tools#installing) in the tools repository. For Visual Studio (2022) and Rider, it is less evident as it depends on the tool. So, where am I heading with this? Right, the need to update the Azure Functions Tools.
Normally, VS and Rider do it automatically. Azure Functions Tools feed (https://functionscdn.azureedge.net/public/cli-feed-v4.json) stored at `%LocalAppData%\AzureFunctionsTools` has a JSON feed file, `feed-v.json`, that is periodically updated. This file points to all the necessary information, including the latest version for the version of the function (v4 in my case).
```
"v4": {
  "release": "4.20.0",
  "releaseQuality": "GA",
  "hidden": false
},
```
Release points at the Core Tools version
```
"coreTools": [
    {
      "OS": "Linux",
      "Architecture": "x64",
      "downloadLink": "https://functionscdn.azureedge.net/public/4.0.4704/Azure.Functions.Cli.linux-x64.4.0.4704.zip",
      //...
    },
```
When running your Functions project and noticing that the version is falling behind, there are a few things to check:
1. The feed file. It could be that the feed is stale.
2. The tooling in the IDE is not updating.
For #2, there's a difference between VS and Rider.
- Rider will check for a newer version of Azure Functions Tools each time a project is loaded\*
- VS will check for a newer version when a new Functions project is \*\*created\*\*
\\*Rider also allows inspecting the version and manually replacing it with another version by going through Settings --> Tools --> Azure --> Functions and configuring Azure Functions Tools location.
![Rider settings screenshot][1]
With VS, it's not really intuitive. If I work on the same project and do not add new triggers or Funcitons projects to the solution, it can be very confusing. Rider does a better job, no doubt.
\*Running the same project before and after adding an \_additional\_ Funcitons project just to update the tools.\*
Before:
![before][2]
After:
![after][3]
With this, the version of Tools can always be up-to-date.
[1]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2022/updating-azure-functions-tools/image.png
[2]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2022/updating-azure-functions-tools/image-1.png
[3]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2022/updating-azure-functions-tools/image-2.png
