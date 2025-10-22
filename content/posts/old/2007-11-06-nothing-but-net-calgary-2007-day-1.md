---
title: Nothing But .NET, Calgary 2007 - Day 1
slug: nothing-but-net-calgary-2007-day-1
date: '2007-11-06T08:12:00'
updated: '2007-11-06T08:12:00'
draft: false
author: Sean Feldman
---


I had/will not have time over the week of the training course to sort out all the notes I am taking while participating at the session. Saying that, I want to make it clear that these are uncensored  thoughts of mine at a crazy pace of the course with tones of new material flying around between 0800 and 2400 (with a few little breaks in between).

One more thing I had to mention - feeling like a fish in water is a  great feeling. What I'm down to is that finally it feels good to be around smart and intelligent people that are striving to get the knowledge as much as you are if not even more.

So the notes from day 01 (text format, typed in Notepad2):

**0830**- slickrun to speed up things (there's something for mac OS as well)   
- no mouse   
- do not rely on debugger.. rely on logs and tests   
[v] get the plan for the week from JP   
- web dev. is a lot context switching (JS, CSS, Markup, etc)   
JP IP 192.168.100.15   
- criticize everything and actively question it   
- books: head first design patterns; head first A & D; applying UML and patterns; clr via c#; Code complete;  Pragmatic programmer(!!!); DDD - tackling complexity by Eril Evans; Working effectively with legacy code; Agile principles, patterns and designs in C#;  Core J2EE patterns; NHibernate in Action (!); xUnit testing pattern (!); Roy Osherovs book;   
- Boodhoo Listmania!;   
- MIT open courseware (==> change; real oop; 6months;)   
- JPs wishlist at Amazon   
- Subversion software (teams up to 1k)   
*[xxxxxxxx - r# lisence or amazon?]*[bring pain killers...]   
- svn scheme : UMATC = Update Merge Add Test Commit   
- 1st project: C:\Development\Course\labexercises\SeanF\product\test\xunit - wow   
[bring more pain killers...]   
- TestDriven.Net -> the investment is worth (?! James Kovacs = JC)   
- Visual SVN --> SVN for vs.net   
CTRL-Shift-A --> add a new item in vs.net   
- coding standards doc should not be long - what should matter is how to solve problems and raise the quality of code   
CTRL-minus --> run macro to rename test method   
ALT-R-N-I (R# new interface)   
CTRL-Space (auto completion)   
CTRL-Shift-space (smart auto completion)   
- Logical assertion - keep assertions low   
- MbUnit can do parameterized test methods (combined with attributes Row and RowTest)   
- unit test should not change the state of the system - each test is a 'clean slate' (JP)   
- SRP principle   
- logic and assertions (parameters checks) should not be mixed -> pull out into assertion class (SRP)   
**1245-1330 lunch**- R# has a NAnt support   
- Final Builder - a commercial tool for deployment to abstract complexity   
- "files excluded from compilation" - dangerous - requires visual judgment from a developer - potentially bugs   
- <http://nant.sourceforge.net>   
- Tasks are executable units   
- <http://www.visualsvn.com/>   
- SVN can point at external repository (like HTTP)   
- book: Pragmatic Subversion (for SVN)   
- R# CTRL-Shift-N (search filenames)   
- <property name="xunit.console.args" value="${labExercises.output} /sr /rt:Text" /> <!--show report; report type-->   
**1515 Events/Delegates**   
- R# CTRL-ALT-Space (all matching classes to partially typed name)   
- Test should contain the behavior - ie if i test the click, don't create an event handler, but an anonymous delegate   
- Anonymous delegates should strive to 1-line only   
- private EventHandler<BreakDownEventArgs> \_handler; ==> private EventHandler<BreakDownEventArgs> \_handler = delegate{}; // NON empty handler   
- EventHandler<EventArgs<MyDto>> where EventArgs<T> is a custom generic class along with the MyDto class   
- EventHandlerList (CLS class) with AddHandler and RemoveHandler   
- Implicit interface implementation --> have to cast to the interface explicitly   
- ISSUE: .Net events are introducing coupling...   
**1645**- microsoft.msdn.ca/ignite -->JC on tools   
- scoop: R# will have its own solution explorer   
- enums are bad for internalization => replace by Value Object pattern (class) --> PayloadKeys example  
- SUT (System/subject under testing) never has a member field   
**1730**   
- Const is published with the using code, and not the class   
- Subscriber & Publisher attributes are published in a seporate assembly (interface assembly) and given to the 3rd party   
==> Q: how to load plugging with asp.net??? A: observer   
- R# -> LOOP snippet for for statement   
- IEnumerable<T> --> grand parent of all collections (typed)   
- "Tell Dont Ask" principle (collection.Property.Count vs. collection.IsEmpty)   
**2130** [Need pain killer... NOW!]   
- Compiles != No errors => to resolve TDD & CI   
- Structs impose design limitations   
- Termin: "Necessary Evil"   
- ReferenceEquals() method - very fast   
- method length != number of responsibilities   
**2215**==> Q: issues with method chaining (case when int, int passed into double, double with returned type string... A: use classes and not static utility methods, separate concerns   
- R# --> when implementing interface, can DELEGATE to parameter passed in to do automated forwarding   
- Decorator forwards to decorated object then adds functionality / Proxy can choose if to do the forwarding or not   
**2250**- Suffixing with Pattern name should only be on Factories   
- IEqualityComparer<T> + Decorator from an IList to IRichList   
- decorator for comparer   
- Comparison<T> ==> adaptor pattern   
**2400 (EOM)**


