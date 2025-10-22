---
title: Sending Big Files with WCF
slug: sending-big-files-with-wcf
date: '2010-05-30T23:36:00'
updated: '2010-05-30T23:36:00'
draft: false
tags:
- .NET
- WCF
author: Sean Feldman
---


I had to look into a project that submits large files to WCF service. Implementation is based on data chunking. This is a good approach when your client and server are not both based on WCF, bud different technologies.

The problem with something like this is that chunking (either you wish it or not) complicates the overall solution. Alternative would be streaming. In WCF to WCF scenario, this is a piece of cake. When client is Java, it becomes a bit more challenging (has anyone implemented Java client streaming data to WCF service?).

What I really liked about .NET implementation with WCF, is that sending header info along with stream was dead simple, and from the developer point of view looked like it’s all a part of the DTO passed into the service.

```
[ServiceContract]
public interface IFileUpload
{
  [OperationContract]
  void UploadFile(SendFileMessage message);
}
```

Where *SendFileMessage* is

```
[MessageContract]
public class SendFileMessage
{
  [MessageBodyMember(Order = 1)]
  public Stream FileData;

  [MessageHeader(MustUnderstand = true)]
  public FileTransferInfo FileTransferInfo;
}
```

