#build and store a deck, and get updates on prices.
import urllib
import re
#import urllib2

from bs4 import BeautifulSoup
import requests

class MagicDeck:
  #lets first build the deck
  
  def __init__(self):
    self.deck = []
    self.run = True
    self.checkDeck()
    
    
    
    
  def checkDeck(self):
    self.deckfile = open('magicdeck.txt', 'r')
    if self.deckfile.read() == '':
      print 'empty file'
      self.deckfile.close()
      self.populateDeck()
    else:
      print 'file exists and is populated'
      
      while self.run == True:
        a = raw_input('Add, Remove, Clear, View, Price Card, Price Deck, Quit: ')
        if a == 'Add':
          self.populateDeck()
        elif a == 'Remove':
          #remove card method
          self.removeCard()
        elif a == 'Clear':
          #clear list method
          self.clearDeck()
        elif a == 'View':
          self.readDeck()
        elif a == 'Price Card':
          self.priceCard()
        elif a == 'Price Deck':
          self.getDeckPrice()
        else:
          self.run = False
          #quit()
          break
        
  def clearDeck(self):
    self.deckfile = open('magicdeck.txt', 'w').close()
      
  def removeCard(self):
    self.deckfile = open('magicdeck.txt', 'r')
    lines = self.deckfile.readlines()
    self.deckfile.close()
    self.deckfile = open('magicdeck.txt', 'w')
    remCard = raw_input('Name of card to remove: ')
    for line in lines:
      if line != remCard+'\n':
        self.deckfile.write(line)
    self.deckfile.close()
    
      
    
  def populateDeck(self):
    self.deckfile = open('magicdeck.txt', 'a')
    print 'type \'Quit\' to quit'
    newcard = ''
    while newcard != 'Quit':
      newcard = raw_input("Enter name of card to add: ")
      newcardset = raw_input("From what set? ")
      if newcard == 'Quit':
        self.deckfile.close()
        break
      else:
        self.deckfile.write(newcard + ' : ' + newcardset + '\n')
    
    
  def readDeck(self):
    self.deckfile = open('magicdeck.txt', 'r')
    i = 0
    for line in self.deckfile:
      print line
      i += 1
    print 'File contains ' + str(i) + ' cards'  
    self.deckfile.close()
    
  def priceCard(self):
    a = 0
    url = 'http://www.mtggoldfish.com/price/'
    card = raw_input("Name of card: ")
    set = raw_input("What Set? ")
    cardcor = ''
    setcor = ''
    for i in card:
      if i == ',':
        cardcor += ''
      elif i != ' ':
        cardcor += i
      elif i == ' ':
        cardcor += '+'
      
    for i in set:
      if i != ' ':
        setcor += i
      elif i == ' ':
        setcor += '+'
    corurl = url + setcor + '/' + cardcor + '#paper'

    htmlfile = urllib.urlopen(corurl)
    htmltext = htmlfile.read()
    #print htmltext
    soup = BeautifulSoup(htmltext, "html.parser")
    pricebox = soup.find_all('div', class_="price-box-price")
    pstr = str(pricebox[1])
    p = ''
    for i in pstr:
      if i.isdigit():
        p += str(i)
      elif i == '.':
        p += '.'
    print p
    
  def getCardPrice(self, set, card):
    url = 'http://www.mtggoldfish.com/price/'
    cardcor = ''
    setcor = ''
    for i in card:
      if i == ',' or i == '\'':
        cardcor += ''
      elif i != ' ':
        cardcor += i
      elif i == ' ':
        cardcor += '+'
      
    for i in set:
      if i != ' ':
        setcor += i
      elif i == ' ':
        setcor += '+'
    
    corurl = url + setcor + '/' + cardcor + '#paper'
    htmlfile = urllib.urlopen(corurl)
    htmltext = htmlfile.read()
    soup = BeautifulSoup(htmltext, "html.parser")
    pricebox = soup.find_all('div', class_="price-box-price")
    try:
      pstr = str(pricebox[1])
      p = ''
      for i in pstr:
        if i.isdigit():
          p += str(i)
        elif i == '.':
          p += '.'
      return p
    except:
      print 'error'
  def getDeckPrice(self):
    self.deckfile = open('magicdeck.txt', 'r')
    lines = self.deckfile.readlines()
    card = ''
    set = ''
    n = 0
    dex = 0
    sum = 0.00
    for line in lines:
      for index, char in enumerate(line):
        if char == ':':
          dex = index
      for index, char in enumerate(line):
        if index < dex - 1:
          card += str(char)
        elif index > dex + 1:
          set += str(char)
      set = set[:-1]
      n += 1
      sum += float(self.getCardPrice(set, card))
      print str(n)
      card = ''
      set = ''
      dex = 0
    print sum  
    self.deckfile.close()   
      
    
    
def main():
  print 'Welcome to Christopher\'s Deck Utility'
  deck = MagicDeck()
  
  
if __name__ == '__main__':
  main()