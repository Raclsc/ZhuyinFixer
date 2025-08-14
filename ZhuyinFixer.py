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
        
    if text[-1] not in ["6", "3", "4", "7"]:    # 最末字不含聲調時，視為一聲(陰平聲)，補空格
        text = text + " "
        
    word = ""
    result = []
    for char in text:
        if char in [" ", "6", "3", "4", "7", "+"]:   # 聲調，空格指一聲(陰平聲)，6、3、4、7分別指二聲、三聲、四聲與輕聲
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

def convert():
    """讀取輸入的亂碼字串依序轉換成注音符號及中文詞語後輸出至表格中"""
    InputText = InputEntry.get("1.0", tk.END).strip().replace("\n", "+")
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
    ChineseDict = ChineseDictFile()
    root = tk.Tk()
    root.title("I Forgot To Change The Input Method. - 注音輸入法")
    
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
    