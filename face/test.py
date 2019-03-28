import pathlib
import face_recognition
from PIL import Image

if __name__ == '__main__':
  src_img_path = (pathlib.Path('.') / 'series-2019-03-28_14-04-35' / 'image00000.jpg').resolve()
  img = face_recognition.load_image_file(str(src_img_path))

  face_locations = face_recognition.face_locations(img)
  print('Found: {} faces\n'.format(len(face_locations)))
