---
title: Too Loosely Coupled Code – One Year Later
slug: too-loosely-coupled-code-one-year-later
date: '2009-10-07T02:00:00'
updated: '2009-10-07T02:00:00'
draft: false
tags:
- OO
- Patterns
- TDD
author: Sean Feldman
---


More than a year ago, I have posted a [blog entry](http://weblogs.asp.net/sfeldman/archive/2008/06/09/too-loosely-coupled-code.aspx) related to what I was trying to implement in one of the projects. Unfortunately, not my team could understand what I was trying to do, neither I was able to make myself clear. Either way, I ended up closing the blog with a question “*can code be too loosely (coupled), or your code is so coupled, that anything else is difficult to digest?*”. Now I can answer my own question question.

Today, my current team had a team learning session, when the latest project demonstration showed what are we doing with a [IoC](http://weblogs.asp.net/sfeldman/archive/2008/02/14/understanding-ioc-container.aspx) container we started to leverage ([StructureMap](http://structuremap.sourceforge.net/Default.htm)). The team is not the same one I had back a year+ ago. This team has also had **same** difficulty in the beginning – code that was too coupled. We have started from “Poor mans’ injection”,  moved to home-grown Dependency Resolver with a typical Startup Task, and now have reached the point, where a third party open-source IoC container is used. I think that could be achieved because:

* We worked on decoupling code, learning the pros and cons
* We got to the point were [SRP](http://en.wikipedia.org/wiki/Single_responsibility_principle) is followed
* We have got to the point were [Design by Contract](http://en.wikipedia.org/wiki/Design_by_contract) is almost entirely how we develop
* We have a complete [TDD](http://en.wikipedia.org/wiki/Test_driven_development) development in place

So why I could not root the idea in my previous team? Because it was way too early for my team mates and I was not ready to wait.

Oh, and how the code looks now? Even better than before ;)

```

public class ComponentB : IComponentB
{
  private IComponentA dependency;
 
  public ComponentB(IComponentA dependency)
  {
```
this.dependency = dependency;
```
}
 
  public void SomeFunctionality(string param)
  {
```
var result = dependency.OperationDefinedByDependencyContract(param);
return DoSomethingWith(result);
```
}
}

```

Benefits:

* [TDD/BDD](http://weblogs.asp.net/sfeldman/archive/2008/12/12/quot-hello-world-quot-tdd-style.aspx) development style is enforced better when there’s no default constructor with Dependency Resolver or Poor’s man injection
* No messy Startup Task that is a must when doing Dependency Resolver
* Can leverage smarts of IoC container to perform tasks on a massive scale (interceptors, events, etc)
* Easy way to verify if all dependencies are wired or not (contract based dependencies)

And as one commenter of the original blog post has asked correctly: “*The question might be more appropriately be, is the code self-documenting? Can someone who did not write the original code follow the logic and modify and maintain it?*”. The answer is: **it depends**.

You have to get to a certain level to answer Yes. Until you get to that level, the answer will always be No. In order for code to be self-documenting, it needs to be of high quality and accompanied with tests/specifications. In order to be modified, maintained, and logic followed by a person who did not write it, it has to have the listed above **AND** have the person to be at a certain level of skills.


