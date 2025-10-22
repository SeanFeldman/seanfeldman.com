---
title: Deploying an Azure WebJob with GitHub Actions
slug: azure-webjob-with-github-action
date: '2020-06-02T05:11:00'
updated: '2022-04-01T20:04:51.184355'
draft: false
tags:
- WebJob; GitHub
author: Sean Feldman
---
![enter image description here][1]

**2022-04 Update**: as Lee McMullen has [pointed out][2], the deployment task `srijken/azure-zip-deploy@v1.0.1` has been replaced by `azure/webapps-deploy@`.

WebJobs are a hidden gem within Azure App Service. While it's coupled to the web application, one of the neat tricks is to turn it into a worker service for continuous background processing. Arguably, this could be also accomplished by Azure Functions, but in certain scenarios, it's simpler to have an equivalent of what used to be a Windows Service. I will skip the building a WebJob part. It's sufficiently enough [documented](https://docs.microsoft.com/en-us/azure/app-service/webjobs-create) by Microsoft. [Yves Goeleven](https://twitter.com/yvesgoeleven) has done some really nice work with WebJobs he'd be happy to share with those that are looking for ideas. And while what he's done is great, I will mention that I'd love to see a WebJob as a Service kind of offer coming soon. Or some Worker as a role. Something that would fill in the gap that is there. Not everything is containers/Kubernetes or Functions. And using WebJobs under the App Service umbrella feels like hunting a mosquito with a canon. Without further ado, how to deploy a WebJob using GitHub actions?

## Assumptions

### Operation system

When using GitHub actions, the operating system used matters. Windows images are twice more expensive than Linux. This directly translates into having half the free minutes when running with Windows. While it's not the biggest factor, there's really no reason to demand a Windows image when building, testing, and deploying to Azure a .NET based WebJob. Therefore, I'll be using a Linux image for this post.

### Conditional execution

If you're like me and push almost every commit, it can become quite expensive very fast. I also like to work in PRs, leveraging draft PRs as an indication the work is still in progress. With that in mind, I'd like to avoid unnecessary deployments on PR builds while PRs are marked as draft PRs. In addition to that, I'll skip the packaging of the WebJob if a deployment is not taking place. While it's such a small optimization, it leads to faster build execution.

### Managing secrets

GitHub Actions has support for [creating and managing secrets](https://help.github.com/en/actions/configuring-and-managing-workflows/creating-and-storing-encrypted-secrets). I'll use that and frankly, recommend you always store your secrets that way. In my example, I'll be storing `.publishsettings` files retrieved from the portal as GitHub secrets.

### Project structure

```csharp
WebJobSolution/
├── .github/workflows/
│   └── dotnet-core.yml
└── src/
    ├── worker
    │   ├── worker.csproj
    │   ├── run.cmd
    │   ├── settings.job
    │   └── ...
    └── worker.sln
```
## Action script

```csharp
name: .NET Core
env:
  BINARIES: './output/app_data/jobs/continuous/mywebjob' # the last folder name will become the webjob name in the portal
  ZIP_FILE: 'webjob.zip'
  ZIP_PATH: './output'
  ZIP_FILEPATH: './output/webjob.zip'
on:
  push:
    branches: [ master, develop ]
  pull_request:
    branches: [ master, develop ]
    types: [review_requested, ready_for_review]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Setup .NET Core
      uses: actions/setup-dotnet@v1
      with:
        dotnet-version: 3.1.101
    - name: Install dependencies
      run: dotnet restore ./src/worker.sln
    - name: Build
      run: dotnet build ./src/worker.sln --configuration Release --no-restore --output ${{env.BINARIES}}
    - name: Test
      run: dotnet test ./src/worker.sln --no-restore --verbosity normal --output ${{env.BINARIES}}
    - name: Zip
      if: github.event_name != 'pull_request' # skip on PRs
      uses: nguyenquyhy/zip-release@v0.3.0
      with:
        filename: '${{env.ZIP_FILE}}'
        workingDirectory:  ${{env.ZIP_PATH}}
        exclusions: 'worker.exe app_data/**/unix/*' # skip .exe and Unix runtime as deployment will be to a Windows App Service
    - name: Deploy to Test (develop branch) # skip on PRs
      if: github.ref == 'refs/heads/develop' && github.event_name != 'pull_request' # skip on PRs, deploy develop branch to the test environment
      uses: srijken/azure-zip-deploy@v1.0.1
      with:
        zip-file: ${{env.ZIP_FILEPATH}}
        publish-profile: ${{ secrets.WEBJOB_PUBLISH_PROFILE_TEST }}
    - name: Deploy to Production (master branch)
      if: github.ref == 'refs/heads/master' && github.event_name != 'pull_request' # skip on PRs, deploy master branch to the production environment
      uses: azure/webapps-deploy@v2
      with:
        app-name: ${{ env.AZURE_WEBAPP_NAME }}
        package: ${{env.ZIP_FILEPATH}}
        publish-profile: ${{ secrets.WEBJOB_PUBLISH_PROFILE_PROD }}
```
With this fairly small script, an automated CI/CD will be executed and deploy the WebJob whenever a change is done on `develop` or `master` branches, deploying the bits into the testing or production environment. Happy deploying!


[1]: https://aspblogs.blob.core.windows.net:443/media/sfeldman/2020/azure-webjob-with-github-action/cogwheel.jpg
[2]: https://twitter.com/leemcmullen/status/1509821581329149954
