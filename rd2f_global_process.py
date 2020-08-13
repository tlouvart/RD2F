from rd2f_get_last_images import get_last_image, get_list_cam
from rd2f_settings import RD2F_root, Loaded_model
from rd2f_test_image import predict_image_class

### Using time to schedule operations every 1 min
import time

choice = 0
incrementation = 0

# Parameter put on true if we want a .txt with list of cameras
list_cam = get_list_cam(save_in_folder=True)

print("List of cameras available : \n")
for i, cam_name in enumerate(list_cam):
    print("{} : {}".format(i, cam_name))
    
choice = int(input("Enable watch on which camera  ? (Nbr expected) : "))
print("Camera chosen : {}".format(list_cam[choice]))

starttime = time.time()

while True:
    path = get_last_image(RD2F_root, incrementation, choice)
    predict_image_class(Loaded_model, path)
    incrementation += 1
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))