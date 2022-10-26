from .text import Text

class Tools(
    Text
):
    def __init__(self, client: Client):
        self.client = client