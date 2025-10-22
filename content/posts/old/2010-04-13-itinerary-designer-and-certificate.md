---
title: Itinerary Designer and Certificate
slug: itinerary-designer-and-certificate
date: '2010-04-13T20:40:00'
updated: '2010-04-13T20:40:00'
draft: false
tags:
- ESB
author: Sean Feldman
---

> A X509 Certificate is required in the model property 'EncryptionCertificate' to encrypt any sensitive property in the designer.

By design, Itinerary designer requires a certificate to save a newly created itinerary. This is required to encrypt “sensitive”  data. What if you don’t have that kind of data, or not willing to use certificate? There’s an option to disable designer from requesting the certificate described in [linked post](http://weblogs.asp.net/hernandl/archive/2009/06/29/biztalk-esb-toolkit-all-about-itinerary-designer-security.aspx), as well as how properly to use one in case it’s needed.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_56068245.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_7F0E9090.png) Once value is switched to false, error will become a warning, allowing itinerary persistence without certificate.


