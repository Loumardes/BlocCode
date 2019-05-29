from Bloccode_V1 import *

writed_folder({"folder": "default", "funct_name": "init", "tag_function": "load"})
write(
    ["say datapack loaded"]
    + new_objective("snake_rang")
    + new_objective("snake_id")
    + new_objective("snake_lengh")
)
writed_folder({"folder": "startsnake", "funct_name": "main"})
write(
    set_entity(
        {
            "coords": ["~", "~", "~"],
            "tags": "snake",
            "scores": {"snake_rang": 0, "snake_lengh": 10}
        }
    )
)

               
writed_folder({"folder": "default", "funct_name": "main", "tag_function": "tick"})
write(
    ["scoreboard players add @e[tag=snake] snake_rang 1"]
    + execute(
        "as @e[tag=snake,scores={snake_rang=1}] at @s",
        get_function("default", "head_forward"),
    )
    + execute(
        "as @e[tag=snake,scores={snake_rang=0}] at @s",
        get_function("default", "check_collision"),
    )
    + execute(
        "at @e[tag=snake,scores={snake_rang=0}] if entity @e[tag=apple,distance=0.5]",
        "scoreboard players add @e[tag=snake] snake_lengh 1",
    )
    + ["execute as @e[tag=snake] if score @s snake_rang = @s snake_lengh run kill @s"]
)


writed_folder({"folder": "default", "funct_name": "head_forward"})
write(execute("at @s",
    [
        "teleport @p ~ ~ ~",
        "tp @s @p",
        "tp @s ~ ~ ~ ~ 0"]+
        set_entity(
        {
            "coords": ["^", "^", "^0.25"],
            "tags": "snake",
            "scores": {"snake_rang": 0},
            "commands": take_score(
                "@s", "snake_lengh", "@e[tag=snake,limit=1]", "snake_lengh"
            )
            }
        )
    )
)

writed_folder({"folder": "default", "funct_name": "check_collision"})
write(
    execute(
        "if entity @e[tag=snake,distance=0.24,scores={snake_rang=1}]",
        get_function("default", "destroy_snake"),
    )
    + execute(
        "if block ~ ~-1 ~ minecraft:air", get_function("default", "destroy_snake")
    )
)

writed_folder({"folder": "default", "funct_name": "destroy_snake"})
write(["kill @e[tag=snake]"])


