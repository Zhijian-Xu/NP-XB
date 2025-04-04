import pandas as pd
from rdkit import Chem

#读取天然产物数据库
file1 = pd.read_csv('ETCM_2.csv', header=None, names=['ID', 'SMILES'])
file2 = pd.read_csv('LOTUS.csv', header=None, names=['ID', 'SMILES'])
file3 = pd.read_csv('COCONUT.csv', header=None, names=['ID', 'SMILES'])

#合并数据
combined_df = pd.concat([file1, file2, file3], ignore_index=True)

#SMILES列标准化
canonical_smiles = []
for smiles in combined_df['SMILES']:
    mol = Chem.MolFromSmiles(smiles)
    if mol:
        canonical_smiles.append(Chem.MolToSmiles(mol, isomericSmiles=True))
    else:
        canonical_smiles.append(None)

#添加标准化的SMILES列
combined_df['Canonical_SMILES'] = canonical_smiles

#去除无效列
combined_df = combined_df.dropna(subset=['Canonical_SMILES'])

#根据标准化后的SMILES进行去重
final_df = combined_df.drop_duplicates(subset=['Canonical_SMILES'])

#输出结果
final_df.to_csv('NP-CU.csv', index=False)

print("合并、标准化并去重完成，结果已保存为 'NP-CU.csv'")
