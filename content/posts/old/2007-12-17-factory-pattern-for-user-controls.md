---
title: Factory Pattern for User Controls
slug: factory-pattern-for-user-controls
date: '2007-12-17T17:01:10'
updated: '2007-12-17T17:01:10'
draft: false
tags:
- .NET
- ASP.NET
- OO
- Patterns
author: Sean Feldman
---


User Controls are handy when working in web forms, but what a mess they can generate. I was asked what to do when UCs are used and some dependencies need to be injected during the construction - but UCs are a bit tricky in regards to construction. So the possibilities are:

1. Use new operator and instantiate a user control (Web Application Project) - no good as the visual elements residing on the designer surface (.ascx) then not loaded.

2. Use Page.LoadControl(<path>) - but no option to pass in parameters.

3. Use Page.LoadControl(<type>, params object) - not strongly typed.

So all these possibilities are nice, but not helping to use a load with strongly typed parameters. Then the idea proposed at one of the replies with almost the same question was to use a static factory. I tried to play with the idea and this was a result.

Step 1 - create the UC

| ``` <%@ Control Language="C#" AutoEventWireup="true" CodeBehind="SomeUserControl.ascx.cs" Inherits="LoadControlWithFactory.SomeUserControl" %> <asp:TextBox runat="server" id="txtName"></asp:TextBox> ``` |
| --- |

Step 2 - create the code behind with static factory method

| ```     1:    public partial class SomeUserControl : UserControl    2:    {    3:      private string name;    4:    5:      protected override void OnLoad(EventArgs e)    6:      {    7:        base.OnLoad(e);    8:        txtName.Text = name;    9:      }   10:   11:      public static SomeUserControl Create(string name)   12:      {   13:        SomeUserControl some =        ((Page)HttpContext.Current.Handler).LoadControl("~/SomeUserControl.ascx") as SomeUserControl;   14:        some.name = name;   15:        return some;   16:      }   17:    }  ``` |
| --- |

Note: the underlined code has a bad smell - but that was the only idea I had to gain access to the currently executed page. Any other ideas are welcomed.

Step 3 - load UC dynamically through the code with injected data

| ```     1:    public partial class _Default : System.Web.UI.Page    2:    {    3:      protected override void OnPreRender(EventArgs e)    4:      {    5:        base.OnPreRender(e);    6:        phContent.Controls.Add(SomeUserControl.Create("Sean Feldman"));    7:        phContent.Controls.Add(SomeUserControl.Create("Anna Feldman"));    8:      }    9:    }  ``` |
| --- |

Conclusions

What it seems is that this allowed a few more things than just a pattern implementation. It allowed:

1. DRY principle - rather than replicating the .ascx path wherever UC is loaded, this information is now stored and encapsulated inside the factory.
   ```
   LoadControl("~/SomeUserControl.ascx") as SomeUserControl; // for Sean
   LoadControl("~/SomeUserControl.ascx") as SomeUserControl; // for Sean
   ```
   - Simplicity - **Drop Dead Simple** principle (well, this is something I like to apply recently to the code to make is easy to digest, so this is the name I came up with).
     > | ```  SomeUserControl.FactoryMethod();  ``` |
     > | --- |
     
     - Maintainability - simple and affordable.

Update 2007-12-17: I have re-arranged slightly the post to minimize clipping and attached the [code](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/StaticFactoryMethod.zip).


