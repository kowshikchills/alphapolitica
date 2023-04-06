from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import sys
from tqdm import tqdm
import pandas as pd

device = "cpu"
tokenizer = AutoTokenizer.from_pretrained("humarin/chatgpt_paraphraser_on_T5_base")
model = AutoModelForSeq2SeqLM.from_pretrained("humarin/chatgpt_paraphraser_on_T5_base").to(device)

start = int(sys.argv[1])
end = int(sys.argv[2])
print('start', sys.argv[1])
print('end', sys.argv[2])

def paraphrase(
    question,
    num_beams=5,
    num_beam_groups=5,
    num_return_sequences=5,
    repetition_penalty=10.0,
    diversity_penalty=3.0,
    no_repeat_ngram_size=2,
    temperature=0.7,
    max_length=128
):
    input_ids = tokenizer(
        f'paraphrase: {question}',
        return_tensors="pt", padding="longest",
        max_length=max_length,
        truncation=True,
    ).input_ids
    outputs = model.generate(
        input_ids, temperature=temperature, repetition_penalty=repetition_penalty,
        num_return_sequences=num_return_sequences, no_repeat_ngram_size=no_repeat_ngram_size,
        num_beams=num_beams, num_beam_groups=num_beam_groups,
        max_length=max_length, diversity_penalty=diversity_penalty
    )
    res = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    return res

df_trans = pd.read_csv('../data/kowshik_file_translated.csv')
del df_trans['Unnamed: 0']
del df_trans['sno']
df_trans = df_trans[start:end]
para_phrased = []
for i in tqdm(df_trans['translated'].values):
    try:
        para_phrased.append(paraphrase(i))
    except:
        para_phrased.append(['None'])
df_trans['para_phrased'] = para_phrased
df_trans.to_csv('../data/kowshik_file_translated_para_phrased_' + str(start) +'_' +str(end) + '.csv')