class BestFit:


    def __init__(self, blocks):

        self.blocks = blocks



    def allocate(self, process):


        best = None



        for block in self.blocks:


            if block.process is None:


                if block.size >= process.size:


                    if best is None or block.size < best.size:


                        best = block




        if best:


            best.process = process

            return True



        return False