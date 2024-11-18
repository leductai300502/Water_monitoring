from PIL import Image
image = Image.open('off1.png')
new_image = image.resize((100, 100))
new_image.save('off.png')