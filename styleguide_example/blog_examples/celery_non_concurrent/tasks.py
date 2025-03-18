import logging
from functools import wraps

from celery import shared_task

from styleguide_example.tasks import celery_app

inspect = celery_app.control.inspect

logger = logging.getLogger(__name__)


def non_concurrent_task(_func=None, *args, **kwargs):
    def wrapper(func):
        @wraps(func)
        def inner(_bound_self, *_func_args, **_func_kwargs):
            running_task_count = 0

            queues = inspect().active()

            if queues is None:
                queues = {}

            for running_tasks in queues.values():
                for task in running_tasks:
                    if task["name"] == _bound_self.name:
                        running_task_count += 1

                    if running_task_count > 1:
                        logger.warning(f"[non_concurrent_task] Task {_bound_self.name} is already running")
                        return

            return func(*_func_args, **_func_kwargs)

        return shared_task(bind=True, *args, **kwargs)(inner)

    if _func is None:
        return wrapper

    return wrapper(_func)


@non_concurrent_task
def test_non_concurrent_task():
    logger.info("A non-concurrent task is running")
    import time
    time.sleep(10)
    logger.info("A non-concurrent task finished")
