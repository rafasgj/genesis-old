"""Algoritms for collision detection."""


class Collider:
    """Encapsulates all collision detect methods."""

    class __Algo:
        @classmethod
        def ellipse_rect(cls, ellipse, rect):
            """Verify colision between an ellipse and a rectangle."""
            def test(a, b):
                d = (a - h) ** 2 / (rx * rx) + (b - k) ** 2 / (ry * ry)
                return d <= 0.9
            h, k, rx, ry = ellipse
            x, y, width, height = rect
            p1 = test(x, y)
            p2 = test(x, y + height)
            p3 = test(x + width, y)
            p4 = test(x + width, y + height)
            return p1 or p2 or p3 or p4

        @classmethod
        def circle_rect(cls, circle, rect):
            """Verify colision between an ellipse and a rectangle."""
            x, y, w, h = rect
            cx, cy, r = circle
            r *= r
            for a, b in [(x, y), (x + w, y), (x, y + h), (x + w, y + h)]:
                dx = (x - cx) ** 2
                dy = (y - cy) ** 2
                if (dx + dy) < r:
                    return True
            return False

        @classmethod
        def circle_circle(cls, c1, c2):
            """Verify colision between an ellipse and a rectangle."""
            cx1, cy1, r1 = c1
            cx2, cy2, r2 = c2
            cx = (cx1 - cx2) ** 2
            cy = (cy1 - cy2) ** 2
            r = (r1 + r2) ** 2
            return (cx + cy) < r

        @classmethod
        def rect_rect(cls, r1, r2):
            """Verify colision between an ellipse and a rectangle."""
            x1, y1, w1, h1 = r1
            x2, y2, w2, h2 = r2
            if x1 > x2 + w2 or x1 + w1 < x2:
                return False
            if y1 > y2 + h2 or y1 + h1 < y2:
                return False
            return True

        @classmethod
        def invert(cls, fn):
            def do_it(a, b):
                return fn(b, a)
            return do_it

    BOX = "box"
    ELLIPSE = "ellipse"
    RECT = "rect"
    CIRCLE = "circle"

    __functions = {
        "ellipse_rect": __Algo.ellipse_rect,
        "rect_ellipse": __Algo.invert(__Algo.ellipse_rect),
        # "ellipse_circle": __Algo.ellipse_circle,
        # "circle_ellipse": __Algo.invert(__Algo.ellipse_circle),
        "circle_rect": __Algo.circle_rect,
        "rect_circle": __Algo.invert(__Algo.circle_rect),
        "rect_rect": __Algo.rect_rect,
        "circle_circle": __Algo.circle_circle,
        "ellipse_ellipse": __Algo.circle_circle,
    }

    def __init__(self, bounding_shape):
        """Initialize the collision detection algorithms."""
        self.__bounding_shape = bounding_shape

    @property
    def bounding_shape(self):
        """Retrieve the object bounding shape."""
        return self.__bounding_shape

    def did_collide(self, object):
        """Return true if collides with object."""
        shape = self.bounding_shape + "_" + object.bounding_shape
        fn = Collider.__functions.get(shape, lambda a, b: False)
        return fn(self.bounds, object.bounds)

    def collide_with(self, object):
        """Handle collision event."""
        raise NotImplementedError("Subclasses must implement collide_with().")
