#version 460

uniform vec3 base_color;
out vec4 fragColor;

void main() {
    fragColor = vec4(base_color.x, base_color.y, base_color.z, 1.0);
}
