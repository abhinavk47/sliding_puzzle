import arcade
import random
import time
import cv2
from collections import defaultdict 
import sys
import os
PACKAGE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,PACKAGE_ROOT)
from config.constants import *
from core.graph import Node, get_distance, BFS

im = cv2.imread(IMAGE_PATH)
width, height = im.shape[0], im.shape[1]
size = min(width, height)

piece_size = size//PUZZLE_N
if PUZZLE_N>SIZE_OFFSET:
    PIECE_SCALED_SIZE-=(PUZZLE_N-SIZE_OFFSET)*10

class MyGame(arcade.Window):
    def __init__(self):
        """
        Variables
        _____________
        picture_textures: textures of sepatated pieces of the image
        empty_no: blank piece for moving other pieces
        curr_pos: target piece to be moved
        pos_x, pos_y: position of target piece to animate transition
        alpha: transparency of the target piece during transition
        """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, title=PUZZLE_TITLE)
        self.picture_textures = {}
        self.empty_no = PUZZLE_N**2-1
        for i in range(0, PUZZLE_N**2):
            if i==self.empty_no:
                self.picture_textures.update({
                    i:[None, i]
                })
                continue
            self.picture_textures.update({
                    i:[
                        arcade.load_texture(
                            IMAGE_PATH,
                            x=piece_size*(i%(PUZZLE_N)), y=piece_size*(i//(PUZZLE_N)),
                            width=piece_size, height=piece_size
                        ),
                        i
                    ]
                }
            )
        self.curr_pos = self.empty_no
        self.pos_x = 0
        self.pos_y = 0
        self.alpha = 255
        self.pressed = False
        self.steps = []
        self.moves = 0
        self.moves_list = []


    def solve(self):
        """
        Using BFS to solve
        """
        start = time.time()
        puzzle_list = [self.picture_textures[i][1] for i in self.picture_textures]
        
        moves, no_of_iterations = BFS(puzzle_list)
        
        self.moves = 0
        if moves!=None:
            self.moves_list = moves
            for move in moves:
                self.on_key_press(KEY_MAPPING[move], "modifiers")
                self.on_key_release("key", "modifiers")
        
        print("time taken: " + str(time.time()-start))
        print("number of iterations: "+str(no_of_iterations))

    def retrace(self):
        """
        Go back one step
        """
        if len(self.steps)!=0:
            if self.steps[-1]=='UP':
                self.steps.pop(-1)
                self.on_key_press(arcade.key.DOWN, "modifiers")
            elif self.steps[-1]=='DOWN':
                self.steps.pop(-1)
                self.on_key_press(arcade.key.UP, "modifiers")
            elif self.steps[-1]=='LEFT':
                self.steps.pop(-1)
                self.on_key_press(arcade.key.RIGHT, "modifiers")
            elif self.steps[-1]=='RIGHT':
                self.steps.pop(-1)
                self.on_key_press(arcade.key.LEFT, "modifiers")
            self.on_key_release("key", "modifiers")
            self.steps.pop(-1)

    def randomize(self):
        """
        Scramble the pieces
        """
        for _ in range(NO_OF_RND_HITS):
            key = random.choice(['left', 'right', 'up', 'down'])
            self.on_key_press(KEY_MAPPING[key], "modifiers")
            self.on_key_release("key", "modifiers")
        self.steps = []
        self.moves = 0

    def update(self, dt):
        """
        dt: deltatime
        """
        speed = 200
        self.alpha = 150
        if abs(self.curr_pos-self.empty_no)==1 and abs(self.pos_x)<=PIECE_SCALED_SIZE:
            self.pos_x += (self.curr_pos-self.empty_no)*dt*speed
        elif abs(self.curr_pos-self.empty_no)%PUZZLE_N==0 and abs(self.pos_y)<=PIECE_SCALED_SIZE:
            self.pos_y += ((self.curr_pos-self.empty_no)//PUZZLE_N)*dt*speed

    def rectangle_params(self, pos, is_curr):
        """
        returns rectangle parameters from position of the piece
        """
        pos_x, pos_y, alpha = 0,0,255
        if is_curr:
            pos_x, pos_y, alpha = -self.pos_x, self.pos_y, self.alpha
        return {
            "bottom_left_x":X_OFFSET+PIECE_SCALED_SIZE*(pos%PUZZLE_N)+pos_x, 
            "bottom_left_y":Y_OFFSET+(PUZZLE_N-1)*PIECE_SCALED_SIZE-PIECE_SCALED_SIZE*(pos//PUZZLE_N)+pos_y, 
            "width":PIECE_SCALED_SIZE, "height":PIECE_SCALED_SIZE, 
            "texture":self.picture_textures[pos][0], 
            "alpha":alpha
        }
    
    def text_params(self, pos, is_curr):
        """
        returns draw text parameters
        """
        pos_x, pos_y = 0,0
        if is_curr:
            pos_x, pos_y = -self.pos_x, self.pos_y
        return self.picture_textures[pos][1]==pos, {
            "text":str(self.picture_textures[pos][1]), 
            "start_x":X_OFFSET+PIECE_SCALED_SIZE//2+PIECE_SCALED_SIZE*(pos%PUZZLE_N)+pos_x, 
            "start_y":Y_OFFSET+PIECE_SCALED_SIZE//2+(PUZZLE_N-1)*PIECE_SCALED_SIZE-PIECE_SCALED_SIZE*(pos//PUZZLE_N)+pos_y, 
            "color":arcade.color.WHITE, 
            "font_size":PIECE_SCALED_SIZE*40//100, 
            "anchor_x":"center",
            "anchor_y":"center",
            "bold": True
        }

    def swap_positions(self):
        """
        swaps position of target piece with empty piece
        """
        temp = self.picture_textures[self.curr_pos]
        self.picture_textures[self.curr_pos] = self.picture_textures[self.empty_no]
        self.picture_textures[self.empty_no] = temp
        self.empty_no = self.curr_pos
        self.pos_x = 0
        self.pos_y = 0
        self.alpha = 255

    def button_params(self, text, pos_x, pos_y, radius, font_size, color):
        return {
            "center_x":pos_x,
            "center_y":pos_y,
            "radius":radius,
            "color":[0, 128, 128]
        }, {
            "text":text,
            "start_x":pos_x,
            "start_y":pos_y,
            "color":color,
            "font_size":font_size,
            "align":"center",
            "anchor_x":"center",
            "anchor_y":"center"
        }

    def on_draw(self):
        """
        Draws pieces of the image and show numbers button
        """
        arcade.start_render()
        is_done = True
        for i in range(0, PUZZLE_N**2):
            if i==self.empty_no:
                continue
            if i!=self.curr_pos:
                arcade.draw_lrwh_rectangle_textured(
                    **self.rectangle_params(i, False)
                )
                done, text_params = self.text_params(i, False)
                if self.pressed:
                    arcade.draw_text(
                        **text_params
                    )
                if not done:
                    is_done = False
        if self.curr_pos != self.empty_no:
            arcade.draw_lrwh_rectangle_textured(
                **self.rectangle_params(self.curr_pos, True)
            )
        done, text_params = self.text_params(self.curr_pos, True)
        if self.pressed and self.curr_pos!=self.empty_no:
            arcade.draw_text(
                **text_params
            )
        if not done:
            is_done = False
        
        if is_done:
            arcade.draw_text(
                text="Finished!", start_x=800, start_y=800,
                color=arcade.color.WHITE, font_size=20,
                align="center", 
                anchor_x="center", anchor_y="center"
            )
        
        text = "Show \nNumbers"
        if self.pressed:
            text = "Hide \nNumbers"

        color = arcade.color.BLACK
        
        circle_params, text_params = self.button_params(text, 1400, 700, 50, 14, color)
        arcade.draw_circle_filled(
            **circle_params
        )
        arcade.draw_text(
            **text_params
        )

        text = "Randomize"
        circle_params, text_params = self.button_params(text, 1400, 550, 50, 14, color)
        arcade.draw_circle_filled(
            **circle_params
        )
        arcade.draw_text(
            **text_params
        )

        text = "Solve"
        circle_params, text_params = self.button_params(text, 1400, 400, 50, 14, color)
        arcade.draw_circle_filled(
            **circle_params
        )
        arcade.draw_text(
            **text_params
        )

        text = "back"
        circle_params, text_params = self.button_params(text, 100, 800, 30, 14, color)
        arcade.draw_circle_filled(
            **circle_params
        )
        arcade.draw_text(
            **text_params
        )

        color = arcade.color.WHITE
        text = "moves: "+str(self.moves)
        _, text_params = self.button_params(text, 300, 800, 30, 25, color)
        arcade.draw_text(
            **text_params
        )

        color = arcade.color.WHITE
        part_1 = self.moves_list[:10]
        part_2 = "" if len(self.moves_list[10:])==0 else self.moves_list[10:]
        text = "moves list: "+str(part_1)+"\n"+str(part_2)
        _, text_params = self.button_params(text, 300, 700, 30, 13, color)
        arcade.draw_text(
            **text_params
        )


    def on_key_press(self, key, modifiers):
        """
        Transition with key press
        """
        if key==arcade.key.Q:
            self.close()
        elif key==arcade.key.LEFT:
            if self.empty_no%PUZZLE_N!=PUZZLE_N-1:
                self.curr_pos = self.empty_no+1
                if len(self.steps)>2:
                    self.steps.pop(0)
                self.steps.append('LEFT')
                self.moves+=1
        elif key==arcade.key.RIGHT:
            if self.empty_no%PUZZLE_N!=0:
                self.curr_pos = self.empty_no-1
                if len(self.steps)>2:
                    self.steps.pop(0)
                self.steps.append('RIGHT')
                self.moves+=1
        elif key==arcade.key.UP:
            if self.empty_no//PUZZLE_N!=PUZZLE_N-1:
                self.curr_pos = self.empty_no+PUZZLE_N
                if len(self.steps)>2:
                    self.steps.pop(0)
                self.steps.append('UP')
                self.moves+=1
        elif key==arcade.key.DOWN:
            if self.empty_no//PUZZLE_N!=0:
                self.curr_pos = self.empty_no-PUZZLE_N
                if len(self.steps)>2:
                    self.steps.pop(0)
                self.steps.append('DOWN')
                self.moves+=1

    def on_key_release(self, key, modifiers):
        self.swap_positions()
    
    def on_mouse_press(self, x, y, button, modifiers):
        """
        Transisiton with mouse press
        """
        if button==arcade.MOUSE_BUTTON_LEFT:
            if (x>X_OFFSET and x<PIECE_SCALED_SIZE*PUZZLE_N+X_OFFSET) and \
                (y>Y_OFFSET and y<PIECE_SCALED_SIZE*PUZZLE_N+Y_OFFSET):
                i = ((Y_OFFSET+(PUZZLE_N)*PIECE_SCALED_SIZE-y)//PIECE_SCALED_SIZE)*PUZZLE_N+(x-X_OFFSET)//PIECE_SCALED_SIZE
                offset=abs(i-self.empty_no)
                if offset==1 or offset%PUZZLE_N==0 and offset<=PUZZLE_N:
                    curr_pos = i
                    step = None
                    if curr_pos-self.empty_no==1 and curr_pos%PUZZLE_N!=0:
                        step = 'LEFT'
                    if curr_pos-self.empty_no==-1 and curr_pos%PUZZLE_N!=PUZZLE_N-1:
                        step = 'RIGHT'
                    if curr_pos>PUZZLE_N-1 and curr_pos-self.empty_no==PUZZLE_N:
                        step = 'UP'
                    if curr_pos<PUZZLE_N**2-PUZZLE_N and curr_pos-self.empty_no==-PUZZLE_N:
                        step = 'DOWN'
                    if step!=None:
                        self.curr_pos = curr_pos
                        if len(self.steps)>2:
                            self.steps.pop(0)
                        self.steps.append(step)
                        self.moves+=1

        if (1400-x)**2+(700-y)**2<=50**2:
            self.pressed = ~self.pressed

        if (1400-x)**2+(550-y)**2<=50**2:
            self.randomize()

        if (1400-x)**2+(400-y)**2<=50**2:
            self.solve()

        if (100-x)**2+(800-y)**2<=30**2:
            self.retrace()
    
    def on_mouse_release(self, x, y, button, modifiers):
        self.swap_positions()


if __name__ == "__main__":
    window = MyGame()
    arcade.run()


