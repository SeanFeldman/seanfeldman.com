---
title: Elvis Operator to the Rescue
slug: elvis-operator-to-the-rescue
date: '2016-03-03T05:14:49.092253+00:00'
updated: '2016-03-03T05:14:48.871616+00:00'
draft: false
author: Sean Feldman
---
Null-Conditional Operator in C# 6 (`?.`), also known as "Elvis" operator, has allowed compacting code by removing boilerplate code for a null check to avoid `NullReferenceException`. But there's more to that than just a null check. I've run into a case where Elvis operator also removed need for an extra code to implement a [Decorator pattern](http://www.dofactory.com/net/decorator-design-pattern), which resulted in removing complexity. Here's the original code implemented using Decorator pattern:

```
var useTransaction = ShouldUseTransaction();
using (var tx = useTransaction ?  new TransactionScopeDecorator(new TransactionScope()) : new TransactionScopeDecorator())
{
  // custom code
  tx.Complete();
}
```

Where `TransactionScopeDecorator` was defined in the following way:

```
private class TransactionScopeDecorator : IDisposable
{
    private readonly TransactionScope transactionScope;
    readonly bool hasTx;
    public TransactionScopeDecorator()
    {
        hasTx = false;
    }
    public TransactionScopeDecorator(TransactionScope transactionScope)
    {
        this.transactionScope = transactionScope;
        hasTx = true;
    }
    public void Dispose()
    {
        if (hasTx)
            transactionScope.Dispose();
    }
    public void Complete()
    {
        if (hasTx)
            transactionScope.Complete();
    }
}
```

While the first snippet is easy to read and understand, `TransactionScopeDecorator` is quite a lot to add. Elvis operator takes that away entirely.


```
var useTransaction = ShouldUseTransaction();
using (var tx = useTransaction ? new TransactionScope() : null)
{
    // custom code
    tx?.Complete();
}
```

There are many other handy usages for Elvis operator. What have you used it for in your projects?

