---
title: Generating AssemblyInfo with NAnt Gotcha
slug: generating-assemblyinfo-with-nant-gotha
date: '2010-01-23T03:41:00'
updated: '2010-01-23T03:41:00'
draft: false
tags:
- .NET
- CI
author: Sean Feldman
---


As a part of the build script I tend to generate AssemblyInfo.cs in order to inject assembly information dynamically, such as version, name, etc. One gotcha I ran into lately, is when you have internals that are testable and need to generate that information from NAnt as well.

Normally, the code in AssemblyInfo.cs wood look like this:

```

[assembly: InternalsVisibleTo("Project.Test")]

```

NAnt fails. Reason - NAnt is requires full class name, which is *InternalsVisibleToAttribute*, so that the line of code showed above looks like this:

```

[assembly: InternalsVisibleToAttribute("Project.Test")]

```

