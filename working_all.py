import oom_markdown
import os
import argparse
import robo
import working_helper
#process
#  locations set in working_parts.ods 
#  export to working_parts.csvhe best letrence_ doside of the board
#  run this script

def main(**kwargs):
    print("Starting working_all")    
    import working_oomp
    print("Starting working_oomp")
    working_oomp.main(**kwargs)
    
    
    #do ai work
    import working
    if True:
        print("Starting working")
        kwargs["mode"] = "ai"
        filters = ["research", ""]
        #filters = ["zzzzzz"]

        for filt in filters:
            kwargs["filter"] = filt        
            working.main(**kwargs)
    
    
    
    if True:
        print("Starting working corel")
        kwargs["mode"] = "corel"
        #filters = ["medication", ""]
        filters = [""]

        for filt in filters:
            kwargs["filter"] = filt        
            working.main(**kwargs)
    
    
    #summary 
    if True:
        print("Starting working summary")   
        import working_summary
        print("Starting working_summary")
        working_summary.main(**kwargs)


        



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