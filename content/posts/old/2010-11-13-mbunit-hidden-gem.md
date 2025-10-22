---
title: MbUnit–Hidden Gem
slug: mbunit-hidden-gem
date: '2010-11-13T05:16:00'
updated: '2010-11-13T05:16:00'
draft: false
tags:
- C#
- TDD
author: Sean Feldman
---


Row tests are fun. You can simulate various inputs with expected outputs and execute them all with a single observation (test). The problem for myself was always the fact that when this was done, the only way to accomplish it was to merge the logical *because* which operates on system under test behaviour and the observation itself (assertion). This leads to a slightly less readable code IMO.

```
[Row(“hello”, 5)]
[Row(“you”, 3)]
public void behaviour_and_observation(string value, int expected_number_of_letters)
{
	system_under_test.GetLenth(value).Should_be_equal_to(expected_number_of_letters);
}


```

Luckily, as pointed out by one of my ex-coworkers Dragosh, MbUnit has a way to assist with a specification that is trying to keep concerns separated. It’s called [ParameterAttribute](http://www.gallio.org/api/html/T_MbUnit_Framework_ParameterAttribute.htm).

What specification does look like then?

```
[Header("Value", "ExpectedLength")]
[Row("hello", 5)]
[Row("you", 3)]
[Specification]
public class Some_specification : ContextSpecification
{
	[Parameter]
```
public string Value{ get; set; }
             [Parameter]
             public int ExpectedLength{ get; set; }
             [Because]
             protected void When_obtaining_length()
             {
                      result = system_under_test.GetLength(Value);
             }
             [Observation]
  	 public void Should_get_proper_length()
             {
                      result.Should_be_equal_to(ExpectedLength);
             }
```
}
```

This is a trivial code, but with a bit more complex code the technique becomes really handy.


