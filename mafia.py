ROLES = {
    "mafia": 0,
    "whore": 1,
    "doctor": 2,
    "villager": 3
}


class Player:
    def __init__(self, usr_id, role):
        self.id = usr_id
        self.role = ROLES.get(role)


class Mafia:
    def __init__(self):
        self.player_count = 0
        self.mafias = []
        self.whores = []
        self.doctors = []
        self.villagers = []


def add_player(usr_id, role):
    pass
