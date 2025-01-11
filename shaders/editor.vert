#version 460

layout (location=0) in vec3 vertex;
layout (location=1) in vec3 color;

uniform mat4 m_persp;
uniform mat4 m_view;
uniform mat4 m_model;

out vec3 color_buffer;


void main() {
    gl_Position = gm_persp * gm_view * gm_model * vec4(vertex, 1.0);

    color_buffer = color;
}
