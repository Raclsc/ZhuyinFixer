# Zhuyin Fixer 
# 功能:
#       將忘記切換輸入法導致的英文亂碼轉換為注音符號，
#       再將注音符號轉換成繁體中文。
#       支援詞語配對，盡可能地將注音轉換成完整詞語。

import os
import sys
import json
import tkinter as tk
import importlib.metadata


def ResourcePath(filepath):
    """取得打包後的資源路徑"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filepath)
    return os.path.join(os.path.abspath("."), filepath)

def ChineseDictFile():
    """讀取中文字詞典檔案"""
    DictFile = ResourcePath("ChineseDictionary.json")
    with open(DictFile, "r", encoding="utf-8") as f:
        return json.load(f)

def fix2zhuyin(text):
    """將亂碼字串轉換成注音符號列表，並以聲調當作分界"""
    Consonants = ["ㄅ", "ㄆ", "ㄇ", "ㄈ", "ㄉ", "ㄊ", "ㄋ", "ㄌ", "ㄍ", "ㄎ", "ㄏ", 
                  "ㄐ", "ㄑ", "ㄒ", "ㄓ", "ㄔ", "ㄕ", "ㄖ", "ㄗ", "ㄘ", "ㄙ"]
    Medials = ["ㄧ", "ㄨ", "ㄩ"]
    Rhymes = ["ㄚ", "ㄛ", "ㄜ", "ㄝ", "ㄞ", "ㄟ", "ㄠ", "ㄡ", "ㄢ", "ㄣ", "ㄤ", "ㄥ", "ㄦ"]
    Tonal = ["-", "ˊ", "ˇ", "ˋ", "˙"]
    
    DictFile = ResourcePath("Zhuyin_mapping.json")
    with open(DictFile, "r", encoding="utf-8") as f:
        mapping = json.load(f)
        
    if text[-1] not in ["6", "3", "4", "7"]:    # 最末字不含聲調時，視為一聲(陰平聲)，補空格
        text = text + " "
        
    Cona = ""
    Medi = ""
    Rhy = ""
    Ton = ""
    result = []
    for char in text:
        mark = mapping.get(char, f"{char}")
        
        if mark in Consonants:
            Cona = mark
        elif mark in Medials:
            Medi = mark
        elif mark in Rhymes:
            Rhy = mark
        elif mark in Tonal:
            Ton = mark
            word = Cona + Medi + Rhy + Ton
            result.append(word)
            Cona = ""
            Medi = ""
            Rhy = ""
            Ton = ""
        else:
            word = Cona + Medi + Rhy + Ton
            result.append(word)
            Cona = ""
            Medi = ""
            Rhy = ""
            Ton = ""
            result.append(mark)
        
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
        temp = ChineseDict.get(word, f"{word}")
        if word in ChineseDict.keys():      # 如果出現同音字詞預設選用第一個做為轉換的中文詞語
            text += temp[0]
        else:
            text += temp
        
    return text

def convert():
    """讀取輸入的亂碼字串依序轉換成注音符號及中文詞語後輸出至表格中"""
    InputText = InputEntry.get("1.0", tk.END).strip().replace("\n", "+").lower()
    zhuyin = fix2zhuyin(InputText)
    zhuyinWords = WordSplit(zhuyin)
    Chinesetext = fix2Chinese(zhuyinWords)

    ZhuyinLable.config(state="normal")
    ZhuyinLable.delete("1.0", tk.END)
    ZhuyinLable.insert("1.0", " ".join(zhuyin).replace("+ ", "\n"))
    ZhuyinLable.config(state="disabled")
    
    ChineseLable.config(state="normal")
    ChineseLable.delete("1.0", tk.END)
    ChineseLable.insert("1.0", "".join(Chinesetext).replace("+", "\n"))
    ChineseLable.config(state="disabled")


if __name__ == "__main__":
    __version__ = "1.0.1.8-beta"
    ChineseDict = ChineseDictFile()
    root = tk.Tk()
    root.title(f"I Forgot To Change The Input Method. - 注音輸入法 ver.{__version__}")
    
    tk.Label(root, text="請貼上英數字字串:", font=(14)).pack(pady=5)
    InputEntry = tk.Text(root, wrap="char", height=3, width=60, font=(12))
    InputEntry.pack(padx=5, pady=5, fill="both")
    InputEntry.insert("1.0", "hk4g4g4z04")
    
    tk.Button(root, text="轉換", font=(14), background="#B2CCEE", command=convert).pack(padx=5, pady=5, fill="both")

    tk.Label(root, text="注音:", font=(14)).pack(pady=5)
    ZhuyinLable = tk.Text(root, wrap="char", height=3, width=60, font=(12))
    ZhuyinLable.pack(padx=5, pady=5, fill="both")
    ZhuyinLable.insert("1.0", "ㄘㄜˋ ㄕˋ ㄕˋ ㄈㄢˋ")
    
    tk.Label(root, text="中文:", font=(14)).pack(pady=5)
    ChineseLable = tk.Text(root, wrap="char", height=3, width=60, font=(12))
    ChineseLable.pack(padx=5, pady=10, fill="both")
    ChineseLable.insert("1.0", "測試示範")

    root.mainloop()
    