from build_in_tasks import create_single_tasks
create_single_tasks()

if __name__ == "__main__":
    from logger import Logger
    Logger(filename_output='winsau.log')
    import tui

    Logger().global_level = Logger.Level.DEBUG
    tui.MainMenu().show_loop()

