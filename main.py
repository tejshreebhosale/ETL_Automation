from src.engine.runner import run

if __name__ == "__main__":
    status = run()

    if not status:
        exit(1)   # optional: fail execution for CI/CD