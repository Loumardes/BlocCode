# BlocCode
Scripting language for Minecraft datapacks

## Bloccode documentation :


set_folder(folder=BCfolder, function_name=BCfunction_name, tag_function=False,
           file_path="", file_name="BCfile.txt")

Description :
    This command defines in wich file the "write" function will write his text


write(text)

Description :
    This command write the text input at the end of the existing text inside the file set with "set_file"


write_in(
    folder=BCfolder, function_name=BCfunction_name, tag_function=False,
    file_path="", file_name="BCfile.txt",
    text="")

Description :
    This command is basically a "set_folder" and a "write" command grouped in a single command
    Does not change the file where the next "write" command will write


new_objective(objective_name, stat = "dummy")

Description :
This command add a scoreboard objective at datapack loading


get_function(folder=BCfolder, function_name="")

Description :
This command return the MCcommand "/function" wich target the file gived by the arguments


def execute(criteria, commands):

Description :
This command execute the commands with the criteria as /execute arguments


set_entity(
    entity_type="armor_stand",
    coords=["~", "~", "~"],
    tags=[],
    nbt="",
    scores={},
    commands=[])

Description :
This command summon an entity with some additions to the /summon command

take_score(target_entity="@s", target_objective="", aim_entity="@s", aim_objective = "")

Description :
This command return the MCcommand wich give to an entity the score of an other entity


while_loop(
    criteria="", folder=BCfolder, function_name="test", commands="", late_commands="")

Description :
This create a while loop in minecraft's mcfunctions : the commands are runned as long as the criteria is meet


for_loop(objectivename="", count=0, entity="@s",
    criteria="", folder=BCfolder, function_name="test", commands=[], late_commands="")

Description :
This create a for loop in minecraft's mcfunctions : the commands are runned the given count, and as long as the optional criteria is meet
set_folder(folder=BCfolder, function_name=BCfunction_name, tag_function=False,
           file_path="", file_name="BCfile.txt")
Description :
    This command defines in wich file the "write" function will write his text


write(text)

Description :
    This command write the text input at the end of the existing text inside the file set with "set_file"


write_in(
    folder=BCfolder, function_name=BCfunction_name, tag_function=False,
    file_path="", file_name="BCfile.txt",
    text="")

Description :
    This command is basically a "set_folder" and a "write" command grouped in a single command
    Does not change the file where the next "write" command will write


new_objective(objective_name, stat = "dummy")

Description :
This command add a scoreboard objective at datapack loading


get_function(folder=BCfolder, function_name="")

Description :
This command return the MCcommand "/function" wich target the file gived by the arguments


def execute(criteria, commands):

Description :
This command execute the commands with the criteria as /execute arguments


set_entity(
    entity_type="armor_stand",
    coords=["~", "~", "~"],
    tags=[],
    nbt="",
    scores={},
    commands=[])

Description :
This command summon an entity with some additions to the /summon command

take_score(target_entity="@s", target_objective="", aim_entity="@s", aim_objective = "")

Description :
This command return the MCcommand wich give to an entity the score of an other entity


while_loop(
    criteria="", folder=BCfolder, function_name="test", commands="", late_commands="")

Description :
This create a while loop in minecraft's mcfunctions : the commands are runned as long as the criteria is meet


for_loop(objectivename="", count=0, entity="@s",
    criteria="", folder=BCfolder, function_name="test", commands=[], late_commands="")

Description :
This create a for loop in minecraft's mcfunctions : the commands are runned the given count, and as long as the optional criteria is meet



## Syntax :

Bloccode instructions are made with preceding instructions
instructions are written as simple as possible in python language
The scripts you write are python scripts as well, don't worry, all the syntax you must know is described here

Type of syntax elements :

	“abcd” Quotations mark : 	String, it’s a list of character, used as text
 	used for all Minecraft commands to write
 	stackable : “a” + “b” == “ab”
 	/!\ Spaces in quotations matter : “ a “ != “a”
 	
	(a, b, c) Brackets : 			Bloccode functions arguments 
 	/!\ always required after a Bloccode's fuction name
 	
	[a, b, c] Square Brackets : 	List of elements 
 	used as argument and outputted by most Bloccode functions
 	stackable : [a, b] + [c, d] == [a, b, c, d]
 	/!\ In bloccode, elements are always strings : [“a”, “b”]
 	      Don’t make list of list : [a, b] , [c, d] will raise exceptions
 	
	{a : A, b : B, c : C} Braces :	dictionary
 	no order : { a : A, b : B} == { b : B, a : A}
 	{key1 : value1, key2 : value2, … }
 	
	abcd    No Symbol	:		Values names
 	used for functions arguments in bloccode, it’s the base of programming
 	/!\ Missing quotations mark are interpreted as values
