import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.escape

import os
import sys
import random
import pandas as pd
import numpy

settings = {
    "static_path": os.path.dirname(__file__)
}

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('ga.html')

class MyFormHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<html><body><form action="/myform" method="POST">'
                   '<input type="text" name="message">'
                   '<input type="submit" value="Submit">'
                   '</form></body></html>')

    def post(self):
        self.set_header("Content-Type", "text/plain")
        self.write("You test wrote " + self.get_body_argument("message"))
        
class EchoWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        df = self.genAlg1(message)


    def on_close(self):
        print("WebSocket closed")

    def randomWord (self, length):
      chars= "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789!@#$%^&*();',./:<>?`~_+=-[]\{}| "
      wrd = ''
      for i in range(length):
        wrd += random.choice(chars)
      return wrd

    def evalueation(self, goal, current):
        """ given goal and current string, get how different are them
        """
        chars= "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789!@#$%^&*();',./:<>?`~_+=-[]\{}| "
        distance = 0
        for i in range(len(goal)):
            if goal[i] != current[i]:
                current_distance = abs(chars.index(goal[i]) - chars.index(current[i]))
                distance += current_distance
        return distance
        

    def genAlg1(self, goal):
      chars= list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789!@#$%^&*();',./:<>?`~_+=-[]\{}| ")
      start = self.randomWord(len(goal))
      parent_score = self.evalueation(goal, start)
      df = pd.DataFrame({'evaluation':[parent_score], 'string': [start]})
      
      while start != goal:
          parent_score = df.iloc[-1]['evaluation']
          # since string is not muttable, we need to change start to a list
          child = list(start)
          child[random.choice(range(0,len(start)))] = chars[random.choice(range(0,len(chars)))]
          child = "".join(child)
          child_score = self.evalueation(goal, child)
          
          if child_score < parent_score:
              start = child
              current_df = pd.DataFrame({'evaluation':[child_score], 'string': [start]})
              self.write_message(current_df.loc[0, "string"])
              df = df.append(current_df, ignore_index = True)
              
      return df


if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", MainHandler),
        (r"/myform", MyFormHandler),
        (r'/ws', EchoWebSocket)
        ], debug = True, static_path = os.path.join(os.path.dirname(__file__), "static"))
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
    