import pandas as pd
import csv 

# TODO:
#  2 columns - In hour total, out hour total
#  2 columns - % in vs % out split
#  3 columns * 2 - min, max, avg of in and out data


# Total number of columns to be read.
no_of_cols = 56

# Read the data needed for the calculations into the data frame.
df = pd.read_csv('Meter Sequential - Variable Length - CSV kWh - Electricity - Anchor Boulevard - 230608.csv', skiprows=7, usecols=[i for i in range(no_of_cols)])

# Read all the extra data needed for the final CSV file.
df_with_extra_data= pd.read_csv('Meter Sequential - Variable Length - CSV kWh - Electricity - Anchor Boulevard - 230608.csv', header=None, nrows=6, names=range(2))

# IN_TIME and OUT_TIME variables should be configureable by the end users as needed.
IN_TIME = '08:00'
OUT_TIME = '17:00'

# Text based columns to be ommitted form the df to be merged once calculations are completed.
omitted_columns =[0,1,2,3,4,5,6,7]
omitted_df = df[df.columns[omitted_columns]]

# extract only columns with relavent data for the calculations.
df = df.iloc[:-1, 8:57]

# Get all the columns within the given time range.
columns = df.columns[(df.columns >=IN_TIME) & (df.columns <= OUT_TIME)]

# Get all the columns outside the given time range.
columns_out = df.columns[(df.columns <IN_TIME) | (df.columns > OUT_TIME)]

# Compute the sum for each row within the time range.
df['SumOutsideRange'] = df[columns].sum(axis=1)

# Compute the sum for each row outside the time range.
df['SumWithinRange'] = df[columns_out].sum(axis=1)

# Calculate percentages based on the sums and total time
df['PercentageWithinRange'] = (df['SumWithinRange'] / df.sum(axis=1)) * 100
df['PercentageOutsideRange'] = (df['SumOutsideRange'] / df.sum(axis=1)) * 100

# Calculate statistics for columns within the range.
df['Min_within_range'] = df[columns].min(axis=1)
df['Max_within_range'] = df[columns].max(axis=1)
df['Avg_within_range'] = df[columns].mean(axis=1)

# Calculate statistics for columns outside the range.
df['Min_outside_range'] = df[columns_out].min(axis=1)
df['Max_outside_range'] = df[columns_out].max(axis=1)
df['Avg_outside_range'] = df[columns_out].mean(axis=1)

# Round the decimal value to 3 points.
rounded_df = df.round(3)
merged_df = pd.concat([ omitted_df, rounded_df], axis=1)
df_no_na = df_with_extra_data.fillna('')

# Add in the missing rows from the original file.
with open(('output.csv'), 'w',newline='') as f:
	writer = csv.writer(f)
	for index,row in df_no_na.iterrows():
		writer.writerow(row)
	writer.writerow("\n")
	write_index = True
	for index1,row1 in merged_df.iterrows():
		if write_index:
			writer.writerow(row1.index)
			write_index=False
		else:
			writer.writerow(row1)

