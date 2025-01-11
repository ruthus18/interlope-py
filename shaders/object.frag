#version 460

struct DirectionLight
{
    vec3 color;
    float ambient_intensity;
    float diffuse_intensity;
    vec3 direction;
};

struct Material
{
    vec3 ambient_color;
    vec3 diffuse_color;
};


// Buffers
in vec3 normals;
in vec2 texcoords;

// Textures
layout (binding=0) uniform sampler2D texture_diff;
// layout (binding=1) uniform sampler2D texture_normal;

uniform DirectionLight light;
uniform Material material;

out vec4 fragColor;


void main() {
    vec4 ambient_color = 
        vec4(light.color, 1.0) *
        light.ambient_intensity *
        vec4(material.ambient_color, 1.0f);

    float diffuse_factor = dot(normalize(normals), -light.direction);
    vec4 diffuse_color = vec4(0.0, 0.0, 0.0, 0.0);

    if (diffuse_factor > 0) {
        diffuse_color =            
            vec4(light.color, 1.0) *
            light.diffuse_intensity *
            vec4(material.diffuse_color, 1.0f);
    }

    // fragColor = texture(texture_diff, texcoords) * vec4(light.color + material.diffuse_color, 1.0);
    fragColor = texture(texture_diff, texcoords) * vec4(light.color + material.diffuse_color + 1.0, 1.0);
}
