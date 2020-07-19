
import face_recognition,cv2,numpy as np

"""
构建videocaptrue对象
"""
video_capture =  cv2.VideoCapture(0)

obama_image = face_recognition.load_image_file("zhangyuqi.jpg")
obama_image1 = face_recognition.load_image_file("liyitong.jpg")
obama_image2 = face_recognition.load_image_file("caihongbo.jpg")
obama_image3 = face_recognition.load_image_file("wuxi.jpg")
obama_image4 = face_recognition.load_image_file("jinyida.jpg")
obama_image5 = face_recognition.load_image_file("sunshiyin.jpg")
# print('Files Loaded')
"""
获取每个图像文件中每个面部的面部编码
由于每个图像中可能有多个人脸，所以返回一个编码列表。
但是事先知道每个图像只有一个人脸，每个图像中的第一个编码，取索引0。
"""
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
obama_face_encoding1 = face_recognition.face_encodings(obama_image1)[0]
obama_face_encoding2 = face_recognition.face_encodings(obama_image2)[0]
obama_face_encoding3 = face_recognition.face_encodings(obama_image3)[0]
obama_face_encoding4 = face_recognition.face_encodings(obama_image4)[0]
obama_face_encoding5 = face_recognition.face_encodings(obama_image5)[0]
# obama_face_encoding = face_recognition.face_encodings(obama_image)
# obama_face_encoding1 = face_recognition.face_encodings(obama_image1)

print(obama_face_encoding)
print(obama_face_encoding1)
print(obama_face_encoding2)
known_face_encodings = [
    obama_face_encoding,
    obama_face_encoding1,
    obama_face_encoding2,
    obama_face_encoding3,
    obama_face_encoding4,
    obama_face_encoding5

]
known_face_names = [
    "zhangyuqi",
    "liyitong",
    "caihongbo",
    "wuxi",
    "jinyida",
    "sunshiyin"

]

# print('Names loaded')

# Initialize some variables
# 初始化一些变量
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    #抓取每一帧视频
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding,tolerance=0.4)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()