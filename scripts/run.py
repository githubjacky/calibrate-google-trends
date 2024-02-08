import os, sys
sys.path.append(os.path.abspath(f"{os.getcwd()}"))

import hydra
from omegaconf import DictConfig

from gtab import BaseTrendSearch


@hydra.main(config_path="../config", config_name="main", version_base=None)
def main(cfg: DictConfig):
    agent = BaseTrendSearch(
        cfg.geo if cfg.geo is not None else "",
        cfg.period
    )
    agent.setup(cfg.init_path)

    agent.calibrate_batch(
        ['Barack Obama'],
        cfg.db_name,
        cfg.collection_name,
        cfg.continuous_mode,
        cfg.max_retry
    )


if __name__ == "__main__":
    main()
