from bots.base import CountingBot
class GeneralPlayer(CountingBot):
    def declare_action(self, valid_actions, hole_card, round_state):
        # Convert hole cards and community cards to PyPokerEngine format
        community_cards = round_state["community_card"]

        # Estimate hand strength using win rate estimation
        num_active_players = self.count_active_players(round_state)
        win_rate = estimate_hole_card_win_rate(
            nb_simulation=1000,
            nb_player=num_active_players,
            hole_card=gen_cards(hole_card),
            community_card=gen_cards(community_cards),
        )

        # Retrieve pot size and bet amount
        pot_size = self.get_pot_size(round_state)

        if win_rate >= 1/num_active_players:  # If win rate is greater than 50% (since 2 players), raise by average of min and max raise
            raise_action = next(
                (a for a in valid_actions if a["action"] == "raise"), None
            )
            if raise_action:
                min_raise = raise_action["amount"]["min"]
                max_raise = raise_action["amount"]["max"]
                raise_amount = (min_raise + max_raise) / 2
                action = {"action": "raise", "amount": raise_amount}
            else:
                # No raise option, fallback to call if available
                action = next(
                    (a for a in valid_actions if a["action"] == "call"), None
                ) ## no call option even, then fold
                if not action:
                    action = next(
                        (a for a in valid_actions if a["action"] == "fold"), None
                    )

        else :  # If win rate is less than 1/n where n is no. of players, use fold
            action = next((a for a in valid_actions if a["action"] == "fold"), None)
            if not action:
                action = next((a for a in valid_actions if a["action"] == "fold"), None)


        # Handle case where no valid action is found
        if action is None:
            # If no suitable action is found, default to fold
            action = {'action': 'fold', 'amount': 0}

        # Extract amount (handle raise min-max structure)
        amount = action.get("amount")
        amount = action.get("amount")
        if isinstance(amount, dict):
            amount = amount.get("min", 0)  # Get min raise amount
            if amount < 0:              # Check if min amount is negative
                amount = 0              # If negative, set to 0

        if amount is None or amount < 0:
            amount = 0  # Default to 0 if amount is invalid or negative

        self.game_history.append({
        "round_state": round_state,
        "valid_actions": valid_actions,
        "action_taken": (action, amount)
        })


        return action["action"], int(amount)

    def get_pot_size(self, round_state):
        # Assume pot_size starts at 0
        pot_size = round_state['pot']['main']['amount']
        return pot_size

    def count_active_players(self,round_state):
        return len(round_state["seats"])
