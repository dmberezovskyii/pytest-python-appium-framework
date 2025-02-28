from dynaconf import Dynaconf

settings = Dynaconf(
    settings_files=[
        "settings/settings.yaml",  # Default settings
        "settings/stage.yaml",     # Development-specific settings
        "settings/prod.yaml",      # Production-specific settings
        "settings/.secrets.yaml",  # Sensitive data
    ],
    environments=True,
    load_dotenv=True,
    envvar_prefix="PW",
    env_switcher="ENV_FOR_PW",
    dotenv_path="configs/.env",
)
