from lib.states.main_menu import Main, MainMenu


if __name__ == '__main__':
    game = Main()
    main_menu = MainMenu()
    game.run(main_menu)
