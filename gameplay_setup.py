# remember to instantiate your bots eg ab= ABot()
# Configure and start the game
config = setup_config(max_round=3, initial_stack=5000, small_blind_amount=5)
config.register_player(name="RBot", algorithm=rb)
config.register_player(name="FBot", algorithm=fb)
game_result = start_poker(config, verbose=1)
