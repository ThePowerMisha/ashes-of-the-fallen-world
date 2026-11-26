"""Submit the verified standard archive as a new file of one CurseForge project."""

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
from zipfile import ZipFile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("tag")
    args = parser.parse_args()
    with ZipFile(args.archive) as archive:
        manifest = json.loads(archive.read("manifest.json"))

    version = manifest["version"]
    if args.tag != f"curseforge-v{version}" or not re.fullmatch(r"[0-9][A-Za-z0-9.-]*", version):
        parser.error(f"expected release tag curseforge-v{version} from manifest.json")
    release_notes = Path(__file__).resolve().parents[1] / "CHANGELOG.md"
    section = re.search(
        rf"^### {re.escape(version)}[ \t]*\n(.*?)(?=^#{{1,3}} |\Z)",
        release_notes.read_text(encoding="utf-8"),
        re.MULTILINE | re.DOTALL,
    )
    if section is None or not section[1].strip():
        parser.error(f"CHANGELOG.md needs a section '### {version}' with release notes")

    project = os.environ.get("CURSEFORGE_PROJECT_ID", "")
    token = os.environ.get("CURSEFORGE_UPLOAD_TOKEN", "")
    if not re.fullmatch(r"[1-9][0-9]*", project) or not token or "\n" in token or "\r" in token:
        parser.error("configure CURSEFORGE_PROJECT_ID and CURSEFORGE_UPLOAD_TOKEN in GitHub Actions")

    prerelease = version.partition("-")[2]
    release_type = "alpha" if "alpha" in prerelease else "beta" if prerelease else "release"
    metadata = {
        "changelog": section[1].strip(),
        "changelogType": "markdown",
        "displayName": f"{manifest['name']} {version}",
        "gameVersionNames": [manifest["minecraft"]["version"], "Forge", "Client"],
        "releaseType": release_type,
    }
    response = subprocess.run(
        [
            "curl", "--silent", "--show-error", "--fail", "--max-time", "180",
            "--header", "@-",
            "--form-string", f"metadata={json.dumps(metadata, ensure_ascii=False)}",
            "--form", f"file=@{args.archive};filename=Ashes-{version}.zip;type=application/zip",
            f"https://minecraft.curseforge.com/api/projects/{project}/upload-file",
        ],
        input=f"X-Api-Token: {token}\n",
        capture_output=True,
        encoding="utf-8",
    )
    if response.returncode:
        parser.exit(1, f"CurseForge submission failed: {response.stderr.strip()}\n")
    file_id = json.loads(response.stdout).get("id")
    if not isinstance(file_id, int) or file_id < 1:
        parser.exit(1, "CurseForge did not return a file ID. Check the author's dashboard.\n")
    print(f"Submitted {version} to CurseForge project {project}. File ID: {file_id}.")


if __name__ == "__main__":
    main()
