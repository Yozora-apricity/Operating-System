from mft.mft_base import MFTBase



class BestFit(MFTBase):


    def allocate(self, process):

        available = [
            b for b in self.blocks
            if b.is_free()
            and b.size >= process.size
        ]


        if not available:

            return False



        best = min(
            available,
            key=lambda x:x.size
        )


        best.allocate(process)

        return True