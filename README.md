# CHyMer
(or Clinical Hypothesis Miner). 

The goal of this pipeline is to uncover adverse drug responses from patient experiences that are shared online. 

## Usage

Requirements can be found in requirements.txt

python main.py --norm_model_dir <NORMALIZATION MODEL DIRECTORY> --datapath ./data/ExampleDataInput.tsv --ner_model_dir <NER MODEL DIR> 
  
Other options included in the main script are: 
  -- restricted_drugs 
  
  This command allows you to restrict which drugs ADR can be linked to. The restricted drugs should be provided in /data/restricted_druglist.txt file
  
  -- output_dir <OUTPUT_DIR>
  
  This command allows you to change the default output directory (./output)
  
  -- use_cuda 
  
  Adding this argument allows the script to use available GPU power. By default GPU is not used. 
  
  --dictionary_path <DICTIONARY_PATH>
  
  This command allows you to specify an alternative concept dictionary for ADR normalization. Default is /data/ConceptDictionary.txt
  

## What is included? 

Due to privacy restrictions, our data could not be shared and is not included. Nonetheless a dashboard of results can be found at: https://dashboard-gist-adr.herokuapp.com/

A full concept dictionary is also not included due to restrictions imposed by SNOMED-CT. We provide a small concept dictionary as an example in this script. The full concept dictionary can be requested upon demonstration of access to SNOMED-CT from dr. Verberne (s.verberne@liacs.leidenuniv.nl) 
  
Models necessary for this pipeline can be found at:
https://huggingface.co/annedirkson
  
## Further references

Part of this pipeline is an adaption of the work by Sung et al. (BioSyn): https://github.com/dmis-lab/BioSyn

This pipeline and its creation is described further in: 
Anne Dirkson, Suzan Verberne, Wessel Kraaij, Gerard van Oortmerssen & Hans Gelderblom. Automated gathering of real-world evidence from online patient forums can complement pharmacovigilance for rare cancers. Submitted. 

