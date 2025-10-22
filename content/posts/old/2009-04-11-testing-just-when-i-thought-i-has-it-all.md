---
title: Testing - Just When I Thought I Had It All
slug: testing-just-when-i-thought-i-has-it-all
date: '2009-04-11T08:07:00'
updated: '2009-04-11T08:07:00'
draft: false
tags:
- Agile
author: Sean Feldman
---


Testing is normally divided into unit testing and integration testing. Is it?

The current project I am involved in has gone through some very interesting turns. I was privileged to get into some really interesting debates and get exposed to different approaches that might not always can agree with, but definitely contribute to my better understanding of testing in general. Testing, one word so many meanings...

Do you write tests to guard against unexpected changes in your code? Or do you write the tests to validate assumptions? Maybe you do it to drive out the design and implementation? Or you testing how components work together when they actually put together? If you do one of those, you do testing. Then the question comes - is that enough or  should all of the mentioned be done plus more? Well, this is the reason I decided to blog about the subject.

My initial attempts to write tests were lack of satisfaction with the way I created code, the guts feeling that there must be a better way. I want to know that 2+2 is actually 4, and when it's replaced by x and y the result is what it should be. Later I liked the power of being able to validate interactions between the components without having the whole shebang up and running. Mocking it is called. Along combined with state based testing it felt good. It felt right, but still something was missing. The missing part was the clarity - I needed to understand what is happening with the tests, and that's why I loved the AAA syntax showed to me down the road and specification based testing. From that moment it became an infection that spread all over the brain and it was irreversible. And I am glad it was like that.

But a few project have showed that it still did not bring me the complete satisfaction and confidence in the code. This is were pain for integration was a clear sign. The last project has proved that the ration between so called "unit" testing (specifications) and automated integration testing should be about 50% to 50%. I know it sounds extreme, but imagine this: a component A that has a dependency on a component B. For specifications and design drive B can be mocked and everything is great. The key assumptions is that if B is tested and passes, there's no point of re-testing it along with A, as in A's tests we are only interested to exercise A's stuff. But are we? Well, partially true. For design and implementation purposes, yes. B should and will be mocked out. But right after that should come an integration test, where the real A and B both are used. That will ensure that the design secured by specification tests is implemented the way integration tests are using it. This is the total coverage.

So integration tests are required and team buys into that, but what will be an automated integration testing? This is what it is defined:

1. Touching DB

2. Going over a wire

3. Touching file system

4. Performing anything that is not in memory

Do I agree with the traditional definitions? Nope!

Doing anything that will cause more than a single component to execute it's production code with a purpose of getting the result anticipated from a production code - to me is an integration test. It can be all in memory, it can touch the DB, it can do whatever is necessary to make sure that production code will stand the expectations. And we can always optimize things, right? Locally cloned DB, emulating file system, instantiating multiple objects to work against. It is all good.

So if you do tests, keep in mind the importance of integration testing. Do not let it go invisible just because specifications are in place and make you feel comfy. Remember 50%/50%, or would it be more 100% to 100% - you own call, as long as you can live with it.


