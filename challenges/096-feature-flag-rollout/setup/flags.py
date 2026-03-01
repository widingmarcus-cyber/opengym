class FeatureFlags:
    def __init__(self, config_path=None):
        pass

    def is_enabled(self, flag_name, user_id=None):
        pass

    def enable(self, flag_name):
        pass

    def disable(self, flag_name):
        pass

    def set_rollout_percentage(self, flag_name, pct):
        pass

    def get_all_flags(self):
        pass
