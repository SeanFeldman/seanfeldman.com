---
title: Azure Blob Storage Cold Tier
slug: azure-blob-storage-cold-tier
date: '2023-08-16T04:31:46.617033+00:00'
updated: '2023-08-16T04:31:46.585752+00:00'
draft: false
author: Sean Feldman
---
Azure Storage service is the foundational building block in cloud architecture. Cheap, reliable, resilient, and powerful. From small solutions to monster systems, Blob service, in particular, is convenient. Any system that involves any type of document slowly but steadily has the number of blobs/files growing over time. Be it specific business requirements or legal aspects, blobs must be kept around for some time. But not all blobs are equal.
Blobs has had the concept of tiers for quite a while. Two tiers that are opposite extremes are Hot and Archive. The Hot tier is fast and inexpensive to access but more expensive to store. The Archive tier is inexpensive to store, but when it comes to reading and writing, let's say it's not a good idea. For a while, there was also the Cool tier. A middle ground if you wish. Blobs that might be accessed but very infrequently.
Recently, there's even more granularity when it comes to tiers. The Cold tier. The Cold tier is positioned between the Cool and Archive, adding more cost-effectiveness to storing blobs.
So how do you choose which tier is the right tear for the problem?
Understand the business needs. How blobs will be used. Plan accordingly. In many cases, blobs must be frequently accessed initially and then progress into the next, cooler tier, depending on the business rules. Microsoft recommended strategy is the [following][1].
- \*\*Cool\*\* tier: minimum retention of 30 days
- \*\*Cold\*\* tier: minimum retention of 90 days
- \*\*Archive\*\* tier: minimum retention of 180 days
This doesn't mean you absolutely must follow this recommendation. What if your blobs are stored and never accessed? Or stored and might be accessed at any time?
This is where [Blob Lifecycle Management Policies][2] are so handy. For example, let's say I'd like to reduce the cost of keeping blobs from day one but have the option to access those. I.e. not fully archived. The following policy would help with that by moving all blobs (including the existing ones) to the new Cold tier right away (some delay is expected as Storage service runs this not in real-time).
```
{
  "rules": [
    {
      "enabled": true,
      "name": "To-Cold",
      "type": "Lifecycle",
      "definition": {
        "actions": {
          "baseBlob": {
            "tierToCold": {
              "daysAfterModificationGreaterThan": 0
            }
          }
        },
        "filters": {
          "blobTypes": [
            "blockBlob"
          ],
          "prefixMatch": [
            "masters/"
          ]
        }
      }
    }
  ]
}
```
This will allow much lower storage costs. Remember, there will be higher access and transaction costs when blobs are accessed. The difference is that these blobs will be available \*\*immediately\*\* and not \*\*eventually\*\*, as they would be with the Archived tier.
[1]: https://learn.microsoft.com/en-us/azure/storage/blobs/access-tiers-overview#summary-of-access-tier-options
[2]: https://learn.microsoft.com/en-us/azure/storage/blobs/lifecycle-management-policy-configure
