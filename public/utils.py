import os
import pygame


def translate_pos(pos: list[int]) -> list[int]:
    x, y = pos
    return [abs(x - 7), abs(y - 7)]


def format_time(time: float) -> str:
    time = round(time)
    minute = str(time // 60)
    second = str(time % 60)

    while len(minute) < 2:
        minute = "0" + minute
    while len(second) < 2:
        second = "0" + second

    return f"{minute}:{second}"


def load_assets(tile_size: int) -> tuple[list]:
    white_assets = list(
        map(
            lambda img: pygame.transform.smoothscale(img, (tile_size, tile_size)),
            [
                pygame.image.load(os.path.join("assets", "white", "wk.png")),
                pygame.image.load(os.path.join("assets", "white", "wq.png")),
                pygame.image.load(os.path.join("assets", "white", "wb.png")),
                pygame.image.load(os.path.join("assets", "white", "wn.png")),
                pygame.image.load(os.path.join("assets", "white", "wr.png")),
                pygame.image.load(os.path.join("assets", "white", "wp.png")),
            ],
        )
    )
    black_assets = list(
        map(
            lambda img: pygame.transform.smoothscale(img, (tile_size, tile_size)),
            [
                pygame.image.load(os.path.join("assets", "black", "bk.png")),
                pygame.image.load(os.path.join("assets", "black", "bq.png")),
                pygame.image.load(os.path.join("assets", "black", "bb.png")),
                pygame.image.load(os.path.join("assets", "black", "bn.png")),
                pygame.image.load(os.path.join("assets", "black", "br.png")),
                pygame.image.load(os.path.join("assets", "black", "bp.png")),
            ],
        )
    )

    return (white_assets, black_assets)
