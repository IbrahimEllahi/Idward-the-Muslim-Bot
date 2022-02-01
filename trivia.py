import json, requests
from random import shuffle


def remove_tags(text):
  # Removes html tags from string
  
  data = text
  
  if '&' in data:

    data = data.replace(
      data[data.index('&') : data.index(';')+1],
      ''
    )

    data = remove_tags(data)

  return data

def gen_question():


  data = json.loads(requests.get('https://opentdb.com/api.php?amount=1').text)['results'][0]


  question = remove_tags(data['question'])
  answer = remove_tags(data['correct_answer'])
  options = [remove_tags(opt) for opt in data['incorrect_answers']]
  options.append(answer)
  shuffle(options)

  return [question, answer, options]
