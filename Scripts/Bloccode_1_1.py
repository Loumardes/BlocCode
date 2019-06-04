import warnings
import os
datapack_name = "datapackFolder"
folder = "default"
funct_name = "main"
mainloop_functions = []
load_functions = []
path = os.path.join(
    "outputed_functions",
    datapack_name,
    "data\datapacksubfolder",
    "functions\default",
    "main.mcfunction",
)

"""
Tecnical functions :
"""
def check_required_argument(value, Warning_message):
    if value == False :
        warnings.warn(Warning_message, Warning, stacklevel=3)
        #print("[Warning]", Warning_message)




"""
Scripting functions :
"""

def writed_folder(new_folder = folder, function_name = funct_name, tag_function = False):
    #EXAMPLE : writed_folder("folder" : "default" , "funct_name" : "test"})     writed_folder({"folder" : "default" , "funct_name" : "test" , "tag_function":"load")
    global path, folder, funct_name, mainloop_functions, load_functions
    folder = new_folder
    try:
        os.makedirs(
            os.path.join(
                "outputed_functions",
                datapack_name,
                "data\datapacksubfolder",
                "functions\\",
                folder,
            )
        )
    except OSError as exc:
        pass
    funct_name = function_name
    path = os.path.join(
        "outputed_functions",
        datapack_name,
        "data\datapacksubfolder",
        "functions\\",
        folder,
        function_name + ".mcfunction",
    )

    if folder != None:
        folder = folder + "/"
    if tag_function :
        json_execute = "datapacksubfolder:" + folder + funct_name
        if tag_function == "tick" and not(json_execute in mainloop_functions) :
            mainloop_functions.append(json_execute)
        if tag_function == "load" and not(json_execute in load_functions) :
            load_functions.append(json_execute)


def write(text):
    #EXAMPLE :  write("a command")  #write(["command","secondcommand","other command"])
    global path
    Bc_function = open(path, "a")
    if isinstance(text, list):
        for x in text:
            Bc_function.write("\n" + x)
    else:
        Bc_function.write("\n" + text)
    Bc_function.close()


def write_in(temp_folder = folder, temp_name = funct_name, tag_function = False,
             commands = ""):
    #EXAMPLE :  write_in(temp_folder : "dtest" , temp_name : "t2", commands = ["command","secondcommand","other command"])
    global path
    current_path = path
    writed_folder(new_folder = temp_folder, function_name = temp_name, tag_function = tag_function)
    write(commands)
    path = current_path


def new_objective(objective_name):  # add a minecraft dummy objective at loading
    init_objective = []
    if isinstance(objective_name, list):
        for x in objective_name:
            init_objective.append("scoreboard objectives add " + x + " dummy")
    else:
        init_objective.append("scoreboard objectives add " + objective_name + " dummy")
    write_in(temp_folder = "bc_functions", temp_name = "bc_init", tag_function = "load",
             commands = init_objective)
    

def get_function(folder = folder, function_name = ""):
    check_required_argument(funct_name,
                            "\"get_function\" command requires a missing mcfunction name,\n"+
                            "it will return an invalid minecraft command")
    if folder != "":
        folder = folder + "/"
    return ["function datapacksubfolder:" + folder + funct_name]



def execute(criteria, commands):
    #EXAMPLE :  execute("at @a", ["say hello world","say hi"])
    output = []
    if isinstance(commands, list):
        for x in commands:
            output.append("execute " + criteria + " run " + x)
    else:
        output.append("execute " + criteria + " run " + commands)
    return output


def set_entity(entity_type = "armor_stand", coords = ["~","~","~"], tags = [], nbt = "", scores = {}, commands = []):
    #EXAMPLE :  set_entity({"coords":["0","~","~"],"tags":["a","b","c"],"scores":{"obj1":1,"obj2":2, "commands":["say hi"]}})
    output = []
    X = coords[0]
    Y = coords[1]
    Z = coords[2]
    newtags = ""
    if isinstance(tags, list):
        for x in range(len(tags)):
            if x > 0:
                newtags = newtags + ","
            newtags = newtags + tags[x]
    else:
        newtags = tags
    if "scores" or "commands" :
        newtags = newtags + ",BCnew"

    else:
        newtags = taglist

    new_entity = (
        "summon "+ entity_type+ " "
        + X + " "
        + Y + " "
        + Z
        + " {Tags:["+ newtags+ "],"
        + nbt+ "}"
    )
    output.append(new_entity)

    if scores or commands :
        if scores:
            for k, v in scores.items():
                output.append(
                    "scoreboard players set @e[tag=BCnew] " + k + " " + str(v)
                )
        if commands :
            commandes = ""
            for x in commands :
                commandes += x + "\n"
                output += execute("as @e[tag=BCnew]", x)
        if scores or commands :
            output.append("tag @e remove BCnew")
    return output


def take_score(target_entity = "@s", target_objective = "", aim_entity = "@s", aim_objective = ""):
    check_required_argument(target_objective, "a \"take_score\" command requires a minecraft ojective to target\n"
                            "it will return an invalid minecraft command")
    check_required_argument(aim_objective, )
    return [
        "execute store result entity "
        + target_entity
        + " "
        + target_objective
        + " float 1 run scoreboard players get "
        + aim_entity
        + " "
        + aim_objective
    ]


def while_loop(criteria = "", folder = folder, function_name = "test", commands = "", late_commands = ""):
    #EXAMPLE :  while_loop({"criteria":"if entity @e[limit=1]", "folder" : "default", "funct_name" : "test","commands":"an effective command", "late_commands":"this runs after the loop"})

    check_required_argument(criteria,
                            "\"while_loop\" command requires a valid execute criteria to continue loop execution\n" +
                            "otherwise, the "+function_name+" will run once only")    
    
    check_required_argument(commands,
                            "\"while_loop\" command requires minecraft commands to interact with execute criteria and stop loop execution\n" +
                            "otherwise, the "+function_name+" if run will freese the game until execution count = maxCommandChainLengh")

    if funct_name :         
        temp_path = {folder: folder, function_name : function_name}
        write_in(commands = commands, **temp_path)
        write_in(temp_folder = folder, temp_name = function_name,
                 commands = "execute " + criteria + " run " + get_function(new_folder = folder, funct_name = funct_name)
        )
        write_in(late_commands = late_commands, **temp_path)
        return [
            "execute "
            + criteria
            + " run "
            + get_function(folder, function_name)
        ]
    else :
        warnings.warn("\"while_loop\" command requires a valid dedicated function_name to store the commands\n" +
                      "Cancelled while_loop", Warning, stacklevel=2)

def for_loop(objectivename = "", count = 0, entity = "@s", criteria = " ", folder = folder, function_name = "test", commands = [], late_commands = ""):
    #EXAMPLE :  for_loop({"objectivename":"looptimes","range":3,"entity":"@s","criteria":"if entity @e[limit=1]", "folder" : "default", "funct_name" : "test","commands":"an effective command", "late_commands":"this runs after the loop"})

    check_required_argument(objectivename,
                            "\"while_loop\" command requires a valid dedicated objectivename to store the execution count\n" +
                            "an invalid minecraft command will be outputed")

    check_required_argument(entity,
                            "\"while_loop\" command requires a valid entity selector to store the execution count as an ojective\n" +
                            "an invalid minecraft command will be outputed")

    commands.append("scoreboard players remove " + entity + " 1 " + objectivename)
    
    selector = list(entity)
    if selector[-1] == "]":
        del selector[-1]
        entity = ""
        criteria = (
            "if entity "
            + str(selector)
            + ",scores={"
            + objectivename
            + "="
            + str(count)
            + "..}]"
            + criteria
        )
    else:
        selector = (
            str(selector)
            + "[scores={"
            + objectivename
            + "="
            + str(count)
            + "..}] "
        )
    while_loop_output = while_loop(criteria = criteria, folder = folder, function_name = function_name, commands = commands, late_commands = late_commands)
    return while_loop_output + ["scoreboard players add " + entity +" "+ str(count) +" "+ objectivename]


"""
Creating .dat folder
"""
try:
    os.makedirs(
        os.path.join(
            "outputed_functions",
            datapack_name,
            "data\datapacksubfolder",
            "functions\default",
        )
    )
except OSError as exc:
    pass

Bc_function = open(
    os.path.join("outputed_functions", datapack_name, "pack.mcmeta"), "a"
)
Bc_function.write(
    """   {
   "pack": {
      "pack_format": 1,
      "description": "Data Pack generated by BlocCode"
   }
}"""
)
Bc_function.close()





def set_tag_functions():
    """
    Creating tick load json folders
    """
    try:
        os.makedirs(
            os.path.join(
                "outputed_functions",
                datapack_name,
                "data",
                "minecraft",
                "tags",
                "functions\\",
            )
        )
    except OSError as exc:
        pass

    Bc_function = open(
        os.path.join(
            "outputed_functions",
            datapack_name,
            "data",
            "minecraft",
            "tags",
            "functions",
            "tick" + ".json",
        ),
        "a",
    )
    Bc_function.write(
        """{
        "values": ["""
    )
    for x in mainloop_functions:
        Bc_function.write('\n        "' + x + '"')
    Bc_function.write(
        """
        ]
    }"""
    )
    Bc_function.close()

    Bc_function = open(
        os.path.join(
            "outputed_functions",
            datapack_name,
            "data",
            "minecraft",
            "tags",
            "functions",
            "load" + ".json",
        ),
        "a",
    )
    Bc_function.write(
        """{
        "values": ["""
    )
    for x in load_functions:
        Bc_function.write('\n        "' + x + '"')
    Bc_function.write(
        """
        ]
    }"""
    )
    Bc_function.close()
