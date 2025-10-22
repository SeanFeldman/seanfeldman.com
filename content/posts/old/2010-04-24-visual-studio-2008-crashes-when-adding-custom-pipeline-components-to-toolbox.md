---
title: Visual Studio 2008 Crashes When Adding Custom Pipeline Components to Toolbox
slug: visual-studio-2008-crashes-when-adding-custom-pipeline-components-to-toolbox
date: '2010-04-24T15:29:00'
updated: '2010-04-24T15:29:00'
draft: false
tags:
- BizTalk
author: Sean Feldman
---


I have run into this issue trying to add custom pipeline component to toolbox. The only way (I know about) to add a custom pipeline component to a customized pipeline is using the visual designer. In order to do that you have to have components on toolbox. This was a bit frustrating. Google has brought [one result](http://connectedthoughts.wordpress.com/2009/07/01/visual-studio-crash-when-trying-to-add-pipeline-components-to-toolbox/) which was exactly what I needed. One of the comments had another link, to the similar issue, but this time with a different title: [Hotfix for BizTalk 2009 and Visual Studio 2008](http://go2.wordpress.com/?id=725X1342&site=connectedthoughts.wordpress.com&url=http%3A%2F%2Fsupport.microsoft.com%2Fkb%2F977428%2Fen-us&sref=http%3A%2F%2Fconnectedthoughts.wordpress.com%2F2010%2F01%2F25%2Fhotfix-for-biztalk-2009-and-visual-studio-2008-issues-released%2F). I followed the link, installed hotfix, and it worked. Oh, yes, you **have** to reboot your machine for hotfix to work completely (this is where I spent some time pulling my hair out and asking why hotfix didn’t work?!). Once this is done, you are good to go.

Among other things, this hotfix deals with BizTalk project references to each other and items not being updated (like distinguished fields in schemas project not reflected in orchestrations project). Here’s the full list:

\* The orchestrations in the referenced BizTalk project may show compiler warnings.   
\* The changes that are made to the referenced BizTalk project are not propagated on to the referencing project.   
\* When you edit the orchestrations of the referenced project, XLANG errors are thrown. These errors may disappear after the orchestrations are saved and recompiled.   
\* After you deploy the referencing project, the local copies of the referenced project’s binaries are deleted.   
\* After you deploy the referencing project, various errors or warnings occur in Orchestration Designer.


