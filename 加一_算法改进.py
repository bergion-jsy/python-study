
aaaa= [9]
def plusOne(digits):
        i = len(digits) - 1
        while i >= 0 and digits[i] == 9:
            digits[i] = 0
            i -= 1
        if i >= 0:
            digits[i] += 1
            
        else:
            digits = [1] + digits
        return digits

print(plusOne(aaaa))
            




        
        