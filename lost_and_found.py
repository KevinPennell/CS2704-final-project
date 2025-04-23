import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def extract_breed(breed_string):
    if isinstance(breed_string, str):
        if 'Cat -' in breed_string:
            return breed_string.split('Cat -')[1].strip()
        else:
            return breed_string.strip()
    return breed_string

def main():
    file_path = r"C:\Users\kevin\pythonStuff\.venv\CS2704 Final\animalslostandfound.xlsx"
    
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    print("Columns in the dataset:", df.columns.tolist())

    if 'Breed' not in df.columns or 'State' not in df.columns:
        print("Expected columns 'Breed' and 'State' not found in the data.")
        return

    df['is_cat'] = df['Breed'].apply(lambda x: isinstance(x, str) and 'Cat -' in x)
    df['CleanedBreed'] = df['Breed'].apply(extract_breed)

    grouped = df.groupby('CleanedBreed').agg(
        total_count=('State', 'count'),
        found_count=('State', lambda x: (x == 'Found').sum()),
        is_cat=('is_cat', 'any')
    ).reset_index()

    grouped['found_rate'] = (grouped['found_count'] / grouped['total_count']) * 100

    cats_group = grouped[grouped['is_cat'] == True].sort_values('total_count', ascending=False).head(10)
    non_cats_group = grouped[grouped['is_cat'] == False].sort_values('total_count', ascending=False).head(10)

    fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=True)

    axes[0].bar(cats_group['CleanedBreed'], cats_group['found_rate'], color='red')
    axes[0].set_title("Top 10 Cats by Total Count")
    axes[0].set_xlabel("Cat Breed")
    axes[0].set_ylabel("Percentage Found (%)")
    axes[0].tick_params(axis='x', rotation=45)

    for bar in axes[0].patches:
        height = bar.get_height()
        axes[0].annotate(f'{height:.1f}%', 
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3),
                         textcoords="offset points",
                         ha='center', va='bottom')

    axes[1].bar(non_cats_group['CleanedBreed'], non_cats_group['found_rate'], color='skyblue')
    axes[1].set_title("Top 10 Non-Cats by Total Count")
    axes[1].set_xlabel("Breed/Animal")
    axes[1].tick_params(axis='x', rotation=45)

    for bar in axes[1].patches:
        height = bar.get_height()
        axes[1].annotate(f'{height:.1f}%', 
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3),
                         textcoords="offset points",
                         ha='center', va='bottom')

    plt.suptitle("Comparison of Found Rate: Top 10 Cat Breeds vs Top 10 Non-Cat Animals")
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

    # Heatmap Section

    # Take top 20 overall breeds
    top_20_breeds = grouped.sort_values('total_count', ascending=False).head(20)

    # Set breed as index for heatmap
    heatmap_data = top_20_breeds.set_index('CleanedBreed')[['found_rate']]

    # Plotting the heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="YlOrRd", linewidths=0.5, cbar_kws={'label': 'Found Rate (%)'})
    plt.title("Heatmap of Found Rates for Top 20 Breeds/Animals")
    plt.xlabel("Found Rate (%)")
    plt.ylabel("Breed/Animal")
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
