---
title: Nothing But .NET, Calgary 2007 - Day 2
slug: nothing-but-net-calgary-2007-day-2
date: '2007-11-07T16:01:06'
updated: '2007-11-07T16:01:06'
draft: false
tags:
- .NET
- Personal
author: Sean Feldman
---


The second day was as good as the first, with a tiny exception for configuration of CruiseControl.NET - IMO, technique is valuable, not the technical details. Specification technique was bright, logging exercise was a healthy one. Learned to differentiate between state testing andA0 interaction testing, but I am not completely set on it. Here are the notes taken through out the day 2:

09:00   
- <http://codekata.pragprog.com>   
- Build process and not compilation in vs.net: speed; logging; testing;   
- Spike new stuff, do not have a deep understanding, until you have to have it in your project   
- "Use the tool knowing you can produce the same result without the tool." - J. Nielson   
- "Speaking and writting is not an elite club - be honest and be good in what you do." - JP   
- Plan success for yourself for a short/long periods of time.   
- It doesn't matter what you do as you do it the best.   
- IEnumerable<T> is a gateway to get an Iterator<T>   
10:00   
- "Introduce Local Extension" refactoring technique - exampe: IRichList and RichList   
- Refactoring book - re-read   
- Decorator has exactly the same interface as the object it decorates (intent: add functionality without changing the public interface)   
- Client - dont care about what Decorator does. With "Local Extension" you care about implementation   
- Extension methods in .Net 3.5 will introduce a form of a code reuse that can quickly become a code abuse   
- IComparer<T> --> Strategy implementation for comparng in .Net   
- R# CTRL-N \*Pub will find all classes with "Pub" in it   
- one ONE 1 return per method - old and good school   
11:00   
- Proxy = secured composing mechanism   
- Use the best tools for the right tasks (me:)   
- Aggregate - boundry of protection (library and it's books)   
- Composite - complex structure - the root and the leaf are of the same interface and the difference is that some operations on leafs might not do what the do on root or oppositeA0 (with Iterators and Visitors, with Command)   
- Think Domain Driven, not Data Driven   
11:30 Querying   
[Q] How to do TDD with WebControls?   
- function that return function -> return a new delegate   
11:50 Specifications   
*// TODO: implement ISpecification for IEntityCollection*   
- Specifications create a tree of objects, that can be translated into a query for DB or any other repository   
- LINQ: abstruction the details of how the provider takes the expression and converts into query   
scoop: "Nothing But \*" sessions will be coming soon with different well known people   
**13:25**- FW harvesting: design solution for the client and pull out pieces for the FW to be reused   
- FW should be harvested from the real life projects and not built in isolation   
**14:00 DB**- Developers should have local DB to speed development and not to delay the rest of the team while testing/developing   
- File Unlocker - <http://ccollomb.free.fr/unlocker/>   
- Windows Task Switcher - <http://ccollomb.free.fr/unlocker/>   
- MyUninstaller utility - keyboard friendly   
- Console - tabbed console   
- QueryExpress - sql server management studio alternative   
A joke that CJ told: "I had a problem i wanted to solve with regex. Now I have 2 problems to solve."   
**15:37 Continuous Integration (WebApp)**- Test has A)Unit (test) B)Integration (test)   
- Aspect# (Castle, AOP)   
**15:50 Mocked Testing**   
- Mocked testing is an interaction testing   
- RhinoMocks framework   
- using (mockery.Record()){}   
- using (mockery.Playback()){}   
**17:30 Testing**   
- State Base vs. Interaction Based (mocked) testing   
- Component partitioning - separating interfaces from implementors for separate packaging   
- examples: Log class is a static gateway   
**19:00 CruiseControl.NET**   
- a front controller implementation that allows dashboard configuration through xsl files   
- CI = Compilation, Unit testing, Code Coverage, FxCop, Versioning, Reporting, Publishing   
- a role of a build-manager cycles through the iteration to spread the knowledge and know how to do that   
- development cycle should be short (around 15 minutes) so when you commit the changes the amount of collisions when merging would be minimal   
**21:45 --- END OF ITERATION 0 ---A0   
22:30 EOM**


