---
title: Earthly Service Level Agreement
layout: page
---

<link rel="stylesheet" href="/assets/css/subpage.css">

*How to Use*: This Earthly Service Level Agreement (Version 1.0) (“**SLA**”) operates as an Attachment to the Earthly Cloud Terms. To use this SLA, Customer and Provider incorporate this SLA by reference on their Cover Page. The parties may modify any element of this SLA, including the SLA Key Terms Chart (see Section 7 below), by reference on their Cover Page. Capitalized terms not defined in this SLA have the meanings given in the Earthly Cloud Terms.

**1. Service Levels**. Provider will use commercially reasonable efforts to provide the Cloud Service at or above Target Availability. The SLA will only apply to Provider’s “Team” and “Enterprise” tiers. If a lower tier was subscribed to, Provider will use commercially reasonable efforts to make the Cloud Service available for Customer’s use 99% of the time in each month.

**2. Monitoring**. Provider will provide or otherwise make available to Customer, upon request, reports measuring the Monthly Uptime Percentage as against Target Availability.

**3. Service Credits**. If there is a verified failure of the Cloud Service to meet Target Availability in a particular month and Customer makes a request for service credit within 30 days after the end of such month, Customer will be entitled to a Service Credit calculated in accordance with the SLA Key Terms Chart below. Provider will apply each Service Credit to Customer’s next invoice, provided that Customer’s account is fully paid up (without outstanding payment issues or disputes). Customer will receive no refund or other credit for unused Service Credits.

**4. Multiple Failures**. To the extent that the Cloud Service experiences Multiple Failures, then Customer may, upon notice to Provider no more than 30 days after the date the Multiple Failures occurred, terminate the Order for the applicable Cloud Service. In such case Provider will refund to Customer any pre-paid, unused fees for the terminated portion of the Subscription Term.

**5. Exclusive Remedies**. Service Credits constitute liquidated damages and are not a penalty. Service Credits and the Multiple Failures termination right set forth in Section 4 above are Customer’s exclusive remedies, and Provider’s sole liability, for Provider’s failure to meet Target Availability.

**6. Definitions**.

“<ins>Build</ins>” means execution of a CI/CD task on the Cloud Service, whether triggered manually by Users or automatically (including when triggered by an integration with a Third-Party Platform).

“<ins>Compute Minute</ins>” has the definition given on our pricing page at [https://earthly.dev/pricing](https://earthly.dev/pricing).

“<ins>Maintenance</ins>” means Provider’s routine maintenance of the Cloud Service conducted in accordance with its Maintenance Procedures or reasonable emergency maintenance.

“<ins>Maintenance Procedures</ins>” means Provider’s standard Cloud Service maintenance schedule as posted or otherwise made available by Provider upon request by Customer.

“<ins>Monthly Uptime Percentage</ins>” means the number of Builds executed by Customer on the Cloud Service that are not subject to an Outage during a calendar month divided by the total number of Build executed by Customer on the Cloud Service in that calendar month.

“<ins>Multiple Failures</ins>” is defined in the SLA Key Terms Chart.

“<ins>Outage</ins>” means an unplanned interruption or material disruption of the Cloud Service, but excluding unavailability to the extent caused by (a) Customer’s use of the Cloud Service in a manner not authorized in the Agreement or Documentation, (b) general Internet problems, Force Majeure events or other factors outside of Provider’s reasonable control, (c) Customer’s network connections or other infrastructure or (d) Maintenance.

“<ins>Service Credit</ins>” means a credit issued by Provider based on the monthly fees due for the affected Cloud Service in such month.

“<ins>Target Availability</ins>” is defined in the SLA Key Terms Chart.

**7. SLA Key Terms Chart**.

<table class="agreement-table">
  <thead>
    <tr>
      <th colspan="3">SLA Key Terms Chart</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td></td>
      <td><b>Monthly Uptime Percentage:</b></td>
      <td><b>Service Credit:</b></td>
    </tr>
    <tr>
      <td style="width: 18%"><b>Target Availability:</b></td>
      <td style="width: 31%">99% or higher</td>
      <td style="width: 51%">None</td>
    </tr>
    <tr>
      <td>Credit Tier 1</td>
      <td>97% - 98.99%</td>
      <td>5% of monthly recurring fees plus the value of the Compute Minutes applicable to Builds that are subject to an Outage.</td>
    </tr>
    <tr>
      <td>Credit Tier 2</td>
      <td>94% - 96.99%</td>
      <td>20% of monthly recurring fees plus the value of the Compute Minutes applicable to Builds that are subject to an Outage.</td>
    </tr>
    <tr>
      <td>Credit Tier 3</td>
      <td>90% - 93.99%</td>
      <td>35% of monthly recurring fees plus the value of the Compute Minutes applicable to Builds that are subject to an Outage.</td>
    </tr>
    <tr>
      <td>Credit Tier 4</td>
      <td>&lt; 90%</td>
      <td>50% of monthly recurring fees plus the value of the Compute Minutes applicable to Builds that are subject to an Outage.</td>
    </tr>
    <tr>
      <td colspan="3"></td>
    </tr>
    <tr>
      <td><b>Multiple Failures:</b></td>
      <td colspan="2">
        means Target Availability is not met for 2 consecutive months or any 3
        months in a rolling 12-month period.
      </td>
    </tr>
  </tbody>
</table>
