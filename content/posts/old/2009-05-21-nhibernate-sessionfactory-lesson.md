---
title: NHibernate SessionFactory Lesson
slug: nhibernate-sessionfactory-lesson
date: '2009-05-21T05:22:00'
updated: '2009-05-21T05:22:00'
draft: false
tags:
- NHibernate
author: Sean Feldman
---


Anyone who worked with NHibernate knows that SessionFactory is an expensive object, that better to be constructed once, cached and re-used to build lightweight and disposable NHibernate sessions. It’s always shows up as a warning in books ([NHibernate in Action](http://www.manning.com/kuate/), page 35), WIKIs, blogs, etc.

Today our team had a chance to experience what a wrong handling of SessionFactory can turn into – a huge memory leak. SessionFactory is a heavy object, it’s initialization and allocation is not a trivial one. Each time SessionFactory is constructed, it uses a significant amount of recourses and holds to those. If SessionFactory is not cached as a single instance, each allocation causes to the overall memory leak. Combine that with luck of Session disposing generates a very interesting result – more than a gig of  memory for something that is barely 20 megs.

Moral of the story:

- As in pair programming, so is in pair-troubleshooting – team works better

- Using a third party components (even the best out there) without exploratory tests will cause eventually pain

- Follow simple notes third party components authors write, they might simplify your life


