# Power BI final validation checklist

Source/data validation passed. Native Power BI validation is pending.

1. Extract the whole project ZIP to a short local folder path.
2. Open Banking.pbip in current Power BI Desktop and refresh.
3. Check the unfiltered baseline:
   - Bank revenue: CAD 3,911,430.27
   - Transactions: 250,000
   - Customers: 25,000
   - Active customers: 20,233
   - Inactive rate: 19.068%
   - Digital share: 69.616%
   - Products per customer: 2.8238
4. Inspect all three pages. Check titles, KPI formatting, charts, slicers and cross-filtering.
5. Confirm month selections change transaction/revenue metrics; fixed customer status and portfolio measures remain full-period.
6. Reconcile at least one selected month and segment against the downloadable raw-data analysis. Clear all slicers and verify the baseline returns.
7. Record any refresh, DAX, M or visual errors. Save as PBIX only after resolving them.
8. Export screenshots and retain the Desktop version, validation date, and checked results.

Opening and checking the source JSON does not execute DAX or M. The included validate_source.py independently checks embedded CSVs and references.

Official opening/saving guidance: https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview
