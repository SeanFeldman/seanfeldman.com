---
title: Fixing NServiceBus default databus serializer in .NET 6
slug: fixing-nservicebus-default-databus-serializer-in-net-6
date: '2022-05-06T17:31:00'
updated: '2022-05-20T16:09:03.921603+00:00'
draft: false
tags:
- C#
- NServiceBus
author: Sean Feldman
---
Upgrading to .NET 6, updating all the packages, boosters turned on, launching testing.
Houston, we've got a problem.
> System.NotSupportedException: BinaryFormatter serialization and
> deserialization are disabled within this application. See
> https://aka.ms/binaryformatter for more information.
Ouch! What just happened? There were no warnings, no obsolete messages, nothing on to the autopsy.
NServiceBus has a [data bus](https://docs.particular.net/nservicebus/messaging/databus/) (or a 'databus') feature. The feature implements the [Claim Check pattern](https://docs.microsoft.com/en-us/azure/architecture/patterns/claim-check) to allow messages to surpass the imposed maximum message size by the underlying messaging technology. The feature serializes the data internally, and the default `DefaultDataBusSerializer` uses `BinaryFormatter`. Nothing new; it has been [used for years](https://github.com/Particular/NServiceBus/blame/a510c214806540d920de10ed81b50f191129fbed/src/databus/NServiceBus.Databus/DefaultDatabusSerializer.cs#L6). Unfortunately, with .NET 5, `BinaryFormatter` was deprecated due to a [security risk](https://docs.microsoft.com/en-ca/dotnet/standard/serialization/binaryformatter-security-guide) it poses. And while you could skip .NET 5 and live with .NET Core 3.1, .NET 6 is breathing down the neck, and an upgrade is imminent.
There is only one option:
1. [Re-enable the binary formatter](https://docs.microsoft.com/en-us/dotnet/core/compatibility/core-libraries/5.0/binaryformatter-serialization-obsolete) 🦨
1. Work around the problem until Particular has an official solution
You read it right. Until an official fix, #2 is the only option that will be compliant with most environments.
The workaround can be summarized as the following:
- Pick serialization
- Replace the default data bus serializer with the custom version
- Deploy
## Picking serialization
I've chosen to go with BSON. The naive implementation is the following:
```
public class BsonDataBusSerializer : IDataBusSerializer
{
    public void Serialize(object databusProperty, Stream stream)
    {
        using var writer = CreateNonClosingStreamWriter(stream);
        using var bsonBinaryWriter = new BsonBinaryWriter(stream);
        BsonSerializer.Serialize(bsonBinaryWriter, databusProperty);
    }
    StreamWriter CreateNonClosingStreamWriter(Stream stream)
        => new(stream, Encoding.UTF8, bufferSize: 1024, leaveOpen: true);
    public object Deserialize(Stream stream)
    {
        using var bsonBinaryReader = new BsonBinaryReader(stream);
        return BsonSerializer.Deserialize<object>(bsonBinaryReader);
    }
}
```
## Replacing the default data bus serializer
\*\*Update\*\*: there's a cleaner option. Skip to the I Need a Better Option section below.
One of the things I wanted to avoid is sprinkling the code-base with the replacement code in various projects that use NServiceBus. So rather than going to the multiple places and having to register the workaround in the following way:
```
// TODO: required workaround for issue (link). Remove when fixed.
endpoint.AdvancedConfiguration.RegisterComponents(c => 
    c.RegisterSingleton<IDataBusSerializer>(new BsonDataBusSerializer()));
```
A perfect candidate would be using an auto-registered [features](https://docs.particular.net/nservicebus/pipeline/features) feature. A feature could be a part of the Shared solution that all endpoints are using and would automatically replace the data bus serializer w/o any endpoints having to do anything in the configuration code.
```
internal class BsonDataBusSerializerFeature : Feature
{
    public BsonDataBusSerializerFeature()
    {
        DependsOn<NServiceBus.Features.DataBus>();
        EnableByDefault();
    }
    protected override void Setup(FeatureConfigurationContext context)
    {
        if (context.Container.HasComponent<IDataBusSerializer>())
        {
           // ???. Remove(defaultDataBusSerializer);
        }
        context.Container.ConfigureComponent<IDataBusSerializer>(_ => 
              new BsonDataBusSerializer(), DependencyLifecycle.SingleInstance);
    }
}
```
Except there's no way to achieve that with NServiceBus \_today\_. The `IServiceCollection` is adapted into NServiceBus `ServiceCollectionAdapter`, which doesn't provide a way to remove any previously registered services as one can do with a plain `IServiceCollection`. More details [here](https://github.com/Particular/NServiceBus/issues/6374#issuecomment-1119799315).
## Workaround for the workaround
This part might be a bit smelly, but it's the necessary evil. NServiceBus adapts `IServiceCollection` and keeps a reference as a private member field. With some reflection, we can get hold of the service collection and purge the default `IDataBusSerializer` implementation to ensure it's not registered and [resolved first](https://github.com/Particular/NServiceBus/issues/6374#issuecomment-1114447110).
```
protected override void Setup(FeatureConfigurationContext context)
{
	if (context.Container.HasComponent<IDataBusSerializer>())
	{
		var serviceCollection = context.Container.GetFieldValue<IServiceCollection>("serviceCollection");
		if (serviceCollection is not null)
		{
			var defaultDataBusSerializer = serviceCollection.FirstOrDefault(descriptor =>
                       descriptor.ServiceType == typeof(IDataBusSerializer));
			if (defaultDataBusSerializer is not null)
			{
				serviceCollection.Remove(defaultDataBusSerializer);
			}
		}
	}
	context.Container.ConfigureComponent<IDataBusSerializer>(_ => 
             new BsonDataBusSerializer(), DependencyLifecycle.SingleInstance);
}
```
With a slight modification to the `Setup` method, the feature is now ready to be used!
## I Need a Better Option
And as was [pointed out](https://github.com/Particular/NServiceBus/issues/6374#issuecomment-1129634358) by Particular, there's an option to register a custom data bus serializer earlier than Core does it, removing the need in reflection. The feature could be replaced by an [`INeedInitialization` component](https://docs.particular.net/nservicebus/lifecycle/ineedinitialization), which is invoked \_before\_ endpoint creation and initialization.
```
public class ReplaceDefaultDataBusSerializer : INeedInitialization
{
  public void Customize(EndpointConfiguration endpointConfiguration)
  {
    endpointConfiguration.RegisterComponents(components =>
      components.RegisterSingleton<IDataBusSerializer>(new BsonDataBusSerializer()));
  }
}
```
## Deploying
A word of caution for the solutions using one of these features in combination with data bus:
- Events
- Delayed messages
You will need to tread carefully. The migration is not a simple data bus serializer replacement in these scenarios. It has to cater to the fact that messages serialized with `BinaryFormatter` could be processed by the endpoints converted to use the new serialization. Subscribing to the [issue](https://github.com/Particular/NServiceBus/issues/6058) on this topic is probably a safe bet. Or at least toss a few ideas before you start. And no matter what, good luck!
