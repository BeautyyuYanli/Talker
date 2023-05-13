from abc import abstractmethod

from typing import Dict, List, Optional, Union, Any


class DB:
    def __init__(self, id: str) -> None:
        self.id = id

    @abstractmethod
    def add(self, user_msg: Dict[str, Any], comp_msg: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

    @abstractmethod
    def get_msg(self, token: int, trim: bool = False) -> List[Dict[str, Any]]:
        pass
