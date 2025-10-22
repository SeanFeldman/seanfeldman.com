---
title: LINQ to XML for Better Maintainability
slug: linq-to-xml-for-better-maintainability
date: '2009-10-09T03:28:00'
updated: '2009-10-09T03:28:00'
draft: false
tags:
- .NET
author: Sean Feldman
---


Today I was trying to solve a simple technical problem. Given a specific XML, needed to clean it up by removing any elements of a particular type.

```

  file1.pdf
  1

  file2.pdf
  2


```

Result had to be without Id elements

```

  file1.pdf

  file2.pdf


```

A few choices for implementation:

1. Regex
2. XmlDocument
3. LINQ to XML
4. XSLT *(as suggested in comments)*

Regex option is probably the most efficient, but not the most maintainable. Myself, looking sometimes at the solutions with Regex I ask “what the heck did I try to do here”. So much for “code doesn’t lie”.

XmlDocument is more expressive than Regex option, but way too chatty.

LINQ to XML same as XmlDocument, expressive. As well as very clear and fluent. I picked this option not for performance, but for maintainability sake. I know it will take less developer type to understand and/or modify code when it’s time to change it. And it documents itself very well, with no need to write any comments.

```

var xdoc = XDocument.Load(new StringReader(received_content));
xdoc.Descendants().Where(element => element.Name == "Id").Remove();
return xdoc.ToString();

```

Note: this is a very specific case, which does not indicate it’s a solution to all kinds of problems. Regex / XmlDocument are valid tools for all sorts of other problems.


