project('game-state-service', version: '0.0.0')

dbus_dep = dependency ('dbus-1')
session_bus_services_dir = get_option('session-bus-services-dir')

if session_bus_services_dir == ''
   session_bus_services_dir = dbus_dep.get_pkgconfig_variable('session_bus_services_dir')
endif

conf = configuration_data()
conf.set('bindir', join_paths(get_option('prefix'), get_option('bindir')))

configure_file(
    input: 'com.endlessm.GameStateService.service.in',
    output: 'com.endlessm.GameStateService.service',
    install: true,
    install_dir: session_bus_services_dir,
    configuration: conf
)

install_data(
    'game-state-service',
    install_dir: get_option('bindir')
)

data_dir = join_paths(get_option('prefix'), get_option('datadir'))

subdir('data')

message('\n'.join([
    '@0@ @1@'.format(meson.project_name(), meson.project_version()),
    '--------------------------------------',
    'Directories:',
    '    prefix: @0@'.format(get_option('prefix')),
    '    bindir: @0@'.format(get_option('bindir')),
    '    datadir: @0@'.format(data_dir),
    '    session_bus_services_dir: @0@'.format(session_bus_services_dir),
    ''
]))
