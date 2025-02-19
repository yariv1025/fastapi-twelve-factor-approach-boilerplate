import subprocess
import logging
from app.core.config import get_settings

settings = get_settings()


def is_container_running(container_name: str) -> bool:
    """
    Check if a Docker container is already running.

    :param container_name: Name of the container to check.
    :return: True if running, False otherwise.
    """
    result = subprocess.run(
        ["/usr/bin/docker", "ps", "--filter", f"name={container_name}", "--format", "{{.Names}}"],
        capture_output=True, text=True
    )
    return container_name in result.stdout.strip()


def start_mongo():
    """Start MongoDB container if not running."""
    if is_container_running("mongo-container"):
        logging.info("MongoDB is already running.")
        return

    logging.info("Starting MongoDB container...")
    subprocess.run([
        "docker", "run", "-d", "--name", "mongo-container",
        "-e", f"MONGO_INITDB_ROOT_USERNAME={settings.MONGO_USER}",
        "-e", f"MONGO_INITDB_ROOT_PASSWORD={settings.MONGO_PASSWORD}",
        "-v", "mongo_data:/data/db", "-p", "27017:27017", "mongo:latest"
    ])

    logging.info("Waiting for MongoDB to initialize...")
    subprocess.run(["sleep", "5"])

    logging.info("Creating MongoDB admin user...")
    mongo_admin_script = f"""
        use {settings.MONGO_DB_NAME};
        db.createUser({{
            user: "{settings.MONGO_ADMIN_USER}",
            pwd: "{settings.MONGO_ADMIN_PASSWORD}",
            roles: [{{ role: "readWrite", db: "{settings.MONGO_DB_NAME}" }}]
        }});
    """
    subprocess.run([
        "docker", "exec", "-i", "mongo-container",
        "mongosh", "-u", settings.MONGO_USER, "-p", settings.MONGO_PASSWORD, "--authenticationDatabase", "admin"
    ], input=mongo_admin_script, text=True)

    logging.info("MongoDB setup complete.")


def start_redis():
    """Start Redis container if not running."""
    if is_container_running("redis-container"):
        logging.info("Redis is already running.")
        return

    logging.info("Starting Redis container...")
    subprocess.run([
        "docker", "run", "-d", "--name", "redis-container",
        "-e", f"REDIS_PASSWORD={settings.REDIS_PASSWORD}",
        "-v", "redis_data:/data", "-p", "6379:6379", "redis:latest",
        "--requirepass", settings.REDIS_PASSWORD
    ])
    logging.info("Redis setup complete.")


def start_postgres():
    """Start PostgreSQL container if not running."""
    if is_container_running("postgres-container"):
        logging.info("PostgreSQL is already running.")
        return

    logging.info("Starting PostgreSQL container...")
    subprocess.run([
        "docker", "run", "-d", "--name", "postgres-container",
        "-e", f"POSTGRES_USER={settings.POSTGRES_USER}",
        "-e", f"POSTGRES_PASSWORD={settings.POSTGRES_PASSWORD}",
        "-e", f"POSTGRES_DB={settings.POSTGRES_DB_NAME}",
        "-v", "postgres_data:/var/lib/postgresql/data", "-p", "5432:5432", "postgres:latest"
    ])
    logging.info("PostgreSQL setup complete.")


def initialize_databases():
    """Ensure all database containers are running."""
    logging.info("Initializing required databases...")
    start_mongo()
    start_redis()
    start_postgres()
    logging.info("All necessary databases are set up and running.")
