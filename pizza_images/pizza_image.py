import os
from PIL import Image


class ImageCreator:
    def __init__(self, ingradients):
        self.ingradients = ingradients
        
    def ingradients_correction(self, ingradient):
        ingradients_list = {
            "pepperoni": (100, 70),
            "peppers": (0, 10),
            "bacon": (50, 50),
            "cheese": (50, 80),
            "olives": (-50, -50),
            "chicken": (80, 90)
        }
        return ingradients_list[ingradient]
        
    
    def create_pizza_image(self, name):
        pizza_base = Image.open("pizza_images/pizza_base.png")
        
        
        for ingradient in self.ingradients:
            ingradient = str(ingradient)
            ing = Image.open(f'pizza_images/{ingradient}.png')
            pizza_base.paste(ing, self.ingradients_correction(ingradient), ing)
        
        pizza_base.save(f"pizza_images/pizza_images/{name}.png")
        
        return pizza_base
    
    def delete_pizza_image(path):
        try:
            os.remove("pizza_images/" + path)
            return f"Image {path} removed"
        except:
            return "File delete failed"
