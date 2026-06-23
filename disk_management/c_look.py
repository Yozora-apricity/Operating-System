from utils import calculate_movement

class CLOOKScheduler:
    def execute(self, head, requests, direction="up"):
        """Circular LOOK"""
        left = sorted([r for r in requests if r < head])
        right = sorted([r for r in requests if r >= head])
        sequence = [head]
        
        if direction == "up":
            sequence.extend(right)
            sequence.extend(left)
        else:
            sequence.extend(reversed(left))
            sequence.extend(reversed(right))
            
        return {"sequence": sequence, "total_movement": calculate_movement(sequence)}