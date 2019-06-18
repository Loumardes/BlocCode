# coding: utf8
import warnings
import os

"""
Values
"""
location = "outputed_functions\\"
datapack_name = "datapackFolder"
datapacksubfolder = "subfolder"
path = datapack_name + "\data\\" + datapacksubfolder + "\functions"
folder = "default"
function_name = "main"

#use path = function_path inside your script to restore the path to MCfunctions
function_path = datapack_name + "\data\\" + datapacksubfolder + "\functions"

#path used by write function
path = os.path.join(location,
                    datapack_name,
                    "data",
                    datapacksubfolder,
                    "functions",
                    folder,
                    new_function_name + ".mcfunction")

"""
json tag functions list
"""
mainloop_functions = []
load_functions = []



"""
Tecnical functions :
"""
def check_required_argument(value, Warning_message):
    if value == False :
        warnings.warn(Warning_message, Warning, stacklevel=3)
        return False
    else :
        return True




"""
Scripting functions :
"""

def set_folder(new_folder = folder, new_function_name = function_name, tag_function = False,
                  file_path = "", file_name = "BCfile.txt"):
    """
Description :
This function defines in wich file the write function will write his text

Arguments for a MCfunction :
  - new_function_name :
        input : the name of the MCfunction
        default value : the last used name
  
  - new_folder :
        input : the folders where to put the MCfunction
            it is inside the function folder of the datapack
        default value : the last used folders

  - tag_function :
        input :
            "load" : make the MCfunction run at datapack loading
            "tick" : make the MCfunction run at each game ticks
        default value : None

Arguments for an other file :
    file_name : the name of the file, including the extension
    file_path : the folder's path where the file is
        can be absolute or relative path
"""

    global folder, function_name, path
    folder, function_name = new_folder, new_function_name
    
    if file_path :
        #Creating the file asked if needed
        if file_name == "BCfile.txt" :
            warnings.warn("\"set_folder\" command does not have a file_name argument associated with the file_path\n"+
                          "the default file name \"BCfile.txt\" will be used", Warning, stacklevel=2)
        
        file_path.encode('unicode_escape')
        path = file_path

        try:
            os.makedirs(path)
        except OSError as exc:
            pass

        path = os.path.join(path, file_name)

        
    else :
        #Creating a mcfunction file if needed
        path = os.path.join(location,
                            datapack_name,
                            "data",
                            datapacksubfolder,
                            "functions",
                            folder)

        try:
            os.makedirs(path)
        except OSError as exc:
            pass

        path = os.path.join(path, new_function_name + ".mcfunction")

        #adding the functions to json
        global mainloop_functions, load_functions
        if folder != None:
            folder = folder + "/"
        if tag_function :
            json_execute = "" + datapacksubfolder + ":" + folder + function_name
            if tag_function == "tick" and not(json_execute in mainloop_functions) :
                mainloop_functions.append(json_execute)
            if tag_function == "load" and not(json_execute in load_functions) :
                load_functions.append(json_execute)


def write(text):
    #EXAMPLE :  write("a command")  #write(["command","secondcommand","other command"])
    """
Description :
    this command write the text input at the end of the existing text inside the file set with \"set_file\"
    For MCcommands : You will use the output of others Bloccode's Functions as input

Argument :
    a string containing the text/MCcommands to write
 or a list of string containing the text/MCcommands to write
"""
    #This function uses the global value "path" to find the file
    #and open it with python's os module
    global path
    Bc_function = open(path, "a")

    #here we check the input type and write each line
    if isinstance(text, list):
        for x in text:
            Bc_function.write("\n" + x)
    else:
        Bc_function.write("\n" + text)
    Bc_function.close()




def write_in(temp_folder = folder, temp_name = function_name, tag_function = False,
             file_path = "", file_name = "BCfile.txt",
             commands = ""):
    #EXAMPLE :  write_in(temp_folder : "dtest" , temp_name : "t2", commands = ["command","secondcommand","other command"])
    global path
    current_path = path
    set_folder(new_folder = temp_folder, new_function_name = temp_name, tag_function = tag_function,
                  file_path = file_path, file_name = file_name)
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
    check_required_argument(function_name,
                            "\"get_function\" command requires a missing mcfunction name,\n"+
                            "it will return an invalid minecraft command")
    if folder != "":
        folder = folder + "/"
    return ["function " + datapacksubfolder + ":" + folder + function_name]



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
                
        if isinstance(commands, str):
            commands = [commands]
        output += commands
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
    #EXAMPLE :  while_loop({"criteria":"if entity @e[limit=1]", "folder" : "default", "function_name" : "test","commands":"an effective command", "late_commands":"this runs after the loop"})

    check_required_argument(criteria,
                            "\"while_loop\" command requires a valid execute criteria to continue loop execution\n" +
                            "otherwise, the "+function_name+" will run once only")    
    
    check_required_argument(commands,
                            "\"while_loop\" command requires minecraft commands to interact with execute criteria and stop loop execution\n" +
                            "otherwise, the "+function_name+" if run will freese the game until execution count = maxCommandChainLengh")

    if function_name :         
        temp_path = {folder: folder, new_function_name : function_name}
        write_in(commands = commands, **temp_path)
        write_in(temp_folder = folder, temp_name = function_name,
                 commands = "execute " + criteria + " run " + get_function(new_folder = folder, function_name = function_name)
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
    #EXAMPLE :  for_loop({"objectivename":"looptimes","range":3,"entity":"@s","criteria":"if entity @e[limit=1]", "folder" : "default", "function_name" : "test","commands":"an effective command", "late_commands":"this runs after the loop"})

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
            "data\\" + datapacksubfolder,
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
