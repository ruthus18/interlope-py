"""gfx - Graphics Module

OpenGL backend for 3D graphics processing
"""
import enum
import logging
from ctypes import c_void_p
from dataclasses import dataclass

import glm
from glm import mat4
from glm import vec3
from OpenGL import GL as g
from PIL import Image

from .config import config
from .gfx_uniform import UniformPtr
from .gfx_uniform import UniformType
from .gfx_uniform import uniform_create
from .gfx_uniform import uniform_set
from .iofs import iofs_read_shader_file

logger = logging.getLogger(__name__)


_SHADER_EXTENSIONS = {
    'vert': g.GL_VERTEX_SHADER,
    'frag': g.GL_FRAGMENT_SHADER,
}

class ShaderPath:
    OBJECT_VERT = 'object.vert'
    OBJECT_FRAG = 'object.frag'
    META_GEOMETRY_VERT = 'meta_geometry.vert'
    META_GEOMETRY_FRAG = 'meta_geometry.frag'


class DrawMode(enum.StrEnum):
    points = enum.auto()
    lines = enum.auto()
    triangles = enum.auto()


@dataclass
class MeshGfxData:
    vao: int
    vbo: int
    ibo: int
    vertices_count: int
    indices_count: int
    cw_order: bool


@dataclass
class TextureGfxData:
    id: int


@dataclass
class GfxData:
    m_persp: UniformPtr[mat4]
    m_view: UniformPtr[mat4]
    m_model: UniformPtr[mat4]

    light_color: UniformPtr[vec3]
    # light_ambient_intensity: UniformPtr[float]
    # light_diffuse_intensity: UniformPtr[float]
    # light_direction: UniformPtr[vec3]

    # material_ambient_color: UniformPtr[vec3]
    # material_diffuse_color: UniformPtr[vec3]


@dataclass
class GfxInstance:
    obj_program: int
    data: GfxData


def gfx_create() -> GfxInstance:
    g.glPointSize(6)
    g.glLineWidth(2)
    g.glEnable(g.GL_CULL_FACE)
    g.glEnable(g.GL_DEPTH_TEST)

    # TODO toggler
    # g.glPolygonMode(g.GL_FRONT_AND_BACK, g.GL_LINE)
    # g.glPolygonMode(g.GL_FRONT_AND_BACK, g.GL_FILL)

    program = gfx_create_program(ShaderPath.OBJECT_VERT, ShaderPath.OBJECT_FRAG)
    gfx_use_program(program)

    # -- Camera data
    m_persp = uniform_create(program, 'm_persp', UniformType.mat4)
    m_view = uniform_create(program, 'm_view', UniformType.mat4)
    m_model = uniform_create(program, 'm_model', UniformType.mat4)

    # -- Shading data
    light_color = uniform_create(program, 'light.color', UniformType.vec3)
    # light_ambient_intensity = uniform_create(
    #     program, 'light.ambient_intensity', UniformType.float
    # )
    # light_diffuse_intensity = uniform_create(
    #     program, 'light.diffuse_intensity', UniformType.float
    # )
    # light_direction = uniform_create(
    #     program, 'light.direction', UniformType.vec3
    # )

    # material_ambient_color = uniform_create(
    #     program, 'material.ambient_color', UniformType.vec3
    # )
    # material_diffuse_color = uniform_create(
    #     program, 'material.diffuse_color', UniformType.vec3
    # )

    gfx_use_program(0)

    return GfxInstance(
        obj_program=program,
        data=GfxData(
            m_persp=m_persp,
            m_model=m_model,
            m_view=m_view,
            light_color=light_color,
            # light_ambient_intensity=light_ambient_intensity,
            # light_diffuse_intensity=light_diffuse_intensity,
            # light_direction=light_direction,
            # material_ambient_color=material_ambient_color,
            # material_diffuse_color=material_diffuse_color,
        ),
    )


def gfx_log_info() -> None:
    vendor = g.glGetString(g.GL_VENDOR).decode()
    renderer = g.glGetString(g.GL_RENDERER).decode()
    gl_version = g.glGetString(g.GL_VERSION).decode()

    logger.info(f'')
    logger.info(f'======  {config.WINDOW_TITLE}  ======')
    logger.info(f'OPENGL VERSION: {gl_version}')
    logger.info(f'VIDEO DEVICE: {vendor} ({renderer})')
    logger.info(f'RESOLUTION: {config.WINDOW_WIDTH} x {config.WINDOW_HEIGHT}')
    logger.info('------')


should_stop: bool = False


def gfx_should_stop() -> bool:
    global should_stop
    return should_stop


def gfx_stop() -> None:
    global should_stop
    should_stop = True


def gfx_shutdown() -> None:
    # TODO opengl shutdown
    logger.info('Rendering shutdown. See you next time')


def gfx_create_program(*shader_paths: list[str]) -> int:
    program = g.glCreateProgram()

    if program == 0:
        raise RuntimeError('Unable to create OpenGL Program')

    for path in shader_paths:
        gfx_compile_shader(program, path)

    # -- Program Linking
    g.glLinkProgram(program)

    link_ok = g.glGetProgramiv(program, g.GL_LINK_STATUS)
    if not link_ok:
        error_msg = g.glGetProgramInfoLog(program)
        g.glDeleteProgram(program)

        raise RuntimeError(
            f'Program linking error:\n{error_msg}'
        )
    else:
        logger.debug('OpenGL program linked')

    # -- Program Validation
    g.glValidateProgram(program)

    program_ok = g.glGetProgramiv(program, g.GL_VALIDATE_STATUS)
    if not program_ok:
        error_msg = g.glGetProgramInfoLog(program)
        g.glDeleteProgram(program)

        raise RuntimeError(
            f'Program validation error:\n{error_msg}'
        )
    else:
        logger.debug('OpenGL program validated')

    return program


def gfx_compile_shader(program: int, shader_filename: str):
    ext = shader_filename.split('.')[1]

    shader_type = _SHADER_EXTENSIONS[ext]
    shader_src = iofs_read_shader_file(shader_filename)

    shader = g.glCreateShader(shader_type)
    if shader == 0:
        raise RuntimeError(f'Unable to create OpenGL Shader; shader_id={shader}')
    
    g.glShaderSource(shader, shader_src)
    g.glCompileShader(shader)

    compile_ok = g.glGetShaderiv(shader, g.GL_COMPILE_STATUS)
    if not compile_ok:
        error_msg = g.glGetShaderInfoLog(shader).decode()
        g.glDeleteShader(shader)

        logger.exception(
            f'Shader compilation error: {shader_filename}\n'
            f'{error_msg}'
        )
    else:
        logger.info(f'Shader compiled: {shader_filename}')

    g.glAttachShader(program, shader)


def gfx_use_program(program: int) -> None:
    g.glUseProgram(program)


def gfx_clear() -> None:
    g.glClear(g.GL_COLOR_BUFFER_BIT)
    g.glClearColor(*config.WINDOW_COLOR)
    g.glClear(g.GL_DEPTH_BUFFER_BIT)


def _create_vertex_buffer(data: glm.array) -> int:
    vbo = g.glGenBuffers(1)

    g.glBindBuffer(g.GL_ARRAY_BUFFER, vbo)
    g.glBufferData(
        g.GL_ARRAY_BUFFER, data.nbytes, data.ptr, g.GL_STATIC_DRAW
    )
    return vbo


def _create_index_buffer(data: glm.array) -> int:
    ibo = g.glGenBuffers(1)

    g.glBindBuffer(g.GL_ELEMENT_ARRAY_BUFFER, ibo)
    g.glBufferData(
        g.GL_ELEMENT_ARRAY_BUFFER, data.nbytes, data.ptr, g.GL_STATIC_DRAW
    )
    return ibo


def _enable_buffer_attribute(attr: int, ptr: c_void_p, size: int = 3) -> None:
    g.glVertexAttribPointer(attr, size, g.GL_FLOAT, False, 0, ptr)
    g.glEnableVertexAttribArray(attr)


def gfx_load_mesh(
    self: GfxInstance,
    vertex_data: glm.array,
    index_data: glm.array,
    vertices_count: int,
    indices_count: int,
    cw_order: bool,
) -> MeshGfxData:
    gfx_use_program(self.obj_program)

    vao = g.glGenVertexArrays(1)
    g.glBindVertexArray(vao)

    vbo = _create_vertex_buffer(vertex_data)
    ibo = _create_index_buffer(index_data)

    # -- Enable buffer attributes
    # buffer format: (v1, v2, ..., vn1, vn2, ..., vt1, vt2, ...)
    #
    # More about formats: https://stackoverflow.com/a/39684775
    #
    vertex_attr = 0
    vertex_ptr = c_void_p(0)

    normal_attr = 1
    normal_ptr = c_void_p(glm.sizeof(vec3) * vertices_count)

    texcoord_attr = 2
    texcoord_ptr = c_void_p(glm.sizeof(vec3) * vertices_count * 2)

    _enable_buffer_attribute(vertex_attr, vertex_ptr)
    _enable_buffer_attribute(normal_attr, normal_ptr)
    _enable_buffer_attribute(texcoord_attr, texcoord_ptr, 2)

    # -- Cleanup

    g.glBindBuffer(g.GL_ARRAY_BUFFER, 0)
    g.glBindBuffer(g.GL_ELEMENT_ARRAY_BUFFER, 0)
    g.glBindVertexArray(0)
    gfx_use_program(0)

    logger.debug('Mesh loaded')
    return MeshGfxData(
        vao=vao,
        vbo=vbo,
        ibo=ibo,
        vertices_count=vertices_count,
        indices_count=indices_count,
        cw_order=cw_order,
    )


def gfx_load_texture(self: GfxInstance, image: Image) -> TextureGfxData:
    gfx_use_program(self.obj_program)

    texture = g.glGenTextures(1)
    # g.glActiveTexture(g.GL_TEXTURE0)
    g.glBindTexture(g.GL_TEXTURE_2D, texture)
    
    num_components = len(image.getbands())
    match num_components:
        case 1:
            format = g.GL_RED
        case 3:
            format = g.GL_RGB
        case _:
            format = g.GL_RGBA

    # -- Texture Loading
    g.glTexImage2D(
        g.GL_TEXTURE_2D,       # target
        0,                     # mipmap level
        format,              # tex format
        image.width,         # width
        image.height,         # height
        0,                     # some legacy stuff...
        format,              # source format
        g.GL_UNSIGNED_BYTE,    # source datatype
        image.tobytes(),
    )
    g.glGenerateMipmap(g.GL_TEXTURE_2D)

    # -- Texture Parameters
    g.glTexParameteri(g.GL_TEXTURE_2D, g.GL_TEXTURE_WRAP_S, g.GL_REPEAT)
    g.glTexParameteri(g.GL_TEXTURE_2D, g.GL_TEXTURE_WRAP_T, g.GL_REPEAT)
    g.glTexParameteri(g.GL_TEXTURE_2D, g.GL_TEXTURE_MIN_FILTER, g.GL_LINEAR_MIPMAP_LINEAR)
    g.glTexParameteri(g.GL_TEXTURE_2D, g.GL_TEXTURE_MAG_FILTER, g.GL_LINEAR)

    # -- Cleanup
    gfx_use_program(0)

    return TextureGfxData(id=texture)


def gfx_draw_scene(
    self: GfxInstance,
    persp_mat: mat4,
    view_mat: mat4,
    objects_queue: tuple[tuple[MeshGfxData, TextureGfxData, mat4]],
) -> None:
    gfx_clear()

    # -- Object Renderer --
    gfx_use_program(self.obj_program)

    gfx_set_draw_camera(self, persp_mat, view_mat)
    
    for gpu_mesh, gpu_texture, model_mat in objects_queue:
        gfx_draw(self, gpu_mesh, gpu_texture, model_mat)

    # -- Cleanup --
    gfx_use_program(0)


def gfx_set_light(self: GfxInstance, color: tuple) -> None:
    uniform_set(self.data.light, vec3(*color))


def gfx_set_draw_camera(self: GfxInstance, persp_mat: mat4, view_mat: mat4) -> None:
    uniform_set(self.data.m_persp, persp_mat)
    uniform_set(self.data.m_view, view_mat)


def gfx_draw(
    self: GfxInstance,
    mesh: MeshGfxData,
    texture: TextureGfxData,
    model_mat: mat4,
) -> None:
    # -- 1. Draw textures
    # g.glActiveTexture(g.GL_TEXTURE0)
    g.glBindTexture(g.GL_TEXTURE_2D, texture.id)
    # sampler = uniform_create(state.program, 'texture_out', UniformType.int)
    # uniform_set(sampler, 0)

    # -- 2. Draw Mesh
    g.glBindVertexArray(mesh.vao)
    uniform_set(self.data.m_model, model_mat)

    g.glBindBuffer(g.GL_ARRAY_BUFFER, mesh.vbo)
    g.glBindBuffer(g.GL_ELEMENT_ARRAY_BUFFER, mesh.ibo)

    face_orient = g.GL_CW if mesh.cw_order else g.GL_CCW
    g.glFrontFace(face_orient)

    g.glDrawElements(
        g.GL_TRIANGLES, mesh.indices_count, g.GL_UNSIGNED_INT, None
    )

    # -- 3. Reset texture binding
    g.glBindTexture(g.GL_TEXTURE_2D, 0)
