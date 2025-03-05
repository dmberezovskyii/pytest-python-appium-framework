from dynaconf import Dynaconf

settings = Dynaconf(
    settings_files=[
        "config/settings.yaml",  # Default settings
        "config/.secrets.yaml",  # Sensitive data
    ],
    environments=True,
    load_dotenv=True,
    envvar_prefix="APPIUM",
    env_switcher="ENV_FOR_APPIUM",
    dotenv_path="configs/.env",  # Enable env switcher
)
