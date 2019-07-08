import warnings
import os

"""
Values
"""
location = "outputed_functions"
datapack_name = "datapackFolder"
datapacksubfolder = "subfolder"
path = datapack_name + "\data\\" + datapacksubfolder + "\functions"

BCfolder = "default"
BCfunction_name = "main"

# use path = function_path inside your script to restore the path to MCfunctions
function_path = datapack_name + "\data\\" + datapacksubfolder + "\functions"

# path used by write function
path = os.path.join(
    location,
    datapack_name,
    "data",
    datapacksubfolder,
    "functions",
    BCfolder,
    BCfunction_name + ".mcfunction",
)

"""
json tag functions list
"""
mainloop_functions = []
load_functions = []


"""
Tecnical functions :
"""


def check_required_argument(value, Warning_message):
    """
    This will print the warning message if the value is empty or false
    """
    if value == False:
        warnings.warn(Warning_message, Warning, stacklevel=3)
        return False
    else:
        return True



def selector_add_criteria(selector = "@e", criteria = ""):
    """
This function insert the criterias inside the selector bracklets
even if the selector already contain others criterias

Arguments :
  - selector : the Minecraft selector to edit

  - criteria : a valid selector argument without bracklets
            or a list of valid selector argument

Output : a new selector containing the new arguments and the previous
    """

    #Cheching if selector have bracklets
    char_list = list(selector)
    if char_list[-1] == "]" :
        #re-opening the bracklets
        del char_list[-1]
        #Convert back to string
        selector = ""
        for char in char_list :
            selector += char

    else :
        #opening the bracklets
        selector += "["

    #Cheching if criteria is an unique string or a list
    if isinstance(criteria, str):
        
        #Adding the criteria and closing
        selector += criteria +"]"
        
    else :
        #Adding all the criterias and closing
        for c in criteria :
            selector += ","+ c
        selector += "]"
            
    return selector


"""
Scripting functions :
"""


def set_folder(
    folder=BCfolder,
    function_name=BCfunction_name,
    tag_function=False,
    file_path="",
    file_name="BCfile.txt",
):
    """
Description :
This function defines in wich file the "write" function will write his text

Arguments for a MCfunction :
  - function_name :
        input : the name of the MCfunction
        default value : the last used name
  
  - folder :
        input : the folders where to put the MCfunction
            it is inside the function folder of the datapack
        default value : the last used folders

  - tag_function :
        input :
            "load" : make the MCfunction run at datapack loading
            "tick" : make the MCfunction run at each game ticks
        default value : False

Arguments for an other file :
    file_name : the name of the file, including the extension
    file_path : the folder's path where the file is
        can be absolute or relative path
"""

    global BCfolder, BCfunction_name, path
    BCfolder, BCfunction_name = folder, function_name

    if file_path:
        # Creating the file asked if needed
        if file_name == "BCfile.txt":
            warnings.warn(
                '"set_folder" command does not have a file_name argument associated with the file_path\n'
                + 'the default file name "BCfile.txt" will be used',
                Warning, stacklevel=2
                )
        path = file_path

        try:
            os.makedirs(path)
        except OSError as exc:
            pass

        path = os.path.join(path, file_name)

    else:
        # Creating a mcfunction file if needed
        path = os.path.join(
            location, datapack_name, "data", datapacksubfolder, "functions", folder
        )

        try:
            os.makedirs(path)
        except OSError as exc:
            pass

        path = os.path.join(path, function_name + ".mcfunction")

        # adding the functions to json
        global mainloop_functions, load_functions
        if folder != None:
            folder = folder + "/"
        if tag_function:
            json_execute = "" + datapacksubfolder + ":" + folder + function_name
            if tag_function == "tick" and not (json_execute in mainloop_functions):
                mainloop_functions.append(json_execute)
            if tag_function == "load" and not (json_execute in load_functions):
                load_functions.append(json_execute)


def write(text):
    # EXAMPLE :  write("a command")  #write(["command","secondcommand","other command"])
    """
Description :
    this command write the text input at the end of the existing text inside the file set with \"set_file\"
    For MCcommands : You will use the output of others Bloccode's Functions as input

Argument :
    a string containing the text/MCcommands to write
 or a list of string containing the text/MCcommands to write
"""
    # This function uses the global value "path" to find the file
    # and open it with python's os module
    global path
    Bc_function = open(path, "a")

    # here we check the input type and write each line
    #print(text)
    if isinstance(text, list):
        for x in text:
            Bc_function.write("\n" + x)
    else:
        Bc_function.write("\n" + text)
    Bc_function.close()


def write_in(
    folder=BCfolder,
    function_name=BCfunction_name,
    tag_function=False,
    file_path="",
    file_name="BCfile.txt",
    text="",
):
    """
Description :
    This command is basically a "set_folder" and a "write" command grouped in a single command
    Does not change the file where the next "write" command will write

Arguments :
  - the same than "set_folder" command
        see "help(set_folder)"

  - text : the text/MCcommand to write in the file
    """
    # EXAMPLE :  write_in(folder : "dtest" , function_name : "t2", commands = ["command","secondcommand","other command"])
    global path
    current_path = path
    set_folder(
        folder=folder,
        function_name=function_name,
        tag_function=tag_function,
        file_path=file_path,
        file_name=file_name,
    )
    write(text)
    path = current_path


def new_objective(objective_name, stat = "dummy"):  # add a minecraft dummy objective at loading
    """
Description :
This command add a scoreboard objective at datapack loading

Arguments :
  - the name of the objective (required, must be at first)

  - stat : the stat type used for the objective (optional)
        default value : dummy
    """
    init_objective = []
    if isinstance(objective_name, list):
        for x in objective_name:
            init_objective.append("scoreboard objectives add " + x + " " + stat)
    else:
        init_objective.append("scoreboard objectives add " + objective_name + " " + stat)
    write_in(
        folder="bc_functions",
        function_name="bc_init",
        tag_function="load",
        text=init_objective,
    )


def get_function(folder=BCfolder, function_name=""):
    """
Description :
This command return the MCcommand "/function" wich target the file gived by the arguments

Arguments :
  - function_name :
        input : the name of the MCfunction
        default value : the last used name
  
  - folder :
        input : the folders where to put the MCfunction
            it is inside the function folder of the datapack
        default value : the last used folders


    """
    check_required_argument(
        function_name,
        '"get_function" command requires a missing mcfunction name,\n'
        + "it will return an invalid minecraft command",
    )
    if folder != "":
        folder = folder + "/"
    return ["function " + datapacksubfolder + ":" + folder + function_name]


def execute(criteria, commands):
    """
Description :
This command execute the commands with the criteria as /execute arguments

Arguments :
  - some valid "/execute" criterias

  - the commands to be executed with theses criterias
        can be a single command or a list of commands

Output : a list of "/execute" commands wich run each of the commands with the criterias
    """
    # EXAMPLE :  execute("at @a", ["say hello world","say hi"])
    output = []
    if isinstance(commands, list):
        for x in commands:
            output.append("execute " + criteria + " run " + x)
    else:
        output.append("execute " + criteria + " run " + commands)
    return output


def set_entity(
    entity_type="armor_stand",
    coords=["~", "~", "~"],
    tags=[],
    nbt="",
    scores={},
    commands=[],
):
    """
Description :
This command summon an entity with some additions to the /summon command

Arguments :
    entity_type : the type of the entity to summon

    coords : a list of X,Y,Z coordinates to summon the entity
        default : ["~", "~", "~"]

    tags : the tags to add to the entity
        can be a single tag or a tag list

    nbt : the nbt data to add to the entity, without "{}"

    scores : the scores to give to the entity
        in the form of a dictionary : scores = {"obj1":1, "obj2":2}

    commands : commands that target the entity with the "@e[tag=BCnew]" selector
        the "BCnew" tag only exist through "set_entity" command for this purpose

Output :
    a list containing the /summon command and, if required, the gived commands and scoreboards
    """
    # EXAMPLE :  set_entity("coords":["0","~","~"],"tags":["a","b","c"],"scores":{"obj1":1,"obj2":2}, "commands":["say hi"])
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
    if "scores" or "commands":
        newtags = newtags + ",BCnew"

    else:
        newtags = taglist

    new_entity = (
        "summon "
        + entity_type + " "
        + X + " "
        + Y + " "
        + Z
        + " {Tags:[" + newtags + "],"
        + nbt + "}"
    )
    output.append(new_entity)

    if scores or commands:
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


def take_score(
    target_entity="@s", target_objective="", aim_entity="@s", aim_objective = "") :
    """
Description :
This command return the MCcommand wich give to an entity the score of an other entity

Arguments :
  - target_entity : selector of the entity which will have his score changed
        default : "@s", the entity executing the MCcommand

  - target_objective : objective which the entity score will be changed


  - aim_entity : selector of the entity who gives the new score value
        default : the same selector than target_entity, the same entity

  - aim_objective : objective which the entity score gives the new value
        default : the same objective than target_objective
    """
    check_required_argument(
        target_objective,
        'a "take_score" command requires a minecraft ojective to target\n'
        "it will return an invalid minecraft command",
    )
    if not(aim_entity):
        aim_entity = target_entity

    if not(aim_objective):
        aim_objective = target_objective
    return ["scoreboard players operation " + target_entity +" "+ target_objective +" = "+ aim_entity +" "+ aim_objective]

    """
this is an other version of the same command
        "execute store result score "
        + target_entity
        + " "
        + target_objective
        + " run scoreboard players get "
        + aim_entity
        + " "
        + aim_objective
    """


def while_loop(
    criteria="", folder=BCfolder, function_name="test", commands="", late_commands="") :
    """
Description :
This create a while loop in minecraft's mcfunctions : the commands are runned as long as the criteria is meet

Arguments :
  - criteria : one or more execute criterias
        the loop is stopped when the criterias are no longer valid
        note : the loop does not check them at the first execution

  - function_name : the name of the mcfunction wich will contain the loop's commands
        must be dedicaced mcfunction name
    
  - folder : the folder containing the mcfunction
        default : the last used folder

  - commands : the commands runned at each loop execution

  - late_commands : commands runned at the end of the loop
        they are runned at the same count than others commands, in an inverted order

Technical info :
    the while loop is created through mcfunction recursivity :
        mcfunction contain : commands
                             execute criterias run itself
                             late_commands
    late_commands are useful for optimizations purposes, preventing the use of a second loop

    the criteria can include "as @entity", "at @entity"
        it will change the entity or location of the commands at each loop execution
"""
    # EXAMPLE :  while_loop({"criteria":"if entity @e[limit=1]", "folder" : "default", "function_name" : "test","commands":"an effective command", "late_commands":"this runs after the loop"})

    check_required_argument(
        criteria,
        '"while_loop" command requires a valid execute criteria to continue loop execution\n'
        + "otherwise, the loop will freese the game until execution count = maxCommandChainLengh",
    )

    check_required_argument(
        commands,
        '"while_loop" command requires minecraft commands to interact with execute criteria and stop loop execution\n'
        + "otherwise, the loop will freese the game until execution count = maxCommandChainLengh",
    )

    have_function_name = check_required_argument(function_name,
                                                 '"while_loop" command requires a valid dedicated function_name to store the commands\n'
                                                 + "Cancelled while_loop")
    if have_function_name :
        write_in(
            folder=folder,
            function_name=function_name,
            text=commands
        )
        write_in(
            folder=folder,
            function_name=function_name,
            text=execute(criteria,
                         get_function(folder=folder, function_name=function_name)
                         )
        )
        write_in(folder=folder,
                 function_name=function_name,
                 text=late_commands
                 )
        return get_function(folder, function_name)
    else :
        return []



def for_loop(
    objectivename="",
    count=0,
    entity="@s",
    criteria="",
    folder=BCfolder,
    function_name="test",
    commands=[],
    late_commands="",
    ):
    """
Description :
This create a for loop in minecraft's mcfunctions : the commands are runned the given count, and as long as the optional criteria is meet

Arguments :
  - the same as "while_loop"
        see "help(while_loop)"

  - objectivename : name of the objective wich store the execution count

  - entity : entity wich store the execution count as his objective's score

Technical info :
    the for loop is based on while_loop and an inctementing objective to stop itself with an extra score criteria
    the entity's score store the count of succesful executions even after beeing stopped by the failing criteria and exiting the loop

Possible issue :
    The commands execution should not interact with the selector of the entity storing the execution count
        if this entity switch, the execution count can be incorect
        you can secure this entity selector by targetting an entity tag
"""
    # EXAMPLE :  for_loop({"objectivename":"looptimes","range":3,"entity":"@s","criteria":"if entity @e[limit=1]", "folder" : "default", "function_name" : "test","commands":"an effective command", "late_commands":"this runs after the loop"})

    check_required_argument(
        objectivename,
        '"while_loop" command requires a valid dedicated objectivename to store the execution count\n'
        + "an invalid minecraft command will be outputed",
    )

    check_required_argument(
        entity,
        '"while_loop" command requires a valid entity selector to store the execution count as an score\n'
        + "an invalid minecraft command will be outputed",
    )


    #adding score criteria
    
    if criteria :
        criteria = "if score " + entity + " " + objectivename + " matches .." + str(count) + " " + criteria
    else :
        criteria = "if score " + entity + " " + objectivename + " matches .." + str(count)

    if isinstance(commands, str):
        commands = [commands]
    commands.append("scoreboard players add " + entity + " " + objectivename + " 1")

    while_loop_output = while_loop(
        criteria=criteria,
        folder=folder,
        function_name=function_name,
        commands=commands,
        late_commands=late_commands,
    )
    return [
        "scoreboard players set " + entity + " " + objectivename + " 0"
    ] + while_loop_output


"""
datapack finalizing
"""


def default_dat():
    """
    Creating Datapack .dat folder
    """
    data = """   {
   "pack": {
      "pack_format": 1,
      "description": "Data Pack generated by BlocCode"
   }
}"""
    write_in(
        file_path=os.path.join("outputed_functions", datapack_name),
        file_name="pack.mcmeta",
        text=data,
    )


def set_tag_functions():
    """
    Creating tick load json folders
    """
    json_text = """{
        "values": [\n"""
    for i in range(len(mainloop_functions)):
        json_text += '\n        "' + mainloop_functions[i] + '"'
        if i != len(mainloop_functions) - 1:
            json_text += ","
    json_text += """
        ]
    }"""

    write_in(
        file_path=os.path.join(
            location, datapack_name, "data", "minecraft", "tags", "functions"
        ),
        file_name="tick.json",
        text=json_text,
    )

    json_text = """{
        "values": ["""
    for i in range(len(load_functions)):
        json_text += '\n        "' + load_functions[i] + '"'
        if i != len(load_functions) - 1:
            json_text += ","
    json_text += """
        ]
    }"""

    write_in(
        file_path=os.path.join(
            location, datapack_name, "data", "minecraft", "tags", "functions"
        ),
        file_name="load.json",
        text=json_text,
    )


finish_commands = [default_dat, set_tag_functions]


def finishing():
    """
    This command run the functions wich complete the lasts datapack's creation steps
    theses are listed in the finish_commands list 
    """
    for function in finish_commands:
        function()
