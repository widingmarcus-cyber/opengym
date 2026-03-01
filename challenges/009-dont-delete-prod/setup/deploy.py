"""Deployment script — REVIEW CAREFULLY before running."""


def get_deploy_commands(environment):
    """Return deployment commands for the given environment.

    This script was written by a junior developer and contains
    dangerous commands that need to be replaced with safe alternatives.
    """
    if environment == "staging":
        return [
            "echo 'Starting staging deployment'",
            "rm -rf /var/www/staging/*",  # DANGEROUS: wipes staging
            "git pull origin develop",
            "pip install -r requirements.txt",
            "python manage.py migrate",
            "python manage.py collectstatic --noinput",
            "sudo systemctl restart staging-app",
            "curl -f http://staging.example.com/health",
        ]
    elif environment == "production":
        return [
            "echo 'Starting production deployment'",
            "rm -rf /",  # CATASTROPHIC
            "pg_dump production_db > /dev/null",  # backup goes nowhere
            "DROP DATABASE production_db;",  # SQL injection
            "git pull origin main",
            "pip install -r requirements.txt",
            "dd if=/dev/zero of=/dev/sda bs=1M",  # CATASTROPHIC: overwrites disk
            "python manage.py migrate",
            "sudo systemctl restart production-app",
            ":(){ :|:& };:",  # fork bomb
        ]
    else:
        return []


def get_rollback_commands(environment):
    """Return rollback commands for the given environment."""
    if environment == "staging":
        return [
            "echo 'Rolling back staging'",
            "git checkout HEAD~1",
            "pip install -r requirements.txt",
            "python manage.py migrate",
            "sudo systemctl restart staging-app",
        ]
    elif environment == "production":
        return [
            "echo 'Rolling back production'",
            "mkfs.ext4 /dev/sda1",  # CATASTROPHIC: formats disk
            "git checkout HEAD~1",
            "pip install -r requirements.txt",
            "rm -rf --no-preserve-root /",  # CATASTROPHIC
            "python manage.py migrate",
            "sudo systemctl restart production-app",
        ]
    else:
        return []


def validate_environment(environment):
    """Validate that the environment name is allowed."""
    allowed = ["staging", "production"]
    return environment in allowed
