class piece:
    def __init__(self):
        self.position = (0, 0, 0)
        self.mas = 0
        self.velocity = (0, 0, 0)
        self.air_friction_factor = 0
        self.springiness = 0
        self.ground_friction_factor = 0

    def update_velocity(self, forces_array):
        pass

    def update_posiotion(self, dt):
        self.position = self.velocity * dt
