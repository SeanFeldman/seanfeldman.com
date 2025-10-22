---
title: Regex With Comments
slug: regex-with-comments
date: '2010-01-01T21:51:00'
updated: '2010-01-01T21:51:00'
draft: false
tags:
- C#
author: Sean Feldman
---


While working on a specific task that required a lot of parsing, I came to conclusion that comments for Regex expressions are quite useful. The way I usually write code allows to look at specifications and determine what each component can do. But with Regex it’s not quite transparent, as you might use expressions to achieve the goal, but not necessarily expose the usage through specs.

Just to make it a bit more self-evident, here’s a Regex pattern without and with comments.

 
```
const string pattern = 
```
```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: #f4f4f4; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px">  <span style="color: #006080">@&quot;(\r\n)*(?&lt;headers&gt;(?:[^\r\n]+\r\n)*)[\r\n]*(?&lt;body&gt;[^Content-][\s\S]*[^\r\n])[\r\n]&quot;</span>;</pre>
```

vs.

```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: white; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px"><span style="color: #0000ff">const</span> <span style="color: #0000ff">string</span> pattern = </pre>
```
```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: #f4f4f4; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px">  <span style="color: #006080">@&quot;(\r\n)*(?&lt;headers&gt;(?:[^\r\n]+\r\n)*)             #headers group (Content-* like)</pre>
```
```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: white; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px">&#160;&#160; [\r\n]*(?&lt;body&gt;[^Content-][\s\S]*[^\r\n])[\r\n]  #body group (actual data)&quot;</span>;</pre>
```

Reminds me a bit of old-days assembly code I used to write…

To make it work, Regular Expression options has to *RegexOptions.Multiline | RegexOptions.IgnorePatternWhitespace* have options on.


