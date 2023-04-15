from talker.talker import Talker
import uuid


def inspect_model(model: str) -> str:
    try:
        with open(f"models/{model}.json") as f:
            pass
    except FileNotFoundError:
        model = "default"
    return model


class Pool:
    def __init__(self) -> None:
        self.pool = {}

    def new(self, model: str) -> str:
        model = inspect_model(model)
        id = model + "_" + str(uuid.uuid4())
        self.pool[id] = Talker(model, id)
        return id

    def get(self, id, model=None) -> Talker:
        if id is None:
            try:
                with open(f"models/{model}.json") as f:
                    pass
            except FileNotFoundError:
                model = "default"
            print(f"Warning: id is None, using default id for model: {model}")
            id = f"{model}_default"
            if id not in self.pool:
                self.pool[id] = Talker(model, id)
            return self.pool[id]
        else:
            try:
                with open(f"data/{id}.db") as f:
                    pass
            except FileNotFoundError:
                raise ValueError(f"Invalid id: {id}")
            if id not in self.pool:
                self.pool[id] = Talker(id.split("_")[0], id)
            return self.pool[id]
