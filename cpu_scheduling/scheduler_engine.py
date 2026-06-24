import copy

class SchedulerEngine:
    """Handles the pure scheduling algorithms logic independently from the GUI."""
    @staticmethod
    def simulate(original_processes, mode, time_quantum):
        processes = [copy.deepcopy(p) for p in original_processes]
        current_time = 0
        completed = 0
        n = len(processes)
        gantt_chart = []
        
        rr_queue = []
        visited = [False] * n