class force:
    def __init__(self, active_states):
        self.active_states = active_states

    def get_force_vector(self, piece, state ):
        if state in self.active_states:
            return self.calculate_force(piece)
        else:
            return (0,0,0)