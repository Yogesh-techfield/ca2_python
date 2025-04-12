# Import required libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the Excel file 
df = pd.read_excel(r"C:\Downloads\DDW-0000C-03A.xlsx", skiprows=3)

# Remove completely empty rows and columns
df.dropna(how='all', inplace=True)
df.dropna(axis=1, how='all', inplace=True)

# Rename columns to more meaningful names
df.rename(columns={
    'Unnamed: 3': 'Area',
    'Urban': 'Area_Type',
    'Unnamed: 5': 'Religion',
    'Unnamed: 6': 'Age_Group',
    'Persons': 'Total_Persons',
    'Males': 'Total_Males',
    'Females': 'Total_Females'
}, inplace=True)

# Drop irrelevant unnamed columns if they exist
df.drop(columns=['Unnamed: 0', 'Unnamed: 1', 'Unnamed: 2'], errors='ignore', inplace=True)

# Remove rows with missing values in key columns
df.dropna(subset=['Religion', 'Age_Group', 'Total_Persons'], inplace=True)

# Ensure Total_Persons is numeric and drop rows with NaNs
df['Total_Persons'] = pd.to_numeric(df['Total_Persons'], errors='coerce')
df.dropna(inplace=True)

# Function to categorize a numerical column into 4 labeled bins
def categorize_col(df, col, labels):
    edges = [
        df[col].min(),
        df[col].quantile(0.25),
        df[col].quantile(0.5),
        df[col].quantile(0.75),
        df[col].max()
    ]
    df[col + '_Category'] = pd.cut(df[col], bins=edges, labels=labels, duplicates='drop')
    return df

# Define labels and apply categorization to 'Total_Persons'
labels = ['not_popular', 'below_avg', 'average', 'popular']
df = categorize_col(df, 'Total_Persons', labels)

# Display value counts for the categorized 'Total_Persons'
print("Categories:\n", df['Total_Persons_Category'].value_counts())

# Count the number of records for each religion
print("\nCount of Religion Categories:")
print(df["Religion"].value_counts())

# Print mean and median of Total_Persons
print("Mean Total Persons:", df["Total_Persons"].mean().round())
print("Median Total Persons:", df["Total_Persons"].median().round())

# Display unique age groups in sorted order
print("Age Groups Present:", sorted(df["Age_Group"].unique()))

# Calculate and print the standard deviation of Total_Persons
print("\nStandard Deviation of Total Persons:", df["Total_Persons"].std().round())

# Create a new column converting Total_Persons to thousands
df["Total_Persons_in_thousands"] = df["Total_Persons"] / 1000
print("\nUpdated DataFrame with 'Total_Persons_in_thousands':")
print(df[["Total_Persons", "Total_Persons_in_thousands"]].head())

# Normalize Total_Persons to a 0–1 scale
df["Total_Persons_Normalized"] = (
    (df["Total_Persons"] - df["Total_Persons"].min()) / 
    (df["Total_Persons"].max() - df["Total_Persons"].min())
)
print("\nNormalized 'Total_Persons' column:")
print(df[["Total_Persons", "Total_Persons_Normalized"]].head(10))

# Bar chart showing the number of records per religion
plt.figure(figsize=(12, 6))
sns.countplot(data=df, x='Religion', order=df['Religion'].value_counts().index)
plt.title('Count of Entries by Religion')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# Histogram showing distribution of Total_Persons
if 'Total_Persons' in df.columns:
    plt.figure(figsize=(8, 5))
    sns.histplot(df["Total_Persons"].dropna(), bins=30, kde=True, color="yellow", edgecolor="green")
    plt.title("Distribution of Total Persons (Seaborn)")
    plt.xlabel("Total Persons")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()
else:
    print("Column 'Total_Persons' not found in the DataFrame.")

# Scatter plot: Total_Persons vs Total_Males, colored by Religion
plt.figure(figsize=(10, 6))
sns.scatterplot(
    x=df["Total_Persons"],
    y=df["Total_Males"],
    hue=df["Religion"],
    alpha=0.4,
    legend=True
)
plt.title("Total Persons vs Total Males (Seaborn)")
plt.xlabel("Total Persons")
plt.ylabel("Total Males")
plt.xscale("log")
plt.yscale("log")
plt.tight_layout()
plt.show()

# Correlation heatmap for numerical columns
corr_matrix = df.select_dtypes(include=['number']).corr()
plt.figure(figsize=(10, 6))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", linewidths=0.5)
plt.title("Correlation Heatmap (Seaborn)")
plt.tight_layout()
plt.show()

# Pie chart showing the distribution of religions
plt.figure(figsize=(7, 7))
df["Religion"].value_counts().plot.pie(
    autopct='%.1f%%',
    colors=sns.color_palette("Set2")
)
plt.title("Pie Chart of Religion Distribution")
plt.ylabel("")
plt.show()

# Line plot of the first 20 Total_Persons records
plt.figure(figsize=(5, 4))
plt.plot(df["Total_Persons"].head(20), marker='o', linestyle='dashdot', color='red')
plt.xlabel("Record Index")
plt.ylabel("Total Persons")
plt.title("Line Plot of Total Persons (First 20 Records)")
plt.tight_layout()
plt.show()

# Donut chart showing the distribution of Urban vs Rural area types
area_counts = df["Area_Type"].value_counts()
plt.pie(
    area_counts,
    labels=area_counts.index,
    autopct='%1.1f%%',
    colors=['purple', 'grey']
)
plt.gca().add_artist(plt.Circle((0, 0), 0.7, color='white'))  # Inner white circle
plt.title("Donut Chart of Area Type")
plt.tight_layout()
plt.show()

# Bar chart of top 20 areas by total population
df_area = df.groupby('Area')['Total_Persons'].sum().sort_values(ascending=False).head(20)
plt.figure(figsize=(10, 5))
plt.bar(df_area.index, df_area.values, color='b')
plt.xlabel("Area")
plt.ylabel("Total Persons")
plt.title("Top 20 Areas by Total Population")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
