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

        while completed < n:
            if mode == "RR":
                for i, p in enumerate(processes):
                    if p.arrival_time <= current_time and not visited[i] and p.remaining_time > 0:
                        rr_queue.append(p)
                        visited[i] = True
                        
            available = [p for p in processes if p.arrival_time <= current_time and p.remaining_time > 0]
            
            if (mode != "RR" and not available) or (mode == "RR" and not rr_queue):
                future = [p for p in processes if p.remaining_time > 0]
                if future:
                    next_arrival = min(p.arrival_time for p in future)
                    gantt_chart.append(("Idle", current_time, next_arrival))
                    current_time = next_arrival
                else:
                    current_time += 1
                continue

            if mode == "FCFS":
                selected = min(available, key=lambda x: x.arrival_time)
                time_to_run = selected.remaining_time
            elif mode == "SJF_NON_PREEMP":
                selected = min(available, key=lambda x: x.burst_time)
                time_to_run = selected.remaining_time
            elif mode == "SJF_PREEMP":
                selected = min(available, key=lambda x: x.remaining_time)
                time_to_run = 1
            elif mode == "PRIORITY_NON_PREEMP":
                selected = min(available, key=lambda x: x.priority)
                time_to_run = selected.remaining_time
            elif mode == "PRIORITY_PREEMP":
                selected = min(available, key=lambda x: x.priority)
                time_to_run = 1
            elif mode == "RR":
                selected = rr_queue.pop(0)
                time_to_run = min(time_quantum, selected.remaining_time)
                if selected.start_time == -1:
                selected.start_time = current_time
                
            if gantt_chart and gantt_chart[-1][0] == selected.pid:
                gantt_chart[-1] = (selected.pid, gantt_chart[-1][1], current_time + time_to_run)
            else:
                gantt_chart.append((selected.pid, current_time, current_time + time_to_run))
                
            for _ in range(time_to_run):
                current_time += 1
                if mode == "RR":
                    for i, p in enumerate(processes):
                        if p.arrival_time <= current_time and not visited[i] and p.remaining_time > 0:
                            rr_queue.append(p)
                            visited[i] = True
                            
            selected.remaining_time -= time_to_run
            
            if selected.remaining_time == 0:
                selected.completion_time = current_time
                selected.turnaround_time = selected.completion_time - selected.arrival_time
                selected.waiting_time = selected.turnaround_time - selected.burst_time
                completed += 1
            elif mode == "RR":
                rr_queue.append(selected)

        return processes, gantt_chart