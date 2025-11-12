import io
import json
from typing import Any

class JsonlWriter:
    def __init__(self, path: str):
        self.path = path
        self.fh = io.open(self.path, "w", encoding="utf-8")

    def write(self, obj: Any):
        line = json.dumps(obj, ensure_ascii=False)
        self.fh.write(line + "\n")

    def close(self):
        try:
            self.fh.flush()
        finally:
            self.fh.close()