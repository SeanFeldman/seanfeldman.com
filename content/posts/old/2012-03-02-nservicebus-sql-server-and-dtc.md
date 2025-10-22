---
title: NServiceBus, SQL Server, and DTC
slug: nservicebus-sql-server-and-dtc
date: '2012-03-02T04:16:00'
updated: '2012-03-02T04:16:00'
draft: false
tags:
- NServiceBus
author: Sean Feldman
---


This exception drove me nuts:

> System.Transactions.TransactionException: The partner transaction manager has disabled its support for remote/network transactions. (Exception from HRESULT: 0x8004D025) ---> System.Runtime.InteropServices.COMException: The partner transaction manager has disabled its support for remote/network transactions. (Exception from HRESULT: 0x8004D025)

[This blog post](http://mikaelkoskinen.net/post/fixing-disabled-its-support-for-remote-network-transactions-HRESULT-0x8004D025.aspx) solved it and made my day. Thank you.

DTC was disabled on SQL Server machine, which caused messages sent via NServiceBus to fail when NSB service was trying to process them in transactional manner agains SQL Server. As blog post above says, [Microsoft post](http://technet.microsoft.com/en-us/library/cc753510(WS.10).aspx) explains how to address the issue.


