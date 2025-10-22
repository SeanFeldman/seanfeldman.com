---
title: Consuming WCF Service from BizTalk
slug: consuming-wcf-service-from-biztalk
date: '2010-09-22T03:25:00'
updated: '2010-09-22T03:25:00'
draft: false
tags:
- BizTalk
author: Sean Feldman
---


Sometimes trivial things in .NET are not so trivial in the BizTalk world. Especially for standard .NET developers with the mindset for routine .NET development. Recently, I was asked to give a hand with a simple task that was surprisingly taking too long (and good that was asked for, why to waste time if you can leverage someone to give a hand – always something I resort to). On the web, there are plenty of resources, yet nothing emphasizes the little things that are obvious to somewhat experienced BizTalk-ers and is brand new to mature .NET developers. Lets dive into example.

Lets say we have a business process that requires to involve a WCF service during a message processing, taking a piece of data from the message as a parameter for the service, and working with the returned value.

[![image](http://weblogs.asp.net/blogs/sfeldman/image_thumb_04B10394.png "image")](http://weblogs.asp.net/blogs/sfeldman/image_00A42511.png)

In a standard .NET project we’d define the contract (*ISomeService*)and implement the service (*SomeService*), testing that it adheres to the desired behavior.

```
[ServiceContract]  
public interface ISomeService  
{  
	[OperationContract]  
	string Process(int value);  
}  
  
public class SomeService : ISomeService  
{  
	public string Process(int value)  
	{  
		return string.Format("Processed: {0}", value);  
	}  
}
```

Now the interesting part. To reference a service from a BizTalk project, the simplest way is to point to the service instance running somewhere. This is similar to generating a service reference for a regular .NET project, except that service configuration is stored not in (.NET traditional) configuration file, but in a binding file, typical to BizTalk. The key is to “just generate” this binding, and tweak it later for desired purposes.

The easiest way to get the service running, is to create a simple self-hosting console application (no need in IIS or windows service).

```
static void Main(string[] args)  
{  
	using (var serviceHost = new ServiceHost(typeof(SomeService)))  
	{  
		serviceHost.Open();  
				  
		Console.WriteLine("Running service (press ESC to finish).");  
  
		while(true)  
		{  
			if (!Console.KeyAvailable)   
				continue;  
					  
			var pressedKey = Console.ReadKey(true);  
			if (pressedKey.Key == ConsoleKey.Escape)  
				break;  
		}  
  
		serviceHost.Close();  
		Console.WriteLine("Service finished.");  
	}  
}
```

Again, how service is exposed in self-hosted console runner is not important, the generated binding file (once service is referenced from BizTalk application) can be changes as desired. For simplicity, I hosted it with basic HTTP binding and enabled MEX.

```
<?xml version="1.0" encoding="utf-8" ?>  
<configuration>  
  <system.web>  
    <compilation debug="true" />  
  </system.web>  
  <system.serviceModel>  
    <services>  
      <service name="SomeService.SomeService" behaviorConfiguration="SomeService.SomeServiceBehavior">  
        <host>  
          <baseAddresses>  
            <add baseAddress = "http://localhost/SomeService" />  
          </baseAddresses>  
        </host>  
        <endpoint address ="" binding="basicHttpBinding" contract="SomeService.ISomeService">  
          <identity>  
            <dns value="localhost"/>  
          </identity>  
        </endpoint>  
        <endpoint address="mex" binding="mexHttpBinding" contract="IMetadataExchange"/>  
      </service>  
    </services>  
    <behaviors>  
      <serviceBehaviors>  
        <behavior name="SomeService.SomeServiceBehavior">  
          <serviceMetadata httpGetEnabled="True"/>  
          <serviceDebug includeExceptionDetailInFaults="True" />  
        </behavior>  
      </serviceBehaviors>  
    </behaviors>  
  </system.serviceModel>  
</configuration>
```

From BizTalk project, added Generated Item –> Consume WCF Service, used self-hosted service URL ([*http://localhost/SomeService*](http://localhost/SomeService)). Just before hitting the Next button, don’t forget to run the self-hosted service runner.

Once service is referenced, there are a few items that are auto-generated. The important ones are:

* SomeService\_tempuri\_org.xsd
* SomeService\_BindingInfo.xml

The schema file contains all the schemas for arguments and return type schemas for all the service operations exposed by service. Since *SomeService* exposes a single operation with arguments coming in and return values, these are the generated schemas:

[![image](http://weblogs.asp.net/blogs/sfeldman/image_thumb_5D794B0F.png "image")](http://weblogs.asp.net/blogs/sfeldman/image_5B3CC253.png) Since the name of the operation is *Process*, arguments and return schemas use the name. Returned type is *string*, yet in order to work with the value in orchestration, I recommend to make it a distinguished field.

Next step is to define a map, that would take the message we process and map into the message of a type that *Process* operation accepts (can be constructed from a scratch, but mapping is easier, cleaner, and easily testable).

[![image](http://weblogs.asp.net/blogs/sfeldman/image_thumb_6F586F8D.png "image")](http://weblogs.asp.net/blogs/sfeldman/image_4AC45158.png)

Once in place, we can finalize the orchestration

[![image](http://weblogs.asp.net/blogs/sfeldman/image_thumb_1550B095.png "image")](http://weblogs.asp.net/blogs/sfeldman/image_3811E852.png)

Trace just to ensure that the service is executed as expected.

```
System.Diagnostics.Trace.WriteLine(System.DateTime.Now.ToString());      
System.Diagnostics.Trace.WriteLine(msgFromService.parameters.ProcessResult);    
```

Deploying and executing this process results in the next output for the given input of 123:

```
<ns0:Message xmlns:ns0="http://InvokerApp">  
  <Value>123</Value>  
</ns0:Message>
```

[![image](http://weblogs.asp.net/blogs/sfeldman/image_thumb_2FB3345D.png "image")](http://weblogs.asp.net/blogs/sfeldman/image_32C59252.png)

The console runner has to be there for the time of BizTalk application execution since the binding file (that is supposed to be deployed into BizTalk along with the BT Application) contains information about that service configuration. Quick review of the binding information shows that it’s just a service configuration, and should be re-written to meet the real service configuration.

```
<?xml version="1.0" encoding="utf-8"?>  
<BindingInfo xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" Assembly="Microsoft.BizTalk.Adapter.Wcf.Consuming, Version=3.0.1.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35" Version="3.5.1.0">  
  <Timestamp>2010-09-20T09:53:57.2895-06:00</Timestamp>  
  <SendPortCollection>  
    <SendPort Name="WcfSendPort_SomeService_BasicHttpBinding_ISomeService" IsStatic="true" IsTwoWay="true" BindingOption="0">  
      <Description>service "SomeService" port "BasicHttpBinding_ISomeService"</Description>  
      <TransmitPipeline Name="Microsoft.BizTalk.DefaultPipelines.PassThruTransmit" FullyQualifiedName="Microsoft.BizTalk.DefaultPipelines.PassThruTransmit, Microsoft.BizTalk.DefaultPipelines, Version=3.0.1.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35" Type="2" />  
      <PrimaryTransport>  
        <Address>http://localhost/SomeService</Address>  
        <TransportType Name="WCF-BasicHttp" Capabilities="899" ConfigurationClsid="467c1a52-373f-4f09-9008-27af6b985f14" />  
        <TransportTypeData>&lt;CustomProps&gt;  
  &lt;MaxReceivedMessageSize vt="3"&gt;65536&lt;/MaxReceivedMessageSize&gt;  
  &lt;MessageEncoding vt="8"&gt;Text&lt;/MessageEncoding&gt;  
  &lt;TextEncoding vt="8"&gt;utf-8&lt;/TextEncoding&gt;  
  &lt;SecurityMode vt="8"&gt;None&lt;/SecurityMode&gt;  
  &lt;MessageClientCredentialType vt="8"&gt;UserName&lt;/MessageClientCredentialType&gt;  
  &lt;AlgorithmSuite vt="8"&gt;Basic256&lt;/AlgorithmSuite&gt;  
  &lt;TransportClientCredentialType vt="8"&gt;None&lt;/TransportClientCredentialType&gt;  
  &lt;UseSSO vt="11"&gt;0&lt;/UseSSO&gt;  
  &lt;ProxyToUse vt="8"&gt;Default&lt;/ProxyToUse&gt;  
  &lt;StaticAction vt="8"&gt;&amp;lt;BtsActionMapping xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"&amp;gt;  
  &amp;lt;Operation Name="Process" Action="http://tempuri.org/ISomeService/Process" /&amp;gt;  
&amp;lt;/BtsActionMapping&amp;gt;&lt;/StaticAction&gt;  
  &lt;InboundBodyLocation vt="8"&gt;UseBodyElement&lt;/InboundBodyLocation&gt;  
  &lt;InboundNodeEncoding vt="8"&gt;Xml&lt;/InboundNodeEncoding&gt;  
  &lt;OutboundBodyLocation vt="8"&gt;UseBodyElement&lt;/OutboundBodyLocation&gt;  
  &lt;OutboundXmlTemplate vt="8"&gt;&amp;lt;bts-msg-body xmlns="http://www.microsoft.com/schemas/bts2007" encoding="xml"/&amp;gt;&lt;/OutboundXmlTemplate&gt;  
  &lt;PropagateFaultMessage vt="11"&gt;-1&lt;/PropagateFaultMessage&gt;  
  &lt;OpenTimeout vt="8"&gt;00:01:00&lt;/OpenTimeout&gt;  
  &lt;SendTimeout vt="8"&gt;00:01:00&lt;/SendTimeout&gt;  
  &lt;CloseTimeout vt="8"&gt;00:01:00&lt;/CloseTimeout&gt;  
&lt;/CustomProps&gt;</TransportTypeData>  
        <RetryCount>3</RetryCount>  
        <RetryInterval>5</RetryInterval>  
        <ServiceWindowEnabled>false</ServiceWindowEnabled>  
        <FromTime>2000-01-01T00:00:00</FromTime>  
        <ToTime>2000-01-01T23:59:59</ToTime>  
        <Primary>true</Primary>  
        <OrderedDelivery>false</OrderedDelivery>  
        <DeliveryNotification>1</DeliveryNotification>  
        <SendHandler xsi:nil="true" />  
      </PrimaryTransport>  
      <ReceivePipeline Name="Microsoft.BizTalk.DefaultPipelines.XMLReceive" FullyQualifiedName="Microsoft.BizTalk.DefaultPipelines.XMLReceive, Microsoft.BizTalk.DefaultPipelines, Version=3.0.1.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35" Type="1" />  
      <ReceivePipelineData xsi:nil="true" />  
      <Tracking>0</Tracking>  
      <Filter />  
      <OrderedDelivery>false</OrderedDelivery>  
      <Priority>5</Priority>  
      <StopSendingOnFailure>false</StopSendingOnFailure>  
      <RouteFailedMessage>false</RouteFailedMessage>  
      <ApplicationName xsi:nil="true" />  
    </SendPort>  
  </SendPortCollection>  
</BindingInfo>
```

Behind the scenes, BizTalk generates a proxy that is getting deployed along with the BizTalk application. I wish ChannelFactory option would be available with BizTalk as well, so that the contract is enough to spin of a dynamic service proxy. On the flip side, having BizTalk to generate all the schemas is very handy.

[BizTalkInvokeWCF.zip](http://weblogs.asp.net/blogs/sfeldman/BizTalkInvokeWCF_6CD6EFE2.zip)  is attached.
