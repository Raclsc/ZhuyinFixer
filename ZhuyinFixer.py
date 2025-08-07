# Zhuyin Fixer 
# V輸入亂碼 > V比對mapping > V逐個轉換成注音 > V根據音標分割單字 > 比對Dictionary > 轉換成中文詞 > 組合成一句話 > 輸出結果

'''
假設7個字"ji3vu;3ul4t 1u/ fu6xup6"，猜分成單字["ji3", "vu;3", "ul4", "t ", "1u/ ", "fu6", "xup6"],
根據按鍵位置轉換成注音符號['ㄨㄛˇ', 'ㄒㄧㄤˇ', 'ㄧㄠˋ', 'ㄔ-', 'ㄅㄧㄥ-', 'ㄑㄧˊ', 'ㄌㄧㄣˊ'], 
以最大字數嘗試轉換成繁體中文詞語, [0:7]比對失敗, [0:6]比對失敗, [0:5]比對失敗......, [0:2]比對失敗, [0:1]比對出中文字["我"],
[i,j], i = 0 ~ 7(max length), j = 7 ~ 1,
接著第二次從i = 1 ~ 7, j = 7 ~ 2, [1:7]比對失敗, [1:6]比對失敗......, [1:4]比對失敗, [1:3]比對出中文字["想要"],
接著第三次從i = 3 ~ 7, j = 7 ~ 4, [3:7]比對失敗, [3:6]比對失敗, [3:5]比對失敗, [3:4]比對出中文字["吃"],
接著第四次從i = 4 ~ 7, j = 7 ~ 5, [4:7]比對出中文字["冰淇淋"],
最後組合所有詞語並輸出"我想要吃冰淇淋"
'''

import json


def fix2zhuyin(text):
    with open("Zhuyin_mapping.json", "r", encoding="utf-8") as f:
        mapping = json.load(f)
        
    word = ""
    result = []
    for char in text:
        if char in [" ", "6", "3", "4", "7"]:
            word += mapping.get(char, "?")
            result.append(word)
            word = ""
        else:
            word += mapping.get(char, "?")
            
    if word != "":
        result.append(word)
        
    return result

def ChineseDictFile():
    with open("ChineseDictionary.json", "r", encoding="utf-8") as f:
        return json.load(f)
        
def WordSplit(wordlist):
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
                
        if not matched:
            result.append(wordlist[i])
            i += 1
            
    return result

if __name__ == "__main__":
    InputText = input("Please type wrong characters:")
    zhuyin = fix2zhuyin(InputText)
    print("Transfer to Zhuyin is: %s" %(zhuyin))
    ChineseDict = ChineseDictFile()
    words = WordSplit(zhuyin)
    print("Transfer to Words is: %s" %(words))
    