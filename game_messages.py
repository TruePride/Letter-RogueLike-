import tcod as libtcod

import textwrap


class Message:
    def __init__(self, text, color=libtcod.white):
        self.text = text
        self.color = color

class MessageLog:
    def __init__(self, x, width, height):
        self.messages = []
        self.x = x
        self.width = width
        self.height = height

    def add_message(self, message):
        # Splits messages if message is too long across multiple lines
        new_msg_lines = textwrap.wrap(message.text, self.width)

        for line in new_msg_lines:
            # if list of messages too big, removes first line to create room for the new one
            if len(self.messages) == self.height:
                del self.messages[0]

            # adds the new message as a Message object with its text and colors
            self.messages.append(Message(line, message.color))