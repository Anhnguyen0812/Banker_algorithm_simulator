
def read_input(filename):
    """Read input data from file"""
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file.readlines() if line.strip() and not line.strip().startswith('#')]
        
        # First line: number of processes and resources
        n_processes, n_resources = map(int, lines[0].split())
        
        # Second line: available resources
        available = list(map(int, lines[1].split()))
        
        # Next n_processes lines: maximum demand for each process
        max_demand = []
        for i in range(2, 2 + n_processes):
            max_demand.append(list(map(int, lines[i].split())))
        
        # Next n_processes lines: allocated resources for each process
        allocation = []
        for i in range(2 + n_processes, 2 + 2 * n_processes):
            allocation.append(list(map(int, lines[i].split())))
    
    return n_processes, n_resources, available, max_demand, allocation

def calculate_need(max_demand, allocation):
    """Calculate the Need matrix (Max - Allocation)"""
    return [
        [max_demand[i][j] - allocation[i][j] for j in range(len(max_demand[0]))]
        for i in range(len(max_demand))
    ]

def is_safe(available, max_demand, allocation, n_processes, n_resources):
    """Check if the system is in a safe state and return execution steps"""
    # Create work and finish arrays
    work = available.copy()
    finish = [False] * n_processes
    safe_sequence = []
    execution_steps = []
    
    # Calculate need matrix
    need = calculate_need(max_demand, allocation)
    
    # Find a safe sequence
    count = 0
    while count < n_processes:
        found = False
        for i in range(n_processes):
            if not finish[i]:
                can_allocate = True
                for j in range(n_resources):
                    if need[i][j] > work[j]:
                        can_allocate = False
                        break
                
                if can_allocate:
                    # Process can complete, add its resources to work
                    step = {
                        'process': i,
                        'work_before': work.copy(),
                        'allocation': allocation[i].copy(),
                    }
                    
                    for j in range(n_resources):
                        work[j] += allocation[i][j]
                    
                    step['work_after'] = work.copy()
                    execution_steps.append(step)
                    
                    finish[i] = True
                    safe_sequence.append(i)
                    found = True
                    count += 1
        
        if not found:
            break
    
    # Check if all processes finished
    is_safe = all(finish)
    return is_safe, safe_sequence, execution_steps

def request_resources(process_idx, request, available, max_demand, allocation, n_resources):
    """Handle a resource request"""
    # Check if request exceeds max claim
    need = calculate_need(max_demand, allocation)
    for j in range(n_resources):
        if request[j] > need[process_idx][j]:
            return False, "Error: Request exceeds maximum claim"
        if request[j] > available[j]:
            return False, "Error: Resources not available"
    
    # Temporarily allocate resources
    temp_available = available.copy()
    temp_allocation = [row.copy() for row in allocation]
    
    for j in range(n_resources):
        temp_available[j] -= request[j]
        temp_allocation[process_idx][j] += request[j]
    
    # Check if resulting state is safe
    safe, sequence, steps = is_safe(temp_available, max_demand, temp_allocation, len(allocation), n_resources)
    
    if safe:
        return True, sequence, steps
    else:
        return False, "Request denied: resulting state would be unsafe", None


