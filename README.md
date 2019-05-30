# BlocCode
Scripting language for Minecraft datapacks

## Bloccode documentation :

### writed_folder(folder = <folder/path , function_name = <mcfuction_name>)
Choose the mcfunction where the next commands will be writed

#### Arguments :
•	folder : The subfolder of the mcfunction
 	default value : last used folder
 	
•	function _name : The name of the mcfunction
 	
•	tag_function(optional) : “load” or “tick”
“load” make the mcfunction run at datapack loading 
“tick”  make the mcfunction run at each game ticks
#### Examples :
writed_folder(folder = "default" , function _name = "test")     
writed_folder(folder = "default" , function _name = "test" , tag_function = "load")




### write(Commands)
Write commands of the list in the mcfunction selected by the writed_folder command

#### Arguments :	
•	a list of correct minecraft commands : 	[“command 1”, “command 2”]
or a single command : 			“command”

#### Examples :
write("a command")  
write(["command","secondcommand","other command"])




### write_in(commands = [Command list], temp_folder = folder/path , function_name = mcfuction_name)
Write the commands in the asked mcfunction without changing the writed_folder selected mcfunction

#### Arguments :	just like write and writed_folder combined
•	a list of correct minecraft commands : 	[“command 1”, “command 2”]
or a single command : 			“command”


•	folder : The subfolder of the mcfunction
 	default value : last used folder
•	function_name : The name of the mcfunction

•	tag_function(optional) : “load” or “tick”
 	 “load” makes the mcfunction run at datapack loading 
 	“tick”  makes the mcfunction run at each game ticks
 	
•	commands : the commands to write in


#### Examples :
write_in(commands = ["command", "other command"], folder = "default" , function_name = "test"})     




### new_objective(objective_name)
Create the new objective at datapack loading with the scoreboard command
Arguments : objective_name : a name of Minecraft objective
Examples :
new_objective(”objective_name”)




### get_function(folder = folder, function_name = funct_name)
Return the Minecraft /function command which target the selected mcfunction

#### Arguments :
•	folder : The subfolder of the mcfunction
 	default value : last used folder
 	
•	function_name : The name of the mcfunction


#### Examples :
get_function(folder = “folder/path”, function_name = “a_function_name”)

keep in mind All command's list can be replaced by functions outputting other command's list





### execute(criterias = criterias, commands = commands)
Add the execute criteria to the command’s list

#### Arguments :
•	criterias : a /execute valid argument such as “at”, “as”, “if” . . . 
•	commands : a list of MCcommands or a Bloccode function returning command’s

#### Output :
the same list with “execute” the criterias and the commands
#### Examples :
execute("at @a", ["say hello world","say hi"])
execute("as @e[tag=snake] if score @s objective = @s other_objective”, 
              ["say hello world", "say hi @s"])




### set_entity(entity_type =”entityname”, coords = ["X","Y","Z"],
tags = ["a","b","c"],nbt = <”nbt_tag:1b”>,scores = {"obj1":1,"obj2":2},            commands = [<Command list>]})
Summon an entity with the requested position, tags, score, NBT and trigger the commands on it
#### Arguments : (all optionals)
•	entity_type : 	entity summoned
 	default : armor_stand
 	
•	coords : 	a list of xyz cords, can be absolute, relative “~” or “^” 
 	default : [“~”,“~”,“~”]
 	
•	tags : 		list of tags to add to the entity

•	nbt :		nbt to add to the entity

•	scores : 	{“objective_name”: score, …}

•	commands :	the so used command’s list

#### Examples :
set_entity(entity_type = "zombie", coords = ["0","~","~"], tags = ["a","b","c"], 
           nbt = "NoAi:1b",scores = {"obj1":1,"obj2":2}, commands = ["say hi"])




### while_loop(criteria = "if entity @e[limit=1]", folder = "default", funct_name = "test", commands = "an effective command", late_commands = "this runs after the loop")
Will run the commands as long as the criteria is meet
#### Arguments :	
•	criteria
•	a list of correct minecraft commands : 	[“command 1”, “command 2”]
or a single command : 			“command”




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
