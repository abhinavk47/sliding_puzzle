import arcade
import random
import time
import cv2
from collections import defaultdict 

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900

image_path = 'data/harry_potter.jpg'
im = cv2.imread(image_path)
width, height = im.shape[0], im.shape[1]
size = min(width, height)

puzzle_n = 4
piece_size = size//puzzle_n
piece_scaled_size = 100
if puzzle_n>9:
    piece_scaled_size-=(puzzle_n-9)*10

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
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, title="puzzle")
        self.picture_textures = {}
        self.empty_no = puzzle_n**2-1
        for i in range(0, puzzle_n**2):
            if i==self.empty_no:
                self.picture_textures.update({
                    i:[None, i]
                })
                continue
            self.picture_textures.update({
                    i:[
                        arcade.load_texture(
                            image_path,
                            x=piece_size*(i%(puzzle_n)), y=piece_size*(i//(puzzle_n)),
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
        for _ in range(2000):
            x = random.randint(200, piece_scaled_size*puzzle_n+200)
            y = random.randint(200, piece_scaled_size*puzzle_n+200)
            self.on_mouse_press(x, y, arcade.MOUSE_BUTTON_LEFT, "modifiers")
            self.on_mouse_release(x, y, arcade.MOUSE_BUTTON_LEFT, "modifiers")
        self.steps = []
        self.moves = 0

    def update(self, dt):
        """
        dt: deltatime
        """
        speed = 200
        self.alpha = 150
        if abs(self.curr_pos-self.empty_no)==1 and abs(self.pos_x)<=piece_scaled_size:
            self.pos_x += (self.curr_pos-self.empty_no)*dt*speed
        elif abs(self.curr_pos-self.empty_no)%puzzle_n==0 and abs(self.pos_y)<=piece_scaled_size:
            self.pos_y += ((self.curr_pos-self.empty_no)//puzzle_n)*dt*speed

    def rectangle_params(self, pos, is_curr):
        """
        returns rectangle parameters from position of the piece
        """
        pos_x, pos_y, alpha = 0,0,255
        if is_curr:
            pos_x, pos_y, alpha = -self.pos_x, self.pos_y, self.alpha
        return {
            "bottom_left_x":200+piece_scaled_size*(pos%puzzle_n)+pos_x, 
            "bottom_left_y":200+(puzzle_n-1)*piece_scaled_size-piece_scaled_size*(pos//puzzle_n)+pos_y, 
            "width":piece_scaled_size, "height":piece_scaled_size, 
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
            "start_x":200+piece_scaled_size//2+piece_scaled_size*(pos%puzzle_n)+pos_x, 
            "start_y":200+piece_scaled_size//2+(puzzle_n-1)*piece_scaled_size-piece_scaled_size*(pos//puzzle_n)+pos_y, 
            "color":arcade.color.CADET_GREY, 
            "font_size":piece_scaled_size*40//100, 
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
        for i in range(0, puzzle_n**2):
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


    def on_key_press(self, key, modifiers):
        """
        Transition with key press
        """
        if key==arcade.key.Q:
            self.close()
        elif key==arcade.key.LEFT:
            if self.empty_no%puzzle_n!=puzzle_n-1:
                self.curr_pos = self.empty_no+1
                if len(self.steps)>2:
                    self.steps.pop(0)
                self.steps.append('LEFT')
                self.moves+=1
        elif key==arcade.key.RIGHT:
            if self.empty_no%puzzle_n!=0:
                self.curr_pos = self.empty_no-1
                if len(self.steps)>2:
                    self.steps.pop(0)
                self.steps.append('RIGHT')
                self.moves+=1
        elif key==arcade.key.UP:
            if self.empty_no//puzzle_n!=puzzle_n-1:
                self.curr_pos = self.empty_no+puzzle_n
                if len(self.steps)>2:
                    self.steps.pop(0)
                self.steps.append('UP')
                self.moves+=1
        elif key==arcade.key.DOWN:
            if self.empty_no//puzzle_n!=0:
                self.curr_pos = self.empty_no-puzzle_n
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
            if (x>200 and x<piece_scaled_size*puzzle_n+200) and \
                (y>200 and y<piece_scaled_size*puzzle_n+200):
                i = ((200+(puzzle_n)*piece_scaled_size-y)//piece_scaled_size)*puzzle_n+(x-200)//piece_scaled_size
                offset=abs(i-self.empty_no)
                if offset==1 or offset%puzzle_n==0 and offset<=puzzle_n:
                    self.curr_pos = i
                    if self.curr_pos-self.empty_no==1:
                        step = 'LEFT'
                    elif self.curr_pos-self.empty_no==-1:
                        step = 'RIGHT'
                    elif self.curr_pos-self.empty_no>0:
                        step = 'UP'
                    else:
                        step = 'DOWN'
                    if len(self.steps)>2:
                        self.steps.pop(0)
                    self.steps.append(step)
                    self.moves+=1

        if (1400-x)**2+(700-y)**2<=50**2:
            self.pressed = ~self.pressed

        if (1400-x)**2+(550-y)**2<=50**2:
            self.randomize()

        if (100-x)**2+(800-y)**2<=30**2:
            self.retrace()
    
    def on_mouse_release(self, x, y, button, modifiers):
        self.swap_positions()

class Graph:
    def __init__(self):
        self.graph = defaultdict(list)
    def addEdge(self, u, v):
        self.graph[u].append(v)
    def BFS(self, s):
        visited = [False] * (len(self.graph))
        queue = []
        queue.append(s)
        visited[s] = True

        while queue:
            s = queue.pop(0)
            print(s, end = " ")
            for i in self.graph[s]:
                if visited[i]==False:
                    queue.append(i)
                    visited[i]=True


if __name__ == "__main__":
    window = MyGame()
    arcade.run()


