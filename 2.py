# arr = list(map(int, input("Enter array: ").split()))
# unique = list(set(arr))
# unique.sort()
# if len(unique) >= 2:
#     print("Second largest:", unique[-2])
# else:
#     print("No second largest")


# n = int(input("Enter a number:"))
# if (n%2 == 0):
#     print("Even")
# else:
#     print("odd")
    
s = input("Enter: ")
if s == s[::-1]:
    print("Palindrom")
else:
    print("not palindrom")