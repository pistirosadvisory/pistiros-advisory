# Data centres and AI compute in Bulgaria: power, chips and security

Summary: Bulgaria is trying to move from software outsourcing into hosting and running compute itself. A European AI factory is planned in Sofia, a global data-centre operator has entered the market, and cheap midday solar power is in surplus. The constraints are chip-export rules, power and grid limits, and a physical-security environment that has become less forgiving.
Published: October 2026
Date: 2026-10-25
Category: sectors

## What is being built

- **The BRAIN++ AI factory.** Bulgaria won EU funding of up to €90 million for one of the first European "AI factories", at Sofia Tech Park with the INSAIT research institute, with about half the money from the national budget. It builds on the Discoverer supercomputer with an upgrade, Discoverer++, using Nvidia H200 accelerators. Construction was due to begin in 2026, offering compute to public bodies, universities and companies, and training for small firms ([Capital](https://www.capital.bg/en/economy/2025/03/20/4758056_brain_and_bulgarias_bid_for_ai_relevancy/)).
- **Commercial colocation.** In 2026 US-based Digital Realty acquired Telepoint, a Bulgarian operator with carrier-neutral facilities in Sofia and a site in Montana, giving combined capacity of about 14.8 MW across about 9,000 m² ([DCD](https://www.datacenterdynamics.com/en/news/digital-realty-acquires-bulgarian-data-center-operator-telepoint/)). This is small by Western European standards but marks the entry of a global operator.
- **Network infrastructure.** In 2024 Exa Infrastructure acquired the Bulgarian telecoms operator GCN, reinforcing Sofia's role as a regional interconnection point ([DCD](https://www.datacenterdynamics.com/en/tags/sofia/)).

## The case for Bulgaria

- **Power.** Bulgaria has nuclear baseload at Kozloduy, more than 6 GW of solar and the EU's highest share of battery storage relative to generation, with midday surpluses that push prices below zero. Over 1 TWh of solar was wasted in 2025 for lack of storage ([IENE](https://www.iene.eu/energy-news/bulgaria-emerges-as-eu-leader-in-electricity-storage-p8681.html)). Large, flexible loads such as data centres could absorb it.
- **Talent.** An established software industry and research institutes.
- **Cost.** Land, construction and labour below Western European levels.
- **Location.** EU and euro membership, with connectivity towards Turkey, Greece and the Black Sea.

## The constraints

- **Chips.** The US "AI diffusion" rule announced in January 2025 would have placed Bulgaria among EU states with capped access to the most advanced accelerators. BRAIN++ was planned under that uncertainty ([Capital](https://www.capital.bg/en/economy/2025/03/20/4758056_brain_and_bulgarias_bid_for_ai_relevancy/)). The rule was rescinded in May 2025 before it took effect, but US policy on advanced-chip exports keeps changing, so check the current rules before planning large GPU deployments.
- **Power density.** AI racks run far above traditional data-centre loads; a Discoverer rack is approaching 90 kW. That needs grid connections, cooling and redundancy that most existing sites lack.
- **Grid.** Connection queues, congested interconnectors and pumped storage offline until at least 2027 limit what can be built quickly.
- **Physical security.** On 9 October 2026, Starlink antennas outside Sofia were set on fire in a planned attack; prosecutors charged two German citizens in absentia and a Sofia court approved European arrest warrants ([AP via NY1](https://ny1.com/nyc/all-boroughs/ap-top-news/2026/10/19/bulgarian-authorities-seek-arrests-germans-in-arson-of-starlink-antennas)). Bulgarian authorities have not publicly attributed motive, but similar attacks in Poland and Lithuania have been linked by those countries to Russia. Critical digital infrastructure in Bulgaria should plan for sabotage risk.

## Compliance points

- **Export controls on compute.** Advanced chips, and some high-performance computing services, are subject to US and EU export rules. A Bulgarian facility serving customers outside the EU must screen who uses the compute.
- **Know-your-customer.** Cloud and colocation providers can be used to train or run models for sanctioned or restricted users. Screening is expected.
- **Data protection and NIS2.** EU cybersecurity rules for essential and important entities, including data-centre providers, impose security and incident-reporting duties.
- **Ownership.** Investors from outside the EU in data centres and telecoms may trigger Bulgaria's investment screening regime.

## What this means for buyers and investors

- If you place workloads in Bulgaria, who owns the facility, and does it meet your security and resilience standards?
- Can the site deliver the power density and redundancy your workloads need?
- If you deploy advanced GPUs, have you checked current US chip-export rules for Bulgaria?
- Does the provider screen its customers for export-control and sanctions risk?
- Does a non-EU investment in the facility need screening approval?

We do not give legal or investment advice. Export-control and security questions belong with qualified advisers.

Related notes: [Energy: nuclear new-build and the solar boom](insight-bulgaria-energy-nuclear-and-solar.html); [Software and IT in Bulgaria](insight-bulgaria-fast-growing-sector.html); [Chinese investment in Bulgaria and how screening works](insight-chinese-investment-and-fdi-screening.html).

## Sources

- [https://www.capital.bg/en/economy/2025/03/20/4758056_brain_and_bulgarias_bid_for_ai_relevancy/](https://www.capital.bg/en/economy/2025/03/20/4758056_brain_and_bulgarias_bid_for_ai_relevancy/)
- [https://www.datacenterdynamics.com/en/news/digital-realty-acquires-bulgarian-data-center-operator-telepoint/](https://www.datacenterdynamics.com/en/news/digital-realty-acquires-bulgarian-data-center-operator-telepoint/)
- [https://www.datacenterdynamics.com/en/tags/sofia/](https://www.datacenterdynamics.com/en/tags/sofia/)
- [https://www.iene.eu/energy-news/bulgaria-emerges-as-eu-leader-in-electricity-storage-p8681.html](https://www.iene.eu/energy-news/bulgaria-emerges-as-eu-leader-in-electricity-storage-p8681.html)
- [https://ny1.com/nyc/all-boroughs/ap-top-news/2026/10/19/bulgarian-authorities-seek-arrests-germans-in-arson-of-starlink-antennas](https://ny1.com/nyc/all-boroughs/ap-top-news/2026/10/19/bulgarian-authorities-seek-arrests-germans-in-arson-of-starlink-antennas)
