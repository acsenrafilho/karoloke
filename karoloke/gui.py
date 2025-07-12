import PySimpleGUI as sg

import karoloke.player_controls as pc


def start_player_with_controllers(player, monitor):
    end_status = 0
    player.set_fullscreen(True)
    player.play()

    sg.theme('LightBlue')
    layout = [
        [
            sg.Button('+ Vol'),
            sg.Button('- Vol'),
            sg.Button('Pause'),
            sg.Button('Fechar Música'),
        ],  # noqa
    ]

    # Create the window
    window = sg.Window(
        'Karol-Oke Controles',
        layout,
        keep_on_top=True,
        location=(monitor.width, 0),
        finalize=True,
    )

    event_actions = {
        '+ Vol': pc.increase_volume,
        '- Vol': pc.decrease_volume,
        'Pause': pc.pause,
        'Fechar Música': pc.stop_music,
        'Ok': pc.select_music,
    }

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        event_actions[event](player, sg)
        if event in (sg.WIN_CLOSED, 'Fechar Música'):
            end_status = 1
            break

    window.close()

    return end_status
