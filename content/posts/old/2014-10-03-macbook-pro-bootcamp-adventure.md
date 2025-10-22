---
title: Macbook Pro / Bootcamp Adventure
slug: macbook-pro-bootcamp-adventure
date: '2014-10-03T05:00:59.890441+00:00'
updated: '2014-10-03T05:00:59.734191+00:00'
draft: false
tags:
- Personal
author: Sean Feldman
---


A development machine is always a tricky thing. On one hand you want it to be powerful enough to allow you to do what you want to do (and mostly to be fast and not wait). On another hand you want it to be light and thin. I was debating between [Dell XPS 15 15-8949sLV Touchscreen](http://www.microsoftstore.com/store/msca/en_CA/pdp/Dell-XPS-15-15-8949sLV-Touchscreen-Laptop/productID.306254400) and [Macbook Pro 15](http://store.apple.com/ca/buy-mac/macbook-pro?product=MGXC2LL/A&step=config#). Dell was **very** appealing, have to admit. At $500 (now almost $700) and touch enabled display it was a better candidate. Until I've read about overheating issues. That was a show stopper.

So with a new MBP I have started looking into 2 options:

1. Running Windows in a VM on OSX using Parallels or VMWare Fusion
2. Running Windows in Bootcamp ("on the metal")

With VM option I chose to try VMWare Fustion. It was simple, quick, and painless. But performance is not as good as I expected. Perhaps because I did not allocate enough resources to my VM. At the same time, what the point of waisting those resources on OSX if I need Windows.

So I started exploring Bootcamp option. It seemed not so complicated. There's plenty of documentation and Apple makes it look super-duper simple. Until I ran into a problem.

![](https://aspblogs.blob.core.windows.net:443/media/sfeldman/2014/WP_20140928_002.jpg)

And that's when headache started :)

I have tried contacting Apple support, explaining that I'm trying to bootcamp Windows 8.1 Update 1. Was kidly suggested to re-install OSX and get the latest version of bootcamp. Not exactly what I was looking for. Issue was with the version of Windows 8.1 Image - bootcamp didn't support Update 1. Going with plain Windows 8.1 image (w/o Update) worked just fine. Next pain point was the trackpad. Boy it felt... akward. So after research for a while, I found a wonderful [trackpad++](http://trackpad.powerplan7.com/) that made trackpad usable again.

This is not over. At least not yet. I have to figure out how to backup efficiently my machine (ideally something that would take care of both Bootcamp and OSX). For now I'm a happy bootcamper :)


