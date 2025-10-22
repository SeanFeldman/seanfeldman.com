---
title: The Art of Unit Testing – The Book
slug: the-art-of-unit-testing-the-book
date: '2009-06-24T10:54:00'
updated: '2009-06-24T10:54:00'
draft: false
tags:
- Books
author: Sean Feldman
---


I have finished reading the book and wanted to write a short review, but [![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_2E19B79A.png "image")](http://www.amazon.ca/Art-Unit-Testing-Examples-Net/dp/1933988274) the best I could come up with is a list of cons and pros. Lame, I know, but this will give you a hint at least.

##### pros

1. Smooth introduction, complexity is added step by step
2. “Strict mocks are causing brittle tests” – more than that, it causes to get into the private details of execution, rather than overall design and behaviour
3. “Method strings are bad inside tests” – absolutely
4. “Mapping tests to projects” – very right decision to spend time on the subject and show a right example
5. One-test-class-per-feature pattern is mentioned (music to BDD fan ears)
6. Writing maintainable tests – critical topic that was covered
7. DRY in test code – in general I agree that an unnecessary duplication should be removed from the test code. But there’s a think line that should not be crossed – tests should be readable and maintainable. For that, duplication sometimes is necessary. This is the less evil for a bigger cause – readability and maintainability.
8. Row testing is showed
9. “Integrating unit testing into the organization” – a very, very useful chapter, especially if you have to pioneer the field at your work place. Personally, I wish I would read this long time ago.

##### cons

1. Tests naming conventions
2. Too much is dedicated to Stubs and manual Mocks
3. Chapter 5 - Isolation (mock object) framework is explained with Rhino.Mocks Record/Playback rather that AAA that is more natural

* Note: AAA sample is showed, but after Record/Playback, which IMHO is a wrong way of teaching it. AAA is more intuitive and sticks more than the opponent.

5. TypeMock promotion – [Roy](http://weblogs.asp.net/rosherove/) is working for TypeMock that is a commercial tool. He could definitely use an OSS framework to show AAA mocking framework, like [Moq](http://code.google.com/p/moq/) framework. In an absence of a free tool, I would accept TypeMock as an example, or as a part of available commercial tools. (Page 130 shows the distribution of popularity, and Rhino.Mocks with Moq are the two most popular free mocking frameworks). This was a promo for the tool… not nice.

* Note: I am not a big fan of the fluent naming TypeMock is using. *Isolate.Fake*.Instance<IWebService>() is two verbs that are not intuitive.

7. Naming conventions for tests – both unit tests and integration tests are suffixed with a single word “Test”. I would rather distinguish and use context “Spec” and “Integration” as an example.
8. One-test-class-per-class pattern – for someone who’s doing BDD this is an anti-pattern. One big test class is a smell. It leads to brutal test code that is not only difficult to maintain, but even understand from it what it is doing. Very typical to the classical TDD.

* Note: Roy has provided a tip on this, politically correctly hinting that not everything from the big heads ([Meszaro](http://www.amazon.com/xUnit-Test-Patterns-Refactoring-Addison-Wesley/dp/0131495054) in this case) is always an absolute must.

10. Assertion with Extension Methods to improve tests readability was not showed at all

* Note: IMO *Assert.AreEqual(found, expected)* is confusing. I prefer to reveal intent with a code like *result.Should\_Be\_Equal\_To(expected);*

12. NO BDD SAMPLES – BAD BAD BAD. I strongly believe that just with classic TDD testing is not complete. BDD is the next step in the right direction, and skipping it entirely was a mistake.

##### Conclusions

If you are a newbie in TDD or just “checking it out” – go for this book, worth it. In case you already have experience in TDD/BDD, and you are doing it for a while, it will not add much to your tool belt. Either way, the book is welcomed, and I am excited that more and more of this kind of literature is becoming available for .NET developers. I only wish the next version will be written **BDD** style, right Roy? ;)


