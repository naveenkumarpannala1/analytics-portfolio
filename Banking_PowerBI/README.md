# Banking Customer Intelligence - Power BI Project
Status: opened and refreshed in Power BI Desktop 2.151.1182.0 on October 14, 2026. Seven native DAX baseline checks passed, all three pages rendered, and selected month/segment filters were verified. A PBIX copy was saved. See NATIVE_VALIDATION.md for scope and download.
## Open and review
1. Extract the entire ZIP on a Windows computer with current Power BI Desktop.
2. Open Banking.pbip (or Banking.Report/definition.pbir).
3. Refresh to load embedded synthetic CSVs; no local file paths or credentials are needed.
4. Confirm baseline values: $3,911,430.27 bank revenue, 250,000 transactions, 25,000 customers, 20,233 active customers, 19.068% inactive, 69.616% digital share, 2.8238 products/customer.
5. Review all three pages, slicers and cross-filtering. Format titles/colors if Desktop applies its default theme. Save as .pbix after validation.
## Model
Transactions fact -> Customers, Products, Channels, Calendar. Accounts -> Customers and Products. One-way dimension-to-fact filters. There is no fact-to-fact relationship. Six import tables, six relationships, eleven DAX measures, three report pages, six charts/tables, twelve KPI cards and six slicers.
CSV snapshots are compressed and embedded in M expressions for portability. They are synthetic and frozen. Power Query converts types with en-CA locale.
## Interpretation
Active/inactive customer status is fixed as of August 31, 2026. Calendar selection filters transactions only; fixed customer-status and account-portfolio measures do not become monthly churn or retention rates. Product/channel filters do not back-filter the customer dimension. Portfolio-customer and transacting-customer denominators are distinct. Cross-product customer counts are not additive. No real financial institution performance is represented.
## Validation limits
JSON schemas and reference integrity are checked. Raw-data KPI reconciliation is checked independently. Native M refresh, selected DAX checks, and page rendering have been performed in Desktop. See NATIVE_VALIDATION.md for the documented scope.
## Official format references
https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview
https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-report
https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-dataset