"""Algoritms for collision detection."""

from math import copysign


def sign(x):
    """Return -1 if x is negative, 1 is it is positive."""
    return copysign(1, x)


class Collider:
    """Encapsulates all collision detect methods."""

    class __Algo:
        @staticmethod
        def __distance_to_ellipse(ellipse, point):
            h, k, rx, ry = ellipse
            rx //= 2
            ry //= 2
            a, b = point
            return (a - h) ** 2 / (rx * rx) + (b - k) ** 2 / (ry * ry)

        @classmethod
        def ellipse_point(cls, ellipse, point):
            """Verify colision between an ellipse and a rectangle."""
            return cls.__distance_to_ellipse(ellipse, point) <= 0.9

        @classmethod
        def ellipse_circle(cls, ellipse, circle):
            """Verify colision between an ellipse and a rectangle."""
            x, y, r = circle
            return cls.__distance_to_ellipse(ellipse, (x, y)) <= 1.95 * r

        @classmethod
        def ellipse_rect(cls, ellipse, rect):
            """Verify colision between an ellipse and a rectangle."""
            x, y, width, height = rect
            for p in ((x, y), (x, y + height),
                      (x + width, y), (x + width, y + height)):
                if cls.ellipse_point(ellipse, p):
                    return True
            return False

        @classmethod
        def ellipse_ellipse(cls, e1, e2):
            """Verify collision between two ellipses."""
            # TODO: implement it!
            return False

        @classmethod
        def ellipse_line(cls, ellipse, line):
            """Verify colision between an ellipse and a rectangle."""
            for p in line:
                if cls.ellipse_point(ellipse, p):
                    return True
            return False

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
        def point_rect(cls, point, rect):
            """Verify collision between point and rectangle."""
            xo, yo = point
            x, y, w, h = rect
            return xo >= x and xo <= x + w and yo >= y and yo <= y + h

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
        def line_line(cls, l1, l2):
            """Check if a line segment intersects another."""
            def abc(p1, p2):
                x1, y1 = p1
                x2, y2 = p2
                a = y2 - y1
                b = x1 - x2
                c = x2 * y1 - x1 * y2
                return (a, b, c)

            def verify(abc, p1, p2):
                a, b, c = abc
                x1, y1 = p1
                x2, y2 = p2
                r1 = a * x2 + b * y1 + c
                r2 = a * x1 + b * y2 + c
                return r1 != 0 and r2 != 0 and sign(r1) == sign(r2)

            p1, p2 = l1
            p3, p4 = l2

            if verify(abc(p1, p2), p3, p4):
                return False
            if verify(abc(p3, p4), p1, p2):
                return False
            return True

        @classmethod
        def line_rect(cls, line, rect):
            """Check if a line segment intersects a rectangle."""
            p1, p2 = line
            x, y, w, h = rect
            if cls.point_rect(p1, rect) or cls.point_rect(p2, rect):
                return True
            for l in (((x, y), (x + w, y)), ((x, y), (x, y + h)),
                      ((x, y + h), (x + w, y + h)),
                      ((x + w, y), (x + w, y + h))):
                if cls.line_line(line, l):
                    return True
            return False

        @classmethod
        def invert(cls, fn):
            def do_it(a, b):
                return fn(b, a)
            return do_it

    # BOX = "box"
    ELLIPSE = "ellipse"
    RECT = "rect"
    CIRCLE = "circle"
    LINE = "line"
    POINT = "point"

    __functions = {
        "ellipse_rect": __Algo.ellipse_rect,
        "rect_ellipse": __Algo.invert(__Algo.ellipse_rect),
        "ellipse_circle": __Algo.ellipse_circle,
        "circle_ellipse": __Algo.invert(__Algo.ellipse_circle),
        "circle_rect": __Algo.circle_rect,
        "rect_circle": __Algo.invert(__Algo.circle_rect),
        "rect_rect": __Algo.rect_rect,
        "circle_circle": __Algo.circle_circle,
        "ellipse_ellipse": __Algo.ellipse_ellipse,
        "line_line": __Algo.line_line,
        "line_circle": lambda a, b: False,
        "circle_line": __Algo.invert(lambda a, b: False),
        "line_rect": __Algo.line_rect,
        "rect_line": __Algo.invert(__Algo.line_rect),
        "line_ellipse": __Algo.invert(__Algo.ellipse_line),
        "ellipse_line": __Algo.ellipse_line,
        "point_ellipse": __Algo.invert(__Algo.ellipse_point),
        "ellipse_point": __Algo.ellipse_point,
        "point_rect": __Algo.point_rect,
        "rect_point": __Algo.invert(__Algo.point_rect),
    }

    def __init__(self, bounding_shape):
        """Initialize the collision detection algorithms."""
        self.__bounding_shape = bounding_shape
        self.should_collide = True

    @property
    def bounding_shape(self):
        """Retrieve the object bounding shape."""
        return self.__bounding_shape

    def did_collide(self, object):
        """Return true if collides with object."""
        if not self.should_collide or not object.should_collide:
            return False
        shape = self.bounding_shape + "_" + object.bounding_shape
        fn = Collider.__functions.get(shape, lambda a, b: False)
        return fn(self.bounds, object.bounds)

    def collide_with(self, object):
        """Handle collision event."""
        raise NotImplementedError("Subclasses must implement collide_with().")

    @property
    def bounds(self):
        """Query object bounds."""
        x, y = self.position
        cx, cy = self.center
        w, h = self.dimension
        case = {Collider.ELLIPSE: (cx, cy, w, h),
                Collider.RECT: (x, y, w, h),
                Collider.CIRCLE: (cx, cy, min(w, h))}
        return case[self.bounding_shape]
