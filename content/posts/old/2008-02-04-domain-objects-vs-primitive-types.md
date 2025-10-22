---
title: Domain Objects vs. Primitive Types
slug: domain-objects-vs-primitive-types
date: '2008-02-04T04:25:44'
updated: '2008-02-04T04:25:44'
draft: false
tags:
- .NET
- OO
- Personal
author: Sean Feldman
---


Lately I am paying more and more attention to aspects of Domain Driven Development (DDD), development where code is looking more at the domain in which it is trying to resolve problem(s), rather than technologies it is using. One of the biggest headaches that you getting into when trying to adopt DDD is persistence. Normally persistence is done in Relational database such as SQL server, Oracle, or another vendor database. And this is exactly the problem - Object Oriented model vs. Relational Data model. So what is more important, a software that is written in DDD way,  that forces you to put DB on a lower priority, or DB efficiency as a priority pushing your software from Domain driven development to become a Data Driven development? If you asking me - domain is more  valuable. I will show an example that to me serves the best proof for those who still try to save the "extra round trips to DB" or "we could combine the queries and have a single call to the DB". Keep in mind, I am not going against DB efficiency, after all a sloppy data access can kill the best application out there. But having a great data access model will not make you application writing easier, on contrary.

The example is simple. The system defines Organizations. One of the views has to list all the organizations in the system with one business rule that is coming from a client as a requirement - "the default" organization has always to appear on top.

So having a list of Organizations I need to apply the rule to transform the list and pass to the view. Simple. This is where differences between Domain DD and Data DD are starting to bubble up.

Note: according to the client, default organization is setup once per application and is not changing. The development team has decided to store the default organization id (Guid) in a configuration file for simplicity.

The first code does the next:

```



```
```

   1:  namespace Sample
   2:  {
   3:    public class DefaultOrganizationIsOnTopBusinessRule
   4:    {
   5:      private readonly Organization defaultOrganization;
   6:      private readonly List originalOrganizationList;
   7:   
   8:      public DefaultOrganizationIsOnTopBusinessRule(
   9:                  IEnumerable organizations,
  10:                  Organization defaultOrganization)
  11:      {
  12:        originalOrganizationList = new List(organizations);
  13:        this.defaultOrganization = defaultOrganization;
  14:      }
  15:   
  16:      public IList Apply()
  17:      {
  18:        if (originalOrganizationList.Contains(defaultOrganization))
  19:        {
  20:          List newList = new List();
  21:          newList.Add(originalOrganizationList
  22:                      .Find(delegate(Organization org)
  23:                      {
  24:                         return org.Equals(defaultOrganization);
  25:                      }));
  26:          newList.AddRange(originalOrganizationList
  27:                     .FindAll(delegate(Organization org)
  28:                     {
  29:                        return !org.Equals(defaultOrganization);
  30:                     }));
  31:          return newList;
  32:        }
  33:   
  34:        return originalOrganizationList;
  35:      }
  36:    }
  37:  }

```

The second code, does almost the same, except that it tries to "save a trip to DB" in terms of supplying just the default organization id, and not the entity. the code is:

```

   1:  namespace Sample
   2:  {
   3:    public class DefaultOrganizationIsOnTopBusinessRule
   4:    {
   5:      private readonly Guid defaultOrganizationGuid;
   6:      private readonly List originalOrganizationList;
   7:   
   8:      public DefaultOrganizationIsOnTopBusinessRule(
   9:                  IEnumerable organizations,
  10:                  Guid defaultOrganizationGuid)
  11:      {
  12:        originalOrganizationList = new List(organizations);
  13:        this.defaultOrganizationGuid = defaultOrganizationGuid;
  14:      }
  15:   
  16:      public IList Apply()
  17:      {
  18:        Organization defaultOrg = originalOrganizationList
  19:                      .Find(delegate(Organization org)
  20:                      {
  21:                         return org.Guid == defaultOrganizationGuid;
  22:                      });
  23:        if (defaultOrg != null)
  24:        {
  25:          List newList = new List();
  26:          newList.Add(defaultOrg);
  27:          newList.AddRange(originalOrganizationList
  28:                     .FindAll(delegate(Organization org)
  29:                     {
  30:                        return org.Guid != defaultOrganizationGuid;
  31:                     }));
  32:          return newList;
  33:        }
  34:   
  35:        return originalOrganizationList;
  36:      }
  37:    }
  38:  }

```

but this is an illusion of "quick" and "quality" code - several reasons:

1. Who said we need to reconstruct the default organization all the time? We can leverage caching to keep it available to us without hitting DB each time
2. Who said that organization entity is going to be identified by a Guid in the next few iterations?
3. We are violating encapsulation by reaching out into the internals of an entity (object) - an object should know how to do things on itself
4. Maintainability - what is easy to understand, a code that requires an object, or a code that expects a Guid?
5. How easy it is to break the code if rather than sending a Guid of an organization we will send a Guid of another entity type that is also identified by a Guid?

If you answer these questions and you find yourself preferring the 1st code snippet, then domain is what you care for more, and along with it maintainability of what you build. In case the second code snippet is more appealing to your heart, then DB is all you care and get ready for some serious hacks and workarounds in your code to keep it running for the sake of efficient DB access.

To finish this post, I would like to comment a few sentences from Eric Evans book:

"*The goal of domain-driven design is to create better software by focusing on a model of the domain rather than the technology. By the time a developer has constructed an SQL query, passed it to a query service in the infrastructure layer, obtained a result set of table rows, pulled the necessary information out, and passed it to a constructor or FACTORY, the model focus is gone. It becomes natural to think of the objects as containers for the data that the queries provide, and the whole design shifts toward a data-processing style. The details of the technology vary, but the problem remains that the client is dealing with technology, rather than model concepts.*"


