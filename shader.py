import pygame
import moderngl
import numpy as np


class ShaderRenderer:
    def __init__(self, width, height):
        """
        Initialize Pygame and ModernGL with shader support

        Args:
            width (int): Width of the rendering window
            height (int): Height of the rendering window
        """
        # Initialize Pygame
        pygame.init()

        # Set up OpenGL context for Pygame
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

        # Create the window
        self.screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
        pygame.display.set_caption("Pygame ModernGL Shader Example")

        # Create ModernGL context
        self.ctx = moderngl.create_context()

        # Set up viewport
        self.ctx.viewport = (0, 0, width, height)

    def create_shader_program(self, vertex_shader, fragment_shader):
        """
        Create a shader program from vertex and fragment shader sources

        Args:
            vertex_shader (str): Vertex shader source code
            fragment_shader (str): Fragment shader source code

        Returns:
            moderngl.Program: Compiled shader program
        """
        # Compile shader program
        prog = self.ctx.program(
            vertex_shader=vertex_shader,
            fragment_shader=fragment_shader
        )
        return prog

    def create_quad_buffer(self):
        """
        Create a quad covering the entire screen

        Returns:
            moderngl.Buffer: Vertex buffer for a full-screen quad
        """
        # Vertex data for a full-screen quad
        vertices = np.array([
            # x,    y,   u,   v
            -1.0, -1.0, 0.0, 0.0,
            1.0, -1.0, 1.0, 0.0,
            -1.0, 1.0, 0.0, 1.0,
            1.0, 1.0, 1.0, 1.0
        ], dtype='f4')

        # Create vertex buffer
        return self.ctx.buffer(vertices.tobytes())

    def run_basic_shader_example(self):
        """
        Run a basic example of shader rendering
        """
        # Vertex shader
        vertex_shader = """
        #version 330

        in vec2 in_position;
        in vec2 in_texcoord_0;

        out vec2 v_texcoord;

        void main() {
            gl_Position = vec4(in_position, 0.0, 1.0);
            v_texcoord = in_texcoord_0;
        }
        """

        # Fragment shader (simple color gradient)
        fragment_shader = """
        #version 330

        out vec4 f_color;
        in vec2 v_texcoord;

        uniform float time;

        void main() {
            // Create a color gradient that changes over time
            vec3 color = vec3(
                abs(sin(time + v_texcoord.x * 3.0)),
                abs(cos(time + v_texcoord.y * 3.0)),
                abs(sin(time * 0.5 + v_texcoord.x + v_texcoord.y))
            );

            f_color = vec4(color, 1.0);
        }
        """

        # Create shader program
        prog = self.create_shader_program(vertex_shader, fragment_shader)

        # Create quad buffer
        quad_buffer = self.create_quad_buffer()

        # Create vertex array object (VAO)
        vao = self.ctx.vertex_array(
            prog,
            [(quad_buffer, '2f 2f', 'in_position', 'in_texcoord_0')]
        )

        # Clock for timing
        clock = pygame.time.Clock()

        # Main game loop
        running = True
        start_time = pygame.time.get_ticks()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Clear the screen
            self.ctx.clear(0.0, 0.0, 0.0)

            # Update time uniform
            current_time = (pygame.time.get_ticks() - start_time) / 1000.0
            prog['time'].value = current_time

            # Render the quad with shader
            vao.render()

            # Swap buffers
            pygame.display.flip()

            # Control frame rate
            clock.tick(60)

        # Clean up
        vao.release()
        quad_buffer.release()
        prog.release()

    def run(self):
        """
        Run the shader demonstration
        """
        try:
            self.run_basic_shader_example()
        finally:
            # Quit Pygame
            pygame.quit()


# Example usage
if __name__ == "__main__":
    renderer = ShaderRenderer(800, 600)
    renderer.run()
