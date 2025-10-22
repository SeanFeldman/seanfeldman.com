---
title: Mercurial on IIS
slug: mercurial-on-iis
date: '2011-06-02T16:25:00'
updated: '2011-06-02T16:25:00'
draft: false
tags:
- Other
author: Sean Feldman
---


[Mercurial](http://mercurial.selenic.com) is a very appealing distributed source code versioning system. I used it with Google code and also for some local work when no server repository was available. Worked great. This time I wanted to go through the scenario of setting up Mercurial as a team repository with a centralized server. This would be still useful for an individual developer to have local commits (better than committing every single change just to ensure it’s captured) and would allow to push an entire change set to be versioned on the server and allow others to retrieve that change set with all the “intermediate bookmarks”.

Setting up Mercurial on a server through IIS was not painful, but tedious and too manual (yes, I prefer simplicity over unnecessary complexity – hint: VisualSVN server). I was a bit turned down by the fact that Active Directory authentication is not working with IIS for Mercurial. You can get it going with LDAP support build into Apache web server.

For me – for now I am going with Subversion. When something like VisualSVN Server for Mercurial shows up, I’m switching.  Unless I need the local (disconnected) mode ![Smile](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/wlEmoticon-smile_547E6291.png)


