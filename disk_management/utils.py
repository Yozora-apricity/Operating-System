def calculate_movement(sequence):
    """Calculates the total head movement for a given sequence."""
    movement = 0
    for i in range(len(sequence) - 1):
        movement += abs(sequence[i] - sequence[i+1])
    return movement