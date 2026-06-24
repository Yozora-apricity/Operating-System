class MemoryBlock:


    def __init__(self, block_id, size):

        self.block_id = block_id
        self.size = size
        self.process = None



    def is_free(self):

        return self.process is None



    def allocate(self, process):

        self.process = process

        process.allocate(
            self.block_id
        )



    def free(self):

        self.process=None



    def __str__(self):

        if self.process:

            return (
                f"Partition {self.block_id}: "
                f"{self.process.name} "
                f"{self.process.size}KB"
            )


        return (
            f"Partition {self.block_id}: FREE "
            f"{self.size}KB"
        )