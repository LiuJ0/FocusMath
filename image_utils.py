from TextRenderer.bin.renderer import Renderer
import cv2
import numpy as np
from PIL import Image
import os
import StepPyStep
from theme import themeConfig


# Dependency of crop_transparent()
def remove_transparency(img_path, write_path, background_color=(0, 0, 0)) -> None:
    """
    img_path: str, write_path: str, background_color: int_tuple
    remove_transparency is used as a dependency of crop_transparent().
    It creates a mask as an alpha-composite and then writes it into an image.
    This effectively replaces all transparencies with the given background color, defaulted to black.
    """

    img = Image.open(img_path).convert('RGBA')
    background = Image.new('RGBA', img.size, background_color)

    alpha_composite = Image.alpha_composite(background, img)
    alpha_composite.save(write_path, 'PNG', quality=80)


# Dependency of crop_transparent()
def crop_bounding_color(path, final_path) -> None:
    """
    path: str, final_path: str
    crop_bounding_color is used as a dependency of crop_transparent.
    It creates a grayscale copy of an image, which is used to determine the bounds of the image.
    Then, it crops the image based on the bounds of the image.
    """
    # grayscale image
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    # find bounding rectangle
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]
    x, y, w, h = cv2.boundingRect(cnt)

    # crop
    crop = img[y:y+h, x:x+w]
    cv2.imwrite(final_path, crop)


def crop_transparent(img_path, final_path, background_color=(0, 0, 0)) -> None:
    """
    img_path: str, final_path: str, background_color: int_tuple
    crop_transparent can take in any rectangularly-bound image and remove the transparencies outside of the bounds.
    It replaces the transparency with black, then crops out black by bounds.
    """
    # put it together
    remove_transparency(img_path, "temp.png", background_color=background_color)
    crop_bounding_color("temp.png", final_path)
    os.remove("temp.png")


def render_text(latex, write_path, intermediate_path="temp.png", delete_intermediate=False) -> None:
    """
    latex: str, write_path: str, intermediate_path: str, delete_intermediate: bool
    render_text takes in a latex-string and a writepath to direct it where to place the rendered images.
    intermediate_path is where the individually rendered images are stored.
    delete_intermediate will cause the function to remove these intermediate images, but you may choose
    to make it False, which will keep the steps.
    """
    print("rendering")
    theme = themeConfig()
    theme.read_theme()
    render = Renderer(theme.font_math,
                      theme.font_math_italic)
    
    latex = process_latex(latex)
    intermediate_path = intermediate_path.replace(".png", "")
    print(latex)
    if '\n' in latex:
        print("newline found")
        latex = latex.split("\n")
        paths = []
        for expr in latex:
            if 'text' not in expr:
                print(f"{expr}: {latex.index(expr)}")
                render.Render(expr, 0xFFFFFFFF, 80)
                paths.append(f"{intermediate_path}{latex.index(expr)}.png")

                render.Image(
                    f"{intermediate_path}{latex.index(expr)}.png"
                )
                render.Clear()
        image_list = []
        for img in paths:
            print(img)
            image_list.append(cv2.imread(img))
        im_v_resize = vconcat_resize_min(image_list)
        cv2.imwrite(write_path, im_v_resize)
        black_to_transparent(write_path, write_path)
        if delete_intermediate:
            print("deleting...")
            for img in paths:
                os.remove(img)
    else:
        print("beginning to render...")
        render.Render(latex, 0xFFFFFFFF, 80)
        print("making image...")
        render.Image(
            write_path
        )
        render.Clear()
    print(f"done rendering, file is at {write_path}")



def vconcat_resize_min(im_list, interpolation=cv2.INTER_CUBIC) -> None:
    """
    im_list: cv2 image
    Dependency of render_text.
    Used to vertically concatenate images with widths of different numbers.
    """
    w_min = min(im.shape[1] for im in im_list)
    im_list_resize = [cv2.resize(im, (w_min, int(im.shape[0] * w_min / im.shape[1])), interpolation=interpolation)
                        for im in im_list]
    return cv2.vconcat(im_list_resize)


def process_latex(latex: str) -> str:
    """
    latex: str
    Dependency of render_text().
    """
    latex = latex.replace(' ', '')
    latex = latex.replace("(", '')
    latex = latex.replace(")", '')
    if "array" in latex:
        latex = StepPyStep.parse_tex().split_array(latex)
        array_latex = '\n'.join(latex)
        print(f"process_latex: {array_latex}")
        return array_latex

    print(f"process_latex: {latex}")

    return latex


def black_to_transparent(image, temp_writepath) -> None:
    """
    image: str, temp_writepath: str
    Dependency of render_text()
    """
    img = Image.open(image)
    img = img.convert("RGBA")
    data = img.getdata()
    new_data = []
    for datum in data:
        if datum[0] == 0 and datum[1] == 0 and datum[2] == 0:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(datum)
    img.putdata(new_data)
    img.save(temp_writepath)

