import os
import requests
import base64
from dotenv import load_dotenv
load_dotenv()

KEY = os.getenv("STABILITY_KEY")


def image_to_image(
        prompt: str,
        input_image_path: str,
        output_image_path: str = r"D:\Code 2025\TweenCraft\2D AI Aniamtion App\Exports\refined_output.png",
        strength: float = 0.3,
        steps: int = 30 ):

    with open(input_image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    response = requests.post(
        "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
        headers={
            "Authorization": f"Bearer {KEY}",
            "Content-Type": "application/json"
        },
        json={
            "text_prompts": [{"text": prompt}],
            "init_image": image_data,
            "init_image_mode": "IMAGE_STRENGTH",
            "strength": strength,
            "steps": steps,
            "samples": 1
        }
    )   
    if response.status_code == 200:
        image_data = response.json()["artifacts"][0]["base64"]
        with open(output_image_path, "wb") as f:
            f.write(base64.b64decode(image_data))
        print(f"✅ Image saved to {output_image_path}")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")

#Run

image_to_image(
    prompt="clean up this sketch, keep the same character and pose, smooth lines, 2D animation style, increased resolution, line art" '2d animation' 'sketch' 'line art' 'clean up' 'single character' 'same pose',
    input_image_path=r"D:\Code 2025\TweenCraft\2D AI Aniamtion App\Exports\sword.png",
    output_image_path="output.png",
    strength=0.3,
)