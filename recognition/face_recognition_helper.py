import face_recognition
import numpy as np
import os
import random
import string
import glob


def generateId(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits)
                          for i in range(length)))
    return result_str


def recognize(file_path, name):
    image = face_recognition.load_image_file(file_path)
    image_encoding = face_recognition.face_encodings(image)[0]
    with open(os.path.join("encoding", "{}.{}.encoding".format(generateId(5), name)), 'w') as encoding_file:
        np.savetxt(encoding_file, image_encoding)
        encoding_file.close()
    return image_encoding


def compare(file_path):
    image = face_recognition.load_image_file(file_path)
    image_encoding = face_recognition.face_encodings(image)[0]
    encoding_files = [file for file in glob.glob(
        os.path.join("encoding", "*.encoding"))]
    encoding_files = [{"data": np.loadtxt(file), "file_path": file, "name": file.split('.')[1]}
                      for file in encoding_files]
    for encoding_file in encoding_files:
        results = face_recognition.compare_faces(
            [encoding_file["data"]], image_encoding)
        if results[0] == True:
            return encoding_file["name"]

    return None
