---
title: Too Loosely Coupled Code
slug: too-loosely-coupled-code
date: '2008-06-10T02:41:49'
updated: '2008-06-10T02:41:49'
draft: false
tags:
- OO
- Patterns
- TDD
author: Sean Feldman
---


***Strive for loosely coupled designs between objects that interact.*** 

By minimizing the knowledge one class has of another, you decrease dependency between those classes. Independent classes provide more flexibility in design.

Does this mean your application becomes more difficult to understand? Yes to a certain degree. You have to understand a few things before trying to work with loosely coupled code, things like the idea behind this principle. Why coupling is bad in first place. Determine how coupled your code that you normally created. Why you need loosely coupled code (or "what's in it for me").

One of the benefits of TDD I figured out for myself is that it forces you (yes, forces) to stick to the loosely coupled design. ***Program to an interface, not an implementation.*** By defining interface/contract first, and deferring it's implementation for later, you defer the concrete implementation of other components that are not the primarily target at the moment. That is a loose coupling, since you minimize the dependency on details of those components. ***Depend upon abstractions. Do not depend upon concrete classes.*** Interface is the abstraction, allowing to substitute implementer of it. Combined with ***Dependency Injection Principle***, you achieve a true loose coupling.

So the code like the one at the bottom (that doesn't really do anything significant) is loosely coupled to the component of type IComponentA, which is an abstraction. We don't know who is the implementer of this contract unless look into either a startup code or configuration file that sets the implementers for the contracts.

How difficult to learn that from looking briefly at the code? Probably not the easiest task. But you would never get it in first place, without understanding the principles. So saying that the code is 'hard to trace' indicated that there's no understanding of the principles. When you understand what DependencyResolver is, and concepts it implements, you immediately understand what the chained constructor is doing. TDD is forcing to expose the 2nd (parameterized) constructor for easier dependency supply. You could configure DependencyResolver for tests, but then it adds complexity to the testing.

So my question is can code be too loosely, or your code is so coupled, that anything else is difficult to digest?

```

   1:  public class ComponentB : IComponentB
   2:  {
   3:      private IComponentA dependency;
   4:
   5:      public ComponentB() :
   6:            this(DependencyResolver.GetImplementationOf())
```
{}
```
7:      public ComponentB(IComponentA dependency)
   8:      {
   9:         this.dependency = dependency;
  10:      }
  11:   
  12:      public void SomeFunctionality(string param)
  13:      {
  14:         var result =
```
dependency.OperationDefinedByDependencyContract(param);
```
15:         return DoSomethingWith(result);
  16:      }
  17:  }

```

