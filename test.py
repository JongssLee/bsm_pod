import cv2
import numpy as np
import asyncio

async def async_add_text_box(input_path):
    await asyncio.to_thread(add_text_box, input_path)


def add_text_box(input_path):
    # 이미지 로드
    img = cv2.imread(input_path)
    
    # 이미지 크기 확인 및 조정
    if img.shape[:2] != (720, 1280):
        img = cv2.resize(img, (1280, 720))
    
    # 텍스트 설정
    text = "Link"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 2
    text_color = (0, 255, 0)  # 형광초록 (BGR 형식)
    
    # 텍스트 크기 계산
    text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
    
    # 박스 설정
    padding = 20
    box_width = text_size[0] + padding * 2
    box_height = text_size[1] + padding * 2
    
    # 박스 위치 계산 (이미지 중앙)
    box_x = (img.shape[1] - box_width) // 2
    box_y = (img.shape[0] - box_height) // 2
    
    # 둥근 모서리의 사각형 그리기
    overlay = img.copy()
    sub_img = overlay[box_y:box_y+box_height, box_x:box_x+box_width]
    white_rect = np.ones(sub_img.shape, dtype=np.uint8) * 255
    res = cv2.addWeighted(sub_img, 0.5, white_rect, 0.5, 1.0)
    
    # 둥근 모서리 마스크 생성
    mask = np.zeros(sub_img.shape[:2], np.uint8)
    cv2.rectangle(mask, (0, 0), (box_width, box_height), 255, -1)
    mask = cv2.GaussianBlur(mask, (11, 11), 0)
    
    # 마스크를 사용하여 둥근 모서리 적용
    img_masked = cv2.bitwise_and(res, res, mask=mask)
    img[box_y:box_y+box_height, box_x:box_x+box_width] = img_masked
    
    # 텍스트 위치 계산
    text_x = box_x + (box_width - text_size[0]) // 2
    text_y = box_y + (box_height + text_size[1]) // 2
    
    # 텍스트 그리기
    cv2.putText(img, text, (text_x, text_y), font, font_scale, text_color, font_thickness)
    output_path = input_path.replace('.jpg', '_output.jpg')
    # 결과 이미지 저장
    cv2.imwrite(output_path, img)
    return output_path

# 함수 사용 예
