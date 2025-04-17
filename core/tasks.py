from config.celery import app


@app.task
def add(x, y):
    """Add two numbers."""
    print(f"Adding {x} and {y}", x + y)
