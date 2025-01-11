#version 460

in vec3 vertices;
uniform vec3 position;

void main() {
    vec3 coord = vertices + position;
    gl_Position = vec4(coord.x, coord.y, coord.z, 1.0);
}
