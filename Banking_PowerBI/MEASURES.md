# DAX measures

## Total Bank Revenue
```dax
SUM(Transactions[bank_revenue])
```

## Transactions
```dax
COUNTROWS(Transactions)
```

## Total Customers
```dax
COUNTROWS(Customers)
```

## Active Customers As Of Aug 31
```dax
CALCULATE(COUNTROWS(Customers), Customers[customer_status] = "Active")
```

## Inactive Rate As Of Aug 31
```dax
DIVIDE(CALCULATE(COUNTROWS(Customers), Customers[customer_status] = "Inactive"), [Total Customers])
```

## Digital Transaction Share
```dax
DIVIDE(CALCULATE(COUNTROWS(Transactions), Transactions[is_digital] = 1), [Transactions])
```

## Bank Revenue Per Portfolio Customer
```dax
DIVIDE([Total Bank Revenue], [Total Customers])
```

## Transacting Customers
```dax
DISTINCTCOUNT(Transactions[customer_id])
```

## Bank Revenue Per Transacting Customer
```dax
DIVIDE([Total Bank Revenue], [Transacting Customers])
```

## Products Per Customer
```dax
DIVIDE(COUNTROWS(Accounts), [Total Customers])
```

## Revenue Share Within Selection
```dax
DIVIDE([Total Bank Revenue], CALCULATE([Total Bank Revenue], ALLSELECTED(Products[product_name])))
```

