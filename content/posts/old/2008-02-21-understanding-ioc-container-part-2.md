---
title: Understanding IoC Container - Part 2
slug: understanding-ioc-container-part-2
date: '2008-02-21T05:36:53'
updated: '2008-02-21T05:36:53'
draft: false
tags:
- .NET
- OO
author: Sean Feldman
---


I try to lower expectations in order not to be disappointed, but in this case I was asked by several individuals to address the fact that IoC container power is in the ability to "hook" implementer with the contract through an external file, leaving application code unaware of the actual implementer till the run-time, having no reference to implementers' assembly or whatsoever. I am going to expand the sample from the [part 1](http://weblogs.asp.net/sfeldman/archive/2008/02/14/understanding-ioc-container.aspx) post to achieve that goal in a couple of days.

In the last post we left with the application with an ApplicationStartup() method that would register all implementers against the contracts they implement. That causes a serious coupling between the ConsoleApp assembly and the one that implements the XmlLogger, AssemblyTwo. This is not a good idea, especially when we want to be able to replace the implementer without touching/modifying the application itself (by recompiling it).

Solution would be to take the code found in ApplicationStartup() method out of the code and express in a form of some configuration file that container would process. By doing that, we minimize coupling of the AssemblyTwo to Core only, and completely removing coupling of ConsoleApp on AssemblyTwo.

[![ioc_configuration_file_1](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/UnderstandingIoCContainerPart2_143D6/ioc_configuration_file_1_thumb.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/UnderstandingIoCContainerPart2_143D6/ioc_configuration_file_1_2.png)

Now ConsoleApp has only references to what it really utilizes directly.

```
using System;
using AssemblyOne; // IGadget
using Core.IoC;    // ILogger and Container
```

Next step is to describe the relationships between contracts and implementers. Something like an XML file should be ok.

[![ioc_configuration_file_2](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/UnderstandingIoCContainerPart2_143D6/ioc_configuration_file_2_thumb.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/UnderstandingIoCContainerPart2_143D6/ioc_configuration_file_2_2.png)

Once this is place, the rest is just forcing Container to scan a file and look for Container.xml, registering all of the contracts and their implementers and passing that information back to the container for registration. To transform from a string presentation into a .NET type, I use reflection and that takes care of loading the desired assembly into memory. From there we get the type and register in container, allowing later instantiation.

The code that loads the XML file:

```
namespace Core.IoC
{
  public sealed class XmlConfiguration
  {
```
<span class="kwrd">private</span> <span class="kwrd">readonly</span> <span class="kwrd">string</span> filename;
<span class="kwrd">public</span> XmlConfiguration() : <span class="kwrd">this</span>(<span class="str">&quot;Container.xml&quot;</span>)
{
}
<span class="kwrd">public</span> XmlConfiguration(<span class="kwrd">string</span> filename)
{
  <span class="kwrd">this</span>.filename = filename;
}
<span class="kwrd">public</span> Dictionary&lt;Type, Type&gt; GetAllRegistrations()
{
  Dictionary&lt;Type, Type&gt; result = <span class="kwrd">new</span> Dictionary&lt;Type, Type&gt;();
  <span class="kwrd">string</span> fileWithPath = GetPathAndName();
  <span class="kwrd">if</span> (File.Exists(fileWithPath))
  {
    XmlReader reader = XmlTextReader.Create(fileWithPath);
    reader.MoveToContent();
    <span class="kwrd">while</span> (reader.Read())
    {
      <span class="kwrd">if</span> (reader.LocalName == <span class="str">&quot;Register&quot;</span>)
      {
        Type contract = BuildTypeFromAssemblyAndTypeName(
                                      reader.GetAttribute(<span class="str">&quot;Contract&quot;</span>));
        Type implementer = BuildTypeFromAssemblyAndTypeName(
                                   reader.GetAttribute(<span class="str">&quot;Implementer&quot;</span>));
        result.Add(contract, implementer);
      }
    }
  }
  <span class="kwrd">return</span> result;
}
<span class="kwrd">private</span> Type BuildTypeFromAssemblyAndTypeName(<span class="kwrd">string</span> fullTypeName)
{
  <span class="kwrd">int</span> commaIndex = fullTypeName.IndexOf(<span class="str">&quot;,&quot;</span>);
  <span class="kwrd">string</span> typeName = fullTypeName.Substring(0, commaIndex).Trim();
  <span class="kwrd">string</span> assemblyName = fullTypeName.Substring(commaIndex + 1).Trim();
  <span class="kwrd">return</span> Assembly.Load(assemblyName).GetType(typeName, <span class="kwrd">false</span>, <span class="kwrd">false</span>);
}
<span class="kwrd">private</span> <span class="kwrd">string</span> GetPathAndName()
{
  <span class="kwrd">string</span>[] split =
    Path.Combine(AppDomain.CurrentDomain.BaseDirectory, filename)
            .Split(<span class="kwrd">new</span> <span class="kwrd">string</span>[] {&quot;\\bin\\&quot;},
                   StringSplitOptions.RemoveEmptyEntries);
  <span class="kwrd">return</span> Path.Combine(split[0], filename);
}
```
}
}
```

Updated Container class will have to reflect changes:

```
using System;
using System.Collections.Generic;

namespace Core.IoC
{
  public class Container : IContainer
  {
```
<span class="kwrd">public</span> <span class="kwrd">static</span> <span class="kwrd">readonly</span> IContainer Instance = <span class="kwrd">new</span> Container();
<span class="kwrd">private</span> <span class="kwrd">readonly</span> Dictionary&lt;Type, Type&gt; container;
<span class="kwrd">private</span> Container() : <span class="kwrd">this</span>(<span class="kwrd">new</span> XmlConfiguration())
{
}
```
    private Container(XmlConfiguration xmlConfiguration)
```
{
  container = <span class="kwrd">new</span> Dictionary&lt;Type, Type&gt;();
  <span class="kwrd">foreach</span> (KeyValuePair&lt;Type, Type&gt; pair <span class="kwrd">in</span>
                                xmlConfiguration.GetAllRegistrations())
  {
    AddImplemeterTypeForContractType(pair.Key, pair.Value);
  }
}</strong>
<span class="kwrd">public</span> <span class="kwrd">void</span> AddImplementerFor&lt;ContractType&gt;(Type implementer)
{
  AddImplemeterTypeForContractType(<span class="kwrd">typeof</span> (ContractType), implementer);
}
<span class="kwrd">private</span> <span class="kwrd">void</span> AddImplemeterTypeForContractType(Type contractType,
                                              Type implementerType)
{
  container.Add(contractType, implementerType);
}
<span class="kwrd">public</span> ContractType GetImplementerOf&lt;ContractType&gt;()
{
  <span class="kwrd">return</span> (ContractType) Activator.CreateInstance(
                          container[<span class="kwrd">typeof</span> (ContractType)]);
}
```
}
}
```

What we've got now? An option of specifying implementers outside of the application code. Having this, teams (team members) can split up, code, and configure an external file to do the mapping between contract and implementer  without touching the application code itself. Implementer is only coupled to the Core (where contract ILogger) is defined. The Core / AssemblyOne  / ConsoleApp know nothing about implementer, but are able to leverage it to do the work.

[![ioc_configuration_file_3](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/UnderstandingIoCContainerPart2_143D6/ioc_configuration_file_3_thumb.png)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/UnderstandingIoCContainerPart2_143D6/ioc_configuration_file_3_2.png)

Next steps? Well, we could talk about chains of dependencies, parameterized constructors,  factories, etc. But this is where I am pausing and suggesting not to re-invent the wheel. Go grab some existing IoC container and pump your application to achieve it's best relying on technology that now you do not consider to be a magical anymore.

Updated code is [here](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/UnderstandingIoCContainerPart2_143D6/IoC_xml.zip).


