# Author: Seth Hobbes
# Company: Springboro Technologies, LLC DBA Monarch Technologies
# Date: 1/20/2022
# Property of Seth Hobbes, member of Monarch Technologies, all rights reserved
# Image assets credit to: https://github.com/exewin https://exewin.github.io/
import space_marauders


# Main game function
def main():
    '''
    The main function.
    '''
    game = space_marauders.game.game.Game()
    game.run()


# Call main function
if __name__ == '__main__':
    main()
