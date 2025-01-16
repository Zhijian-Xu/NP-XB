import pandas as pd

# read data
df1 = pd.read_csv("chembl_activity_terms.csv", header=None)
df2 = pd.read_csv("assay.csv", header=None)

# assign column names to df1 and df2
df1.columns = ['chem', 'canonical_smi', 'standard', 'pvalue', 'Assay_ChEMBL_ID', 'Assay_Type', 'target_id', 'target_name', 'target_organism']
df2.columns = ['ChEMBL_ID', 'confidence_score']

# create an empty list to store confidence score
confidence_scores = []

# search matched value
for index, row in df1.iterrows():
    assay_chembl_id = row['Assay_ChEMBL_ID'] 
    matched_score = None 
    for _, row2 in df2.iterrows():
        if row2['ChEMBL_ID'] == assay_chembl_id:  
            matched_score = row2['confidence_score']  
            break  
    confidence_scores.append(matched_score)  

# add new column to df1
df1['confidence_score'] = confidence_scores

# Insert 'confidence_score' column after 'Assay_Type'
assay_type_idx = df1.columns.get_loc('Assay_Type') + 1
df1.insert(assay_type_idx, 'confidence_score', df1.pop('confidence_score'))

# add filter condition 
df_filtered = df1[df1['confidence_score'] == 9]
df_filtered_b = df_filtered[df_filtered['Assay_Type'] == 'B']
df_filtered_b_standard = df_filtered_b[df_filtered_b['standard'].isin(['IC50', 'EC50', 'Ki', 'Kd'])]

# create lists to store rows halogen-free and halogen-containing
output_rows = []
output_rows_nox = []


for _, row in df_filtered_b_standard.iterrows():
    smiles = row['canonical_smi']
    if 'F' in smiles or 'Cl' in smiles or 'Br' in smiles or 'I' in smiles:
        output_rows.append(row)
    else:
        output_rows_nox.append(row)

# Convert the lists of rows back into DataFrames
df_with_halogen = pd.DataFrame(output_rows)
df_without_halogen = pd.DataFrame(output_rows_nox)

# Save the results
df_with_halogen.to_csv("halogen_containing.csv", index=False)
df_without_halogen.to_csv("halogen_free.csv", index=False)


