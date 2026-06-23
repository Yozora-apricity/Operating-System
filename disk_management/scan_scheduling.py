from utils import calculate_movement

class SCANScheduler:
    def __init__(self, disk_size=200):
        # Default disk size from 0 to 199
        self.disk_size = disk_size

    def execute(self, head, requests, direction="up"):
        """SCAN (Elevator Algorithm)"""
        left = sorted([r for r in requests if r < head])
        right = sorted([r for r in requests if r >= head])
        sequence = [head]
        
        if direction == "up":
            sequence.extend(right)
            if left: # Go to the end, then reverse
                sequence.append(self.disk_size - 1)
                sequence.extend(reversed(left))
        else: # direction == "down"
            sequence.extend(reversed(left))
            if right: # Go to 0, then reverse
                sequence.append(0)
                sequence.extend(right)
                
        return {"sequence": sequence, "total_movement": calculate_movement(sequence)}