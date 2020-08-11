#
# Copyright © 2020 Endless OS Foundation LLC.
#
# This file is part of hack-game-state-service
# (see https://github.com/endlessm/hack-game-state-service).
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
from gi.repository import Gio, GLib

_loop = GLib.MainLoop()

_samples = {
    'SAMPLE_001': {
        'value': True,
        'signature': 'b',
    },
    'SAMPLE_002': {
        'value': 10,
        'signature': 'x',
    },
    'SAMPLE_003': {
        'value': 0.10,
        'signature': 'd',
    },
    'SAMPLE_004': {
        'value': 'STRING',
        'signature': 's',
    },
    'SAMPLE_005': {
        'value': [1, 2, 3],
        'signature': 'ax',
    },
    'SAMPLE_006': {
        'value': ['1', '2', '3'],
        'signature': 'as',
    },
}

_proxy = Gio.DBusProxy.new_sync(Gio.bus_get_sync(Gio.BusType.SESSION, None),
                                0,
                                None,
                                'com.hack_computer.GameStateService',
                                '/com/hack_computer/GameStateService',
                                'com.hack_computer.GameStateService',
                                None)


def _on_changed(proxy, sender, signal, params):
    key, value = params.unpack()
    print(key + ' OK(c)' if value == _samples[key]['value'] else 'FAILED(c)')
    if key == 'SAMPLE_006':
        _loop.quit()


def _methods(key):
    variant = GLib.Variant(_samples[key]['signature'], _samples[key]['value'])
    _proxy.Set('(sv)', key, variant)
    value = _proxy.Get('(s)', key)
    print(key + ' OK' if value == _samples[key]['value'] else 'FAILED')


def _exceptions(key):
    try:
        _proxy.Get('(s)', key)
    except GLib.Error as error:
        print(error)
        print('%s OK' % key)
    else:
        print('%s FAILED' % key)


_proxy.connect('g_signal', _on_changed)

_methods('SAMPLE_001')
_methods('SAMPLE_002')
_methods('SAMPLE_003')
_methods('SAMPLE_004')
_methods('SAMPLE_005')
_methods('SAMPLE_006')

_exceptions('SAMPLE_NOTFOUND')

_loop.run()
