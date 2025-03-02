# Custom modules
import Controller.InterfaceController as InterfaceController
import Controller.LevelController as LevelController


while True:
    level, algorithm = InterfaceController.DrawSelectionMenu()
    print(level, algorithm)
    LevelController.InitLevel(level, algorithm)
