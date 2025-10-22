---
title: Two Loosely Coupled Code - Part 2
slug: two-loosely-coupled-code-part-2
date: '2008-06-11T15:15:40'
updated: '2008-06-11T15:15:40'
draft: false
tags:
- .NET
- OO
author: Sean Feldman
---


In the  I raised the question of "Too loosely coupled design". There's a lot to discuss about it, and I am not going more time on it, except showing one more sample that IMHO shows the benefits and outcomes of the principle being applies, or consequences of not doing so.

Table 1

```
namespace Local.ADL.Home
{
  public class HomePresenter : IPresenter
  {
```
<span class="kwrd">private</span> <span class="kwrd">readonly</span> IHomeModel model;
<span class="kwrd">private</span> <span class="kwrd">readonly</span> IHomeView view;
```
```
<span class="kwrd">public</span> HomePresenter(IHomeView view): 
                    <span class="kwrd">this</span>(view, <u><span class="kwrd">new</span> HomeModel()</u>){}
```
```
<span class="kwrd">public</span> HomePresenter(IHomeView view, IHomeModel model)
{
  <span class="kwrd">this</span>.view = view;
  <span class="kwrd">this</span>.model = model;
}
```
```
<span class="kwrd">public</span> <span class="kwrd">void</span> Initialize()
{
  view.Load += View_OnLoad;
}
```
```
<span class="kwrd">private</span> <span class="kwrd">void</span> View_OnLoad(<span class="kwrd">object</span> sender, EventArgs e)
{
  <span class="kwrd">if</span> (!view.IsPostBack)
  {
    view.AssignInitialData(model.IsUserMemberOfPlanAOrPlanB(),
            model.CanShowSomething());
  }
}
```
}
}

```

Table 2

```
namespace Local.ADL.Home
{
  public class HomeModel : IHomeModel
  {
```
<span class="kwrd">public</span> <span class="kwrd">bool</span> IsUserMemberOfPlanAOrPlanB()
{
  <span class="kwrd">return</span> <u>UserSession.IsPlanAorB</u>;
}
```
```
<span class="kwrd">public</span> <span class="kwrd">bool</span> CanShowSomething()
{
  <span class="kwrd">return</span> <u>UserSession.ShouldSeeSomething</u>;
}
```
}
}
```

**Q:** Can HomePresenter be tested based on the code in Table 1?

**A:** Yes. It has a parameterized constructor that accepts all dependencies for HomePresenter as contracts (interfaces) without knowing or carrying who are the real components that implement those contracts. Loosely coupled code, where we depend upon abstraction and not concrete implementation.

**Q:** Does HomePresenter is loosely coupled at run-time?

**A:** No. It has a direct dependency on HomeModel class. This is a tight coupling, meaning that anywhere in the code we used this type of coupling, we made HomeModel “visible” for HomePresenter, i.e. we violated the principle of depending upon abstraction and not concrete implementation. What would be a solution? Dependency Injection Principle with a standard container (lets call it DependencyResolver). Using this simple principle would change the code to be something similar to the code in Table 3. Now HomePresenter is loosely coupled to the implementer of the IHomeModel contract. Some configuration file / startup code will determine who is the actual implementer at run-time. Testing is still possible.

Table 3

```
namespace Local.ADL.Home
{
  public class HomePresenter : IPresenter
  {
```
<span class="kwrd">private</span> <span class="kwrd">readonly</span> IHomeModel model;
<span class="kwrd">private</span> <span class="kwrd">readonly</span> IHomeView view;
```
```
<span class="kwrd">public</span> HomePresenter(IHomeView view): 
   <span class="kwrd">this</span>(view, <u>DependencyResolver.GetImplementerOf(IHomeModel)</u>){}
```
```
<span class="kwrd">public</span> HomePresenter(IHomeView view, IHomeModel model)
{
  <span class="kwrd">this</span>.view = view;
  <span class="kwrd">this</span>.model = model;
}
```
```
<span class="rem">// ...</span>
```

```

**Q:** Can HomeModel be tested based on the code in Table 2?

**A:** No. It is tightly coupled to the UserSession, which in its’ case is a static class and cannot be mocked / faked / taken out as a component that is not required to be tested at this moment.

To solve it:

* UserSession has to be implementer of a contract, lets call it IUserSession
* The implementer of IUserSession has to be supplied / injected as a dependency during construction time either directly or through container, similar to the example in HomePresenter code in Table 3















