---
title: Why Event Sourcing?
slug: why-event-sourcing
date: '2023-05-31T05:10:00'
updated: '2023-05-31T05:11:09.106632+00:00'
draft: false
tags:
- EventSourcing
author: Sean Feldman
---
![refill][1]

# Some context

I've seen software systems built since 2001. My first exposure was to classic ASP and VB6 applications with traditional state-based architecture. As someone new to software development, I was both fascinated by the use of data stores such as SQL Server to persist the vast amounts of data and horrified by the ease of irreversible mistakes that could take place. I should be honest; that **took** place when I accidentally ran some SQL update statements against the wrong database. Glorious days of a newbie developer at a startup company. I learned quickly that a safe strategy includes backing up data frequently. 

Twenty years later, I realized it could have been a *safe* strategy. Still, it wasn't a good solution, to begin with, for a domain that involves business applications. So let's dig into the details.

# State-based Application lie

I've been with a particular pharmacy for a long time. We moved a lot, and with each address change, the local pharmacy has always registered my new address and used that to confirm my identity each time I picked up a prescription. I had lived for over 5 years at the current address, so you can imagine my surprise when I failed the identity verification during a routine prescription pick-up. I'm older these days, but still not at the stage where I forget my address. So that was quite confusing.

When asked if I could provide a different address, I returned to the memory lane to the previous address. But, to my even bigger surprise, that wasn't the address on the file either. So I asked the pharmacist if they happened to store more than one address, trying the theory that the pharmacy system is not showing the default address. But no, the system only has a single address. So now I was really puzzled. But just for kicks, I gave it the address I had over 15 years ago. And bingo! My identity was confirmed. But let's unpack what has happened here.

The address in the system has changed. Obviously, somewhere in the pharmacy's system *something* changed my address from the current to the one I had over 15 years ago. But what was that event? Would it be possible to look at a log to determine what happened? If I file a complaint, would it be possible to find out what happened? And how did the dormant address for 15 years miraculously get resurrected, replacing my active address? A mystery surrounded by more guesses than answers.

# Operating within the constraints

So how would a "mystery" of this sort get approached in a conventional system? Logs. Let's look into logs to see what has happened. That's assuming logs account for such a scenario and log the details. But it's virtually impossible to log absolutely every permutation in the system.

Track database changes! See if there's anything in the data. Well, that's not a trivial exercise, either. Assuming data changes are captured. And let's assume those data changes are captured; what's the context? What was the **event** that took place that caused the system to start using that 15yo address? Cricket.

# What's a better approach?

This is the question I've been toying around for quite a while. My career has taken me from business applications to libraries and back. And it was the second round when I started questioning the state-based approach and the conventional architecture. This is where I got to return to the idea of Event Sourcing and re-evaluate the approach. If my **data** are the events that take place in the system, those events are the authoritative source of truth, not only allowing us to reconstruct the current state but also help understand how that state was derived. And that's a game changer.

I will save you from the details as plenty of more competent people wrote better posts on the topic. I'll just wrap up with my own experience highlight. Being able to trust the system and understand how it got to the place where it is is invaluable for business applications.

![events][2]

# Great. How do I do it?

YMMV. I've started simple. No frameworks and no products. Just Azure Storage Tables to store my events, Azure Service Bus to communicate events for projections (async), and Azure MySQL Flex Server to keep projections for searches and queries. Knowing what I know today, I would probably do that again but choose slightly different services. Nothing works better than building your own to understand the concepts. If you need someone else to take over, consider a framework of some sort.


[1]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2023/why-event-sourcing/refill.jpg
[2]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2023/why-event-sourcing/log.jpg
