---
title: CategoryAttribute
slug: categoryattribute
date: '2009-05-08T03:45:30'
updated: '2009-05-08T03:45:30'
draft: false
tags:
- TDD
author: Sean Feldman
---


Anyone who's doing TDD is familiar with the CategoryAttribute coming with the most of frameworks. Today (I am surprised it took us so long!) we got read of

 
```
[Category("Integration")]
```

and started to use the right approach

```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none">[Category(Categories.Integration)]</pre>
```

where Categories is a sealed class with constants

```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #0000ff">public</span> <span style="color: #0000ff">sealed</span> <span style="color: #0000ff">class</span> Categories</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none">{</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none">    <span style="color: #0000ff">public</span> <span style="color: #0000ff">const</span> <span style="color: #0000ff">string</span> Integration = <span style="color: #006080">&quot;Integration&quot;</span>;</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none">}</pre>
```

Why is it good? First - it's DRY (rather that finding strings such as "Integration" and "Integration**s**" all over the place. Second - it's easy to refactor.


