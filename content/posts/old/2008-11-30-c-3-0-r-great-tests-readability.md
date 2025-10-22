---
title: C# 3.0 + R# = Great Tests Readability
slug: c-3-0-r-great-tests-readability
date: '2008-11-30T05:09:00'
updated: '2008-11-30T05:09:00'
draft: false
tags:
- TDD
author: Sean Feldman
---


C# 3.0 has introduced lots of great features to make our life easier and syntax sweeter. Lots of people talked about it already, and I am not scooping here anything new. What I do want to demonstrate, is how to make the code easier to understand.

Confession is that I am relying on a tool to help me achieve what I will demonstrate – [ReSharper](http://www.jetbrains.com/resharper/). Not only it’s a great refactoring tool, but an excellent guide to C# 3.0 features (and not only). So lets roll to an example.

The test is trying to confirm that whatever path is being returned by system under test (SUT) is ending with either “\bin”, “\debug”, or “\release”. Normally, this is what I would write:

 
```
   1: [Test]
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   2:</span> <span style="color: rgb(0, 0, 255);">public</span> <span style="color: rgb(0, 0, 255);">void</span> Should_return_the_path_represented_by_system_as_a_BaseDirectory()</pre>
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   3:</span> {</pre>
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   4:</span>     var isMatching = result.path.EndsWith(<span style="color: rgb(0, 96, 128);">@"\bin"</span>, StringComparison.InvariantCultureIgnoreCase)</pre>
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   5:</span>                    || result.EndsWith(<span style="color: rgb(0, 96, 128);">@"\debug"</span>, StringComparison.InvariantCultureIgnoreCase)</pre>
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   6:</span>                    || result.EndsWith(<span style="color: rgb(0, 96, 128);">@"\release"</span>, StringComparison.InvariantCultureIgnoreCase);</pre>
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   7:</span>     Assert.IsTrue(isMatching);</pre>
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   8:</span> }</pre>
```

Way too chatty. The whole EndsWith is more of a distraction, rather than help.

Next step – introduce an Extension Method that would encapsulate testing. One option would be to write a method that takes boolean and asserts.

```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   1:</span> <span style="color: rgb(0, 0, 255);">public</span> <span style="color: rgb(0, 0, 255);">static</span> <span style="color: rgb(0, 0, 255);">void</span> should_be_true(<span style="color: rgb(0, 0, 255);">this</span> <span style="color: rgb(0, 0, 255);">bool</span> item)</pre>
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   2:</span> {</pre>
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   3:</span>    Assert.IsTrue(item);</pre>
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   4:</span> }</pre>
```

Then the code would read a bit more descriptive, but still with lots of ‘noise’.

```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   1:</span> isMatching.should_be_true(result.EndsWith(...) || (...) || (...));</pre>
```

Not nice :) Another way is to have an extension method accepting a Func<T, bool> and leverage method group

```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   1:</span> <span style="color: rgb(0, 0, 255);">public</span> <span style="color: rgb(0, 0, 255);">static</span> <span style="color: rgb(0, 0, 255);">void</span> should_be&lt;T&gt;(<span style="color: rgb(0, 0, 255);">this</span> T item, Func&lt;T, <span style="color: rgb(0, 0, 255);">bool</span>&gt; evalueationWith)</pre>
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   2:</span> {</pre>
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   3:</span>      Assert.IsTrue(evalueationWith(item));</pre>
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   4:</span> }</pre>
```

To escape the ‘noise’ I do what have described in the [previous post](http://weblogs.asp.net/sfeldman/archive/2008/11/29/test-helpers-and-fluent-interfaces.aspx) (Test Helper with Fluent Interface).

```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   1:</span> <span style="color: rgb(0, 0, 255);">private</span> <span style="color: rgb(0, 0, 255);">class</span> True</pre>
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   2:</span> {</pre>
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   3:</span>    <span style="color: rgb(0, 0, 255);">public</span> <span style="color: rgb(0, 0, 255);">static</span> <span style="color: rgb(0, 0, 255);">bool</span> for_the_given_path(<span style="color: rgb(0, 0, 255);">string</span> path)</pre>
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   4:</span>    {</pre>
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   5:</span>      <span style="color: rgb(0, 0, 255);">return</span> path.EndsWith(<span style="color: rgb(0, 96, 128);">@"\bin"</span>, StringComparison.InvariantCultureIgnoreCase)</pre>
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   6:</span>             || path.EndsWith(<span style="color: rgb(0, 96, 128);">@"\debug"</span>, StringComparison.InvariantCultureIgnoreCase)</pre>
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   7:</span>             || path.EndsWith(<span style="color: rgb(0, 96, 128);">@"\release"</span>, StringComparison.InvariantCultureIgnoreCase);</pre>
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   8:</span>    }</pre>
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   9:</span> }</pre>
```

Bringing the test to the form it becomes cleaner.

```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   1:</span> [Test]</pre>
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   2:</span> <span style="color: rgb(0, 0, 255);">public</span> <span style="color: rgb(0, 0, 255);">void</span> Should_return_the_path_represented_by_system_as_a_BaseDirectory()</pre>
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   3:</span> {</pre>
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   4:</span>   result.should_be(s =&gt; True.for_the_given_path(s));</pre>
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   5:</span> }</pre>
```

With some hints from R#…

[![image](http://weblogs.asp.net/blogs/sfeldman/image_thumb_6D946AB7.png "image")](http://weblogs.asp.net/blogs/sfeldman/image_62684FBC.png)

It becomes “now I get it”, as my team mate [Terry Thibodeau](http://www.connicus.com/) says, to hint me that finally the test becomes readable and simple to be considered good.

```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   1:</span> [Observation]</pre>
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   2:</span> <span style="color: rgb(0, 0, 255);">public</span> <span style="color: rgb(0, 0, 255);">void</span> Should_return_the_path_represented_by_system_as_a_BaseDirectory()</pre>
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   3:</span> {</pre>
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   4:</span>    result.should_be(True.for_the_given_path);</pre>
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   5:</span> }</pre>
```

Develop code, not bugs!


