from PIL import Image
import os

input_file = "D:/PRC_long_march_anime_military.png"

img = Image.open(input_file)

print("原图尺寸：", img.size)

FRAME_WIDTH = 156
FRAME_HEIGHT = img.height

FRAME_COUNT = img.width // FRAME_WIDTH

print("预计帧数：", FRAME_COUNT)
print("每帧尺寸：", FRAME_WIDTH, "×", FRAME_HEIGHT)

os.makedirs("frames", exist_ok=True)

for i in range(FRAME_COUNT):

    left = i * FRAME_WIDTH
    right = left + FRAME_WIDTH

    frame = img.crop(
        (left, 0, right, FRAME_HEIGHT)
    )

    filename = f"frames/frame_{i+1:03d}.png"

    frame.save(filename)

    print(
        filename,
        "->",
        f"x={left}~{right}"
    )

print("切帧完成")
print("剩余像素：", img.width - FRAME_COUNT * FRAME_WIDTH)