from data import UserState

def prev_stage(stage_str):
    stages = list(UserState)
    stage = UserState(stage_str)
    idx = stages.index(stage)
    prev_idx = idx - 1
    if prev_idx > 0:
        return stages[prev_idx]
    else:
        return None
