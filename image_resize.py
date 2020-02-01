import argparse
import sys

from PIL import Image


def main():
    parameters = parse_parameters()
    path = parameters['path']
    output_path = parameters['output']
    width = parameters['width']
    height = parameters['height']
    scale = parameters['scale']

    image = Image.open(path)
    original_size = image.size

    size_parameters_key = (bool(scale), bool(width), bool(height))
    wrong_combination_keys = [
        (True, True, False),  # combination of scale and width
        (True, False, True),  # combination of scale and height
        (True, True, True)  # combination of scale, width and height
    ]

    if size_parameters_key == (False, False, False):
        raise Exception('I need some positive parameters to work with. '
                        'Please restart script with right parameters.')

    elif size_parameters_key in wrong_combination_keys:
        raise Exception('I can not resize your image with '
                        'such combination of parameters. '
                        'Please restart the script either '
                        'with just the scale parameter '
                        'or with one or both of the width and height parameters.')

    elif size_parameters_key == (True, False, False):
        output_size = count_image_size_by_scaling(original_size=original_size,
                                                  scale=scale)
    elif size_parameters_key == (False, True, False):
        output_size = count_image_size_by_width(original_size=original_size,
                                                new_width=width)
    elif size_parameters_key == (False, False, True):
        output_size = count_image_size_by_height(original_size=original_size,
                                                 new_height=height)
    elif size_parameters_key == (False, True, True):
        output_size = (height, width)
        original_size_proportions = get_proportion(size=original_size)
        output_size_proportions = get_proportion(size=output_size)
        if output_size_proportions != original_size_proportions:
            print('Preparation: With changing size by such parameters '
                  'of width and height will change the image proportions')

    resize_and_save_image(image=image,
                          output_size=output_size,
                          original_path=path,
                          output_path=output_path)


def resize_and_save_image(image: Image,
                          output_size: tuple,
                          original_path: str,
                          output_path):
    image_name = image.filename
    image.thumbnail(output_size)  # resizing image
    new_image_size = image.size

    new_image_name = image_name.replace('.', '_{}x{}.'.format(new_image_size[0],
                                                              new_image_size[1]))
    if output_path:
        output_path_name = output_path + image_name
    else:
        output_path_name = original_path.replace(image_name, new_image_name)

    image.save(output_path_name)  # saving image
    print('Image was successfully resized. New image name {}'.format(
        new_image_name))


def count_image_size_by_scaling(original_size: tuple, scale: int):
    output_size = tuple([scale * x for x in original_size])

    return output_size


def count_image_size_by_width(original_size: tuple, new_width: int):
    proportion = get_proportion(size=original_size)
    new_height = new_width / proportion
    output_size = (new_width, new_height)

    return output_size


def count_image_size_by_height(original_size: tuple, new_height: int):
    proportion = get_proportion(size=original_size)
    new_width = round(new_height * proportion)
    output_size = (new_width, new_height)

    return output_size


def get_proportion(size: tuple):
    proportion = size[0] / size[1]
    return proportion


def parse_parameters():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('-s', '--scale', type=float)
    parser.add_argument('-wd', '--width', type=int)
    parser.add_argument('-hg', '--height', type=int)
    parser.add_argument('-o', '--output', type=str)

    parameters = vars(parser.parse_args(sys.argv[1:]))
    return parameters


if __name__ == '__main__':
    main()
