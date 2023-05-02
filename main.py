# Get the absolute path of the current working directory
import os
import cv2
import argparse
import cairosvg
from PIL import Image

abs_path = os.path.abspath(os.getcwd())
print("The current working directory is " + f'"{abs_path}"')

parser = argparse.ArgumentParser()
parser.add_argument("--target_file", type=str, default="none",
                    help="target image file, located in <target_images>")

args = parser.parse_args()

if (args.target_file == "none"):
    print("Please specify the target file")
    exit(0)

vedio = args.target_file
target = f"{abs_path}/input/"
cap = cv2.VideoCapture(target + vedio)
print("read file: ", target + vedio)

def save_image(image, path, m):
    # Save image
    cv2.imwrite(path + str(m) + '.jpg', image)
    # print('Saved frame%d.jpg' % m)

success, frame = cap.read()
i = 0
# set the rate to save frame
frame_rate = 10
count = 0
while success:
    i += 1
    if i % frame_rate == 0:
        count += 1
        # Save frame as JPG file
        save_image(frame, f"./CLIPasso/target_images/temp_frames/", count)

    # Read next frame
    success, frame = cap.read()
print(f'Successfully read {count} frames')

# Run CLIPasso to process frames
os.system(f"{abs_path}/CLIPasso/bash.sh '{abs_path}/CLIPasso'")

# Convert the best 'svg' outputs to 'png'
os.system("pip install cairosvg")

for i in range(1, count+1):
    path = f'{abs_path}/CLIPasso/output_sketches/' + str(i) + '/'
    try:
        cairosvg.svg2png(file_obj=open(path + str(i) + '_20strokes_seed' + '0_best.svg'), write_to=path+'best_iter.png')
    except:
        try:
            cairosvg.svg2png(file_obj=open(path + str(i) + '_20strokes_seed' + '1000_best.svg'), write_to=path+'best_iter.png')
        except:
            cairosvg.svg2png(file_obj=open(path + str(i) + '_20strokes_seed' + '2000_best.svg'), write_to=path+'best_iter.png')

# Generate the first vedio
# create a video writer object, avi uses *'MJPG' codec
fourcc = cv2.VideoWriter(f'{abs_path}/output/output_best.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 10, (224,224))

# Convert each png into jpg first then generate the vedio
i = 1
while i <= count:
    path = f'{abs_path}/CLIPasso/output_sketches/' + str(i) + '/'
    img_png = Image.open(path + 'best_iter.png')
    bg = Image.new("RGB", img_png.size, (255,255,255))
    bg.paste(img_png,img_png)
    bg.save(path + "best_iter.jpg")
    # cv2.imwrite(path + 'best_iter.jpg', img_png)
    img = cv2.imread(path + 'best_iter.jpg')
    img = cv2.resize(img, (224,224))
    count = 0
    # write the fps of each frame
    while count < 1:
        fourcc.write(img)
        count += 1
    i += 1
    
fourcc.release()

# Frame interpolation
os.system("cd ./ECCV2022-RIFE && python inference_video.py --exp=5 --video=./output/output_best.mp4 --scale=2")
# clear temporary files
os.system(f"rm -rf {abs_path}/CLIPasso/target_images/temp_frames/")
os.system(f"rm -rf {abs_path}/CLIPasso/output_sketches/")
os.system(f"mkdir {abs_path}/CLIPasso/output_sketches/")
os.system(f"mkdir {abs_path}/CLIPasso/target_images/temp_frames/")