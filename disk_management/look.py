from utils import calculate_movement

class LOOKScheduler:
    def execute(self, head, requests, direction="up"):
        """LOOK Algorithm"""
        left = sorted([r for r in requests if r < head])
        right = sorted([r for r in requests if r >= head])
        sequence = [head]
        
        if direction == "up":
            sequence.extend(right)
            sequence.extend(reversed(left))
        else:
            sequence.extend(reversed(left))
            sequence.extend(right)
            
        return {"sequence": sequence, "total_movement": calculate_movement(sequence)}