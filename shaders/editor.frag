#version 460

in vec3 color_buffer;

out vec4 fragColor;


void main() {
    fragColor = vec4(color_buffer, 1.0);
}
