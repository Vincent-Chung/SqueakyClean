# SqueakyClean Examples 📚

This document provides comprehensive examples for using each function in the SqueakyClean library. All examples use the `squeakyclean` import for consistency.

```python
import pandas as pd
import squeakyclean as sc
```

---

## Data Essentials (`squeakyclean.squeakyessentials`)

### ColKeepie - Keep Only Specified Columns

```python
# Sample data with many columns
df = pd.DataFrame({
    'id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'city': ['NYC', 'LA', 'Chicago'],
    'salary': [50000, 60000, 70000],
    'department': ['IT', 'HR', 'Finance']
})

# Keep only essential columns
clean_df = sc.ColKeepie(df, columns=['id', 'name', 'age'])
print(clean_df)
# Result: DataFrame with only id, name, age columns
```

### ColDroppie - Remove Specified Columns

```python
# Remove sensitive or unnecessary columns
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'ssn': ['123-45-6789', '987-65-4321', '555-12-3456'],
    'salary': [50000, 60000, 70000],
    'notes': ['Good employee', 'Needs training', 'Excellent']
})

clean_df = sc.ColDroppie(df, columns=['ssn', 'notes'])
print(clean_df)
# Result: DataFrame without ssn and notes columns
```

### DataTypeSwitcheroo - Convert Column Data Types

```python
# Handle mixed data types and convert to desired types
df = pd.DataFrame({
    'product_id': ['1', '2', '3'],
    'price': ['$29.99', '$49.50', '$19.95'],
    'in_stock': ['True', 'False', 'True'],
    'rating': ['4.5', '3.8', '5.0']
})

# Convert to appropriate types
clean_df = (
    df
    .pipe(sc.DataTypeSwitcheroo, column='product_id', to_type='int')
    .pipe(sc.DataTypeSwitcheroo, column='price', to_type='float')
    .pipe(sc.DataTypeSwitcheroo, column='in_stock', to_type='bool')
    .pipe(sc.DataTypeSwitcheroo, column='rating', to_type='float')
)
print(clean_df.dtypes)
```

### KeepRowsContains / DeleteRowsContains - Filter Rows by Content

```python
# Filter rows based on text content
df = pd.DataFrame({
    'product': ['Widget A', 'Widget B', 'Gadget X', 'Widget C'],
    'status': ['active', 'discontinued', 'active', 'pending'],
    'category': ['electronics', 'electronics', 'tools', 'electronics']
})

# Keep only active products
active_df = sc.KeepRowsContains(df, column='status', value='active')
print(active_df)

# Remove discontinued items
no_discontinued_df = sc.DeleteRowsContains(df, column='status', value='discontinued')
print(no_discontinued_df)
```

---

## Text Processing (`squeakyclean.squeakytext`)

### SubstringLeft / SubstringRight - Extract Text Portions

```python
# Extract parts of strings using delimiters
df = pd.DataFrame({
    'full_name': ['John Doe', 'Jane Smith', 'Bob Johnson'],
    'email': ['john.doe@company.com', 'jane.smith@company.com', 'bob.johnson@company.com']
})

# Get first names
first_names = sc.SubstringLeft(df, 'full_name', ' ')
print(first_names['full_name'])
# Result: ['John', 'Jane', 'Bob']

# Get last names
last_names = sc.SubstringRight(df, 'full_name', ' ')
print(last_names['full_name'])
# Result: ['Doe', 'Smith', 'Johnson']

# Extract domain from email
domains = sc.SubstringRight(df, 'email', '@')
print(domains['email'])
# Result: ['company.com', 'company.com', 'company.com']
```

### SubStringMiddle - Extract Middle Portions of Text

```python
# Extract text between positions
df = pd.DataFrame({
    'phone': ['(555) 123-4567', '(555) 987-6543'],
    'date': ['2023-12-25', '2024-01-15']
})

# Extract area code (characters 2-5)
area_codes = sc.SubStringMiddle(df, 'phone', 2, 5)
print(area_codes['phone'])
# Result: ['555', '555']

# Extract month from date
months = sc.SubStringMiddle(df, 'date', 6, 7)
print(months['date'])
# Result: ['12', '01']
```

### FindReplace - Replace Text Patterns

```python
# Clean and standardize text data
df = pd.DataFrame({
    'address': [
        '123 Main St, Apt 4B',
        '456 Oak Ave, Suite 200',
        '789 Pine Rd, Unit #5'
    ],
    'status': ['Active', 'active', 'ACTIVE']
})

# Standardize abbreviations
clean_addresses = sc.FindReplace(df, 'address', 'St', 'Street')
clean_addresses = sc.FindReplace(clean_addresses, 'address', 'Ave', 'Avenue')
print(clean_addresses['address'])

# Standardize case
standardized_status = sc.FindReplace(df, 'status', 'ACTIVE', 'Active')
standardized_status = sc.FindReplace(standardized_status, 'status', 'active', 'Active')
print(standardized_status['status'])
```

### LeftPadZero - Pad Strings with Leading Zeros

```python
# Format IDs and codes with consistent padding
df = pd.DataFrame({
    'customer_id': [1, 25, 456],
    'product_code': ['A1', 'B25', 'C456']
})

# Pad customer IDs to 4 digits
padded_ids = sc.LeftPadZero(df, 'customer_id', 4)
print(padded_ids['customer_id'])
# Result: ['0001', '0025', '0456']

# Pad product codes to 5 characters
padded_codes = sc.LeftPadZero(df, 'product_code', 5)
print(padded_codes['product_code'])
# Result: ['A1   ', 'B25  ', 'C456 ']  # Note: pads with spaces for strings
```

### SmooshColNames - Clean Column Names

```python
# Standardize column names by removing spaces
df = pd.DataFrame({
    'First Name': ['Alice', 'Bob'],
    'Last Name': ['Smith', 'Jones'],
    'Phone Number': ['555-1234', '555-5678']
})

clean_df = sc.SmooshColNames(df)
print(clean_df.columns)
# Result: ['FirstName', 'LastName', 'PhoneNumber']
```

---

## Time Processing (`squeakyclean.squeakytime`)

### DateExtract - Extract Date Components

```python
# Extract various date components
df = pd.DataFrame({
    'transaction_date': ['20231215', '20240108', '20240220'],
    'event_date': ['2023-12-25', '2024-01-01', '2024-02-14']
})

# Extract months from YYYYMMDD format
months = sc.DateExtract(df, 'month', 'transaction_date', 'month')
print(months['month'])
# Result: [12, 1, 2]

# Extract days
days = sc.DateExtract(df, 'day', 'transaction_date', 'day')
print(days['day'])
# Result: [15, 8, 20]

# Extract day of week (Monday=0, Sunday=6)
weekdays = sc.DateExtract(df, 'day_of_week', 'event_date', 'weekday')
print(weekdays['weekday'])
# Result: [0, 1, 2]  # Monday, Tuesday, Wednesday
```

### CalcDaysSinceX - Calculate Days Since Reference Date

```python
# Calculate days since important dates
df = pd.DataFrame({
    'customer_since': ['2020-01-15', '2019-06-20', '2021-03-10'],
    'last_purchase': ['2024-01-01', '2023-12-15', '2024-02-01']
})

# Days since customer joined
days_customer = sc.CalcDaysSinceX(df, 'customer_since', 'days_as_customer')
print(days_customer['days_as_customer'])

# Days since last purchase
days_since_purchase = sc.CalcDaysSinceX(df, 'last_purchase', 'days_since_purchase')
print(days_since_purchase['days_since_purchase'])
```

### FilterBetweenDates - Filter by Date Ranges

```python
# Filter data within date ranges
df = pd.DataFrame({
    'date': [1.5, 2.5, 3.5, 4.5],
    'start_range': [1.0, 1.0, 1.0, 1.0],
    'end_range': [2.0, 3.0, 4.0, 5.0],
    'value': [100, 200, 300, 400]
})

# Keep only rows where date falls between start and end ranges
filtered_df = sc.FilterBetweenDates(df, 'date', 'start_range', 'end_range')
print(filtered_df)
# Result: Rows where date is between start_range and end_range
```

### CalcDuration - Calculate Duration Between Dates

```python
# Calculate time spans between events
df = pd.DataFrame({
    'start_date': ['20240101', '20240201', '20240301'],
    'end_date': ['20240105', '20240210', '20240315']
})

# Calculate duration in days
duration_df = sc.CalcDuration(df, 'duration_days', 'start_date', 'end_date')
print(duration_df['duration_days'])
# Result: [4, 9, 14]
```

---

## ML Preprocessing (`squeakyclean.squeakyscience`)

### one_hot_encode - Encode Categorical Variables

```python
# Convert categorical columns to one-hot encoded indicators
df = pd.DataFrame({
    'product': ['Widget', 'Gadget', 'Widget', 'Tool'],
    'category': ['A', 'B', 'A', 'C'],
    'price': [10.99, 25.50, 15.75, 8.99]
})

# One-hot encode the category column
encoded_df = sc.one_hot_encode(df, 'category')
print(encoded_df.columns)
# Result: ['product', 'price', 'category_B', 'category_C']  # category_A dropped as reference
```

### tfidf_clusters - Text Feature Engineering

```python
# Transform high-cardinality text columns into cluster features
df = pd.DataFrame({
    'product_name': [
        'Wireless Bluetooth Headphones',
        'Gaming Mechanical Keyboard',
        'Wireless Gaming Mouse',
        'Bluetooth Speaker System',
        'USB-C Charging Cable'
    ],
    'category': ['Electronics', 'Electronics', 'Electronics', 'Electronics', 'Accessories']
})

# Create TF-IDF based clusters for product names
clustered_df = sc.tfidf_clusters(df, 'product_name', 'product_cluster', K=3, KeepPct=0.8)
print(clustered_df[['product_name', 'product_cluster']])
# Result: Products grouped into semantic clusters
```

### calc_quantile - Statistical Transformations

```python
# Add quantile-based features
df = pd.DataFrame({
    'value': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
    'group': ['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C', 'C']
})

# Calculate quantile ranks within groups
quantile_df = sc.calc_quantile(df, 'value', 'value_quantile', Groups=4)
print(quantile_df[['value', 'value_quantile']])
```

### calc_min_max_norm - Feature Scaling

```python
# Scale numerical features to [0,1] range
df = pd.DataFrame({
    'feature1': [10, 20, 30, 40, 50],
    'feature2': [100, 200, 300, 400, 500],
    'category': ['A', 'B', 'A', 'B', 'A']
})

# Normalize feature1
normalized_df = sc.calc_min_max_norm(df, 'feature1', 'feature1_scaled')
print(normalized_df[['feature1', 'feature1_scaled']])
# Result: feature1_scaled ranges from 0 to 1
```

### easy_drop - Automated Column Removal

```python
# Remove problematic columns automatically
df = pd.DataFrame({
    'good_col': [1, 2, 3, 4, 5],
    'mostly_null': [1, None, None, None, None],  # High missing
    'constant': [1, 1, 1, 1, 1],  # No variance
    'sparse': [1, 2, 1, 2, 1],  # Low variance
    'target': ['A', 'B', 'A', 'B', 'A']  # Target column to protect
})

# Remove columns with high missing rates or low variance
clean_df = sc.easy_drop(df, 'target')
print(clean_df.columns)
# Result: Keeps 'good_col' and 'target', removes problematic columns
```

---

## Method Chaining Examples

### Complete Data Cleaning Pipeline

```python
import pandas as pd
import squeakyclean as sc

# Raw, messy data
raw_data = {
    'Customer_ID': ['001', '002', '003', '004'],
    'Full_Name': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown'],
    'Account_Balance': ['$1,250.00', '$3,400.50', 'ERROR', '$750.25'],
    'Signup_Date': ['20230115', '20230220', '20230310', '20230405'],
    'Status': ['Active', 'Active', 'Inactive', 'Active'],
    'Internal_Notes': ['Good customer', 'Prefers email', 'Remove', 'New customer'],
    'Temp_Column': [None, None, None, None]
}

df = pd.DataFrame(raw_data)

# Complete cleaning pipeline
clean_df = (
    df
    # Remove unnecessary columns
    .pipe(sc.ColDroppie, columns=['Temp_Column'])
    # Remove invalid rows
    .pipe(sc.DeleteRowsContains, column='Internal_Notes', value='Remove')
    # Clean and convert data types
    .pipe(sc.DataTypeSwitcheroo, column='Customer_ID', to_type='int')
    .pipe(sc.DataTypeSwitcheroo, column='Account_Balance', to_type='float')
    # Extract date components
    .pipe(sc.DateExtract, ExtractType='month', Col='Signup_Date', ColName='signup_month')
    # Clean text data
    .pipe(sc.SubstringLeft, Col='Full_Name', Delimiter=' ', NewCol='first_name')
    .pipe(sc.SubstringRight, Col='Full_Name', Delimiter=' ', NewCol='last_name')
    # Final column selection
    .pipe(sc.ColKeepie, columns=[
        'Customer_ID', 'first_name', 'last_name',
        'Account_Balance', 'signup_month', 'Status'
    ])
)

print("Final clean dataset:")
print(clean_df)
print(f"\nData types:\n{clean_df.dtypes}")
```

This examples file demonstrates the full range of SqueakyClean's capabilities and shows how functions can be chained together for comprehensive data cleaning workflows.