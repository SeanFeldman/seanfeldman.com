---
title: NUnit vs. MbUnit
slug: nunit-vs-mbunit
date: '2008-11-13T05:07:36'
updated: '2008-11-13T05:07:36'
draft: false
tags:
- TDD
author: Sean Feldman
---


It's not a secret that I prefer certain tools/frameworks/applications over other ones. So is true with unit testing framework. My currently preferred one is MbUnit. My team was using NUnit so far, and honestly I respected the choice and didn't mind that much. Until this week.

This week we moved to MbUnit (yupi!). Several reasons for that:

* Row testing was not possible - despite the [NUnit.Rowtest extension](http://www.andreas-schlapsi.com/projects/rowtest-extension-for-nunit/), it was not working with R# unit tests runner
* Multiple assertions would fail if the first one would not pass
* *Assert.AreEqual* behaved weirdly

The last item was quiet a surprise. What happened is that we decided to try to be more expressive in our tests, and therefor substitute *Assert.AreEqual()* with extension method *should\_be\_equal\_to()* allowing a more fluent syntax and human expressiveness (yes, side effect is abstracting away the unit testing framework, but that was not the primarily intent).

One interesting fact about how we implemented it. As I have mentioned, with extension method. The code is quiet simple:

 
```
public static class AssertionsExtensions
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none">{</pre>
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none">    <span style="color: #0000ff">public</span> <span style="color: #0000ff">void</span> should_be_equal_to(<span style="color: #0000ff">this</span> <span style="color: #0000ff">object</span> actual, <span style="color: #0000ff">object</span> expected)</pre>
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none">    {</pre>
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><blockquote dir="ltr" style="margin-right: 0px"><p>    Assert.AreEqual(expected, actual);</p></blockquote></pre>
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none">    }</pre>
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none">}</pre>
```

It was working just fine. So an expression like

```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none">var result = CreateSystemUnderTest();</pre>
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none">result.Id.should_be_equal_to(1);</pre>
```

would work. Until we introduced MbUnit and it started complaining. It complained about the fact that if result would be a string "1" value, and expected value would have been 1 numeric, still it would report it as equal, despite the fact that they are not of the same type. Our fix was to get away from an *object* type and use generics:

```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #0000ff">public</span> <span style="color: #0000ff">static</span> <span style="color: #0000ff">class</span> AssertionsExtensions</pre>
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none">{</pre>
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none">    <span style="color: #0000ff">public</span> <span style="color: #0000ff">void</span> should_be_equal_to&lt;T&gt;(<span style="color: #0000ff">this</span> T actual, T expected)</pre>
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none">    {</pre>
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none">        Assert.AreEqual(expected, actual);</pre>
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none">    }</pre>
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none">}</pre>
```

Now MbUnit was satisfied and we were happy - tests passing again.

So what happened? Apperently *Assert.AreEqual()* expects either two strings or two objects. When a string and another type are supplied, it does *ToString()* and compares the values. 1.*ToString()* would be the same as "1". But these two are not equal in the normal context. MbUnit was smart enough to pick that and warn about it.

Kudos to MbUnit. Good for us :)


