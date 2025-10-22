---
title: MIME Header - Content-Disposition
slug: mime-header-content-disposition
date: '2009-06-02T05:17:00'
updated: '2009-06-02T05:17:00'
draft: false
tags:
- Other
author: Sean Feldman
---


I am trying to figure out something on MIME header, and just can’t understand who is standing behind the RFCs. Are they trying to read it on their own and realize if it makes sense?!

The problem I am facing is attachments in another standard, RosettaNet, that is leveraging MIME for attachments. We are using a third party component to parse a RosettaNet message and load all the attachments. Attachments original filenames are supposed to be in the “Content-Disposition” property, marked as “Content-Disposition: attachment; filename=some\_filename” according to the [this WIKI](http://en.wikipedia.org/wiki/MIME#Content-Disposition). “But WIKI is not RFC” you say, well, read [RFC 2183](http://tools.ietf.org/html/rfc2183). It says

> ```
> In addition to allowing the sender to specify the presentational
> disposition of a message component, it is desirable to allow her to
> indicate a default archival disposition; a filename. The optional
> "filename" parameter provides for this.
> ```

And later:

> ```
> 
> ##### 2.3 The Filename Parameter
> 
> The sender may want to suggest a filename to be used if the entity is
>    detached and stored in a separate file. If the receiving MUA writes
>    the entity to a file, the suggested filename should be used as a
>    basis for the actual filename, where possible.
> ```

Reading more of the great RFC, I found an example #3, in section 2.10

> ```
> The following body part contains a JPEG image that should be
> displayed to the user only if the user requests it. If the JPEG is
> written to a file, the file should be named "genome.jpg".  The
> recipient's user might also choose to set the last-modified date of
> the stored file to date in the modification-date parameter:
> ```
> Content-Type: image/jpeg
>     Content-Disposition: attachment; filename=genome.jpeg;
>       modification-date=&quot;Wed, 12 Feb 1997 16:29:51 -0500&quot;;
>     Content-Description: a complete map of the human genome
>     &lt;jpeg data&gt;</pre>
> ```
> 
> ```

I am really confused.  One part says “it’s optional”, the other part says “should be used”. So in case I want to save the attachment in a file with the original filename, I might end up not having one (filename)?! Great… Long live standards.


