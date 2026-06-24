import random

from models.process import Process



def generate_process():

    number=random.randint(1,100)

    size=random.randint(50,500)


    return Process(
        f"P{number}",
        size
    )