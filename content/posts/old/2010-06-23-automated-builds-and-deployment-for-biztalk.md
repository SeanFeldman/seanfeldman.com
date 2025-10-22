---
title: Automated Builds and Deployment for BizTalk
slug: automated-builds-and-deployment-for-biztalk
date: '2010-06-23T04:38:00'
updated: '2010-06-23T04:38:00'
draft: false
tags:
- Agile
- BizTalk
author: Sean Feldman
---


Automated builds are an essential part of Continuous Integration. Definition commonly found is

> *Continuous Integration is a software development practice where members of a team integrate their work frequently, usually each person integrates at least daily - leading to multiple integrations per day. Each integration is verified by an automated build (including test) to detect integration errors as quickly as possible. Many teams find that this approach leads to significantly reduced integration problems and allows a team to develop cohesive software more rapidly.*

Continuous Integration can be done on any project. Literally any, including BizTalk. What is interesting, is that getting it running for BizTalk applications is somewhat challenging, especially when the vast majority of resources are using “traditional techniques”. If you are already coming from an environment that exercises CI, just the though of deploying something from within Visual Studio .NET by clicking context menu “Deploy” is making you feel uncomfortable. No one likes black magic. Especially when you’ve seen that there’s a way.

I searched a lot for how to set up automated builds for BizTalk application and automate deployments to the maximum. Options are various, and probably not everything that is out there, but I’ll demonstrate what I found to be quite efficient for me.

#### Option 1 – Visual Studio .NET

A few years ago I would jump on someone even thinking about this option. Yet, for someone who’s not a developer and is more of an integration person stuck with BizTalk all by himself, this might be not such a bad idea. Cons of this approach are multiple, and among them are

* Installing VS.NET on the test and production environments
* No way to know who/what exactly did what
* Process is not repeatable (in terms of using same artifacts to reproduce installation)

This is not something I would not recommend.

#### Option 2 – MSI Export/Import

Once BizTalk application is installed, it can be exported from BizTalk console. The extracted MSI and Bindings XML (both are required to completely “backup” and application) can be used later to install that same application on another machine. The benefit of this is that we no longer rely on VS.NET to exist to deploy straight from the code. The biggest con, in my opinion, is the fact that source code can live in complete independence from the “snapshot” captured by MSI file, i.e. MSI represents a certain version, while it can be completely outdated since a manual deployment and MSI extraction is required to have the right version.

#### Option 3 – Build Server

This is the one I prefer. BizTalk projects are nothing but .NET projects. These projects are compiled using MsBuild. The artifacts are assemblies, .NET signed assemblies. These assemblies can be generated every single time there’s an update to the code, and it will be performed by build server upon any code change in repository. I use combination of NAnt scripts with solution (.sln) and project (.csproj) files that are just MsBuild scripts after all. Build artifacts are gathered into an automatically generated MSI installer, created with WiX project. Fully configurable, a 100% automated.

The caveat is deployment. Deployment is really deployment to the BizTalk and GAC. This can be easily done by either leveraging the updated [NAntContrib](http://nantcontrib.sourceforge.net/release/0.85/help/tasks/btsdeploy.html) library latest version that has support for BizTalk tasks, or by [SDC Tasks](http://sdctasks.codeplex.com/) for MsBuild. Either way, [btstask.exe](http://msdn.microsoft.com/en-us/library/aa559686%28BTS.20%29.aspx) is what is used to deploy and undeploy.

As a part of MSI installer, I package MsBuild scripts and batch files that invokes those to perform the actual deployment of artifacts into BizTalk.

Note: bindings are extracted manually from a deployed application, and then packaged with the rest of build artifacts into MSI to allow import of binding during automated deployment (batch file).

Benefits of this you asking yourself? Lots.

1. Repeatable
2. Automated
3. Allows testing
4. Brainless deployment
5. Process documented in build/deployment scripts

I hope this post is going to help someone to find an option, just like I hoped to find one when was just starting. If something is hard to test, ask yourself, am I doing the right thing. If you can’t positively answer that one, then there’s another way, you just haven’t found it.


