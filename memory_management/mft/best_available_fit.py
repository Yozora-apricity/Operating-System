from mft.mft_base import MFTBase



class BestAvailableFit(MFTBase):


    def allocate(self, process):

        available = [
            b for b in self.blocks
            if b.is_free()
        ]


        if not available:

            return False



        block = max(
            available,
            key=lambda x:x.size
        )



        if block.size >= process.size:

            block.allocate(process)
            return True


        return False