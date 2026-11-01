#version 450
// SPDX-License-Identifier: MIT
// ColecoVision NTSC encoder, custom adaptation, 2026-09-15.
// Original implementation of a fixed-phase RGB-to-YIQ modulation stage.
// Interface compatible with guest(r)'s NTSC-Adaptive decode passes, based on
// Themaister's NTSC work. No guest shader source is embedded in this file.
//
// TMS9928A: pixel clock = master / 2; NTSC carrier = master / 3.
// 342 pixel clocks per line therefore contain 228 complete carrier cycles.
// Hold phase across rows and frames instead of importing NES phase rotation.
// Absolute encoder phase is an approximation, adjustable in cycles below.
// The input is Gearcoleco's rendered palette, not measured analogue voltages.

layout(push_constant) uniform Push
{
    vec4 OriginalSize;
    float ntsc_sat;
    float cust_fringing;
    float cust_artifacting;
    float ntsc_bright;
    float ntsc_gamma;
    float cv_phase_offset;
    float cv_board_strength;
} params;

layout(std140, set = 0, binding = 0) uniform UBO
{
    mat4 MVP;
} global;

#pragma parameter cust_artifacting "NTSC Artifacting Value" 1.0 0.0 5.0 0.1
#pragma parameter cust_fringing "NTSC Fringing Value" 1.0 0.0 5.0 0.1
#pragma parameter ntsc_sat "NTSC Color Saturation" 1.0 0.0 2.0 0.01
#pragma parameter ntsc_bright "NTSC Brightness" 1.0 0.0 1.5 0.01
#pragma parameter ntsc_gamma "NTSC Filtering Gamma Correction" 1.0 0.25 2.5 0.025
#pragma parameter cv_phase_offset "Coleco NTSC carrier phase offset (cycles)" 0.0 0.0 1.0 0.08333333

#pragma parameter cv_board_strength "Coleco experimental board response" 0.0 0.0 1.0 0.25

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


// Isolated rev F network; source/loading unmeasured.
const float cv_filter_Y[64] = float[64](0.1532613948,0.2793704281,0.2525240890,0.1761811710,0.1016150680,0.0473175228,0.0147953053,-0.0011215418,-0.0067120451,-0.0070138844,-0.0052807791,-0.0032510466,-0.0016454699,-0.0006190118,-0.0000766588,0.0001440458,0.0001877691,0.0001545515,0.0001016203,0.0000553213,0.0000236515,0.0000057206,-0.0000024141,-0.0000047872,-0.0000044055,-0.0000031057,-0.0000018083,-0.0000008529,-0.0000002754,0.0000000106,0.0000001136,0.0000001218,0.0000000928,0.0000000577,0.0000000295,0.0000000113,0.0000000016,-0.0000000024,-0.0000000032,-0.0000000027,-0.0000000018,-0.0000000010,-0.0000000004,-0.0000000001,0.0000000000,0.0000000001,0.0000000001,0.0000000001,0.0000000000,0.0000000000,0.0000000000,-0.0000000000,-0.0000000000,-0.0000000000,-0.0000000000,-0.0000000000,-0.0000000000,-0.0000000000,-0.0000000000,0.0000000000,0.0000000000,0.0000000000,0.0000000000,0.0000000000);
const float cv_filter_C[64] = float[64](0.0176287222,0.0469029069,0.0680233092,0.0821043473,0.0902486391,0.0935123406,0.0928798317,0.0892465099,0.0834084535,0.0760577646,0.0677824752,0.0590699951,0.0503131917,0.0418183040,0.0338140138,0.0264611049,0.0198622541,0.0140715912,0.0091037579,0.0049422698,0.0015470569,-0.0011388903,-0.0031837916,-0.0046622546,-0.0056513168,-0.0062272943,-0.0064633612,-0.0064277783,-0.0061826860,-0.0057833743,-0.0052779488,-0.0047073145,-0.0041054071,-0.0034996080,-0.0029112881,-0.0023564330,-0.0018463100,-0.0013881455,-0.0009857866,-0.0006403295,-0.0003506987,-0.0001141715,0.0000731612,0.0002159960,0.0003194818,0.0003889436,0.0004296634,0.0004467109,0.0004448192,0.0004283010,0.0004009960,0.0003662479,0.0003269021,0.0002853211,0.0002434135,0.0002026703,0.0001642091,0.0001288192,0.0000970092,0.0000690524,0.0000450304,0.0000248734,0.0000083963,-0.0000046687);
vec3 cv_board(vec2 uv) {
 vec3 direct=texture(Source,uv).rgb;
 if(params.cv_board_strength<=0.0)return direct;
 vec3 filtered=vec3(0.0);
 for(int k=0;k<64;k++){
  vec3 col=texture(Source,uv-vec2(float(k)*0.25*params.OriginalSize.z,0.0)).rgb;
  float yy=dot(col,vec3(0.2989,0.5870,0.1140));
  filtered+=yy*cv_filter_Y[k]+(col-yy)*cv_filter_C[k];
 }
 return mix(direct,filtered,params.cv_board_strength);
}

void main()
{
    vec3 rgb = cv_board(vTexCoord);
    float y = pow(max(dot(rgb, vec3(0.2989, 0.5870, 0.1140)), 0.0), params.ntsc_gamma);
    float i = dot(rgb, vec3(0.5959, -0.2744, -0.3216));
    float q = dot(rgb, vec3(0.2115, -0.5229, 0.3114));

    // Anchor to the 256-pixel active image when the core includes side borders.
    float border = max(params.OriginalSize.x - 256.0, 0.0) * 0.5;
    float x = vTexCoord.x * params.OriginalSize.x - border;
    float theta = 6.283185307179586 * (x * (2.0 / 3.0) + params.cv_phase_offset);
    float c = cos(theta);
    float s = sin(theta);

    // Y/C crosstalk plus synchronous quadrature demodulation. The subsequent
    // Guest FIR stage rejects the residual carrier and limits Y/C bandwidth.
    float luma = params.ntsc_bright * y + params.cust_fringing * (i * c + q * s);
    float chroma_i = params.cust_artifacting * y * c + 2.0 * params.ntsc_sat * i * c * c;
    float chroma_q = params.cust_artifacting * y * s + 2.0 * params.ntsc_sat * q * s * s;
    FragColor = vec4(luma, chroma_i, chroma_q, y);
}
