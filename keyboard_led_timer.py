#!/usr/bin/env python
#
# Lara Maia <dev@lara.click> 2018
#
# The keyboard-led-timer is free software: you can redistribute
# it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# The keyboard-led-timer is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see http://www.gnu.org/licenses/.
#

import ctypes
import time
import asyncio

user32 = ctypes.WinDLL('User32.dll')

KEYCODE = {
    'CAPS_LOCK': 0x14,
    'NUM_LOCK': 0x90,
    'SCROLL_LOCK': 0x91,
}

SCANCODE = {
    'CAPS_LOCK': 0x003A,
    'NUM_LOCK': 0x0045,
    'SCROLL_LOCK': 0x0046,
}

EXTENDEDKEY = 0x0001
KEYUP = 0x0002
KEYDOWN = 0x0000
DEBUG = False

def debug(message):
    if DEBUG:
        print(message)

async def check_key(keycode: KEYCODE, scancode: SCANCODE) -> None:
    if user32.GetKeyState(keycode) != 0:
        debug(f'{keycode} is pressed. waiting 15 seconds.')
        for _ in range(29):
            await asyncio.sleep(1)
            if user32.GetKeyState(keycode) == 0:
                debug(f'skipping {keycode} because key was been released.')
                asyncio.ensure_future(check_key(keycode, scancode))
                return

        debug(f'releasing {keycode}.')
        user32.keybd_event(keycode, scancode, EXTENDEDKEY|KEYDOWN, 0)
        await asyncio.sleep(1)
        user32.keybd_event(keycode, scancode, EXTENDEDKEY|KEYUP, 0)
        debug(f'done releasing {keycode}.')
    else:
        debug(f'{keycode} is not pressed, ignoring.')

    debug(f'waiting 1 seconds for recheck {keycode}')
    await asyncio.sleep(1)
    asyncio.ensure_future(check_key(keycode, scancode))

    
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    
    asyncio.ensure_future(check_key(KEYCODE['CAPS_LOCK'], SCANCODE['CAPS_LOCK']))
    asyncio.ensure_future(check_key(KEYCODE['NUM_LOCK'], SCANCODE['SCROLL_LOCK']))
    asyncio.ensure_future(check_key(KEYCODE['SCROLL_LOCK'], SCANCODE['NUM_LOCK']))

    loop.run_forever()
   