---
title: With Power Comes Responsibility
slug: with-power-comes-responsibility
date: '2009-06-12T17:20:00'
updated: '2009-06-12T17:20:00'
draft: false
tags:
- Other
author: Sean Feldman
---


In software like in a real life, not always everything can be extremely simple. One example I can think of right away is Inversion of Control container (IoC). In a simple application, it’s not a big deal, and normally achieved easily. The dependent component leverages some sort of Static Gateway container to resolve the dependencies based on contacts.

 
```
   1: public class Component
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">   2:</span> {</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">   3:</span>     <span style="color: #0000ff">public</span> Component(IDependency dependency) <span style="color: #008000">//...</span></pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">   4:</span>     <span style="color: #0000ff">public</span> Component() : <span style="color: #0000ff">this</span>(DependencyResolver.Resolve&lt;IDependency&gt;()) <span style="color: #008000">//...</span></pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">   5:</span> }</pre>
```

In order to “populate” container with all the dependencies, normally we’d leverage some sort of start-up task to achieve the goal.

```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">   1:</span> <span style="color: #0000ff">public</span> <span style="color: #0000ff">class</span> StartupTask : ICommand</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">   2:</span> {</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">   3:</span>     <span style="color: #0000ff">public</span> <span style="color: #0000ff">void</span> Execute()</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">   4:</span>     {</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">   5:</span>         DependencyResolver.Register&lt;IDependency&gt;(() =&gt; <span style="color: #0000ff">new</span> Dependency());</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">   6:</span>     }</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">   7:</span> }</pre>
```

When does the complexity creeps in? When a real life scenario kicks in. One of those scenarios are services. Why services? Because now it’s no longer a linear execution (a service can be started and stopped), and we neither want to pollute the service code with start-up tasks’ responsibilities. Solution? Different ones, but either way, a bit of complexity is added and from that moment and on developers are required to “ramp up” in knowledge to be able to understand and maintain it (develop or just-keep-alive). This is where “with power comes responsibility” is mostly used.

So is happening in real life. I was quiet surprised to see the most unexpected place – kids playground.

Playgrounds in Israel are mostly for kids up to age of 6 and not extremely attractive for teens.  Despite unmatched age, those normally spend some time at playgrounds as well, ruining them completely. A bright idea that a wise man had was to introduce “work-out” machines side-by-side with kids playground, so teens would invest their energy in a more peaceful way. Boy it worked! Not only little kids now have playgrounds in normal and usable condition and their parents a peace of mind, but also the awareness among teenagers for physical fitness has significantly raised. Well done. Here are some shots of proof how with power comes responsibility.

[![P6100051](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/P6100051_thumb_516EFAAC.jpg "P6100051")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/P6100051_590A8FE6.jpg) [![P6100057](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/P6100057_thumb_73F2ED8D.jpg "P6100057")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/P6100057_669D0054.jpg) [![P6100053](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/P6100053_thumb_4936C116.jpg "P6100053")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/P6100053_7B4EAD3A.jpg) [![P6100055](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/P6100055_thumb_7B0E1606.jpg "P6100055")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/P6100055_49DF7740.jpg)


