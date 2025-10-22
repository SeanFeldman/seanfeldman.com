---
title: IDs to Objects
slug: ids-to-objects
date: '2008-06-27T16:05:00'
updated: '2008-06-27T16:05:00'
draft: false
tags:
- DDD
- Patterns
author: Sean Feldman
---


A few months ago I blogged about [Domain Objects vs. Primitive Types](http://weblogs.asp.net/sfeldman/archive/2008/02/03/domain-objects-vs-primitive-types.aspx). Back then it felt right to me to transform a primitive type, like a Guid that represented an organization ID, to an Organization domain object. Unfortunately at that time I was not educated enough to know that this is a common idiom among many object designers. Apparently it is. [Craig Larman](http://www.amazon.com/Applying-UML-Patterns-Introduction-Object-Oriented/dp/0131489062) writes it nicely in his book (in my case Organization is what Craig references to as a Customer):

> *Why bother? Having a true Customer object that encapsulates a set of information about the customer, and which can have behaviour , frequently becomes beneficial and flexible as the design grows, even if the designer does not originally perceive a need for a true object and thought instead  that a plain number of ID would be sufficient.*

The other important note is when this transformation is taking place - when an ID or a Key leaves the UI layer and gets to the Domain Layer.


