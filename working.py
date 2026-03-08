import oom_markdown
import os
import argparse

import robo
import working_helper

#process
#  locations set in working_parts.ods 
#  export to working_parts.csv
#  put components on the right side of the board
#  run this script

def main(**kwargs):
    pass
    

    #make_readme(**kwargs)
    #working_helper.run_utility(**kwargs)
    
    
   #ai_stuff
    if True:
        import working_oomp
        working_oomp.main(**kwargs)
        kwargs["mode"] = "all"
        working_helper.run_robo_ai(**kwargs)


    #summary
    if True:
        import working_summary
        summaries_filters = []
        summaries_filters.append(["","all"])
        kwargs["summaries_filters"] = summaries_filters
        working_summary.main(**kwargs)
        
        

def make_readme(**kwargs):
    os.system("generate_resolution.bat")
    oom_markdown.generate_readme_project(**kwargs)
    #oom_markdown.generate_readme_teardown(**kwargs)


if __name__ == '__main__':
    # parse arguments
    argparser = argparse.ArgumentParser(description='project description')
    #--file_input -fi
    argparser.add_argument('--file_input', '-fi', type=str, default='', help='file_input')    
    args = argparser.parse_args()
    kwargs = {}
    # update kwargs with args
    kwargs.update(vars(args))

    
    
    
    
    main(**kwargs)