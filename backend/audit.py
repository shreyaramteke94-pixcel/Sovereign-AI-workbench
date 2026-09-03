from pathlib import Path
from datetime import datetime
import json


LOG_FILE = Path("./logs/audit.jsonl")

LOG_FILE.parent.mkdir(parents=True, exist_ok=True)


def write_audit(task: str, trace: list, answer: str):

    entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "task": task,
        "trace": trace,
        "answer": answer
    }

    try:
        with LOG_FILE.open("a", encoding="utf-8") as file:
            file.write(
                json.dumps(entry, ensure_ascii=False) + "\n"
            )

    except Exception as error:
        print(f"Audit logging failed: {error}")


def read_audit(limit: int = 20):

    if not LOG_FILE.exists():
        return []

    try:
        lines = LOG_FILE.read_text(
            encoding="utf-8"
        ).splitlines()

        entries = []

        for line in lines[-limit:]:
            if line.strip():
                entries.append(
                    json.loads(line)
                )

        return entries

    except Exception as error:
        return [
            {
                "error": f"Could not read audit log: {error}"
            }
        ]