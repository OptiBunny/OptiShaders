#version 450
// SPDX-License-Identifier: MIT
// Separated Y/C input for ColecoVision Clean and S-Video, 2026-09-16.
// These presets deliberately omit Y/C crosstalk. Supply baseband YIQ to the
// following Guest filters, retaining their independent luma/chroma bandwidth.
// This avoids synthetic carrier ripple in the high-bandwidth Clean preset.
// Input colours are Gearcoleco's palette, not measured hardware voltages.

layout(push_constant) uniform Push
{
    vec4 OriginalSize;
    float cv_rgb_passthrough;
    float cv_skew;
    float ntsc_sat;
    float ntsc_bright;
    float ntsc_gamma;
} params;

layout(std140, set = 0, binding = 0) uniform UBO
{
    mat4 MVP;
} global;

#pragma parameter ntsc_sat "NTSC Color Saturation" 1.0 0.0 2.0 0.01
#pragma parameter ntsc_bright "NTSC Brightness" 1.0 0.0 1.5 0.01
#pragma parameter ntsc_gamma "NTSC Filtering Gamma Correction" 1.0 0.25 2.5 0.025

#pragma parameter cv_rgb_passthrough "Coleco RGB geometry pass" 0.0 0.0 1.0 1.0
#pragma parameter cv_skew "Coleco static picture skew (native pixels)" 0.0 -3.0 3.0 0.25

#pragma stage vertex
layout(location = 0) in vec4 Position;
layout(location = 1) in vec2 TexCoord;
layout(location = 0) out vec2 vTexCoord;

void main()
{
    gl_Position = global.MVP * Position;
    vTexCoord = TexCoord;
}

#pragma stage fragment
layout(location = 0) in vec2 vTexCoord;
layout(location = 0) out vec4 FragColor;
layout(set = 0, binding = 2) uniform sampler2D Source;

void main()
{
    vec2 uv=vTexCoord;
    if(params.cv_rgb_passthrough>0.5){
        float yy=2.0*uv.y-1.0;
        uv.x+=params.cv_skew*yy*yy*yy*params.OriginalSize.z;
        FragColor=vec4(texture(Source,uv).rgb,1.0);return;
    }
    vec3 rgb=texture(Source,uv).rgb;
    float y = pow(max(dot(rgb, vec3(0.2989, 0.5870, 0.1140)), 0.0), params.ntsc_gamma);
    float i = dot(rgb, vec3(0.5959, -0.2744, -0.3216));
    float q = dot(rgb, vec3(0.2115, -0.5229, 0.3114));
    FragColor = vec4(params.ntsc_bright * y, params.ntsc_sat * i, params.ntsc_sat * q, y);
}
