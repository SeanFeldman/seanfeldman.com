---
title: Moq – ToString() Method Pitfall
slug: moq-pitfall-on-tostring-method
date: '2009-08-05T04:53:00'
updated: '2009-08-05T04:53:00'
draft: false
tags:
- .NET
- C#
- TDD
author: Sean Feldman
---


I was working on some code today, when run into a pitfall with Moq. This was probably my misreading of documentation.

The component I was testing looked somewhat like the code below

```
public class SomeOtherType  
{  
  private readonly ISomeType someType;  
  
  public SomeOtherType(ISomeType someType)  
  {  
    this.someType = someType;  
  }  
  
  public string Do()  
  {  
    return "And it was: " + someType.ToString();  
  }  
}
```

where dependency in injected and .ToString() method is invoked on it to construct the final result.

Specification looked quiet simple

```
[Concern(typeof (SomeType))]  
[TestFixture]  
public class ToStringMoqIssue : StaticContextSpecification  
{  
  private Mock<ISomeType> dependency = new Mock<ISomeType>();  
  private string result;  
  
  protected override void establish_context()  
  {  
    dependency.Setup(x => x.ToString()).Returns("dependency");  
  }  
  
  protected override void because()  
  {  
    result = new SomeOtherType(dependency.Object).Do();  
  }  
  
  [Observation]  
  public void Should_return_And_it_worked()  
  {  
    result.Should_Be_Equal_To("And it was: dependency");  
  }  
}
```

Dependency contract was dead simple

```
  public interface ISomeType  
  {  
  }
```

Observation is clear and simple. Yet I was getting an unexpected failure.

*Expected Value : "And it was: dependency"
```
<br>Actual Value&nbsp;&nbsp; : "And it was: <b>ISomeTypeProxy14b81655017446cc9f41c4740251e9c1</b>" </i></p>
```

Something obviously did not work right. Then I realized that ToString() is a method of Object and not of the Contract, and by default is assigned to any object (even if you reference it by the contract…). Update to the contract has fixed it.

```
public interface ISomeType  
{  
  string ToString();  
}
```

Reminder for myself – careful with ToString()!*


