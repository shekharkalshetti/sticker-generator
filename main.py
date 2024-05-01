from diffusion import generate_image_from_prompt
from sticker_utils import create_sticker, show_sticker_from_image


def main():
    prompt = input("Enter prompt: ")
    image = generate_image_from_prompt(prompt)
    sticker = create_sticker(image)
    show_sticker_from_image(sticker)


if __name__ == "__main__":
    main()
