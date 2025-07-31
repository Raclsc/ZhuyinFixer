# Zhuyin Fixer 
import json


def fix2zhuyin(text):
    result = ""
    for char in text:
        result += mapping.get(char, "?")
    
    return result


if __name__ == "__main__":
    with open("Zhuyin_mapping.json", "r", encoding="utf-8") as f:
        mapping = json.load(f)
        
    InputText = input("Please type wrong characters:")
    zhuyin = fix2zhuyin(InputText)
    print("Transfer to Zhuyin is: %s" %(zhuyin))