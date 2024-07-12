import importlib

def load_scenario(game_state):
    day = game_state.day
    module_name = f'scenarios.days.day_{day}'
    day_module = importlib.import_module(module_name)
    day_instance = getattr(day_module, f'Day{day}')
    day_instance().load_day(game_state)


