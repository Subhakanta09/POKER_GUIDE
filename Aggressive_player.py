
class AggressivePlayer(CountingBot):
    def __init__(self):
        super().__init__("AggressivePlayer")
        self.c = 0 ##c denotes no. of raise actions
        self.s = 1 ## s denotes no. of streets

    def check_bluffing(self, opponent_name, round_count):
        try:
            game_history_df = opponent_name.game_history_df
                        # Filter for opponent's actions and the last 2. rounds (or all if < 2)
            rounds = sorted(game_history_df["round_state"].apply(lambda x: x["round_count"]).unique())
            last_2_rounds = rounds[-2:] if len(rounds) >= 2 else rounds

            opponent_moves = game_history_df[
                (game_history_df["bot_name"] == opponent_name.bot_name) &  # Use bot_name for comparison
                (game_history_df["round_state"].apply(lambda x: x["round_count"] in last_2_rounds))
            ]

            c = 0
            s = 1
            for _, row in opponent_moves.iterrows():
                action_taken = row["action_taken"][0]
                amount = row["action_taken"][1]
                s += 1
                if action_taken["action"] == "raise":
                    c += 1
            return c, s
        except AttributeError:  # Handle cases where opponent_name might not have game_history_df yet
            return 0, 1
        except Exception as e:
            print(f"Error in check_bluffing: {e}")
            return 0,1


    def declare_action(self, valid_actions, hole_card, round_state):
        round_count = round_state["round_count"]

        # Access the ABot instance correctly
        global ab  # Access the globally defined ab object
        self.c, self.s = self.check_bluffing(ab, round_count)

        # Act aggressively in the upcoming round if the condition is met
        if round_count > 3 and self.c / self.s > 0.5:  # Adjusted condition for aggressiveness
            print("\n PLAYING AGGRESSIVELY \n")
            return ABot().declare_action(valid_actions, hole_card, round_state)
        # Default to GeneralPlayer behavior if not in aggressive mode
        return GeneralPlayer().declare_action(valid_actions, hole_card, round_state)
