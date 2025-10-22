---
title: Strict Mocks - Thoughts
slug: strict-mocks-thoughts
date: '2009-03-14T04:09:43'
updated: '2009-03-14T04:09:43'
draft: false
tags:
- TDD
author: Sean Feldman
---


Today we had a discussion about having strict mocks for all of our dependencies in code. Reason - to force the tests to serve as a safety net for production code. I will try to explain pros  and cons of this approach from the point of view myself is found.

Why not to have strict mocks all over the place?

* Too much of intimacy with production code - test becomes the production code line by line
* Painful refactoring - how many times the same code is invoked, etc
* Behaviour Driven Development becomes impossible (single observation rather than multiple ones)

Why would one like to have all mocks as strict mocks?

* Safety net - change in code causes tests to fail right away
* Simplicity, as opposed to the complexity generated when trying to do BDD with spec based testing

What I am asking, is wouldn't the fact of making all mocks strict cause tests to have more than one responsibility? Rather that to have a single one - test if production code is failing or not, it will also have the responsibility of serving as a security net to prevent developers from starting code from production code and not tests first.

Would it make sense to read

 
```
dependency.VerifyAllExpectations();
```

vs.

```
<pre style="padding-right: 0px; padding-left: 0px; font-size: 8pt; padding-bottom: 0px; margin: 0em; overflow: visible; width: 100%; color: black; border-top-style: none; line-height: 12pt; padding-top: 0px; font-family: consolas, &#39;Courier New&#39;, courier, monospace; border-right-style: none; border-left-style: none; background-color: white; border-bottom-style: none">dependency.AssertWasToldTo(x =&gt; x.SomeBehaviour());</pre>
```

Not sure.

I can definitely see the benefit of forcing strict mocks to force people to get into habit of testing properly, but beyond that, it is a meter of team agreement to adhere to the coding style (tests first). None can ensure that code will go into repository with accompanying tests or tests will necessarily be good. Strict mocks should definitely not be used to pursuit that particular goal.

Share your opinion and experience with our team, feel free to comment.


