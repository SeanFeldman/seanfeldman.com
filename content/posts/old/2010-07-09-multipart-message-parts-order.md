---
title: Multi-Part Message Parts Order
slug: multipart-message-parts-order
date: '2010-07-09T21:17:00'
updated: '2010-07-09T21:17:00'
draft: false
tags:
- BizTalk
- TDD
author: Sean Feldman
---


For the project I work on, processing involves multiple files. Files are packaged in a ZIP archive and it’s BizTalk application that opens the archive and builds a message for processing. In BizTalk terminology, this is a multi-part message.

Interestingly, if you search for more information, mostly you’ll find how to receive a MIME message that is already multi-part message (i.e. BizTalk can already handle it) or how to do it with Orchestration, by defining a contract (schema) of the multi-part message. But what if you want to construct your multi-part message within a pipeline? And what if you don’t know how many parts you have?

In my scenario a message is defined as a document with any number of attachments. Document becomes the body part, attachments become additional message parts. So far quite simple. Except that there’s a catch – order of parts at creation time of a multi-part message **matters**. It is not enough to mart the body part with a boolean flag to indicate that that’s a body part, you also have to insert the body part **first**, and only after that any additional parts. If that’s not happening, BizTalk throws a nice [WrongBodyPartException](http://msdn.microsoft.com/en-us/library/microsoft.xlangs.basetypes.wrongbodypartexception%28BTS.20%29.aspx) exception.

From the API point of view, this is a little bit of a smell, since you expect the engine to be smart enough to read first the part that is marked as a body (why would you mark it as a body then). The doubt that I’ll give it is that I am not fully aware how internals are working. So hopefully this will save someone time and efforts of troubleshooting an issue like this.

For the project I wanted to document it, and again, the best way to document it was tests. First I needed the test to fail to verify the expected issue. Once custom pipeline component was fixed, the test passed, and documentation is a living and breathing code. And code doesn’t lie.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_2D09E583.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_21DDCA88.png)


