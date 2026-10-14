-- Mature cohorts: all opportunities evaluated at a common 90-day horizon.
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
