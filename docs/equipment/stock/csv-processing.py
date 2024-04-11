import pandas as pd

# Read the CSV file
df = pd.read_csv('docs/equipment/stock/User Selection List.csv', encoding='utf-8')

# Filter only active assets and where 'Asset Type' is 0 and any of 'Year 1', 'Year 2', or 'Year 3' is 'Yes'
df = df[(df['Active'] == 'Yes') & (df['Asset Type'] == 0) & ((df['Year 1'] == 'Yes') | (df['Year 2'] == 'Yes') | (df['Year 3'] == 'Yes'))]

# Replace 'Yes' with checkmark and 'No' with empty string in relevant columns
df[['Year 1', 'Year 2', 'Year 4', 'Selected']] = df[['Year 1', 'Year 2', 'Year 4', 'Selected']].replace({'Yes': '&#10003;', 'No': ''}, regex=True)

# Search through the categories for microphones, if there is a match, ignore case, ignore NaNs and replace with just 'Microphones'
df.loc[df['Category'].str.contains('microphone', case=False, na=False), 'Category'] = 'Microphones'

# Replace NaN values in 'Asset Description' with empty string
df['Asset Description'].fillna('', inplace=True)

# Replace single line breaks with double line breaks in 'Asset Description'
df['Asset Description'] = df['Asset Description'].str.replace('\n', '\n\n')

# Define function to format Markdown table
def format_markdown_table(data):
    markdown_table = '|'.join(data.columns) + '\n'
    markdown_table += '|'.join(['---'] * len(data.columns)) + '\n'
    for index, row in data.iterrows():
        markdown_table += '|'.join(row) + '\n'
    return markdown_table

# Write data to a single Markdown file
with open('docs/equipment/stock/assets.md', 'w', encoding='utf-8') as file:
    file.write('''# What's in Stores?\n''')
    for category, group in df.groupby('Category'):
        # Write category heading
        file.write(f'## {category}\n\n')
        for index, row in group.iterrows():
            # Write asset heading and description
            file.write(f'### {row["Asset Name"]}\n\n')
            # Write table of years with access
            file.write(format_markdown_table(row[['Year 1', 'Year 2', 'Year 4']].to_frame().T) + '\n')
            # Write asset description with double line breaks
            file.write(f'{row["Asset Description"]}\n\n')
