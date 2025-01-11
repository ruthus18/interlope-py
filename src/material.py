from dataclasses import dataclass

from glm import vec4


@dataclass
class Material:
    ambient: vec4
    diffuse: vec4
    specular: vec4
    metallic: float
    emission: None = None


PEWTER = Material(
    ambient=vec4(0.11, 0.06, 0.11, 1.0),
    diffuse=vec4(0.43, 0.47, 0.54, 1.0),
    specular=vec4(0.33, 0.33, 0.52, 1.0),
    metallic=9.85,
)

GOLD = Material(
    ambient=vec4(0.2473, 0.1995, 0.0745, 1.0),
    diffuse=vec4(0.7516, 0.6065, 0.2265, 1.0),
    specular=vec4(0.6283, 0.5558, 0.3661, 1.0),
    metallic=51.200,
)

# JADE = Material(
#     ambient=RGBA(0.11, 0.06, 0.11, 1.0),
#     diffuse=RGBA(0.43, 0.47, 0.54, 1.0),
#     specular=RGBA(0.33, 0.33, 0.52, 1.0),
#     metallic=12.800,
# )

# PEARL = Material(
#     ambient=RGBA(0.11, 0.06, 0.11, 1.0),
#     diffuse=RGBA(0.43, 0.47, 0.54, 1.0),
#     specular=RGBA(0.33, 0.33, 0.52, 1.0),
#     metallic=11.264,
# )

# SILVER = Material(
#     ambient=RGBA(0.11, 0.06, 0.11, 1.0),
#     diffuse=RGBA(0.43, 0.47, 0.54, 1.0),
#     specular=RGBA(0.33, 0.33, 0.52, 1.0),
#     metallic=51.200,
# )
