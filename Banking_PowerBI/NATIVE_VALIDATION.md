# Native Power BI validation

Validation date: October 14, 2026. Power BI Desktop 2.151.1182.0. No service sign-in was used.

Passed:
- M refresh loaded 250,000 transactions, 25,000 customers, 8 products, 70,595 accounts, 5 channels, and 974 calendar rows.
- Native DAX baseline pass/fail query returned PASS for bank revenue CAD 3,911,430.27, transactions 250,000, customers 25,000, active customers 20,233, inactive rate 0.19068, digital share 0.69616, and products per customer 2.8238.
- Executive, customer value, and products/digital pages rendered charts and cards without visible errors.
- January 2024 slicer returned 3,182 transactions, 59.7% displayed digital share, and approximately CAD 35K revenue (source: CAD 35,437). Fixed customer-status card remained unchanged.
- Affluent segment returned 4,195 customers and CAD 255.35 revenue per portfolio customer.
- Selections were cleared and the baseline restored. Saved Naveenkumar_Pannala_Banking_Analytics.pbix with the Executive page active.

Scope: selected baseline and filter checks, not exhaustive testing of every slicer combination, cross-highlighting interaction, or future Desktop version. All data is synthetic.

The included validation_results.json documents the exact checks and PBIX checksum. Screenshots and the PBIX are available from the live banking case study.

Download PBIX: https://naveen-analytics-portfolio.ochreiris32.chatgpt.site/assets/Naveenkumar_Pannala_Banking_Analytics.pbix