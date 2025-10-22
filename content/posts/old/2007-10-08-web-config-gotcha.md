---
title: Web.config gotcha
slug: web-config-gotcha
date: '2007-10-08T15:37:00'
updated: '2007-10-08T15:37:00'
draft: false
tags:
- VS.NET
author: Sean Feldman
---


I haven't paid attention to the space in the namespace attribute value and had to spin my wills till found it:

```
<pages maintainScrollPositionOnPostBack="true">
  <controls>
```
&lt;</SPAN><SPAN style="COLOR: rgb(163,21,21)">add</SPAN><SPAN style="COLOR: rgb(0,0,255)"> </SPAN><SPAN style="COLOR: rgb(255,0,0)">tagPrefix</SPAN><SPAN style="COLOR: rgb(0,0,255)">=</SPAN>"<SPAN style="COLOR: rgb(0,0,255)">Tempo</SPAN>"<SPAN style="COLOR: rgb(0,0,255)"> </SPAN><SPAN style="COLOR: rgb(255,0,0)">assembly</SPAN><SPAN style="COLOR: rgb(0,0,255)">=</SPAN>"<SPAN style="COLOR: rgb(0,0,255)">Tempo.Web.3.0.1</SPAN>"<SPAN style="COLOR: rgb(0,0,255)"> </SPAN><SPAN style="COLOR: rgb(255,0,0)"><BR>            namespace</SPAN><SPAN style="COLOR: rgb(0,0,255)">=</SPAN>"<SPAN style="COLOR: rgb(0,0,255)">Tempo.Web.UI.WebControls </SPAN>"<SPAN style="COLOR: rgb(0,0,255)">/&gt;</SPAN></PRE>
```

Moral - be accurate with web.config


```

