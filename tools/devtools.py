"""Offline development tools for Ashes; Python 3.11+, no external dependencies."""
import argparse
import csv
import gzip
import hashlib
import io
import json
import re
import struct
import sys
import tomllib
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ID = re.compile(r"[a-z0-9_.-]+:[a-z0-9_./-]+")
DATA = Path("overrides/kubejs/data")
QUESTS = Path("overrides/config/ftbquests/quests/chapters")
KUBE = Path("overrides/kubejs")


def load(p):
    return json.loads(p.read_text(encoding="utf-8"))


def emit(obj, output=None):
    s = json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(s, encoding="utf-8")
    else:
        print(s, end="")


def require(ok, msg):
    if not ok:
        raise ValueError(msg)


def resource_id(value):
    return isinstance(value, str) and ID.fullmatch(value) is not None


def chapters(root):
    for p in sorted((root / QUESTS).glob("*.snbt")):
        yield p.stem, load(p)


def authored_items(root):
    source = (root / KUBE / "startup_scripts/ashes_items.js").read_text(encoding="utf-8")
    return sorted("kubejs:" + n for n in re.findall(r"event\.create\('([^']+)'\)", source))


def recipe_rows(root):
    source = (root / KUBE / "server_scripts/ashes_recipes.js").read_text(encoding="utf-8")
    rows = []
    # Supported generated syntax: single-line shapeless recipes; fail closed on other syntax.
    for line in source.splitlines():
        if "event.shapeless(" not in line:
            continue
        m = re.search(r"event\.shapeless\('(?:(\d+)x )?([^']+)',\s*\[(.*?)\]\)\.id\('([^']+)'\)", line)
        require(m is not None, "Unrecognized generated recipe: " + line)
        count, result, ingredients, name = m.groups()
        ins = re.findall(r"""['"]([^'"]+)['"]""", ingredients)
        require(resource_id(result) and resource_id(name) and all(resource_id(i) for i in ins), name)
        rows.append(dict(id=name, output=result, count=int(count or 1), inputs=ins))
    return rows


def walk(obj):
    if isinstance(obj, dict):
        yield obj
        for v in obj.values():
            yield from walk(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk(v)


def data_files(root, kind, suffix=".json"):
    for ns in sorted((root / DATA).iterdir()):
        if ns.is_dir():
            folder = ns / kind
            for p in sorted(folder.rglob("*" + suffix)):
                yield ns.name + ":" + p.relative_to(folder).as_posix()[:-len(suffix)], p


class NBT:
    """Bounded big-endian NBT decoder for authored Minecraft structure templates."""
    def __init__(self, data):
        self.f = io.BytesIO(data)

    def read(self, n):
        require(0 <= n <= 32 * 1024 * 1024, "Invalid NBT length")
        b = self.f.read(n)
        require(len(b) == n, "Truncated NBT")
        return b

    def num(self, fmt):
        return struct.unpack(">" + fmt, self.read(struct.calcsize(">" + fmt)))[0]

    def string(self):
        return self.read(self.num("H")).decode("utf-8")

    def payload(self, t, depth=0):
        require(depth < 64, "NBT nesting too deep")
        if t in (1, 2, 3, 4, 5, 6):
            return self.num({1: "b", 2: "h", 3: "i", 4: "q", 5: "f", 6: "d"}[t])
        if t == 8:
            return self.string()
        if t in (7, 9, 11, 12):
            child = self.num("B") if t == 9 else {7: 1, 11: 3, 12: 4}[t]
            count = self.num("i")
            require(0 <= count <= 2_000_000 and (child != 0 or count == 0), "Invalid NBT array")
            if t == 7:
                return self.read(count)
            return [self.payload(child, depth + 1) for _ in range(count)]
        if t == 10:
            obj = {}
            while (child := self.num("B")) != 0:
                key = self.string()
                require(key not in obj, "Duplicate NBT key")
                obj[key] = self.payload(child, depth + 1)
            return obj
        raise ValueError("Unsupported NBT tag " + str(t))

    def parse(self):
        require(self.num("B") == 10, "NBT root is not compound")
        self.string()
        obj = self.payload(10)
        require(not self.f.read(1), "Trailing NBT data")
        return obj


def inspect_template(path):
    with gzip.open(path, "rb") as f:
        raw = f.read(32 * 1024 * 1024 + 1)
    require(len(raw) <= 32 * 1024 * 1024, "NBT too large")
    obj = NBT(raw).parse()
    size, palette, blocks = obj["size"], obj["palette"], obj["blocks"]
    require(obj["DataVersion"] == 3465, "Unexpected DataVersion")
    require(len(size) == 3 and all(type(n) is int and 0 < n <= 128 for n in size), "Invalid size")
    require(bool(palette) and all(resource_id(s["Name"]) for s in palette), "Invalid palette")
    require(isinstance(obj["entities"], list), "Invalid entity list")
    seen, loot, entities = set(), set(), set()
    for e in obj["entities"]:
        entity_id = e.get("nbt", {}).get("id")
        require(resource_id(entity_id), "Invalid entity ID")
        pos = e.get("pos", [])
        require(len(pos) == 3 and all(type(x) in (int, float) and 0 <= x < n
                                     for x, n in zip(pos, size)), "Entity out of bounds")
        block_pos = e.get("blockPos", [])
        require(len(block_pos) == 3 and all(type(x) is int and x <= axis < x + 1
                                           for x, axis in zip(block_pos, pos)), "Invalid entity blockPos")
        entities.add(entity_id)
    for b in blocks:
        pos = tuple(b["pos"])
        require(len(pos) == 3 and all(type(x) is int and 0 <= x < n for x, n in zip(pos, size)), "Out of bounds: " + str(pos))
        require(pos not in seen, "Duplicate position: " + str(pos))
        seen.add(pos)
        require(type(b["state"]) is int and 0 <= b["state"] < len(palette), "Bad palette index")
        if "LootTable" in b.get("nbt", {}):
            lid = b["nbt"]["LootTable"]
            require(resource_id(lid), "Invalid loot ID")
            loot.add(lid)
    return dict(size=size, blocks=len(blocks), chests=sum("LootTable" in b.get("nbt", {}) for b in blocks),
                palette=sorted({s["Name"] for s in palette}), loot=sorted(loot), entities=sorted(entities))


def structures(root):
    loot_ids = {i for i, _ in data_files(root, "loot_tables")}
    expected = {r["template"]: r for r in load(root / "docs/lore-structures.json")}
    result = {}
    for name, path in data_files(root, "structures", ".nbt"):
        info = inspect_template(path)
        missing = {i for i in info["loot"] if i.startswith("ashes:")} - loot_ids
        require(not missing, str(path) + ": missing loot " + str(missing))
        if name.startswith("ashes:lore/"):
            row = expected.pop(name.split(":", 1)[1])
            require(all(info[k] == row[k] for k in ("size", "blocks", "chests")), "Stale lore inventory: " + name)
        result[name] = info
    require(not expected, "Missing lore templates: " + str(expected))
    return result


def references(root, templates=None):
    refs = defaultdict(set)
    for name, c in chapters(root):
        for q in c["quests"]:
            for task in q["tasks"]:
                if task["type"] == "item":
                    refs["item"].add(task["item"])
            for reward in q.get("rewards", []):
                if reward.get("type") == "item":
                    refs["item"].add(reward["item"])
    for row in recipe_rows(root):
        refs["item"].update([row["output"], *row["inputs"]])
    for _, p in data_files(root, "loot_tables"):
        for entry in walk(load(p)):
            if entry.get("type") == "minecraft:item":
                refs["item"].add(entry["name"])
    for t in (templates if templates is not None else structures(root)).values():
        refs["block"].update(t["palette"])
        refs["entity_type"].update(t["entities"])
    return {k: sorted(v) for k, v in sorted(refs.items())}


def registry_check(root, path):
    # Accept vanilla/Forge reports/registries.json or a normalized map of complete ID lists.
    raw = load(path)
    result = {}
    for kind, names in references(root).items():
        key = "minecraft:" + kind
        value = raw.get(key, raw.get(kind))
        require(isinstance(value, (dict, list)), "Missing registry: " + key)
        if isinstance(value, dict):
            value = value.get("entries")
            require(isinstance(value, dict), "Missing entries: " + key)
        known = set(value)
        require(all(resource_id(i) for i in known), "Invalid registry IDs: " + key)
        result[kind] = dict(checked=len(names), missing=sorted(set(names) - known))
    return result


def jar_candidates(mods):
    """Resource evidence only; assets are not a registered block/item/entity registry."""
    result = dict(mods=[], block_candidates={}, item_candidates={}, errors=[])
    for p in sorted(mods.glob("*.jar")):
        try:
            with zipfile.ZipFile(p) as z:
                names = z.namelist()
                meta = tomllib.loads(z.read("META-INF/mods.toml").decode("utf-8-sig")) if "META-INF/mods.toml" in names else {}
                result["mods"].append(dict(file=p.name, ids=sorted(m["modId"] for m in meta.get("mods", [])),
                                           sha256=file_hash(p)))
                for n in names:
                    m = re.fullmatch(r"assets/([^/]+)/(blockstates|models/item)/(.+)\.json", n)
                    if m:
                        ns, kind, name = m.groups()
                        target = result["block_candidates" if kind == "blockstates" else "item_candidates"]
                        target.setdefault(ns + ":" + name, []).append(p.name)
        except (OSError, ValueError, KeyError, zipfile.BadZipFile) as e:
            result["errors"].append(p.name + ": " + str(e))
    require(bool(result["mods"] or result["errors"]), "No JAR files found in " + str(mods))
    result["note"] = "Assets only; generated models, unregistered resources and nested JARs may be absent. Use runtime registry for confirmation; audit_mods.py for dependencies."
    return result


def file_hash(p):
    with p.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def balance(root):
    byid, summaries = {}, {}
    for name, c in chapters(root):
        qlist = c["quests"]
        for q in qlist:
            byid[q["id"]] = q
        summaries[name] = dict(quests=len(qlist), manual=sum(any(t["type"] == "checkmark" for t in q["tasks"]) for q in qlist),
                               rewards=Counter(r.get("type", "unknown") for q in qlist for r in q.get("rewards", [])),
                               item_tasks=dict(Counter(t["item"].split(":")[0] for q in qlist for t in q["tasks"] if t["type"] == "item")))
    depths, active = {}, set()

    def depth(qid):
        if qid not in depths:
            require(qid in byid and qid not in active, "Invalid quest graph: " + qid)
            active.add(qid)
            depths[qid] = 1 + max((depth(d) for d in byid[qid].get("dependencies", [])), default=0)
            active.remove(qid)
        return depths[qid]
    for qid in byid:
        depth(qid)
    return dict(chapters=summaries, quests=len(byid), manual=sum(x["manual"] for x in summaries.values()),
                longest_dependency_chain=max(depths.values(), default=0),
                recipes=recipe_rows(root), note="Structural metrics, not playtime or mod recipe economics.")


def worldgen(root):
    result = {"structure_sets": {}, "configured_features": {}, "commands": []}
    for name, p in data_files(root, "worldgen/structure_set"):
        obj = load(p)
        result["structure_sets"][name] = obj
        for entry in obj["structures"]:
            result["commands"].append("/locate structure " + entry["structure"])
    for name, p in data_files(root, "worldgen/configured_feature"):
        obj = load(p)
        result["configured_features"][name] = {"type": obj.get("type"), "size": obj.get("config", {}).get("size")}
    result["note"] = "Configuration only; run commands on several new test worlds. Does not measure spawn frequency or ore yield."
    return result


def snapshot(root):
    manifest = load(root / "manifest.json")
    with (root / "overrides/ashes_docs/mods-lock.tsv").open(encoding="utf-8") as f:
        mods = list(csv.DictReader(f, delimiter="\t"))
    t = structures(root)
    return dict(version=manifest["version"], minecraft=manifest["minecraft"], mods=mods, authored_items=authored_items(root),
                references=references(root, t), structures=t, balance=balance(root), worldgen=worldgen(root),
                source_files=[str(p.relative_to(root).as_posix()) for folder in ("tools", "docs") for p in sorted((root / folder).rglob("*"))
                              if p.is_file() and "__pycache__" not in p.parts],
                note="Generated from committed sources; not a runtime registry.")


def crash_summary(path):
    patterns = {"dependencies": r"missing (?:mandatory |required )?dependenc|requires .+ (?:version|or above)|mod .+ requires",
                "mixins": r"mixin.{0,100}(?:failed|error|exception)|MixinApplyError|InvalidMixinException",
                "registry": r"missing registry|unknown registry|unbound values|unknown (?:item|block)|failed to load registries",
                "datapack": r"(?:datapack|loot table|recipe|worldgen).{0,100}(?:error|failed|exception)|failed to parse",
                "memory": r"OutOfMemoryError|GC overhead limit", "exception": r"Caused by:|FATAL|Exception in thread"}
    counts = Counter()
    lines = defaultdict(list)
    # Return line numbers only: avoid exposing access tokens, paths and private chat from logs.
    with path.open(encoding="utf-8", errors="replace") as f:
        for n, line in enumerate(f, 1):
            for kind, pattern in patterns.items():
                if re.search(pattern, line, re.I):
                    counts[kind] += 1
                    if len(lines[kind]) < 20:
                        lines[kind].append(n)
    return dict(counts=counts, line_numbers=lines, note="Heuristics only; inspect causes in local log. No automatic fixes.")


def loot_preview(spec):
    pools = []
    for pool in spec["pools"]:
        rolls = pool["rolls"]
        require(type(rolls) is int and 1 <= rolls <= 16, "rolls must be 1..16")
        entries = []
        for entry in pool["entries"]:
            item, weight = entry["item"], entry.get("weight", 1)
            lo, hi = entry.get("min", 1), entry.get("max", 1)
            require(resource_id(item) and type(weight) is int and weight > 0, "Invalid loot entry")
            require(type(lo) is int and type(hi) is int and 1 <= lo <= hi <= 64, "Invalid loot count")
            e = dict(type="minecraft:item", name=item, weight=weight)
            if (lo, hi) != (1, 1):
                e["functions"] = [{"function": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": lo, "max": hi}}]
            entries.append(e)
        require(bool(entries), "Empty loot pool")
        pools.append(dict(rolls=rolls, entries=entries))
    require(bool(pools), "No loot pools")
    return dict(type="minecraft:chest", pools=pools)


def check(root):
    t = structures(root)
    refs = references(root, t)
    require(set(i for i in refs.get("item", []) if i.startswith("kubejs:")) <= set(authored_items(root)), "Unknown authored item")
    require(len({r["id"] for r in recipe_rows(root)}) == len(recipe_rows(root)), "Duplicate recipe ID")
    balance(root)
    worldgen(root)
    for p in ("AGENTS.md", "PROJECT_INDEX.md", "PROJECT_CONTEXT.md", "docs/DEVELOPMENT_RULES.md", "docs/KNOWLEDGE_BASE.md"):
        require((root / p).is_file(), "Missing knowledge file: " + p)
    print("PASS: devtools structure geometry, source references, progression and knowledge files. Runtime NOT tested.")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("snapshot", "structures", "balance", "worldgen", "refs", "scan-jars", "registry-check", "crash", "loot-preview"):
        cmd = sub.add_parser(name)
        if name in ("scan-jars", "registry-check", "crash", "loot-preview"):
            cmd.add_argument("path", type=Path)
        cmd.add_argument("-o", "--output", type=Path)
    sub.add_parser("check")
    a = p.parse_args()
    try:
        if a.cmd == "check":
            check(ROOT)
            return 0
        callbacks = {"snapshot": lambda: snapshot(ROOT), "structures": lambda: structures(ROOT),
                     "balance": lambda: balance(ROOT), "worldgen": lambda: worldgen(ROOT), "refs": lambda: references(ROOT),
                     "scan-jars": lambda: jar_candidates(a.path), "registry-check": lambda: registry_check(ROOT, a.path),
                     "crash": lambda: crash_summary(a.path), "loot-preview": lambda: loot_preview(load(a.path))}
        result = callbacks[a.cmd]()
        emit(result, a.output)
        if a.cmd == "registry-check" and any(v["missing"] for v in result.values()):
            return 1
        if a.cmd == "scan-jars" and result["errors"]:
            return 1
        return 0
    except (OSError, ValueError, KeyError, TypeError, IndexError, struct.error) as e:
        print("FAIL:", e, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
