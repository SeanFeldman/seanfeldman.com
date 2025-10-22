---
title: Sending large messages without exposing the storage account
slug: sending-large-messages-wo-exposing-storage-account
date: '2017-09-18T04:54:00'
updated: '2017-09-22T16:06:08.596572+00:00'
draft: false
tags:
- AttachmentPlugin
author: Sean Feldman
---
[ServiceBus.AttachmentPlugin][1] is an Azure Service Bus plugin to help with messages exceeding the allowed maximum size. Sender would store the message body as a Azure Storage blob and receive would read blob content to re-hydrate the message body just before message is given to the consumer code. This assumes that both sender and receiver share the knowledge about Azure Storage account and both can access it. But what if that's not the case?

Occasionally, there's a need to send messages to a party that should not have access to the blob storage for attachments. For that, Azure Storage service supports blobs with SAS URIs. It enables blob retrieval without the need in storage account. Starting from version 1.1.0 of the ServiceBus.AttachmentPlugin, you can send messages w/o exposing storage account connection string. Receivers will only need to know and specify the message property used to identify blob [SAS URI][2].

```
new AzureStorageAttachmentConfiguration(storageConnectionString)
     .WithSasUri(messagePropertyToIdentifySasUri: "sender-provided-sas-uri-property-name");
```

Et voilà! Message is sent without storage being exposed. 
![ASB message][3]

where "mySasUriProperty" is http://&lt;storage&gt;/attachments/3bfe3abe-8a04-4827-bb6b-f90e1ca87bfa?sv=2017-04-17&sr=b&sig=%2B2vYnQR7TEzGJicoJugt2WGzpB1C4w2h6p%2Fx9tnlEro%3D&st=2017-09-18T05%3A02%3A03Z&se=2017-09-18T09%3A07%3A03Z&sp=rd"

SAS permissions include `SharedAccessBlobPermissions.Read` and `SharedAccessBlobPermissions.Delete` (to allow blob removal by the receiver if required).

An additional scenario for this is to spread the load between multiple storage accounts upon sending w/o necessarily synchronizing storage connections strings with all the receivers.

Get the [latest version][4] of the plugin to handle your large messages.
Read [release notes][5] for details.

Special thank you to [Mats Iremark][6] for feature PR.


[1]: https://github.com/SeanFeldman/ServiceBus.AttachmentPlugin
[2]: https://docs.microsoft.com/en-us/azure/storage/common/storage-dotnet-shared-access-signature-part-1
[3]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2017/sending-large-message-wo-connection-string/image.png
[4]: https://www.nuget.org/packages/ServiceBus.AttachmentPlugin/1.1.0
[5]: https://github.com/SeanFeldman/ServiceBus.AttachmentPlugin/releases/tag/1.1.0
[6]: https://github.com/iremmats
