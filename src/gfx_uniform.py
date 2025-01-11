import enum
import typing as t
from dataclasses import dataclass

from glm import mat4
from glm import value_ptr
from glm import vec2
from glm import vec3
from glm import vec4
from OpenGL import GL as g

UniformData: t.TypeAlias = bool | int | float | vec2 | vec3 | vec4 | mat4


type UniformPtr[T] = int


class UniformType(enum.StrEnum):
    int = enum.auto()
    bool = enum.auto()
    float = enum.auto()
    vec2 = enum.auto()
    vec3 = enum.auto()
    vec4 = enum.auto()
    mat4 = enum.auto()


@dataclass
class Uniform:
    id: int
    name: str
    type: UniformType
    data: UniformData | None = None


def uniform_create(program: int, name: str, type: UniformType) -> Uniform:
    uniform_id = g.glGetUniformLocation(program, name)
    if uniform_id == -1:
        raise RuntimeError(f'Not found shader uniform: {name}')

    return Uniform(id=uniform_id, name=name, type=type)


def uniform_set(uniform: Uniform, data: UniformData) -> None:
    match uniform.type:
        case UniformType.bool:
            assert isinstance(data, bool)
            g.glUniform1i(uniform.id, int(data))

        case UniformType.int:
            assert isinstance(data, int)
            g.glUniform1i(uniform.id, data)

        case UniformType.float:
            assert isinstance(data, float)
            g.glUniform1f(uniform.id, data)

        case UniformType.vec2:
            assert isinstance(data, vec2)
            g.glUniform2f(uniform.id, *tuple(data))

        case UniformType.vec3:
            assert isinstance(data, vec3)
            g.glUniform3f(uniform.id, *tuple(data))

        case UniformType.vec4:
            assert isinstance(data, vec4)
            g.glUniform4f(uniform.id, *tuple(data))

        case UniformType.mat4:
            assert isinstance(data, mat4)
            g.glUniformMatrix4fv(uniform.id, 1, g.GL_FALSE, value_ptr(data))

        case _:
            raise ValueError
