---
title: CosmosDB - container provisioning throttling
slug: cosmosdb-container-provisioning-throttling
date: '2020-09-09T05:47:00'
updated: '2020-09-09T16:35:25.023069+00:00'
draft: false
tags:
- CosmosDB
author: Sean Feldman
---
![throttling][1]
When working with CosmosDB, you're quickly accustomed to the idea that each operation costs a certain amount of RUs. And when there's not enough RUs, the request gets throttled. There's a [capacity calculator][2] that helps to find out the estimated required throughput based on the operations and other criteria to avoid throttling. But this calculator is omitting important information that does not appear to be documented at the moment. Creating collections can be throttled as well, except not due to an insufficient amount of RUs. To demonstrate how collection creation requests can be throttled, I'll emulate concurrent requests coming to the broker to create temporary collection.
```
var builder = new CosmosClientBuilder("<connection-string>");
using var client = builder.Build();
```
var database = client.GetDatabase("cosmos-db");
var tasks = new List();
for (var i = 0; i < 40; i++)
{
$"Create container temp-{i}".Dump();
var containerProperties = new ContainerProperties($"temp-{i}", partitionKeyPath: "/PartitionKey");
tasks.Add(database.CreateContainerIfNotExistsAsync(containerProperties));
}
await Task.WhenAll(tasks);
for (var i = 0; i < 40; i++)
{
var containerProperties = new ContainerProperties($"temp-{i}", partitionKeyPath: "/PartitionKey");
try
{
var container = database.GetContainer($"temp-{i}");
await container.DeleteContainerAsync();
}
catch (CosmosException)
{
continue;
}
}
While my database has plenty of RUs, this code is still getting throttled.
```
CosmosException: Response status code does not indicate success: TooManyRequests (429); Substatus: 3200; ActivityId: e5797480-8cda-4123-b721-5731560c7669; Reason: ({
  "code": "429",
  "message": "Message: {\"Errors\":[\"Request rate is large. More Request Units may be needed, so no changes were made. Please retry this request later. Learn more: http://aka.ms/cosmosdb-error-429\"]}\r\nActivityId: e5797480-8cda-4123-b721-5731560c7669, Request URI: /apps/ba11a36b-ba48-43cf-bfd9-7b2c8cf533da/services/a3491e68-7504-441b-a03f-d6a4acfe8b5e/partitions/d0e40c30-0561-42b5-badc-86a05e4aebf2/replicas/132440638817019063p, RequestStats: , SDK: Microsoft.Azure.Documents.Common/2.11.0"
});
```
Requests to create containers are throttled and status code 429 is returned. What's really confusing is that the error message makes a reference to the potentially insufficient RUs.
The real reason for the throttling has to do with the number of containers created concurrently per unit of time and not RUs provisioned for the database. And that number is 5 containers per minute as it stands today. Keep that in mind.
[1]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2020/cosmosdb%20-%20collections%20rate%20limitting/speed.limit.jpg
[2]: https://cosmos.azure.com/capacitycalculator/
