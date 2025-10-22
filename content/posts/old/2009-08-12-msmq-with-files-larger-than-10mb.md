---
title: MSMQ With Files Larger Than 10MB?
slug: msmq-with-files-larger-than-10mb
date: '2009-08-12T06:13:00'
updated: '2009-08-12T06:13:00'
draft: false
tags:
- .NET
author: Sean Feldman
---


**Update 2009-09-11**: I was playing with the sample provided in two comments, and has run into issue with chunking binding. See thread: <http://code.msdn.microsoft.com/msmqpluswcf/Thread/View.aspx?ThreadId=2265>  


Has anyone dealt with this issue before? We are running into a problem when our system has to use queues, but files can be more than 10MB.

I have googled around, and found a few things about MSMQ/T (BizTalk related/unrelated), but nothing concrete ([example](http://blogs.msdn.com/johnbreakwell/archive/2007/08/22/how-to-send-msmq-messages-over-4mb-in-size-1-using-mqrtlarge-dll.aspx)).

Has anyone had some production code with messages more than 4MB using MSMQ/T and can point to the right resources? Thank you.


