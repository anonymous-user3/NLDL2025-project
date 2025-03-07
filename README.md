# Graph Neural Networks for Trustworthy Molecular Property Prediction using Substructure-Mask-Explanations and Uncertainty Quantification

This repository contains the code for my project titled "Graph Neural Networks for Trustworthy Molecular Property Prediction using Substructure-Mask-Explanations and Uncertainty Quantification", for the NLDL winter school 2025. This repository is based on previous work on Substructure-Mask Explanations for molecular property prediction, which can be found here https://github.com/wzxxxx/Substructure-Mask-Explanation


## Installation Guide

#### Clone repository

```
git clone https://github.com/anonymous-user3/NLDL2025-project.git
```

Given the large size of the codebase, cloning via Git may be interrupted. Alternatively, consider downloading the ZIP file from the website and extracting it for use.

#### Create conda environments

Two different conda environments need to be used, one for running the models and calculating predictions on the GPU, and one for running the evaluation notebook files. You can install the them via their yaml file

```
conda env create -f environment_slurm.yml
conda env create -f environment_UQ_evaluation.yml
```



## Develop the molecular property prediction models 
#### 1. Build graph datasets

Assume that the project is at */root* and therefore the project path is */root/Substructure-Mask-Explanation*.

The task names of datasets used in in this study are: ESOL and Mutagenicity

```
cd /root/Substructure-Mask-Explanation/MaskGNN_interpretation
python build_graph_dataset.py --task_name ESOL
```

After that, the graph datasets will be saved at the */root/Substructure-Mask-Explanation/data/graph_data/*

#### 2. Train the molecular property prediction models (RGCN)

Develop the molecular property prediction models based on the following code:

```
cd /root/Substructure-Mask-Explanation/MaskGNN_interpretation
python Main.py --task_name ESOL
```

This can also be run with the slurm script ```train.sh``` on a cluster.

## XAI: generate explanation using SME
Explanations are generated using substructure-mask-explanations based on meaningful chemical substructures. Here, three different types for substructures are used: BRICS, murcko scaffolds and functional groups.

#### 3. Calculate the attribution of different substructures base on SME

**For reproduction of** **SME**, the calculation of attribution of different datasets are as follows:

```
cd /root/Substructure-Mask-Explanation/MaskGNN_interpretation
python SMEG_explain_for_substructure.py # calculate the prediction of molecules with different substructures masked
python preciction_summary.py # summary the prediction of molecules with different substructures mask
python attribution_calculate.py # calculate the attribution of different substructures
```

To run this on a cluster, you can use the slurm scipts ```test_SMEG_explanations.sh```, ```prediction_summary.sh``` and ```test_attribution_calculation.sh```.


## UQ: evaluate predictions and explanation with uncertainty quantification
Different methods for measuring predictive uncertainties and explanation uncertainties are tested and compared. Finally, the relation between these uncertainties is studied. 
```
cd uncertainty_quantification
```
#### 4. Calculate uncertainties and evaluate their contribution towards trustwothiness 

Run ```ESOL.ipynb``` for the evaluation on the ESOL dataset, and ```mutagenicity.ipynb``` for the evaluation on the mutagenicity dataset respectively. This will automatically produce the plots used in the project report. 

For a visualisation of the explanation on specific molecules, run ```mutagenicity_visualisation.ipynb```.