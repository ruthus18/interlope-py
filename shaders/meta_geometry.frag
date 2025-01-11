#version 460

in vec3 color_buffer;

uniform vec3 object_color;

out vec4 fragColor;


void main() {
    if (has_color_buffer) {
        fragColor = vec4(color_buffer * light_color, 1.0);
    }
    else {
        fragColor = vec4(object_color * light_color, 1.0);
    }
}
