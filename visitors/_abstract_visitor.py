from abc import ABC, abstractmethod


class AbstractVisitor(ABC):
    @abstractmethod
    def visit(self, apps):
        return []