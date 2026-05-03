# Module 11 Assignment: Data Visualization with Matplotlib
# SunCoast Retail Visual Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("=" * 60)
print("SUNCOAST RETAIL VISUAL ANALYSIS")
print("=" * 60)

# ----- USE THE FOLLOWING CODE TO CREATE SAMPLE DATA (DO NOT MODIFY) -----
np.random.seed(42)

quarters = pd.date_range(start='2022-01-01', periods=8, freq='Q')
quarter_labels = ['Q1 2022', 'Q2 2022', 'Q3 2022', 'Q4 2022', 
                 'Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023']

locations = ['Tampa', 'Miami', 'Orlando', 'Jacksonville']
categories = ['Electronics', 'Clothing', 'Home Goods', 'Sporting Goods', 'Beauty']

quarterly_data = []

for quarter_idx, quarter in enumerate(quarters):
    for location in locations:
        for category in categories:
            base_sales = np.random.normal(loc=100000, scale=20000)
            seasonal_factor = 1.0
            if quarter.quarter == 4:  # Q4 (holiday boost)
                seasonal_factor = 1.3
            elif quarter.quarter == 1:  # Q1 (post-holiday dip)
                seasonal_factor = 0.8
            
            location_factor = {
                'Tampa': 1.0,
                'Miami': 1.2,
                'Orlando': 0.9,
                'Jacksonville': 0.8
            }[location]
            
            category_factor = {
                'Electronics': 1.5,
                'Clothing': 1.0,
                'Home Goods': 0.8,
                'Sporting Goods': 0.7,
                'Beauty': 0.9
            }[category]
            
            growth_factor = (1 + 0.05/4) ** quarter_idx
            
            sales = base_sales * seasonal_factor * location_factor * category_factor * growth_factor
            sales = sales * np.random.normal(loc=1.0, scale=0.1)
            
            ad_spend = (sales ** 0.7) * 0.05 * np.random.normal(loc=1.0, scale=0.2)
            
            quarterly_data.append({
                'Quarter': quarter,
                'QuarterLabel': quarter_labels[quarter_idx],
                'Location': location,
                'Category': category,
                'Sales': round(sales, 2),
                'AdSpend': round(ad_spend, 2),
                'Year': quarter.year
            })

customer_data = []
total_customers = 2000

age_params = {
    'Tampa': (45, 15),
    'Miami': (35, 12),
    'Orlando': (38, 14),
    'Jacksonville': (42, 13)
}

for location in locations:
    mean_age, std_age = age_params[location]
    customer_count = int(total_customers * {
        'Tampa': 0.3,
        'Miami': 0.35,
        'Orlando': 0.2,
        'Jacksonville': 0.15
    }[location])
    
    ages = np.random.normal(loc=mean_age, scale=std_age, size=customer_count)
    ages = np.clip(ages, 18, 80).astype(int)
    
    for age in ages:
        if age < 30:
            category_preference = np.random.choice(categories, p=[0.3, 0.3, 0.1, 0.2, 0.1])
        elif age < 50:
            category_preference = np.random.choice(categories, p=[0.25, 0.2, 0.25, 0.15, 0.15])
        else:
            category_preference = np.random.choice(categories, p=[0.15, 0.1, 0.35, 0.1, 0.3])
        
        base_amount = np.random.gamma(shape=5, scale=20)
        
        price_tier = np.random.choice(['Budget', 'Mid-range', 'Premium'], 
                                     p=[0.3, 0.5, 0.2])
        
        tier_factor = {'Budget': 0.7, 'Mid-range': 1.0, 'Premium': 1.8}[price_tier]
        
        purchase_amount = base_amount * tier_factor
        
        customer_data.append({
            'Location': location,
            'Age': age,
            'Category': category_preference,
            'PurchaseAmount': round(purchase_amount, 2),
            'PriceTier': price_tier
        })

sales_df = pd.DataFrame(quarterly_data)
customer_df = pd.DataFrame(customer_data)

sales_df['Quarter_Num'] = sales_df['Quarter'].dt.quarter
sales_df['SalesPerDollarSpent'] = sales_df['Sales'] / sales_df['AdSpend']

print("\nSales Data Sample:")
print(sales_df.head())
print("\nCustomer Data Sample:")
print(customer_df.head())
print("\nDataFrames created successfully. Ready for visualization!")
# ----- END OF DATA CREATION -----


# 1.1 total sales trend line chart
def plot_quarterly_sales_trend():
    """
    Create a line chart showing total sales for each quarter.
    REQUIRED: Return the figure object
    """
    totals = sales_df.groupby('QuarterLabel')['Sales'].sum().reset_index()
    totals['order'] = totals['QuarterLabel'].apply(lambda x: quarter_labels.index(x))
    totals = totals.sort_values('order')

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(totals['QuarterLabel'], totals['Sales'] / 1e6,
            marker='o', color='steelblue', linewidth=2, markersize=7)
    ax.set_title('Total Quarterly Sales (2022-2023)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Quarter', fontsize=12)
    ax.set_ylabel('Total Sales (Millions $)', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.tick_params(axis='x', rotation=30)
    plt.tight_layout()
    return fig


# 1.2 sales per location over time
def plot_location_sales_comparison():
    """
    Create a multi-line chart comparing quarterly sales across different locations.
    REQUIRED: Return the figure object
    """
    loc_q = sales_df.groupby(['QuarterLabel', 'Location'])['Sales'].sum().reset_index()
    loc_q['order'] = loc_q['QuarterLabel'].apply(lambda x: quarter_labels.index(x))
    loc_q = loc_q.sort_values('order')

    colors  = {'Tampa': 'steelblue', 'Miami': 'tomato', 'Orlando': 'seagreen', 'Jacksonville': 'darkorange'}
    markers = {'Tampa': 'o', 'Miami': 's', 'Orlando': '^', 'Jacksonville': 'D'}

    fig, ax = plt.subplots(figsize=(11, 5))
    for loc in locations:
        d = loc_q[loc_q['Location'] == loc]
        ax.plot(d['QuarterLabel'], d['Sales'] / 1e6,
                label=loc, marker=markers[loc], color=colors[loc], linewidth=2, markersize=7)
    ax.set_title('Quarterly Sales by Location (2022-2023)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Quarter', fontsize=12)
    ax.set_ylabel('Sales (Millions $)', fontsize=12)
    ax.legend(title='Location')
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.tick_params(axis='x', rotation=30)
    plt.tight_layout()
    return fig


# 2.1 grouped bar - category sales by location for Q4 2023
def plot_category_performance_by_location():
    """
    Create a grouped bar chart showing how each product category performs in different locations.
    REQUIRED: Return the figure object
    """
    recent = sales_df[sales_df['QuarterLabel'] == 'Q4 2023']
    grouped = recent.groupby(['Location', 'Category'])['Sales'].sum().unstack()

    fig, ax = plt.subplots(figsize=(12, 6))
    grouped.plot(kind='bar', ax=ax, width=0.7)
    ax.set_title('Category Sales by Location - Q4 2023', fontsize=14, fontweight='bold')
    ax.set_xlabel('Location', fontsize=12)
    ax.set_ylabel('Sales ($)', fontsize=12)
    ax.legend(title='Category', bbox_to_anchor=(1.01, 1), loc='upper left')
    ax.tick_params(axis='x', rotation=15)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    return fig


# 2.2 stacked bar - % of sales per category per location
def plot_sales_composition_by_location():
    """
    Create a stacked bar chart showing the composition of sales across categories for each location.
    REQUIRED: Return the figure object
    """
    comp = sales_df.groupby(['Location', 'Category'])['Sales'].sum().unstack()
    comp_pct = comp.div(comp.sum(axis=1), axis=0) * 100

    fig, ax = plt.subplots(figsize=(10, 6))
    comp_pct.plot(kind='bar', stacked=True, ax=ax, colormap='tab10', width=0.6)
    ax.set_title('Sales Composition by Location (%)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Location', fontsize=12)
    ax.set_ylabel('% of Sales', fontsize=12)
    ax.legend(title='Category', bbox_to_anchor=(1.01, 1), loc='upper left')
    ax.tick_params(axis='x', rotation=15)
    ax.set_ylim(0, 110)
    plt.tight_layout()
    return fig


# 3.1 scatter plot - ad spend vs sales
def plot_ad_spend_vs_sales():
    """
    Create a scatter plot to visualize the relationship between advertising spend and sales.
    REQUIRED: Return the figure object
    """
    color_map = {'Tampa': 'steelblue', 'Miami': 'tomato', 'Orlando': 'seagreen', 'Jacksonville': 'darkorange'}

    fig, ax = plt.subplots(figsize=(9, 6))
    for loc in locations:
        s = sales_df[sales_df['Location'] == loc]
        ax.scatter(s['AdSpend'], s['Sales'] / 1e3,
                   label=loc, color=color_map[loc], alpha=0.6, s=50)

    m, b = np.polyfit(sales_df['AdSpend'], sales_df['Sales'] / 1e3, 1)
    x_line = np.linspace(sales_df['AdSpend'].min(), sales_df['AdSpend'].max(), 100)
    ax.plot(x_line, m * x_line + b, color='black', linewidth=1.5, linestyle='--', label='Best Fit')

    for _, row in sales_df.nlargest(3, 'Sales').iterrows():
        ax.annotate(f"{row['Location']}\n{row['QuarterLabel']}",
                    xy=(row['AdSpend'], row['Sales'] / 1e3),
                    xytext=(row['AdSpend'] + 10, row['Sales'] / 1e3 + 5),
                    fontsize=7, arrowprops=dict(arrowstyle='->', color='gray'))

    ax.set_title('Ad Spend vs. Sales', fontsize=14, fontweight='bold')
    ax.set_xlabel('Ad Spend ($)', fontsize=12)
    ax.set_ylabel('Sales (Thousands $)', fontsize=12)
    ax.legend(title='Location')
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    return fig


# 3.2 ad efficiency line chart
def plot_ad_efficiency_over_time():
    """
    Create a line chart showing how efficient advertising spend has been over time.
    REQUIRED: Return the figure object
    """
    eff = sales_df.groupby('QuarterLabel')['SalesPerDollarSpent'].mean().reset_index()
    eff['order'] = eff['QuarterLabel'].apply(lambda x: quarter_labels.index(x))
    eff = eff.sort_values('order')

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(eff['QuarterLabel'], eff['SalesPerDollarSpent'],
            marker='o', color='purple', linewidth=2, markersize=7)

    peak = eff.loc[eff['SalesPerDollarSpent'].idxmax()]
    ax.annotate(f"Peak\n{peak['QuarterLabel']}",
                xy=(peak['QuarterLabel'], peak['SalesPerDollarSpent']),
                xytext=(peak['QuarterLabel'], peak['SalesPerDollarSpent'] + 1),
                fontsize=9, ha='center',
                arrowprops=dict(arrowstyle='->', color='gray'))

    ax.set_title('Ad Efficiency Over Time', fontsize=14, fontweight='bold')
    ax.set_xlabel('Quarter', fontsize=12)
    ax.set_ylabel('Sales per Dollar Spent', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.tick_params(axis='x', rotation=30)
    plt.tight_layout()
    return fig


# 4.1 age distribution histograms overall + per location
def plot_customer_age_distribution():
    """
    Create histograms showing the age distribution of customers, both overall and by location.
    REQUIRED: Return the figure object
    """
    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    axes = axes.flatten()

    ax = axes[0]
    ax.hist(customer_df['Age'], bins=20, color='steelblue', edgecolor='white', alpha=0.8)
    ax.axvline(customer_df['Age'].mean(), color='red', linestyle='--', linewidth=1.5,
               label=f"Mean: {customer_df['Age'].mean():.1f}")
    ax.axvline(customer_df['Age'].median(), color='orange', linestyle='-', linewidth=1.5,
               label=f"Median: {customer_df['Age'].median():.1f}")
    ax.set_title('All Locations', fontsize=11, fontweight='bold')
    ax.set_xlabel('Age')
    ax.set_ylabel('Count')
    ax.legend(fontsize=8)

    loc_colors = {'Tampa': 'steelblue', 'Miami': 'tomato', 'Orlando': 'seagreen', 'Jacksonville': 'darkorange'}
    for i, loc in enumerate(locations):
        ax = axes[i + 1]
        sub = customer_df[customer_df['Location'] == loc]['Age']
        ax.hist(sub, bins=15, color=loc_colors[loc], edgecolor='white', alpha=0.8)
        ax.axvline(sub.mean(), color='red', linestyle='--', linewidth=1.5,
                   label=f"Mean: {sub.mean():.1f}")
        ax.axvline(sub.median(), color='black', linestyle='-', linewidth=1.5,
                   label=f"Median: {sub.median():.1f}")
        ax.set_title(loc, fontsize=11, fontweight='bold')
        ax.set_xlabel('Age')
        ax.set_ylabel('Count')
        ax.legend(fontsize=8)

    axes[5].set_visible(False)
    fig.suptitle('Customer Age Distribution by Location', fontsize=14, fontweight='bold')
    plt.tight_layout()
    return fig


# 4.2 box plots - purchase amount by age group
def plot_purchase_by_age_group():
    """
    Create box plots showing purchase amounts across different age groups.
    REQUIRED: Return the figure object
    """
    df = customer_df.copy()
    df['AgeGroup'] = pd.cut(df['Age'], bins=[17, 30, 45, 60, 80],
                            labels=['18-30', '31-45', '46-60', '61+'])

    groups = [df[df['AgeGroup'] == g]['PurchaseAmount'].dropna()
              for g in ['18-30', '31-45', '46-60', '61+']]

    fig, ax = plt.subplots(figsize=(9, 6))
    bp = ax.boxplot(groups, labels=['18-30', '31-45', '46-60', '61+'],
                    patch_artist=True, medianprops=dict(color='black', linewidth=2))

    for patch, color in zip(bp['boxes'], ['#5b9bd5', '#70ad47', '#ffc000', '#ff6347']):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    ax.set_title('Purchase Amounts by Age Group', fontsize=14, fontweight='bold')
    ax.set_xlabel('Age Group', fontsize=12)
    ax.set_ylabel('Purchase Amount ($)', fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    return fig


# 5.1 histogram of purchase amounts
def plot_purchase_amount_distribution():
    """
    Create a histogram showing the distribution of purchase amounts.
    REQUIRED: Return the figure object
    """
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.hist(customer_df['PurchaseAmount'], bins=40, color='teal', edgecolor='white', alpha=0.8)
    ax.set_title('Purchase Amount Distribution', fontsize=14, fontweight='bold')
    ax.set_xlabel('Purchase Amount ($)', fontsize=12)
    ax.set_ylabel('Number of Customers', fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    return fig


# 5.2 pie chart - sales by price tier
def plot_sales_by_price_tier():
    """
    Create a pie chart showing the breakdown of sales by price tier.
    REQUIRED: Return the figure object
    """
    tier_sales = customer_df.groupby('PriceTier')['PurchaseAmount'].sum()
    tier_sales = tier_sales.reindex(['Budget', 'Mid-range', 'Premium'])
    explode = [0.08 if i == tier_sales.argmax() else 0 for i in range(len(tier_sales))]

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(tier_sales, labels=tier_sales.index, autopct='%1.1f%%',
           explode=explode, colors=['#5b9bd5', '#ffc000', '#ff6347'],
           startangle=140, textprops={'fontsize': 11})
    ax.set_title('Sales by Price Tier', fontsize=14, fontweight='bold')
    plt.tight_layout()
    return fig


# 6.1 pie chart - market share by category
def plot_category_market_share():
    """
    Create a pie chart showing the market share of each product category.
    REQUIRED: Return the figure object
    """
    cat_sales = sales_df.groupby('Category')['Sales'].sum().reindex(categories)
    explode = [0.08 if i == cat_sales.argmax() else 0 for i in range(len(cat_sales))]

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(cat_sales, labels=cat_sales.index, autopct='%1.1f%%',
           explode=explode, colors=list(plt.cm.Set2.colors[:5]),
           startangle=140, textprops={'fontsize': 11})
    ax.set_title('Market Share by Category', fontsize=14, fontweight='bold')
    plt.tight_layout()
    return fig


# 6.2 pie chart - sales by location
def plot_location_sales_distribution():
    """
    Create a pie chart showing the distribution of sales across different store locations.
    REQUIRED: Return the figure object
    """
    loc_sales = sales_df.groupby('Location')['Sales'].sum().reindex(locations)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(loc_sales, labels=loc_sales.index, autopct='%1.1f%%',
           colors=['steelblue', 'tomato', 'seagreen', 'darkorange'],
           startangle=140, textprops={'fontsize': 11})
    ax.set_title('Sales by Location', fontsize=14, fontweight='bold')
    plt.tight_layout()
    return fig


# 7 - dashboard (6 subplots)
def create_business_dashboard():
    """
    Create a comprehensive dashboard with multiple subplots highlighting key business insights.
    REQUIRED: Return the figure object with at least 4 subplots
    """
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    fig.suptitle('SunCoast Retail - Business Dashboard (2022-2023)',
                 fontsize=15, fontweight='bold')

    loc_colors = {'Tampa': 'steelblue', 'Miami': 'tomato',
                  'Orlando': 'seagreen', 'Jacksonville': 'darkorange'}

    # total sales trend
    ax1 = axes[0, 0]
    qt = sales_df.groupby('QuarterLabel')['Sales'].sum().reset_index()
    qt['order'] = qt['QuarterLabel'].apply(lambda x: quarter_labels.index(x))
    qt = qt.sort_values('order')
    ax1.plot(qt['QuarterLabel'], qt['Sales'] / 1e6,
             marker='o', color='steelblue', linewidth=2, markersize=5)
    ax1.set_title('Total Quarterly Sales', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Sales (M$)')
    ax1.tick_params(axis='x', rotation=45, labelsize=7)
    ax1.grid(True, linestyle='--', alpha=0.5)

    # sales by location
    ax2 = axes[0, 1]
    lq = sales_df.groupby(['QuarterLabel', 'Location'])['Sales'].sum().reset_index()
    lq['order'] = lq['QuarterLabel'].apply(lambda x: quarter_labels.index(x))
    lq = lq.sort_values('order')
    for loc in locations:
        d = lq[lq['Location'] == loc]
        ax2.plot(d['QuarterLabel'], d['Sales'] / 1e6,
                 label=loc, marker='o', color=loc_colors[loc], linewidth=1.8, markersize=5)
    ax2.set_title('Sales by Location', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Sales (M$)')
    ax2.tick_params(axis='x', rotation=45, labelsize=7)
    ax2.legend(fontsize=7, loc='upper left')
    ax2.grid(True, linestyle='--', alpha=0.5)

    # category market share pie
    ax3 = axes[0, 2]
    cs = sales_df.groupby('Category')['Sales'].sum().reindex(categories)
    explode = [0.07 if i == cs.argmax() else 0 for i in range(len(cs))]
    ax3.pie(cs, labels=cs.index, autopct='%1.1f%%',
            explode=explode, colors=list(plt.cm.Set2.colors[:5]),
            startangle=140, textprops={'fontsize': 8})
    ax3.set_title('Category Market Share', fontsize=11, fontweight='bold')

    # grouped bar Q4 2023
    ax4 = axes[1, 0]
    recent = sales_df[sales_df['QuarterLabel'] == 'Q4 2023']
    grouped = recent.groupby(['Location', 'Category'])['Sales'].sum().unstack()
    grouped.plot(kind='bar', ax=ax4, width=0.7, legend=False)
    ax4.set_title('Category Performance Q4 2023', fontsize=11, fontweight='bold')
    ax4.set_ylabel('Sales ($)')
    ax4.tick_params(axis='x', rotation=15, labelsize=8)
    ax4.grid(axis='y', linestyle='--', alpha=0.5)

    # ad spend vs sales scatter
    ax5 = axes[1, 1]
    for loc in locations:
        s = sales_df[sales_df['Location'] == loc]
        ax5.scatter(s['AdSpend'], s['Sales'] / 1e3,
                    label=loc, color=loc_colors[loc], alpha=0.5, s=25)
    m, b = np.polyfit(sales_df['AdSpend'], sales_df['Sales'] / 1e3, 1)
    x_line = np.linspace(sales_df['AdSpend'].min(), sales_df['AdSpend'].max(), 100)
    ax5.plot(x_line, m * x_line + b, color='black', linewidth=1.5, linestyle='--')
    ax5.set_title('Ad Spend vs. Sales', fontsize=11, fontweight='bold')
    ax5.set_xlabel('Ad Spend ($)')
    ax5.set_ylabel('Sales (K$)')
    ax5.legend(fontsize=7)
    ax5.grid(True, linestyle='--', alpha=0.5)

    # price tier pie
    ax6 = axes[1, 2]
    ts = customer_df.groupby('PriceTier')['PurchaseAmount'].sum().reindex(['Budget', 'Mid-range', 'Premium'])
    explode_t = [0.07 if i == ts.argmax() else 0 for i in range(len(ts))]
    ax6.pie(ts, labels=ts.index, autopct='%1.1f%%',
            explode=explode_t, colors=['#5b9bd5', '#ffc000', '#ff6347'],
            startangle=140, textprops={'fontsize': 9})
    ax6.set_title('Sales by Price Tier', fontsize=11, fontweight='bold')

    plt.tight_layout()
    return fig


# REQUIRED: Do not modify this function name
def main():
    print("\n" + "=" * 60)
    print("SUNCOAST RETAIL VISUAL ANALYSIS RESULTS")
    print("=" * 60)

    fig1  = plot_quarterly_sales_trend()
    fig2  = plot_location_sales_comparison()
    fig3  = plot_category_performance_by_location()
    fig4  = plot_sales_composition_by_location()
    fig5  = plot_ad_spend_vs_sales()
    fig6  = plot_ad_efficiency_over_time()
    fig7  = plot_customer_age_distribution()
    fig8  = plot_purchase_by_age_group()
    fig9  = plot_purchase_amount_distribution()
    fig10 = plot_sales_by_price_tier()
    fig11 = plot_category_market_share()
    fig12 = plot_location_sales_distribution()
    fig13 = create_business_dashboard()

    print("\nKEY BUSINESS INSIGHTS:")
    print("-" * 60)
    print("1. SALES TREND: Sales grew steadily 2022-2023. Q4 peaks each year; Q1 dips.")
    print("2. LOCATIONS: Miami leads in revenue. Jacksonville is the weakest store.")
    print("3. CATEGORIES: Electronics has the highest market share. Sporting Goods lags.")
    print("4. ADVERTISING: Ad spend and sales are positively correlated. ROI fluctuates.")
    print("5. DEMOGRAPHICS: Tampa customers avg age ~45; Miami skews younger (~35).")
    print("6. PRICING: Mid-range dominates. Premium is an upsell opportunity.")
    print()
    print("RECOMMENDATIONS:")
    print("  - Stock up and add staff every Q4 for the holiday spike.")
    print("  - Run targeted promotions in Jacksonville.")
    print("  - Push Electronics and Premium products.")
    print("  - Tailor marketing by location.")

    plt.show()

if __name__ == "__main__":
    main()