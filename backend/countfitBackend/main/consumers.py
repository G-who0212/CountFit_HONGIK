import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import base64
import os, sys
import cv2
import numpy as np
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))))
from AI.demo.get_count import predict_image

# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()  # No need for room groups in this scenario

#         # Send a welcome message (optional)
#         self.send(text_data=json.dumps({
#             'type': 'connection_established',
#             'message': 'You are now connected!'
#         }))

#     def receive(self, text_data):
#         PUSH_UP = 0
#         PULL_UP = 1
#         SQUAT = 2

#         text_data_json = json.loads(text_data)
#         if text_data_json['type'] == 'video_frame':
            
#             if text_data_json['data']:
#                 # 1. base64 디코딩
#                 frame_data = base64.b64decode(text_data_json['data'])

#                 # 2. numpy 배열로 변환
#                 np_arr = np.frombuffer(frame_data, np.uint8)

#                 # 3. OpenCV 이미지로 변환
#                 image_bgr = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

#                 # Optional: 이미지가 제대로 변환되었는지 확인 (디버깅 용)
#                 # print('Received frame:', image_bgr.shape)

#                 # 4. predict_image 함수에 전달
#                 return image_bgr

#             # Process frame data here (optional)

#             # Broadcast the frame to all connected clients (optional)
#             # async_to_sync(self.channel_layer.group_send)(
#             #     self.room_group_name,  # Remove if not using groups
#             #     {
#             #         'type': 'broadcast_video_frame',
#             #         'frame_data': frame_data
#             #     }
#             # )

#     def disconnect(self, close_code):
#         pass



class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()  # 연결 수락
        PUSH_UP = 0
        PULL_UP = 1
        SQUAT = 2
        # 초기 변수 설정

        self.chk = 0
        self.count = 0
        self.exercise_type = SQUAT  # 변경 가능

        # 클라이언트에 연결 확인 메시지 전송
        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'You are now connected!'
        }))

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json['type'] == 'video_frame':
            if text_data_json['data']:
                # base64 디코딩
                frame_data = base64.b64decode(text_data_json['data'])
                # numpy 배열로 변환
                np_arr = np.frombuffer(frame_data, np.uint8)
                # OpenCV 이미지로 변환
                image_bgr = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

                # predict_image 함수에 이미지 전달 및 운동 횟수 카운트
                count_chk, self.chk = predict_image(image_bgr, self.chk, self.exercise_type)
                if count_chk:
                    self.count += 1
                    print(f"count {self.count}")
                    # 클라이언트에 현재 카운트 전송
                    self.send(text_data=json.dumps({
                        'type': 'count_update',
                        'count': self.count
                    }))

    def disconnect(self, close_code):
        pass