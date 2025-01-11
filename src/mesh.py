import logging
from dataclasses import dataclass

import glm
from glm import vec2
from glm import vec3

from .db import ModelRecord
from .gfx import GfxInstance
from .gfx import MeshGfxData
from .gfx import gfx_load_mesh
from .iofs import iofs_read_mesh_file

logger = logging.getLogger(__name__)


type MeshID = str


@dataclass
class Mesh:
    id: MeshID
    path: str
    gfx_data: MeshGfxData


@dataclass
class ObjFile:
    name: str | None
    vertices: list[vec3]
    normals: list[vec3]
    texcoords: list[vec2]

    # face format: ("v/vt/vn", "v/vt/vn", "v/vt/vn")
    faces: list[tuple[str, str, str]]


# TODO: support Model abstraction (with multiple meshes)
def mesh_load_from_record(record: ModelRecord, gfx: GfxInstance) -> Mesh:
    _, ext = record.path.split('.')

    if ext != 'obj':
        raise NotImplementedError(f'Unsupported mesh extension: {ext}')

    obj = mesh_parse_obj_file(record.path)

    # ----- OBJ -> OPENGL MAPPING -----
    # .obj has data format different than OpenGL, so
    # normals and texcoords should be mapped to each vertex
    face_storage = []
    gl_indices = []
    gl_vertices = []
    gl_texcoords = []
    gl_normals = []

    for face_elem in obj.faces:
        for face in face_elem:
            v_index, tc_index, n_index = (int(i) for i in face.split('/'))

            if face not in face_storage:
                face_storage.append(face)

                gl_vertices.append(obj.vertices[v_index-1])
                gl_texcoords.append(obj.texcoords[tc_index-1])
                gl_normals.append(obj.normals[n_index-1])

            idx = face_storage.index(face)
            gl_indices.append(idx)

    del obj

    # ----- VECTORS UNPACKING -----
    # ([vec3, vec3] -> [f, f, f, f, f, f])
    gl_vertices = [v_i for v in gl_vertices for v_i in v]
    gl_texcoords = [vt_i for vt in gl_texcoords for vt_i in vt]
    gl_normals = [vn_i for vn in gl_normals for vn_i in vn]

    vertex_buffer = gl_vertices + gl_normals + gl_texcoords

    gfx_data = gfx_load_mesh(
        gfx,
        vertex_data=glm.array.from_numbers(glm.float32, *vertex_buffer),
        index_data=glm.array.from_numbers(glm.uint32, *gl_indices),
        vertices_count=int(len(gl_vertices) / 3),
        indices_count=len(gl_indices),
        cw_order=False,  # .obj mesh foramt has CCW ordering
    )
    logger.info(f'Mesh loaded: {record.id}')
    return Mesh(
        id=record.id,
        path=record.path,
        gfx_data=gfx_data,
    )


def mesh_parse_obj_file(path: str) -> ObjFile:
    content = iofs_read_mesh_file(path).split('\n')
    obj_name = None
    vertices = []
    normals = []
    texcoords = []
    faces = []

    for row in content:
        if row.startswith('#'):
            continue

        match row.split(' '):
            case ['o', name]:
                obj_name = name

            case ['v', x, y, z]:
                vertices.append(vec3(float(x), float(y), float(z)))

            case ['vn', x, y, z]:
                normals.append(vec3(float(x), float(y), float(z)))

            case ['vt', s, t]:
                texcoords.append(vec2(float(s), float(t)))

            case ['f', *face_elem]:
                faces.append(face_elem)

            case ['mtllib', *_]:
                pass

            case ['usemtl', *_]:
                pass

            case ['s', id]:
                pass

            case ['']:
                continue

            case unknown:
                raise ValueError(f'Error while parsing OBJ row: {unknown}')

    return ObjFile(
        name=obj_name,
        vertices=vertices,
        normals=normals,
        texcoords=texcoords,
        faces=faces,
    )


# --
# Predefined debug meshes

# PLANE = Mesh(
#     vertices=[
#         -0.5, 0.0,  0.5,   -0.5, 0.0, -0.5,   0.5, 0.0,  0.5,
#         0.5, 0.0,  0.5,   -0.5, 0.0, -0.5,   0.5, 0.0, -0.5,
#     ],
#     texcoords=[
#         0.0, 0.0,    0.0, 1.0,    1.0, 0.0,
#         1.0, 0.0,    0.0, 1.0,    1.0, 1.0,
#     ],
# )

# TODO: size should be = 1m
# CUBE = Mesh(
#     vertices=[
#         # red front
#         0.0, 0.0,  0.0,   0.0, 0.5,  0.0,   0.5, 0.0,  0.0,
#         0.5, 0.0,  0.0,   0.0, 0.5,  0.0,   0.5, 0.5,  0.0,
#         # red back
#         0.5, 0.0, -0.5,   0.5, 0.5, -0.5,   0.0, 0.0, -0.5,
#         0.0, 0.0, -0.5,   0.5, 0.5, -0.5,   0.0, 0.5, -0.5,
#         # blue left
#         0.0, 0.5, -0.5,   0.0, 0.5,  0.0,   0.0, 0.0,  0.0,
#         0.0, 0.0, -0.5,   0.0, 0.5, -0.5,   0.0, 0.0,  0.0,
#         # blue right
#         0.5, 0.0,  0.0,   0.5, 0.5,  0.0,   0.5, 0.0, -0.5,
#         0.5, 0.5,  0.0,   0.5, 0.5, -0.5,   0.5, 0.0, -0.5,
#         # green top
#         0.0, 0.5,  0.0,   0.0, 0.5, -0.5,   0.5, 0.5,  0.0,
#         0.5, 0.5,  0.0,   0.0, 0.5, -0.5,   0.5, 0.5, -0.5,
#         # green bottom
#         0.0, 0.0,  0.0,   0.5, 0.0, -0.5,   0.0, 0.0, -0.5,
#         0.0, 0.0,  0.0,   0.5, 0.0,  0.0,   0.5, 0.0, -0.5,
#     ],
    # texcoords=[  # FIXME
    #     0.0, 0.0,    0.0, 1.0,    1.0, 0.0,
    #     1.0, 0.0,    0.0, 1.0,    1.0, 1.0,
    #     0.0, 0.0,    0.0, 1.0,    1.0, 0.0,
    #     1.0, 0.0,    0.0, 1.0,    1.0, 1.0,

    #     0.0, 0.0,    0.0, 1.0,    1.0, 0.0,
    #     1.0, 0.0,    0.0, 1.0,    1.0, 1.0,
    #     0.0, 0.0,    0.0, 1.0,    1.0, 0.0,
    #     1.0, 0.0,    0.0, 1.0,    1.0, 1.0,

    #     0.0, 0.0,    0.0, 1.0,    1.0, 0.0,
    #     1.0, 0.0,    0.0, 1.0,    1.0, 1.0,
    #     0.0, 0.0,    0.0, 1.0,    1.0, 0.0,
    #     1.0, 0.0,    0.0, 1.0,    1.0, 1.0,
    # ],
# )

# CUBE_COLORED = Mesh(
#     vertices=CUBE.vertices,
#     colors=[
#         # red front
#         1.0, 0.0, 0.0,   1.0, 0.0, 0.0,   1.0, 0.0, 0.0,
#         1.0, 0.0, 0.0,   1.0, 0.0, 0.0,   1.0, 0.0, 0.0,
#         # red back
#         1.0, 0.0, 0.0,   1.0, 0.0, 0.0,   1.0, 0.0, 0.0,
#         1.0, 0.0, 0.0,   1.0, 0.0, 0.0,   1.0, 0.0, 0.0,
#         # blue left
#         0.0, 0.0, 1.0,   0.0, 0.0, 1.0,   0.0, 0.0, 1.0,
#         0.0, 0.0, 1.0,   0.0, 0.0, 1.0,   0.0, 0.0, 1.0,
#         # blue right
#         0.0, 0.0, 1.0,   0.0, 0.0, 1.0,   0.0, 0.0, 1.0,
#         0.0, 0.0, 1.0,   0.0, 0.0, 1.0,   0.0, 0.0, 1.0,
#         # green top
#         0.0, 1.0, 0.0,   0.0, 1.0, 0.0,   0.0, 1.0, 0.0,
#         0.0, 1.0, 0.0,   0.0, 1.0, 0.0,   0.0, 1.0, 0.0,
#         # green bottom
#         0.0, 1.0, 0.0,   0.0, 1.0, 0.0,   0.0, 1.0, 0.0,
#         0.0, 1.0, 0.0,   0.0, 1.0, 0.0,   0.0, 1.0, 0.0,
#     ],
# )
