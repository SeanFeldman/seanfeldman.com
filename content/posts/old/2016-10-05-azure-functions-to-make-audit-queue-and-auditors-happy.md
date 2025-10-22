---
title: Azure Functions to make audit queue and auditors happy
slug: azure-functions-to-make-audit-queue-and-auditors-happy
date: '2016-10-05T06:40:00'
updated: '2018-07-09T22:27:58.843414+00:00'
draft: false
tags:
- Azure
- Functions
author: Sean Feldman
---
Using NServiceBus on Azure allows the best of two worlds – robust and reliable messaging framework on top of excellent Azure services. Azure services and any other cloud provider as well have strict capacity and quotas. For Azure transports NServiceBus is using, those are usually allowed maximum throughput, the total number of messages, the number of concurrent connections, etc. With Azure Storage Queues there’s an additional constraint that while is not significant on its own, does have a weight in a system: [maximum message TTL is seven days only]( https://azure.microsoft.com/en-us/documentation/articles/service-bus-azure-and-service-bus-queues-compared-contrasted/#capacity-and-quotas). Yes, yes, you’ve heard right. 7 days only. Almost as if someone at the storage team took the saying “a happy queue is an empty queue” and implemented maximum message TTL using that as a requirement. While it’s ok to have such a short message TTL for a message that is intended to be processed, for messages that are processed and need to be stored that could be an issue.

NServiceBus has [feature to audit]( https://docs.particular.net/nservicebus/operations/auditing) any successfully processed messages. For some projects audits are a must and having these audits is out of the question. The challenge is to have these audits kept in the audit queue created by NServiceBus. After seven days those messages are purged by the Azure Storage service. Ironically, this is the same service that can keep up to 500TB of blobs for as long as you need them, supporting various [redundancy levels]( https://azure.microsoft.com/en-us/documentation/articles/storage-redundancy/#zone-redundant-storage) such as LRS, ZRS, and GRS. With LRS and ZRS there are three copies of the data. With GRS there are six copies of the data and data is replicated across multiple data centers. Heaven for audits.

If you’re not using Particular Platform, or [Service Pulse](http://particular.net/servicepulse) specifically, you will have to build some mechanism to move your audit messages into a storage of some kind and keep it for whatever the retention period that is required. Building such an ETL service is not difficult, but it is an investment that requires investment, deployment, and maintenance. Ideally, it should be automated and scheduled. I’ll let your imagination complete the rest. Though for a cloud-based solution “when in Rome, do as the Romans do”. 

One of the silently revolutionizing services in the Azure ecosystem is [Azure Functions]( https://azure.microsoft.com/en-us/services/functions/). While it sounds very simple and not as exciting as micro-services with Service Fabric or Containerization with Docker, it has managed to coin a buzz word of its own (serverless computing) and demonstrated that usages could be quite various. To a certain extent could be labeled as “nano-service”. But enough with this, back to audits.

Azure Functions  support various [triggers and binding]( https://azure.microsoft.com/en-us/documentation/articles/functions-triggers-bindings/). Among those, you’ll find Storage Queues and Storage Blobs. If combined, they could help to build the following simple ETL:

![enter image description here][1]

Azure Functions supports two types of bindings: declarative and imperative. Let’s focus on the declarative one first.

A declarative binding allows to specify a binding to a queue or an HTTP request and convert that into an object that a Function can consume. Using such a binding with an Azure Storage queue allows declaratively bind an incoming message to a variable in the list of function parameters rather than working with a raw CloudQueueMessage. It also allows getting some of the standard CloudQueueMessage attributes such as Id, DequeueCount, etc. Configuring a trigger using Azure Functions UI is incredibly easy.

 1. Create a new function that is triggered by a Storage queue 
 2. Specify
```
function parameter name that will be used in code (myQueueItem)
```
 3. Specify storage account to be used (settings key that represents
```
storage account connection string)
```
 4. Specify queue to be monitored for
```
messages
```

![enter image description here][2]

Once function created, you’ll have be able to replace its signature with an asynchronous version that will look like the following:

```
public static async Task Run(string myQueueItem, TraceWriter log)
```

That’s it for the input. This will allow the function to receive notifications about new messages found on a queue and receive the content as a string parameter. Additionally, we could add declarative bindings for the standard properties. For this sample, I’ll add Id of the ASQ message.

```
public static async Task Run(string myQueueItem, string id, TraceWriter log)
```

The objective is to turn the message into a blob file. This will require persisting the content to the storage account. A simple solution would be to specify the output declaratively by selecting an Azure Storage Blob as an output type and using a path with a unique {rand-guid} template (random GUID).

![enter image description here][3]

Using this approach, we’ll have all messages stored in the “audits” container with a random GUID as a file name. To have a bit friendlier audits, I’d like to perform the following:

 - Partition audit messages based on the date (year-month-day)
 - Partition audits based on the endpoint that processed the messages using NServiceBus audit information from within the message itself
 - Store each audit message as JSON file with where filename is the original ASQ transport message ID
Let’s see the code and analyze it step by step.


`#r "Newtonsoft.Json"`

```
using System;
using System.Text;
using System.IO;
using Newtonsoft.Json;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Host.Bindings.Runtime;
static readonly string byteOrderMarkUtf8 = Encoding.UTF8.GetString(Encoding.UTF8.GetPreamble());
public static async Task Run(string myQueueItem, string id, Binder binder, TraceWriter log)
{
    log.Info($"C# Queue trigger function triggered");
    log.Info($"Original ASQ message ID: {id}");
    var value =myQueueItem.StartsWith(byteOrderMarkUtf8) ? (myQueueItem).Remove(0, byteOrderMarkUtf8.Length) : myQueueItem; 
    var obj = JsonConvert.DeserializeObject<MessageWrapper>(value);
    var endpointName = obj.Headers["NServiceBus.ProcessingEndpoint"];
    var attributes = new Attribute[]
    {
        new BlobAttribute($"audits/{DateTime.UtcNow.ToString("yyyy-MM-dd")}/{endpointName}/{id}.json"),
        new StorageAccountAttribute("asqetl_STORAGE")
    };
    using (var writer = await binder.BindAsync<TextWriter>(attributes).ConfigureAwait(false))
    {
        writer.Write(myQueueItem);
    }
    log.Info($"Done ");
}
public class MessageWrapper
{
    public string IdForCorrelation { get; set; }
    public string Id { get; set; }
    public int MessageIntent { get; set; }
    public string ReplyToAddress { get; set; }
    public string TimeToBeReceived { get; set; }
    public Dictionary<string, string> Headers { get; set; }
    public string Body { get; set; }
    public string CorrelationId { get; set; }
    public bool Recoverable { get; set; }
}
```

1.	I’ve modified the signature to inject a Binder into the method. Binder allows imperative bindings to be performed at run-time. In this case, specifying the output blob.
2.	NServiceBus ASQ transport is encoding messages with a BOM (Byte Order Mark). Declared byteOrderMarkUtf8 variable is used to strip it out to persist message as raw JSON.
3.	MessageWrapper class represents the message wrapper used by NServiceBus ASQ transport. Since native Storage Queues messages do not have headers, MessageWrapper is used to contain both headers and the payload. ["NServiceBus.ProcessingEndpoint" header]( https://docs.particular.net/nservicebus/messaging/headers#send-headers) will provide the information at what endpoint a given message was successfully processed.
4.	Once we have all the prerequisites, the “black magic” can start. This is where Binder is used to providing the underlying WebJobs SDK information where the blob should be created. To provide these hints, we need to instantiate two attributes: BlobAttribute and StorageAccountAttribute and supply those to the Binder.BindAsync method. The first attribute, BlobAttribute, is specifying the path of the blob to use. The second attribute, StorageAccountAttribute, is determining the settings key to be used to retrieve storage connection string. Note that w/o StorageAccountAttribute account the default (AzureWebJobsStorage) setting key is used. That’s the storage account used to create the function in the portal.
5.	Passing the attributes to the BindAsync method to get a writer and writing the message content into the blob is finishing is the final step. After that content of the queue message will be stored as a blob with the desired name at the path represented by “audits/year-month-day/endpoint/original-asq-message-id.json”.

To validate the function is working, one of the NServiceBus [ASQ transport samples]( https://docs.particular.net/samples/azure/storage-queues/?version=ASQ_7) can be used.  Configure the sample to use the same storage account and execute it. Endpoint1 and Endpoint2 will process messages, but not emit any audits. To enable audits, the following configuration modification is required in Program.cs for each endpoint:

```
endpointConfiguration.AuditProcessedMessagesTo("audit");
```

Once auditing is enabled, blob storage will start feeling up with any new audit messages emitted by the endpoints.

![enter image description here][4]

The function will be running from now on and convert audit messages into blobs. Endpoints can be added or removed; the function will adopt itself and emit files in the appropriate location. In a few lines of code, we made both, the audit queue and the auditors happy.

**Update**: quitely, Storage team has enabled [unlimitted TTL](https://docs.microsoft.com/en-us/rest/api/storageservices/put-message#uri-parameters)

[1]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2016/azure-functions-etl/clipboard.png
[2]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2016/azure-functions-etl/clipboard-1.png
[3]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2016/azure-functions-etl/clipboard-2.png
[4]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2016/azure-functions-etl/clipboard-3.png
