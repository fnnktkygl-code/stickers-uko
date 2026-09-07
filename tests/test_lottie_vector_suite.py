import json
import os
import zipfile
import unittest

class TestAitukoLottieSuite(unittest.TestCase):
    STATES = [
        "00_idle", "01_waving", "02_celebrating", "03_ai_thinking",
        "04_error_404", "05_thumbs_up", "06_sleeping", "07_pointing",
        "08_searching", "09_loading", "10_idea", "11_security", "12_goodbye"
    ]

    def test_all_13_states_lottie_exist_and_valid(self):
        for st in self.STATES:
            for base_dir in ["assets", "mascots/aituko/assets"]:
                p = os.path.join(base_dir, st, "lottie.json")
                self.assertTrue(os.path.exists(p), f"Missing lottie file: {p}")
                
                sz_kb = os.path.getsize(p) / 1024.0
                self.assertLess(sz_kb, 50.0, f"Lottie file too large: {p} ({sz_kb:.1f} KB > 50 KB)")
                
                with open(p, "r", encoding="utf-8") as f:
                    doc = json.load(f)
                
                self.assertIn("v", doc)
                self.assertEqual(doc["v"], "5.7.4")
                self.assertEqual(doc["w"], 512)
                self.assertEqual(doc["h"], 512)
                self.assertIn("layers", doc)
                self.assertGreater(len(doc["layers"]), 3)

    def test_snippets_have_lottie_keys(self):
        for st in self.STATES:
            p = os.path.join("assets", st, "snippet.json")
            self.assertTrue(os.path.exists(p))
            with open(p, "r", encoding="utf-8") as f:
                snip = json.load(f)
            self.assertIn("lottie_react", snip)
            self.assertIn("lottie_flutter", snip)
            self.assertIn("lottie_web", snip)

    def test_zip_bundles_contain_lottie(self):
        starter_zip = "downloads/AItuko-Starter-Pack.zip"
        pro_zip = "downloads/AItuko-Pro-12-States.zip"
        self.assertTrue(os.path.exists(starter_zip))
        self.assertTrue(os.path.exists(pro_zip))
        
        with zipfile.ZipFile(starter_zip, "r") as z:
            names = z.namelist()
            self.assertTrue(any("lottie.json" in n for n in names), "Starter zip missing lottie.json")
            
        with zipfile.ZipFile(pro_zip, "r") as z:
            names = z.namelist()
            lottie_count = sum(1 for n in names if n.endswith("lottie.json"))
            self.assertGreaterEqual(lottie_count, 6, "Pro zip should contain multiple lottie.json files")

if __name__ == "__main__":
    unittest.main()
