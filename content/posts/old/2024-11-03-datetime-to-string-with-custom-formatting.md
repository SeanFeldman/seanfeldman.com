---
title: DateTime to String with Custom Formatting
slug: datetime-to-string-with-custom-formatting
date: '2024-11-03T20:49:36.494129+00:00'
updated: '2024-11-03T20:49:36.384646+00:00'
draft: false
tags:
- C#
author: Sean Feldman
---
When formatting `DateTime` to a string, the format specifier provides access to the parts of the date and time we want to express as a string. E.g. 
```csharp
DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss.fff")
```
will produce something like `2024-11-03 12:34:56.789`. But, you must be extra careful with the time separator `:`. It's not always the same for all cultures, and if an explicit culture is not specified, the default local culture might surprise you. Let's see an example.

Let's say the code is running on a machine set up with Finish culture. 

```csharp
DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss.fff", new CultureInfo("fi-FI")).Dump();
```
The same code snippet used earlier produces an entirely different result, `2024-11-03 12.34.56.789`. But how is that possible? That's because the `:` custom format specifier is culture-specific. The separator character must be specified within a literal string delimiter to change the time separator for a particular date and time string. 

```csharp
DateTime.UtcNow.ToString("yyyy-MM-dd HH':'mm':'ss.fff")
```
 Or escaped. 

```csharp
DateTime.UtcNow.ToString("yyyy-MM-dd HH\\:mm\\:ss.fff")
```
Escaping would be required to avoid surprises if date formatting `yyyy/MM/dd` is needed. Find more about date and time separator specifiers on [MSDN][1].

[1]: https://learn.microsoft.com/en-us/dotnet/standard/base-types/custom-date-and-time-format-strings#date-and-time-separator-specifiers
