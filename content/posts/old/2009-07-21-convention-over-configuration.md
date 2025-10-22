---
title: Convention over Configuration
slug: convention-over-configuration
date: '2009-07-21T04:23:14'
updated: '2009-07-21T04:23:14'
draft: false
tags:
- .NET
- Agile
- OO
author: Sean Feldman
---


Convention over is defined in [Wikipedia](http://en.wikipedia.org/wiki/Convention_over_configuration) as follow:

> Convention over Configuration (aka Coding by convention) is a software design paradigm which seeks to decrease the number of decisions that developers need to make, gaining simplicity, but not necessarily losing flexibility.

Our current project, that is no longer a skinny cow, has a state machine of message statuses, and a factory that can produce the state object from a key. Today I ran into a bug, when added two new message states, but forgot to update the factory, that happened to reside in a completely different assembly from the one that contains state classes. After a quick trace the bug was found. But how painful it is:

1. As a developer I had to keep in mind to link between new message state classes and message state factory. This is getting easily out of control when you either new to the project or have not worked on it for a while. New developers have to be familiar with the limitation or find it out the difficult way.
2. Each time a message state is added or removed to the state machine, factory has to be updated.
3. Message state factory specification (tests) has to be updated as the production code, and again that’s a manual process that can lead to forgetfulness.

The conclusion was “we have to have **A Pit of Success**”. Convention over Configuration (or simply CoC) is what we need. So I spiked this quickly (no specs, sorry for that) and this is what is looks like.

#### Defining a “State”

```
public abstract class BaseState
{
  public abstract string Name { get; }

  public virtual BaseState MoveToNextState()
  {
```
<span style="color: blue">throw new </span><span style="color: #2b91af">NotImplementedException</span>(<span style="color: blue">string</span>.Format(<span style="color: #a31515">&quot;State '{0}' is not implemented.&quot;</span>, Name));
```
}
}
```

Base abstract BaseState class defines the default behavior and attribute for state name. A few state (three for simplicity) with only ability to move forward would look like the following code snippets.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_27C9B36B.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_6CE280A1.png)

public classInitialState : BaseState
```
<br /></span>{
```
  
  public const stringStateName = "Initial";
  

  
  public override stringName
  
  {
  
    get{ returnStateName; }
  
  }
  

  
  public overrideBaseState MoveToNextState()
  
  {
  
    return newIntermediateState();
  
  }
  
}
  


```
public class IntermediateState : BaseState
{
  public const string StateName = "Intermediate";

  public override string Name
  {
```
<span style="color: blue">get </span>{ <span style="color: blue">return </span>StateName; }
```
}

  public override BaseState MoveToNextState()
  {
```
<span style="color: blue">return new </span><span style="color: #2b91af">FinalState</span>();
```
}
}
```
```
public class FinalState : BaseState
{
  public const string StateName = "Final";

  public override string Name
  {
```
<span style="color: blue">get </span>{ <span style="color: blue">return </span>StateName; }
```
}
}
```

Fairly simple and straightforward. State factory, normally, would be a collection of all states, with a getter behavior that would allow from a key to get the state object. For simplicity, I am omitting the case when requested key has no equivalent state object.

```
public class StateFactory
{
  private static readonly Dictionary<string, BaseState> dictionary = new Dictionary<string, BaseState>
```
{
                                                                      {<span style="color: #2b91af">InitialState</span>.StateName, <span style="color: blue">new </span><span style="color: #2b91af">InitialState</span>()},
                                                                      {<span style="color: #2b91af">IntermediateState</span>.StateName, <span style="color: blue">new </span><span style="color: #2b91af">IntermediateState</span>()},
                                                                      {<span style="color: #2b91af">FinalState</span>.StateName, <span style="color: blue">new </span><span style="color: #2b91af">FinalState</span>()},
                                                                   };
```
public BaseState GetStateFromName(string stateName)
  {
```
<span style="color: blue">return </span>dictionary[stateName];
```
}
}
```

This is the spot where the disconnection has happened. Each time a state is added or removed, dictionary has to be updates as well. So end this up, we can leverage CoC to reflectively discover statuses, and prevent future manual updates and forgetfulness (thanks David for a nice way of putting it in words).

#### Reflective Discoverer

The contract for reflective discoverer would accept 3 Funcs

1. Function to return an array of assemblies to scan, determined at the time of invocation.
2. Function to generate a key value, based on the item type.
3. Function to verify is a type is matching the required criteria (could be predicate).

```
public interface IReflectiveDiscoverer
{
  Dictionary<key_type, item_type> Discover<key_type, item_type>(Func<Assembly[]> assembliesToScan,
```
<span style="color: #2b91af">Func</span>&lt;item_type, key_type&gt; generateKeyFrom,
                                                            <span style="color: #2b91af">Func</span>&lt;<span style="color: #2b91af">Type</span>, <span style="color: blue">bool</span>&gt; verifyTypeCanBeUsed);
```
}
```

Implementation of the contract:

```
public class ReflectiveDiscoverer : IReflectiveDiscoverer
{
  public Dictionary<key_type, item_type> Discover<key_type, item_type>(Func<Assembly[]> assemblies_to_scan,
```
<span style="color: #2b91af">Func</span>&lt;item_type, key_type&gt; generate_key_from,
                                                                   <span style="color: #2b91af">Func</span>&lt;<span style="color: #2b91af">Type</span>, <span style="color: blue">bool</span>&gt; verify_type_can_be_used)
```
{
```
<span style="color: blue">var </span>dictionary = <span style="color: blue">new </span><span style="color: #2b91af">Dictionary</span>&lt;key_type, item_type&gt;();
```
```
<span style="color: blue">foreach </span>(<span style="color: blue">var </span>assembly <span style="color: blue">in </span>assemblies_to_scan())
{
  <span style="color: blue">var </span>all_types_in_assembly = assembly.GetTypes().Where(verify_type_can_be_used);
```
```
<span style="color: blue">foreach </span>(<span style="color: blue">var </span>candidate_type <span style="color: blue">in </span>all_types_in_assembly)
  {
    <span style="color: blue">var </span>instance = (item_type)<span style="color: #2b91af">Activator</span>.CreateInstance(candidate_type);
    dictionary.Add(generate_key_from(instance), instance);
  }
}
```
```
<span style="color: blue">return </span>dictionary;
```
}
}
```

Now it’s time to update StateFactory to use ReflectiveDiscoverer.

```
public class StateFactory
{
  public BaseState GetStateFromName(string stateName)
  {
```
<span style="color: blue">var </span>states = <span style="color: blue">new </span><span style="color: #2b91af">ReflectiveDiscoverer</span>().Discover&lt;<span style="color: blue">string</span>, <span style="color: #2b91af">BaseState</span>&gt;(() =&gt; <span style="color: #2b91af">AppDomain</span>.CurrentDomain.GetAssemblies(),
                                                                    state =&gt; state.Name,
                                                                    type =&gt; type.IsSubclassOf(<span style="color: blue">typeof </span>(<span style="color: #2b91af">BaseState</span>)))
<span style="color: blue">return </span>states[stateName];
```
}
}
```

A few implementation details missing in this version:

1. Factory is used frequently, and probably should keep states cached.
2. We skipped specifications, and therefore have un-testable code.

Fixing those issues is not difficult. For testability we need to inject IReflectiveDiscoverer. For performance issue – keep the dictionary cached.

#### Final Version

```
private static Dictionary<string, BaseState> states;

public StateFactory() : this(new ReflectiveDiscoverer()) {}

public StateFactory(IReflectiveDiscoverer reflectiveDiscoverer)
{
  if (states != null) return;

  states = reflectiveDiscoverer.Discover<string, BaseState>(() => AppDomain.CurrentDomain.GetAssemblies(),
```
state =&gt; state.Name,
                                                        type =&gt; type.IsSubclassOf(<span style="color: blue">typeof </span>(<span style="color: #2b91af">BaseState</span>)));
```
}

public BaseState GetStateFromName(string stateName)
{
  return states[stateName];
}
```

Parameterless constructor is replacing container functionality. “states” dictionary is a static member field that caches states with a guard clause in constructor.

Now, the code is cleaner and automated. No need to add states when those are added or removed. This will ensure that developers don’t make mistake of forgetting to update factory.

Finally, if we developers embrace the concept “People don’t fail, processes do”, our code will be better.


