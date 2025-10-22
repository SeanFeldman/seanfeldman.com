---
title: Depend Upon Abstractions - reiteration.
slug: depend-upon-abstractions-reiteration
date: '2008-11-22T16:17:00'
updated: '2008-11-22T16:17:00'
draft: false
tags:
- OO
- TDD
author: Sean Feldman
---


I was reading through the [book](http://weblogs.asp.net/sfeldman/archive/2008/11/14/clean-code-a-handbook-of-agile-software-craftsmanship.aspx) when combined several subjects together, such as "help tests" and "error handling", and realized that the core "Depend upon abstraction.  Do not depend upon concretions." principle is underused by myself.

Normally, I apply this great principle when thinking of another not less good one - "Design to an interface and not an implementation". And usually it happens when I generate new pieces of code. But this can and should be applies to an existing code as well, especially if it's a 3rd party code. I am going to demo the concept along with the other subjects based on the book example, sorry for luck of 'creativity on an early weekend morning' :)

Lets pretend our code depends on the 3rd party component that has some strict rules about values it can operate on (for the sake of simplicity). It documents that 0 and 100 should never be used. Thirst thing is to verify this behaviour, document it and make sure we learn it and can verify the same behaviour or capture any changes in the next versions of the 3rd party component when we upgrade it (another reason to have learning/exploratory tests)

```

   1:   [TestsOn(typeof (ThirdPartyComponent))]
   2:    [TestFixture]
   3:    public class ThirdPartyComponent_LearningTests
   4:    {
   5:      [Test]
   6:      [ExpectedException(typeof(InitializationException))]
   7:      public void When_passing_zero_Should_get_an_exception()
   8:      {
   9:        var sut = new ThirdPartyComponent();
  10:        sut.ActOn(0);
  11:      }
  12:
  13:      [Test]
  14:      [ExpectedException(typeof(ExceptionalValueException))]
  15:      public void When_passing_a_hundred_Should_get_an_exception()
  16:      {
  17:        var sut = new ThirdPartyComponent();
  18:        sut.ActOn(100);
  19:      }
  20:    }

```

Result - behaviour verified and documented.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/DependUponAbstractionsreiteration_82B8/image_5.png)](http://gallio.org)

You can leave the job, knowing that someday someone will thank you for doing that. Or maybe not. Well, don't quit yet ;) Using the component now is quiet simple, we don't have the 'surprise' factor, but painful:

```

   1:        try
   2:        {
   3:          new ThirdPartyComponent().ActOn(0);
   4:        }
   5:        catch (InitializationException e)
   6:        {
   7:          Logger.Log(e.Message);
   8:        }
   9:        catch (ExceptionalValueException e)
  10:        {
  11:          Logger.Log(e.Message);
  12:        }
  13:        // more exceptions cases
  14:        finally
  15:        {
  16:          Logger.Log("Done with 3rd party component.");
  17:        }

```

This will hunt you down if you use the component several times several places. Solution (as per [book](http://weblogs.asp.net/sfeldman/archive/2008/11/14/clean-code-a-handbook-of-agile-software-craftsmanship.aspx)) - abstract it from the system in a way that suites our needs (logging in this case) and does not affect the client code when test cases are added/removed in the future. Again, through the test we define the interface of the abstracted component:

```

   1:   [TestFixture]
   2:    public class When_abstracted_component_is_asked_to_
   3:                                           act_on_special_case_values
   4:    {
   5:      [Test]
   6:      [Row(0)]
   7:      [Row(100)]
   8:      [ExpectedException(typeof(AbstractedComponentException))]
   9:      public void Should_throw_an_abstracted_exception(int value)
  10:      {
  11:        create_system_under_test().ActOn(value);
  12:      }
  13:
  14:      private AbstractedComponent create_system_under_test()
  15:      {
  16:        return new AbstractedComponent();
  17:      }
  18:    }

```

Now the client code is shielded from all the different exceptions specific to the 3rd party component an instance can throw, allowing other exceptions to propogate as normal. Implementation of *AbstractedComponent* encapsulates what used to be in the client code:

```

   1:    public class AbstractedComponent : IAbstractedComponent
   2:    {
   3:      private ThirdPartyComponent component;
   4:
   5:      public AbstractedComponent()
   6:      {
   7:        component = new ThirdPartyComponent();
   8:      }
   9:
  10:      public void ActOn(int value)
  11:      {
  12:        try
  13:        {
  14:          component.ActOn(value);
  15:        }
  16:        catch (InitializationException e)
  17:        {
  18:          Logger.Log(e.Message);
  19:          throw new AbstractedComponentException(e);
  20:        }
  21:        catch (ExceptionalValueException e)
  22:        {
  23:          Logger.Log(e.Message);
  24:          throw new AbstractedComponentException(e);
  25:        }
  26:        // more exceptions
  27:      }
  28:    }

```

*AbstractedComponentException* is basically a DTO to carry *ThirdPartyComponent* various current (and future) exceptions, allowing the client concentrate on component work/failure without going into the implementation details of possible failures.

```

   1:    public class AbstractedComponentException : Exception
   2:    {
   3:      public AbstractedComponentException(Exception exception)
   4:        : base("AbstractedComponent exception", exception)    {  }
   5:    }

```

The new client code now looks cleaner and DRYer.

```

   1:        try
   2:        {
   3:          new AbstractedComponent().ActOn(0);
   4:        }
   5:        catch (AbstractedComponentException e)
   6:        {
   7:          Logger.Log(e.Message);
   8:        }

```

The exception message can be improved to provide the required information without too much of hassle, but that's not the main point. The point is that client code is not shielded from unnecessary details, is not replicated, simple to read, and most of all verifiable/testable down the road. Change of the 3rd party component is not an agony for the application, but a routine exercise of already existing learning tests (personally like the word 'exploratory' more).

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/DependUponAbstractionsreiteration_82B8/image_thumb_2.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/DependUponAbstractionsreiteration_82B8/image_7.png)

As always, comments and notes are welcomed. Have a great week!

[WrappingExceptions.zip](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/DependUponAbstractionsreiteration_82B8/WrappingExceptions.zip) Update: side note - I used R# 4.1 and Gallio for example.  

