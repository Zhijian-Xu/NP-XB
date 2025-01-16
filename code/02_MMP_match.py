import rdkit
from rdkit import Chem
from rdkit.Chem import AllChem
import pandas as pd
import numpy as np

df1 = pd.read_csv("halogen_containing_duplicate_smi.csv", header=None)

smiles = df1[1]
chem_id = df1[0]

df2 = pd.read_csv("np_structure_duplicate_smi.csv", header=None)

natural_id = df2[0]
np_smiles = df2[1]


canon = []

for x in np_smiles:
    smi = Chem.CanonSmiles(x)
    canon.append(smi)


#Remove halogen 
results = []

patt=Chem.MolFromSmarts('[F,Cl,Br,I]')

for m in range(len(smiles)):
    mol = Chem.MolFromSmiles(smiles[m])
    rm = AllChem.DeleteSubstructs(mol, patt)
    rm = Chem.MolToSmiles(rm)
    smi1 = Chem.CanonSmiles(rm)
#Text comparison smiles, if they are the same, save them
    for n in range(len(np_smiles)):
        smi2 = canon[n]
        if smi1 == smi2:
            results.append([natural_id[n], np_smiles[n], chem_id[m],smiles[m]])

r = np.array(results)
df = pd.DataFrame(r)
df.to_csv('MMP_match.csv',index=False)

