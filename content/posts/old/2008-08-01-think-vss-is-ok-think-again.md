---
title: Think VSS is OK? Think Again.
slug: think-vss-is-ok-think-again
date: '2008-08-01T18:16:33'
updated: '2008-08-01T18:16:33'
draft: false
author: Sean Feldman
---


Issues are:

* Constant requirement to defrag the VSS database* Loosing checked in code* Merging is absolute on block, and not partial merging* VSS client for VS.NET sucks, when getting latest version and focus away, the VSS dialog box hangs, along with VS.NET itself* Deleting checked out files leaves them on server* Checking in files that were touched, but final result was not different from original (1)* Patching?

What did you find that I didn't list here? Help me to convince my good fellow coworkers to move away from the beast. Thank you.

(1) Checked out file for change and reverted change to original code (i.e. file has not changed)


