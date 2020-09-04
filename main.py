from newspaper import Article 
import random
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings
warnings.filterwarnings('ignore')

nltk.download('punkt', quiet=True)


article = Article('https://www.mayoclinic.org/diseases-conditions/coronavirus/symptoms-causes/syc-20479963')

article.download()
article.parse()
article.nlp()

covid = article.text


#print(covid)


text = covid
sentence_list = nltk.sent_tokenize(text)

def greeting_response(greeting):
  greeting = greeting.lower()

  bot_greet = ['howdy', 'Hi','hey','hello','hola']
  user_greet = ['wassup', 'Hi','hey','hello','hola']

  for word in greeting:
    if word in user_greet:
      return random.choice(bot_greet)
  return 'greeting done'

def index_sort(list_var):
  length = len(list_var)
  list_index = list(range(0, length))

  x = list_var
  for i in range(length):
    for j in range(length):
      if x[list_index[i]] > x[list_index[j]]:
        temp = list_index[i]
        list_index[i] = list_index[j]
        list_index[j] = temp
  return list_index


def bot_response(user_input):
  user_input = user_input.lower()
  sentence_list.append(user_input)
  bot_response = ''
  cm = CountVectorizer().fit_transform(sentence_list)
  similarity_scores = cosine_similarity(cm[-1], cm)
  similarity_scores_list = similarity_scores.flatten()
  index = index_sort(similarity_scores_list)
  index = index[1:]
  response_flag = 0

  j = 0
  for i in range(len(index)):
    if similarity_scores_list[index[i]] > 0.0:
      bot_response = bot_response + ' ' + sentence_list[index[i]]
      response_flag = 1
      j+=1
    if j > 2:
      break
  if not response_flag:
    bot_response = bot_response + ' ' + 'I apologise, I do not understand, please refer to WHO guidlines'

  sentence_list.remove(user_input)
  return bot_response


#Starting the chat
print('Covid Bot: Covid Chatbot here, I will answer your questions!')
print('Covid Bot: Type bye to exit.')
while(True):
  user_input = input()
  if user_input.lower() == 'bye':
    print('Covid Bot: see you later!')
    break
  else:
    if greeting_response(user_input) != 'greeting done':
      print('Covid Bot: ' + greeting_response(user_input) + '\n')
    else:
      print('Covid Bot: ' + bot_response(user_input) + '\n')
