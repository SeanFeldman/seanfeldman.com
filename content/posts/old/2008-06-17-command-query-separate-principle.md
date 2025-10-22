---
title: Command-Query Separation Principle
slug: command-query-separate-principle
date: '2008-06-17T05:12:00'
updated: '2008-06-17T05:12:00'
draft: false
tags:
- .NET
- OO
- Patterns
author: Sean Feldman
---


A few days ago read in Larman's book about Command-Query Separation Principle. Funny to mention  that I heard about the concept many times ago, but this is the only source that stated it as a principle. And it makes total sense once you evaluate all the pros and cons of the idea.

What's the principle? Simple. There are two kinds of messages to objects:

* Commands - ones that are affecting the state of the object
* Queries - ones that are querying an object for its' state without affecting its' state at all

A Command message would be "void Calculate()" or "void Add(double value)". Command message never returns a value, and that's for clear separation of the messages and easier maintenance of the object state (i.e. no surprises). A Query message would be what Command isn't "int GetValue()" or "IsVisible()".

One exception the author brought up was internal/private messages that are not a part of the interface, and therefore can violate the principle - I guess this is a matter of personal preference.

An example is an implementation of a Die (for a monopoly game) modified by myself.

```
    public interface IDie   
    {  
        void Roll();  
        int GetFaceValue();  
    }  
      
    public class Die : IDie  
    {  
        private int faceValue;  
        private Random rand = new Random();  
          
        public void Roll()  
        {  
            faceValue = rand.Next(6) + 1;  
        }  
          
        public int GetFaceValue()  
        {  
            return faceValue;  
        }  
    }
```

I added the interface on purpose, to have DbC, where implementation doesn't matter that much, because the contract is expressing well enough the intension of how to use an implementer of  an IDie. Thanks to the CQS Principle it becomes crystal clear. It is easy to determine a value of a die, and there's no surprises when a die is queried for it's value.

Now imagine a system with a significant number of components that violate this principle versus a system where components follow it. Can you imagine the difference?

[![](http://ecx.images-amazon.com/images/I/51997V9J7QL._SL500_BO2,204,203,200_PIlitb-dp-500-arrow,TopRight,45,-64_OU01_AA240_SH20_.jpg)](http://www.amazon.com/Applying-UML-Patterns-Introduction-Object-Oriented/dp/0130925691/ref=sr_1_1?ie=UTF8&s=books&qid=1213679659&sr=1-1)


