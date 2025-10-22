---
title: Disjunction and Conjunction in NHibernate
slug: disjunction-and-conjunction-in-nhibernate
date: '2009-07-22T13:29:00'
updated: '2009-07-22T13:29:00'
draft: false
tags:
- NHibernate
author: Sean Feldman
---


Criteria involving multiple ORs and ANDs can quickly become ugly. [David](http://davidmorgantini.blogspot.com) [showed](http://davidmorgantini.blogspot.com/2009/07/nhibernate-disjunction.html) how some of our code became more readable by using a feature to join multiple *ICriterion-*s instead of using *Restrictions* class (as well as how to quickly leverage expressions to get away from using property names, and allow better refactoring by replacing strings with compile-able code).

James Gregory has provided earlier a very [simple explanation](http://stackoverflow.com/questions/386308?sort=oldest#sort-top) on the subject. Absolutely love when things become simpler!


