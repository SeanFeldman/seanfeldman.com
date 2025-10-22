---
title: Building NuGet Notifications Nano Service with Azure Functions
slug: building-nuget-notifications-nano-service-with-azure-functions
date: '2016-05-09T06:12:09.820514+00:00'
updated: '2016-05-09T06:12:09.804884+00:00'
draft: false
tags:
- Functions
author: Sean Feldman
---
Cloud Services (CS), then WebApps (formerly Web Sites), then WebJobs, and now Azure Functions.  Are Functions to replace the predecessors? Well, before we jump into conclusion and "function" it all, I wanted to find where functions would make sense. 
Among the things I do, I maintain a repository that has a dependency on Azure Service Bus (ASB). Whenever a new version of ASB is released, I'd like to get notified. Yes, there are services to achieve it. Though, imagine there are none. This kind of "service" is a self-contained. Very simple functionality and dependencies. The behavior is clear: detect if there's a new version of the package. If there's one, send a notification (email). Repeat the procedure every given period.

Imagine proceeding with Cloud Services. A cloud service would require a role (probably worker role). With a single instance, you'd still be looking at running a full VM 24/7. Doesn't sound too appealing.
A better alternative could be going with WebApps. With a shared plan, it could be a good compromise. But if you already have a WebApp, you could also implement this as a WebJob. A WebJob that would behave like a light service. Though this will require a WebApp. Not so light anymore. Notice I don't like to call it a micro. It's a nano-service! Oh well, without trolling, it could be looked at as a safe contained functionality w/o dependencies for input or output. 

To implement a function to notify about ASB NuGet package changes, I'm going to use NuGet API to query about recent package changes. Azure Functions are implemented on top of WebJobs. That allows keeping files around between executions. I'll keep a "stamp" file to know when was the last execution. Whenever a package is released past an existing stamp, an email will be sent out announcing about a new package. For email functionality, I'm going to use SendGrid  (with 25,000 emails per day a free tier should be more than enough). The function will be running every 24 hours. A little excessive if you ask me (unless ASB team will be releasing like crazy). 
With Azure Functions being charged based on GB/sec, and the first 400k GB/Sec and the first 1 million requests free, it will take quite a long time to accumulate and significant charges. 
How is this possible, you might think? Thanks to the new, Dynamic Hosting, functions can execute for a short period w/o significant charges.

To start a new function, https://functions.azure.com is the address. https://functions.azure.com If you'd like to play with the experimental features, use the canary link https://functions-next.azure.com

A function is defined by a single `run.csx` default file. It can be more complex and reference other files, though I'd argue if you get into that, you probably not using Functions for what it was intended.

To provide 3rd party assemblies (NuGet and SendGrid APIs), nuget packages can be referenced and Azure Functions will restore those. References are defined in by adding the appropreate references in the `Project.json` file. Create one if it doesn't exist in the same folder for the function you're working on.

```
{
  "frameworks": {
    "net46":{
      "dependencies": {
        "NuGet.PackageManagement": "3.4.3",
        "SendGrid": "6.3.4"
      }
    }
   }
}
```

Now the function itself.

```
using System;
using System.Text;
using NuGet;
using SendGrid;
using System.Net.Mail;
public static async Task Run(TimerInfo myTimer, TraceWriter log)
{
    log.Info($"C# Timer trigger function executed at: {DateTime.Now}");    
    var home = Environment.GetEnvironmentVariable("HOME");
    var filePath  = Path.Combine(home, @"data\Functions\lastexecution.txt");
    var lastScanDate = await ReadLastExecutionDate(filePath, log).ConfigureAwait(false);
    var package = GetNugetPackagePublishedAfterLastScan(lastScanDate, log);
	if(package == null)
	    return;
    await SendEmail(package, log).ConfigureAwait(false);    
    await SaveLastExecutionDate(filePath).ConfigureAwait(false);
}
static async Task<DateTime> ReadLastExecutionDate(string filePath, TraceWriter log)
{
    using (var reader = File.OpenText(filePath))
    {
        var fileText = await reader.ReadToEndAsync();
        log.Verbose(fileText);
        return DateTime.Parse(fileText);
    }
}
static Task SaveLastExecutionDate(string filePath)
{
    using (FileStream sourceStream = new FileStream(filePath, FileMode.Truncate, FileAccess.Write, FileShare.ReadWrite, 
            bufferSize: 1024, useAsync: true))
    {
        var d = Encoding.Default.GetBytes(DateTime.UtcNow.ToString());
        return sourceStream.WriteAsync(d, 0, d.Length);
    };
}
static IPackage GetNugetPackagePublishedAfterLastScan(DateTime lastScan, TraceWriter log)
{
    var repo = PackageRepositoryFactory.Default.CreateRepository("https://packages.nuget.org/api/v2");
	List<IPackage> packages = repo.FindPackagesById("WindowsAzure.ServiceBus").ToList();
	var package = packages.Where(x => x.IsReleaseVersion() == true)
		.OrderByDescending(x => x.Version)
		.Where(x => x.Published > lastScan)
		.FirstOrDefault();
	if(package == null)
	{
	    log.Info("No updates."); 
	}
	else
	{
	    log.Verbose(($"{package?.Version}  {package?.Published?.ToUniversalTime()}"));
	}
	return package;
}	
static Task SendEmail(IPackage package, TraceWriter log)
{
    var apiKey = "[key]";
	var transportWeb = new Web(apiKey);
	SendGridMessage myMessage = new SendGridMessage();
	myMessage.AddTo("[email]");
	myMessage.From = new MailAddress("feldman.sean@gmail.com", "Sean Feldman");
	myMessage.Subject = $"WindowsAzure.ServiceBus {package.Version} was released";
	myMessage.Text = $"Release date: {package.Published}\n\n{package.ReleaseNotes}";
	return transportWeb.DeliverAsync(myMessage);
}
```

Function is based on a time trigger, therefore schedule is set either on time span or a cron expression. 

That's it. Zero deployment, a notification service will be executed every 24 hours, sending email if a new version of a package is released.

While this is an overs-simplified example, its purpose is to highlight what Azure Functions can help with and what they are good at. Trying to apply those at more complex problems will lead to more headaches then benefits. Keep functions for small, well defined, and self-contained pieces of logic that nothing else depends on.
