---
title: 'Azure Function: One Line of Insanity'
slug: azure-function-a-single-line-to-drive-you-nuts
date: '2023-08-12T22:48:00'
updated: '2023-08-12T23:03:28.455664'
draft: false
tags:
- Functions
author: Sean Feldman
---

Azure Functions Isolated Worker SDK is an easy-to-set-up and get-running framework.
The minimal `Progarm.cs` is hard to mess up.
```
var host = new HostBuilder()
    .ConfigureFunctionsWorkerDefaults()
    .Build();
await host.RunAsync();
```
Right? Except when it's not. The extension method, `ConfigureFunctionsWorkerDefaults` is a critical piece of code that \*\*has\*\* to be invoked, or the generic host will start, but nothing will be wired up. When it's just a few lines, it's not hard to miss if the call is accidentally omitted. But it's less noticeable if that's an average Functions Application with several things configured, such as dependency services and configurations.
And that's the situation I found myself in. While performing code refactoring, I unintentionally deleted the invocation of ConfigureFunctionsWorkerDefaults. Surprisingly, there were no compilation errors or startup issues. However, an unexpected problem arose: binding a configuration file to one of my custom configuration classes failed. This raised eyebrows. When I examined the configuration providers, I immediately noticed that the environment variables provider was absent, which should have been included by default. At this point, I realized that I had accidentally eliminated the entire startup process of the Isolated Worker by inadvertently omitting that crucial extension method call.
Even more ironic is that I commented on a [similar issue][1] about six months ago. Same setup, same problem. And the suggestion I made back then would help me today - an analyzer that ensures `ConfigureFunctionsWorkerDefaults` is not removed accidentally.
Why do I still think that analyzer could be helpful? No one wants to remember special methods to be called. The point in the case is the class below.
```
class Demo
{
  public void Initialize() { // important initialization here }
  public void DoSomething() {}
}
```
To use `d`, it needs to be initialized.
```
var d = new Demo();
d.Initialize();
d.DoSomehting();
```
From the class itself, it is not apparent that `Initialize()` has to take place, and it is easy to omit the call. That's why `DoSomething()` is likely to validate if the initialization took place.
```
class Demo
{
  private bool initialized;
  public void Initialize()
  {
    // important initialization here 
    initialized = true;
  }
  private CheckWasInitialized()
  {
    if (initialized == false)
    {
      throw new Exception("Initialization did not occur. Call Initialize() first");
    }
  }
  public void DoSomething()
  {
    CheckWasInitialized();
    // logic
  }
}
```
Not the most elegant approach, but you get the idea. Trying to use an instance of `Demo` without going through initialization will cause an exception to be thrown.
However, achieving this goal using ConfigureFunctionsWorkerDefaults is currently not feasible. If the complete initialization of Azure Functions relies on this method, it would be desirable to implement a protective measure that guarantees its presence. One potential solution could involve utilizing a Roslyn analyzer to verify the method's existence. This might appear excessive at first glance, but this precaution could be worthwhile considering the potential consequences of removing a single line of code, which could bring down the entire function app without a clear indication of the issue. Currently, prioritizing stability and error prevention is paramount when compensation is no longer tied to the number of code lines produced.
[1]: https://github.com/Azure/azure-functions-dotnet-worker/issues/1347
[2]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2023/azure-function-a-single-line-to-drive-you-nuts/functions.jpg
