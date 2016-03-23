import re

def fixPunctuation(sentence):                             #kui lause on " lause lause lasue ? " siis eemaldatakse jutumärgid ( ” , ", “)
  sentence = re.sub('^\s|\s$', '', sentence)
  sentence = re.sub('”', '"', sentence)
  sentence = re.sub('“', '"', sentence)
  if sentence.count('"')== 4 and sentence.endswith('"') and sentence.startswith('"') :      #Sobivad laused "Tere," ütles Peeter "kuidas läheb?".
    return sentence
  if sentence.count('"')== 1 or sentence.count('"')== 3 or sentence.count('"') > 4 :
    sentence = ""
    return sentence
  if sentence.count('"')== 2 and sentence.endswith('"') and sentence.startswith('"'):
    sentence = re.sub('^"|"$', '', sentence)
  sentence = re.sub('\s\s', ' ', sentence)
  sentence = re.sub('^\s|\s$', '', sentence)
  return sentence


sentence = ' " Tere , mdkfsd,  kdf  " jejrwe" kdlfkds" kolsdkf"'
print (fixPunctuation(sentence))
