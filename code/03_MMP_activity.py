import pandas as pd

# read data
df_mmp = pd.read_csv("MMP_match.csv", header=None)  
df_halogen_free = pd.read_csv("halogen_free.csv")  
df_halogen_containing = pd.read_csv("halogen_containing.csv")  

# add column names
df_mmp.columns = ['natural_id', 'np_smiles', 'chem_id', 'smiles']

# empty lists
halogen_free_activity = []
halogen_containing_activity = []

# match according to smi
for index, row in df_mmp.iterrows():
    np_smiles = row['np_smiles']
    for _, row2 in df_halogen_free.iterrows():
        if np_smiles == row2['canonical_smi']:
            halogen_free_activity.append([row['natural_id'], row['np_smiles']] + row2[2:].tolist() + [row['chem_id'], row['smiles']])

# match according to id
for index, row in df_mmp.iterrows():
    chem_id = row['chem_id']
    for _, row2 in df_halogen_containing.iterrows():
        if chem_id == row2['chem']:
            halogen_containing_activity.append([row['natural_id'], row['np_smiles'],row['chem_id'], row['smiles']] + row2[2:].tolist())

# save results
df_free = pd.DataFrame(halogen_free_activity, columns=['natural_id', 'np_smiles'] + list(df_halogen_free.columns[2:]) + ['chem_id', 'smiles'])
df_containing = pd.DataFrame(halogen_containing_activity, columns=['natural_id', 'np_smiles', 'chem_id', 'smiles'] + list(df_halogen_containing.columns[2:]))
df_free.to_csv('matched_halogen_free_activity.csv', index=False)
df_containing.to_csv('matched_halogen_containing_activity.csv', index=False)

