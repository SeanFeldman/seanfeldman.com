---
title: WPF - DataContext And IValueConverter Thoughts
slug: wpf-datacontext-and-ivalueconverter-thoughts
date: '2008-08-13T15:48:04'
updated: '2008-08-13T15:48:04'
draft: false
tags:
- .NET
- WPF
author: Sean Feldman
---


I am a total newbie in WPF development. One of the things I wanted to have is to format the values coming out of my domain object into UI, and being able to parse those values back into business objects.

I am coming from a web environment, where no state exists in between requests. I started with an approach usually apply in the web applications, quickly realizing it will not work that way. The fact that DataContext (like a ViewData) is there and doesn't have to be reconstructed is great. The down side - it's not strongly typed. At the same time maybe the only way to use it is one, when assigning the data(object) and that's it. Also bugging the fact that the properties are used for binding as string texts, but that I have to understand better.

Since the DataContext is going nowhere, and it's a reference to domain object, DataBinding done in TwoWay mode (which is the default) assures that any change (as long as it is valid) will propagate back into the domain object (it's property). Converters are another piece of this not so trivial puzzle - they make life easy. By implementing IValueConverter, it is possible to implement the logic for value transformations upon each way of binding. Handy, since it allowed me to decorate currency attributes of my domain object to show currency details on UI, and strip that off and get a plain number when taking the currency value back into the domain object.

The XAML way - not sure I like it completely at this stage. Being able to express binding and converter for the binding in a codeless way is nice. The facts that:

* You have to create a static resource on each "view" (window/user control) did not sound well
* The loose control over the binding gives you now firm understanding of what's going on behind the scene

So I started to poke around the idea of using a single converter all over the place. And found it. Again, declaratively, it was a mess, since WPF XAML parse had an issue with it, even though it was compiling. Pure code approach was simple, and XAML parser did not complain.

I put converter into a single location where it can be used by any "view" and it looked like this:

```
namespace WpfApplication1
{
  public static class Converters
  {
```
<span class="kwrd">public</span> <span class="kwrd">static</span> CurrencyConverter CurrencyConverter = <span class="kwrd">new</span> CurrencyConverter();
```
}
}
```

And the code that was doing binding looked like the following snippet:

```
var binding = new Binding("Amount");
binding.Source = myObject;
binding.Converter = Converters.CurrencyConverter;
txt.SetBinding(TextBox.TextProperty, binding);
```

The declarative way looked uglier:

```
<Window x:Class="WpfApplication1.MainWindow"
```
<span class="attr">xmlns</span><span class="kwrd">="http://schemas.microsoft.com/winfx/2006/xaml/presentation"</span>
<span class="attr">xmlns:x</span><span class="kwrd">="http://schemas.microsoft.com/winfx/2006/xaml"</span>
<span class="attr">xmlns:app</span><span class="kwrd">="clr-namespace:WpfApplication1"</span><span class="kwrd">&gt;</span>
```
<Grid>
```
<span class="kwrd">&lt;</span><span class="html">Grid.RowDefinitions</span><span class="kwrd">&gt;</span>
  <span class="kwrd">&lt;</span><span class="html">RowDefinition</span> <span class="kwrd">/&gt;</span>
  <span class="kwrd">&lt;</span><span class="html">RowDefinition</span> <span class="kwrd">/&gt;</span>
<span class="kwrd">&lt;/</span><span class="html">Grid.RowDefinitions</span><span class="kwrd">&gt;</span>
    <span class="kwrd">&lt;</span><span class="html">TextBox</span> <span class="attr">Grid</span>.<span class="attr">Row</span><span class="kwrd">="0"</span>
                 <span class="attr">Text</span><span class="kwrd">="{Binding Path=Amount, Converter={x:Static app:Converters.CurrencyConverter}}"</span>
                <span class="attr">Height</span><span class="kwrd">="20"</span> <span class="attr">Width</span><span class="kwrd">="100"</span><span class="kwrd">&gt;&lt;/</span><span class="html">TextBox</span><span class="kwrd">&gt;</span>
<span class="kwrd">&lt;</span><span class="html">Button</span> <span class="attr">Grid</span>.<span class="attr">Row</span><span class="kwrd">="1"</span> <span class="attr">Name</span><span class="kwrd">="btn"</span> <span class="attr">Height</span><span class="kwrd">="20"</span> <span class="attr">Content</span><span class="kwrd">="Report value"</span><span class="kwrd">&gt;&lt;/</span><span class="html">Button</span><span class="kwrd">&gt;</span>
```
</Grid>
</Window>
```

The currency converter is dead simple:

```
namespace WpfApplication1
{
  [ValueConversion(typeof(double), typeof(string))] 
  public class CurrencyConverter : IValueConverter
  {
```
<span class="kwrd">public</span> <span class="kwrd">object</span> Convert(<span class="kwrd">object</span> <span class="kwrd">value</span>, Type targetType, <span class="kwrd">object</span> parameter, CultureInfo culture)
{
  <span class="kwrd">return</span> ((<span class="kwrd">double</span>) <span class="kwrd">value</span>).ToString(<span class="str">"C2"</span>, culture);
}
<span class="kwrd">public</span> <span class="kwrd">object</span> ConvertBack(<span class="kwrd">object</span> <span class="kwrd">value</span>, Type targetType, <span class="kwrd">object</span> parameter, CultureInfo culture)
{
  <span class="kwrd">double</span> result;
  <span class="kwrd">double</span>.TryParse(<span class="kwrd">value</span>.ToString(), NumberStyles.Currency, culture, <span class="kwrd">out</span> result);
  <span class="kwrd">return</span> result;
}
```
}
}
```

Thoughts, comments, sources for more information are more than appreciated.


