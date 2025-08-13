# Zhuyin Fixer 
# 功能:
#       將忘記切換輸入法導致的英文亂碼轉換為注音符號，
#       再將注音符號轉換成繁體中文。
#       支援詞語配對，盡可能地將注音轉換成完整詞語。

import json
import tkinter as tk


def ChineseDictFile():
    """讀取中文字詞典檔案"""
    with open("ChineseDictionary.json", "r", encoding="utf-8") as f:
        return json.load(f)

def fix2zhuyin(text):
    """將亂碼字串轉換成注音符號列表，並以聲調當作分界"""
    with open("Zhuyin_mapping.json", "r", encoding="utf-8") as f:
        mapping = json.load(f)
        
    word = ""
    result = []
    for char in text:
        if char in [" ", "6", "3", "4", "7"]:   # 聲調，空格指一聲(陰平聲)
            word += mapping.get(char, f"{char}")
            result.append(word)
            word = ""
        else:
            word += mapping.get(char, f"{char}")
            
    if word != "":
        result.append(word)
        
    return result

        
def WordSplit(wordlist):
    """使用最大匹配演算法分割注音成詞語"""
    i = 0
    length = len(wordlist)
    result = []
    while i < length:
        matched = False
        for j in range((length - i), 0, -1):
            temp = wordlist[i:i+j]
            tempwords = "".join(temp)
            if tempwords in ChineseDict:
                result.append(tempwords)
                i += j
                matched = True
                break
                
        if not matched:     # 無匹配時，當作單字
            result.append(wordlist[i])
            i += 1
            
    return result
    
def fix2Chinese(zhuyinWords):
    """將分割後的注音詞語轉換成繁體中文詞語"""
    text = ""
    for word in zhuyinWords:
        text += ChineseDict.get(word, f"{word}")
        
    return text

if __name__ == "__main__":
    InputText = input("Please type wrong characters:")
    zhuyin = fix2zhuyin(InputText)
    print(f"Transfer to Zhuyin is: {zhuyin}")
    ChineseDict = ChineseDictFile()
    words = WordSplit(zhuyin)
    print(f"Transfer to Words is: {words}")
    ChineseText = fix2Chinese(words)
    print(f"Transfer to Chinese is: {ChineseText}")
    