#version 330 core

layout (location = 0) in vec4 Vertex;
layout (location = 1) in vec3 Color;

uniform mat4 MVP_Matrix;

out vec3 FragColor;

void main(void) {
        gl_Position = MVP_Matrix * Vertex;
        FragColor = Color;
}
