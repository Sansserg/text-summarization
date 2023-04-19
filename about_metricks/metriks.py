from rouge_metric import PyRouge
from tkinter import filedialog
path_to_file = filedialog.askopenfilename()


summed_ook = open(path_to_file, "r")

suum_text = summed_ook.readlines()

# Load summary results
hypotheses = "The Old Arbat is a picturesque pedestrian street in Moscow, running west from Arbat Square (which is part of the Boulevard Ring) towards Smolenskaya Square (which is part of the Garden Ring). The Old Arbat has the reputation of being Moscow's most touristy street, with lots of entertainment and souvenirs sold. It is distinct from the New Arbat, a street running parallel to it and lined with Soviet skyscrapers made of steel, concrete, and glass. During the 16th and 17th centuries, the neighbourhood was graced with elegant churches, notably the one featured in Vasily Polenov's celebrated painting A Courtyard in Moscow (1879). In the 18th century, the Arbat came to be regarded by the Russian nobility as the most prestigious living area in Moscow. Probably the most original monument to this new trend is the Melnikov Mansion. Simultaneously, most of the Arbat's churches were demolished, including that of St Nicholas, regarded as one of the finest examples of Godunov style. It has several notable statues, including one to Princess Turandot in front of the Vakhtangov Theatre and another to Soviet-era folk singer, bard, and poet, Bulat Okudzhava, who wrote several poignant songs about the Arbat. To this day, Russian youth frequently gather on the Arbat to play the songs of Tsoi and other Russian songwriters.".split(".")
references = suum_text

print(hypotheses, references, sep="\n")



# Evaluate document-wise ROUGE scores
rouge = PyRouge(rouge_n=(1,2, 4), rouge_l=True, rouge_w=True,
                rouge_w_weight=1.2, rouge_s=True, rouge_su=True, skip_gap=4)
scores = rouge.evaluate(hypotheses, references)
print(scores)
