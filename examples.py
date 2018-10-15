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
                                'com.endlessm.GameStateService',
                                '/com/endlessm/GameStateService',
                                'com.endlessm.GameStateService',
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
