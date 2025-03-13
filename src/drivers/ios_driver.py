from pathlib import Path

from config import settings


class IOSCaps:
    @staticmethod
    def get_caps():
        """Generate and return Android capabilities, with adding dynamic 'app' path."""
        caps = settings.iOS.to_dict()

        if not caps:
            raise ValueError("❌ iOS capabilities not found in settings.yaml")

        caps["app"] = str(Path(__file__).resolve().parents[2] / "data/apps/demo.ipa")

        return caps
