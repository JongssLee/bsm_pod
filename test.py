import cv2
import numpy as np
import asyncio
from PIL import Image, ImageDraw, ImageFont

async def async_add_text_box(input_path):
    return await asyncio.to_thread(add_text_box, input_path)

def add_text_box(input_path):
    # 이미지 로드
    img = cv2.imread(input_path)
    
    # 이미지 크기 확인 및 조정
    if img.shape[:2] != (720, 1280):
        img = cv2.resize(img, (1280, 720))
    
    # 텍스트 설정
    text = "들으러 가기"
    font_path = "NanumGothic.ttf"  # 사용할 폰트 파일 경로
    font_size = 40
    font = ImageFont.truetype(font_path, font_size)
    text_color = (0, 0, 255)  # 파랑색 (RGB 형식)
    
    # PIL 이미지를 사용하여 텍스트 추가
    pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    
    # 텍스트 크기 계산
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # 박스 설정
    padding = 20
    box_width = text_width + padding * 2
    box_height = text_height + padding * 2
    
    # 박스 위치 계산 (이미지 중앙)
    box_x = (pil_img.width - box_width) // 2
    box_y = (pil_img.height - box_height) // 2
    
    # 박스 그리기
    draw.rounded_rectangle(
        [box_x, box_y, box_x + box_width, box_y + box_height],
        fill=(255, 255, 255),
        radius=20
    )
    
    # 텍스트 위치 계산
    text_x = box_x + (box_width - text_width) // 2
    text_y = box_y + (box_height - text_height) // 2
    
    # 텍스트 그리기
    draw.text((text_x, text_y), text, font=font, fill=text_color)
    
    # OpenCV 이미지로 변환
    img_with_text = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    
    # 결과 이미지 저장
    output_path = input_path.replace('.jpg', '_output.jpg')
    cv2.imwrite(output_path, img_with_text)
    print(f"Saved to {output_path}")
    return output_path

# 함수 사용 예
# asyncio.run(async_add_text_box('input_image.jpg'))
