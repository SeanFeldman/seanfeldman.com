---
title: Creating BizTalk Message in Custom .NET Component
slug: creating-biztalk-message-in-custom-net-component
date: '2010-09-30T04:26:00'
updated: '2010-09-30T04:26:00'
draft: false
tags:
- BizTalk
- C#
- WCF
author: Sean Feldman
---


In my previous blog about [consuming WCF service from BizTalk orchestration](http://weblogs.asp.net/sfeldman/archive/2010/09/21/consuming-wcf-service-from-biztalk.aspx) I wrote about how we’d invoke a service based on a document coming in and mapping it into the service request schema.

This time I had the input for the service coming from a context, and not necessarily from the document itself, and needed to be able to perform same service invocation, yet constructing request document dynamically with-in the orchestration. To simplify the process, I still pass in a document, and distinguish a field with the value I want to pass into the service. This way I don’t actually have to waste time on property promotion. The key here is to invoke a custom .NET component (GAC-ed singleton) to construct the message with the value(s) coming from the original message context.

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_269BB732.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_1CB6C5C7.png)

Where the code is quite simple – invoke singleton with the required value(s):

```
System.Diagnostics.Trace.WriteLine("Invoking factory.");
toServiceMsg = MessageFactory.RequestMessageFactory.CreateProcessMessage(originalMsg.Value);
System.Diagnostics.Trace.WriteLine("Done invoking factory.");
```

The interesting part is the *CreateProcessMessage* method itself. The message I am generating is of schema *Process* (service incoming schema, *ProcessResponse* is outgoing schema). I couldn’t use XLANGMessage since it’s an abstract class. Therefore needed something to allow BizTalk message construction. This is where I ran into this [great blog post](http://blogs.msdn.com/b/appfabriccat/archive/2010/06/23/4-different-ways-to-process-an-xlangmessage-within-an-helper-component-invoked-by-an-orchestration.aspx) describing some of the options. I tried to look up more info, but honestly, this part of BizTalk is so badly documented IMO, that couldn’t get a lot. Not to mention that there’s no intellisense on these things… Anyways, this is what the method does:

```
namespace MessageFactory
{
	public static class RequestMessageFactory
	{
		private const string Namespace = "http://tempuri.org/";

		public static XLANGMessage CreateProcessMessage(int value)
		{
			var message = new GeneralMessage("Process");
			var memoryStream = new MemoryStream();
			using (var writer = XmlWriter.Create(memoryStream))
			{
				writer.WriteStartDocument();
				writer.WriteStartElement("Process", Namespace);
				writer.WriteStartElement("value", Namespace);
				writer.WriteString(value.ToString());
				writer.WriteEndElement();
				writer.WriteEndElement();
			}
			memoryStream.Seek(0, SeekOrigin.Begin);

			message[0].LoadFrom(memoryStream);
			return message.GetMessageWrapperForUserCode();
		}
	}

	[Serializable]
	public sealed class GeneralMessage : BTXMessage
	{
		public GeneralMessage(string messageName) 
			: this (messageName, Service.RootService.XlangStore.OwningContext)
		{}

		private GeneralMessage(string messageName, Context owningContext) 
			: base(messageName, owningContext)
		{
			owningContext.RefMessage(this);
			AddAnyPart("Body");
		}
	}

}
```

A lot of magic IMO. I wish Microsoft would provide a bit more on the subject, such as what *Service.RootService.XlangStore.OwningContex* is and why we need to *Ref*-a-*Message* (guessing is not knowing!).

Another “smell” is that now the factory (custom .NET component) had to be aware of the contract without being connected to the schema file itself or any visible link. So whenever the contract is changing, factory has to reflect that change. The only way I can capture that is a test that would generate the message and try to validate it against the schema.

Any thoughts on the subject? Don’t be shy.


