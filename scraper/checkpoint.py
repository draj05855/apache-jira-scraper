import json
from pathlib import Path
from typing import Dict

class Checkpoint:
    def __init__(self, path="state.json"):
        self.path = Path(path)
        if not self.path.exists():
            self._write({})

    def _read(self) -> Dict:
        return json.loads(self.path.read_text())

    def _write(self, d: Dict):
        self.path.write_text(json.dumps(d, indent=2))

    def get(self, project):
        d = self._read()
        return d.get(project)

    def set(self, project, value):
        d = self._read()
        d[project] = value
        self._write(d)
