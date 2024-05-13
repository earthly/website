---
title: "Terraform Route53 And DNS Fun"
categories:
  - Tutorials
author: Adam
internal-links:
 - terraform route53
 - aws route53
 - route53
excerpt: |
    Learn how to fix DNS issues and import DNS records from AWS's Route53 into Terraform in this informative article by Adam. Discover the steps he took to update his HTTP API and ensure that his DNS records were updated as well.
last_modified_at: 2023-07-14
---
**Uncover the essentials of a Terraform DNS fix in this article. Earthly ensures your infrastructure builds match the reliability of your application builds. [Learn more about Earthly](https://cloud.earthly.dev/login).**

In my previous article [about terraform](/blog/terraform-lambda/) I moved my lambda and all related infrastructure to Terraform. I even tested things by destroying everything and then recreating it.

Imagine my surprise then, when several days later I got this.

~~~{.bash caption=">_"}
$ curl https://earthly-tools.com/text-mode
~~~

~~~{.merge-code}
curl: (6) Could not resolve host: earthly-tools.com
~~~

**In this post, I'll show you how I fixed this and got my DNS records from AWS's Route53 into terraform.**

## The Problem

So, I had a working lambda that was getting all requests to earthly-tools.com, but then it stopped working. What was going on?

First, lets check and see what dig says:

~~~{.bash caption=">_"}
$ dig earthly-tools.com
~~~

~~~{.merge-code}
;; QUESTION SECTION:
;earthly-tools.com.        IN    A

~~~

Dig is missing the IPs for the A record of my domain name. Here is what a DIG response should look like:

~~~{.bash caption=">_"}
$ dig google.com 
~~~

~~~{.merge-code}
;; QUESTION SECTION:
;google.com.                    IN      A

;; ANSWER SECTION:
google.com.             210     IN      A       172.217.1.14
~~~

I can also use [`dnschecker.org`](https://dnschecker.org/) to validate that something is wrong:

{% picture {{site.pimages}}{{page.slug}}/3010.png --alt {{ No A Record Found }} %}

This is strange, because if I look in AWS, under Route53, I can see the A record is setup to point to my HTTP API.

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/8850.png --alt {{ Route 53 A Record }} %}
<figcaption>Route 53 A Record</figcaption>
</div>

But here lies the problem. The A value of DNS record points to an API Gateway domain name, but not the one I have setup in AWS.

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/3610.png --alt {{ API Gateway doesn't match DNS }} %}
<figcaption>API Gateway doesn't match DNS</figcaption>
</div>

The problem is when I tore down my API gateway, I left a dangling DNS record pointing to a non-existent API Gateway endpoint. The surprising thing is it kept working for a while. Both the new value and the old must resolve to the same IP, and with all the caching that happens in DNS things just kept working for a while.

So the solution is simple, I need to pull my DNS records into Terraform, so that when I make changes to my HTTP API my DNS records also get updated.

## Terraform Import

First thing I do is define my zone resource:

~~~{.groovy}
resource "aws_route53_zone" "primary" {
 name = "earthly-tools.com" 
}
~~~

The I import the existing zone:

~~~{.bash caption=">_"}
$ terraform import aws_route53_zone.primary Z0907636HDO135DJDT7G
~~~

With the zone in place, I can create the resource for my A record:

~~~{.groovy}
resource "aws_route53_record" "A" {
    name    = "earthly-tools.com"
    type    = "A"
    zone_id = aws_route53_zone.primary.id
}
~~~

And then I import it.

~~~{.bash caption=">_"}

$ terraform import aws_route53_record.A Z0907636HDO135DJDT7G_earthly-tools.com_A
~~~

Then, I need to configure it to point to the domain name and zone of my API gateway. To do that I add in an alias property.

~~~{.diff}
 resource "aws_route53_record" "A" {
     name    = "earthly-tools.com"
     type    = "A"
     zone_id = aws_route53_zone.primary.id
 
+    alias {
+        evaluate_target_health = true
+        name                   = aws_api_gateway_domain_name.earthly-tools-com.regional_domain_name
+        zone_id                = aws_api_gateway_domain_name.earthly-tools-com.regional_zone_id
+    }
 }
~~~

And with that in place, I can just apply everything.

~~~{.bash caption=">_"}
$ terraform apply

~~~

~~~{.ini .merge-code caption=""}
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
~~~

And now everything is working.

~~~{.bash caption=">_"}
$ curl https://earthly-tools.com/text-mode

~~~

~~~{.ini .merge-code caption=""}
Earthly.dev Presents:                                                                                              

  _____                 _       
 |_   _|   ___  __  __ | |_     
   | |    / _ \ \ \/ / | __|    
   | |   |  __/  >  <  | |_     
   |_|    \___| /_/\_\  \__|    
                                
  __  __               _        
 |  \/  |   ___     __| |   ___ 
 | |\/| |  / _ \   / _` |  / _ \
 | |  | | | (_) | | (_| | |  __/
 |_|  |_|  \___/   \__,_|  \___|
~~~

The code is on [GitHub](https://github.com/earthly/cloud-services-example/commit/e213af302cf6372aca4c099419bc6d2a0896ae7a)

{% include_html cta/bottom-cta.html %}
