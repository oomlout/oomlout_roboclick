import os
import copy

def main(**kwargs):

    commit_to_git = False
    #commit_to_git = True

    #clone or pull oomlout_oompbuilder into temporary/oomlout_oomp_builder
    repo_url = "https://github.com/oomlout/oomlout_oomp_builder"
    repo_dir = "temporary\\oomlout_oomp_builder"
    if not os.path.exists(repo_dir):
        os.system(f"git clone {repo_url} {repo_dir}")
    else:
        os.system(f"cd {repo_dir} && git pull")

    #check the configuration directory exists and isn't empty
    config_dir = "configuration"
    if not os.path.exists(config_dir) or not os.listdir(config_dir):
        input("Configuration directory is empty or doesn't exist. Press enter to continue to copy default build configuration")
        #copy the default build configuration to the configuration directory in windows
        command = f"copy {repo_dir}\\configuration {config_dir}"
        print(command)
        os.system(command)
        
    

    
    
    #import run.py from the cloned repo
    import sys
    sys.path.append(repo_dir)
    import run
    run.main(**kwargs)

    if commit_to_git:
        os.system("git add .")
        os.system('git commit -m "Build OOMP parts using oomlout_oomp_builder"')
        os.system("git push")



if __name__ == '__main__':
    #add args parse and add a filter -f option
    import argparse
    parser = argparse.ArgumentParser(description="Build OOMP parts using oomlout_oomp_builder.")
    parser.add_argument('-f', '--filter', default="", type=str, help="Filter for the build process.")
    args = parser.parse_args()
    #convert args to kwargs
    kwargs = copy.deepcopy(vars(args))
    print(f"kwargs: {kwargs}")
    #kwargs = {}
    main(**kwargs)