"""List newer CurseForge files tagged for Minecraft 1.20.1 and Forge."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from urllib.request import urlopen

from audit_mods import read_lock


def latest_candidate(entry, include_beta):
    project_id = int(entry["projectID"])
    locked_id = int(entry["fileID"])
    result = {
        "slug": entry["slug"],
        "project": project_id,
        "locked_id": locked_id,
        "locked_file": entry["filename"],
    }
    if not entry["filename"].endswith(".jar"):
        return dict(result, status="shader")

    allowed_types = {1, 2} if include_beta else {1}
    page_size = 50
    for index in range(0, 250, page_size):
        url = (
            f"https://www.curseforge.com/api/v1/mods/{project_id}/files"
            f"?pageSize={page_size}&index={index}"
        )
        try:
            with urlopen(url, timeout=10) as response:
                files = json.load(response)["data"]
        except (OSError, ValueError, KeyError) as error:
            return dict(result, status="unresolved", error=type(error).__name__)

        for file in files:
            if file["id"] <= locked_id:
                return dict(result, status="no_newer_tagged_file")
            if {"1.20.1", "Forge"} <= set(file["gameVersions"]) and file["releaseType"] in allowed_types:
                return dict(
                    result,
                    status="candidate",
                    candidate_id=file["id"],
                    candidate_file=file["fileName"],
                    beta=file["releaseType"] == 2,
                )
        if len(files) < page_size:
            return dict(result, status="no_newer_tagged_file")

    return dict(result, status="unresolved", error="page_limit")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--include-beta", action="store_true")
    args = parser.parse_args()
    with ThreadPoolExecutor(max_workers=12) as executor:
        rows = list(executor.map(lambda row: latest_candidate(row, args.include_beta), read_lock()))
    print(json.dumps(rows, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
