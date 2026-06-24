from mft.mft_base import MFTBase


class FirstFit(MFTBase):


    def allocate(self, process):

        for block in self.blocks:

            if block.is_free() and block.size >= process.size:

                block.allocate(process)
                return True


        return False