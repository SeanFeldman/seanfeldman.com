---
title: Azure Automation – Reducing Cost
slug: azure-automation-reducing-cost
date: '2014-04-08T14:18:00'
updated: '2014-04-08T14:18:00'
draft: false
author: Sean Feldman
---


The idea behind this is extremely simple: to run a deployment machine in Azure that will be used to deploy updates to production. In my environment we get everything packaged on build server, but deployment has to happen in a controlled environment and from a manual kick-off. Deployments are not performed at night, hence compute time is wasted. To save 50% (at least) of compute time, VM has to be down.

Plan for solution: get a single instance VM down during night and up at work hours. My initial thought was to use Azure Cloud Services auto-scale feature.

Pros:

- Defined under Cloud Service VM instance belongs to

- Scaling is a property of Cloud Service

Cons:

- Requires Availability Set to be created and associated with VM instance

- Requires at least 2 VM instances to run Auto-Scaling (deal breaker!)



Fortunately, with the new release of Azure Automation, this can be done with Runbooks (a Runbook is a workflow that contains a PowerShell script, that can also call child Runbooks).

Pros:

- Doesn’t require multiple instances of VM (hence saving money)

- Runs under the context of subscription, therefore has access to **all resources**

Cons:

- Scheduling is not as flexible as with Auto-Scaling and needs to be associated with a Runbook



What I ended up doing was quick and dirty, but it does the job for now.

1. Create an automation object (Virtual-Machines)

[![clip_image001](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/clip_image001_thumb_0BCA6BB9.png "clip_image001")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/clip_image001_478773BB.png)

2. Imported two Runbooks into automation (Start-AzureVMsOnSchedule and Stop-AzureMVsOnSchedule)

[![clip_image002](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/clip_image002_thumb_4B2AAFFA.png "clip_image002")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/clip_image002_1B6D077B.png)

Note that “import” is as simple as importing PS script wrapped in *workflow name\_of\_workflow { #powershell script }*

3. Published imported runbooks

[![clip_image003](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/clip_image003_thumb_759971C8.png "clip_image003")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/clip_image003_7AE85879.png)

4. Associated a schedule with each runbook

[![clip_image004](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/clip_image004_thumb_47427CCC.png "clip_image004")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/clip_image004_6C403D45.png)

5. Specified for each schedule to execute on a certain time daily (for Start runbook to run at 7AM, for Stop runbook to run at 7PM). BTW, parameters can be passed to individual runbooks, so that job (executed runbook) becomes a parameterized job. Also, resources can be used from all

[![clip_image005](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/clip_image005_thumb_7FEFB78A.png "clip_image005")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/clip_image005_7E1F61C3.png)

6. Once a job (schedule runbook) was executed, it’s logged (you can drill into details of each command – can see Bruce`s eyes light up)

[![clip_image006](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/clip_image006_thumb_317DB5D1.png "clip_image006")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/clip_image006_6FE37984.png)

7. Job executed (spike at 7AM) and VM is up and running. Big Success \*Borat accent\* :)

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_0326C0D5.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_08097491.png)

[![image](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_thumb_7961595C.png "image")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/image_3A03A5CC.png)

Note that when you edit Draft of your runbook, you can run (test) it before publishing. Also, you can import existing modules (Azure module is imported by default) using command toolbar at the bottom, add settings that can be shared by multiple runbooks, and insert Activity (powershell command) / Runbook / setting.

[![clip_image007](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/clip_image007_thumb_76BB2E5C.png "clip_image007")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/clip_image007_298B34D1.png)

Azure Automation is a great feature to leverage. Excited to see all of these things shaping up and making work easier, allowing to cut down costs at the same time.

Update 1: I’ve noticed that while VM was started and stopped, scripts didn’t execute cleanly. To solve that, I had to wrap commands in InlineScript { #start/stop-AzureVM … } construct








































































