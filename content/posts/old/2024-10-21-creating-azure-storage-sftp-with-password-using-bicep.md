---
title: Creating Azure Storage SFTP with Password using Bicep
slug: creating-azure-storage-sftp-with-password-using-bicep
date: '2024-10-21T04:08:20.433375+00:00'
updated: '2024-10-21T04:08:20.355240+00:00'
draft: false
tags:
- Azure
- Bicep
author: Sean Feldman
---
Azure Storage service has a neat little option for hosting an SFTP. Doing so lets you upload your files as blobs to your Storage account. This is extremely helpful, especially when working on the decades-old system migrated to Azure but still requiring SFTP for data transfer. The documentation and setup of SFTP with a Storage account are straightforward—until you try to create the resource using Bicep and set the password as part of Bicep deployment. This is where it's getting a bit cumbersome.

TLDR: Setting the password when creating the Storage account and SFTP user using Bicep is impossible. The password has to be **reset**.

This means that OOTB Bicep can create an SFTP user but cannot set the password. The password needs to be reset, even if it hasn't been set yet, and the only way to do that is via the portal UI or scripting. The portal UI option is unacceptable if you're trying to automate your resource deployment. Which leaves the scripting option. Let's dive into the code.

```csharp
param location string = resourceGroup().location
var sftpRootContainterName = 'sftp'
var sftpUserName = 'sftpuser'
var unique = uniqueString(resourceGroup().id)
resource storageAccount 'Microsoft.Storage/storageAccounts@2022-09-01' = {
  name: toLower('mysftp${unique}')
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    allowBlobPublicAccess: false
    allowCrossTenantReplication: false
    allowSharedKeyAccess: true
    isHnsEnabled: true
    isLocalUserEnabled: true
    isSftpEnabled: true
    isNfsV3Enabled: false
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
  }
  tags: {}
}
resource blobServicesResource 'Microsoft.Storage/storageAccounts/blobServices@2022-09-01' = {
  parent: storageAccount
  name: 'default'
  properties: {
  }
  resource sftpStorageContainer 'containers' = {
    name: sftpRootContainterName
    properties: {
      publicAccess: 'None'
    }
  }
}
resource sftpLocalUserResource 'Microsoft.Storage/storageAccounts/localUsers@2023-05-01' = {
  name: sftpUserName
  parent: storageAccount
  properties: {
    permissionScopes: [
      {
        permissions: 'rcwdl'
        service: 'blob'
        resourceName: sftpRootContainterName
      }
    ]
    homeDirectory: '${sftpRootContainterName}/' // This user will have complete control over the "root" directory in sftpRootContainterName
    hasSharedKey: false
  }
}
// Managed identity necessary to execute the scirpt
resource storageAccountManagedIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' existing = {
  name: 'mi-sandbox-sean-feldman'
  scope: resourceGroup()
}
// The script to reset the password
resource deploymentScript 'Microsoft.Resources/deploymentScripts@2023-08-01'= {
  name: 'mysftp-inlineCLI-${unique}'
  location: location
  kind: 'AzureCLI'
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${storageAccountManagedIdentity.id}': {}
    }
  }
  properties: {
    azCliVersion: '2.63.0'
    arguments: '${storageAccount.name} ${resourceGroup().name} ${sftpUserName}'
    scriptContent: '''
      az storage account local-user regenerate-password --account-name $1 -g $2 -n $3
    '''
    timeout: 'PT5M'                 // Set timeout for the script execution (optional)
    cleanupPreference: 'OnSuccess'  // Automatically clean up after success
    retentionInterval: 'PT1H'       // Retain script resources for 1 hour after execution
  }
}
// DO NOT do this in production
output text string = deploymentScript.properties.outputs.sshPassword
```
The solution is to deploy and run the `deploymentScript` AZ CLI script to reset the password. The output of the `az storage account local-user regenerate-password` is the generated password, the output object of the script resource, as the `sshPassword`. But this is not ideal for production. For production, keeping the password in Azure KeyVault or Azure Config Service is better. With a twist, testing if the value exists first and setting it only if it doesn't is better.
