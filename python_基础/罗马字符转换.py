def romanToInt(s: str) -> int:
    # 1. 建立字符到数值的映射
    roman_map = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000
    }
    
    total = 0

    for i in range(len(s)):
        val = roman_map[s[i]]
        
        if i < len(s) - 1 and val < roman_map[s[i+1]]:
            total -= val
        else:
            total += val
    
    return total


if __name__ == "__main__":
    # 测试用例
    print(romanToInt("III"))      # 3
    print(romanToInt("IV"))       # 4
    print(romanToInt("IX"))       # 9
    print(romanToInt("LVIII"))    # 58
    print(romanToInt("MCMXCIV"))  # 1994
