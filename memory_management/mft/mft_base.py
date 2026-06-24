class MFTBase:


    def __init__(self, blocks):

        self.blocks = blocks



    def allocate(self, process):

        raise NotImplementedError