---
title: Bizmonade
slug: bizmonade
date: '2010-07-02T04:56:00'
updated: '2010-07-02T04:56:00'
draft: false
tags:
- BizTalk
- TDD
author: Sean Feldman
---


[Bizmonade](http://bizmonade.matricis.com/) is a project allowing to simulate execution of BizTalk orchestrations without deployment to BizTalk server. What is it good for? Testing. Unit testing. The fact that the logic can be tested without deployment hassle is good. There are a few issues that I have encountered so far, and my experience with the particular tool is less than 24 hours (so excuse me in case I am not accurate – corrections are welcomed always):

1. You have to use orchestrations that subscribe to a specific schema message. What if I subscribe on any message (System.Xml.XmlDocument) based on receiving port? No documentation on that, neither clear if it’s possible from the samples.
2. Default configuration/documentation assumes Bizmonade is GAC-ed. Personally, I don’t like that. For Continuous Integration scenario it is better to be self-contained with-in a project. Good news is that you can do it easily.
3. Lack of API documentation. It would be nice to have some sort of documentation. Yes, code should be self descriptive, yet would be nice to have documentation, or at least some hints.
4. \_\_Simulated classes. This is not truely Bizmonade issue, maybe more of the ReSharper, but having no intellisense on those is annoying a bit.

Bottom line, from the entire list the only serious one I find #1. I hope there’s an option to achieve what I want. The this library becomes a real gem for my project.


