---
title: Automatically create Service Bus trigger queue for Azure Function
slug: automatic-queue-creation-for-function
date: '2021-01-08T07:41:25.222065+00:00'
updated: '2021-01-08T07:41:25.206462'
draft: false
tags:
- Azure
- Functions
- AzureServiceBus
author: Sean Feldman
---
![header][1]

Azure Functions are great. Take HTTP triggered Function. You make a request, it's passed into the Function code, the code is executed, and that's it. Simple. What does it take to deploy an HTTP-triggered function? Packaging and deploying it.

```
[FunctionName("HttpTriggerFunc")]
public async Task<IActionResult> Run(
    [HttpTrigger(AuthorizationLevel.Function, "get", "post", Route = null)]
    HttpRequest req, ILogger log)
{
    log.LogInformation("C# HTTP trigger function processed a request.");
```

```
string name = req.Query["name"];
```

```
return name != null
        ? (ActionResult)new OkObjectResult($"Hello, {name}")
        : new BadRequestObjectResult("Please pass a name on the query string");
}
```

If only all triggers were that simple. Let's take a queue triggered Function.

Let's write a function that is triggered by incoming messages on a queue called `myqueue` and logs its label to mimic the message's processing. Here's how the code would look like:

```
[FunctionName("ServiceBusQueueTriggerCSharp")]                    
public Task Run([ServiceBusTrigger("myqueue")] Message message, ILogger log)
{
    log.LogInformation($"Received message with label: {message.Label}");
    return Task.CompletedTask;
}
```

What does it take to deploy a Service Bus triggered function? Packaging and deploying it? Unfortunately not that simple. The queue that we'd like the function to be listening to has to be provisioned first. But to trigger the function the message has to arrive from that queue. This means it has to be there in the first place before the function even runs. A queue-triggered function will only execute if there's a message, i.e. a queue has to be there. That's sort of a chicken and egg situation.

The obvious solution is to provision the queue first and then deploy the function. While some even prefer this controlled infrastructure deployment, some prefer not to split the queue provision and the deployment of the function. I.e. have the function to create what's needed. What's gives?

Sometimes, a brute force approach is an approach to take. If you're using statically defined Functions, have a look at using the `FunctionsHostBuilder` approach. It enables the generic host approach and DI container use with Functions. It also opens up the option of executing an arbitrary code when setting up dependencies. And it runs _before_ any trigger, upon function startup.

```
[assembly: FunctionsStartup(typeof(Startup))]
public class Startup : FunctionsStartup
{
    public override void Configure(IFunctionsHostBuilder builder)
    {
      // DI setup
    }
}
```

This is the spot that could be used to "hack" the provisioning of the necessary infrastructure! Adding a helper method to create the queue:

```
static async Task CreateTopology(IConfiguration configuration)
{
    var connectionString = configuration.GetValue<string>("AzureWebJobsServiceBus"); // this is the default connection string name
    var managementClient = new ManagementClient(connectionString);
    if (!await managementClient.QueueExistsAsync("myqueue"))
    {
        await managementClient.CreateQueueAsync("myqueue");
    }
}
```

All that's left is to call the helper method from the Configure class. Unfortunately, this would be calling an asynchronous helper method from a synchronous `Configure` method, which will require somewhat dirty implementation but hey, à la guerre comme à la guerre!

```
[assembly: FunctionsStartup(typeof(Startup))]
public class Startup : FunctionsStartup
{
    public override void Configure(IFunctionsHostBuilder builder)
    {
      CreateTopology(builder.GetContext().Configuration).GetAwaiter().GetResult();
    }
}
```

That's it. Now the function can be deployed, and no need to worry about queue deployment. The helper method is invoked once only when a function instance is created or scaled-out. A small price to pay to not worry about queue provisioning: the same approach can be applied to subscription-triggered functions.


[1]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2021/automatic-queue-creation-for-function/chicken-egg.jpg
