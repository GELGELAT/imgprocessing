import tkinter
from tkinter import *
from tkinter import messagebox, filedialog
from PIL import ImageTk, Image


class ImageList:
    pass


def create_image_list(pil_data):
    image_node = ImageList()
    image_node.pil_image = pil_data
    image_node.next = None
    return image_node


def image_list_prepend(head, pil_data):
    new_node = create_image_list(pil_data)
    new_node.next = head
    return new_node


def image_list_append(head, pil_data):
    if head:
        new_node = create_image_list(pil_data)
        current = head
        while current.next:
            current = current.next
        current.next = new_node
        new_node.previous = current
        return head
    return image_list_prepend(head, pil_data)

def get_last_image(head):
    current = head
    while current:
        current = current.next
    return current

def get_image(head, index):
    index_current = 0
    current = head
    while current:
        if index == index_current:
            return current
        index_current += 1
        current = current.next
    return head

def length_image(head):
    length = 0
    current = head
    while current:
        length += 1
        current = current.next
    return length




