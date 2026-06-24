class FirstFit:


    def __init__(self, blocks):

        self.blocks = blocks



    def allocate(self, process):


        for block in self.blocks:


            if block.process is None:


                if block.size >= process.size:


                    block.process = process

                    return True



        return False