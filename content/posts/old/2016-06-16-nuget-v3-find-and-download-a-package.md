---
title: NuGet V3 - Find and Download a Package
slug: nuget-v3-find-and-download-a-package
date: '2016-06-16T07:01:00'
updated: '2016-06-17T16:05:33.143803+00:00'
draft: false
tags:
- NuGet
author: Sean Feldman
---
While working on a side project, I've run into a need to discover the latest version of a given NuGet package and download it. Being a side project, I've decided rather that using NuGet v2 API to try out v3. I was hoping to find some documentation at the [official site](https://docs.nuget.org/), but that didn't turn out to be as successful as I was expecting. All my attempts to figure it out on my own were failing and had to admit it felt nasty. After fiddling with it, trying to get some information on the interwebs, posting a question on [SO](http://stackoverflow.com/questions/37650619/find-if-nuget-package-has-an-update-using-net-api-v3), cursing at the dozens of NuGet packages required just to query, almost gave up.
The hope came from Maarten Balliauw at MyGet. He suggested rather than going through something that is not quite an API and frankly way too complicated, to just go through the raw NuGet REST API.
NuGet v3 feed is a JSON file (f.e. the official NuGet v3 feed https://api.nuget.org/v3/index.json) containing all the operations you can perform and URLs you need to invoke to get those operations performed.
First, we need to search for the package by ID. `SearchQueryService` `@type` element will give us the URL to invoke for the search. That would be https://api-v2v3search-0.nuget.org/query in the case of the original NuGet v3 feed or https://api-v2v3search-1.nuget.org/query. To narrow down the scope to a particular package, package ID has to be provided. Assuming I'm interested in Newtonsoft.Json package, the search URL to use becomes https://api-v2v3search-0.nuget.org/query?q=packageid:newtonsoft.json.
Note: if you need to query pre-released packages as well, pass `prerelease=true` in the query.
Next step is to find the `PackageBaseAddress` `@type` in the original feed and use its URL to download the required package version. Assuming, `8.0.3` is the version we're interested in. The download link would be https://api.nuget.org/v3-flatcontainer/newtonsoft.json/8.0.3/newtonsoft.json.8.0.3.nupkg
This is a direct link to Azure blob storage that contains the package.
Huge thank you to [Maarten Balliauw](http://blog.maartenballiauw.be/) who has helped me to get this information. The sample project is available [here](https://github.com/SeanFeldman/Nuget.Updater).
