---
author: Sean Feldman
title: New Blog Tech Stack
slug: new-blog-tech-stack
date: '2025-10-24'
featuredImage: /posts/new-blog-tech-stack/new-blog-tech-stack.webp
summary: "What powers my new self-hosted blog: site generator, theme, and the tooling I picked."
tags: 
  - Blog
comments: true
enableReadingTime: true
toc:
  enable: false
draft: false
---

My first blog hosted with Live Spaces, and its successor, hosted with weblogs.asp.net where fully hosted solutions. The latter was actaully a full blown CMS, Orchard CMS, which was quite powerful but also overcomplicated for something that is primarely used to share thoughts, code, and occacionally some images.

For a long time I didn't care much about two aspects
1. Look and feel
1. Data ownership

While the first one is arguably is still not my primary focus, though I have to admit having your "branding" is neat, the second aspect is way more important than I thought. And here's why.

For two decades, I've trusted blog hosters. For two decades I've stored all of the posts somewhere I had no clue where it was stored. And, I must confess, it's nice not to worry about hosting. Especially when self-hosting was not so cheap and amount of work to get it all set up and running wasn't trivial. But times have changed, hosting became a commodity, and data ownership has turned to be more important than I thought. To be specific, [weblogs.asp.net](https://weblogs.asp.net/) is being shut down by Microsoft, slowly strangling it to the point that it will drop. And the option of retrievig the posts hosted with the platform is no longer available. It probably sounds weird to want to see your 18 year old first post, but there's a sentimental value to that. And there's also a practical value. I post to share knowledge and often go back to my posts as notes. [User Secrets, the human-readable version](https://seanfeldman.com/posts/user-secrets-the-human-readable-version/) is one of those posts, helping me to refresh my memory where .NET user secrets are stored. Or what's the `.csproj` property to use. But I'm digressing. The point is that if you don't own that data, one day you might lose it all. So what did I do about it?

Well, I procrastinated. For a long time I sat on a fence, knowing the day will come, but not prioritizing it much. And, in a way, I'm glad I haven't done much. Because the time went by and the options have increased. And my definition of what I wanted vs didn't want to do with a blog. Here's that objectives list.

1. **No coding**. It's not a pet project. I just need to write and publish my thoughts.
1. **Customizable, but not too complex**. Something that allows me to arrange things the way I like them.
1. **A flow I'm comfortable with**. I'm a developer, if a code-based flow can be used, I'll use it.
1. **Zero infrastructure**. I don't want to deal with hosting, deployments, etc.
1. **Own my posts**. Ownership of the posts and ability to take if from one place to another if necessary.
1. **Ease of composing**. Markdown for documentation worked well for me in the past. I'd like to do that and avoid CSS nightmares for my content.

Based on those, the natural choice was a static site generator. The idea of a static site generator is by no means revolutionary or new. It's been around for quite a while. TLDR: a tool that takes your static content, transforms it into HTML/CSS/JS to run as a static webapp. I've looked at Statiq, Jekyll, Zola, and Hugo. [Hugo](https://gohugo.io/) was the one that I liked for it's simplicity and advertized speed. Theming options were quite diverse and good enough for me.

The next part was hosting. And that was a problem solved long ago by GitHub with [GitHub Pages](https://docs.github.com/en/pages), allowing you to host and serve a static website from a Git based repository. Wait, that's two birds with a single stone. I get to keep my posts in a repository, use the repository as a hosting mechanism, and enjoy the Git flow for my posts. More than two birds!

For publishing, I've opted out to publish using GitHub Action on whenever the `master` branch gets updated. Which is happening when a PR is merged. Because I like feature branches and each post goes through a PR. Just like this one while I'm working on it. And, you get to write as many posts and keep those as drafts, aka draft PRs, until they are ready to be published.

But, Sean, isn't that too manual? Well, writing is manual. And maybe this is not the most sophisticated approach, but it works, it's effective, and it's simple. The older I'm getting the more I appreciate simple things that just work.

The last variable is the domain name. If you want to have a custom domain name, well, you pay for that one and configure it with GitHub pages. Et voila, you've a blog that looks almost professional 😄

With this setup, one can work on posts, preview those before publishing, not worry that one day posts can vanish, and when bored or just have too much time on hands, experiment with themes and features.