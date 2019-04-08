"""Tools for adding a shadow effect to pygame images.

Exports make_shadow, make_shadow_opaque, place_shadow, add_shadow.

pygame.display.set_mode() must be called before this module's functions
can be used.

shadows.py module from https://www.pygame.org/wiki/ShadowEffects
Author unknown.
"""

import pygame
_arraytype = pygame.surfarray.get_arraytype()
if _arraytype == 'numeric':
    from Numeric import UInt8 as uint8, minimum, array
    from Numeric import Float32 as float32, Int32 as int32
elif _arraytype == 'numpy':
    from numpy import uint8, minimum, array, float32, int32
else:
    raise TypeError("Unrecognized surfarray array type %s" % _arraytype)


def make_shadow(image, ambience=None):
    """Return a shadow representation of image for a given ambient lighting.

    image - foreground image.
    ambience (optional) - 0.0 to 1.0: Ambient light ratio. 0.0 gives a
                          totally black shadow while 1.0 gives no shadow.
                          Defaults to 0.0 .
    """
    if ambience is None:
        ambience = 0.0
    elif not (0.0 <= ambience <= 1.0):
        raise ValueError("ambience must be between 0.0 and 1.0 inclusive")
    if image.get_masks()[3] != 0:
        image_alpha = pygame.surfarray.pixels_alpha(image)
        if ambience > 0.0:
            shadow_alpha = (image_alpha *
                            (1.0 - ambience)).astype(uint8)
        else:
            shadow_alpha = image_alpha
    elif image.get_colorkey() is not None:
        image_alpha = pygame.surfarray.array_colorkey(image)
        image.unlock()
        image.unlock()  # pygame 1.7 bug (fixed in 1.8).
        surface_alpha = image.get_alpha()
        if surface_alpha is not None:
            # Do what array_colorkey should have done: use surface alpha!
            minimum(image_alpha, surface_alpha, image_alpha)
        if ambience > 0.0:
            shadow_alpha = (image_alpha *
                            (1.0 - ambience)).astype(uint8)
        else:
            shadow_alpha = image_alpha
    else:
        image_alpha = image.get_alpha()
        if image_alpha is None:
            image_alpha = 255
        shadow_alpha = int(image_alpha * (1.0 - ambience))
    shadow = image.convert_alpha()
    shading = pygame.Surface(shadow.get_size(), pygame.SRCALPHA, 32)
    pygame.surfarray.pixels_alpha(shading)[...] = image_alpha
    shadow.blit(shading, (0, 0))
    pygame.surfarray.pixels_alpha(shadow)[...] = shadow_alpha
    return shadow


def make_shadow_opaque(size, ambience=None, pixel_size=None):
    """Return a retangular shadow for the given ambient lighting.

    size - (width, height): shadow dimensions.
    ambience (optional) - 0.0 to 1.0: Ambient light ratio. 0.0 gives a
                          totally black shadow while 1.0 gives no shadow.
                          Defaults to 0.0 .
    pixel_size (optional) - bits per pixel - defaults to screen value.

    This version is provided for performance.
    """
    if ambience is None:
        ambience = 0.0
    if pixel_size is None:
        rest = ()
    else:
        rest = (pixel_size,)
    shadow = pygame.Surface(size, 0, rest)
    shadow.set_alpha(255 * (1.0 - ambience))
    return shadow


def place_shadow(image, shadow, shadow_offset):
    """Return a surface that combines the image and shadow.

    image - foreground image.
    shadow - image shadow.
    shadow_offset - (dx, dy) amount, in pixel, to shift
                    shadow center relative to image center.
    """
    image_rect = image.get_rect()
    shadow_rect = shadow.get_rect()
    shadow_rect.center = image_rect.center
    shadow_rect.move_ip(shadow_offset)
    rect = image_rect.union(shadow_rect)
    result = pygame.Surface(rect.size, pygame.SRCALPHA, 32)
    result.blit(shadow, (shadow_rect.left - rect.left,
                         shadow_rect.top - rect.top))
    result.blit(image, (image_rect.left - rect.left,
                        image_rect.top - rect.top))
    return result


def add_shadow(image, shadow_offset, shadow_scale=None, ambience=None):
    """Return a copy of image with a shadow added.

    image - a surface with or without alpha or colorkey.
    shadow_offset - (dx, dy) amount, in pixel, to shift
                    shadow center relative to image center.
    shadow_scale (optional) - amount by which to scale the shadow.
                              defaults to 1.0 (no scaling).
    ambience (optional) - 0.0 to 1.0: Ambient light ratio. 0.0 gives a
                          totally black shadow while 1.0 gives no shadow.
                          Defaults to 0.0 .
    """
    if (image.get_flags() & pygame.SRCALPHA or
            image.get_colorkey() is not None):
        shadow = make_shadow(image, ambience)
        if shadow_scale is not None:
            a = array(shadow.get_size(), float32)
            size = (a * shadow_scale).astype(int32)
            shadow = pygame.transform.smoothscale(shadow, size)
    else:
        size = (array(image.get_size(), float32) * shadow_scale).astype(int32)
        if shadow_scale is None:
            shadow_scale = 1.0
        shadow = make_shadow_opaque(size, ambience, image.get_bitsize())
    return place_shadow(image, shadow, shadow_offset)


__all__ = ['make_shadow', 'make_shadow_opaque', 'place_shadow', 'add_shadow']
