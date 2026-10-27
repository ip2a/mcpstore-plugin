#!/usr/bin/env python3
"""Generate the market index: `dist/<id>.zip` + `index.json` from `clients/*/.

The index is the only file an mcpstore daemon fetches: one document listing
every plugin with its version, blake3 digest, and discover rules. Zip roots
carry `plugin.toml` directly — the daemon unpacks the archive as the plugin
folder itself.
"""

import json
import tomllib
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from blake3 import blake3

ROOT = Path(__file__).resolve().parents[1]
CLIENTS = ROOT / "clients"
DIST = ROOT / "dist"


def main() -> None:
    DIST.mkdir(exist_ok=True)
    plugins = []
    for client_dir in sorted(p for p in CLIENTS.iterdir() if p.is_dir()):
        manifest_path = client_dir / "plugin.toml"
        if not manifest_path.is_file():
            continue
        manifest = tomllib.loads(manifest_path.read_text())
        plugin = manifest["plugin"]
        plugin_id = plugin["id"]
        if plugin_id != client_dir.name:
            raise SystemExit(f"{client_dir}: folder name must equal plugin id")
        if "discover" not in manifest:
            raise SystemExit(f"{plugin_id}: manifest has no [discover] section")

        zipped = DIST / f"{plugin_id}.zip"
        with ZipFile(zipped, "w", ZIP_DEFLATED) as archive:
            for file in sorted(client_dir.rglob("*")):
                if file.is_file():
                    archive.write(file, file.relative_to(client_dir))

        plugins.append(
            {
                "id": plugin_id,
                "label": plugin["label"],
                "plugin_version": plugin["plugin_version"],
                "spec_version": plugin["spec_version"],
                "description": plugin.get("description"),
                "download": f"dist/{plugin_id}.zip",
                "digest": blake3(zipped.read_bytes()).hexdigest(),
                "discover": manifest["discover"],
            }
        )

    index = {
        "spec_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "plugins": plugins,
    }
    (ROOT / "index.json").write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n")
    print(f"index.json written: {len(plugins)} plugins")


if __name__ == "__main__":
    main()
