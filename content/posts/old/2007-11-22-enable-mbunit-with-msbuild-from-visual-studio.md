---
title: Enable MbUnit with MSBuild from Visual Studio
slug: enable-mbunit-with-msbuild-from-visual-studio
date: '2007-11-22T22:06:29'
updated: '2007-11-22T22:06:29'
draft: false
author: Sean Feldman
---


Editing the project file and adding this section will ensure the MbUnit tests are executed on successful builds.

<PropertyGroup>  
    <PostBuildEvent>"$(ProjectDir)<*location in the project*>\MbUnit.Cons.exe" "$(TargetPath)"  /sr /rt:text</PostBuildEvent>  
</PropertyGroup>

location in the project - something that I picked up from JP Boodhoo. The idea is to keep all the tools used for the development encapsulated with the project. That way maintenance and setup on new workstations is not an issue.




