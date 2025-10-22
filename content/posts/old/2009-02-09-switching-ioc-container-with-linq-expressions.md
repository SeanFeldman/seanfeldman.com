---
title: Switching IoC Container with LINQ Expressions
slug: switching-ioc-container-with-linq-expressions
date: '2009-02-09T04:51:00'
updated: '2009-02-09T04:51:00'
draft: false
tags:
- C#
- Patterns
author: Sean Feldman
---


Several last projects I used a simple IoC container, leveraging Activator.CreateInstance(type). The main reason - simplicity. Once there was a need to go to a higher level, I would switch to Windsor Container. One of the projects used Unity. The only issue was that I would always have to do some customization to my container (or DependencyResolver), which is nothing but a static gateway.

What I have decided, is that I do not want to invest effort in something that was working before just because the underlying implementation of container has changed. The container engine might be changed, but my code should not (OCP?). Therefore, DependencyResolver had to be coded slightly different. To make it possible, I decided to go with the LINQ Expressions. It allows to pass code in data structures, and thus allows to manipulate how to execute the code.

For demonstration purposes, I will only demonstrate the simple case, more complex cases are feasible as well.

 
```
   1: public interface IService
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   2:</span> {</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   3:</span>     <span style="color: rgb(0, 0, 255);">void</span> DoSomething();</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   4:</span> }</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   5:</span>&nbsp; </pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   6:</span> <span style="color: rgb(0, 0, 255);">public</span> <span style="color: rgb(0, 0, 255);">class</span> ServiceImpl : IService </pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   7:</span> {</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   8:</span>     <span style="color: rgb(0, 0, 255);">public</span> <span style="color: rgb(0, 0, 255);">void</span> DoSomething()</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   9:</span>     {</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  10:</span>         Console.WriteLine(<span style="color: rgb(0, 96, 128);">"ServiceImpl"</span>);</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  11:</span>     }</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  12:</span> }</pre>
```

DependencyResolver (which is static gateway) is

```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   1:</span> <span style="color: rgb(0, 0, 255);">public</span> <span style="color: rgb(0, 0, 255);">static</span> <span style="color: rgb(0, 0, 255);">class</span> DependencyResolver</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   2:</span> {</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   3:</span>     <span style="color: rgb(0, 0, 255);">private</span> <span style="color: rgb(0, 0, 255);">static</span> IDependencyResolver <b>instance</b> = <span style="color: rgb(0, 0, 255);">new</span> LambdaDependencyResolver();</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   4:</span>&nbsp; </pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   5:</span>     <span style="color: rgb(0, 0, 255);">public</span> <span style="color: rgb(0, 0, 255);">static</span> <span style="color: rgb(0, 0, 255);">void</span> InitializeWith(IDependencyResolver resolver)</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   6:</span>     {</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   7:</span>         instance = resolver;</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   8:</span>     }</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   9:</span>&nbsp; </pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  10:</span>     <span style="color: rgb(0, 0, 255);">public</span> <span style="color: rgb(0, 0, 255);">static</span> <span style="color: rgb(0, 0, 255);">void</span> Register&lt;ContractType&gt;(Expression&lt;Func&lt;ContractType&gt;&gt; func)</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  11:</span>     {</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  12:</span>         instance.Register(func);</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  13:</span>     }</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  14:</span>&nbsp; </pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  15:</span>     <span style="color: rgb(0, 0, 255);">public</span> <span style="color: rgb(0, 0, 255);">static</span> ContractType Resolve&lt;ContractType&gt;()</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  16:</span>     {</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  17:</span>         <span style="color: rgb(0, 0, 255);">return</span> instance.Resolve&lt;ContractType&gt;();</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  18:</span>     }</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  19:</span> }</pre>
```

By default, LambdaDependencyResolver is going to be used. Registration is done by passing in an Expression<Func<ContractType>> that is nothing but a function that returns a ContractType implementer. The idea to wrap it with Expression, so that the instance (a particular dependency resolver implementation) would take care of the details based on how it works.

IDependencyResolver code

```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   1:</span> <span style="color: rgb(0, 0, 255);">public</span> <span style="color: rgb(0, 0, 255);">interface</span> IDependencyResolver</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   2:</span> {</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   3:</span>     <span style="color: rgb(0, 0, 255);">void</span> Register&lt;ContractType&gt;(Expression&lt;Func&lt;ContractType&gt;&gt; func);</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   4:</span>     ContractType Resolve&lt;ContractType&gt;();</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   5:</span> }</pre>
```

LambdaDependencyResolver code

```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   1:</span> <span style="color: rgb(0, 0, 255);">public</span> <span style="color: rgb(0, 0, 255);">class</span> LambdaDependencyResolver : IDependencyResolver</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   2:</span> {</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   3:</span>     <span style="color: rgb(0, 0, 255);">private</span> Dictionary&lt;Type, <span style="color: rgb(0, 0, 255);">object</span>&gt; dictionary = <span style="color: rgb(0, 0, 255);">new</span> Dictionary&lt;Type, <span style="color: rgb(0, 0, 255);">object</span>&gt;();</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   4:</span>&nbsp; </pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   5:</span>     <span style="color: rgb(0, 0, 255);">public</span> <span style="color: rgb(0, 0, 255);">void</span> Register&lt;ContractType&gt;(Expression&lt;Func&lt;ContractType&gt;&gt; func)</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   6:</span>     {</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   7:</span>         <span style="color: rgb(0, 0, 255);">if</span> (dictionary.ContainsKey(<span style="color: rgb(0, 0, 255);">typeof</span>(ContractType)))</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   8:</span>         {</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   9:</span>             <span style="color: rgb(0, 0, 255);">throw</span> <span style="color: rgb(0, 0, 255);">new</span> InvalidOperationException(<span style="color: rgb(0, 0, 255);">typeof</span>(ContractType).FullName + <span style="color: rgb(0, 96, 128);">" was added already to container."</span>);</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  10:</span>         }</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  11:</span>&nbsp; </pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  12:</span>         dictionary.Add(<span style="color: rgb(0, 0, 255);">typeof</span>(ContractType), func);</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  13:</span>     }</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  14:</span>&nbsp; </pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  15:</span>     <span style="color: rgb(0, 0, 255);">public</span> ContractType Resolve&lt;ContractType&gt;()</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  16:</span>     {</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  17:</span>         <span style="color: rgb(0, 0, 255);">if</span> (!dictionary.ContainsKey(<span style="color: rgb(0, 0, 255);">typeof</span>(ContractType)))</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  18:</span>         {</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  19:</span>             <span style="color: rgb(0, 0, 255);">throw</span> <span style="color: rgb(0, 0, 255);">new</span> InvalidOperationException(<span style="color: rgb(0, 0, 255);">typeof</span>(ContractType).FullName + <span style="color: rgb(0, 96, 128);">" was not found in container."</span>);</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  20:</span>         }</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  21:</span>&nbsp; </pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  22:</span>         <b>var expression = dictionary[<span style="color: rgb(0, 0, 255);">typeof</span> (ContractType)];</b></pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  23:</span>         <b>var compiledLambda = ((Expression&lt;Func&lt;ContractType&gt;&gt;)expression).Compile();</b></pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  24:</span>       <b>  <span style="color: rgb(0, 0, 255);">return</span> compiledLambda.Invoke(<span style="color: rgb(0, 0, 255);">this</span>);</b></pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  25:</span>     }</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  26:</span> }</pre>
```

The usage

```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   1:</span> DependencyResolver.Register&lt;IService&gt;(() =&gt; <span style="color: rgb(0, 0, 255);">new</span> ServiceImpl());</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   2:</span> var service = DependencyResolver.Resolve&lt;IService&gt;();</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   3:</span> service.DoSomething();</pre>
```

It's working, great. Some time later, we need to switch to some 3rd party container, and we don't want to change our code that relies on DependencyResolver. This is where Expressions are handy. I have used Unity container, but that could be StructureMap, Windsor Container, or anything else.

```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   1:</span> <span style="color: rgb(0, 0, 255);">public</span> <span style="color: rgb(0, 0, 255);">class</span> UnityDependencyResolver : IDependencyResolver</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   2:</span> {</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   3:</span>     <span style="color: rgb(0, 0, 255);">private</span> UnityContainer container = <span style="color: rgb(0, 0, 255);">new</span> UnityContainer();</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   4:</span>&nbsp; </pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   5:</span>     <span style="color: rgb(0, 0, 255);">public</span> <span style="color: rgb(0, 0, 255);">void</span> Register&lt;ContractType&gt;(Expression&lt;Func&lt;ContractType&gt;&gt; func)</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   6:</span>     {</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   7:</span>         <b>var newExpression = (NewExpression)func.Body;</b></pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   8:</span>         <b>container.RegisterType(<span style="color: rgb(0, 0, 255);">typeof</span> (ContractType), newExpression.Type, <span style="color: rgb(0, 0, 255);">new</span> InjectionMember[] {});</b></pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   9:</span>     }</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  10:</span>&nbsp; </pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  11:</span>     <span style="color: rgb(0, 0, 255);">public</span> ContractType Resolve&lt;ContractType&gt;()</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  12:</span>     {</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  13:</span>         <span style="color: rgb(0, 0, 255);">return</span> (ContractType) container.Resolve(<span style="color: rgb(0, 0, 255);">typeof</span>(ContractType));</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  14:</span>     }</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  15:</span> }</pre>
```

Bolded code in LambdaDependencyResolver and UnityDependencyResolver is simply leveraging LINQ Expressions to make it all work. You can definitely make it more sophisticated and elegant as needed.


