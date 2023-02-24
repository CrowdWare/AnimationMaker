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

def timeString(val, showMinutes):
    minutes = int(val / 60000)
    seconds = int((val - minutes * 60000) / 1000)
    milliseconds = int(val - minutes * 60000 - seconds * 1000)
    txt = ""
    if minutes > 0 or showMinutes:
        txt = f"{minutes}:{seconds:02}.{milliseconds // 100}"
    else:
        txt = f"{seconds:2}.{milliseconds // 100}"
    return txt