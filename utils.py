from clients.python.utils import idx_to_x_z_rot
import math

def get_exp_name(cfg):
    """Get the experiment name from the config"""
    exp_name = f"{cfg.model.name}_{cfg.data.dataset}_{cfg.train.lr}-lr_{cfg.data.num_samples}-data_{cfg.exp_name}"
    return exp_name
