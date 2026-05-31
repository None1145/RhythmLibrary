from .request import UserAPI

from ...common import utils
from ...common import config

import time

class Processor(UserAPI):
    def get_data(self) -> dict:
        raw_data = self.get_login_data()
        
        user_id = raw_data["userId"]
        
        save_dir = config.DATA_DIR / "rizline" / user_id / "data"
        save_dir.mkdir(parents=True, exist_ok=True)
        utils.save_data_to_file(raw_data, save_dir / time.time())
        
        return raw_data
