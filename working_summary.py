import oomlout_ai_roboclick
import os


def main(**kwargs):
    pass

    

    # Set the directory for parts55 15262

    #mode = "all"
    #mode = "ai"
    #mode = "corel"
    mode = "summary"
    kwargs["mode"] = mode

    #filt = "sticker_sheet"
    filt = ""
    kwargs["filter"] = filt


    directory = kwargs.get("directory", "parts")
    kwargs["directory"] = directory
    if True:        
        
        if "all" in mode or "ai" in mode:
            mode = "oomlout_ai_roboclick"
            kwargs["mode"] = mode
            oomlout_ai_roboclick.main(**kwargs)

        if "corel" in mode or "all" in mode:
            mode = "oomlout_corel_roboclick"
            kwargs["mode"] = mode
            oomlout_ai_roboclick.main(**kwargs)

            for i in range(1, 10):
                mode = f"oomlout_corel_roboclick_{i}"
                kwargs["mode"] = mode
                oomlout_ai_roboclick.main(**kwargs)
       
        if "summary" in mode or "all" in mode:
            #go through the parts directory and put all the trace.pdf files in a folder with "sticker" in its name into a single pdf output\sticker_trace_summarry.pdf
            
            summaries = []
            summaries.append("")
            

            summaries_filters = kwargs.get("summaries_filters", None)


            filters = []
            if summaries_filters is not None:
                filters = summaries_filters
            else:
                filters.append(["","all"])
            #dates
            if False:
                #go through all the folders in parts and extract the date portion from helen_school_spelling_forced_spelling_word_unicorns_word_11_september_2025_date
                folders = os.listdir("parts")
                dates = []
                for folder in folders:
                    #each folder is of this format helen_school_spelling_forced_spelling_word_unicorns_word_11_september_2025_date
                    #extract 11_september_2025_date
                    parts = folder.split("_")
                    
                    if len(parts) > 4:
                        date_part = "_".join(parts[-4:])
                        if date_part not in dates:
                            dates.append(date_part)
                for date in dates:
                    filters.append([date, date])


            summary_filenames = []
            summary_filenames.append("working.pdf")
            #summary_filenames.append("initial_generated_card_multiple.pdf")

            for filt in filters:
                filt_main = filt[0]
                filt_directory = filt[1]
                for sum in summaries:
                    for summary_filename in summary_filenames:
                        print(f"Creating summary for {sum} with filter {filt}")
                        folder = f"parts"
                        files = []
                        # loop through the parts directory and find all files with "sticker" in their name
                        #check if directory exists
                        if not os.path.exists(folder):
                            print(f"Directory {folder} does not exist")
                            continue                        
                        folders = os.listdir(folder)
                        for folder in folders:
                            if sum in folder and filt_main in folder:
                                # loop through the files in the folder
                                file_name = os.path.join(folder, summary_filename)
                                #add parts to filename
                                file_name = os.path.join("parts", file_name)
                                #make absolute
                                file_name = os.path.abspath(file_name)
                                if os.path.exists(file_name):
                                    files.append(file_name)
                                    print(".", end="", flush=True)
                        print("")
                        print(f"    Found {len(files)} files for {sum}")
                        # create a pdf file with all the files in it using PyPDF2
                        from PyPDF2 import PdfMerger
                        merger = PdfMerger()
                        dir_local = f"output\\summary\\{filt_directory}\\{sum}\\{summary_filename.split('.')[0]}\\"
                        dir_local_source = f"{dir_local}\\source"
                        os.makedirs(dir_local_source, exist_ok=True)
                        os.makedirs(dir_local, exist_ok=True)
                        for file in files:
                            merger.append(file)
                            file_source = file
                            #last directory
                            last_dir = os.path.basename(os.path.dirname(file))
                            file_destination = f"{dir_local_source}\\{last_dir}_trace.pdf"
                            
                            #copy the file to the source folder
                            import shutil
                            shutil.copy(file_source, file_destination)
                        file_name_output = f"{dir_local}\\summary.pdf"
                        merger.write(file_name_output)
                        merger.close()
                    






if __name__ == "__main__":
    kwargs = {}
    directory = "parts"
    directory = os.path.abspath(directory)
    kwargs["directory"] = directory
    # run the function
    main(**kwargs)  