---
title: Goodbye Azure Storage Emulator. Hello Azurite!
slug: hello-azurite
date: '2020-06-06T20:36:00'
updated: '2020-07-27T15:38:48.527234+00:00'
draft: false
tags:
- GitHub;
author: Sean Feldman
---
![hello Azurite][1]

## Why Azurite?

For a long time, I was using Storage Emulator to execute some verification tests for [ServiceBus.AttachmentPlugin](https://github.com/SeanFeldman/ServiceBus.AttachmentPlugin) project. And I'd continue using it if not a few inconveniences it had.

 - Needs to be installed. While it's not big of a deal, using something like PowerShell it can be download and installed swiftly. 
<br>

```
$msiPath = "$($env:USERPROFILE)\MicrosoftAzureStorageEmulator.msi"
        (New-Object Net.WebClient).DownloadFile('https://download.visualstudio.microsoft.com/download/pr/e9476781-1f65-40e4-b7fd-e6b49840c7de/7028682de076b2dbc1aa5f1e02ec420a/microsoftazurestorageemulator.msi', $msiPath)<br>
cmd /c start /wait msiexec /i $msiPath /quiet<br>
del $msiPath
```

 - Requires Microsoft SQL Server 2012 Express LocalDB instance
 - Has [no support for HTTPS](https://docs.microsoft.com/en-us/azure/storage/common/storage-use-emulator#authenticating-requests-against-the-storage-emulator)
 - Is not cross-platform

And for quite some time I was OK with these limitations. Until GitHub Actions knocked on the door.
I wanted to run the test suite and Windows runner on GitHub would have to have both Storage Emulator and SQL Server Express installed. That would mean increased time for the builds, which I wanted to reduce rather than expand. The second issue was running my CI/CD on Windows only. In my earlier post [Deploying an Azure WebJob with GitHub Actions](https://weblogs.asp.net/sfeldman/azure-webjob-with-github-action) I was able to run build and deploy using Linux runner to reduce the cost. I surely wanted to stay in that realm which would not be doable with the Storage Emulator.

## Azurite to the rescue

Fortunately, there's an OSS project that Microsoft/Azure supports now and that was Azurite. Not only that, it's now the first option [recommended by Microsoft](https://docs.microsoft.com/en-us/azure/storage/common/storage-use-azurite). And it surely looks like as if the investment is going into this tool rather than the Storage Emulator. Some of the benefits of this new tool are:

 - Install and run with NPM similar to .NET Core global tool (`npm install -g azurite`
 - Can run a single service only (Blobs or Queues)
 - Can run as a Docker container and the image is provided by Microsoft
 - Open-source with a GitHub issue tracker (I'll expand on the importance of that below)
 - Easy to purge (data stored in a folder that can be deleted to remove everything)
 - Has support for HTTPS and Oauth
 - Still supports `devstoreaccount1` credentials and `UseDevelopmentStorage=true` connection string
 - Works with Storage SDK v12
 - Plays well with [Storage Explorer](https://azure.microsoft.com/en-us/features/storage-explorer/)
 - Nice integration with VS Code (if you need that)

The tool met all of my requirements and even exceeded those. But be aware, not everything is flawless. There are a few differences between Storage Explorer and Azurite. The ones are worth noting are:

 1. Error messages may be different, while error status codes align.
 2. No support for Table Storage. **Update**: support will be added back and is [worked on][2].

While the first discrepancy is not as bad as you might think, after all, status codes matter more, the second limitation is substantial.  It means the tool cannot be used to verify Table Storage based code. At all. Now recall the benefit of being OSS and having an issue tracker? Well, there's an [issue to lobby for Table Storage support](https://github.com/Azure/Azurite/issues/428). As for now, the [official response is](https://github.com/Azure/Azurite/issues/253#issuecomment-524146020): 

> The Azure Storage Emulator is being deprecated in favour of Azurite V3. Till Aug 13, 2020, the Azure Storage Emulator will continue to be available for download via the standalone installer and via the Azure SDK and will continue to support the latest Storage REST service versions. New feature capabilities, however, will be available only in Azurite starting REST service version 2019-02-02. Azure Table will not be supported in Azurite. Instead, the CosmosDB emulator should be used for emulating Table access.

And it would almost work for my scenario, except CosmosSB emulator is not cross platform. I hope there's a plan to make it cross-platform. These days, with .NET Core and [.NET Core Global tools](https://docs.microsoft.com/en-us/dotnet/core/tools/global-tools) everything is possible.

## Build server woes

I'm using AppVeyor and had to find a way to get Azurite running in the background while the tests where running. 

For Azure DevOps, the answer was simple, provided on the [issue tracker](https://github.com/Azure/Azurite/issues/382). 
For AppVeyor I was able to use PowerShell cmdlet to run a background process using `Start-Process azurite-blob.cmd -PassThru`. Note the `.cmd`. It's important to specify file extension on Windows as there's also an extensionless variant that is a Bash script, which PowerShell will fail to execute.

But none of this worked with GitHub Actions (I was trying with the Windows runner rather than Linux). Thanks to Edward Thomson, he has [reminded](https://github.com/Azure/Azurite/issues/451#issuecomment-639398801) that there's a Linux version that just worked.

And now I can run the test suite with Azurite!

![Result in action][3]

<p><p><div style="height:50px"><br</p></p>


[1]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2020/hello-azurite/image-1.png
[2]: https://github.com/Azure/Azurite/issues/428#issuecomment-664213293
[3]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2020/hello-azurite/image.png
