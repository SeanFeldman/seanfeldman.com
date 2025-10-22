---
title: State Pattern with FluentNHibernate
slug: state-pattern-with-fluentnhibernate
date: '2009-04-25T02:58:00'
updated: '2009-04-25T02:58:00'
draft: false
tags:
- DDD
- OO
- Patterns
author: Sean Feldman
---


FluentNHibernate is an amazingly nice DSL to use for quick NHibernate mapping implementation. Today I had to refactor some of the code we did at work, in order to persist a state of an object. The original code was implemented using State pattern, which allows simple division of responsibility and easy decision making at each given step. I have decided to create a simple example of State pattern persisted with FluentNHibernate in order to demonstrate how powerful it is and what kind of freedom it can give to developers.

The domain for the sample will be some sort of simple message processing system. Listed below are all [![image](http://weblogs.asp.net/blogs/sfeldman/image_thumb_58E41599.png "image")](http://weblogs.asp.net/blogs/sfeldman/image_4BEA3588.png)possible message statuses we can have in the system. A message starts its life in the system when it’s  received the first time, and then its’ status is set to “Received”. When message is processed, in case processing has ended successfully, it’s being send to the destinator and marked as Processed. In case processing was not successful, it’s state is updated to the “FailedProcessing”. When a successfully processed message is sent out, its’ status is set to “Sent”, which is the last status possible in the given system.

First we want to implement the Status using State pattern.

 
```
   1: public abstract class MessageStatus : Entity
```
```
   2: {
```
```
   3:   protected MessageStatus(string status)
```
```
   4:   {
```
```
   5:     Status = status;
```
```
   6:   }
```
```
   7:  
```
```
   8:   public string Status { get; protected set; }
```
```
   9:  
```
```
  10:   public virtual void Complete()
```
```
  11:   {
```
```
  12:     throw new InvalidOperationException(string.Format("Status '{0}' cannot have a complete state.", Status));
```
```
  13:   }
```
```
  14:  
```
```
  15:   public virtual void Fail()
```
```
  16:   {
```
```
  17:     throw new InvalidOperationException(string.Format("Status '{0}' cannot have a failed state.", Status));
```
```
  18:   }
```
```
  19: }
```

I want to be able to store message (current) status as an entity on its’ own. We will use this to query system for messages with a particular status. MessageStatus is an Entity, entity is a base class for all entities (included in source code) to handle ID handling and equality.

Next step is to define behavior for the statuses we have. Let’s do it through tests.

```
   1: [Concern(typeof (MessageStatus))]
```
```
   2: [TestFixture]
```
```
   3: public abstract class ReceivedStatus_Specs : ContextSpecification<MessageStatus>
```
```
   4: {
```
```
   5:   protected override MessageStatus create_system_under_test()
```
```
   6:   {
```
```
   7:     return new ReceivedStatus();
```
```
   8:   }
```
```
   9:  
```
```
  10:   protected override void establish_context()
```
```
  11:   {
```
```
  12:     system_under_test = create_system_under_test();
```
```
  13:   }
```
```
  14: }
```
```
  15:  
```
```
  16: public class When_ReceivedStatus_is_asked_to_complete : ReceivedStatus_Specs
```
```
  17: {
```
```
  18:   protected override void because()
```
```
  19:   {
```
```
  20:     system_under_test.Complete();
```
```
  21:   }
```
```
  22:  
```
```
  23:   [Observation]
```
```
  24:   public void Should_become_Processed_status()
```
```
  25:   {
```
```
  26:     system_under_test.Status.Should_Be_Equal_To(ProcessedStatus.StatusName);
```
```
  27:   }
```
```
  28: }
```
```
  29:  
```
```
  30: public class When_ReceivedStatus_is_asked_to_fail : ReceivedStatus_Specs
```
```
  31: {
```
```
  32:   protected override void because() {}
```
```
  33:  
```
```
  34:   [Observation]
```
```
  35:   [ExpectedException(typeof(InvalidOperationException))]
```
```
  36:   public void Should_throw_an_exception()
```
```
  37:   {
```
```
  38:     system_under_test.Fail();
```
```
  39:   }
```
```
  40: }
```

Complete state transition specification will fail. Fixing the test will complete the implementation.

```
   1: public class ReceivedStatus : MessageStatus
```
```
   2: {
```
```
   3:   public const string StatusName = "Received";
```
```
   4:  
```
```
   5:   public ReceivedStatus() : base(StatusName) {}
```
```
   6:  
```
```
   7:   public override void Complete()
```
```
   8:   {
```
```
   9:     Status = ProcessedStatus.StatusName;
```
```
  10:   }
```
```
  11: }
```

The rest of the statuses are very much similar.

* “Processed” status overrides both Complete() and Fail()
* “Finished” and “FailedProcessing” statuses do not override anything as they are the final states

```
   1: public class ProcessedStatus : MessageStatus
```
```
   2: {
```
```
   3:   public const string StatusName = "Processed";
```
```
   4:  
```
```
   5:   public ProcessedStatus() : base(StatusName) { }
```
```
   6:  
```
```
   7:   public override void Complete()
```
```
   8:   {
```
```
   9:     Status = SentStatus.StatusName;
```
```
  10:   }
```
```
  11:  
```
```
  12:   public override void Fail()
```
```
  13:   {
```
```
  14:     Status = FailedProcessingStatus.StatusName;
```
```
  15:   }
```
```
  16:  
```
```
  17: public class SentStatus : MessageStatus
```
```
  18: {
```
```
  19:   public const string StatusName = "Sent";
```
```
  20:  
```
```
  21:   public SentStatus() : base(StatusName) { }
```
```
  22: }
```
```
  23:  
```
```
  24: public class FailedProcessingStatus : MessageStatus
```
```
  25: {
```
```
  26:   public const string StatusName = "FailedProcessing";
```
```
  27:  
```
```
  28:   public FailedProcessingStatus() : base(StatusName) { }
```
```
  29: }
```

Next step – mapping.

Mapping is done with FluentNHibernate, which is a great DSL to simplify and abstract XML mapping from domain world into relational database. Saying that, it is a good practice to understand what is done behind the scenes. There are plenty of resources out there. My recommendation is the XXX book.

Message mapping looks like this:

```
   1: public sealed class MessageMap : ClassMap<Message>
```
```
   2: {
```
```
   3:   public MessageMap()
```
```
   4:   {
```
```
   5:     Not.LazyLoad(); 
```
```
   6:     Id(x => x.Id);
```
```
   7:     Component(x => x.Content, part =>
```
```
   8:                               part.Map(y => y.Value)
```
```
   9:                                 .ColumnName("Content")
```
```
  10:                                 .CustomSqlTypeIs("text")
```
```
  11:                                 .Not.Nullable());
```
```
  12:  
```
```
  13:     References(x => x.Status)
```
```
  14:       .Not.Nullable()
```
```
  15:       .Not.LazyLoad()
```
```
  16:       .FetchType.Join();
```
```
  17:   }
```
```
  18:  
```
```
  19:   private XmlDocument Generate()
```
```
  20:   {
```
```
  21:     var mapping = CreateMapping(new MappingVisitor());
```
```
  22:     Trace.WriteLine(Regex.Replace(mapping.InnerXml, ">", ">\r"));
```
```
  23:     return mapping;
```
```
  24:   }
```
```
  25: }
```

Content is just a string at this moment, but it makes sense to wrap it with a value object and give it a meaning of Content, rather than just a string. Lately I see more an more benefit in this technique, especially when dealing with a new domain and understanding of domain concepts is rapidly changing.

Messages’ status is referenced by message. Cascade.All() will cause saving of the MessageStatus entity with messages’ ID. That is done intentionally, in order to allow querying later with no message data, just the ID. Mapping looks like this (and generated by the Visitor provided by FluentNHibernate):

```
   1: <?xml version="1.0" encoding="utf-8"?>
```
```
   2:     <hibernate-mapping xmlns="urn:nhibernate-mapping-2.2" default-lazy="true" assembly="StatePatternPersisted" namespace="StatePatternPersisted.Domain">
```
```
   3:         <class name="Message" table="`Message`" xmlns="urn:nhibernate-mapping-2.2" lazy="false"><id name="Id"><generator class="native"/></id>
```
```
   4:             <many-to-one cascade="all" not-null="true" lazy="proxy" fetch="join" name="Status" column="Status_id" />
```
```
   5:             <component name="Content" insert="true" update="true">
```
```
   6:                 <property name="Value" length="100" type="String">
```
```
   7:                     <column name="Content" not-null="true" sql-type="text" />
```
```
   8:                 </property>
```
```
   9:             </component>
```
```
  10:         </class>
```
```
  11: </hibernate-mapping>
```

Writing this by hand is possible, but too tedious.

Mapping MessageStatus has to be based on the fact that each entity will have a value (discriminator) that will cause NHibernate to instantiate this or another descendent of MessageStatus base abstract class.

```
   1: public MessageStatusMap()
```
```
   2: {
```
```
   3:   Not.LazyLoad();
```
```
   4:   Id(x => x.Id);
```
```
   5:   var column_name = "Status";
```
```
   6:  
```
```
   7:   DiscriminateSubClassesOnColumn<string>(column_name)
```
```
   8:     .SubClass<ReceivedStatus>(ReceivedStatus.StatusName, x => { })
```
```
   9:     .SubClass<ProcessedStatus>(ProcessedStatus.StatusName, x => { })
```
```
  10:     .SubClass<SentStatus>(SentStatus.StatusName, x => { })
```
```
  11:     .SubClass<FailedProcessingStatus>(FailedProcessingStatus.StatusName, x => { });
```
```
  12: }
```

The generated HBM shows the details:

```
   1: <?xml version="1.0" encoding="utf-8"?>
```
```
   2: <hibernate-mapping xmlns="urn:nhibernate-mapping-2.2" default-lazy="true" assembly="StatePatternPersisted" namespace="StatePatternPersisted.Domain">
```
```
   3:     <class name="MessageStatus" table="`MessageStatus`" xmlns="urn:nhibernate-mapping-2.2" lazy="false"><id name="Id"><generator class="native"/></id>
```
```
   4:         <discriminator column="Status" type="String" />
```
```
   5:         <subclass name="StatePatternPersisted.Domain.MessageStatuses.SentStatus, StatePatternPersisted, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null" discriminator-value="Sent" />
```
```
   6:         <subclass name="StatePatternPersisted.Domain.MessageStatuses.FailedProcessingStatus, StatePatternPersisted, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null" discriminator-value="FailedProcessing" />
```
```
   7:         <subclass name="StatePatternPersisted.Domain.MessageStatuses.ReceivedStatus, StatePatternPersisted, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null" discriminator-value="Received" />
```
```
   8:         <subclass name="StatePatternPersisted.Domain.MessageStatuses.ProcessedStatus, StatePatternPersisted, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null" discriminator-value="Processed" />
```
```
   9:     </class>
```
```
  10: </hibernate-mapping>
```

NHibernate will use the column “Status” to discriminate the entities based on the value in that column. Each value is mapped to a particular MessageStatus implementer.

What’s next?

Next we should be doing configuration and persistence into the actual database, which I leave to your own choice. In order to allow code download, I have stripped the “heavy tools/libraries” in case those can be downloaded separately by just looking on the empty folder names in the Build project. I hope this example will help others to see the oportunities hidden behind FluentNHibernate DSL, to leverage an easy ORM such as NHibernate in order to create better code.

Code for [download](http://weblogs.asp.net/blogs/sfeldman/StatePatternPersisted_34B65BA4.zip)

**Update:** Seems like I completely forgot to implement the Entity class itself. public abstract class Entity { public int Id {get; private set;} ...}  
Entity has also to implement the  overriden GenHashCode, ToString, and Equality.


