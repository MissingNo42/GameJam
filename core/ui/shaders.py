from kivy.properties import NumericProperty
from kivy.uix.effectwidget import EffectBase


__all__ = (
    "ChromaticAberationSickness0",
    "ChromaticAberationSickness1",
    "ChromaticAberationSickness2",
    "ChromaticAberationSickness3",
)


class ChromaticAberationSickness0(EffectBase):
    '''Adds scanlines to the input.'''

    life = NumericProperty(0)

    def __init__(self, *args, **kwargs):
        super(ChromaticAberationSickness0, self).__init__(*args, **kwargs)
        self.do_glsl()

    def on_life(self, *x):
        self.do_glsl()

    def do_glsl(self):
        self.glsl = '''
vec4 effect(vec4 color, sampler2D texture, vec2 tex_coords, vec2 coords)
{{
vec2 q = tex_coords * vec2(1, -1);

// Add a large animated distortion to the texture coordinates, scaled by lifeFactor
float wave = sin(time + q.y * 5.0) * 0.05 * {0}/100;
float wave2 = cos(time + q.x * 2.0) * 0.05 * {0}/100;
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

if({0} > 50) 
{{
// Apply much more subtle psychedelic color cycling using time-based sinusoidal functions
float colorShiftStrength = 0.1;  // Lower strength for subtle shifts
col.r = col.r + sin(time * 1.0) * colorShiftStrength;  // Smaller modulation
col.g = col.g + sin(time * 1.2) * colorShiftStrength;
col.b = col.b + sin(time * 1.4) * colorShiftStrength;
}}

// Apply a time-based factor to animate distortion, slightly reducing overall brightness
col *= 0.95;
col *= 0.97;

// You can keep the original blending logic if desired
// float comp = smoothstep(0.2, 0.7, sin(time));
// col = mix(col, oricol, clamp(-2.0 + 2.0 * q.x + 3.0 * comp, 0.0, 1.0));

return vec4(col, color.w);
}}
'''.format(float(self.life))


class ChromaticAberationSickness1(EffectBase):
    '''Adds scanlines to the input.'''
    def __init__(self, *args, **kwargs):
        super(ChromaticAberationSickness1, self).__init__(*args, **kwargs)
        self.glsl = '''
vec4 effect(vec4 color, sampler2D texture, vec2 tex_coords, vec2 coords)
{
 vec2 q = tex_coords * vec2(1, -1);

// Add a large animated distortion to the texture coordinates, scaled by lifeFactor
float wave = sin(time + q.y * 0.0) * 0.05 * lifeFactor;
float wave2 = cos(time + q.x * 0.0) * 0.05 * lifeFactor;
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

// Apply a time-based factor to animate distortion, slightly reducing overall brightness
col *= 0.95;
col *= 0.97;

// You can keep the original blending logic if desired
// float comp = smoothstep(0.2, 0.7, sin(time));
// col = mix(col, oricol, clamp(-2.0 + 2.0 * q.x + 3.0 * comp, 0.0, 1.0));

return vec4(col, color.w);
}
'''

class ChromaticAberationSickness2(EffectBase):
    '''Adds scanlines to the input.'''
    def __init__(self, *args, **kwargs):
        super(ChromaticAberationSickness2, self).__init__(*args, **kwargs)
        self.glsl = '''
vec4 effect(vec4 color, sampler2D texture, vec2 tex_coords, vec2 coords)
{
  vec2 q = tex_coords * vec2(1, -1);

// Add a large animated distortion to the texture coordinates
float wave = sin(time + q.y * 1.0) * 0.05;
float wave2 = cos(time + q.x * 1.0) * 0.05;
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

// Apply a time-based factor to animate distortion, slightly reducing overall brightness
col *= 0.95;
col *= 0.97;


// Removed original color blending for the distortion effect
// You can keep this line if you want to blend the original color with the distorted version
// float comp = smoothstep(0.2, 0.7, sin(time));
// col = mix(col, oricol, clamp(-2.0 + 2.0 * q.x + 3.0 * comp, 0.0, 1.0));


return vec4(col, color.w);
}
'''


class ChromaticAberationSickness3(EffectBase):
    '''Adds scanlines to the input.'''
    def __init__(self, *args, **kwargs):
        super(ChromaticAberationSickness3, self).__init__(*args, **kwargs)
        self.glsl = '''
vec4 effect(vec4 color, sampler2D texture, vec2 tex_coords, vec2 coords)
{
vec2 q = tex_coords * vec2(1, -1);

// Add a large animated distortion to the texture coordinates
float wave = sin(time + q.y * 10.0) * 0.05;
float wave2 = cos(time + q.x * 5.0) * 0.05;
vec2 uv = 0.5 + (q - 0.5) + vec2(wave, wave2); // Distortion applied to uv coordinates

vec3 oricol = texture2D(texture, vec2(q.x, 1.0 - q.y)).xyz;
vec3 col;

// Sample red, green, and blue channels with small offsets based on distorted uv
col.r = texture2D(texture, vec2(uv.x + 0.003, -uv.y)).x;
col.g = texture2D(texture, vec2(uv.x + 0.000, -uv.y)).y;
col.b = texture2D(texture, vec2(uv.x - 0.003, -uv.y)).z;

// Apply much more subtle psychedelic color cycling using time-based sinusoidal functions
float colorShiftStrength = 0.1;  // Lower strength for subtle shifts
col.r = col.r + sin(time * 1.0) * colorShiftStrength;  // Smaller modulation
col.g = col.g + sin(time * 1.2) * colorShiftStrength;
col.b = col.b + sin(time * 1.4) * colorShiftStrength;

// Apply more moderate color adjustment for less exaggerated contrast
col = clamp(col * 0.5 + 0.5 * col * col * 1.2, 0.0, 1.0);

// Introduce softer, slower color tints
col *= vec3(1.1, 0.95, 1.1) * (0.95 + 0.05 * sin(time * 0.5));  // More subtle tint shifting

// Apply a very subtle sine modulation for light pulsations in brightness
col *= 0.98 + 0.02 * sin(time * 0.8 + uv.y * 50.0);  // Much slower and reduced pulsing

return vec4(col, color.w);

}
'''
