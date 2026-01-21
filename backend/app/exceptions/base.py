# Super model for detailed exceptions
class ProblemDetailException(Exception):
    def __init__(self, type_: str, title: str, status: int, detail: str):
        self.type = type_
        self.title = title
        self.status = status
        self.detail = detail
        super().__init__(detail)
