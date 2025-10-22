---
title: WPF Visual / Logical Tree(s)
slug: wpf-visual-logical-tree-s
date: '2008-09-10T15:29:09'
updated: '2008-09-10T15:29:09'
draft: false
tags:
- WPF
author: Sean Feldman
---


Coming from the ASP.NET development, I am quit used to the fact that a page has a tree of controls and by traversing the tree you can navigate to the elements.

With WPF is it a bit more sophisticated. WPF application has both visual and logical tree or several of those. Josh Smith has wrote a very useful [post](http://www.codeproject.com/KB/WPF/WpfElementTrees.aspx) to start understanding about the subject. Also there is a VS.NET debugger visualizer [Woodstock](http://www.codeproject.com/KB/WPF/WoodstockForWPF.aspx) to assist in understanding WPF trees.

The need to have to separate trees comes out of the fact that WPF has several different base classes for elements: ContentElement, Visual and Visual3D.

Visual is a base class for (the list is quit long, so it's not complete)

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/WPFVisualLogicalTrees_8220/image_thumb.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/WPFVisualLogicalTrees_8220/image_2.png)

Where ContentElement is a base class for:

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/WPFVisualLogicalTrees_8220/image_thumb_1.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/WPFVisualLogicalTrees_8220/image_4.png)

What is important to mention is that ContentElement derived instances are not a part of the visual tree, but the logical tree. In order to be rendered at all, ContentElement has to be hosted by a Visual control (which makes sense).

An example where it's becoming critical is when trying to traverse the tree from a given element, the order matters. First the logical path attempt and then the visual.

Two .NET framework classes that assist with the task are LogicalTreeHelper and VisualTreeHelper.


