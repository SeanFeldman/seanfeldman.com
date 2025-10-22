---
title: Test Helpers and Fluent Interfaces
slug: test-helpers-and-fluent-interfaces
date: '2008-11-29T08:06:00'
updated: '2008-11-29T08:06:00'
draft: false
tags:
- Agile
- OO
- TDD
author: Sean Feldman
---


Today was a great day. One of the things we do with the team is experiment how we write our test. Experimenting seems the most effective way of figuring out what should be our testing approach. At this point we are mostly doing specification driven tests (unit tests).

We had a few questions in regards to code duplication and keeping it DRY and self-explanatory at the same time, hiding no important details. At the same time overwhelming details should not be annoying the test reader/explorer.

One of the things that is crucial, is to keep the spot light on the most important in the test – subject under test (SUT) and what are the assertions about it behavior/state. Anything else is secondary, but not unimportant. Therefore, anything that is not primarily should be communicated in the simplest manner and preferably in human language with simplistic logic in order not to steal the scene from SUT and result.

The component my pair partner and I were working on was a strategy component, based on time. A very simple one with the following rules:

1. A report can be issued to a client if reporting time is within 10 minutes in the past from the current system’s time
2. Anything that outside of the time frame defined in #1 means no report issued to the client

Simple one.

First step was to abstract the System.DateTime object in order to manipulate the current time. There are plenty of resources on that, and despite the fact that I loved a particular testing implementation proposed by Oren [here](http://ayende.com/Blog/archive/2008/07/07/Dealing-with-time-in-tests.aspx), we ended up doing contract based implementation and usage of an instance based custom SystemDateTime solution.

 
```
   1: public interface ISystemDateTime
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   2:</span> {</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   3:</span>     DateTime Now { get; }</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   4:</span> }</pre>
```


```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   1:</span> <span style="color: rgb(0, 0, 255);">public</span> <span style="color: rgb(0, 0, 255);">class</span> SystemDateTime : ISystemDateTime </pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   2:</span> {</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   3:</span>     <span style="color: rgb(0, 0, 255);">public</span> DateTime Now</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   4:</span>     {</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   5:</span>         get { <span style="color: rgb(0, 0, 255);">return</span> DateTime.Now; }</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   6:</span>     }</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   7:</span> }</pre>
```

Once that  was in place, we started to craft the tests for the strategy object. But something was wrong.

```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   1:</span> [Concern(<span style="color: rgb(0, 0, 255);">typeof</span>(TimeBasedReportExecutionStrategy))]</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   2:</span>   [TestFixture]</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   3:</span>   <span style="color: rgb(0, 0, 255);">public</span> <span style="color: rgb(0, 0, 255);">class</span> When_time_based_report_execution_strategy_is_asked_to_determine_can_report_be_executed_for_a_given_client_information : SpecificationContext&lt;IReportExecutionStrategy&gt;</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   4:</span>   {</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   5:</span>       <span style="color: rgb(0, 0, 255);">private</span> ISystemDateTime systemDateTime;</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   6:</span>       <span style="color: rgb(0, 0, 255);">private</span> DateTime clientReportExecutionTime = <span style="color: rgb(0, 0, 255);">new</span> DateTime(2008, 1, 1, 12, 0, 0);</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   7:</span>       </pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   8:</span>       <span style="color: rgb(0, 0, 255);">protected</span> <span style="color: rgb(0, 0, 255);">override</span> IReportExecutionStrategy EstablishContext()</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   9:</span>       {</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  10:</span>           systemDateTime = Stub&lt;ISystemDateTime&gt;();</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  11:</span>&nbsp; </pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  12:</span>           <span style="color: rgb(0, 0, 255);">return</span> <span style="color: rgb(0, 0, 255);">new</span> TimeBasedReportExecutionStrategy(systemDateTime);</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  13:</span>       }</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  14:</span>&nbsp; </pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  15:</span>       <span style="color: rgb(0, 0, 255);">protected</span> <span style="color: rgb(0, 0, 255);">override</span> <span style="color: rgb(0, 0, 255);">void</span> BecauseOf(){}</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  16:</span>&nbsp; </pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  17:</span>       [Test]</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  18:</span>       <span style="color: rgb(0, 0, 255);">public</span> <span style="color: rgb(0, 0, 255);">void</span> Should_allow_report_execution_when_escalation_time_is_within_executable_threshold()</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  19:</span>       {</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  20:</span>           systemDateTime.Stub(t =&gt; { var readProperty = t.Now; })</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  21:</span>               .Return(clientReportExecutionTime.AddMinutes(5));</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  22:</span>&nbsp; </pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  23:</span>           var result = system_under_test.CanIssueReportFor(<span style="color: rgb(0, 0, 255);">new</span> ClientEscalationInfo(<span style="color: rgb(0, 96, 128);">"client_id"</span>, clientReportExecutionTime, <span style="color: rgb(0, 96, 128);">"recipients"</span>));</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  24:</span>           result.should_be_true();</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  25:</span>       }</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  26:</span> }</pre>
```

What bothered us is the expression that was setting up a stubbed version of the  system current time, “clientReportExecutionTime.AddMinutes(5)”. It was too much of information to process just to determine that we want to test what happens when SUT has a client report time that is less than 10 minutes old.

So we started to think, and gosh I love pair programming. I know it’s unnecessary to promote it any further, but just can’t stop getting excited about pair programming I recall “the days of silo”. And if you read these lines and think this dude went from the “days of silo” to the “days of psycho”, then yes, I am mad about it :)

Anyhow, this test was not the only one, we wanted to test more than 10 minutes in the past, as well as what happens when report time is in future, etc. How we can make it as clear as possible? This is where we went to the Test Helper class pattern. It was nice, but still not what we wanted, we wanted something that would feel natural. Next step was to think towards the natural syntax – fluent interface. After a few iterations, name changes and debates, this is what we got:

```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   1:</span> [Concern(<span style="color: rgb(0, 0, 255);">typeof</span>(TimeBasedReportExecutionStrategy))]</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   2:</span>     [TestFixture]</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   3:</span>     <span style="color: rgb(0, 0, 255);">public</span> <span style="color: rgb(0, 0, 255);">class</span> When_time_based_report_execution_strategy_is_asked_to_determine_can_report_be_executed_for_a_given_client_information : SpecificationContext&lt;IReportExecutionStrategy&gt;</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   4:</span>     {</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   5:</span>         <span style="color: rgb(0, 0, 255);">private</span> ISystemDateTime systemDateTime;</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   6:</span>         <span style="color: rgb(0, 0, 255);">private</span> DateTime clientReportExecutionTime = <span style="color: rgb(0, 0, 255);">new</span> DateTime(2008, 1, 1, 12, 0, 0);</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   7:</span>         </pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   8:</span>         <span style="color: rgb(0, 0, 255);">protected</span> <span style="color: rgb(0, 0, 255);">override</span> IReportExecutionStrategy EstablishContext()</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   9:</span>         {</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  10:</span>             systemDateTime = Stub&lt;ISystemDateTime&gt;();</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  11:</span>&nbsp; </pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  12:</span>             <span style="color: rgb(0, 0, 255);">return</span> <span style="color: rgb(0, 0, 255);">new</span> TimeBasedReportExecutionStrategy(systemDateTime);</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  13:</span>         }</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  14:</span>&nbsp; </pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  15:</span>         <span style="color: rgb(0, 0, 255);">protected</span> <span style="color: rgb(0, 0, 255);">override</span> <span style="color: rgb(0, 0, 255);">void</span> BecauseOf(){}</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  16:</span>&nbsp; </pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  17:</span>         [Test]</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  18:</span>         <span style="color: rgb(0, 0, 255);">public</span> <span style="color: rgb(0, 0, 255);">void</span> Should_allow_report_execution_when_escalation_time_is_within_executable_threshold()</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  19:</span>         {</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  20:</span>             systemDateTime.Stub(t =&gt; { var readProperty = t.Now; })</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  21:</span>                 .Return(TestHelper.When(clientReportExecutionTime).Is(5).minutes_in_the_past);</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  22:</span>&nbsp; </pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  23:</span>             var result = system_under_test.CanIssueReportFor(<span style="color: rgb(0, 0, 255);">new</span> ClientEscalationInfo(<span style="color: rgb(0, 96, 128);">"client_id"</span>, clientReportExecutionTime, <span style="color: rgb(0, 96, 128);">"recipients"</span>));</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  24:</span>             result.should_be_true();</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  25:</span>         }</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  26:</span>&nbsp; </pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  27:</span>         [Test]</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  28:</span>         <span style="color: rgb(0, 0, 255);">public</span> <span style="color: rgb(0, 0, 255);">void</span> Should_not_allow_report_execution_when_escalation_time_is_within_executable_threshold_in_the_future()</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  29:</span>         {</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  30:</span>             systemDateTime.Stub(t =&gt; { var readProperty = t.Now; })</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  31:</span>                 .Return(TestHelper.When(clientReportExecutionTime).Is(5).minutes_in_the_future);</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  32:</span>&nbsp; </pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  33:</span>             var result = system_under_test.CanIssueReportFor(<span style="color: rgb(0, 0, 255);">new</span> ClientEscalationInfo(<span style="color: rgb(0, 96, 128);">"client_id"</span>, clientReportExecutionTime, <span style="color: rgb(0, 96, 128);">"recipients"</span>));</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  34:</span>             result.should_be_false();</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  35:</span>         }</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  36:</span>&nbsp; </pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  37:</span>         [Test]</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  38:</span>         <span style="color: rgb(0, 0, 255);">public</span> <span style="color: rgb(0, 0, 255);">void</span> Should_not_allow_report_execution_when_escalation_time_is_outside_of_executable_threshold_in_the_past()</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  39:</span>         {</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  40:</span>             systemDateTime.Stub(t =&gt; { var readProperty = t.Now; })</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  41:</span>                 .Return(TestHelper.When(clientReportExecutionTime).Is(11).minutes_in_the_past);</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  42:</span>             var result = system_under_test.CanIssueReportFor(<span style="color: rgb(0, 0, 255);">new</span> ClientEscalationInfo(<span style="color: rgb(0, 96, 128);">"client_id"</span>, clientReportExecutionTime, <span style="color: rgb(0, 96, 128);">"recipients"</span>));</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  43:</span>&nbsp; </pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  44:</span>             result.should_be_false();</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  45:</span>         }</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  46:</span>&nbsp; </pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  47:</span>         [Test]</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  48:</span>         <span style="color: rgb(0, 0, 255);">public</span> <span style="color: rgb(0, 0, 255);">void</span> Should_not_allow_report_execution_when_escalation_time_is_outside_of_executable_threshold_in_the_future()</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  49:</span>         {</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  50:</span>             systemDateTime.Stub(t =&gt; { var readProperty = t.Now; })</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  51:</span>                 .Return(TestHelper.When(clientReportExecutionTime).Is(11).minutes_in_the_future);</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  52:</span>&nbsp; </pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  53:</span>             var result = system_under_test.CanIssueReportFor(<span style="color: rgb(0, 0, 255);">new</span> ClientEscalationInfo(<span style="color: rgb(0, 96, 128);">"client_id"</span>, clientReportExecutionTime, <span style="color: rgb(0, 96, 128);">"recipients"</span>));</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  54:</span>&nbsp; </pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  55:</span>             result.should_be_false();</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  56:</span>         }</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  57:</span> }</pre>
```

The TestHelper in this case was a private class that implemented the fluent interface.

```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   1:</span> <span style="color: rgb(0, 0, 255);">private</span> <span style="color: rgb(0, 0, 255);">class</span> TestHelper</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   2:</span> {</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   3:</span>     <span style="color: rgb(0, 0, 255);">private</span> DateTime anchorTime;</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   4:</span>     <span style="color: rgb(0, 0, 255);">private</span> <span style="color: rgb(0, 0, 255);">int</span> minutesToUse;</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   5:</span>&nbsp; </pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   6:</span>     <span style="color: rgb(0, 0, 255);">private</span> TestHelper(DateTime anchorTime)</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   7:</span>     {</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">   8:</span>         <span style="color: rgb(0, 0, 255);">this</span>.anchorTime = anchorTime;</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">   9:</span>     }</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  10:</span>&nbsp; </pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  11:</span>     <span style="color: rgb(0, 0, 255);">public</span> <span style="color: rgb(0, 0, 255);">static</span> TestHelper When(DateTime anchorTime)</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  12:</span>     {</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  13:</span>         <span style="color: rgb(0, 0, 255);">return</span> <span style="color: rgb(0, 0, 255);">new</span> TestHelper(anchorTime);</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  14:</span>     }</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  15:</span>&nbsp; </pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  16:</span>     <span style="color: rgb(0, 0, 255);">public</span> TestHelper Is(<span style="color: rgb(0, 0, 255);">int</span> minutes)</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  17:</span>     {</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  18:</span>         minutesToUse = minutes;</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  19:</span>         <span style="color: rgb(0, 0, 255);">return</span> <span style="color: rgb(0, 0, 255);">this</span>;</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  20:</span>     }</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  21:</span>&nbsp; </pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  22:</span>     <span style="color: rgb(0, 0, 255);">public</span> DateTime minutes_in_the_future</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  23:</span>     {</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  24:</span>         get</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  25:</span>         {</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  26:</span>             <span style="color: rgb(0, 0, 255);">return</span> anchorTime.AddMinutes(minutesToUse);</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  27:</span>         }</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  28:</span>     }</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  29:</span>&nbsp; </pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  30:</span>     <span style="color: rgb(0, 0, 255);">public</span> DateTime minutes_in_the_past</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  31:</span>     {</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  32:</span>         get</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  33:</span>         {</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  34:</span>             <span style="color: rgb(0, 0, 255);">return</span> anchorTime.AddMinutes(-minutesToUse);</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  35:</span>         }</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: rgb(244, 244, 244);"><span style="color: rgb(96, 96, 96);">  36:</span>     }</pre>
```
```
<pre style="border-style: none; margin: 0em; padding: 0px; overflow: visible; font-size: 8pt; width: 100%; color: black; line-height: 12pt; font-family: consolas,'Courier New',courier,monospace; background-color: white;"><span style="color: rgb(96, 96, 96);">  37:</span> }</pre>
```

An interesting observation we made for ourselves was that just by doing it this way, not only we simplified tests reading, but also have taken the concern of date/time math out of the real concern – testing the real SUT, the strategy.

**Conclusions**

1. I am not a 100% confident this is the best way to implement a test, but this is something that my team likes, and we will keep exploring it and getting better in expressiveness in our tests.
2. Tests should be ‘clean’ ([according to Uncle Bob](http://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)) or they are not communicating the idea, become un-maintainable down the road, and abandoned eventually.
3. If it feels wrong, it is wrong. Do everything it takes to feel right.

