import oomp
import copy

def main(**kwargs):
    load_parts(**kwargs)

def load_parts(**kwargs):
    make_files = kwargs.get("make_files", True)
    #print "loading parts" plus the module name get the module name from the filename using __name__
    print(f"  loading parts {__name__}")
    create_generic(**kwargs)

def create_generic(**kwargs):
    print(f"  loading parts from part_source")
    things = {}    
    
    #load parts from parts_source directory
    directory = "part_source"
    import os
    if not os.path.exists(directory):
        print(f"      directory {directory} does not exist, creating it")
        #create it
        os.makedirs(directory)
    for filename in os.listdir(directory):
        import yaml
        #go through directories and load working.yaml files
        # only load .yaml files
        if "working.yaml" in filename:
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
                for thing in data:
                    things[thing] = data[thing]

    default_empty = {}
    default_empty["classification"] = ""
    default_empty["type"] = ""
    default_empty["size"] = ""
    default_empty["color"] = ""
    default_empty["description_main"] = ""
    default_empty["description_extra"] = ""
    default_empty["manufacturer"] = ""
    default_empty["part_number"] = ""


    parts = []

    for thing in things:
        current = things[thing]                
        #name stuff
        part = copy.deepcopy(default_empty)
        part.update(current)
        part["name"] = thing
        part["name_space"] = thing.replace("_", " ")
        part["name_proper"] = part["name_space"].title()
        part["name_upper"] = part["name_space"].upper()
        
        
        

        #image
        if False:
            count = 1
            for prompt in prompts:
            #creating actions                
                actions = []
                action = {}
                #- command: 'new_chat'
                action["command"] = "new_chat"  
                action["description"] = f"rice image {current["name"]}"
                actions.append(action)
                #- command: 'query'
                    #text: 'can i get some pictures of tourist attractions in hx2 halifax uk, please ensure it is definietly in the uk and has the post code hx2?'
                action = {}
                action["command"] = "query"
                action["text"] = prompt
                action["delay"] = 60
                actions.append(action)
                
                action = {}
                #- command: 'save_image'
                action["command"] = "save_image_generated"  
                action["file_name"] = f"initial_generated_cgi.png"
                actions.append(action)


                #- command: 'add_image'
                action = {}
                action["command"] = "add_image"
                action["file_name"] = f"initial_generated_{count}.png"           
                actions.append(action)

                #close tab
                action = {}
                action["command"] = "close_tab"
                actions.append(action)

                base  = {}
                base["actions"] = copy.deepcopy(actions)
                file_test = f"initial_generated_{count}.png"
                base["file_test"] = file_test
                part[f"oomlout_ai_roboclick_{count}"] = base
                count += 1
        
        #trace
        if True:
            #trace file
            count = 1
        
            if True:
                actions = []

                #wait_for_file initial_generation.png
                action = {}
                action["command"] = "wait_for_file"
                action["file_name"] = f"initial_generated.png"                
                actions.append(copy.deepcopy(action))

                action = {}
                action["command"] = "corel_trace_full"
                action["file_source"] = f"template\\working\\working.cdr"
                action["file_source_trace"] = f"initial_generated.png"
                action["file_destination"] = f"trace.cdr"
                action["max_dimension"] = 280
                action["remove_background_color_from_entire_image"] = True
                action["number_of_colors"] = 2
                #cordinates 31,50
                action["x"] = 105
                action["y"] = 297/2
                actions.append(copy.deepcopy(action))
                
                base  = {}
                base["actions"] = copy.deepcopy(actions)
                #the file that is created so skips if done
                file_test = f"trace.png"
                base["file_test"] = file_test
                part["oomlout_corel_roboclick_1"] = base

        #trace
                

        
        
        parts.append(part)
    



    oomp.add_parts(parts, **kwargs)

    #dd file copy
    for part in parts:
        file_copies = part.get("file_copy", [])
        if file_copies != []:
            for file_copy in file_copies:
                directory = part.get("directory", "")
                if directory != "":
                    file_source = f"{file_copy["file_source"]}"
                    file_destination = f"{directory}\\{file_copy["file_destination"]}"
                    import shutil
                    print(f"      copying {file_source} to {file_destination}")
                    try:
                        shutil.copyfile(file_source, file_destination)
                    except Exception as e:
                        print(f"      error copying file: {e}") 

    import time
    time.sleep(2)


if __name__ == "__main__":
    # run the function
    load_parts()    
    