---
title: Nothing But .NET, Calgary 2007 - Day 3
slug: nothing-but-net-calgary-2007-day-3
date: '2007-11-08T21:07:23'
updated: '2007-11-08T21:07:23'
draft: false
author: Sean Feldman
---


They say "The more you know the less youA0 have to say". Almost, my version is "The more you know the more you want to scream". Why scream? Because you realize each time how much more you don't know. Well, it's a healthy process besides the fact that from a side it looks like a total mental disorder... No comments. Day 3 notes:

**09:00**   
- State testing initially only might be better that trying to apply both testing strategies (state and interaction)   
- Developing Top-Down, not the Domain Model First   
- Layers (horizontal, top down): UI, Presentation layer, Service layer, Domain/ORM   
- Layers (vertical): Security, Logging, Utility   
- UI pieces and stories   
- DTOs and Domain Model are not pointing anything else (presentation, ORM, service, UI layers)   
- DTOs allowing domain model and UI to be independent (UI does not dictate what model will be)   
- Service layer is a (Application) Gateway and Facade   
- Application startup is happening in Service layer   
[Note:] Friday (9/11/2007) how to combine domain model business rules validations with client side   
- Service layer should log exceptions   
- Most of exceptions are in the mapping layer (DB constraints violations, timeouts, etc) and domain logic (business rules violation)   
- The only time to catch an exception is to put the system in stable mode, otherwise let it go and show that a system has a bug that has to be fixed   
- Auditing = Decorating the ORM components!   
**10:00 Story Document and Story Cards**- Story cards are 'like' use cases, story document is a bit more detailed   
- Stories are one page long at most and dedicated to the users and products through out the life of the project   
- Stories are ALWAYS coming from the business users with a DEFINED/UNIFIES domain language   
- purpose of story card is to shortly and precisely describe 3 things: WHO / WHAT / WHY   
- you need to have the story card and a strong access to the user (story teller) to supply the details , where strong access to the domain specialist is phone or one on one   
- BA would flush out more out of the story card   
- Story Document + Story Cards + UI prototype mock (what user NEEDS not WANTS) = deliverable for the iteration that both devs and client sigh off (for the iteration 0)   
- Story will disclose many of domain objects (nouns in the domain language) (highlight them when writing)   
"Days of head-down developers are done!"   
- Remind the customer of time impacts on deliverable when adding to the story - let the customer to decide if they want a feature or a down scale of the feature based on what they need and what they want to invest into it   
- Assumptions are evil, especially with clients   
- Front load iterations planning meetings   
- Story card summarizes what story document says in form of who/what/why   
scoop: next year there will be an agile PM course.   
**10:45 UI layer**- Build box doesn't have IDE on it   
- keep 3rd party assemblies in solution so you don't have to configure the environment to stat building (build) process   
- Repeater is better than Grid, Alternate template is lame (?later)   
- avoid postback as much as possible working with the plain html where possible   
**11:08 Presentation - Tests First - Pait Programming**   
- presenter roles: decouple view from model and route messages   
- Interfaces are not serializable, therefor POCO DTOs are the way to go   
- If a name (of a class or interface) does not disclose the meaning and usage, rename it   
- To mock a DTO that cant be instantiated - mark all as virtual   
- R# CTRL-ALT-Space   
- Pair programming - one is building the test, another one is implementing   
- Reading a test in plain English goes bottom to top, from SUT to record stage   
- Test names should present what they really do. Example why: to create a list for QA for testing, reflectively processing the list of test methods   
- Concrete dependencies for tests are initialized in SetUp() and defined as memeber fields   
[Note: not switching to Mac!]   
- NULLs are evil - avoid passing NULLs around   
- Don't only write the test, also try to read it in plain English putting yourself the SUT perspective (as you were the SUT)   
- Interface = contract/blueprint/contract   
- Debugging tests smells bad!   
Q: JP, who is Richard Hurse?   
- WatiN project for UI browser-in testing   
- Interaction tests should be understood how to read in plain language and not as a pure code   
**13:40 Linking UI and Presenter**   
- JP will build his whole site as an MVC project with MS MVC as an open source   
Q: How to use DotTracer?   
- .ASPX / .ASCX is a Template View patterns (classic asp was the same, but no support for separation of concerns)   
- Let the view engine be responsible for rendering the template   
Q: A page that requires more than one task/service AND how to not to couple between them but have cooperating with each other (event aggregator?)   
- Spend 20 minutes on method visibility and 40 on customer feature to be implemented, and not vice versa   
- A view without traces of Presenter --> presenter is actualy a Mediator pattern implementer   
- For presenter, Task/service is not in place, so what we do is we create a private internal stub task/service class to fulfil presenter requirements and to be able to sign off. Stub class for servise/task will be eliminated asap.   
- valueType.ToString("bla bla 0") - no need in curly brackets   
- DTO allows Separation of concerns and SRP principles - a change in a DTO is not forcing a change in view nor presenter   
- In an agile team the DBA has to take part in agile development and devs and DBA cooperate and resolve problems together

[Sean] Compilation should not be indication of syntax error. It should be an indication of bad design.

- ITransformer - a compositional solution to do the fluent interface (ie to perform the conversion of type)   
- .NET 3.5 will allow fluent interface implementation with extension methods (example: Container.DataItem.To<Abc>.Prop)   
**19:30**   
- Passive view - communication between view and presenter is done with events (enforces chattiness in both ways)   
- >>>Supervising controller - logic pushed to the presenter (controller), ui related stuff stay in the view   
- ASP.NET is a more complex abstraction of things that were less complex in the beginning   
- Presentation model   
- J. Miller "The most important 'ility' is maintainability".   
- You have to bring the lowest common level developer to the level to understand agile and TDD or it wont work at all   
- Dispair.com   
**21:40**   
- Building network - linking between blogs and sources   
**22:30**   
- Submitting data from the view to presenter   
- R# CTRL-Shift-E - show stack tree for the exception text in the clipboard   
**23:10**- Duplicate code smells, including in tests - strive to eliminate it completly   
**23:30**   
- Design by Contract   
- Pushing data from UI to Presenter - presenter is available for the view - keep a reference to it   
- Exploring the beauty of discovering controls in a templated container in .NET - not a simple task at 00:11. Nope.   
- Done exploring (00:16) Personal conclusion: no place for political correctness in a team, not in agile team for sure.   
- 5 minute break   
**00:30**   
- Refactoring Patterns   
**01:01**   
- Lost it... "What are we talking about?" - Chicken Little   
- Mapper on Repeater Item   
- "What if" vs. "now what" concept; what if == premature generalization   
**01:17 EOM. Hibernating...**

**05:30 Hibernation failed. System is shutting down for 3 hours of sleep.** (Talks about various subjects)

A0

PS: I am so glad I got on this train, and met all the interesting people. I hope to ride this train for as long and as far as my capacities will allow me.


