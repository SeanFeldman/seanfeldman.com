---
title: User Secrets, the human-readable version
slug: user-secrets-the-human-readable-version
date: '2020-10-09T05:16:00'
updated: '2020-10-12T17:30:39.078141+00:00'
draft: false
tags:
- .NET
author: Sean Feldman
---
![enter image description here][1]

When developing locally, there are many ways to store secrets locally without risk of receiving a GitHub notification about leaked keys and secrets. Environment variables, local files excluded from check-ins, user secrets with secret storage, etc. This post is about user secrets. If you have no experience with user secrets, [this Microsoft article][2] does a good job to go from zero to sixty in about 30 seconds. 

User secrets work just fine. Except if you don't like to read and memorize the mapping between GUIDs to project names, you'll have difficulty understanding what projects have their secrets stored on the file system. Imagine this:

```
4bddaed0-75ba-464a-94f1-917236f36c35
174f8024-a077-4411-8adf-8523f610ef47
...
```

What project is `174f8024-a077-4411-8adf-8523f610ef47` exactly? You get the idea.

Unfortunately, the documentation only speaks about GUIDs as project identifiers. But what if I'd like an identifier that is human-readable *and* to match the project name? Not sure what about you, but for projects that require user secrets, I found those project names to be quite unique. That's an assumption. Right.

The good news - `.csproj` files properties are MSBuild properties. Looking at the user secret definition for a given project:

```
<PropertyGroup>
  <TargetFramework>netcoreapp3.1</TargetFramework>
  <UserSecretsId>174f8024-a077-4411-8adf-8523f610ef47</UserSecretsId>
</PropertyGroup>
```

`UserSecretsId` is a variable assigned a horrific GUID. Instead of that monstrous value, we could use our project name. For the sake of this post, I'll call it `MyWonderfulProject`. The section change to

```
<PropertyGroup>
  <TargetFramework>netcoreapp3.1</TargetFramework>
  <UserSecretsId>MyWonderfulProject</UserSecretsId>
</PropertyGroup>
```

Inspecting `%APPDATA%\Microsoft\UserSecrets\` we'll find a folder called `MyWonderfulProject` with the `secrets.json` file. Great!

Now, a project *might* be renamed. If you really insist on not changing the value of the `UserSecretsId` property ever, that's possible as well. This is where reserved [MSBuild properties][3] are coming in handy. One of those variables is `MSBuildProjectName`. Let's use it.

```
<PropertyGroup>
  <TargetFramework>netcoreapp3.1</TargetFramework>
  <UserSecretsId>$(MSBuildProjectName)</UserSecretsId>
</PropertyGroup>
```

Et voilà! Now we have the following in the secrets store:

```
4bddaed0-75ba-464a-94f1-917236f36c35
MyWonderfulProject  <|-- Look! I know what project is using this folder!
...
```


This works with Visual Studio 2019 (Manage User Secrets). Unfortunately, Rider has no built-in support for user secrets, and [.NET Core User Secrets plugin][4] has a [bug][5] that doesn't allow using MSBuild variables.

**Update**: the wonderful [Maarten Balliauw][6] has raised a PR that is going to fix this and allow user secrets with MSBuild variables to be used with Rider! 🎉


[1]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2020/user-secrets/lockers.png
[2]: https://docs.microsoft.com/en-us/aspnet/core/security/app-secrets?view=aspnetcore-3.1&tabs=windows
[3]: https://docs.microsoft.com/en-us/visualstudio/msbuild/msbuild-reserved-and-well-known-properties?view=vs-2019
[4]: https://plugins.jetbrains.com/plugin/10183--net-core-user-secrets
[5]: https://github.com/Witik/RiderUserSecrets/issues/8
[6]: https://blog.maartenballiauw.be/
