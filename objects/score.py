"""Models the game score."""

from engine import GameObject, Label


class Score(GameObject):
    """Models a game score with high-core."""

    def __init__(self, font, position, **kwargs):
        """Initialize the game object."""
        GameObject.__init__(self, GameObject.Priority.BACKGROUND.value - 10)
        print(font, position)
        self.__position = position
        self.__digits = [Label(font, str(i), (0, 0)) for i in range(10)]
        self.__show_highscore = kwargs.get('highscore', False)
        self.restart()

    def update(self, *args, **kwargs):
        """No need to update it."""

    def draw(self, screen):
        """Draw score to screen."""
        score = self.__highscore if self.__show_highscore else self.__score
        value = "{:0>8}".format(score)
        x, y = self.__position
        for n in value:
            digit = self.__digits[int(n)]
            rect = digit.bounds
            rect.x = x
            x += rect.width
            digit.bounds = rect
            digit.draw(screen)

    def add(self, value):
        """Add a value to the highscore."""
        self.__score += value
        if self.__score > self.__highscore:
            self.__highscore = self.__score

    def toggle_score(self):
        """Toggle wich score to display."""
        self.__show_highscore = not self.__show_highscore

    def restart_score(self):
        """Restart score counting."""
        self.__score = 0

    def restart(self):
        """Restart score counting."""
        self.__score = 0
        self.__highscore = 0
