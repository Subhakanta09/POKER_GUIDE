import pandas as pd
from pypokerengine.api.game import setup_config, start_poker
from pypokerengine.utils.card_utils import gen_cards
from pypokerengine.utils.card_utils import estimate_hole_card_win_rate
from pypokerengine.players import BasePokerPlayer
from tabulate import tabulate
import random

class CountingBot(BasePokerPlayer):

    def __init__(self, bot_name):
        self.bot_name = bot_name
        self.wins = 0
        self.stack = 0
        self.in_game = True
        self.game_history = []
        self.game_history_df = pd.DataFrame(columns=[
            "bot_name", "round_state",
            "valid_actions", "action_taken"
        ])  # Initialize DataFrame

        super().__init__()

    def declare_action(self, valid_actions, hole_card, round_state):
        # Implement your bot's logic here
        pass


    def receive_game_start_message(self, game_info):
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        print(f"{self.bot_name}'s hole cards: {hole_card}")

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, new_action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        for winner in winners:
            if winner["uuid"] == self.uuid:
                self.wins += 1
        for player in round_state["seats"]:
            if player["uuid"] == self.uuid:
                self.stack = player["stack"]

        # Append game history to the DataFrame
        for entry in self.game_history:
            entry["bot_name"] = self.bot_name
            self.game_history_df = pd.concat([self.game_history_df, pd.DataFrame([entry])], ignore_index=True)
        self.game_history = []  # Reset the game history for the next round


