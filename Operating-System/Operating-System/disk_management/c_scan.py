from utils import calculate_movement

class CSCANScheduler:
    def __init__(self, disk_size=200):
        self.disk_size = disk_size

    def execute(self, head, requests, direction="up"):
        """Circular SCAN"""
        left = sorted([r for r in requests if r < head])
        right = sorted([r for r in requests if r >= head])
        sequence = [head]
        
        if direction == "up":
            sequence.extend(right)
            if left: # Hit end, jump to 0, continue up
                sequence.append(self.disk_size - 1)
                sequence.append(0)
                sequence.extend(left)
        else:
            sequence.extend(reversed(left))
            if right: # Hit 0, jump to end, continue down
                sequence.append(0)
                sequence.append(self.disk_size - 1)
                sequence.extend(reversed(right))
                
        return {"sequence": sequence, "total_movement": calculate_movement(sequence)}