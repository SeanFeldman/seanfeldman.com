---
title: '"Hello World" TDD Style'
slug: quot-hello-world-quot-tdd-style
date: '2008-12-13T04:49:14'
updated: '2008-12-13T04:49:14'
draft: false
tags:
- TDD
author: Sean Feldman
---


A friend of mine told me, "what you know and what seems to as trivial, might be completely new to someone else". So I am trying to remember this, and once again the simple life wisdom proved to be correct. One of our team members had to be away while the team was conquering T/BDD and unit testing. As a result, he stayed a little behind, and as catch up exercise, we pared on a very simple problem, Calculator, another version of the classical "Hello World". Maybe this will help someone someday.

Calculator is capable of adding to numbers and return the result. Each time calculator performs an operation like Add, it should log it. Lets break it down

*Calculator* is the contract we are defining for creation. The component that will implement it is going to be the *system under test*. There is exactly one specification at this point, that *Calculator* is performing *Add* operation.  We also have a few observations, such as "should  add two numbers together and return the result", and "should log the operation". Visually (personally, I am an extremely visual person and need to visualize a lot) it look like this:

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_thumb.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_2.png)

Our contract is simple. Do I start implementation just because I know precisely how it's going to be implemented? No. Why not? What's so difficult about adding two numbers and giving back the result?! (Normally it will sound like you trying to insult a person who's supposed to follow these steps). But wait till the end, we'll come back to this again.

Lets start the test, shall we? The test will drive out everything. Prior to this, I would like to mention[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_thumb_2.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_6.png) how we as a team setup our environment, so development is streamlined and templated (no unnecessary friction). Normally, there will be a Build project to contain any utilities, 3rd party components, tools, etc. The rest are the code projects. Ad a team, we concluded that having separate test projects adds too much of a maintenance and can be eliminated by keeping tests along with the tested code. To differentiate between production code and test code we use naming conventions that allow easy filtering at sooner time by automated build script. Specifications for a single component are all locked under the "hood" of a single file - *CoponentName*\_Specs. This allows very quick visual separation between the test code and the 'normal' code. It's also allows a better association between what is tested and where are the tests reside.

In order to create tests with less friction, we have our "abstraction" of testing tools (using MbUnit, Rhino.Mocks). Normally those are grouped in a sub-folder under *Infrastructure*.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_thumb_3.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_8.png)ConcernAttribute - used for documentation generation (specs extraction)

AssertionExtensions - abstraction of MbUnit (also syntactical sugar)

RhinoMocksExtensions - abstraction of Rhino.Mocks (similar to above)

StaticContextSpecification - base specification class to create a framework for all the tests

ContextSpecification - extension of *StaticContextSpecification* for Contract driven tests

TimeBomb - a necessary evil we had to have to postpone a test implementation till a certain date/time

TimeBomb\_Specs - everything has to have a test...

Now that we have seen what the "framework is" we know it's no more than just a few things that will save us typing time. The most interesting ones are *StaticContextSpecification* and *ContextSpecification.*

 
```
   1: [TestFixture]
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">   2:</span> <span style="color: #0000ff">public</span> <span style="color: #0000ff">abstract</span> <span style="color: #0000ff">class</span> StaticContextSpecification</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">   3:</span> {</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">   4:</span>     [SetUp]</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">   5:</span>     <span style="color: #0000ff">public</span> <span style="color: #0000ff">void</span> setup()</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">   6:</span>     {</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">   7:</span>         establish_context();</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">   8:</span>         because();</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">   9:</span>     }</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">  10:</span>&#160; </pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">  11:</span>     [TearDown]</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">  12:</span>     <span style="color: #0000ff">public</span> <span style="color: #0000ff">void</span> tear_down()</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">  13:</span>     {</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">  14:</span>         after_each_specification();</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">  15:</span>     }</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">  16:</span>&#160; </pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">  17:</span>     <span style="color: #0000ff">protected</span> <span style="color: #0000ff">abstract</span> <span style="color: #0000ff">void</span> because();</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">  18:</span>     <span style="color: #0000ff">protected</span> <span style="color: #0000ff">abstract</span> <span style="color: #0000ff">void</span> establish_context();</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">  19:</span>     <span style="color: #0000ff">protected</span> <span style="color: #0000ff">virtual</span> <span style="color: #0000ff">void</span> after_each_specification()</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">  20:</span>     {</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">  21:</span>     }</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">  22:</span>&#160; </pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">  23:</span>     <span style="color: #0000ff">protected</span> InterfaceType dependency&lt;InterfaceType&gt;()</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">  24:</span>     {</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">  25:</span>         <span style="color: #0000ff">return</span> MockRepository.<strong><u>GenerateStub</u></strong>&lt;InterfaceType&gt;();</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">  26:</span>     }</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">  27:</span> }</pre>
```

Some use for dependency Mock, our team has reached the conclusion that by default we should be using Stub, and only in cases when it's really needed turn to Mock. See [documentation](http://ayende.com/Wiki/Default.aspx?Page=Rhino+Mocks+3.5&AspxAutoDetectCookieSupport=1) provided by Oren Eini on this.

```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">   1:</span> <span style="color: #0000ff">public</span> <span style="color: #0000ff">abstract</span> <span style="color: #0000ff">class</span> ContextSpecification&lt;SystemUnderTestType&gt; : StaticContextSpecification</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">   2:</span> {</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">   3:</span>     <span style="color: #0000ff">protected</span> SystemUnderTestType system_under_test;</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">   4:</span>&#160; </pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">   5:</span>     <span style="color: #0000ff">protected</span> <span style="color: #0000ff">abstract</span> SystemUnderTestType create_system_under_test();</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">   6:</span> }</pre>
```

All the underscores is an adopted style quiet popular among TDD/BDD practitioners and frankly speaking feels extremely natural once you get used to the concept **AND** get to know about [AutoHotKey](http://www.autohotkey.com/) utility and how to use it in conjunction with test-related names. [Steven Harman](http://stevenharman.net/blog/archive/2008/06/07/save-your-fingers-use-a-bdd-autohotkey-script.aspx) has a good post about it. (Ismaël, hold on, I am almost done with the script for your name:)[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_thumb_4.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_10.png)

Lets get to the business - specification for calculator. First - definition of concern. [ReSharper](http://www.jetbrains.com/resharper/) is the tool you have to use. No ReSharper (R#), no deal. You can try something else, and if you find better, let me know. So far this is #1 for our team.

Remember we said that test will drive everything, even if it's a dead simple task - so it's happening. Since we specified the concern, R# will assist us to create it.

[[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_thumb_5.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_12.png)![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_thumb_6.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_14.png)

The testing framework we put in place will ensure that the contract for the component we are concerned about is generated as well, forcing the component to implement that specific contract.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_thumb_7.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_16.png) [![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_thumb_8.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_18.png)

This is great! Now system\_under\_test is always expressed by the contract. Anything we define/do on it, is affecting the contract, driving out the design of the component that implements it. I.e., we shape the contract to make it usable and well designed, and component is just the implementation of that contract.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_thumb_11.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_24.png)

Establishing context at this point is very simple. Though, this code smells a bit and it probably will be replicated multiple times for each specification. We will refactor it later, so this becomes an optionaltemplate method with default behavior to instantiate *system\_under\_test*.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_thumb_12.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_26.png) [![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_thumb_14.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_30.png)

Why we are going to have an observation? **Because** some behavior on *system\_under\_test* has happened. Again, *Add* behavior is not defined. We will add it leveraging R#, and this will go into the Contract, not the implementation. But contract will force implementer to have it as well.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_thumb_15.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_32.png)

And this is where it's shockingly simple and yet confusing a lot, we don't implement the behavior and let the exception be thrown. Why? The test should fail, then be fixed. Red-Green-Refactor. That's the rhythm, and it's good.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_thumb_16.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_34.png)

To someone who's not used to this it looks ridiculous. "Why would someone do this silly thing when I know exactly what to return - what's the point". The point that every complex thing starts from something simple. We are not just creating tests here, we are documenting the code, shaping our architecture, go through the issues from the user perspective (usability). It might look like a wasted effort at this point, but down the road it pays off big time. OK, lets refactor *result* to be a member field, rename the specification to something that is more meaningful than *Calculator\_Specs*, such as "*When\_calculator\_is\_asked\_to\_add\_two\_numbers*", and define an observation (Our team uses Gallio addon for Visual Studio.NET to run the tests and unfortunately, ObservationAttribute is not picked up by Gallio as we haven't found what in MbUnit v3 would be equivevalent to the TestPatternAttribute  from MbUnit v2.4. In case you know the solution, would appreciate your help)

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_thumb_18.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_38.png)

Lets run the test

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_thumb_19.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_40.png)

It fails - good. What's good? Is that we need to 'fix' it, i.e. implement and bring to the green. We also keep in mind that we do the simplest thing to pass. This is so tough on people who are absolutely new to the testing, to the point where you sit in front of the line to implement, overwhelmed with all the going on,  thinking that there must be a catch, it's not as simple as it seems. I loved this type of exercise JP gave at his [course](http://blog.jpboodhoo.com/SoWhatDoPastStudentsReallyThinkAboutNothinButNet.aspx). BTW, if you haven't heard about Nothin But .NET bootcamp, you are living a life or a mort. Google it, save for it, and do it. Regardless of your skills level, you will NOT regret. And yes, you get your money back in a HUGE satisfaction after and a complete change in how you do things for better. Especially if you are getting tired of development because it just "doesn't  do it to you" as it used before - get your second breath and self re-invention at his course. So simple thing first...

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_thumb_20.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_42.png)

Run the test - green. Good. Is it? Let's break in the simplest possible way (not that it's hard).

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_thumb_21.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_44.png)

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_thumb_22.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_46.png)

Breaking. But wait a second, what is breaking? No, not the *system\_under\_test*, it's our test is wrong. The lesson is that tests have to be clean and simple, or they are not a tool to assist, but another impediment in the future, and eventually destined to be abandoned. How about extracting those magical numbers with constants?

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_thumb_23.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_48.png)

Re-running the test will still be breaking, but now we are a 100% confident that this is the *system\_under\_test* that is breaking. Lets fix it.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_thumb_24.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_50.png)

Passing again and now we know it's not a hard-coded value, but actual calculation. This is our first observation for this specification that exercises state based testing of the component.

How about the second one, "*Should\_log\_the\_operation*"? Now we getting more into Dependency Injection and interaction testing. We don't want to create the actual logger, but we want to shape and form the contract and verify our *Calculator* works with the logger the way we will design it. A mocking library is a must at this point. Logger is a *dependency* to the *Calculator*. We shall inject it upon creation of *Calculator*.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_thumb_25.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_52.png)

Once again, because we are doing this from test, we will be forced to define a contract for our logger, *ISomeLogger*, and refactor the constructor of *Calculator* to be able to accept it.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_thumb_26.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_54.png)

Again it seems obvious what has to be done, but fight the tempt of doing the evil, resist it and go back to the test. Why? Because we want to document, we want to make sure that it fails first and our implementation is based on the test, and not vice versa, to shape the logger contract before we anything else.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_thumb_27.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_56.png)

We also setup and expectation that logger will be used and it's *Log* method will be called with a parameter "add". This is probably the best documentation I, personally, have seen ever done for a code. This is one of so many reasons why you want to have the tests in place. So we run it and it fails. Why?

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_thumb_28.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_58.png)

Error massage shows us that "System.InvalidOperationException: The object '' is not a mocked object." - Ops, right, we are passing in *logger,* into *Calculator* constructor, but it's nothing. It's our dependency, let's stub it.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_thumb_29.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_60.png)

Fails again, but now the error message gives us direction to the next step that we are supposed to take "Rhino.Mocks.Exceptions.ExpectationViolationException: Expected that ISomeLogger.Log("add"); would be called, but it was not found on the actual calls made on the mocked object.". Let's fix it and run the tests again.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_thumb_30.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_62.png)

This time the assertion passes and tests are all green.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_thumb_31.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/image_64.png)

This observation was an interaction based test. We were not trying to define how logger will get implemented, we deferred that till the last possible moment. Did just enough to get this going - a contract. Implementation will depend on actual requirements. *Calculator* is capable of logging, we ensured well enough that it's documented and traceable in case *Calculator* changes introduce some breaking code.

Now the problem of creating system\_under\_test and establishing context - that can be refactored to remove the smell and remove code duplication:

```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">   1:</span> <span style="color: #0000ff">public</span> <span style="color: #0000ff">abstract</span> <span style="color: #0000ff">class</span> context_for_calculator : ContextSpecification&lt;ICalculator&gt;</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">   2:</span> {</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">   3:</span>     <span style="color: #0000ff">protected</span> ISomeLogger logger;</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">   4:</span>&#160; </pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">   5:</span>     <span style="color: #0000ff">protected</span> <span style="color: #0000ff">override</span> ICalculator create_system_under_test()</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">   6:</span>     {</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">   7:</span>         logger = dependency&lt;ISomeLogger&gt;();</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">   8:</span>         <span style="color: #0000ff">return</span> <span style="color: #0000ff">new</span> Calculator(logger);</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">   9:</span>     }</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">  10:</span>&#160; </pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">  11:</span>     <span style="color: #0000ff">protected</span> <span style="color: #0000ff">override</span> <span style="color: #0000ff">void</span> establish_context()</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">  12:</span>     {</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">  13:</span>         system_under_test = create_system_under_test();</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">  14:</span>     }</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">  15:</span> }</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">  16:</span>&#160; </pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">  17:</span> [Concern(<span style="color: #0000ff">typeof</span>(Calculator))]</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">  18:</span> <span style="color: #0000ff">public</span> <span style="color: #0000ff">class</span> When_calculator_is_asked_to_add_two_numbers : context_for_calculator</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">  19:</span> {</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">  20:</span>     <span style="color: #0000ff">private</span> <span style="color: #0000ff">const</span> <span style="color: #0000ff">double</span> first_number = 8.0;</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">  21:</span>     <span style="color: #0000ff">private</span> <span style="color: #0000ff">const</span> <span style="color: #0000ff">double</span> second_number = 3.0;</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">  22:</span>     <span style="color: #0000ff">private</span> <span style="color: #0000ff">const</span> <span style="color: #0000ff">double</span> sum_of_first_number_and_second_number = first_number + second_number;</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">  23:</span>     <span style="color: #0000ff">private</span> <span style="color: #0000ff">double</span> result;</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">  24:</span>     </pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">  25:</span>     <span style="color: #0000ff">protected</span> <span style="color: #0000ff">override</span> <span style="color: #0000ff">void</span> because()</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">  26:</span>     {</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">  27:</span>         result = system_under_test.Add(first_number, second_number);</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">  28:</span>     }</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">  29:</span>&#160; </pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">  30:</span>     [Test]<span style="color: #008000">//[Observation]</span></pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">  31:</span>     <span style="color: #0000ff">public</span> <span style="color: #0000ff">void</span> Should_return_the_sum_of_two_numbers()</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">  32:</span>     {</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">  33:</span>         result.should_be_equal_to(sum_of_first_number_and_second_number);</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">  34:</span>     }</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">  35:</span>&#160; </pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">  36:</span>     [Test]<span style="color: #008000">//[Observation]</span></pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">  37:</span>     <span style="color: #0000ff">public</span> <span style="color: #0000ff">void</span> Should_log_the_operation()</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">  38:</span>     {</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">  39:</span>         logger.was_told_to(l =&gt; l.Log(<span style="color: #006080">&quot;add&quot;</span>));</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">  40:</span>     }</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">  41:</span> }</pre>
```

Now another member of the team, [Terry](http://www.connicus.com/), looks at it and says "ahh, now it feels good".

I hope this was helpful to someone who's trying to make any sense out of testing. It is funny how I was telling my son again and again to my 5 years old son "do one thing at a time, but do it well", when myself was not following this basic rule. Test one thing at a time, and test it well. This will lead you to the system that is written in such a manner you will enjoy working with it, regardless how difficult the domain problem is.

[Code for download](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/HelloWorldBDDStyle_132D7/CalculatorSpike_1.zip)


