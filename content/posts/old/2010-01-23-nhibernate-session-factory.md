---
title: NHibernate Session Factory
slug: nhibernate-session-factory
date: '2010-01-23T03:39:00'
updated: '2010-01-23T03:39:00'
draft: false
tags:
- NHibernate
author: Sean Feldman
---


Each time we use NHibernate, we have to share production and semi-production code for NHibernate *SessionFactory*. Production code is the portion that is actually responsible to generate the *SessionFactory* on startup. Semi-production code, is the code that generates *SessionFactory* for purpose of schema extraction (SQL statements we use to generate DB). This time around, the smell had to be removed. Having identical code duplicated not only risky, but also becomes intolerable once it grows beyond a single line. This is our new SessionBuilder, that leverages the same code to generate **SessionFactory** for run-time purpose and schema generation at “design” time.

```

private static ISessionFactory sessionFactory;
private ISession session;
 
public ISession GetSession()
{
  Initialize();
  if (session == null)
```
session = sessionFactory.OpenSession();
```
return session;
}
 
public void CloseSession()
{
  if (session.IsNull())
```
return;
```
session.Close();
  session.Dispose();
  session = null;
}
 
private static void Initialize()
{
  if (sessionFactory.IsNull())
```
sessionFactory = GetProjectNHibernateConfiguraton().BuildSessionFactory();
```
}
 
private static FluentConfiguration GetProjectNHibernateConfiguraton()
{
  var nhibernateConfiguration = new Configuration().Configure();
 
  var model = AutoMap.AssemblyOf().IgnoreBase()
```
.Where(type => typeof (Entity).IsAssignableFrom(type))
.Conventions.AddFromAssemblyOf<Entity>()
.UseOverridesFromAssemblyOf<Entity>();
```
return Fluently.Configure(nhibernateConfiguration)
```
.Mappings(mappingConfiguration => mappingConfiguration.AutoMappings.Add(model));
```
}
 
#region Manually used to generate DB schema SQL scripts
 
internal static string DROP_SCHEMA_SQL_SCRIPT_NAME =   new FileInfo(Path.Combine(Path.GetTempPath(), "Schema_Drop.sql")).FullName;
internal static string CREATE_SCHEMA_SQL_SCRIPT_NAME =   new FileInfo(Path.Combine(Path.GetTempPath(), "Schema_Create.sql")).FullName;
 
/// Use TestDriven.Net to run this method as a test to generate SQL scripts and their files.
internal static void Generate_Database_Schema_and_Create_SQL_script_files()
{
  GetProjectNHibernateConfiguraton()
```
.ExposeConfiguration(SchemaGenerator)
.BuildSessionFactory();
```
}
 
private static void SchemaGenerator(Configuration configuration)
{
  var schemaExport = new SchemaExport(configuration);
  schemaExport.SetOutputFile(DROP_SCHEMA_SQL_SCRIPT_NAME).Drop(true, false);
  schemaExport.SetOutputFile(CREATE_SCHEMA_SQL_SCRIPT_NAME).Create(true, false);
}
 
#endregion

```

Region represents the “design-time” code. And I was using Fluent NHibernate with auto-mapping to generate the entities.


