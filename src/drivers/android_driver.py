from pathlib import Path

from config import settings


class AndroidCaps:
    @staticmethod
    def get_caps():
        """Generate and return Android capabilities, with adding dynamic 'app' path."""
        caps = settings.ANDROID.to_dict()

        if not caps:
            raise ValueError("❌ ANDROID capabilities not found in settings.yaml")

        caps["app"] = str(Path(__file__).resolve().parents[2] / "data/apps/demo.apk")

        return caps
