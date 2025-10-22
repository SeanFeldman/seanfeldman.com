---
title: Body Message Part Name in XLANGMessage
slug: body-message-part-name-in-xlangmessage
date: '2010-07-20T14:47:00'
updated: '2010-07-20T14:47:00'
draft: false
tags:
- BizTalk
author: Sean Feldman
---


I was writing a custom component to copy message parts of an untyped message, invoked from orchestration. This message was created in a custom pipeline, and body part name had to have “Body”. For some bizarre reason, when message body part is handled outside of orchestration and passed into .NET code as XLANGMessage, body part name is “part”. ??? The other parts have the original names. I have no idea why this is happening, but thought it could save someone a question or two, especially when writing tests and expecting that the name of the part is “Body”.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_1297A66B.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_0C93361B.png)


