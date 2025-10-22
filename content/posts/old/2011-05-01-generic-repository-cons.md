---
title: Generic Repository–Cons
slug: generic-repository-cons
date: '2011-05-01T02:11:00'
updated: '2011-05-01T02:11:00'
draft: false
author: Sean Feldman
---


Generic Repository (something like Repository<T>) is a good concept with intention of keeping code DRY, though problematic. Here are a few drawbacks of a generic repository:

1. It is not always logical to call behaviours Save, Delete, etc on all repositories
2. Support (logging as an example) requires to know what specific repository was invoked, and not just Repository<T>

Just recently I ran into a log with an exception, where operation on …*Repositories.Repository`1.Save(T obj...)* failed and there was no way to figure out **what** repository out of 4 different one actually failed save operation.


