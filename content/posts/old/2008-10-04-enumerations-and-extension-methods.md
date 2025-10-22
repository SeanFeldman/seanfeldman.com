---
title: Enumerations And Extension Methods
slug: enumerations-and-extension-methods
date: '2008-10-04T04:19:41'
updated: '2008-10-04T04:19:41'
draft: false
tags:
- C#
author: Sean Feldman
---


Enumerations are for enumeration. Obvious. Often, though, it's used also for some metadata knowledge. For example, an enumeration for gender might look like:

```
  public enum Gender
  {
```
Male,
Female
```
}
```

Two options, simple. Now let's say I want to populate  a drop down list with these values and some meta data. It's simple when it's English (a proper enumeration value would mostly match the metadata, but not always), what about another language? Normally I would build a workaround this, to have a utility class that would get a gender value and based on it return the metadata for the required culture. Does the work, but leaves bad taste after.

This is where extension methods can make it nicer. I will not go for the cultures, but capital and lower cases, but culture solution should not be that different.

Gender is closed for changes, but we need to be able to 'extend' it's functionality without 're-opening' it. The next code snippet shows how to achieve the required functionality:

```
  public static class GenderExtensions
  {
```
<span class="kwrd">public</span> <span class="kwrd">static</span> <span class="kwrd">string</span> ToNiceName(<span class="kwrd">this</span> Gender gender,
                          IGenderFormattingStrategy formattingStrategy)
{
  <span class="kwrd">return</span> formattingStrategy.ToStringWithFormatting(gender);
}
```
}
```

In this case I used a strategy pattern for formatting. What is nice, is that now we can test the extension method, knowing that *Gender* is not something we should be testing at all, but the result of *ToNiceName()* method.

```

   1:    [Concern(typeof(GenderExtensions))]
   2:    [TestFixture]
   3:    public class when_converting_gender_to_string_with_strategy
   4:                                      : SpecificationContext
   5:    {
   6:      private string resultMaleCapitalized;
   7:      private string resultMaleLowered;
   8:      private IGenderFormattingStrategy capitalizedStrategy;
   9:      private IGenderFormattingStrategy loweredStrategy;
  10:   
  11:      protected override Gender EstablishContext()
  12:      {
  13:        capitalizedStrategy = Stub();
  14:        loweredStrategy = Stub();
  15:   
  16:        capitalizedStrategy.Expect(
  17:             strategy => strategy.ToStringWithFormatting(Gender.Male))
  18:              .Return("MALE");
  19:        loweredStrategy.Expect(
  20:             strategy => strategy.ToStringWithFormatting(Gender.Male))
  21:              .Return("male");
  22:   
  23:        return Gender.Male;
  24:      }
  25:   
  26:      protected override void BecauseOf()
  27:      {
  28:        resultMaleCapitalized = sut.ToNiceName(capitalizedStrategy);
  29:        resultMaleLowered = sut.ToNiceName(loweredStrategy);
  30:      }
  31:   
  32:      [Test]
  33:      public void should_return_string_formatted_according_to_strategy
```
_rules()
```
34:      {
  35:        resultMaleCapitalized.ShouldBeEqualTo("MALE");
  36:        resultMaleLowered.ShouldBeEqualTo("male");
  37:      }
  38:    }

```

I am still not sure how much this test actually tests the extension method, or more serves as documentation to what it should be doing, but personally find it a good way to make sure that tested only one thing, and the implementation of the rest get deferred to later. In this case strategies are dead simply:

```
  public class CapitalizedStrategy : IGenderFormattingStrategy
  {
```
<span class="kwrd">public</span> <span class="kwrd">string</span> ToStringWithFormatting(Gender gender)
{
  <span class="kwrd">return</span> gender.ToString().ToUpper();
}
```
}
```

So what it's good for besides the metadata? Allows OCP for enumerations, brings a cleaner syntax. If you happened to have another neat usages, welcome to share those.


