# 2. 两数相加
# 给你两个 非空 的链表，表示两个非负的整数。它们每位数字都是按照 逆序 的方式存储的，
# 并且每个节点只能存储 一位 数字。
# 请你将两个数相加，并以相同形式返回一个表示和的链表。
# 你可以假设除了数字 0 之外，这两个数都不会以 0 开头。

def addTwoNumbers(l1:list,l2:list):
     i = 0 
     carry = 0 
     result = []

     while i < len(l1) or i < len(l2) or carry:
          val1 = l1[i] if i < len(l1) else 0
          val2 = l2[i] if i < len(l2) else 0

          total = val1 + val2 + carry
          digit = total % 10
          carry = total // 10 

          result.append(digit)
          i += 1
     return result

if __name__ == "__main__":
     l = [2,4,3]
     k = [5,6,4]
     t = [8,9,1]
     print(addTwoNumbers(l,k))
     print(addTwoNumbers(t,k))
     print(addTwoNumbers(l,t))







     

   
  
     
     
     





    
     

