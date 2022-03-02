import ktrain.text as txt
import ktrain

#modelpath = 'C:\\Users\\dirksonar\\Documents\\Data\\BERTfinal\\predictor_seed256_bert\\'
modelpath = 'C:\\Users\\dirksonar\\Documents\\Data\\BERTfinal\\modelpredictor1_seed256\\'

#modelpath = 'C:\\Users\\dirksonar\\Documents\\Github\\Models\\ADR_extraction_patient_forum\\'

model = ktrain.load_predictor(modelpath)

print(model.predict("I am so nauseous"))