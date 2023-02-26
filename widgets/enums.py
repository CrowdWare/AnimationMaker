#############################################################################
# Copyright (C) 2023 CrowdWare
#
# self file is part of AnimationMaker.
#
#  AnimationMaker is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  AnimationMaker is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with AnimationMaker.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from enum import Enum

class ItemType(Enum):
    TypeItem = 0
    TypeRectangle = 1
    TypeEllipse = 2
    TypeText = 3
    TypeBitmap = 4
    TypeSvg = 5


class EditMode(Enum):
    ModeSelect = 0
    ModeRectangle = 1
    ModeEllipse = 2
    ModeText = 3
    ModeBitmap = 4
    ModeSvg = 5
    ModePlugin = 6

class MouseState(Enum):
    kMouseReleased = 0
    kMouseDown = 1 
    kMouseMoving = 2

class RulerType(Enum):
    Horizontal = 0
    Vertical = 1