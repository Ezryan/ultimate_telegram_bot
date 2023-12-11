class User:
    def __init__(self, rigths):
        # self.id = usr_id
        self.right = rigths
        self.warn_count = 0
        # self.in_coin_game = False
        # self.in_mafia_game = False
        self.is_mute = False
        self.coins = 0