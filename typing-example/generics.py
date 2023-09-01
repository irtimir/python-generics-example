import abc
from dataclasses import dataclass
from typing import Generic, Protocol, TypeVar

# Generics
# The ability to describe the invested type

_ItemType = TypeVar('_ItemType')


class Container(Generic[_ItemType]):
    def __init__(self, item: _ItemType) -> None:
        self.item = item

    def get_item(self) -> _ItemType:
        return self.item


# Protocol
# Convey the idea of “duck typification”, or “structural inheritance”.

class Human:
    def say(self) -> str:
        return 'Hi!'


class Duck:
    def say(self) -> str:
        return 'Quack'


class CanSay(Protocol):
    def say(self) -> str: ...


def say_and_print(instance: CanSay) -> None:
    print(instance.say())


# ABC + Generics

_Wrapped = TypeVar('_Wrapped')


class BaseGreet(Generic[_Wrapped]):
    def __init__(self, wrapped: _Wrapped) -> None:
        self._wrapped = wrapped

    @abc.abstractmethod
    def greet(self) -> str:
        raise NotImplementedError


class StrGreet(BaseGreet[str]):
    def greet(self) -> str:
        return 'Hello, {0}!'.format(self._wrapped)


@dataclass
class MyUser(object):
    name: str


class MyUserGreet(BaseGreet[MyUser]):
    def greet(self) -> str:
        return 'Hello again, {0}'.format(self._wrapped.name)


def greet(instance: BaseGreet):
    return instance.greet()


def demo():
    print(greet(StrGreet('world')))
    print(greet(MyUserGreet(MyUser(name='example'))))
