import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validate_input = load("validate_input", "scripts/validate_input.py")
consistency = load("consistency", "scripts/check_cross_channel_consistency.py")


class ValidatorTests(unittest.TestCase):
    def test_valid_input(self):
        data = {
            "会社名": "○○ホーム", "開催日": "10月1日", "開催時間": "10:00〜17:00",
            "開催場所": "熊本市", "予約方法": "LINE", "掲載終了日": "10月1日",
            "施主許諾": {"写真使用": True}, "来場特典": {}
        }
        self.assertEqual(validate_input.validate(data), ([], []))

    def test_missing_required(self):
        errors, _ = validate_input.validate({})
        self.assertTrue(any("会社名" in item for item in errors))

    def test_consistency(self):
        event = {"会社名": "○○ホーム", "開催日": "10月1日", "開催時間": "10時", "開催場所": "熊本市"}
        rows = consistency.check(event, [("a.txt", "○○ホーム 10月1日 10時 熊本市")])
        self.assertEqual(rows, [])


if __name__ == "__main__":
    unittest.main()
