import robo
import os

def run_robo_ai(**kwargs):
    import oomlout_ai_roboclick
    pass

    

    # Set the directory for parts
    directory = kwargs.get("directory", "parts")
    
    kwargs["directory"] = directory
    # Set the mode
    # Set the mode
    
    
    mod = "all"
    #mod = "ai"
    #mod = "corel"

    mod2 = kwargs.get("mode", mod)

    kwargs["mode"] = mod2
    mod = mod2
    #mode = "oomlout_ai_roboclick"
    #mode = "oomlout_corel_roboclick"                            
    #filt = "sticker_sheet"
    #filt = "postcard"
    #filt = "sticker"
    #filt = "stamp"

    
    #filt = "postcard_regional_united_kingdom_wales_swansea_sa68_dance_camp_wales"

    #filt = ""
    #kwargs["filter"] = filt


    directory = kwargs.get("directory", "parts")
    kwargs["directory"] = directory
    if True:        
        
        if "all" in mod or "ai" in mod:
            
            mode = "oomlout_ai_roboclick"
            kwargs["mode"] = mode
            oomlout_ai_roboclick.main(**kwargs)

        if "corel" in mod or "all" in mod:
            mode = "oomlout_corel_roboclick"
            kwargs["mode"] = mode
            oomlout_ai_roboclick.main(**kwargs)

            
           
def run_utility(**kwargs):
    jobs = []

    job = {}
    job["file_output"] = 'working_oomlout_organizing_paper_divider_binder.svg'
    job['utility'] = 'oomlout_utility_text_search_and_replace_jinja'
    job["command_line_args"] = {}
    job["command_line_args"]['directory_iterative'] = 'parts'
    job["command_line_args"]['file_output'] = job["file_output"]
    template = {}
    template['repo'] = 'oomlout_organizing_paper_divider_binder'
    template['path'] = 'template\\template_1'
    job["template"] = template
    #jobs.append(job)

    job = {}    
    job['utility'] = 'oomlout_utility_image_tile_collage'    
    #directory_iterative
    job["directory_iterative"] = 'parts'
    #photo["file_image_source"] = "working.png"
    #load_working_yaml
    job["load_working_yaml"] = True
    job["command_line_args"] = {}
    job["command_line_args"]['directory_iterative'] = 'parts'
    #job["command_line_args"]['file_output'] = job["file_output"]
    job["command_line_args"]['load_working_yaml'] = True
    jobs.append(job)

    for job in jobs:
        #clone to c:\gh if folder doesnt exist
        utility = job['utility']
        file_output = job.get('file_output', '')
        command_line_args = job.get('command_line_args', {})
        template = job.get('template', None)
        if template is not None:
            template_repo = template['repo']
            template_path = template['path']

        path_utility = f"c:\\gh\\{utility}\\working.py"
        if template is not None:
            path_template = f"c:\\gh\\{template_repo}\\{template_path}"
            extension = os.path.splitext(file_output)[1]
            file_template = f"{path_template}\\working.{extension.lstrip('.')}"
            command_line_args['file_template'] = file_template
        #get repos in
        if True:
            robo.robo_git_clone_repo(repo=utility)
            if template is not None:
                robo.robo_git_clone_repo(repo=template_repo)
        
        #build the call
        if True:
            #mode = "command_line"
            mode = "python"
            if mode == "command_line":
                command_line = f'python "{path_utility}"'
                for key, value in command_line_args.items():
                    command_line += f' --{key} "{value}"'
                print(command_line)
                os.system(command_line)
            elif mode == "python":
                #import the file c:gh\gh\{utility}\working.py and run main using jobs as kwarg
                import importlib.util
                spec = importlib.util.spec_from_file_location("working_module", path_utility)
                working_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(working_module)
                working_module.main(**job)

                
                


        #get tempalte repo in
        
        

