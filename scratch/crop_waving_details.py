from PIL import Image

for i in [2, 3, 4, 5]:
    p = Image.open(f'scratch/waving_panels/panel_{i}.png')
    # Wing is roughly x in [220, 341], y in [0, 240]
    wing_crop = p.crop((220, 0, 341, 240))
    wing_crop.save(f'scratch/waving_panels/wing_p{i}.png')

# Happy eyes in panel 5: x in [100, 240], y in [70, 140]
p5 = Image.open('scratch/waving_panels/panel_5.png')
eyes_crop = p5.crop((100, 70, 240, 140))
eyes_crop.save('scratch/waving_panels/happy_eyes.png')
print("Cropped wing details and happy eyes.")
