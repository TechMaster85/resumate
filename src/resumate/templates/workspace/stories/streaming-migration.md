---
title: Moving shipment tracking from batch to streaming
when: 2023
where: Lakeshore Logistics
tags: [technical-leadership, distributed-systems, customer-impact, migration]
---

<!-- Example story. Replace it with your own. -->

## Situation
Customers saw shipment updates up to 15 minutes late because tracking ran as a batch
job. Support got ~200 "where is my package" tickets a day, many caused purely by lag.

## What I did
Wrote the design doc proposing Kafka + Flink, and got buy-in by prototyping on one
region's traffic over two weeks. Ran the migration as a shadow pipeline for a month,
diffing outputs nightly, so we could cut over with confidence. Paired with two
engineers new to streaming so the team owned it, not just me.

## Result
Latency went from 15 minutes to 4 seconds. Support tickets about stale tracking fell
by about 70%. The shadow-diff approach became our standard for risky migrations.

## Why it matters to me
I like work where an infrastructure change shows up directly as a better experience
for real people, and I like leaving a team more capable than I found it.
