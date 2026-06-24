class WorstFit:


    def __init__(self, blocks):

        self.blocks = blocks



    def allocate(self, process):


        worst = None



        for block in self.blocks:


            if block.process is None:


                if block.size >= process.size:


                    if worst is None or block.size > worst.size:


                        worst = block





        if worst:


            worst.process = process

            return True



        return False