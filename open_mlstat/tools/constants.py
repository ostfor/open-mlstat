import os
from pathlib import Path

home = str(Path.home())

CONFIGS_STORAGE_ROOT = os.path.join(home, ".mlstat", "files")
