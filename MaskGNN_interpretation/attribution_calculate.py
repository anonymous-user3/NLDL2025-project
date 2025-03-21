import pandas as pd
import numpy as np


import pandas as pd
import os

for task_name in ['ESOL', 'Mutagenicity']:
# for task_name in ['Mutagenicity_data_hERG_task']:

    print("Calculating attribution scores for: ", task_name)
    for sub_type in ['fg', 'murcko', 'brics', 'brics_emerge', 'murcko_emerge']:
    #for sub_type in ['fg']:
        attribution_result = pd.DataFrame()
        print('{} {}'.format(task_name, sub_type))
        result_sub = pd.read_csv('../prediction/summary/{}_{}_prediction_summary.csv'.format(task_name, sub_type)) # results for substructure masks
        result_mol = pd.read_csv('../prediction/summary/{}_{}_prediction_summary.csv'.format(task_name, 'mol'))    # results for unmasked molecules

        # data cleaning ________________-----------------____________________
        smis_sub = result_sub['smiles'].tolist()
        smis_mol = result_mol['smiles'].tolist()

        #check if every smiles that is in the substructure results is also in the molecule results
        for smi in smis_sub:
            if smi not in smis_mol:
                print("smi not in smis_mol:", smi)
                # in this case, delete the row from the substructure results
                result_sub = result_sub[result_sub['smiles'] != smi]

        # ________________-----------------____________________
        mol_pred_mean_list_for_sub = [result_mol[result_mol['smiles'] == smi]['pred_mean'].tolist()[0] for smi in
                                 result_sub['smiles'].tolist()]
        mol_pred_std_list_for_sub = [result_mol[result_mol['smiles'] == smi]['pred_std'].tolist()[0] for smi in
                                 result_sub['smiles'].tolist()]
        attribution_result['smiles'] = result_sub['smiles']
        attribution_result['label'] = result_sub['label']
        attribution_result['sub_name'] = result_sub['sub_name']
        attribution_result['group'] = result_sub['group']
        attribution_result['sub_pred_mean'] = result_sub['pred_mean']
        attribution_result['sub_pred_std'] = result_sub['pred_std']
        attribution_result['mol_pred_mean'] = mol_pred_mean_list_for_sub
        attribution_result['mol_pred_std'] = mol_pred_std_list_for_sub
        sub_pred_std_list = result_sub['pred_std']
        attribution_result['attribution'] = attribution_result['mol_pred_mean'] - attribution_result['sub_pred_mean']
        attribution_result['attribution_normalized'] = (np.exp(attribution_result['attribution'].values) - np.exp(
            -attribution_result['attribution'].values)) / (np.exp(attribution_result['attribution'].values) + np.exp(
            -attribution_result['attribution'].values))
        dirs = '../prediction/attribution/'
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        attribution_result.to_csv('../prediction/attribution/{}_{}_attribution_summary.csv'.format(task_name, sub_type), index=False)


