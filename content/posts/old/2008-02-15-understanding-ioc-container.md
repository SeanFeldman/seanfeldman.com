---
title: Understanding IoC Container
slug: understanding-ioc-container
date: '2008-02-15T05:58:00'
updated: '2008-02-15T05:58:00'
draft: false
tags:
- .NET
- OO
- Patterns
author: Sean Feldman
---


In a multi layered application architecture, loosely coupled code is more than a important. It's the basic which can either help the entire project progress, or drive it down the slope to the end (in the bad meaning of the word). One of the basics to keep coupling as low as possible is Inversion of Control (IoC) container.

I will try to show how to put in place a simple version of IoC container to allow loosely coupled design. The solution will contain several projects to emulate a layered application as much as possible. The choice of console application is only driven by intent to keep it as simple as possible.

In our application we do basic logging at all layers. Logger that does it is following the next contract:

```
  public interface ILogger  
  {  
    void Log(string message);  
  }
```

Lets assume that the initial version of logger is implemented as a simple Console logger:

```
  public class ConsoleLogger : ILogger  
  {  
    public void Log(string message)  
    {  
      System.Console.WriteLine(message);  
    }  
  }
```

Now lets look what the layered structure looks like. The lowest layer in the stack is going to be Core. This one will contain the interfaces (such as ILogger for instance) all other layers have to consume. This is a sort of tight coupling, but it is not bad as upper layers will depend on abstraction and not concrete implementation (DIP).

[![ioc_layered_structure](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/UnderstandingIoCContainer_12237/ioc_layered_structure_thumb.jpg)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/UnderstandingIoCContainer_12237/ioc_layered_structure_2.jpg)

AssemblyOne, Two, Three, and others are all potential layers you could have (and I am not necessarily insisting on having them - there should be a rational limit). ConsoleApp is the top layer that represent the application. This could be easily a Windows application or a web application.

To spice up our life, we have to implement a gadget in AssemblyOne that will follow a certain contract (IGadget) and each operation defined by the contract, has to be logged when implementation is invoked. The contract is:

```
  public interface IGadget  
  {  
    void TurnOn();  
    void TurnOff();  
  }
```

Now the implementation of the Gadget will be quiet simple:

```

   1:  using Core;
   2:
   3:  namespace AssemblyOne
   4:  {
   5:    public class Gadget : IGadget
   6:    {
   7:      private readonly ILogger logger;
   8:
   9:      public Gadget(ILogger logger)
  10:      {
  11:        this.logger = logger;
  12:      }
  13:
  14:      // Default constructor will be discussed a bit later
  15:      // public Gadget() {}
  16:
  17:      public void TurnOn()
  18:      {
  19:        logger.Log("TurnOn");
  20:      }
  21:
  22:      public void TurnOff()
  23:      {
  24:        logger.Log("TurnOff");
  25:      }
  26:    }
  27:  }

```

The program in the upper (ConsoleApp) layer will look this way:

```

   1:  using System;
   2:  using AssemblyOne;
   3:  using Core;
   4:
   5:  namespace ConsoleApp
   6:  {
   7:    internal class Program
   8:    {
   9:      private static void Main()
  10:      {
  11:        AppCode();
  12:
  13:        Console.WriteLine("done.");
  14:        Console.ReadLine();
  15:      }
  16:
  17:      private static void AppCode()
  18:      {
  19:        ConsoleLogger logger = new ConsoleLogger();
  20:        Gadget gadget = new Gadget(logger);
  21:        gadget.TurnOn();
  22:        gadget.TurnOff();
  23:      }
  24:    }
  25:  }

```

AppCode method (lines 19-22) is what we are interested in. A few question can be raised at this point:

1. Why logger is of type ConsoleLogger and not ILogger? Isn't this wrong?
2. Why gadget is of type Gadget and not IGadget? Same smell?
3. What if we need to move logger implementer to a different layer than the ConsoleApp?

These are all excellent questions. The first two are definetely a bad smell. Why? Well, because we should be really sticking to what contracts were obligating implementers, and not be even able to use the "extras" provided by contract implementers "outside" of the contract. This will eliminate any chance that an "undocumented" by contract method will extinct from existing, causing our client code to break. The third question is the one that shows that current design is not going to work - current ILogger implementer is located in ConsoleApp layer and we have to pass it as a dependency into gadget. But what if we introduce another implementation of ILogger, like XML logger, and it will live in another layer, AssemblyTwo? And what if we want to be able to create gadget without specifying logger, relying on a default one? This is where IoC container would help.

The idea behind container is simple: lower layer provides an option of registering a contract implementer, and later, retrieve that contract implementer instance, by just using the contract type. Expressing this in code would look like the next snippet:

```
namespace Core.IoC  
{  
  public interface IContainer  
  {  
    // register contract implementer  
    void AddImplementerFor<ContractType>(Type implementer);  
    // retrieve contract implementer  
    ContractType GetImplementerOf<ContractType>();  
  }  
}
```

Implementation of this contract is a subject to a separate discussion. To keep it simple, I have decided to use the simplest way out there:

```

   1:  using System;
   2:  using System.Collections.Generic;
   3:
   4:  namespace Core.IoC
   5:  {
   6:    public class Container : IContainer
   7:    {
   8:      public static readonly IContainer Instance = new Container();
   9:
  10:
  11:      private readonly Dictionary container;
  12:
  13:      private Container()
  14:      {
  15:        container = new Dictionary();
  16:      }
  17:
  18:      public void AddImplementerFor(Type implementer)
  19:      {
  20:        container.Add(typeof(ContractType), implementer);
  21:      }
  22:
  23:      public ContractType GetImplementerOf()
  24:      {
  25:        return
  (ContractType)Activator.CreateInstance(container[typeof (ContractType)]);
  26:      }
  27:    }
  28:  }

```

Yes, the core secret is in Activator class, provided by .NET framework. No magic.

With this in hand, we can start using container all other the place, breaking the dangerous coupling. First thing first, registering contracts and their implementers for the application. This will change how we start our application:

```

   1:  using System;
   2:  using AssemblyOne;
   3:  using Core;
   4:  using Core.IoC;
   5:
   6:  namespace ConsoleApp
   7:  {
   8:    internal class Program
   9:    {
  10:      private static void Main()
  11:      {
  12:        ApplicationStartup();
  13:
  14:        AppCode();
  15:
  16:        Console.WriteLine("done.");
  17:        Console.ReadLine();
  18:      }
  19:
  20:      private static void ApplicationStartup()
  21:      {
  22:        Container.Instance.AddImplementerFor(typeof(
```
ConsoleLogger));
```
23:        Container.Instance.AddImplementerFor(typeof(Gadget));
  24:      }
  25:
  26:      private static void AppCode()
  27:      {
  28:        IGadget gadget =
```
Container.Instance.GetImplementerOf<IGadget>();
```
29:        gadget.TurnOn();
  30:        gadget.TurnOff();
  31:      }
  32:    }
  33:  }

```

Line 12 introduces a new (quiet old actually) concept - application startup point. In web application something like Application\_Start in Global.asax would be an equivevalent. What it does is teaching the container about contracts, and who are the implementers. That way, we can get an instance of an IGadget without worrying who implements it (line 28). Also we don't need to directly inject the logger dependency, due to the fact that gadget can query for the default logger through the container. Updated logger looks like this:

```

   1:  using Core;
   2:  using Core.IoC;
   3:
   4:  namespace AssemblyOne
   5:  {
   6:    public class Gadget : IGadget
   7:    {
   8:      private readonly ILogger logger;
   9:
  10:      public Gadget(ILogger logger)
  11:      {
  12:        this.logger = logger;
  13:      }
  14:
  15:      public Gadget() :
```
this(Container.Instance.GetImplementerOf<ILogger>()) {}
```
16:
  17:      public void TurnOn()
  18:      {
  19:        logger.Log("TurnOn");
  20:      }
  21:
  22:      public void TurnOff()
  23:      {
  24:        logger.Log("TurnOff");
  25:      }
  26:    }
  27:  }

```

Line 15 defines a default constructor that leverages container to get the default implementation of logger.

Now we will substitute the default logger by another implementer, from another assembly (AssemblyTwo) that logs information into an XML file:

```

   1:  using System;
   2:  using System.IO;
   3:  using System.Xml;
   4:  using Core;
   5:
   6:  namespace AssemblyTwo
   7:  {
   8:    public class XmlLogger : ILogger
   9:    {
  10:      private readonly string fileName;
  11:
  12:      public XmlLogger() : this("log.xml")
  13:      {
  14:      }
  15:
  16:      public XmlLogger(string fileName)
  17:      {
  18:        this.fileName = fileName;
  19:      }
  20:
  21:      public void Log(string message)
  22:      {
  23:        XmlDocument document = new XmlDocument();
  24:        string filePath = Path.GetFullPath(fileName);
  25:        CreateFileIfDoesntExist(filePath);
  26:        document.Load(filePath);
  27:        XmlElement root = document.DocumentElement;
  28:        XmlElement element = document.CreateElement("log");
  29:        element.SetAttribute("timestamp",
```
DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss.fff"));
```
30:        element.InnerText = message;
  31:        root.AppendChild(element);
  32:        document.Save(fileName);
  33:      }
  34:
  35:      private void CreateFileIfDoesntExist(string filePath)
  36:      {
  37:        if (!File.Exists(filePath))
  38:        {
  39:          XmlWriter writer = XmlTextWriter.Create(fileName);
  40:          writer.WriteProcessingInstruction("xml",
```
"version='1.0' encoding='UTF-8'");
```
41:          writer.WriteStartElement("logs");
  42:          writer.Close();
  43:        }
  44:      }
  45:    }
  46:  }

```

The adjustment has to be done to the startup method to register the new implementer in the container:

```
    private static void ApplicationStartup()  
    {  
      Container.Instance.AddImplementerFor<ILogger>(typeof(XmlLogger));  
      Container.Instance.AddImplementerFor<IGadget>(typeof(Gadget));  
    }
```

Now the entire system uses XML logger as a default logger:

[![ioc_layered_structure_container](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/UnderstandingIoCContainer_12237/ioc_layered_structure_container_thumb.jpg)](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/UnderstandingIoCContainer_12237/ioc_layered_structure_container_2.jpg)

There is a scenario when contract implementer is in an assembly that should not be referenced from the code (due to the fact that it is just not available during the development time)? Then something like an external file for container configuration can/should be used. We will have to specify the assembly name as well, so the activator would be able through the reflection to invoke constructor.

Bottom line - this is far from being perfect, but it was not intended to do the heavy lifting (though could be used to do IoC container work). My recommendation would be to understand what power it gives you and take one of the existing containers such as Windsor, Spring.NET, StructureMap, etc.

...hey, what's up with the log there? Was it working at all? See for yourself, get the [code](https://aspblogs.blob.core.windows.net/media/sfeldman/WindowsLiveWriter/UnderstandingIoCContainer_12237/IoC_2.zip)

Part 2 of this blog is [here](/sfeldman/archive/2008/02/20/understanding-ioc-container-part-2.aspx).


