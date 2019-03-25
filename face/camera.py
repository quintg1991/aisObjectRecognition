from picamera import PiCamera
import errno
import os
import sys
import threading
from datetime import datetime
from time import sleep
import yaml

import face_recognition
from PIL import Image

config = yaml.safe_load(open(os.path.join(sys.path[0], "config.yml")))
image_number = 0

def create_timestampd_dir(dir):
  try:
    os.makedirs(dir)
  except OSError as e:
    if e.errno != errno.EEXIST:
      raise

def set_camera_options(camera):
  if config['resolution']:
    camera.resolution = (config['resolution']['width'], config['resolution']['height'])

  if config['iso']:
    camera.iso = config['iso']

  if config['shutter_speed']:
    camera.shutter_speed = config['shutter_speed']
    sleep(1)
    camera.exposure_mode = 'off'

  if config['white_balance']:
    camera.awb_mode = 'off'
    camera.awb_gains = (config['white_balance']['red_gain'], config['white_balance']['blue_gain'])

  if config['rotation']:
    camera.rotation = config['rotation']

  return camera

def capture_image():
  try:
    global image_number

    if(image_number < (config['total_images'] - 1)):
      thread = threading.Timer(config['interval'], capture_image).start()

    camera = PiCamera()
    set_camera_options(camera)

    camera.capture(dir + '/image{0:05d}.jpg'.format(image_number))
    camera.close()

    # here is the logical place to check the image
    check_image(dir + '/image{0:05d}.jpg'.format(image_number))

    if(image_number < (config['total_images'] - 1)):
      image_number += 1
    else:
      print('\nTime-lapse capture complete!\n')
      sys.exit()

  except KeyboardInterrupt, SystemExit:
    print '\nTime-lapse capture cancelled.\n'

def check_image(path):
  img face_recognition.load_image_file(str(path))

  face_locations = face_recognition.face_locations(img)
  print('Found: {} faces\n'.format(len(face_locations)))

  for top, right, bottom, left in face_locations:
    print("Found a face at pixel coordinates top: {}, left: {}, bottom: {}, right: {}".format(top, left, bottom, right))

    face_data_array = img[top:bottom, left:right]
    face_image = Image.fromarray(face_data_array)

    # face_img_path = pathlib.Path('{}{}{}{}-face.jpg'.format(top, right, bottom, left))
    # face_img_path.touch()
    # face_image.save(str(face_img_path.resolve()))

dir = os.path.join(sys.path[0], 'series-' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
create_timestampd_dir(dir)

capture_image()

if(config['create_git']):
  print '\nCreating animated gif.\n'
  os.system('convert -delay 10 -loop 0 ' + dir + '/image*.jpg ' + dir + '-timelapse.gif')

if(config['create_video']):
  print '\nCreating video.\n'
  os.system('avconv -framerate 20 -i ' + dir + '/image%05d.jpg -vf format=yuv420p ' + dir + '/timelapse.mp4')


# camera = PiCamera()
# camera.capture('test.jpg')
