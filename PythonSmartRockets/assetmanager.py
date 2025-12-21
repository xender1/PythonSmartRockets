import pygame
from typing import Dict, Optional

 #TODO: singleton now, but maybe pass it in or load once in rocket (class var)?
class AssetManager:
    """Load sprites here once to pass to rockets (singleton)"""

    _instance: Optional['AssetManager'] = None
    sprites: Dict[str, pygame.Surface]

    def __new__(cls):
        """Ensure only one instance exists"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.sprites = {}
        return cls._instance

    def __init__(self) -> None:
        """Initiate empty set of sprites"""
        pass  # sprites dict is created in __new__

    def load_sprite(self, name: str, path: str, colorkey=None, scale=None):
        """load sprite, will get referenced by name when loading"""
        sprite = pygame.image.load(path).convert()
        if colorkey:
            sprite.set_colorkey(colorkey)
        if scale:
            sprite = pygame.transform.scale(sprite, scale)
        self.sprites[name] = sprite

    def get_sprite(self, name: str):
        """Get loaded sprite by name"""
        return self.sprites[name]