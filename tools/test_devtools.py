"""Fast tests for developer utilities; no game installation required."""
import gzip
import tempfile
import unittest
from pathlib import Path
from devtools import NBT, inspect_template, loot_preview, crash_summary, jar_candidates
from structures import nbt
import zipfile


class DevtoolsTests(unittest.TestCase):
    def test_nbt(self):
        obj = {"DataVersion": 3465, "size": [2, 2, 2], "palette": [{"Name": "minecraft:stone"}],
               "blocks": [{"pos": [1, 1, 1], "state": 0}], "entities": []}
        self.assertEqual(NBT(nbt(obj)).parse(), obj)
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "test.nbt"
            p.write_bytes(gzip.compress(nbt(obj)))
            self.assertEqual(inspect_template(p)["blocks"], 1)
            obj["blocks"][0]["pos"] = [2, 0, 0]
            p.write_bytes(gzip.compress(nbt(obj)))
            with self.assertRaises(ValueError):
                inspect_template(p)
        with self.assertRaises(ValueError):
            NBT(nbt(obj)[:-1]).parse()

    def test_loot(self):
        spec = {"pools": [{"rolls": 2, "entries": [{"item": "minecraft:bread", "min": 1, "max": 3}]}]}
        self.assertEqual(loot_preview(spec)["pools"][0]["rolls"], 2)
        spec["pools"][0]["entries"][0]["max"] = 65
        with self.assertRaises(ValueError):
            loot_preview(spec)

    def test_jar_and_log(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            with zipfile.ZipFile(p / "example.jar", "w") as z:
                z.writestr("META-INF/mods.toml", '[[mods]]\nmodId="demo"\n')
                z.writestr("assets/demo/blockstates/example.json", "{}")
                z.writestr("assets/demo/models/item/example.json", "{}")
            result = jar_candidates(p)
            self.assertIn("demo:example", result["block_candidates"])
            self.assertIn("demo:example", result["item_candidates"])
            self.assertEqual(result["mods"][0]["ids"], ["demo"])
            log = p / "latest.log"
            log.write_text("hello\nCaused by: java.lang.OutOfMemoryError\n", encoding="utf-8")
            self.assertEqual(crash_summary(log)["line_numbers"]["memory"], [2])

    def test_critical_injection_after_mixin_warnings(self):
        with tempfile.TemporaryDirectory() as d:
            log = Path(d) / "latest.log"
            warning = "[main/WARN] [mixin/]: Error loading class: optional.Example"
            failure = "Caused by: org.spongepowered.asm.mixin.injection.throwables.InjectionError: Critical injection failure: Callback method postRegisterEvents"
            log.write_text("\n".join([warning] * 25 + [failure]), encoding="utf-8")
            self.assertEqual(crash_summary(log)["line_numbers"]["critical_injections"], [26])


if __name__ == "__main__":
    unittest.main()
