---
title: dynamic in the Wild
slug: dynamic-in-the-wild
date: '2010-10-29T03:49:00'
updated: '2010-10-29T03:49:00'
draft: false
author: Sean Feldman
---


Today [Jonathan](http://agilewarrior.wordpress.com/) and myself worked on a RESTful service that is responsible to create a new invoice. The design decision was to return HTTP status code 409 (Conflict) in case client tries to add more than once the same invoice. The code looked like this:

```
public Invoice AddNewInvoice(Invoice newInvoice)  
        {  
            var existingInvoice = invoices.Find(x => x.Id == newInvoice.Id);  
            var ctx = WebOperationContext.Current;  
            ctx.OutgoingResponse.Headers["Cache-Control"] = "no-cache";  
  
            if (existingInvoice != null)  
            {  
                ctx.OutgoingResponse.StatusCode = HttpStatusCode.Conflict;  
                return null;  
            }  
  
            invoices.Add(newInvoice);  
  
            ctx.OutgoingResponse.StatusCode = HttpStatusCode.Created;  
            ctx.OutgoingResponse.Location = PluginFactory.INSTANCE.InvoiceServiceUri() + "/" + newInvoice.Id;  
  
            return new Invoice(newInvoice.Id, newInvoice.Receiver);  
        }
```

Everything was fine, except that in our client (Silverlight 4.0) application it was impossible to get the HTTP status code you’d normally get on a normal .NET stack. By the looks of it, definitely something Microsoft team should look into.

But no worries, we decided to look into WebException to see if it really that clueless or it actually has what we need and hides it. After all, Response is a WebResponse object.![image](http://weblogs.asp.net/blogs/sfeldman/image_thumb_70881E9A.png "image")

Unfortunately, no luck there. The implementation was exactly what Intellisense showed us.

```
  public abstract class WebResponse : IDisposable  
  {  
    public abstract long ContentLength { get; }  
    public abstract string ContentType { get; }  
    public abstract Uri ResponseUri { get; }  
    public virtual WebHeaderCollection Headers { get; }  
    public virtual bool SupportsHeaders { get; }  
    void IDisposable.Dispose();  
    public abstract Stream GetResponseStream();  
    public abstract void Close();  
  }
```

Then we tried the last resort – review object in debugger. And there we could find an interesting thing. [Silverlight has two HTTP stack implementations](http://msdn.microsoft.com/en-us/library/dd920295%28v=VS.95%29.aspx), Browser and Client. We used the Client one. The type of e.Response was *[System.Net.Browser.ClientHttpWebResponse](http://msdn.microsoft.com/en-us/library/system.net.httpwebresponse%28v=VS.95%29.aspx)* as a result of that. Now *ClientHttpWebResponse* had everything we needed. The only problem was that casting was impossible due to Microsoft decision to make *ClientHttpWebResponse* internal.

[![image](http://weblogs.asp.net/blogs/sfeldman/image_thumb_3156F2A1.png "image")](http://weblogs.asp.net/blogs/sfeldman/image_440BEC58.png)

Normally, we’d go with reflection to access the StatusCode property. But reflection is ugly and painful. This is where *dynamic* becomes really handy. Definition of *dynamic* says:

> Type dynamic behaves like type object in most circumstances. However, operations that contain expressions of type dynamic are not resolved or type checked by the compiler. The compiler packages together information about the operation, and that information is later used to evaluate the operation at run time. As part of the process, variables of type dynamic are compiled into variables of type object. Therefore, type dynamic exists only at compile time, not at run time.

Final result that works:

```
	catch (WebException e)  
                {  
                  dynamic exceptionResponse = e.Response;  
                    if (exceptionResponse.StatusCode == HttpStatusCode.Conflict)  
                        //...  
                    else  
                        //...  
                }
```

Update: JR has actually posted the code were this technique is applied. [Check it out](http://agilewarrior.wordpress.com/2010/10/30/restful-wcf-service-with-silverlight4/).


