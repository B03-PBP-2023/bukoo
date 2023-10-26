from dotenv import load_dotenv

load_dotenv()

import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config(secure=True)

def upload_image(image, name):
  try:
    public_id = f'bukoo/book_cover/{name}'
    cloudinary.uploader.upload(image, public_id=public_id, resource_type="image")
    return cloudinary.CloudinaryImage(public_id).url
  except:
    return None


def delete_image(name):
  try:
    public_id = f'bukoo/book_cover/{name}'
    cloudinary.uploader.destroy(public_id)
  except:
    pass

def edit_image(image, name, last_url):
  if last_url == None:
    return upload_image(image, name)
  last_name = last_url.split('bukoo/book_cover/')[-1]
  if last_name != name:
    delete_image(last_name)
  return upload_image(image, name)


def get_image_name(id, book_title):
  return f'{id}.{book_title.replace(" ", "_")}'