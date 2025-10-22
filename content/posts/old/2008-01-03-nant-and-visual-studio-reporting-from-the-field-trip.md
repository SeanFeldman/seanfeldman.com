---
title: NAnt And Visual Studio - Reporting From the Field Trip
slug: nant-and-visual-studio-reporting-from-the-field-trip
date: '2008-01-03T05:31:00'
updated: '2008-01-03T05:31:00'
draft: false
tags:
- .NET
- Agile
author: Sean Feldman
---


In my [previous blog](http://weblogs.asp.net/sfeldman/archive/2007/11/22/enable-mbunit-with-msbuild-from-visual-studio.aspx) I was looking how to enable MbUnit with MSBuild from visual studio. As nice as it is, I was missing the flexibility and options of going beyond unit testing only.

After attending ["Nothing But .NET" training session](http://www.jpboodhoo.com/blog/NothinButNetHelpTheHomelessCalgaryAlbertaNovember5th9th.aspx) help by JP Boodhoo in Calgary, I was more aware about option of using NAnt and CruiseControl.NET in the future for potential Continuous Integration.

So why NAnt? Several reasons:

* I was exposed to NAnt first
* Simple XML like syntax that makes total sense
* Lots of resources available from the OSS community

As a beginner the first task was to make it work. Downloading the latest from the [official site](http://nant.sourceforge.net) for NAnt, reading how-tos, and... not working. As a Visual Studio grown developer with addictions to Intelisense and mouse, I straggled to build a simple NAnt build file (script file interpretated by NAnt to perform tasks/operations) without copying it entirely from somewhere. Solution - keyboard can replace mouse, but Intelisense - nothing. Google has brought quiet a few results. What I loved in [Kevin](http://blogs.dovetailsoftware.com/blogs/kmiller/archive/2007/10/29/intellisense-for-editing-nant-build-scripts.aspx)'s solution was to teach Visual Studio about NAnt Intelisense using NAnt itself (nice idea!). What it does is basically dumps NAnt schema file into Visual Studio schemas repository folder. The great part about this approach is full automation of the process plus the ability regenerate the schema with updates, such ad [NAntContrib](http://nantcontrib.sourceforge.net) (additional tasks that NAnt can do if you use it), in a painless way my 4 years old son could do. The simplified version looks like this:

| ``` <target name="build-nant-schema-for-vs2005" depends="load-nantcontrib-schema" description="Generate VS intelisense for NAnt">   <call target="load-nantcontrib-schema" />   <nantschema output="NAnt.xsd" target-ns="http://nant.sourceforge.net/release/0.86-beta1/nant.xsd" />   <property name="visual.studio.schemas.path" value="C:\Program Files\Microsoft Visual Studio 8\Xml\Schemas"/>   <copy todir="${visual.studio.schemas.path}" file="NAnt.xsd"/>   <delete file="NAnt.xsd"/></target> ``` |
| --- |

  


Well, I slightly re-factored Kevin's example to be partitioned better. So the target "load-nantcontrib-shema" is just another target (think of it as a sub-routine in NAnt script) to update normal NAnt schema with NAntContrib schema.

| ``` <target name="load-nantcontrib-schema" description="Load NAntContrib tasks to generate schema">   <property name="NAntContrib" value="C:\Data\SandBox\ProjectAbc\Tools\NAantContrib-0.85\bin" />   <loadtasks assembly="${NAntContrib}\NAnt.Contrib.Tasks.dll" />   <echo message="load-nantcontrib-schema finished." /></target> ``` |
| --- |

So now producing the Intelisense for Visual Studio (2005 in this case) as simple as executing a normal NAnt script:

| ``` C:\Data\SandBox\ProjectAbc>nant load-nant-schema-for-vs2005 ``` |
| --- |

This is making sure that any NAnt script file (also called build file) that contains reference to the schema has intelisense. A typical build file starts like this:

| ``` <?xml version="1.0" encoding="utf-8" ?><project name="Proxy" default="help"           xmlns="http://nant.sourceforge.net/release/0.86-beta1/nant.xsd"> ``` |
| --- |

What that default="help"? Help is one of the targets available in this NAnt script and if no target is provided in command line as an argument, the default is used, "help" in this case. I have picked this idea from the book that describes the NAnt in a very quick and practical way - [Expert .NET Delivery Using NAnt and CruiseControl.NET](http://www.amazon.com/gp/product/1590594851/ref=wl_it_dp?ie=UTF8&coliid=I3TW9W6AQV36SN&colid=2J45ANE21AADN). The idea is to have default target that will list all possible targets in script providing some help to people that did not build it, but have to use (the most important 'ility' - maintainability, isn't it?!)

| ``` C:\Data\SandBox\ProjectAbc>nant ``` ``` NAnt 0.86 (Build 0.86.2898.0; beta1; 08/12/2007)Copyright (C) 2001-2007 Gerry Shawhttp://nant.sourceforge.netBuildfile: file:///C:/Projects/Spikes/Proxy/default.buildTarget framework: Microsoft .NET Framework 3.5Target(s) specified: help help:     [echo] Available Targets:     [echo]   build-nant-schema-for-vs2005     [echo]   clean     [echo]   build     [echo]   test     [echo]   runBUILD SUCCEEDEDTotal time: 0.1 seconds. ``` |
| --- |

Great. Now we need to pump the script contents and run it. But I am too lazy to leave the natural environment of inhabiting - Visual Studio. And even a cool tool like Console2 that is outstandingly great for this purpose, still doesn't make me feel like leaving the cave. So there's an add-in for Visual Studio 2005 called [VSCmdShell](http://www.codeplex.com/VSCmdShell) (and 2008 according to authors, but never worked for me) that can give you the command shell as a part of Visual studio, where you can execute your NAnt build script with parameters (targets). Now editing, building and testing can be all done under one hood in peace and harmony - I heard hallelujah?.

The next step - start building the targets to do cleaning, building, testing, and running. Deployment might be an option as well. I am in the beginning of my NAnt climbing curve, but it definitely looks great so far. Happy climbing!

[![](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/NAntAndVisualStudioReportingFromtheField_8BCA/videocdb6f8bd42e0_1.jpg)](http://video.msn.com/video.aspx?vid=e21b9eea-1fe0-4017-b4c2-e1febedbe6b9&from=writer)

PS: I added a [video](http://video.msn.com/video.aspx?vid=e21b9eea-1fe0-4017-b4c2-e1febedbe6b9) to demonstrate how [VSCmdShell](http://www.codeplex.com/VSCmdShell) is playing nicely in VS.NET 2005 in combination with NAnt. My computer was about to die and Windows Media Encoder was not the best choice for encoder, but this is what I had, with this had to win :)


