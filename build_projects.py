"""Reproduce two independent synthetic analytics case studies; never employer data."""
from pathlib import Path
import random,csv,json,sqlite3,math,zipfile
from datetime import date,timedelta
from collections import defaultdict
from scipy.stats import norm
ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/'dist'
(OUT/'assets').mkdir(parents=True,exist_ok=True)
rng=random.Random(20261013)
def writecsv(path,rows):
 with path.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def make_dir(name):
 p=ROOT/name;p.mkdir(exist_ok=True);return p
def readme(p,text): (p/'README.md').write_text(text)
def package(p):
 with zipfile.ZipFile(OUT/'assets'/f'{p.name}.zip','w',zipfile.ZIP_DEFLATED) as z:
  for f in p.iterdir():
   if f.is_file():z.write(f,f'{p.name}/{f.name}')
# Independent sessions: each synthetic visitor has exactly one session and one assigned variant.
p=make_dir('checkout-conversion');sessions=[]
for i in range(40000):
 day=date(2026,7,1)+timedelta(days=rng.randrange(92));device=rng.choices(['Mobile','Desktop'],[.67,.33])[0]
 channel=rng.choices(['Organic','Paid search','Email','Social'],[.38,.28,.19,.15])[0]
 variant=rng.choice(['Control','Treatment']);start=int(rng.random() < (.43 if device=='Mobile' else .52))
 shipping=int(start and rng.random()<(.77 if device=='Mobile' else .88))
 payment=int(shipping and rng.random()<(.77 if device=='Mobile' else .90))
 paid=int(payment and rng.random()<(.82 if device=='Mobile' else .94)+( .075 if variant=='Treatment' and device=='Mobile' else 0))
 revenue=round(rng.uniform(45,180),2) if paid else 0
 sessions.append(dict(session_id=f'S{i+1:05}',visitor_id=f'V{i+1:05}',date=day.isoformat(),month=day.strftime('%Y-%m'),device=device,channel=channel,variant=variant,checkout_started=start,shipping_completed=shipping,payment_attempted=payment,purchased=paid,revenue_cad=revenue))
writecsv(p/'sessions.csv',sessions)
qa={'rows':len(sessions),'unique_sessions':len({x['session_id'] for x in sessions}),'unique_visitors':len({x['visitor_id'] for x in sessions}),'funnel_errors':sum(not (x['purchased']<=x['payment_attempted']<=x['shipping_completed']<=x['checkout_started']) for x in sessions),'revenue_errors':sum((x['revenue_cad']>0)!=bool(x['purchased']) for x in sessions)}
assert qa['funnel_errors']==qa['revenue_errors']==0
agg=defaultdict(lambda:[0,0,0,0,0,0.0])
for x in sessions:
 key=(x['month'],x['device'],x['channel'],x['variant']);v=agg[key]
 for j,k in enumerate(['checkout_started','shipping_completed','payment_attempted','purchased','revenue_cad']):v[j+1]+=x[k]
 v[0]+=1
aggregates=[dict(zip(['month','device','channel','variant','sessions','checkout','shipping','payment','purchases','revenue'],[*k,*v])) for k,v in agg.items()]
writecsv(p/'dashboard_aggregates.csv',aggregates)
c=[x for x in sessions if x['variant']=='Control'];t=[x for x in sessions if x['variant']=='Treatment']
pc=sum(x['purchased'] for x in c)/len(c);pt=sum(x['purchased'] for x in t)/len(t);pooled=(sum(x['purchased'] for x in c+t))/(len(c)+len(t));se0=math.sqrt(pooled*(1-pooled)*(1/len(c)+1/len(t)));se=math.sqrt(pc*(1-pc)/len(c)+pt*(1-pt)/len(t));delta=pt-pc
exp={'control_n':len(c),'treatment_n':len(t),'control_rate':pc,'treatment_rate':pt,'absolute_lift':delta,'relative_lift':delta/pc,'ci_low':delta-1.96*se,'ci_high':delta+1.96*se,'p_value':float(2*norm.sf(abs(delta/se0))),'method':'Two-sided pooled two-proportion z test; unpooled normal 95% CI for absolute difference; intention-to-treat across all assigned visitors.'}
(p/'experiment_results.json').write_text(json.dumps(exp,indent=2));(p/'qa_results.json').write_text(json.dumps(qa,indent=2))
(p/'analysis.sql').write_text('''-- SQLite syntax. Revenue is gross booked purchase revenue, not profit.
SELECT device, COUNT(*) AS sessions, SUM(checkout_started) AS checkout,
 SUM(shipping_completed) AS shipping, SUM(payment_attempted) AS payment,
 SUM(purchased) AS purchases, ROUND(100.0*SUM(purchased)/COUNT(*),2) AS conversion_pct
FROM sessions GROUP BY device;
SELECT variant, COUNT(*) AS visitors, SUM(purchased) AS purchases,
 1.0*SUM(purchased)/COUNT(*) AS purchase_rate FROM sessions GROUP BY variant;
SELECT month, channel, COUNT(*) AS sessions, SUM(revenue_cad) AS revenue
FROM sessions GROUP BY month, channel;
''')
con=sqlite3.connect(p/'analysis.sqlite');con.execute('DROP TABLE IF EXISTS sessions');con.execute('CREATE TABLE sessions (session_id TEXT PRIMARY KEY, visitor_id TEXT, date TEXT, month TEXT, device TEXT, channel TEXT, variant TEXT, checkout_started INT, shipping_completed INT, payment_attempted INT, purchased INT, revenue_cad REAL)');con.executemany('INSERT INTO sessions VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',[tuple(x.values()) for x in sessions]);con.commit();con.close()
readme(p,f'''# Checkout & Conversion Analytics
Synthetic independent case study, built October 2026. This is not Shopify data or an employer project.
## Business question
Where does checkout lose customers, and does a simplified mobile payment experience improve purchase conversion?
## Data and definitions
40,000 unique visitors, one session each, July–September 2026. CAD. Session fields: ID, visitor ID, date/month, device, acquisition channel, random Control/Treatment assignment, ordered binary checkout/shipping/payment/purchase indicators and gross purchase revenue. Channel is a synthetic session acquisition label, not causal attribution.
Conversion = purchases / all sessions. Payment success = purchases / payment attempts. AOV = gross purchase revenue / purchases. Treatment changes mobile payment success in the generating process. Variant assignment precedes the funnel; experiment analysis includes all visitors, not only payment attempters.
## Primary experiment result
Control: {pc:.2%}; treatment: {pt:.2%}. Absolute lift: {delta*100:.2f} percentage points; 95% CI [{exp['ci_low']*100:.2f}, {exp['ci_high']*100:.2f}] pp. Two-sided p = {exp['p_value']:.5f}. Primary outcome is purchase conversion; device splits are exploratory. No multiple-testing claims.
## Recommendation
Test payment UX in a real randomized experiment. Measure purchase conversion alongside refund rate, payment latency and margin. Those guardrails are absent from this dataset, so this simulated result does not justify a production launch.
## Method and limitations
A fixed-seed generator creates synthetic friction and treatment effects; the observed lift is a simulation result, not validated business impact. Normal-approximation CI; independent observations; no sequential stopping. No revenue lift confidence interval or causal channel claims.
## Reproduce
Run `python ../build_projects.py` from the source checkout (Python 3 and scipy). The downloadable bundle contains data, SQLite, SQL, aggregates, QA, and experiment results; `generate_and_analyze.py` is a self-contained generator for both projects. SQL can run independently against analysis.sqlite.
## QA
Unique session and visitor IDs, monotone funnel stages, revenue/purchase consistency, and raw-to-aggregate reconciliation are checked. See qa_results.json.
''')
checkout={'rows':aggregates,'experiment':exp,'qa':qa}
# SaaS opportunity acquisition / revenue operations, independent of ecommerce.
p2=make_dir('revenue-operations');opps=[];spend=[]
channels=['Inbound','Paid search','Partner','Outbound']
for month in range(1,10):
 for channel in channels:
  spend.append(dict(month=f'2026-{month:02}',channel=channel,spend_cad= {'Inbound':12000,'Paid search':26000,'Partner':14000,'Outbound':22000}[channel]+rng.randrange(-2000,2000)))
  for j in range(100):
   qualified=int(rng.random()<{'Inbound':.71,'Paid search':.57,'Partner':.80,'Outbound':.48}[channel]);won=int(qualified and rng.random()<{'Inbound':.34,'Paid search':.27,'Partner':.43,'Outbound':.22}[channel]);arr=round(rng.uniform(7000,33000),2) if won else 0
   opps.append(dict(opportunity_id=f'O{len(opps)+1:05}',cohort_month=f'2026-{month:02}',channel=channel,qualified=qualified,won=won,new_arr_cad=arr,owner=f'AE-{rng.randrange(1,9)}',sales_cycle_days=rng.randrange(18,86) if won else '',source_missing=int(rng.random()<.035),owner_missing=int(rng.random()<.02)))
writecsv(p2/'opportunities.csv',opps);writecsv(p2/'channel_spend.csv',spend)
agg2=defaultdict(lambda:[0,0,0,0.0,0,0,0])
for x in opps:
 v=agg2[(x['cohort_month'],x['channel'])];v[0]+=1;v[1]+=x['qualified'];v[2]+=x['won'];v[3]+=x['new_arr_cad'];v[4]+=int(x['sales_cycle_days'] or 0);v[5]+=x['source_missing'];v[6]+=x['owner_missing']
rows2=[dict(zip(['month','channel','opportunities','qualified','wins','arr','cycle_days_sum','source_missing','owner_missing','spend'],[*k,*v,next(x['spend_cad'] for x in spend if (x['month'],x['channel'])==k)])) for k,v in agg2.items()]
writecsv(p2/'dashboard_aggregates.csv',rows2)
qa2={'opportunities':len(opps),'unique_ids':len({x['opportunity_id'] for x in opps}),'invalid_wins':sum(x['won']>x['qualified'] for x in opps),'source_missing':sum(x['source_missing'] for x in opps),'owner_missing':sum(x['owner_missing'] for x in opps)};assert qa2['invalid_wins']==0
(p2/'qa_results.json').write_text(json.dumps(qa2,indent=2))
sql='''-- Mature cohorts: all opportunities evaluated at a common 90-day horizon.
SELECT channel, COUNT(*) AS opportunities, SUM(qualified) AS qualified,
 SUM(won) AS wins, SUM(new_arr_cad) AS new_arr, 1.0*SUM(won)/COUNT(*) AS win_rate,
 SUM(source_missing) AS source_missing, SUM(owner_missing) AS owner_missing
FROM opportunities GROUP BY channel;
-- Aggregate before joining: avoid multiplying monthly channel spend.
WITH performance AS (SELECT cohort_month, channel, SUM(won) wins, SUM(new_arr_cad) arr
 FROM opportunities GROUP BY cohort_month,channel)
SELECT p.*, s.spend_cad, 1.0*s.spend_cad/NULLIF(p.wins,0) AS acquisition_cost_proxy,
 1.0*p.arr/NULLIF(s.spend_cad,0) AS new_arr_per_spend
FROM performance p JOIN channel_spend s ON s.month=p.cohort_month AND s.channel=p.channel;
'''
(p2/'analysis.sql').write_text(sql)
con=sqlite3.connect(p2/'analysis.sqlite');con.execute('DROP TABLE IF EXISTS opportunities');con.execute('DROP TABLE IF EXISTS channel_spend');con.execute('CREATE TABLE opportunities(opportunity_id TEXT PRIMARY KEY,cohort_month TEXT,channel TEXT,qualified INT,won INT,new_arr_cad REAL,owner TEXT,sales_cycle_days INT,source_missing INT,owner_missing INT)');con.executemany('INSERT INTO opportunities VALUES (?,?,?,?,?,?,?,?,?,?)',[tuple(x.values()) for x in opps]);con.execute('CREATE TABLE channel_spend(month TEXT,channel TEXT,spend_cad REAL,PRIMARY KEY(month,channel))');con.executemany('INSERT INTO channel_spend VALUES (?,?,?)',[tuple(x.values()) for x in spend]);con.commit();con.close()
readme(p2,'''# Revenue Operations & Acquisition Efficiency
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
''')
# Add exact generator and requirements to both downloadable bundles.
for folder in [p,p2]:
 (folder/'generate_and_analyze.py').write_text(Path(__file__).read_text())
 (folder/'requirements.txt').write_text('scipy>=1.10\n')
# Self-contained bundles can run from any extraction location: direct output to local artifacts if no Site dist.
# Output dir exists in the original project; extraction users create it automatically via preamble below.
for folder in [p,p2]:package(folder)
(OUT/'checkout-data.json').write_text(json.dumps(checkout));(OUT/'revenue-data.json').write_text(json.dumps({'rows':rows2,'qa':qa2}))
assert sum(x['sessions'] for x in aggregates)==len(sessions)
assert abs(sum(x['revenue'] for x in aggregates)-sum(x['revenue_cad'] for x in sessions))<.01
assert sum(x['opportunities'] for x in rows2)==len(opps)
assert abs(sum(x['arr'] for x in rows2)-sum(x['new_arr_cad'] for x in opps))<.01
print(json.dumps({'checkout':exp,'revenue_qa':qa2},indent=2))
