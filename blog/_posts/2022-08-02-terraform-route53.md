---
title: "Terraform Route53 And DNS Fun"
categories:
  - Tutorials
toc: true
author: Adam

internal-links:
 - just an example
---
### Writing Article Checklist

- [ ] Write Outline
- [ ] Write Draft
- [ ] Fix Grammarly Errors
- [ ] Read out loud
- [ ] Write 5 or more titles and pick the best on
- [ ] First two paragraphs: What's it about? Why listen to you?
- [ ] Create header image in Canva
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
- [ ] Run mark down linter (`lint`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `link-opp` and find 1-5 places to incorporate links to other articles
- [ ] Add Earthly `CTA` at bottom `{% include cta/cta1.html %}`
- [ ] Raise PR

## Outside Article Checklist

- [ ] Add in Author page
- [ ] Create header image in Canva
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
  - Would any images look better `wide` or without the `figcaption`?
- [ ] Run mark down linter (`lint`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `link-opp` and find 1-5 places to incorporate links
- [ ] Add Earthly `CTA` at bottom `{% include cta/cta1.html %}`

In my previous article [about terraform]() I moved my lambda and all related infrastructure to Terraform. I even tested things by destroying everything and then recreating it. 

Imagine my surprise then, when several days later I got this.

```
curl https://earthly-tools.com/text-mode
curl: (6) Could not resolve host: earthly-tools.com
```

**In this post, I'll show you how I fixed this and got my DNS records from AWS's Route53 into terraform.**


## The Problem

So, I had a working lambda that was getting all requests to earthly-tools.com, but then it stopped working. What was going on? 

First, lets check see what dig says:

```
dig earthly-tools.com

;; QUESTION SECTION:
;earthly-tools.com.		IN	A

```

Dig is missing the IPs for the A record of my domain name. Here is what a DIG response should look like:
```
dig google.com 
;; QUESTION SECTION:
;google.com.                    IN      A

;; ANSWER SECTION:
google.com.             210     IN      A       172.217.1.14
```

I can also use [dnschecker](https://dnschecker.org/) to validate that something is wrong:

{% picture {{site.pimages}}{{page.slug}}/3010.png --alt {{ No A Record Found  }} %}

This is strange, because if I look in AWS, under Route53, I can see the A record is setup to point to my HTTP API.

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/8850.png --alt {{ Route 53 A Record }} %}
<figcaption>Route 53 A Record</figcaption>
</div>

But here lies the problem. The A value of DNS record points to an API Gateway domain name, but not the one I have setup in AWS.

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/8850.png --alt {{  }} %}
<figcaption>API Gateway doesn't match DNS</figcaption>
</div>

The problem is when I tore down my API gateway, I left a dangling DNS record pointing to a no longer existent API Gateway endpoint. The interesting thing is it kept working for a while. Both the new value and the old must resolve to the same IP, and with all the caching that happens in DNS things just kept working for a while.

So the solution is simple, I need to pull my DNS records into Terraform, so that when I make changes to my HTTP API my DNS records also get updated.

## Terraform Import

Bring in the zone:
```
terraform import aws_route53_zone.primary Z0907636HDO135DJDT7G
```

Bring in the record
```
terraform import aws_route53_record.A Z0907636HDO135DJDT7G_earthly-tools.com_A
```




```
Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # aws_route53_record.A will be created
  + resource "aws_route53_record" "A" {
      + allow_overwrite = (known after apply)
      + fqdn            = (known after apply)
      + id              = (known after apply)
      + name            = "earthly-tools.com"
      + type            = "A"
      + zone_id         = "Z0907636HDO135DJDT7G"

      + alias {
          + evaluate_target_health = true
          + name                   = "d-i2cdn11lkf.execute-api.us-east-1.amazonaws.com"
          + zone_id                = "Z1UJRXOUMOOFQ8"
        }
    }

Plan: 1 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

aws_route53_record.A: Creating...
aws_route53_record.A: Still creating... [10s elapsed]
aws_route53_record.A: Still creating... [20s elapsed]
aws_route53_record.A: Still creating... [30s elapsed]
aws_route53_record.A: Creation complete after 38s [id=Z0907636HDO135DJDT7G_earthly-tools.com_A]

Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
```

And now everything is working.

Commit is here:
https://github.com/adamgordonbell/cloudservices/commit/e213af302cf6372aca4c099419bc6d2a0896ae7a
