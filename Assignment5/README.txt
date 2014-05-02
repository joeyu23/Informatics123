Model view controller
Goal: make a headless single-player bot for the whale game.
Start with the MVC code for the whale game: https://github.com/gentimouton/swarch/blob/master/mvc/whale.py
At the end of the assignment, your folder assignment5 should have three files: whaleuser.py, whalebot.py, and common.py. 
There is nothing to submit on EEE.
Start by copying whale.py into your folder. Make a copy of whale.py, and rename it whaleuser.py. 
Rename whale.py into whalebot.py. You should now have two files: whaleuser.py and whalebot.py. 

Q1. Work only in whalebot.py. Currently, the Pygame-based View displays every frame. 
Replace it by a View that prints the position every 50 frames. 
Don’t print the position of pellets or borders. For example:
Position: 51, 103
Position: 51, 53
Position: 51, 3
Position: 189, 77
You will still have to keep a dark Pygame screen on which you don’t display anything, 
just to be able to process the keyboard inputs. So, you input in the Pygame window like before, 
but the output is now the console. (30 points)

Q2. Work only in whalebot.py. Replace the controller with a stupid bot that picks a random direction every frame. 
The whole file should now not depend on Pygame at all. The bot runs by itself. No user input is required, 
except CTRL-C to kill the bot. (40 points)

Q3. The bot and the client are sharing the exact same model. Code is duplicated, 
and we want to avoid this. Create a common.py file holding the model code. No model 
code should remain in whalebot or whaleuser. (30 points)

Q4. Extra credit. Make the bot eat the pellets. (10 points)

