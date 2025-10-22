---
title: Warning – Best Practices
slug: warning-best-practices
date: '2009-07-31T15:03:00'
updated: '2009-07-31T15:03:00'
draft: false
author: Sean Feldman
---


According to the wikipedia definition, [best practice](http://en.wikipedia.org/wiki/Best_practice) is

> …a technique, method, process, activity, incentive or reward that is believed to be more effective at delivering a particular outcome than any other technique, method, process, etc.

The word “believed”, in my opinion, plays an important role. What one believes in, is not necessarily shared by another person. And not only with faith, but with technologies as well. What one technology / platform / methodology will describe as good practice, another one can claim if not the opposite, then at least disagree on the stated.

The motivation for this though was withdrawn from the project I am working on quickly, which is entirely written in Java. Despite my opinions on Java as a language, there’s something fundamental embedded in  Java, that does not exist in C# – one class per file. It bothered me, so I decided to spike the history of the feature.

Now you can debate for hours if this right or wrong. I think this is a **false best practice**. From Object Oriented perspective, there’s nothing wrong with more than one class (or “type”) within a single file. Let me demonstrate a few examples.

#### Example 1 – Design by Contract

The system is coded with a Container (Dependency Injection), and Contracts are what we care about, not implementers. In some cases it makes sense to see **packaging** done the following way:

 
```
   1: public interface IContract
```
```
<pre style="border-bottom-style: none; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: #f4f4f4; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px"><span style="color: #606060">   2:</span> {</pre>
```
```
<pre style="border-bottom-style: none; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: white; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px"><span style="color: #606060">   3:</span>   <span style="color: #008000">//...</span></pre>
```
```
<pre style="border-bottom-style: none; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: #f4f4f4; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px"><span style="color: #606060">   4:</span> }</pre>
```
```
<pre style="border-bottom-style: none; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: white; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px"><span style="color: #606060">   5:</span>&#160; </pre>
```
```
<pre style="border-bottom-style: none; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: #f4f4f4; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px"><span style="color: #606060">   6:</span> <span style="color: #0000ff">internal</span> <span style="color: #0000ff">class</span> DefaultContractImplementation : IContract</pre>
```
```
<pre style="border-bottom-style: none; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: white; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px"><span style="color: #606060">   7:</span> {</pre>
```
```
<pre style="border-bottom-style: none; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: #f4f4f4; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px"><span style="color: #606060">   8:</span>   <span style="color: #008000">//...</span></pre>
```
```
<pre style="border-bottom-style: none; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: white; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px"><span style="color: #606060">   9:</span> }</pre>
```

I intentionally highlighted “packaging”, because in my opinion it’s all about packaging and some sort of convenience.

#### Example 2 – BDD Specifications

If you are familiar with Behaviour-Driven Development, you know that there can be multiple specifications for a single SUT (system under test). The most common and efficient way to achieve it, is to break it into separate classes, extending some sort of base spec for a particular SUT.

```
<pre style="border-bottom-style: none; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: white; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px"><span style="color: #606060">   1:</span> <span style="color: #0000ff">public</span> <span style="color: #0000ff">abstract</span> <span style="color: #0000ff">class</span> DomainService_Specs : ContextSpecification&lt;IDomainService&gt;</pre>
```
```
<pre style="border-bottom-style: none; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: #f4f4f4; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px"><span style="color: #606060">   2:</span> {</pre>
```
```
<pre style="border-bottom-style: none; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: white; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px"><span style="color: #606060">   3:</span>     <span style="color: #0000ff">protected</span> IDomainService system_udner_test;</pre>
```
```
<pre style="border-bottom-style: none; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: #f4f4f4; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px"><span style="color: #606060">   4:</span>     <span style="color: #008000">// ...</span></pre>
```
```
<pre style="border-bottom-style: none; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: white; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px"><span style="color: #606060">   5:</span> }</pre>
```
```
<pre style="border-bottom-style: none; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: #f4f4f4; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px"><span style="color: #606060">   6:</span>&#160; </pre>
```
```
<pre style="border-bottom-style: none; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: white; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px"><span style="color: #606060">   7:</span> <span style="color: #0000ff">public</span> <span style="color: #0000ff">class</span> When_DomainService_is_asked_to_to_deliver_a_message_and_exception_is_thrown : DomainService_Specs</pre>
```
```
<pre style="border-bottom-style: none; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: white; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px"><span style="color: #606060">   9:</span>     [Observation]</pre>
```
```
<pre style="border-bottom-style: none; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: #f4f4f4; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px"><span style="color: #606060">  10:</span>     <span style="color: #0000ff">public</span> <span style="color: #0000ff">void</span> Should_recover_and_log_exception()</pre>
```
```
<pre style="border-bottom-style: none; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: white; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px"><span style="color: #606060">  11:</span>     {}</pre>
```
```
<pre style="border-bottom-style: none; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: #f4f4f4; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px"><span style="color: #606060">  12:</span>&#160; </pre>
```
```
<pre style="border-bottom-style: none; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: white; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px"><span style="color: #606060">  13:</span>     [Observation]</pre>
```
```
<pre style="border-bottom-style: none; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: #f4f4f4; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px"><span style="color: #606060">  14:</span>     <span style="color: #0000ff">public</span> <span style="color: #0000ff">void</span> Should_do_something_else()</pre>
```
```
<pre style="border-bottom-style: none; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: white; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px"><span style="color: #606060">  15:</span>     {}</pre>
```
```
<pre style="border-bottom-style: none; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: #f4f4f4; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px"><span style="color: #606060">  16:</span> }</pre>
```
```
<pre style="border-bottom-style: none; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: white; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px"><span style="color: #606060">  17:</span>&#160; </pre>
```
```
<pre style="border-bottom-style: none; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: #f4f4f4; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px"><span style="color: #606060">  18:</span> <span style="color: #0000ff">public</span> <span style="color: #0000ff">class</span> When_DomainService_is_asked_to_to_find_a_message_by_sender : DomainService_Specs</pre>
```
```
<pre style="border-bottom-style: none; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: white; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px"><span style="color: #606060">  19:</span> {</pre>
```
```
<pre style="border-bottom-style: none; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: #f4f4f4; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px"><span style="color: #606060">  20:</span>     [Observation]</pre>
```
```
<pre style="border-bottom-style: none; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: white; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px"><span style="color: #606060">  21:</span>     <span style="color: #0000ff">public</span> <span style="color: #0000ff">void</span> Should_do_this()</pre>
```
```
<pre style="border-bottom-style: none; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: #f4f4f4; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px"><span style="color: #606060">  22:</span>     {}</pre>
```
```
<pre style="border-bottom-style: none; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: white; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px"><span style="color: #606060">  23:</span>&#160; </pre>
```
```
<pre style="border-bottom-style: none; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: #f4f4f4; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px"><span style="color: #606060">  24:</span>     [Observation]</pre>
```
```
<pre style="border-bottom-style: none; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: white; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px"><span style="color: #606060">  25:</span>     <span style="color: #0000ff">public</span> <span style="color: #0000ff">void</span> Should_do_that()</pre>
```
```
<pre style="border-bottom-style: none; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: #f4f4f4; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px"><span style="color: #606060">  26:</span>     {}</pre>
```
```
<pre style="border-bottom-style: none; padding-bottom: 0px; line-height: 12pt; border-right-style: none; background-color: white; margin: 0em; padding-left: 0px; width: 100%; padding-right: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-top-style: none; color: black; font-size: 8pt; border-left-style: none; overflow: visible; padding-top: 0px"><span style="color: #606060">  27:</span> }</pre>
```

We could potentially break the specs into multiple files, but is it worth it?

#### The Reason

Before making a blind assumption that a best practice is always good thing to apply, always look for the reason(s) it came to existence. Googling why Java had this best practice was an interesting finding ([The Java Language Specification](http://java.sun.com/docs/books/jls/third_edition/html/packages.html#26783)):

> When packages are stored in a file system (�7.2.1), the host system may choose to enforce the restriction that it is a compile-time error if a type is not found in a file under a name composed of the type name plus an extension (such as .java or .jav) if either of the following is true:
> ```
> <br /></p>
> ```
> 
> \* The type is referred to by code in other compilation units of the package in which the type is declared.
> ```
> <br /></p>
> ```
> 
> \* The type is declared public (and therefore is potentially accessible from code in other packages).
> ```
> <br /></p>
> ```
> 
> This restriction implies that there must be at most one such type per compilation unit. This restriction makes it easy for a compiler for the Java programming language or an implementation of the Java virtual machine to find a named class within a package; for example, the source code for a public type wet.sprocket.Toad would be found in a file Toad.java in the directory wet/sprocket, and the corresponding object code would be found in the file Toad.class in the same directory.

It is obvious from the extract that the main reason behind the “best practice” was a technical optimization, and not OO principle implementation (like someone might raise up, Separation of Concerns, for example).

#### Conclusion

Java / C# (.NET) is a bit of a holly war. If you drop who borrowed what and when, you find that there’s an attempt to make a better development environment, and each attempt is packaged with the best practices considered to be “the best” at a time of product development. When product is outdated, or lagging behind, some will try to justify false best practices as best practices of even today. Be practical, search for the reasons, and make your decisions. Make sure you get the best out of the best practice, and not limited by it.

PS: Oh, and you can always convert to C# – proven to be more fun :)


