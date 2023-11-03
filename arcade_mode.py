import time
import mss
import numpy
import pytesseract
import pyautogui
import random
from gensim.models.keyedvectors import KeyedVectors

path = PATH_TO_PRETRAINED_WORD_ASC
model = KeyedVectors.load_word2vec_format(path, binary=True)
pytesseract.pytesseract.tesseract_cmd = PATH_TO_TESSERACT
mon = {'top': 100, 'left': 2500, 'width': 800, 'height': 900}
word_mapping = {}
with mss.mss() as sct:
    while True:
        im = numpy.asarray(sct.grab(mon))
        text = pytesseract.image_to_string(im)
        target_word = ""
        for line in text.split("\n"):
            if ">" in line or "»" in line:
                target_word = line
                break
        typeout = ""
        
        target_word = ''.join(char for char in target_word if char.isalpha())
        target_word = target_word.lower()
        if (word_mapping.get(target_word) == None):
            word_mapping[target_word] = []
        
        if (target_word != ""):
            try:
                candidate_word_tuples = model.most_similar(target_word, topn=30)
            except:
                continue
            
            for candidate_word, _ in candidate_word_tuples:
                candidate_word = candidate_word.lower()
                if target_word[:4] == candidate_word[:4] or len(candidate_word) > 10:
                    continue
                output = candidate_word.lower().replace('_', ' ')
                if (output in target_word or target_word in output or target_word == output):
                    continue
                if (candidate_word in word_mapping[target_word]):
                    continue
                word_mapping[target_word].append(candidate_word)
                typeout = candidate_word.lower().replace('_', ' ')
                break
        else:
            continue
        pyautogui.typewrite(typeout, interval=round(random.random() / 8, 2))
        pyautogui.press('enter')
