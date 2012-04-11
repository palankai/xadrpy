import random
random.seed()

def get_random(length, chars):
    res=[]
    for i in range(0,length):
        res.append(random.choice(chars))
    return "".join(res)
