from abc import ABC, abstractmethod

class IDb(ABC):
    @abstractmethod
    async def shut_down(self):
        pass

    async def select_single_row(self,id):
        pass

    async def select_all_tasks(self) -> []:
        pass

    async def invalidate_queue(self) -> bool:
        pass

    async def change_status(self, dlist: list) -> bool:
        pass

    def close(self):
        pass

    def __del__(self):
        pass