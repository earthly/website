---
title: Unit Testing vs Integration Testing
date: '2020-12-04 17:16:14'
---

In 1998, Kent Beck wrote sUnit, a unit testing framework for SmallTalk. &nbsp;Beck later ported this framework to Java as jUnit. &nbsp;From there, xUnit frameworks spread to the most popular languages. Newer languages, like Golang and Rust, have incorporated testing into the compiler and standard library directly.

But unit testing is not the only game in town. &nbsp;There are also integration tests and performance tests and much more. &nbsp;In my mind, though, Integration tests and unit tests are the foundations of resilient software. So today let's look at the differences between the two and when you might prefer one or the other.

## What Is a Unit?
<figure class="kg-card kg-image-card kg-card-hascaption"><img src="/content/images/2020/11/Screen-Shot-2020-11-27-at-11.06.16-AM.png" class="kg-image" alt srcset="/content/images/size/w600/2020/11/Screen-Shot-2020-11-27-at-11.06.16-AM.png 600w, /content/images/size/w1000/2020/11/Screen-Shot-2020-11-27-at-11.06.16-AM.png 1000w, /content/images/2020/11/Screen-Shot-2020-11-27-at-11.06.16-AM.png 1034w" sizes="(min-width: 720px) 720px"><figcaption>A unit is the smallest piece of code that is logically separate </figcaption></figure>

A unit test is a test that is testing the smallest possible pieces of code in isolation. What then is a unit? &nbsp;

The term unit comes from mathematics. &nbsp;The number 1 is considered the unit as it is the smallest natural number. &nbsp;It is the smallest positive yet whole number. &nbsp;By analogy, a unit of your source code is the smallest piece of code that is logically separate from the rest of the code. &nbsp;It is a whole piece, a logically distinct area code, and it is the smallest possible such piece.

In most programming languages your unit is going to be a function or method call.

The great thing about unit testing is that if your code is structured in small independent pieces then writing tests for them can be quite easy. &nbsp; This ease of writing means that unit testing can be done as you develop features.

In comparison to other forms of testing, the execution time of unit tests is quite small. This means that you can run unit tests very frequently. &nbsp;As software matures a suite of unit tests is a powerful tool for preventing regressions and easing maintenance costs.

## Retroactive Unit Testing

> When considering an effort to add unit tests to existing software, costs, as well as benefits, need to be considered.

A key assumption of unit testing is that the software under test easily separates into distinct units. &nbsp;In software written without unit testing in mind, this assumption rarely holds. &nbsp;Adding unit tests to existing software is often a great way to stabilize it and prevent future regressions, but refactoring the code to support easy unit testing may require substantial effort and could even introduce new defects. &nbsp;When considering an effort to add unit tests to existing software, costs, as well as benefits, need to be considered. &nbsp;If you have working code, and if the code rarely needs to change, and if the code is not easily unit-testable the benefits may not warrant the costs. In such cases, consider leaning on integration tests to prevent defects in that area.

## What Is an Integration Test?
<figure class="kg-card kg-image-card kg-card-hascaption"><img src="/content/images/2020/11/Screen-Shot-2020-11-27-at-11.40.01-AM.png" class="kg-image" alt srcset="/content/images/size/w600/2020/11/Screen-Shot-2020-11-27-at-11.40.01-AM.png 600w, /content/images/size/w1000/2020/11/Screen-Shot-2020-11-27-at-11.40.01-AM.png 1000w, /content/images/2020/11/Screen-Shot-2020-11-27-at-11.40.01-AM.png 1036w" sizes="(min-width: 720px) 720px"><figcaption>Integration tests focus on the whole of the software stack</figcaption></figure>

If the philosophy of unit testing is based on the insight that testing small independent pieces of code is a great way to prevent regressions then integration tests are based on the understanding that things often go wrong at the edges. &nbsp;The outside world is a messy place, and where it interacts with your code is usually where surprises happen.

You can achieve 100% code coverage with your unit tests but still, find your software fails. &nbsp;You might be trying to read a file from the wrong location, or your software might get unexpected output from a service that calls it or it might call a database in an invalid way.

Whereas unit tests should be quick to run and numerous, a great integration testing strategy should focus on a lesser number of high impact tests.

Those tests should cross all the lines that unit tests won't, writing to the file system, reaching out to external resources, and so on.

## When Integration Testing Gets Tricky

Certain truly external systems may be difficult to integrate into tests. &nbsp;This is because they have side effects in the real world that cannot be undone: &nbsp;A financial transaction, an email send, physically moving a paint robot. Before you give up and sidestep them in your testing, look around for solutions. &nbsp;

Many external systems will have a documented way to use them in an integration test. Payment processors often have test credit card numbers, and test users with test email accounts can be set up for testing delivery. &nbsp;

The closer integration tests are to real-world interactions the more likely they are to catch problems and provide real value.

<!--kg-card-begin: html-->

| Service | Integration Test Strategy |
| --- | --- |
| Amazon SES | [Test email addresses](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/send-email-simulator.html) |
| Paypal | [Test credit card numbers](https://developer.paypal.com/docs/payflow/payflow-pro/payflow-pro-testing/) |
| UPS | [Test api mode](https://www.ups.com/us/en/help-center/sri/developer-instruct.page) |

<!--kg-card-end: html-->
# An E-commerce Example

Imagine you are coding a simple e-commerce site, a simple miniature amazon.com. The details matter here so let's assume that you are going to use PostgreSQL as your datastore, PayPal for payments, UPS for shipping, and Amazon Simple Email Service for emailing invoices. &nbsp;

### Unit Testing:

Your unit testing strategy will be testing the logic of your application, in an isolated fashion. &nbsp;This may include:

- Testing that the tax calculating logic correctly calculates the taxes for various jurisdictions. &nbsp; 
- Testing that items placed into a cart data structure are correctly added up.
- Testing that discount codes are properly applied.

Each of these areas will likely have several tests. Each test will verify a small piece of functionality. Unit testing power comes from their number, simplicity, and their speed and ease of execution.

### Integration Testing:

Your integration testing on the other hand will focus on testing where your e-commerce code interacts with other systems. &nbsp;This means testing not just the integration with the data store but also with email sending services, payment services and more. These may include:

- Testing that the shipping rates can be retrieved from the external shipping service.
- Testing that the invoices can be generated and properly sent out.
- Testing that the order information can be persisted and properly retrieved from the datastore.
- Testing that the transactions can be sent and properly processed from the payment processor.

Each of these will likely be verified by one or two integration tests. These tests will be slower to run and probably involve some setup and teardown steps. &nbsp;The payoff is that the code coverage of each test will be quite large. &nbsp;These tests will generate value by catching problems that unit tests could never catch. &nbsp;However, the maintenance cost and execution time will be likely higher.

# Integration Tests vs Unit Tests
<figure class="kg-card kg-image-card kg-card-hascaption"><img src="/content/images/2020/11/Screen-Shot-2020-11-27-at-11.44.36-AM-1.png" class="kg-image" alt srcset="/content/images/size/w600/2020/11/Screen-Shot-2020-11-27-at-11.44.36-AM-1.png 600w, /content/images/size/w1000/2020/11/Screen-Shot-2020-11-27-at-11.44.36-AM-1.png 1000w, /content/images/size/w1600/2020/11/Screen-Shot-2020-11-27-at-11.44.36-AM-1.png 1600w, /content/images/2020/11/Screen-Shot-2020-11-27-at-11.44.36-AM-1.png 2020w" sizes="(min-width: 720px) 720px"><figcaption>Time for a head to head comparison</figcaption></figure>

So which type of test should be preferred? Neither alone is sufficient. &nbsp; Both are parts of a comprehensive testing plan. Let's compare them directly:

<!--kg-card-begin: html-->

| Unit Tests | Integration Tests |
| --- | --- |
| The goal is to make sure a peice of code works as expected | The goal is to make sure pieces of code, including external interfaces work together, as expected |
| Isolated | Integrated |
| Quick to run | Slower to run |
| Many in number | Fewer in number |
| No access to file system, database or external services | Directly testing areas where software interacts with external systems |
| Tests a single piece of functionality | Tests the interaction of several peices of functionality |
| Minimal setup and teardown | May involve extensive setup and teardown of external resources like file systems of database state |
| Stateless | Possibly Stateful |

<!--kg-card-end: html-->
## Working Software Over Idealized Testing

> Each situation is unique and advice that is written based on what works in other contexts should be not followed blindly.

Now we understand that unit tests should not touch the file system and that integration tests should only integrate across loose components. But really, splitting testing into two clear-cut categories is a bit reductionist and if we focus only on the definition we lose sight of the goal, which is correct working software.

Some very thoughtful developers think [unit tests can and should round trip to the database](https://dhh.dk/2014/tdd-is-dead-long-live-testing.html). Others claim that unit tests are a wasted effort and coarse grain integration tests offer the most value.

The thing is that each situation is unique and advice that is written based on what works in other contexts should be not followed blindly. A question to keep in mind is what kind of defects would this test catch. If each test is written thoughtfully to improve software reliability, and if tests are removed when they no longer have value then the specific testing approach that delivers the most value for a particular project will be discovered over time.

## See Also

- [You are using Docker Compose wrong](/youre-using-docker-compose-wrong/)
- [Integration testing guide](https://docs.earthly.dev/guides/integration)
- [Making Integration tests less flaky](https://dev.to/adamgordonbell/how-to-make-integration-tests-less-flaky-bel)
