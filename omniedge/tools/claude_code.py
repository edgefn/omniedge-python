import json
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Protocol


@dataclass
class ClaudeCodeSetResult:
    target_path: Path
    backup_path: Optional[Path]


class ClaudeCodeTool(Protocol):
    primary_name: str
    aliases: List[str]

    def set_config(
        self, *, base_url: str, api_key: str, model: str
    ) -> ClaudeCodeSetResult:
        ...

    def list_backups(self) -> List[Path]:
        ...

    def reset_config(self, backup_path: Path) -> Path:
        ...


class ClaudeCodeIntegration:
    primary_name = "claude-code"
    aliases = ["claude-code", "claude", "claude_code"]

    def __init__(self) -> None:
        self._settings_path = Path.home() / ".claude" / "settings.json"
        self._backup_dir = Path.home() / ".omniedge" / "backup" / "claude-code"

    def set_config(self, *, base_url: str, api_key: str, model: str) -> ClaudeCodeSetResult:
        backup_path = self._create_backup_if_exists()
        data = self._read_settings()
        env = data.get("env")
        if not isinstance(env, dict):
            env = {}
        env.update(
            {
                "ANTHROPIC_BASE_URL": base_url,
                "ANTHROPIC_AUTH_TOKEN": api_key,
                "API_TIMEOUT_MS": "3000000",
                "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": 1,
                "ANTHROPIC_MODEL": model,
                "ANTHROPIC_SMALL_FAST_MODEL": model,
            }
        )
        data["env"] = env
        self._settings_path.parent.mkdir(parents=True, exist_ok=True)
        with self._settings_path.open("w", encoding="utf-8") as fp:
            json.dump(data, fp, indent=2, ensure_ascii=False)
            fp.write("\n")
        return ClaudeCodeSetResult(target_path=self._settings_path, backup_path=backup_path)

    def list_backups(self) -> List[Path]:
        if not self._backup_dir.exists():
            return []
        return sorted([p for p in self._backup_dir.iterdir() if p.is_file()])

    def reset_config(self, backup_path: Path) -> Path:
        if not backup_path.exists():
            raise SystemExit(f"Backup file does not exist: {backup_path}")
        self._settings_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(backup_path, self._settings_path)
        return self._settings_path

    def _create_backup_if_exists(self) -> Optional[Path]:
        if not self._settings_path.exists():
            return None
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        self._backup_dir.mkdir(parents=True, exist_ok=True)
        backup_path = self._backup_dir / f"settings.json.{timestamp}.bak"
        shutil.copy2(self._settings_path, backup_path)
        return backup_path

    def _read_settings(self) -> dict:
        if not self._settings_path.exists():
            return {}
        try:
            with self._settings_path.open("r", encoding="utf-8") as fp:
                data = json.load(fp)
        except (json.JSONDecodeError, OSError):
            return {}
        return data if isinstance(data, dict) else {}
