import pandas as pd
import numpy as np


import pandas as pd
import os

for task_name in ['ESOL', 'Mutagenicity']:

    print("Calculating uncertainty scores for: ", task_name)
    for sub_type in ['fg', 'murcko', 'brics', 'brics_emerge', 'murcko_emerge']:

        print('{} {}'.format(task_name, sub_type))

        uq_result = pd.DataFrame(columns=['smiles', 'label', 'ensemble_pred', 'ensemble_uncertainty', 'UX_highest', 'UX_all', 'UX_weighted', 'UX_scaled'])

        result_sub = pd.read_csv('../prediction/summary/{}_{}_prediction_summary.csv'.format(task_name, sub_type)) # results for substructure masks
        result_mol = pd.read_csv('../prediction/summary/{}_{}_prediction_summary.csv'.format(task_name, 'mol'))    # results for unmasked molecules
        attribution_summary = pd.read_csv('../prediction/attribution/{}_{}_attribution_summary.csv'.format(task_name, sub_type)) # results for substructure masks attributions 

        """
        Calculate the uncertainty of the explanations for each molecule (i.e. for each unique smiles). 
        We use 4 different methods to calculate the uncertainty of the explanations:
        1. UX_highest  : The uncertainty is the maximum uncertainty of the substructure masks for this molecule (i.e. we only care about the uncertainty of the best explanation)
        2. UX_all      : The uncertainty is the sum of the uncertaintie of the different substructure masks for this molecule (i.e. take all possible explanations into account)
        3. UX_weighted : Same as UX_all, but the uncertainty is weighted by the absolute attribution score for each substructure mask
        4. UX_scaled   : Same as UX_weighted, but the weights are the fraction of the absolute attribution score for the substructure masks over all absolution attribution scores for all substructure masks or this molecule
        """

        for smiles in attribution_summary['smiles'].unique():

            # get the label and ensemble prediction for this molecule
            label = result_mol[result_mol['smiles'] == smiles]['label'].values[0]
            ensemble_pred = result_mol[result_mol['smiles'] == smiles]['pred_mean'].values[0]
            
            # the ensemble uncertainty is the variance of the ensemble predictions
            ensemble_uncertainty = result_mol[result_mol['smiles'] == smiles]['pred_std'].values[0] ** 2

            #TODO fix this so that we take the variance of the attributions

            # get the substructure masks for this molecule
            substructures = result_sub[result_sub['smiles'] == smiles]
            # get the attribution summaries for this molecule
            attributions = attribution_summary[attribution_summary['smiles'] == smiles]



            # NEW
            for idx in range(len(substructures)):
                for i in range(10): # number of ensemble members
                    pred_smask = substructures[f'pred_{i+1}'][idx]
                    smiles_smask = substructures['smiles'][idx]
                    pred_mol = result_mol[result_mol['smiles'] == smiles][f'pred_{i+1}'].values[0]

                    attribution_smask_member_i = pred_mol - pred_smask




            # calculate the uncertainty for this molecule
            UX_highest = substructures['pred_std'].max()
            UX_all = substructures['pred_std'].sum()
            UX_weighted = (substructures['pred_std'] * np.abs(attributions['attribution'])).sum()
            UX_scaled = (substructures['pred_std'] * np.abs(attributions['attribution']) / np.abs(attributions['attribution']).sum()).sum()

            # add the results to the dataframe
            #uq_result = uq_result.append({'smiles': smiles, 'UX_highest': UX_highest, 'UX_all': UX_all, 'UX_weighted': UX_weighted, 'UX_scaled': UX_scaled}, ignore_index=True)




        dirs = '../prediction/uncertainty/'
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        uq_result.to_csv('../prediction/uncertainty/{}_{}_uncertainty_summary.csv'.format(task_name, sub_type), index=False)


