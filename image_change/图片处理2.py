from PIL import Image
import os

files = sorted(
    f for f in os.listdir("frames")
    if f.startswith("frame_") and f.endswith(".png")
)

frames = [
    Image.open(os.path.join("frames", f)).convert("RGB")
    for f in files
]

print("读取到", len(frames), "帧")

# 正向 + 反向
animation = frames + frames[-2:0:-1]

animation[0].save(
    "shake2.gif",
    save_all=True,
    append_images=animation[1:],
    duration=80,
    loop=0,
    optimize=False,
    disposal=1
)

print("GIF生成")