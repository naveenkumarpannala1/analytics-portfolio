# Checkout & Conversion Analytics
Synthetic independent case study, built October 2026. This is not Shopify data or an employer project.
## Business question
Where does checkout lose customers, and does a simplified mobile payment experience improve purchase conversion?
## Data and definitions
40,000 unique visitors, one session each, July–September 2026. CAD. Session fields: ID, visitor ID, date/month, device, acquisition channel, random Control/Treatment assignment, ordered binary checkout/shipping/payment/purchase indicators and gross purchase revenue. Channel is a synthetic session acquisition label, not causal attribution.
Conversion = purchases / all sessions. Payment success = purchases / payment attempts. AOV = gross purchase revenue / purchases. Treatment changes mobile payment success in the generating process. Variant assignment precedes the funnel; experiment analysis includes all visitors, not only payment attempters.
## Primary experiment result
Control: 26.81%; treatment: 27.87%. Absolute lift: 1.06 percentage points; 95% CI [0.19, 1.94] pp. Two-sided p = 0.01690. Primary outcome is purchase conversion; device splits are exploratory. No multiple-testing claims.
## Recommendation
Test payment UX in a real randomized experiment. Measure purchase conversion alongside refund rate, payment latency and margin. Those guardrails are absent from this dataset, so this simulated result does not justify a production launch.
## Method and limitations
A fixed-seed generator creates synthetic friction and treatment effects; the observed lift is a simulation result, not validated business impact. Normal-approximation CI; independent observations; no sequential stopping. No revenue lift confidence interval or causal channel claims.
## Reproduce
Run `python ../build_projects.py` from the source checkout (Python 3 and scipy). The downloadable bundle contains data, SQLite, SQL, aggregates, QA, and experiment results; `generate_and_analyze.py` is a self-contained generator for both projects. SQL can run independently against analysis.sqlite.
## QA
Unique session and visitor IDs, monotone funnel stages, revenue/purchase consistency, and raw-to-aggregate reconciliation are checked. See qa_results.json.
