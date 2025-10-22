---
title: Nothing But .NET, Calgary 2007 - Day 4
slug: nothing-but-net-calgary-2007-day-4
date: '2007-11-09T17:12:00'
updated: '2007-11-09T17:12:00'
draft: false
author: Sean Feldman
---


'Almost' productive day - seeing how it works in reality is hilarious. TDD is not only allows testability,  but also to design better your code with regards to not 'what if', but 'what now'. Really powerful tool that would be great to have in my skills set. Script of the day:

**10:00 Domain Model (Rich Domain)**   
- Domain object is more than just properties, it's also behavior   
- 14 AA Points - [here](http://www.jpboodhoo.com/blog/GettingStartedLearningSomeNewDeveloperHabits.aspx) or -> jpboodhoo.com -> search for "Getting Started Learning Some new Developer Habits"   
- R# -> Autocompletion -> Letters and Digits   
- DynamicMock<T> vs. CreateMock<T> (dynamic will always provide the default value when "created" mock has to be told everything)   
**11:15 Domain Driven Design**- Thin service layer & Transaction Script () patterns   
- Use R#, don't accept naked Visual studio - naked it's really ugly.   
- TestDriven.Net   
- [Setup] is for the hard dependencies of the SUT (ie DynamicMock<T>)   
- Book: xUnit Testing Patterns   
- Department / Products: DB relationship is one to many, Domain Model is one to one (ie not Department.GetAllProducts(departmentId), but Catalog.GetAllProductsBelongingTo(departmentObject) )   
**14:15**   
- Service Layer   
- interaction test can later involve into integration testing   
- REQUIREMENT: Important to understand the RhinoMock in order to use it and learn TDD   
- R# CTRL-Shift-E parse the exception from clipboard   
- Hard dependencies should be be dynamic ones and defines for the whole test class   
**16:10 Container**   
- Principles that container helps to respect: DIP, OCP   
- Container (our) should be a static gateway that also an adapter to allow with variety of different containers   
- Concrete dependencies should be removed by using container to decouple from concrete implementation   
- pair-programming / TDD ping-pong   
**23:50**   
- JP is SO tired that reads for a minute a result of breaking test :)   
- Building rich domain model = building smarts with objects (example: ShoppihgCart with CartItem through Factory)   
**00:50**   
Toasted...


