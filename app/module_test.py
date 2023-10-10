import sys
import os
from dotenv import load_dotenv
load_dotenv()

# modules_path = os.path.join(os.getcwd(), "modules")
# if modules_path not in sys.path:
#     print("modules not in sys path. Inserting", modules_path)
#     sys.path.insert(0, modules_path)

print(os.getenv("PYTHONPATH"))

import sentiment_predictor