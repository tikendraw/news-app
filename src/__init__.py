import os
import sys
from datetime import datetime
from pathlib import Path

root_dir=Path(__file__).parent.parent.absolute()

if root_dir.name=='news-app':
    sys.path.append(str(root_dir))
    