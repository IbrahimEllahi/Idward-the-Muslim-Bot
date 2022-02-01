import requests
from bs4 import BeautifulSoup
from pprint import pprint
from typing import *
import json



def remove_tags(html):

  # Removes html tags from string
  
  data = html
  
  if '<' in data:

    data = data.replace(
      data[data.index('<') : data.index('>')+1],
      ''
    )

    data = remove_tags(data)

  return data

def get_truth():

  url = "https://fungenerators.com/random/truth-or-dare?option=truth"

  html_data = requests.get(url).text
  info = BeautifulSoup(html_data,'lxml')
  truth = info.find('h2')
  return remove_tags(str(truth))

def get_dare():

  url = "https://fungenerators.com/random/truth-or-dare?option=dare"

  html_data = requests.get(url).text
  info = BeautifulSoup(html_data,'lxml')

  dare = info.find('h2')
  return remove_tags(str(dare))