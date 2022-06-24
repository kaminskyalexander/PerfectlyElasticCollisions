import pygame
import math
import random

pygame.init()

WIDTH, HEIGHT = 640, 640

# Every pixel is 10 cm or 0.1 m
PIXELS_IN_M = 10

def m_to_pixels(m):
    return m * PIXELS_IN_M

def pixels_to_m(pixels):
    return pixels / PIXELS_IN_M

def get_pixel_position(vector_in_m):
    return m_to_pixels(vector_in_m.x), HEIGHT - m_to_pixels(vector_in_m.y)