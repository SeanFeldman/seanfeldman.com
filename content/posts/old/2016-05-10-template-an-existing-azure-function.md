---
title: Template an existing Azure Function
slug: template-an-existing-azure-function
date: '2016-05-10T01:37:45.277121+00:00'
updated: '2016-05-10T01:37:45.230247+00:00'
draft: false
tags:
- Functions
author: Sean Feldman
---
Do you need to create an Azure Function based on an existing one? While there's no a way to do this using the portal, I found it a temporary workaround.
Head to the SCM portal (kudu portal). If you functions project is called X, then that would be `https://x.scm.azurewebsites.net`. 

Next, navigate to the console. In the console `xcopy` your existing function folder to a new one.

```csharp
xcopy /E ExistingFunctionFolder d:\home\site\wwwroot\NewFunctionFolder\
```
Et viola! Your new function based on an existing one will show up in the portal.
