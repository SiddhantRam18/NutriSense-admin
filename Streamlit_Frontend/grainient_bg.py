import streamlit as st

def add_grainient_background(
    color1="#9fffe4",
    color2="#274cff", 
    color3="#B497CF",
    timeSpeed=0.25,
    colorBalance=0.0,
    warpStrength=1.0,
    warpFrequency=5.0,
    warpSpeed=2.0,
    warpAmplitude=50.0,
    blendAngle=0.0,
    blendSoftness=0.05,
    rotationAmount=500.0,
    noiseScale=2.0,
    grainAmount=0.1,
    grainScale=2.0,
    grainAnimated=False,
    contrast=1.5,
    gamma=1.0,
    saturation=1.0,
    centerX=0.0,
    centerY=0.0,
    zoom=0.9
):
    """
    Add an animated Grainient-style background to the Streamlit page.

    Streamlit components render in sandboxed iframes, so using components.html()
    for a page background is fragile: the injected node may exist in the DOM but
    still sit behind Streamlit's opaque app shell. Injecting CSS directly into the
    Streamlit document and painting .stApp keeps the background in the same
    stacking context as the page content.
    """

    duration = max(10 / max(timeSpeed, 0.1), 5)
    flow_duration = max(4.5 / max(timeSpeed, 0.1), 10)
    grain_opacity = max(0.18, min(grainAmount * 3.2, 0.42))
    grain_frequency = max(0.65, min(2.4 / max(grainScale, 0.25), 1.45))
    grain_seed = 7 if grainAnimated else 3

    st.markdown(
        f"""
<div class="grainient-live-bg" aria-hidden="true">
    <div class="grainient-blob grainient-blob-cyan"></div>
    <div class="grainient-blob grainient-blob-blue"></div>
    <div class="grainient-noise"></div>
</div>

<style>
    @keyframes grainientShift {{
        0% {{
            background-position:
                4% 8%,
                0% 50%,
                82% 18%,
                58% 86%,
                0% 44%;
        }}
        25% {{
            background-position:
                18% 16%,
                35% 48%,
                62% 30%,
                72% 74%,
                36% 48%;
        }}
        50% {{
            background-position:
                30% 10%,
                100% 52%,
                88% 38%,
                44% 68%,
                100% 56%;
        }}
        75% {{
            background-position:
                14% 22%,
                58% 50%,
                68% 14%,
                66% 92%,
                54% 50%;
        }}
        100% {{
            background-position:
                4% 8%,
                0% 50%,
                82% 18%,
                58% 86%,
                0% 44%;
        }}
    }}

    @keyframes grainientGlowFlow {{
        0% {{
            transform: translate3d(-4%, -3%, 0) rotate(0deg) scale(1.05);
            background-position: 12% 14%, 88% 22%, 52% 88%;
        }}
        50% {{
            transform: translate3d(3%, 2%, 0) rotate(1.5deg) scale(1.12);
            background-position: 22% 20%, 70% 30%, 66% 76%;
        }}
        100% {{
            transform: translate3d(-4%, -3%, 0) rotate(0deg) scale(1.05);
            background-position: 12% 14%, 88% 22%, 52% 88%;
        }}
    }}

    @keyframes grainientCyanFlow {{
        0% {{ transform: translate3d(-18%, -14%, 0) scale(0.82) rotate(0deg); }}
        35% {{ transform: translate3d(18%, -2%, 0) scale(1.16) rotate(12deg); }}
        70% {{ transform: translate3d(2%, 18%, 0) scale(0.98) rotate(-8deg); }}
        100% {{ transform: translate3d(-18%, -14%, 0) scale(0.82) rotate(0deg); }}
    }}

    @keyframes grainientBlueFlow {{
        0% {{ transform: translate3d(6%, -7%, 0) scale(1.08) rotate(0deg); }}
        45% {{ transform: translate3d(-12%, 10%, 0) scale(1.18) rotate(-8deg); }}
        100% {{ transform: translate3d(6%, -7%, 0) scale(1.08) rotate(0deg); }}
    }}

    @keyframes grainientGrain {{
        0% {{
            transform: translate3d(0, 0, 0);
        }}
        50% {{
            transform: translate3d(-1.5%, 1%, 0);
        }}
        100% {{
            transform: translate3d(0, 0, 0);
        }}
    }}

    html,
    body {{
        background: #000 !important;
    }}

    .stApp {{
        position: relative;
        isolation: isolate;
        min-height: 100vh;
        color: #f8fafc;
        overflow-x: hidden;
        background: transparent !important;
    }}

    .grainient-live-bg {{
        position: fixed;
        inset: -18vmax;
        z-index: 0;
        overflow: hidden;
        pointer-events: none;
        background:
            radial-gradient(circle at 12% 8%, color-mix(in srgb, {color1} 45%, transparent), transparent 24%),
            linear-gradient(110deg, {color2} 0%, {color2} 24%, color-mix(in srgb, {color1} 34%, {color2}) 38%, {color2} 100%),
            {color2};
        background-size: 180% 180%, 320% 320%, 100% 100%;
        animation: grainientShift {flow_duration * 0.72}s ease-in-out infinite;
        filter: saturate({saturation}) contrast({contrast});
    }}

    .grainient-blob {{
        position: absolute;
        border-radius: 999px;
        filter: blur(34px);
        opacity: 0.86;
        will-change: transform;
    }}

    .grainient-blob-cyan {{
        width: 48vmax;
        height: 42vmax;
        left: -8vmax;
        top: -10vmax;
        background: {color1};
        z-index: 2;
        opacity: 0.52;
        mix-blend-mode: screen;
        animation: grainientCyanFlow {flow_duration}s ease-in-out infinite;
    }}

    .grainient-blob-blue {{
        width: 86vmax;
        height: 72vmax;
        left: 12vmax;
        top: -16vmax;
        background: {color2};
        z-index: 1;
        opacity: 0.74;
        animation: grainientBlueFlow {flow_duration * 1.15}s ease-in-out infinite;
    }}

    .grainient-noise {{
        position: absolute;
        inset: 0;
        z-index: 3;
        pointer-events: none;
        opacity: {grain_opacity};
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 180 180' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='grain'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='{grain_frequency:.3f}' numOctaves='5' seed='{grain_seed}' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3CfeComponentTransfer%3E%3CfeFuncR type='linear' slope='1.55' intercept='-0.24'/%3E%3CfeFuncG type='linear' slope='1.55' intercept='-0.24'/%3E%3CfeFuncB type='linear' slope='1.55' intercept='-0.24'/%3E%3CfeFuncA type='table' tableValues='0 1'/%3E%3C/feComponentTransfer%3E%3C/filter%3E%3Crect width='180' height='180' filter='url(%23grain)' opacity='1'/%3E%3C/svg%3E");
        background-size: 90px 90px;
        animation: grainientGrain 1.1s steps(2, end) infinite;
        mix-blend-mode: overlay;
        filter: contrast(1.45);
    }}

    .stApp > :not(.grainient-live-bg),
    [data-testid="stAppViewContainer"],
    section[data-testid="stSidebar"] {{
        position: relative;
        z-index: 1;
    }}

    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    section[data-testid="stMain"],
    [data-testid="block-container"] {{
        background: transparent !important;
    }}

    [data-testid="stHeader"] {{
        backdrop-filter: none !important;
    }}
</style>
        """,
        unsafe_allow_html=True,
    )
