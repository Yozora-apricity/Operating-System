from utils import calculate_movement

class FCFSScheduler:
    def execute(self, head, requests):
        """First-Come, First-Served"""
        sequence = [head] + requests.copy()
        return {"sequence": sequence, "total_movement": calculate_movement(sequence)}