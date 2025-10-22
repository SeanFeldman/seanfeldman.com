---
title: Humanitarian Toolbox
slug: humanitarian-toolbox
date: '2016-02-21T06:48:00'
updated: '2016-02-21T06:48:17.813662+00:00'
draft: false
author: Sean Feldman
---
I've heard about [Humanitarian Toolbox](http://www.htbox.org/) a few times on the .NET Rocks Show. In case you've never heard of it, this is what it is:

>Humanitarian Toolbox (HTBox) is a charity supporting disaster relief organizations with open source software and services.  We are developers, designers, testers, and industry professionals who want to contribute our unique skills in disaster relief aid. Whether it is through creating apps that map the spread of disease or maintaining software that helps to optimize the delivery of relief supplies, Humanitarian Toolbox has a goal of creating software and programs for relief organizations to have ready in times of need.

I've joined Humanitarian Toolbox hackathon this weekend to try it out.

## How does it work

Everyone involved in this project is volunteering their skills and time to build the software. The project is OSS. Hosted on GitHub under https://github.com/HTBox/allReady. `allReady` is the web application based on .NET and ASP.NET Core. Volunteers can fork the repository and start working on any [existing issues](https://github.com/HTBox/allReady/issues). To reduce contention on the issues caused by concurrent work, you can be a good Samaritan, and ping others, letting th/m know you'd like to work on a particular item.

![enter image description here][1]

Next step after the issue is assigned to you is to fork the repository and start working on it. Create a branch, implement a fix/feature, and submit a pull request (PR) to the original repository (`master` branch). There can be going back and forth until changes fix the issue. The unit tests suite is in place to help you to ensure new changes are not breaking the code that was there before. If changes are accepted, it will get merged. Congrats, you've contributed!

When working in a distributed fashion, pinging multiple people can be problematic. First, you need who the people are responsible for different things. Second, by pinging individuals, you can skip people and by that reduce your chances to get a response faster. A [potential resolution](https://github.com/HTBox/allReady/issues/541) to this could be as simple as leveraging GH groups. Imagine you want to work on a database related issue. You'd ping `@HTBox\database` group to raise questions. Need to have a review of your PR? Not a problem, ping `@HTBox\pr-reviewers` and someone will get back to you.

Note: additional benefit of this approach is that people can join and leave groups, it doesn't affect contributors that need to communicate with group members. Communication also doesn't depend on one familiarity with all member names and what they do on the project.

## Should I try this?

If you've never contributed to an OSS project, this is an excellent opportunity to do so. You get to interact with other developers, learn new technologies (.NET / MVC / EF Core, and much more). You get to find out how software can help after a disaster and be proud of any contribution that will assist people in need.

Big shout out to [Simon Timms](http://blog.simontimms.com/), [James Chambers](http://jameschambers.com/), and [David Paquette](http://www.davepaquette.com/) for organizing, running and helping to get into HTBox.


[1]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2016/working-on-issue.png
