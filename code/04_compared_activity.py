import pandas as pd
import numpy as np

# read data
df_halogen_free = pd.read_csv('matched_halogen_free_activity.csv')
df_halogen_containing = pd.read_csv('matched_halogen_containing_activity.csv')

# duplicate
df_halogen_free_unique = df_halogen_free[['natural_id', 'chem_id', 'Assay_ChEMBL_ID', 'target_id']].drop_duplicates()
df_halogen_containing_unique = df_halogen_containing[['natural_id', 'chem_id', 'Assay_ChEMBL_ID', 'target_id']].drop_duplicates()

# search common rows
common_rows = pd.merge(df_halogen_free_unique, df_halogen_containing_unique, on=['natural_id', 'chem_id', 'Assay_ChEMBL_ID', 'target_id'], how='inner')

# create a empty list
matched_dfs = []

# search matched row
for index, row in common_rows.iterrows():
    df_halogen_free_matched = df_halogen_free[(df_halogen_free['natural_id'] == row['natural_id']) & (df_halogen_free['chem_id'] == row['chem_id']) & (df_halogen_free['Assay_ChEMBL_ID'] == row['Assay_ChEMBL_ID']) & (df_halogen_free['target_id'] == row['target_id'])] 
    df_halogen_containing_matched = df_halogen_containing[(df_halogen_containing['natural_id'] == row['natural_id']) & (df_halogen_containing['chem_id'] == row['chem_id']) & (df_halogen_containing['Assay_ChEMBL_ID'] == row['Assay_ChEMBL_ID']) & (df_halogen_containing['target_id'] == row['target_id'])]
    len_free = len(df_halogen_free_matched)
    len_containing = len(df_halogen_containing_matched)   
    max_len = max(len_free, len_containing)
    fill_free = pd.DataFrame(np.nan, index=range(max_len - len_free), columns=df_halogen_free_matched.columns)
    fill_containing = pd.DataFrame(np.nan, index=range(max_len - len_containing), columns=df_halogen_containing_matched.columns)
    if len_free == len_containing:
        combined_df = pd.concat([df_halogen_free_matched.reset_index(drop=True), df_halogen_containing_matched.reset_index(drop=True)], axis=1)
    elif len_free < len_containing:
        combined_vertical = pd.concat([df_halogen_free_matched.reset_index(drop=True), fill_free], axis=0)
        combined_df = pd.concat([combined_vertical.reset_index(drop=True), df_halogen_containing_matched.reset_index(drop=True)], axis=1)
    else:
        combined_vertical = pd.concat([df_halogen_containing_matched.reset_index(drop=True), fill_containing], axis=0)
        combined_df = pd.concat([df_halogen_free_matched.reset_index(drop=True), combined_vertical.reset_index(drop=True)], axis=1)
    matched_dfs.append(combined_df)

# save results
result_df = pd.concat(matched_dfs, ignore_index=True)
result_df = result_df.iloc[:, list(range(0, 9)) + list(range(13, result_df.shape[1]))]
result_df.to_csv('matched_halogen_activities.csv', index=False)

