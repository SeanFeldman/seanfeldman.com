---
title: DB Trigger - A Friend Or A Foe?
slug: db-trigger-a-friend-or-a-foe
date: '2008-07-15T13:54:57'
updated: '2008-07-15T13:54:57'
draft: false
author: Sean Feldman
---


Database triggers are useful, and I am not going to bush it completely. In some cases, like the one I run into, triggers are more of a distraction and source of issues, rather than help and ease of headache-free maintenance. In order to understand the case, players must be introduced first.

* An application that collects information from user inputs to be stored in database at a very specific table that is uniquely assigned for the purpose of persisting user selections.
* An external service that is asked from time to time to perform a job based on the inputs user has provided from the application.
* Results of the job are stored in database, and for optimization purposes, some metadata stored as well, in a table of its own. What kind of metadata? Well, lets keep it simple and say that a certain job was executed or not. So the next time job (pretend that it's scheduled) has to be run, it will first validate that it wasn't executed before.

Some business process rules around the user inputs are defined as well

* Once a user has updated inputs from the application, any scheduled job running after the fact inputs were changed, has to ignore the fact that the job was run before in order to take in account the new inputs.

What is the standard DB approach and the simplest one to implement - put triggers in place. This is an absolutely valid approach. You observe the Inputs table, on updates to that table you trigger updates to the Metadata table and voilà it's working. Each time user makes an update to inputs, metadata is wiped and job is forced to re-run the calculations when it kicks in. Simple, elegant, but non trivial down the road.

The application evolves, you add down the road more inputs and suddenly - the magic of triggers is done. You validate the fact that they are in place, but it is very easy to skip the fact that within the trigger the newly added fields to the inputs table are not processed.

Another scenario - you want to be able to test the code, and see that changes to the inputs are actually triggering the metadata changes. But how would you do it, unless running in a debug with a real database attached?

One idea is to remove the triggers from the database and implement them in the code, after all it is really an **application behaviour** we are trying to capture and express. Depending on how data access is implemented, the way to implement the code differs. We still are using home grown sort-of entities framework (hopefully not for long), and inputs table has a reflection in the application as an object of it's own. Initial idea was to create a proxy and it would update the metadata once inputs are persisted. Due to technical limitations of the framework we are using, the implementation went in a different technical route, but still, allowed to remove triggers and have it expressed as code, that can be tested and refactored.

What were the goal of this exercise?

* Simplify application maintenance
* Easier refactoring
* Capturing application behaviour in application, and not database

