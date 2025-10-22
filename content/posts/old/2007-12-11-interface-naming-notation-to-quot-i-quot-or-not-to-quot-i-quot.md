---
title: Interface Naming Notation - To "I" or not to "I"
slug: interface-naming-notation-to-quot-i-quot-or-not-to-quot-i-quot
date: '2007-12-11T17:10:34'
updated: '2007-12-11T17:10:34'
draft: false
tags:
- .NET
author: Sean Feldman
---


While reading  R.C. Martin's book converted to C# by M. Martin "Agile Principles, Patterns, and Practices in C#" I could not ignore the fact that the Java notation for interface naming was used all over the place. Trying to be open-minded (or should I use "pragmatic" these days) I want to pop a question what is the benefit of dropping the I-prefix and how it does or does not influence the daily work.

For myself, having an "I" prefix in front of the name not only tells me that this is an interface, but also that this is a pure "contract" (Design by Contract is something I start to like).

| ```     1:  public interface ICustomer    2:  {    3:    // ...    4:  }  ``` | ```     1:  public interface Customer    2:  {    3:    // ...    4:  }  ``` |
| --- | --- |

So what do you have to say about it? To "I" or not to "I"?


