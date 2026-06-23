from utils import calculate_movement

class SSTFScheduler:
    def execute(self, head, requests):
        """Shortest Seek Time First"""
        sequence = [head]
        pending = requests.copy()
        current_pos = head
        
        while pending:
            # Find the closest request to the current head position
            closest = min(pending, key=lambda x: abs(x - current_pos))
            sequence.append(closest)
            pending.remove(closest)
            current_pos = closest
            
        return {"sequence": sequence, "total_movement": calculate_movement(sequence)}