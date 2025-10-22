---
title: Tests Maintainability
slug: tests-maintainability
date: '2009-07-14T05:05:00'
updated: '2009-07-14T05:05:00'
draft: false
tags:
- TDD
author: Sean Feldman
---


Write your test code as you would write your production code. In my opinion, a few of the most critical things are:

* Understanding (Readability and clarity of what the code is doing)
* Easy of change (be able to reflect changes)
* Quick safety net (understand what goes wrong and why)

In [one](http://weblogs.asp.net/sfeldman/archive/2008/10/27/writing-a-test.aspx) of my previous posts, I have blogged about test naming conventions, that is popular among BDD adopters, and starts to pick up among classic-TDD followers as well. Seven months later, I can see where all the bullet items are missing in classical TDD, and present in BDD.

#### True story example

In BDD we have Specifications and Observations breakdown. The classical TDD is missing this aspect. So a specification like the follows,

 
```
   1: public class When_DomainService_is_asked_to_to_deliver_a_message_and_exception_is_thrown
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">   2:</span> {</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">   3:</span>     [Observation]</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">   4:</span>     <span style="color: #0000ff">public</span> <span style="color: #0000ff">void</span> Should_recover_and_log_exception()</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">   5:</span>     {}</pre>
```
```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: #f4f4f4; border-bottom-style: none"><span style="color: #606060">   6:</span> }</pre>
```

looks as next in classic TDD.

```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none"><span style="color: #606060">   1:</span> ShouldRecoverAndLogExceptionWhenDomainServiceThrowsFaultExceptionAndDeliveryQueueServiceThrowsFaultExceptionWhenAttemptingToDeliverMessage</pre>
```

Readability / clarity is definitely compromised. A single word of 138 characters looks a bit complex.

Ease of change is not quiet simple in classic TDD case – you first have to de-crypt what the test actually does before updating test/production code.

Safety net – in this case we are on a thin ice – developers who have a problem to “de-crypt” the test code to figure out what went wrong, will eventually end-up either disabling tests for new code, or worse, removing old tests as well. And that happened in the past.

> The moral of the post – BDD is all about the behaviour. Let the old habits of classic TDD-ism go away, accept that testing code is a first class citizen as the production code.


