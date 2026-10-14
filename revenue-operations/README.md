# Revenue Operations & Acquisition Efficiency
Independent synthetic SaaS case study. This is not real Salesforce data or employer work.
## Business question
Which acquisition channels create efficient new recurring revenue, and which CRM quality issues need attention?
## Data and definitions
3,600 unique opportunities, 100 per month/channel, January–September 2026; four channels. Each cohort has a simulated completed 90-day evaluation window. This is a synthetic mature-cohort assumption, not a claim that September outcomes were already observable in October.
Opportunity fields: unique ID, creation cohort month, reference channel, binary qualification/win, booked new annual recurring revenue in CAD, reference owner, winning sales cycle, and missing-source/owner flags. The reference source/owner remain populated as synthetic truth to quantify missing-field flags; this is an audit simulation, not a dirty CRM export.
Channel spend includes synthetic marketing/sales acquisition allocations. Win rate = wins / all opportunities; qualification = qualified / all opportunities. Acquisition cost proxy = allocated spend / wins. New ARR per spend = new booked annual recurring revenue / allocated spend. ARR is neither recognized revenue nor cash collected; this ratio is not ROAS or profit. No expansion/churn/LTV/payback claims.
## Method
Validate keys and stage ordering, aggregate opportunities by cohort/channel, aggregate spend at the same grain, join once, and evaluate volume, win rate, new ARR efficiency, sales cycle and missing-field audit flags. SQL includes a CTE to avoid spend duplication.
## Recommendations
Pilot expansion of efficient channels within capacity limits; monitor volume and sales cycle rather than optimizing a ratio alone. Create mandatory source/owner rules, a weekly exception queue, and a metric dictionary. Verify business definitions with Finance before using ARR reporting.
## Limitations
Channel economics are intentionally generated with different qualification and win probabilities. These differences demonstrate an analysis method and do not prove causal acquisition impact. Mature cohorts are assumed. Allocated spend does not include all company costs. Reference missing-field flags overlap and must not be added to estimate unique affected records.
## Reproduce and artifacts
Python 3 + scipy; run generate_and_analyze.py. CSVs, SQLite, SQL, aggregates and QA accompany this bundle. The same generator rebuilds the checkout project too.
