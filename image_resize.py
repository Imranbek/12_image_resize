import argparse
import sys

import PIL
from PIL import Image


def main():
    parameters = parse_parameters()
    path = parameters['path']
    output_path = parameters['output']
    width = parameters['width']
    height = parameters['height']
    scale = parameters['scale']

    try:
        image = Image.open(path)
    except PIL.UnidentifiedImageError:
        raise Exception('There is something wrong with your image. '
                        'May be it is not an image at all.'
                        'Please restart the script with another one.')

    original_size = image.size

    size_parameters_key = (bool(scale), bool(width), bool(height))
    keys_functions = {
        (True, True, False): wrong_key_combination_exception,
        (True, False, True): wrong_key_combination_exception,
        (True, True, True): wrong_key_combination_exception,
        (False, False, False): no_positive_parameters_exception,
        (True, False, False): count_image_size_by_scaling,
        (False, True, False): count_image_size_by_width,
        (False, False, True): count_image_size_by_height,
        (False, True, True): count_image_size_by_width_and_height
    }

    output_size = keys_functions[size_parameters_key](original_size=original_size,
                                                      scale=scale,
                                                      new_height=height,
                                                      new_width=width)

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


def wrong_key_combination_exception(original_size: tuple,
                                    scale: tuple,
                                    new_height: int,
                                    new_width: int):
    raise Exception('I can not resize your image with '
                    'such combination of parameters. '
                    'Please restart the script either '
                    'with just the scale parameter '
                    'or with one or both of the width and height parameters.')


def no_positive_parameters_exception(original_size: tuple,
                                     scale: tuple,
                                     new_height: int,
                                     new_width: int):
    raise Exception('I need some positive parameters to work with. '
                    'Please restart the script with right parameters.')


def count_image_size_by_scaling(original_size: tuple,
                                scale: tuple,
                                new_height: int,
                                new_width: int):
    output_size = tuple([scale * x for x in original_size])

    return output_size


def count_image_size_by_width_and_height(original_size: tuple,
                                         scale: tuple,
                                         new_height: int,
                                         new_width: int):
    output_size = (new_width, new_height)
    original_size_proportions = get_proportion(size=original_size)
    output_size_proportions = get_proportion(size=output_size)
    if output_size_proportions != original_size_proportions:
        print('Preparation: With changing size by such parameters '
              'of width and height will change the image proportions')

    return output_size


def count_image_size_by_width(original_size: tuple,
                              scale: tuple,
                              new_height: int,
                              new_width: int):
    proportion = get_proportion(size=original_size)
    new_height = new_width / proportion
    output_size = (new_width, new_height)

    return output_size


def count_image_size_by_height(original_size: tuple,
                               scale: tuple,
                               new_height: int,
                               new_width: int):
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
