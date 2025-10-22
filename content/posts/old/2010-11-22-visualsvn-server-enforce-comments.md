---
title: VisualSVN Server - Enforce Comments
slug: visualsvn-server-enforce-comments
date: '2010-11-22T03:38:00'
updated: '2010-11-22T03:38:00'
draft: false
tags:
- Tools
author: Sean Feldman
---


[![Pre-commit.hook](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/Pre-commit.hook_thumb_31ADA16A.png "Pre-commit.hook")](https://aspblogs.blob.core.windows.net/media/sfeldman/Media/Pre-commit.hook_7D797823.png)

setlocal   
   
set REPOS=%1   
set TXN=%2   
set SVNLOOK="%PROGRAMFILES(X86)%\VisualSVN Server\bin\svnlook.exe"   
   
REM Make sure that the log message contains some text.   
FOR /F "usebackq delims==" %%g IN (`%SVNLOOK% log -t %TXN% %REPOS% FINDSTR /R /C:......`) DO goto NORMAL\_EXIT   
   
:ERROR\_TOO\_SHORT   
echo "Must provide comments" >&2   
goto ERROR\_EXIT   
   
:ERROR\_EXIT   
exit /b 1   
   
REM All checks passed, so allow the commit.   
:NORMAL\_EXIT   
exit 0

2012-01-03: Post on StackOverflow on this: http://stackoverflow.com/questions/247888/how-to-require-commit-messages-in-visualsvn-server
