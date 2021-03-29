import random
import string

if __name__ == '__main__':
    f = open('in.txt', 'a')
    for i in range(100000):
        res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=random.randint(10, 50)))
        f.write(res + '\n')
