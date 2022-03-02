

from biosyn.biosyn import BioSyn
# model_dir = 'C:\\Users\\dirksonar\\Documents\\Github\\Models\\BERT_embeddings_ADR_normalization\\'
model_dir = 'C:\\Users\\dirksonar\\Documents\\Github\\Models\\Out_modern\\'

max_length = 25
use_cuda=False

biosyn = BioSyn().load_model(
    path=model_dir,
    max_length=max_length,
    use_cuda=use_cuda
)
