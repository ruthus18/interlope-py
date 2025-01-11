#version 330

in vec3 position;
in vec3 vertex_color;
out vec3 color;

void main() {
    gl_Position = vec4(position.x, position.y, position.z, 1.0);
    color = vertex_color;
}
