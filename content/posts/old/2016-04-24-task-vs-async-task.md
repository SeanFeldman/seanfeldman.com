---
title: Task vs async Task
slug: task-vs-async-task
date: '2016-04-24T03:13:00'
updated: '2016-04-24T03:13:26.913332+00:00'
draft: false
tags:
- .NET
author: Sean Feldman
---
How often do you write code and think about what will it look like the compiler is done with it? If you're like me, not often. But is it a good thing that over the time we've learned to trust unquestionably the compiler and blindly rely on it to do the job for us? 

I was lucky to get some guidance from [Daniel Marbach][1] on `async`/`await` and the importance of understanding code optimizations that compiler is performing. Without any further due, let's dive into an example.

Consider the following method:

```csharp
Task MainAsync()
{
   return Task.Delay(1000);
}
```
Now the same method with a slight variation, marking the method as async and awaiting the delay.

```csharp
async Task MainAsync()
{
   await Task.Delay(1000);
}
```
Looks almost identical. But is it? Let's look at what compiler generates.

For the first method, it's identical to the original code:

```csharp
Task MainAsync()
{
   return Task.Delay(1000);
}
```
But for the second method, the compiler does... magic and voodoo.

```csharp
private Task MainAsync2()
{
	UserQuery.\u003CMainAsync2\u003Ed__2 mainAsync2D2 = new UserQuery.\u003CMainAsync2\u003Ed__2();
	mainAsync2D2.\u003C\u003E4__this = this;
	mainAsync2D2.\u003C\u003Et__builder = AsyncTaskMethodBuilder.Create();
	mainAsync2D2.\u003C\u003E1__state = -1;
	AsyncTaskMethodBuilder taskMethodBuilder = mainAsync2D2.\u003C\u003Et__builder;
	((AsyncTaskMethodBuilder) @taskMethodBuilder).Start<UserQuery.\u003CMainAsync2\u003Ed__2>((M0&) @mainAsync2D2);
	return ((AsyncTaskMethodBuilder) @mainAsync2D2.\u003C\u003Et__builder).get_Task();
}
```
No magic. The compiler just creates a state machine due to async/await keywords. 
 

```csharp
[/*Attribute with token 0C000007*/CompilerGenerated]
  private sealed class \u003CMainAsync2\u003Ed__2 : IAsyncStateMachine
  {
	public int \u003C\u003E1__state;
	public AsyncTaskMethodBuilder \u003C\u003Et__builder;
	public UserQuery \u003C\u003E4__this;
	private TaskAwaiter \u003C\u003Eu__1;
	public \u003CMainAsync2\u003Ed__2()
	{
	  base.\u002Ector();
	}
	void IAsyncStateMachine.MoveNext()
	{
	  int num1 = this.\u003C\u003E1__state;
	  try
	  {
		TaskAwaiter taskAwaiter;
		int num2;
		if (num1 != 0)
		{
		  taskAwaiter = Task.Delay(1000).GetAwaiter();
		  // ISSUE: explicit reference operation
		  if (!((TaskAwaiter) @taskAwaiter).get_IsCompleted())
		  {
			this.\u003C\u003E1__state = num2 = 0;
			this.\u003C\u003Eu__1 = taskAwaiter;
			UserQuery.\u003CMainAsync2\u003Ed__2 mainAsync2D2 = this;
				((AsyncTaskMethodBuilder) @this.\u003C\u003Et__builder).AwaitUnsafeOnCompleted<TaskAwaiter, UserQuery.\u003CMainAsync2\u003Ed__2>((M0&) @taskAwaiter, (M1&) @mainAsync2D2);
			return;
		  }
		}
		else
		{
		  taskAwaiter = this.\u003C\u003Eu__1;
		  this.\u003C\u003Eu__1 = (TaskAwaiter) null;
		  this.\u003C\u003E1__state = num2 = -1;
		}
		((TaskAwaiter) @taskAwaiter).GetResult();
		taskAwaiter = (TaskAwaiter) null;
	  }
	  catch (Exception ex)
	  {
		this.\u003C\u003E1__state = -2;
		((AsyncTaskMethodBuilder) @this.\u003C\u003Et__builder).SetException(ex);
		return;
	  }
	  this.\u003C\u003E1__state = -2;
	  ((AsyncTaskMethodBuilder) @this.\u003C\u003Et__builder).SetResult();
	}
	[/*Attribute with token 0C000008*/DebuggerHidden]
	void IAsyncStateMachine.SetStateMachine(/*Parameter with token 08000001*/IAsyncStateMachine stateMachine)
	{
	}
  }
```
The moral of this is simple: if you don't need to await, just return the `Task`. It will do the same, and you'll save a lot of unnecessary state machine construction, with its wasteful memory and execution where it's not needed.


[1]: http://www.planetgeek.ch/author/danielmarbach/

