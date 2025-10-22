---
title: Jenkins – Getting Revision for Project with Multiple Modules
slug: jenkins-getting-revision-for-project-with-multiple-modules
date: '2011-04-07T04:43:00'
updated: '2011-04-07T04:43:00'
draft: false
tags:
- CI
author: Sean Feldman
---


I ran into this problem just recently on a project that has more than a single repository for a project. Using Jenkins (Hudson) was awesome for the past 2+ years and I was surprised that it couldn’t handle revision environment variable assignment when more than a single module had a place in a build job. According to [some threads](http://jenkins.361315.n4.nabble.com/svn-revision-with-multiple-modules-my-2EuroCents-td373332.html), this is done by design. One workaround in particular that I liked was to look into the poll log file and get information out of it.

This is a quick implementation of a get-revision function for nant to grab revision based on the project name (*stringToSearch* argument) and its looking at the polling log file per project.

. 
```
   1: <script language="C#" prefix="utils">
```
   1:  
```
```
   2:         <imports>
```
```
   3:             <import namespace="System.Globalization"/>
```
```
   4:             <import namespace="System.IO"/>
```
```
   5:       <import namespace="System.Text.RegularExpressions"/>
```
```
   6:     </imports>
```
```
   7:         <code>
```
```
   8:             <![CDATA[
```
```
   9:               [Function("get-revision")]
```
```
  10:               public static int GetRevision(string filePath, string stringToSearch) 
```
```
  11:                             {
```
```
  12:                 if (!System.IO.File.Exists(filePath))
```
```
  13:                   return 0;
```
```
  14:                                 System.IO.FileInfo file = new System.IO.FileInfo(filePath);
```
```
  15:                 using (System.IO.StreamReader stream = file.OpenText())
```
```
  16:                 {
```
```
  17:                   System.Text.RegularExpressions.Match match = System.Text.RegularExpressions.Regex.Match(stream.ReadToEnd(), stringToSearch + @".*\srevision\s(?<revision>.*?)\r #string_to_search <ANYTHING>revision(group_revision)\r",
```
```
  18:                     System.Text.RegularExpressions.RegexOptions.Multiline |
```
```
  19:                     System.Text.RegularExpressions.RegexOptions.IgnoreCase | 
```
```
  20:                     System.Text.RegularExpressions.RegexOptions.IgnorePatternWhitespace);
```
```
  21:                   return match.Success ? int.Parse(match.Groups["revision"].Value, System.Globalization.NumberStyles.Any) : 0;
```
```
  22:                 }
```
```
  23:               }
```
```
  24:             ]]>
```
```
  25:         </code>
```
```
  26:     
```
</script>
```

And this is how the typical usage would look like:

```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; background-color: white; margin: 0em; border-left-style: none; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; border-right-style: none; font-size: 8pt; overflow: visible; padding-top: 0px"><span style="color: #606060" id="lnum1">   1:</span> <span style="color: #0000ff">&lt;</span><span style="color: #800000">property</span> <span style="color: #ff0000">name</span><span style="color: #0000ff">=&quot;svn.revision&quot;</span> <span style="color: #ff0000">value</span><span style="color: #0000ff">=&quot;0&quot;</span> <span style="color: #ff0000">readonly</span><span style="color: #0000ff">=&quot;false&quot;</span><span style="color: #0000ff">/&gt;</span></pre>
```
```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; background-color: #f4f4f4; margin: 0em; border-left-style: none; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; border-right-style: none; font-size: 8pt; overflow: visible; padding-top: 0px"><span style="color: #606060" id="lnum2">   2:</span>  <span style="color: #0000ff">&lt;</span><span style="color: #800000">if</span> <span style="color: #ff0000">test</span><span style="color: #0000ff">=&quot;${environment::variable-exists('SVN_REVISION')}&quot;</span><span style="color: #0000ff">&gt;</span></pre>
```
```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; background-color: white; margin: 0em; border-left-style: none; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; border-right-style: none; font-size: 8pt; overflow: visible; padding-top: 0px"><span style="color: #606060" id="lnum3">   3:</span>    <span style="color: #0000ff">&lt;</span><span style="color: #800000">property</span> <span style="color: #ff0000">name</span><span style="color: #0000ff">=&quot;svn.revision&quot;</span> <span style="color: #ff0000">value</span><span style="color: #0000ff">=&quot;${environment::get-variable('SVN_REVISION')}&quot;</span> <span style="color: #0000ff">/&gt;</span></pre>
```
```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; background-color: #f4f4f4; margin: 0em; border-left-style: none; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; border-right-style: none; font-size: 8pt; overflow: visible; padding-top: 0px"><span style="color: #606060" id="lnum4">   4:</span>  <span style="color: #0000ff">&lt;/</span><span style="color: #800000">if</span><span style="color: #0000ff">&gt;</span></pre>
```
```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; background-color: white; margin: 0em; border-left-style: none; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; border-right-style: none; font-size: 8pt; overflow: visible; padding-top: 0px"><span style="color: #606060" id="lnum5">   5:</span>  <span style="color: #0000ff">&lt;</span><span style="color: #800000">if</span> <span style="color: #ff0000">test</span><span style="color: #0000ff">=&quot;${not environment::variable-exists('SVN_REVISION')}&quot;</span><span style="color: #0000ff">&gt;</span></pre>
```
```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; background-color: #f4f4f4; margin: 0em; border-left-style: none; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; border-right-style: none; font-size: 8pt; overflow: visible; padding-top: 0px"><span style="color: #606060" id="lnum6">   6:</span>    <span style="color: #0000ff">&lt;</span><span style="color: #800000">property</span> <span style="color: #ff0000">name</span><span style="color: #0000ff">=&quot;svn.revision&quot;</span> <span style="color: #ff0000">value</span><span style="color: #0000ff">=&quot;${utils::get-revision('.\..\scm-polling.log', project::get-name())}&quot;</span> <span style="color: #0000ff">/&gt;</span></pre>
```
```
<pre style="border-bottom-style: none; text-align: left; padding-bottom: 0px; line-height: 12pt; background-color: white; margin: 0em; border-left-style: none; padding-left: 0px; width: 100%; padding-right: 0px; font-family: &#39;Courier New&#39;, courier, monospace; direction: ltr; border-top-style: none; color: black; border-right-style: none; font-size: 8pt; overflow: visible; padding-top: 0px"><span style="color: #606060" id="lnum7">   7:</span>  <span style="color: #0000ff">&lt;/</span><span style="color: #800000">if</span><span style="color: #0000ff">&gt;</span></pre>
```

As an afterthought, I could actually set SVN\_REVISION to the value from the log, and then work with SVN\_REVISION as usual.


