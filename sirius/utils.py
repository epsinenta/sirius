def is_over(widget, pos: tuple):
    """ Проверка координат на нахождение внутри области кнопки
    :param widget: Объект, наведение на которого нужно проверить
    :param pos: Координаты курсора на экране
    :type pos: tuple
    :return: True, если Абсцисса и Ордината находится в области кнопки, иначе False.
    """
    if widget.x_coordinate < pos[0] < widget.x_coordinate + widget.width:
        if widget.y_coordinate < pos[1] < widget.y_coordinate + widget.height:
            return True
    return False

