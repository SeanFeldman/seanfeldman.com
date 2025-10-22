---
title: Updating Azure Service Fabric Settings
slug: updating-azure-service-fabric-settings
date: '2016-07-02T22:36:32.721140+00:00'
updated: '2016-07-02T22:36:32.705495+00:00'
draft: false
tags:
- ServiceFabric
author: Sean Feldman
---
Coming from the world of web applications where configuration file update is a matter of dropping a new version of a web.config file into the application, Azure Service Fabric can be a new territory. Especially with its hard rule on versioning code, data, and config packages. The config package update is what I'd like to focus on in this post.
Versioning is done on the package level with multiple components that need to be packages. Each package represents an Azure Service Fabric Application. An application consists of services. Both Application and services have manifest files.
```
Manifirst For     File Name                           
Application       ApplicationManifest.xml 
Service           ServiceManifest.xml*
```
\\*Manifest file per service
Assuming there's a default Config configuration, the folder `Config` will contain `Settings.xml` configuration file under service(s) you're interested in upgrading configuration for. Note that you can have multiple configurations files. For this post, I'm using a single one called `Config`. Original content of the file:
```
<?xml version="1.0" encoding="utf-8" ?>
<Settings xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://schemas.microsoft.com/2011/01/fabric">
  <Section Name="MyConfigSection">
    <Parameter Name="MyParameter" Value="OriginalValue" />
  </Section>
</Settings>
```
To make an update, first, the original application has to be deployed. There are two options:
1. Deploying using Visual Studio (F5 will work as well).
2. Deploying with PowerShell.
\*Some more assumptions: Application name is SFDeploymentTest; package location somewhere on you local disk is `package\_location`; each deployment package is suffixed with Version at the end (V1, V2, V3, etc).\*
1. Connect-ServiceFabricCluster
2. Copy-ServiceFabricApplicationPackage -ApplicationPackagePath package-package\_location\pkg\SFDeploymentTestV1 -ImageStoreConnectionString file:C:\SfDevCluster\Data\ImageStoreShare -ApplicationPackagePathInImageStore SFDeploymentTestV1
3. Register-ServiceFabricApplicationType -ApplicationPathInImageStore SFDeploymentTestV1
4. New-ServiceFabricApplication -ApplicationName fabric://SFDeploymentTest -ApplicationTypeName SFDeploymentTestType -ApplicationTypeVersion 1.0.0
\*To find out the image store connection string for a dev cluster, navigate to http://localhost:19080/Explorer/index.html#/tab/manifest and select ClusterManifest > FabricSettings > Section Name="Management" > Parameter Name="ImageStoreConnectionString".
```
The default value is file:C:\SfDevCluster\Data\ImageStoreShare*
```
Now comes the interesting part, upgrading the settings package only. To achieve that, the settings only package needs to be created first. The original application & service versions were 1.0.0. Even though it's just a configuration package, it still has to be versioned as a new version of application and service (which contains the configuration). Therefore application and the service will get a new version (I chose it to be 3.0.0 for the post). Make sure to update the following:
\*\*ApplicationManifest.xml\*\*
- ApplicationManifest > ApplicationTypeVersion
- ApplicationManifest >
ServiceManifestImport > ServiceManifestRef > ServiceManifestVersion
\*\*ServiceManifest.xml\*\*
- ServiceManifest > Version
- ServiceManifest > ConfigPackage > Version
Make sure you package only contains the mentioned files, plus the Config folder with the settings.xml file. No code. No data. Config only package. To verify that setting is auto-propagated, I've modified `MyParameter` from `OriginalValue` to `NewValueThree`.
With a new package named `SFDeploymentTestV2`, the update deployment goes as the following:
1. Copy-ServiceFabricApplicationPackage -ApplicationPackagePath package\_location\pkg\SFDeploymentTestV3 -ImageStoreConnectionString file:C:\SfDevCluster\Data\ImageStoreShare -ApplicationPac
```
kagePathInImageStore SFDeploymentTestV3
```
2. Register-ServiceFabricApplicationType -ApplicationPathInImageStore SFDeploymentTestV3
3. Start-ServiceFabricApplicationUpgrade -ApplicationName fabric:/SFDeploymentTest -ApplicationTypeVersion 3.0.0 -HealthCheckStableDurationSec 60 -UpgradeDomainTimeoutSec 1200 -UpgradeTimeout 3000 -FailureAction Rollback -Monitored
A few seconds after deployment is kicked off, the old code get the new setting value:
![enter image description here][1]
If you need to clean up your cluster, here's what I'm using.1. Remove-ServiceFabricService -ServiceName fabric:/SFDeploymentTest/StatelessSvc -Force
2. Remove-ServiceFabricApplication -ApplicationName fabric:/SFDeploymentTest -Force
3. Unregister-ServiceFabricApplicationType -ApplicationTypeName SFDeploymentTestType -ApplicationTypeVersion 3.0.0
4. Unregister-ServiceFabricApplicationType -ApplicationTypeName SFDeploymentTestType -ApplicationTypeVersion 1.0.0
5. Remove-ServiceFabricApplicationPackage -ApplicationPackagePathInImageStore SFDeploymentTestV3 -ImageStoreConnectionString file:C:\SfDevCluster\Data\ImageStoreShare
6. Remove-ServiceFabricApplicationPackage -ApplicationPackagePathInImageStore SFDeploymentTestV1 -ImageStoreConnectionString file:C:\SfDevCluster\Data\ImageStoreShare
A more brutal way is to reset the cluster, but even for a dev cluster is not always the best option if you have SF applications that need to stay.
[1]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2016/SF\_config\_package\_update/clipboard-1.png
