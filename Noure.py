# Noure: 1-34 vs 1-34 scatter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create output directory for plots
output_dir = 'plots'
os.makedirs(output_dir, exist_ok=True)

# Import csv file
df = pd.read_csv('output.csv')

# Drop column 1 & combine AcceptedCmp1-5
df = df.iloc[:, 1:]

# Check if any row has more than one '1' in the specified columns
columns_to_check = ['AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5']
df['MultipleAccepted'] = df[columns_to_check].sum(axis=1) > 1
rows_with_multiple_accepted = df[df['MultipleAccepted']]
# print(rows_with_multiple_accepted)  # there are none as expected

df['AcceptedCmp'] = np.where(df['AcceptedCmp1'] == 1, 1,
                    np.where(df['AcceptedCmp2'] == 1, 2,
                    np.where(df['AcceptedCmp3'] == 1, 3,
                    np.where(df['AcceptedCmp4'] == 1, 4,
                    np.where(df['AcceptedCmp5'] == 1, 5, np.nan)))))

df = df.drop(columns=['AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5', 'Year_Birth', 'MultipleAccepted', 'Dt_Customer', 'AverageIncome'])
file_path = '/Users/nuomiao//Desktop/csv.csv'
df.to_csv(file_path)

# Plot education vs income
education_mapping = {
    'Basic': 0,
    "Bachelor's": 1,
    "Master's": 2,
    'PhD': 3
}
highest_income = df["Income"].max()
lowest_income = df["Income"].min()
income_interval = (highest_income - lowest_income) / 4
bins = [0, 25000, 50000, 75000, float('inf')]
labels = ['0 - 25000', '25000 - 50000', '50000 - 75000', '75000+']
df['Income_Group'] = pd.cut(df['Income'], bins=bins, labels=labels, right=True, include_lowest=True)
income_education_group = df.groupby(['Income_Group', 'Education']).size().unstack(fill_value=0)

plt.figure(figsize=(12, 6))
colors = sns.color_palette("viridis", len(education_mapping))
income_education_group.plot(kind='bar', stacked=True, color=colors)
plt.title('Income vs Education Levels')
plt.xlabel("Customer's Yearly Household Income")
plt.ylabel('Number of Individuals')
plt.xticks(rotation=45)
plt.legend(title='Education Level', labels=education_mapping.keys(), bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "education_vs_income.png"))
plt.close()

# Plot Income vs NumWebVisitsMonth
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='NumWebVisitsMonth', y='Income', palette='viridis')
plt.title('Income vs Number of Web Visits per Month')
plt.xlabel('Number of Web Visits per Month')
plt.ylabel('Income')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "income_vs_web_visits.png"))
plt.close()

# Products scatter plots
products = ['MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']
for product in products:
    plt.figure(figsize=(10, 7))
    sns.scatterplot(data=df, x=product, y='Income', palette='viridis')
    plt.title(f'Income vs Amount Spent on {product.replace("Mnt", "")} in Last 2 Years')
    plt.xlabel(f'Amount Spent on {product.replace("Mnt", "")} in Last 2 Years')
    plt.ylabel('Income')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"income_vs_{product}.png"))
    plt.close()

# Plot NumWebVisitsMonth vs MntMeatProducts
plt.figure(figsize=(10, 7))
sns.barplot(data=df, x='NumWebVisitsMonth', y='MntMeatProducts', palette='viridis')
plt.title('NumWebVisitsMonth vs MntMeatProducts')
plt.xlabel('Number of Web Visits per Month')
plt.ylabel('Amount Spent on Meat in Last 2 Years')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "NumWebVisitsMonth_vs_MntMeat.png"))
plt.close()

# Plot Income vs Age
bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, float('inf')]
labels = ['0-10', '10-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80+']
df['Age_Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False, include_lowest=True)
average_income_by_age_group = df.groupby('Age_Group')['Income'].mean().reset_index()

plt.figure(figsize=(10, 7))
sns.barplot(data=average_income_by_age_group, x='Age_Group', y='Income', palette='viridis')
plt.title('Average Income by Age Group')
plt.xlabel('Age Group')
plt.ylabel('Average Income')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "Average_Income_by_Age_Group.png"))
plt.close()

# Pie chart of products sold
columns_to_sum = ['MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']
total_spent_per_product = df[columns_to_sum].sum()
total_spent = total_spent_per_product.sum()
percentage_of_total = (total_spent_per_product / total_spent) * 100
sorted_indices = percentage_of_total.sort_values().index
sorted_percentages = percentage_of_total[sorted_indices]

plt.figure(figsize=(8, 6))
wedges, texts, autotexts = plt.pie(sorted_percentages, autopct=lambda p: f'{p:.1f}%', startangle=140, colors=sns.color_palette("mako"), radius=0.5, pctdistance=1.1)
legend_labels = ['Fruit', 'Sweets', 'Fish', 'Gold', 'Meat', 'Wine']
plt.legend(wedges, legend_labels, title="Products", loc="upper left")
plt.title('Percentage of Total Spending by Product')
plt.axis('equal')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "spending_percentage_pie_chart_with_legend.png"))
plt.close()

# Plot Income vs Childhome
# Plot MntSweetProducts vs Kidhome
# Plot NumWebPurchases vs Teenhome
# Plot NumWebVisitsMonth vs Teenhome
# Define the plots and corresponding labels
plots = [
    ('Childhome', 'Income', 'Number of Children/Teenagers at Home', 'Income', 'Income vs Number of Children/Teenagers at Home'),
    ('Kidhome', 'MntSweetProducts', 'Number of Children at Home', 'Amount Spent on Sweet in Last 2 Years', 'Amount Spent on Sweet in Last 2 Years vs Number of Children at Home'),
    ('Teenhome', 'NumWebPurchases', 'Number of Teenagers at Home', 'Number of Purchases Made Through the Company’s Website', 'Number of Purchases Made Through the Company’s Website vs Number of Teenagers at Home'),
    ('Teenhome', 'NumWebVisitsMonth', 'Number of Teenagers at Home', 'Number of Web Visits per Month', 'Number of Teenagers at Home vs Number of Web Visits per Month'),
]

# Iterate through the pairs and create bar plots
for x_var, y_var, x_label, y_label, title in plots:
    plt.figure(figsize=(10, 7))
    sns.barplot(data=df, x=x_var, y=y_var, palette='viridis')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{y_var}_vs_{x_var}.png"))
    plt.close()