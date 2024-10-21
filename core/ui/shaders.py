from kivy.properties import NumericProperty
from kivy.uix.effectwidget import EffectBase, AdvancedEffectBase

__all__ = (
    "ChromaticAberationSickness",
)


class ChromaticAberationSickness(AdvancedEffectBase):
    '''Adds scanlines to the input.'''

    life = NumericProperty(0)

    def __init__(self, *args, **kwargs):
        super(ChromaticAberationSickness, self).__init__(uniforms={"lifeFactor": self.life}, *args, **kwargs)
        self.do_glsl()

    def on_life(self, *x):
        self.uniforms["lifeFactor"] = self.life

    def do_glsl(self):
        print("Compile Shader...")
        self.glsl = '''
uniform float lifeFactor;
vec4 effect(vec4 color, sampler2D texture, vec2 tex_coords, vec2 coords)
{
vec2 q = tex_coords * vec2(1, -1);

// Add a large animated distortion to the texture coordinates, scaled by lifeFactor
float wave = sin(time + q.y * 5.0) * 0.05 * lifeFactor/100;
float wave2 = cos(time + q.x * 2.0) * 0.05 * lifeFactor/100;
vec2 uv = 0.5 + (q - 0.5) + vec2(wave, wave2); // Distortion applied to uv coordinates

vec3 oricol = texture2D(texture, vec2(q.x, 1.0 - q.y)).xyz;
vec3 col;

// Sample red, green, and blue channels with small offsets based on distorted uv
col.r = texture2D(texture, vec2(uv.x + 0.003, -uv.y)).x;
col.g = texture2D(texture, vec2(uv.x + 0.000, -uv.y)).y;
col.b = texture2D(texture, vec2(uv.x - 0.003, -uv.y)).z;

// Color adjustment, using a more subtle tone mapping
col = clamp(col * 0.5 + 0.5 * col * col * 1.2, 0.0, 1.0);

// Multiply color by a fixed vec3 value for subtle tinting
col *= vec3(0.8, 1.0, 0.7);

if(lifeFactor > 50) 
{
// Apply much more subtle psychedelic color cycling using time-based sinusoidal functions
float colorShiftStrength = 0.1;  // Lower strength for subtle shifts
col.r = col.r + sin(time * 1.0) * colorShiftStrength;  // Smaller modulation
col.g = col.g + sin(time * 1.2) * colorShiftStrength;
col.b = col.b + sin(time * 1.4) * colorShiftStrength;
}

// Apply a time-based factor to animate distortion, slightly reducing overall brightness
col *= 0.95;
col *= 0.97;

// You can keep the original blending logic if desired
// float comp = smoothstep(0.2, 0.7, sin(time));
// col = mix(col, oricol, clamp(-2.0 + 2.0 * q.x + 3.0 * comp, 0.0, 1.0));

return vec4(col, color.w);
}
'''
