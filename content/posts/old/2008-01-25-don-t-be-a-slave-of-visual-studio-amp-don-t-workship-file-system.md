---
title: Don't Be A Slave Of Visual Studio & Don't Workship File System
slug: don-t-be-a-slave-of-visual-studio-amp-don-t-workship-file-system
date: '2008-01-25T07:01:55'
updated: '2008-01-25T07:01:55'
draft: false
tags:
- Personal
- VS.NET
author: Sean Feldman
---


Understanding what are you working on is the priority #1. If you not sure, then you don't know what are you working on. How do you keep several items linked logically while working on them - you try to keep something common between them. To be more particular, I will bring an example of an application I was exposed to with my team, and show several approaches, including the one I am so against.

The application has several sections. Each section has its' views. All the views are a part of the MVP pattern. One of the sections is called Product Management, where you can list all Product Releases in the system for a given Product, or create a new Product Release, or update an existing one. First image will show how the section file structure looks like.

Note: the team is using R# and is trying to be compliant as much as possible to all its' requirements (such as folder structure should be driving the namespaces, etc).

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/DontBeASlaveOfVisualStudioDontWorkshipFi_14D63/image_thumb.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/DontBeASlaveOfVisualStudioDontWorkshipFi_14D63/image_2.png)

First thing first. ProductManage - sounds good, but DM? As I learned it was an abbreviation of "Domain Model" - but wait a minute, there's view and presenter exist in that same folder as well, so it's no longer just DM.

IViewEdit - bad. Not only it twist the logical naming of the class, but also copies the name of a different contract that belongs to a different section... and only because they partitioned by folders, they do not collide in name. They don't? Yes they do! When you work on those, you want to know what view contract is that. Not mentioning the inverted logic naming convention (IViewEdit, ViewEdit, IModelProduct, ModelProduct, DtoProduct, etc. - Long live Hungarian notation?!). After a few months a name like IProductReleaseEditView will ring a bell faster than IViewEdit, and then digging in what folder/sub-folder it lives in.

To myself this is a slavery to VS.NET and file system.  Rather than trying to arrange all views, models, presenters nicely in a solution window, we should care about meaningful names classes/interfaces are given. Besides, R# is not looking for the file name, it is looking for the class/interface name on a search. And I would definitely put more trust in re-factoring tool, rather than in file editor... but these are personal preferences.


