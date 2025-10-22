---
title: Executing Azure Timer function manually
slug: executing-azure-timer-function-manually
date: '2022-03-21T06:34:00'
updated: '2022-03-21T06:38:25.995035+00:00'
draft: false
tags:
- Functions
- Azure
author: Sean Feldman
---
![enter image description here][1]

Azure timer triggered. Functions are convenient for automated execution. With the specified time interval, a function gets to execute when specified and then sleeps until the subsequent execution.

But what happens when a function needs to be executed on demand? For example, during development, when debugging the logic and want to kick off a function right away rather than waiting?

That's possible with the `TimerTrigger` that accepts an additional parameter, `RunOnStartup`. Assign it a value of `true`, and the function will be executed when the Function App starts. You might want to wrap it with `#if DEBUG` to ensure it gets executed upon each deployment or restarting a Function/Function App in production.

```csharp
[FunctionName(nameof(MyTimerTrigger))]
public async Task RunAsync([TimerTrigger("0 0 */12 * * *"
#if DEBUG
  , RunOnStartup = true
#endif
)] TimerInfo myTimer, ExecutionContext executionContext)
{
 // function code
}
```
That's great, but what if I need to force the function to execute not right away? For example, my function executes every 12 hours (`"0 0 */12 * * *"`), and I need to force it to run earlier than that?

One way is to use the CRON expression from a configuration, update the configuration and restart the Function. But that's clunky and inconvenient. A better way is to force the function to execute by making a request through the administrative API.

An HTTP request to the administrative API with a master key will trigger the function execution. The URL is always of the following format:

`https://<function-app>.azurewebsites.net/admin/functions/<function-name>`

For example, https://my-test-funcapp.azurewebsites.net/admin/functions/MyTimerTrigger

The content to POST-ed for a timer-triggered function can be an empty JSON, `"{}"`.
The master key can be found under the Function App Keys section. Careful with the value, do not share or commit it. The value should be passed with the header `x-functions-key`. 

Note: locally, the `x-functions-key` header is not required.

Upon successful execution, HTTP response code 202 Accepted will be returned.

Conveniently enough, this works on _any_ non-HTTP triggered function and on v3 and v4 In-Process SDK and Isolated Worker SDK.

While this little gem is [documented](https://docs.microsoft.com/en-us/azure/azure-functions/functions-manually-run-non-http), it deserves more publicity it brings some excellent options to the table when it comes to invoking non-HTTP functions on demand.


[1]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2022/executing-azure-timer-function-manually/screwdrivers.jpg
