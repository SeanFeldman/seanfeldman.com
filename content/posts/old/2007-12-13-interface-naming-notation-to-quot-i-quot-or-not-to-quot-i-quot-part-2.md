---
title: Interface Naming Notation - To "I" or not to "I" - Part 2
slug: interface-naming-notation-to-quot-i-quot-or-not-to-quot-i-quot-part-2
date: '2007-12-13T22:16:00'
updated: '2007-12-13T22:16:00'
draft: false
tags:
- .NET
- OO
- Personal
author: Sean Feldman
---


While discussing with JP Boodhoo why he stopped to use the I notation for the interfaces, I think we got to the point where it was clear why would someone drop the "I" or opposite, adopt it.

As a developer, I want to differentiate between a pure abstraction and a concrete thing. So to ease on ourselves, we put the I as a differentiation, rely on the visual interpretation that our brain (little one in my case) is doing ("association" as against to "memorization"). And that would be the justification of using the "I" notation.

Now, if we look at the same issue from a more real-world perspective - bicycle. A bicycle is an abstraction, a 3-wheel or mountain bicycle are something concrete.   So having something like:

| ```     1:  class MountainBicycle : Bicycle    2:  {    3:  }  ``` |
| --- |

Is nothing but

| ```     1:  class MountainBicycle : IBicycle    2:  {    3:  }  ``` |
| --- |

With a difference that you know that bicycle is an abstract thing and if your brain is trained enough about it, then you do not need to have an "I"-hint to trigger the "association".

Personal note: so far, from the comments to my [previous post](http://weblogs.asp.net/sfeldman/archive/2007/12/11/interface-naming-notation-to-quot-i-quot-or-not-to-quot-i-quot.aspx) on this, I have not seen that direction. Does this mean we are "boxed" to a particular thinking and not willing to evaluate other options as a community (.NET)?...

PS: "Hey, what about Customer sample?" you might ask - never too late to admit - I was wrong. Customer is not concrete, therefor it's an interface, what concrete is a CertainTypeOfCustomer or any other deviation of a Customer :)


