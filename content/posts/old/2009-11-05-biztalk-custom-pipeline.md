---
title: BizTalk Custom Pipeline
slug: biztalk-custom-pipeline
date: '2009-11-05T14:17:00'
updated: '2009-11-05T14:17:00'
draft: false
tags:
- BizTalk
author: Sean Feldman
---


I am starting a project that involves a lot BizTalk 2009. Since this is a completely new territory for myself, I decided to blog about it. There a lot of resources available out there, especially from [MSDN](http://msdn.microsoft.com/en-us/biztalk/default.aspx).

First thing I decided to look at was a Custom pipeline. Two types of pipeline exist – sending and receiving. To understand better pipelines, I read [BizTalk 2004: A Message Engine Overview](http://msdn.microsoft.com/en-us/library/ms935116%28BTS.10%29.aspx) on MSDN. It provides more information than just pipelines that is very useful for general BizTalk understanding (which I find a vital if you plan to develop for BizTalk).

A typical receive pipeline has 4 sections (or “component areas”) and send pipeline 3.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_02BD6232.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_1ECB906C.png)

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_3B6A9CF0.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_6B91E7B3.png)

In BizTalk project these pipelines are presented as a flow, with designated areas where you can drop  components designed especially for any given stage in a pipeline of a certain type. [![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_539097FC.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_445A2F2F.png) You can develop pipeline custom components in managed code, but you have to link it to the designer. How that is done? Each component has to be marked with a *ComponentCategory* attribute to indicate where in pipeline it can be assigned. A component that should be only assigned to Decoding section would be marked as:

 
```
[ComponentCategory(CategoryTypes.CATID_PipelineComponent)]
```
```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: #f4f4f4; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px">[ComponentCategory(CategoryTypes.CATID_Decoder)]</pre>
```
```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: white; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px">[System.Runtime.InteropServices.Guid(<span style="color: #006080">&quot;9D0E4103-4CCE-4536-83FA-4A5040674AD6&quot;</span>)]</pre>
```

The interoperability GUID 9D0E4103-4CCE-4536-83FA-4A5040674AD6 stands for “receive pipeline, decode section” and it is used to indicate to Visual Studio designer where the component can be dropped. For this purpose, I have create a component called “CustomPipelineComponent” and decorated with these attributes. Dragged and dropped the component and this is how the BizTalk pipeline looks like after that (XML view):

```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: white; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px"><span style="color: #0000ff">&lt;?</span><span style="color: #800000">xml</span> <span style="color: #ff0000">version</span><span style="color: #0000ff">=&quot;1.0&quot;</span> <span style="color: #ff0000">encoding</span><span style="color: #0000ff">=&quot;utf-16&quot;</span>?<span style="color: #0000ff">&gt;</span></pre>
```
```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: #f4f4f4; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px"><span style="color: #0000ff">&lt;</span><span style="color: #800000">Document</span> <span style="color: #ff0000">xmlns:xsi</span><span style="color: #0000ff">=&quot;http://www.w3.org/2001/XMLSchema-instance&quot;</span> <span style="color: #ff0000">xmlns:xsd</span><span style="color: #0000ff">=&quot;http://www.w3.org/2001/XMLSchema&quot;</span> <span style="color: #ff0000">PolicyFilePath</span><span style="color: #0000ff">=&quot;BTSReceivePolicy.xml&quot;</span> <span style="color: #ff0000">MajorVersion</span><span style="color: #0000ff">=&quot;1&quot;</span> <span style="color: #ff0000">MinorVersion</span><span style="color: #0000ff">=&quot;0&quot;</span><span style="color: #0000ff">&gt;</span></pre>
```
```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: white; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px">  <span style="color: #0000ff">&lt;</span><span style="color: #800000">Description</span> <span style="color: #0000ff">/&gt;</span></pre>
```
```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: #f4f4f4; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px">  <span style="color: #0000ff">&lt;</span><span style="color: #800000">Stages</span><span style="color: #0000ff">&gt;</span></pre>
```
```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: white; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px">    <span style="color: #0000ff">&lt;</span><span style="color: #800000">Stage</span> <span style="color: #ff0000">CategoryId</span><span style="color: #0000ff">=&quot;<u><strong>9d0e4103-4cce-4536-83fa-4a5040674ad6</strong></u>&quot;</span><span style="color: #0000ff">&gt;</span></pre>
```
```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: #f4f4f4; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px">      <span style="color: #0000ff">&lt;</span><span style="color: #800000">Components</span><span style="color: #0000ff">&gt;</span></pre>
```
```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: white; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px">        <span style="color: #0000ff">&lt;</span><span style="color: #800000">Component</span><span style="color: #0000ff">&gt;</span></pre>
```
```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: #f4f4f4; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px">          <span style="color: #0000ff">&lt;</span><span style="color: #800000">Name</span><span style="color: #0000ff">&gt;</span>SimplePipeline.CustomPipelineComponent<span style="color: #0000ff">&lt;/</span><span style="color: #800000">Name</span><span style="color: #0000ff">&gt;</span></pre>
```
```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: white; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px">          <span style="color: #0000ff">&lt;</span><span style="color: #800000">ComponentName</span><span style="color: #0000ff">&gt;</span>SIMPLE Pipeline component<span style="color: #0000ff">&lt;/</span><span style="color: #800000">ComponentName</span><span style="color: #0000ff">&gt;</span></pre>
```
```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: #f4f4f4; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px">          <span style="color: #0000ff">&lt;</span><span style="color: #800000">Description</span><span style="color: #0000ff">&gt;</span>CustomPipelineComponent<span style="color: #0000ff">&lt;/</span><span style="color: #800000">Description</span><span style="color: #0000ff">&gt;</span></pre>
```
```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: white; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px">          <span style="color: #0000ff">&lt;</span><span style="color: #800000">Version</span><span style="color: #0000ff">&gt;</span>1.0.0.0<span style="color: #0000ff">&lt;/</span><span style="color: #800000">Version</span><span style="color: #0000ff">&gt;</span></pre>
```
```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: #f4f4f4; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px">          <span style="color: #0000ff">&lt;</span><span style="color: #800000">CachedIsManaged</span><span style="color: #0000ff">&gt;</span>true<span style="color: #0000ff">&lt;/</span><span style="color: #800000">CachedIsManaged</span><span style="color: #0000ff">&gt;</span></pre>
```
```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: white; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px">        <span style="color: #0000ff">&lt;/</span><span style="color: #800000">Component</span><span style="color: #0000ff">&gt;</span></pre>
```
```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: #f4f4f4; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px">      <span style="color: #0000ff">&lt;/</span><span style="color: #800000">Components</span><span style="color: #0000ff">&gt;</span></pre>
```
```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: white; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px">    <span style="color: #0000ff">&lt;/</span><span style="color: #800000">Stage</span><span style="color: #0000ff">&gt;</span></pre>
```
```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: #f4f4f4; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px">    <span style="color: #0000ff">&lt;</span><span style="color: #800000">Stage</span> <span style="color: #ff0000">CategoryId</span><span style="color: #0000ff">=&quot;9d0e4105-4cce-4536-83fa-4a5040674ad6&quot;</span><span style="color: #0000ff">&gt;</span></pre>
```
```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: white; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px">      <span style="color: #0000ff">&lt;</span><span style="color: #800000">Components</span> <span style="color: #0000ff">/&gt;</span></pre>
```
```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: #f4f4f4; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px">    <span style="color: #0000ff">&lt;/</span><span style="color: #800000">Stage</span><span style="color: #0000ff">&gt;</span></pre>
```
```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: white; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px">    <span style="color: #0000ff">&lt;</span><span style="color: #800000">Stage</span> <span style="color: #ff0000">CategoryId</span><span style="color: #0000ff">=&quot;9d0e410d-4cce-4536-83fa-4a5040674ad6&quot;</span><span style="color: #0000ff">&gt;</span></pre>
```
```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: #f4f4f4; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px">      <span style="color: #0000ff">&lt;</span><span style="color: #800000">Components</span> <span style="color: #0000ff">/&gt;</span></pre>
```
```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: white; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px">    <span style="color: #0000ff">&lt;/</span><span style="color: #800000">Stage</span><span style="color: #0000ff">&gt;</span></pre>
```
```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: #f4f4f4; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px">    <span style="color: #0000ff">&lt;</span><span style="color: #800000">Stage</span> <span style="color: #ff0000">CategoryId</span><span style="color: #0000ff">=&quot;9d0e410e-4cce-4536-83fa-4a5040674ad6&quot;</span><span style="color: #0000ff">&gt;</span></pre>
```
```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: white; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px">      <span style="color: #0000ff">&lt;</span><span style="color: #800000">Components</span> <span style="color: #0000ff">/&gt;</span></pre>
```
```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: #f4f4f4; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px">    <span style="color: #0000ff">&lt;/</span><span style="color: #800000">Stage</span><span style="color: #0000ff">&gt;</span></pre>
```
```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: white; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px">  <span style="color: #0000ff">&lt;/</span><span style="color: #800000">Stages</span><span style="color: #0000ff">&gt;</span></pre>
```
```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: #f4f4f4; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px"><span style="color: #0000ff">&lt;/</span><span style="color: #800000">Document</span><span style="color: #0000ff">&gt;</span></pre>
```

If you look close, each section in pipeline (or Stage) has a designated GUID. Decoder has 9D0E4103-4CCE-4536-83FA-4A5040674AD6, same as we used to decorate our component with.

Now the saucy part – how do I debug and test it?

To debug (which is **NOT** testing) I used BizTalk 2009 SDK utility called Pipeline.exe and located in %ProgramFiles%\Microsoft BizTalk Server 2009\SDK\Utilities\PipelineTools. One disadvantage I found with this utility is the fact that you have to deploy your custom pipeline component assembly to BizTalk 2009 designated location (%ProgramFiles%\Microsoft BizTalk Server 2009\Pipeline Components). Well, at least you can debug your custom component. For that I had to update the project settings of my custom pipeline component project and setup 3 things:

1. Specify **Output** for build artifact (Figure 1)
2. Set **Start Action** to Pipeline.exe (Figure 2)
3. Specify **Command Line Arguments** to use pipeline that contains custom component

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_41D8AF84.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_50EA6CFC.png) Figure 1

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_5111A902.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_1EAB44D2.png)

Figure 2

When a new instance of Debugger is invoked on component project, debugger will kick in and stop at breakpoints.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_678BF99C.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_5995084C.png)

To test a custom component you will have to dig dipper. I have figured a few things:

1. You cannot do unit testing. BizTalk has **integration testing baked in**.
2. You have to include BizTalk test assemblies, located in **%ProgramFiles%\Microsoft BizTalk Server 2009\Developer Tools** (I wish other blogs would mentions this folder!)
3. You will have to **cast your objects to BizTalk base classes** (the ones your maps/pipelines/schemas) in order to invoke testing methods (such as map.TestMap(…), schema.ValidateInstance(…), and pipeline.TestPipeline(…) accordingly)

I found [one good blog post](http://geekswithblogs.net/michaelstephenson/archive/2008/12/12/127827.aspx) about how actually to write a state based testing, so I will not reproduce it here.

PS: an attempt to test pipeline components as unit testing is showed in [this blog](http://geekswithblogs.net/michaelstephenson/archive/2008/03/30/120852.aspx).


