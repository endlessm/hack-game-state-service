# GameStateService

Simply put, it's the player's save-file. More precisely, is a central service that manages all the metadata related to the user's progression in Hack, and is available to all components of the desktop. Technically speaking:

1. Manages all reading and writing operations to the player's state-file.
2. Provides a DBus interface that allows other components of the desktop to interact with the player's state.

## Player's State File

The state-file is just a plain-text file. Progression metadata is stored in this file using the JSON format, in order to keep it human-readable. By default, this file will be located at:

```
~/.var/app/com.hack_computer.GameStateService/data/state.json
```

As mentioned above, the contents of this `state.json` file are objects serialized with the JSON format. See the following example:

```json
{
  "item.key.fizzics.1" : {
    "consume_after_use" : true,
    "used" : true
  },
  "lock.fizzics.1 : {
    "locked" : true
  }
}
```

The example above shows entries that were written and read by the [Clubhouse](https://github.com/endlessm/clubhouse) and by the [Toolbox](https://github.com/endlessm/hack-toolbox-app). In the example, the Clubhouse has given the player the first key in the Fizzics quest line, which was later used and updated by the Toolbox to unlock the first Fizzics lockscreen. All that interaction between the Clubhouse, the Toolbox and the player's state is done throught the GameStateService.

**NOTE**: the root object of player's state must be a dictionary, while the sub-objects can, in theory, use any kind of serializable objects. When in doubt, make sure to test that your objects are being serialized properly, by manually reading the state file.

**NOTE**: the GameStateService does not provide, nor enforces, any kind content schema or structure. The contents of the state-file are entirely defined by the other components of the desktop. Therefore, it requires an agreement between these components to honour these definitions. For now, it is the price of simplicity.

## The DBus Service

The GameStateService exposes the API consumed by other components of the desktop to access and manipulate the player's state.

### Connecting To The Service

```javascript
const {Gio} = imports.gi;

const BusName = 'com.hack_computer.GameStateService';
const BusPath = '/com/hack_computer/GameStateService';
const BusIface = `
<node>
  <interface name='com.hack_computer.GameStateService'>
    <method name='Set'>
      <arg type='s' name='key' direction='in'/>
      <arg type='v' name='value' direction='in'/>
    </method>
    <method name='Get'>
      <arg type='s' name='key' direction='in'/>
      <arg type='v' name='value' direction='out'/>
    </method>
    <signal name='changed'>
      <arg type='s' name='key'/>
      <arg type='v' name='value'/>
    </signal>
  </interface>
</node>
`;
const GameStateProxy = Gio.DBusProxy.makeProxyWrapper(BusIface);
const gameStateProxy = new GameStateProxy(Gio.DBus.session, BusName, BusPath);
```

**NOTE**: in the example above, `BusIface` only includes the methods and signals used in the following examples. Check the [source](game-state-service) for the full list.

### Writing To The State

```javascript
const variant = new GLib.Variant('a{sb}', {locked: false});
gameStateProxy.SetSync('lock.example.1', variant)
```

**NOTE**: the killer-feature of this service, is the ability to store and retrieve virtually any kind of serializable data, as these methods take a [GLib.Variant](https://developer.gnome.org/glib/stable/glib-GVariant.html) as the value.

### Reading From The State

```javascript
const [variant] = gameStateProxy.GetSync('lock.example.1');
const dict = variant.deep_unpack();
print(dict['locked'].deep_unpack());
```

### Monitoring Changes From The State

```javascript
gameStateProxy.connect('g-signal', (proxy, sender, signal, params) => {
    if (signal !== 'changed')
        return;
    const key = params.get_child_value(0).deep_unpack();
    const variant = params.get_child_value(1).deep_unpack();
});
```

**NOTE**: the `changed` signal will always be emitted when any of the keys changes. If you need to listen to specific keys changes, add your own filtering logic, e.g. like is done in the Toolbox [LocksManager](https://github.com/endlessm/hack-toolbox-app/blob/master/src/locksManager.js).

### Miscellaneous Methods

The service also provides other methods that are useful during QA and debugging:

* `Reset` will empty the contents of the state-file. Usually helpful during QA for repeating the quest lines.
* `Reload` will force a re-load of the contents from the state-file. Usually helpful while debugging an issue that can be reproduced given a specific state.

For each of these methods, there is a `reset` and a `reload` signal, in case some desktop component needs to be aware of these events.

**NOTE**: the most realiable source for understanding the service API is the [source](game-state-service) it-self.

## Debugging

To enable debug messages in the GameStateService:

```
$ dbus-update-activation-environment --systemd GAME_STATE_DEBUG=1
```

Then to see the messages:

```
journalctl -f
```

## Development

If you want to quickly build a Flatpak with any changes you may have
done, and install it in the user installation base, you can do:

```
./tools/build-local-flatpak.sh --install
```

**NOTE**: good luck!
