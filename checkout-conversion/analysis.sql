-- SQLite syntax. Revenue is gross booked purchase revenue, not profit.
SELECT device, COUNT(*) AS sessions, SUM(checkout_started) AS checkout,
 SUM(shipping_completed) AS shipping, SUM(payment_attempted) AS payment,
 SUM(purchased) AS purchases, ROUND(100.0*SUM(purchased)/COUNT(*),2) AS conversion_pct
FROM sessions GROUP BY device;
SELECT variant, COUNT(*) AS visitors, SUM(purchased) AS purchases,
 1.0*SUM(purchased)/COUNT(*) AS purchase_rate FROM sessions GROUP BY variant;
SELECT month, channel, COUNT(*) AS sessions, SUM(revenue_cad) AS revenue
FROM sessions GROUP BY month, channel;
