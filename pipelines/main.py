from zenml import pipeline, step
from zenml.logger import get_logger
from zenml.client import Client
import mlflow

logger = get_logger(__name__)

experiment_tracker = Client().active_stack.experiment_tracker


@step(
    experiment_tracker=experiment_tracker.name
    if experiment_tracker is not None
    else None
)
def say_hello() -> str:
    logger.info("Executing say_hello step")
    mlflow.log_param("x", 2)
    return "Hello World!"


@pipeline
def hello_world_pipeline():
    say_hello()


if __name__ == "__main__":
    run = hello_world_pipeline()
    out = run.steps["say_hello"].outputs["output"][0].load()
    logger.info(f"▶︎ Step returned: {out}")
