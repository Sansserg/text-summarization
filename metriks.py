from rouge_metric import PyRouge

rev = open("reveission.txt", "r")
summed_ook = open("Answer_text.txt", "r")

rev_text = rev.readlines()
suum_text = summed_ook.readlines()
print(rev_text)
print(suum_text)

# Load summary results
hypotheses = rev_text
references = suum_text

print(hypotheses)
print(references)

# Evaluate document-wise ROUGE scores
rouge = PyRouge(rouge_n=(1, 2, 4), rouge_l=True, rouge_w=True,
                rouge_w_weight=1.2, rouge_s=True, rouge_su=True, skip_gap=4)
scores = rouge.evaluate(hypotheses, references)
print(scores)