---
title: Backbone.js, NServiceBus, and Cloud Hosting
slug: backbone-js-nservicebus-and-cloud-hosting
date: '2012-05-12T14:47:00'
updated: '2012-05-12T14:47:00'
draft: false
tags:
- Cloud
- JavaScript
- NServiceBus
- SOA
author: Sean Feldman
---

# Past

In the past I have always created on premises solutions for web applications that have mostly based on the server side code responsible for front UI and backend code, with a little to none client side code (usually called “scripting” with intention that it is not really a code), predominant validation on the server side with some duplication on the client. Technology of choice was ASP.NET MVC. When choice was not mine, sometime it would be ASP.NET WebForms. Services would be created using WCF, without auto-generated proxies.

Always had quite  a few challenges with this approach, and those included:

1. How do I test my UI interactions (those are especially brutal when UI generated partially by server side code)
2. How do I communicate data more fluently between server and client
3. How do I handle services related issues
4. How do I scale development for a mixed team that has creative folks w/o coding background or setup on their machines

# Current

After looking where web development is heading, it stroke me that I am dismissing client side big time. For the sake of argument, my cellphone is as much capable as my computer browser. Interesting that I still differentiate the two when besides the size and and scale of horse power both are sort of the same these days…

Either way, after looking at backbone.js and the tooling around it, playing with it in [JetBrains WebStorm IDE](https://www.jetbrains.com/webstorm/) it felt right to write client side application and delegate UI responsibility to the browser executed code, and not script I was using before (note: I still don’t entirely grasp the potential with JavaScript, but hopefully getting there). When watched [Backbone Basics](https://peepcode.com/products/backbone-js) it made me wander, why would I need my server code for UI and related validation? Truly, all it was required for was for data retrieval/storage. I scaled back my server side application to static views, controllers, and integration code (storage, services, etc.).

This way, some of my questions if not got answered, then at least I could see the light at the end of the tunnel. neither designers didn’t have to stare and @Model.FirstName like fields anymore asking what the heck is that, nor had they to have a full blown development environment in order to make CSS change or markup layout update. It felt great. Suddenly, UI interactions testing became more realistic (I have only saw Jasmin and QUnit in action, and it looks way better than no tests for client side at all I used to complaint about).

Another great outcome of this was ubiquitous language. I know it sounds a bit weird, we are using C# on server side and JavaScript on the client side. Ubiquitous language for me was JSON. I know could go back and forth leveraging a single standard for expressing data.

Now in the server side code I could concentrate on things like reliability using [NServiceBus](http://nservicebus.com), which I like a lot, which solved a lot of questions of reliability, boiler platting code, and simplicity.

Next step was to challenge on premises hosting. I have tried Azure (cloud solution or whatever the current name is) and all of the above fit so nicely. It just made sense. Static files became content that could be served faster through CDNs (or at least this is my plan), which would possibly include views, templates, images, and client side code. Services could be scaled if needed (granted they are written in appropriate manner, and this is where NServiceBus helps a lot). I also looked at the cost benefit. Looking at the hosting cost, hardware cost, maintenance cost, cloud becomes more attractive. There’s a lot to figure out and improve in my case, though it feels like the right direction.

# Future

So with all this, where am I heading? Exploring more for sure. I have to figure things like automation and deployments using build server and automated scripts, rather than Visual Studio .NET. I have to learn how to leverage web better for things like caching and distribution. Really get JavaScript and not just use it shallowly. Review my old development assumptions and possibly unlearn a thing or two ![Smile](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/wlEmoticon-smile_4151CD16.png)

Whatever it is going to be, it looks better than were I started, because it’s getting into a shape where I would want my code to be. And if you happened to know good resources for pushing forward approach I am trying to adopt, don’t be shy to share.


