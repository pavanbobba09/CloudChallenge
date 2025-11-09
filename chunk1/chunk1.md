# Cloud Resume Challenge – Debug Notes

## What I Learned

So I was trying to host my Cloud Resume website on AWS using **S3 + CloudFront + Route 53**, and at first everything looked perfect… but when I opened `https://pavan-cloud.com`, it kept showing:

```
This site can’t be reached  
pavan-cloud.com’s DNS address could not be found.  
DNS_PROBE_POSSIBLE
```

At first, I thought it was something wrong with **CloudFront**, but later I found out the real issue was with **Route 53 and the nameservers**.

---

## The Real Issue

Basically, I had **two different sets of name servers**:

- In the **registered domain** section (under Route 53 → Registered Domains), my nameservers were:
  ```
  ns-1088.awsdns-08.org
  ns-557.awsdns-05.net
  ns-1686.awsdns-18.co.uk
  ns-88.awsdns-11.com
  ```

- But in the **hosted zone**, the nameservers were completely different:
  ```
  ns-707.awsdns-24.net
  ns-1213.awsdns-23.org
  ns-305.awsdns-38.com
  ns-1670.awsdns-16.co.uk
  ```

Because these didn’t match, my domain didn’t know which DNS zone to use, and that’s why it couldn’t resolve to my CloudFront distribution.  
Basically, the domain was pointing to the wrong zone.

---

## How I Fixed It

1. Went to **Route 53 → Registered Domains → pavan-cloud.com**  
2. Edited the **Name Servers** and replaced them with the exact 4 from the hosted zone:  
   ```
   ns-707.awsdns-24.net
   ns-1213.awsdns-23.org
   ns-305.awsdns-38.com
   ns-1670.awsdns-16.co.uk
   ```
3. Waited for around **30–60 minutes** for DNS propagation.
4. Checked propagation using [dnschecker.org](https://dnschecker.org).
5. Once it started resolving, my domain loaded perfectly from CloudFront 🎉

---

## My Key Takeaways

- If the site says “DNS_PROBE_POSSIBLE,” always check if **your domain’s nameservers match your Route 53 hosted zone nameservers**.
- Don’t touch the **SOA record** — AWS manages that automatically.
- Always keep the **S3 bucket private** and let CloudFront fetch data via **Origin Access Control (OAC)**.
- Set your **default root object** in CloudFront to `index.html` so the homepage loads directly.
- Be patient — DNS changes can take up to **24 hours**, but usually work within an hour.

---

## Final Setup

✅ **Architecture**

- **S3 bucket** → stores the static site (private)  
- **CloudFront** → CDN distribution with HTTPS (TLSv1.2_2021)  
- **Route 53** → DNS routing with A/AAAA alias records pointing to CloudFront  
- **ACM Certificate** → issued in `us-east-1` for `pavan-cloud.com`

Everything is now working smoothly 🚀

---

### Quick Note
If you ever face the same issue again, first step → check **nameserver mismatch** between Hosted Zone and Registered Domain.

```
# Always match these values!
Hosted Zone NS = Registered Domain NS
```

---

Author: Sai Pavan Tej Bobba  
Project: AWS Cloud Resume Challenge
