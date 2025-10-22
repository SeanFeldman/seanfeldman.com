---
title: Data Driven Or Domain Driven Application?
slug: data-driven-or-domain-driven-application
date: '2008-07-18T05:42:11'
updated: '2008-07-18T05:42:11'
draft: false
tags:
- Personal
author: Sean Feldman
---


The company I work for has a significant amount of web applications of a specific line of business. This line of applications started 8 years ago (I am with the company just for the last 3 only). Since I started to be interested in Domain Driven Design, felt strongly that this line of applications should be re-addressed with a DDD approach. But the resistance was enormous, motivating that "these are the pure data centric applications and there's no place for domain, the data is the domain and as a result of that it is a DATA driven design application".

I disagree.

Why do I disagree? Here's the theory I have that might be applicable not only to this case.

As a company that started web development 8 years ago under Microsoft wing, the natural choice for developers was classic ASP and SQL Server. With or without DDD, the business these applications were intended for had it's behaviour, rules, entities. Now with something like VB Script in classic ASP I cannot imagine proper tool for DDD, and on the other side, database was there to enforce the feeling of key components of design in shape and form of tables (Users, Selections, Benefits, etc.) So DB was a natural selection to grow the domain design, and incorporate some of the business logic (default values, calculations, etc).

Today, when we moved to C# and have a solid language to support good object oriented practices, database gets a role it should have had from the beginning -  persistence medium of the domain objects state. No logic, no design driving power, nothing of that.

How I can be sure about the theory? Over the years I see how painful the maintenance becomes, what challenges our developers face when they need refractor code, how non-trivial it occurs to do a trivial feature addition. The biggest from my point of view, is the fact that looking into the code, you cannot understand the business (behaviour, rules, logic).

This is why I believe those so called "data driven applications" should be reviewed closer, some of them are really "domain driven applications" not expressed well due to the luck of the proper tools at the time of creation.

Question. Doubt. Don't accept just because it's widely accepted.


