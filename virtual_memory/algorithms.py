def fifo_algorithm(pages, num_frames):
    memory = []
    steps = []
    faults, hits = 0, 0
    for p in pages:
        is_fault = False
        if p not in memory:
            is_fault = True
            faults += 1
            if len(memory) < num_frames:
                memory.append(p)
            else:
                memory.pop(0)
                memory.append(p)
        else:
            hits += 1
        steps.append((list(memory), is_fault))
    return steps, faults, hits


def lru_algorithm(pages, num_frames):
    memory = []
    steps = []
    faults, hits = 0, 0
    usage_history = []
    for p in pages:
        is_fault = False
        if p not in memory:
            is_fault = True
            faults += 1
            if len(memory) < num_frames:
                memory.append(p)
            else:
                lru_page = usage_history[0]
                for x in usage_history:
                    if x in memory:
                        lru_page = x
                        break
                memory.remove(lru_page)
                memory.append(p)
        else:
            hits += 1
            usage_history.remove(p)
        usage_history.append(p)
        steps.append((list(memory), is_fault))
    return steps, faults, hits


def optimal_algorithm(pages, num_frames):  # Tinanggal ang self,
    memory = []
    steps = []
    faults, hits = 0, 0
    for i, p in enumerate(pages):
        is_fault = False
        if p not in memory:
            is_fault = True
            faults += 1
            if len(memory) < num_frames:
                memory.append(p)
            else:
                idx_to_replace = -1
                farthest = i
                for j, mem_page in enumerate(memory):
                    try:
                        next_use = pages.index(mem_page, i + 1)
                    except ValueError:
                        next_use = float('inf')
                    if next_use > farthest:
                        farthest = next_use
                        idx_to_replace = j
                if idx_to_replace == -1: 
                    memory[0] = p
                else:
                    memory[idx_to_replace] = p
        else:
            hits += 1
        steps.append((list(memory), is_fault))
    return steps, faults, hits


def counting_algorithm(pages, num_frames, mode="LFU"):  # Tinanggal ang self,
    memory = []
    steps = []
    faults, hits = 0, 0
    counts = {}
    
    for p in pages:
        counts[p] = counts.get(p, 0) + 1
        is_fault = False
        
        if p not in memory:
            is_fault = True
            faults += 1
            if len(memory) < num_frames:
                memory.append(p)
            else:
                target_page = memory[0]
                target_count = counts[target_page]
                
                for mem_page in memory:
                    if mode == "LFU" and counts[mem_page] < target_count:
                        target_count = counts[mem_page]
                        target_page = mem_page
                    elif mode == "MFU" and counts[mem_page] > target_count:
                        target_count = counts[mem_page]
                        target_page = mem_page
                        
                memory.remove(target_page)
                memory.append(p)
        else:
            hits += 1
            
        steps.append((list(memory), is_fault))
    return steps, faults, hits