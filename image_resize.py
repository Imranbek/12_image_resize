import argparse
import math

import PIL
from PIL import Image


def main():
    parameters = parse_parameters()

    path = parameters.path
    output_path = parameters.output
    width = parameters.width
    height = parameters.height
    scale = parameters.scale

    for parameter in [width, height, scale]:
        assert check_value_none_or_positive_number(parameter), \
            'One ore more parameters are negative. ' \
            'Please restart script with positive numeric parameters.'

    image = open_image_by_path(path=path)
    original_size = image.size

    size_parameters_key = (bool(scale), bool(width), bool(height))
    keys_functions = {
        (True, True, False): wrong_key_combination_exception,
        (True, False, True): wrong_key_combination_exception,
        (True, True, True): wrong_key_combination_exception,
        (False, False, False): no_parameters_exception,
        (True, False, False): count_image_size_by_scaling,
        (False, True, False): count_image_size_by_width,
        (False, False, True): count_image_size_by_height,
        (False, True, True): count_image_size_by_width_and_height,
    }

    output_size = keys_functions[size_parameters_key](
        original_size=original_size,
        scale=scale,
        new_height=height,
        new_width=width,
    )

    new_image = change_image_size(
        image=image,
        output_size=output_size,
    )

    new_file_name = get_new_image_name_with_size(
        image=image,
        size=output_size)

    if output_path:
        output_path_name = output_path + new_file_name
    else:
        old_file_name = image.filename
        output_path_name = path.replace(
            old_file_name,
            new_file_name,
        )

    save_image_with_path_name(
        image=new_image,
        output_path_name=output_path_name,
    )


def change_image_size(image: Image,
                      output_size: tuple,
                      ):
    new_image = image.resize(output_size)

    return new_image


def get_new_image_name_with_size(image: Image,
                                 size: tuple,
                                 ):
    image_name = image.filename
    new_image_name = image_name.replace('.', '_{}x{}.'.format(size[0],
                                                              size[1]))
    return new_image_name


def save_image_with_path_name(image: Image,
                              output_path_name: str):
    image.save(output_path_name)  # saving image
    print('Image was successfully resized. '
          'New image name {}'.format(output_path_name))


def open_image_by_path(path: str):
    try:
        image = Image.open(path)
        return image
    except PIL.UnidentifiedImageError:
        raise Exception('There is something wrong with your image. '
                        'May be it is not an image at all.'
                        'Please restart the script with another one.')


def wrong_key_combination_exception(original_size: tuple,
                                    scale: tuple,
                                    new_height: int,
                                    new_width: int):
    raise Exception('I can not resize your image with '
                    'such combination of parameters. '
                    'Please restart the script either '
                    'with just the scale parameter '
                    'or with one or both of the width and height parameters.')


def no_parameters_exception(original_size: tuple,
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
    compare_proportions(
        size_1=original_size,
        size_2=output_size,
    )

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


def compare_proportions(size_1, size_2):
    size_1_proportions = get_proportion(size=size_1)
    size_2_proportions = get_proportion(size=size_2)
    if not math.isclose(size_1_proportions, size_2_proportions):
        print('Preparation: With changing size by such parameters '
              'of width and height will change the image proportions.')


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

    parameters = parser.parse_args()
    return parameters


def check_value_none_or_positive_number(parameter_value):
    if parameter_value is None:
        return True

    return parameter_value > 0


if __name__ == '__main__':
    main()
