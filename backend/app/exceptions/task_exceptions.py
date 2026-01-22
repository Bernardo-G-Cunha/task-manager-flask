from app.exceptions import ProblemDetailException

class TaskNotFoundError(ProblemDetailException):
    """Task was not found."""
    def __init__(self):
        super().__init__(
            type_="errors/task-not-found",
            title="Task Not Found",
            status=404,
            detail="Requested task could not be found."
        )
