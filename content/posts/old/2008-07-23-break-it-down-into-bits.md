---
title: Break It Down Into Bits
slug: break-it-down-into-bits
date: '2008-07-23T15:01:49'
updated: '2008-07-23T15:01:49'
draft: false
tags:
- OO
- Patterns
author: Sean Feldman
---


I had to refactor a portion of code and decided to go with strategy pattern. Interesting thing is that the final result might look more complex, but when discussed with a fellow developer, got green light in terms of "more maintainable" and "self documenting" code result. So here I am sharing it with others for review and opinions.

The problem

A person is associated with a plan it is member of. Association is expressed in a plan code assigned to the person. Based on the code a person is assigned, different fields from his plan details record are pulled into calculation. Possible plan codes are PlanA, PlanB, PlanZ. Each plan is driving out the price for member, spouse, and total costs. Fields involved in calculations are:

* For PlanA:

+ MemberCost = PlanA**Member1** + PlanA**Member2**
+ SpouseCost = PlanA**Spouse1** + PlanA**Spouse2**
+ TotalCost = MemberCost + SpouseCost

* For PlanB and PlanZ - same story

The original code was using reflection and retrieving values based of reflective code that extracted property values based on the fact that attributes (properties) of an object would have the names that are consistent and are prefixed with the plan code. The code then would do everything-in-one-shot.

```

   1:  var planDetails = PlanDetails.Load();
   2:  Type type = typeof(PlanDetails);
   3:  double memberCost
   4:     = type.GetProperty(planCode + "Member1").GetValue(planDetails, null)
   5:     + type.GetProperty(planCode + "Member2").GetValue(planDetails, null);
   6:
   7:  double spouseCost =
   8:     type.GetProperty(planCode + "Spouse1").GetValue(planDetails, null)
   9:     + type.GetProperty(planCode + "Spouse2").GetValue(planDetails, null);
  10:
  11:  double totalCost = memberCost + spouseCost;

```


What are the down sides of this code - fragility.

* Plan code found for a person might not be in the database, the code will explode
* When *PlanDetail* property(s) name is different from the assumed pattern, the code will definitely break
* Not flexible - calculations logic might vary in the future and that will over complex everything-in-one-shot code
* Readability of the code lucks simplicity - overwhelming details

Strategy sounded like a right ways to go. Divide and rule - split each plan calculations into its own class - *PlanA*, *PlanB*, and *PlanZ*. Also adding a *Default* plan to have a fallback mechanism. To make it all sing, a factory would create one of the plans based on the required argument - plan code. To glue it all together an abstraction for all plans is required. I considered an interface first, but since the plans share the calculations at this point, decided to do the simple thing - abstract base class *Plan* that would capture all the similarities and leave the descendents to fill the rest. This is an oversimplified result code (removed extra details and client-associated stuff).

Factory

```

   1:    public class PlanFactory
   2:    {
   3:      public static GetPlanFor(string planCode, IPlanDetails planDetails)
   4:      {
   5:        switch (planCode)
   6:        {
   7:          case "PlanA":
   8:            return new PlanA(planDetails);
   9:          case "PlanB":
  10:            return new PlanB(planDetails);
  11:          case "PlanZ":
  12:            return new PlanZ(planDetails);
  13:          default:
  14:            return new Default();
  15:        }
  16:      }
  17:  }

```

Plan

```

   1:  public abstract class Plan
   2:  {
   3:       public readonly IPlanDetails planDetails;
   4:
   5:       protected Plan(IPlanDetails pd)
   6:       {
   7:         planDetails = pd;
   8:       }
   9:
  10:        public abstract double MemberCost { get; }
  11:        public abstract double SpouseCost { get; }
  12:        public double TotalSpouseCore
  13:        {
  14:          get { return MemberCost + SpouseCost; }
  15:        }
  16:  }

```

PlanA (similar are PlanB and PlanZ):

```

   1:  public class PlanA : Plan
   2:  {
   3:       public PlanA(IPlanDetails pd) : base(pd) {}
   4:
   5:        public override double MemberCost
   6:        {
   7:          get { return planData.PlanAMember1 + planData.PlanAMember2; }
   8:        }
   9:  }

```

Usage:

```

   1:  var plan
```
= PlanFactory.GetPlanFor(user.GetPlanCode(), PlanDetails.Load());
```
2:  double memberCost = plan.MemberCost;
   3:  double spouseCost = plan.SpouseCost
   4:  double totalCost = plan.TotalCost;

```

Now comparing the last chunk of code to the original code - some difference.

**Conclusions**

With simplified for maintainability and readability code, the complexity went up significantly. With power comes responsibility - if you want code that is easy to maintain and change, test and trace, you have to lift your skills and play by the rules. And the rules are simple

* Strive to have a network of objects each handling a single responsibility, rather than procedural one giant class that does it all
* Learn core principles (patterns, idioms, etc)
* Don't be afraid of complexity if it is based on core principles

PS: to spice it up, the real code did actually have a more sophisticated behaviour down the road, which was taken into the *Plan* code (in case it is shared by all plans) or into individual plans when it's unique to that particular plan. The bottom line is the the 'user' code, the usage of the factory, has not changed at all, and the details of each plan where left to the plans themselves, a place where they naturally belong.

PSS: there's something bugging me down - the switch statement in the factory. I would rather have something that would eliminate that switch statement as it feels not right. Ideas?


