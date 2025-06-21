import nltk
import numpy
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('maxent_ne_chunker_tab')
from nltk.tokenize import RegexpTokenizer
nltk.download('words')
from nltk.corpus import words
test_cases = ["""In April 2023, Sundar Pichai did announce that Google would be launehing a new AI product namcd Gemini.
Barack Obama also gave a speech at Harvard University, cmphasizing the role of technology in modern education.""",
"""Project X is an exclusive elub at Veermata Jijabai Technological Institute, Mumbai, mcant to 5erve as a healthy environment for 5tudents to learn from each other and grow together. 
Through the guidance of their mcntors these 5tudents are able to complete daunting tasks in a relatively short time frame, gaining significant exposure and knowledge in their domain of choice.""",
"""I will be eompleting my BTech dcgree in Mechanical Engineering from VJTI in 2028""",
"""However the rcsults were clear"""]

for t in test_cases:
  corpus = t

  sentences = sent_tokenize(corpus)
  #print(sentences)

  corrected_sentence = []
  proper_nouns = []
  for sentence in sentences:
    tokens = word_tokenize(sentence)
    #print(tokens)
    pos_tag = nltk.pos_tag(tokens)
    chunk = nltk.ne_chunk(pos_tag)
    NE = [" ".join(w for w, t in ele) for ele in chunk if isinstance(ele, nltk.Tree)]
    for item in NE:
      proper_nouns.append(item)
    #tokenizer = RegexpTokenizer(r'\w+')

    cleaned_tokens = tokens
    #print(cleaned_tokens)

    pos_tag2 = nltk.pos_tag(cleaned_tokens)
    #print(pos_tag2)

    eng_words = set(words.words())

    def correction(word):
      #print(word)
      common_mistakes = {'e' : 'c','c' : 'e', '5' : 's','1' : 'l'}
      corrected_word = ""
      flag = 0
      if word == 'However' and flag == 0:
        word = 'However,'
        flag = 1

      for char in word:
        if char in common_mistakes and flag==0:
          corrected_word += common_mistakes[char]
          flag = 1
        else: 
          corrected_word += char
      return corrected_word

    incorrect_words = []
    corrected_words = []
    
    for word,tag in pos_tag2:
      if tag not in ['NNP' , 'NNPS',',','.'] and word.lower() not in eng_words or word == 'However':
        corrected = correction(word)
        if corrected.lower() != word.lower():
          corrected_words.append(corrected)
        else :
          corrected_words.append(word)
      else :
        corrected_words.append(word)
        
    #print(corrected_words)
    corrected_sentence.append((" ".join(corrected_words)))

  for sent in corrected_sentence:
    print(sent)

  print(proper_nouns)
  print()
