---
title: naming_a_test
slug: writing-a-test
date: '2008-10-28T04:40:00'
updated: '2008-10-28T04:40:00'
draft: false
tags:
- TDD
author: Sean Feldman
---


Naming conventions is always brought up when a team is trying to standardize the way code is expressed. Tab size of 2 vs. size of 4, Camel case vs. Pascal case, blog opening on a new line vs. same line with expression, member fields prefixed vs. underscored vs. nothing, control names with Hungarian notation or without it. The list goes on and on. The truth is that this is really doesn't matter. I have learned to accept what team decides to go with and once you embrace the style it's all good. What really matters is the code being produces, not the size of the font it's printed in (well, probably not the best example, but you get the idea).

Testing is not an exception. Test code lives along with production code, yet we want to be able visually be able quickly identify it. Many individuals and team do it in various ways, but an interesting fact is that the influence of TDD/BDD has caused to be more "expressive". What I mean by "expressiveness" is the will to make it as close to the human language as possible to describe what are we testing and document it that way. I owe [Mo](http://mokhan.ca/blog/) a big one for giving me this insight and breaking it into small pieces so my tortoise brain could get it.

```
[Test]  
public void ShouldGetTheNumberOfHoursFromDays() {//..}
```

The example is somewhat cryptic. Reading this think is painful, yet compliant with CLR naming standards. On the other hand, having underscores, spices up the name:

```
[Test]  
public void should_get_the_number_of_hours_from_days() {//..}
```

Suddenly it's easier to read! Also the interesting part is that if we really wish, the test name now could be easily read by a home-grown utility and converted in some sort of documentation where underscores are omitted and readable sentences by human show up. Thanks to [JP](http://blog.jpboodhoo.com/) for entertaining with this idea during the course.

Now if we think about this, it makes even more sense to name this way test [![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/writing_a_test_13F20/image_thumb.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/writing_a_test_13F20/image_2.png)classes (or specifications). Next screenshot makes it really easy to see the benefits of underscored naming convention for the testing purposes.

*Note*: I agree that seeing all when\_\* is a bit weird, but there are ways to get over it and make sure that the tested class footprint is left. TestsOnAttribute or custom ConcernAttribute would do it. I welcome any other suggestions that would be less configuration for the team and more of a convention.

Also it looks very natural to keep this type of style to the rest of the testing code. For your judgement:

```
result.should_be_equal_to(expected);
```

over

```
Assert.AreEqual(expected, result);
```

As our team goes through the adventure of maturing our own naming conventions, we are opened and welcoming any thoughtful advises you can share. What would you consider to be a good practice and solid way of doing things, what would be discouraged. We want to learn from your experience!


