---
title: Sick of Relational Databases
slug: sick-of-relational-databases
date: '2009-04-24T03:40:38'
updated: '2009-04-24T03:40:38'
draft: false
tags:
- OO
- Personal
author: Sean Feldman
---


I have started to read a new book about OODB. The reason I decided to get the book and go through it is because I am SICK of the traditional RDBMS and the way it forces us to go through loops and hoops to create domain driven applications.

The very first question to popup - what's the practicality? Don't know, but I know the truth is out there. And it doesn't have a shape of conventional databases.

According to the book, db4o is exceptionally good for any kind of DB activity that operates on object hierarchies rather than any combination of RDB with proper OR Mapper (even such as N/Hibernate). And yes, it sucks when you work with it as query source for things like reporting, but wouldn't be that a re-use/abuse case? For reporting, use the relational representation of the data, not object one.

Why in the world one would like to deal with it? Well, actually a lot of reasons why would someone would like to deal with it. First of all, if you are doing DDD and implement your code with Domain-First approach, data has no meaning without objects. Your data is the state of the objects. Objects cannot keep going without retrieving it's state once they reloaded, but state without objects is meaningless, unless it has a different domain that utilizes it differently (again, reporting is a good example). Therefore, I am questioning the standard approach that "code comes and goes, data stays forever". No. Not in domain driven application.

Have comments? Shoot!


