import os
import datetime
import traceback
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image
# tool modules
from df_duplisearch import duplisearch_main
from df_creatureclasser import creatureclasser_main
from df_cvunpack import cvunpack_main
from df_creaturescale import creaturescale_main

# so it's easier to add/shuffle around the settings
RAW_PATH_SETTING = 0
USE_OUTPUT_FILE_SETTING = 1
OUTPUT_PATH_SETTING = 2
USE_NAME_MODE_SETTING = 3
VERY_DETAILED_WEIGHTS_SETTING = 4


def show_and_print_error(tool_name, error, traceback_string):
    print("Exited " + tool_name + " due to error.")
    errorlog_file = open(output_path + "/df_diagnosipack_errorlog.txt", "a")
    errorlog_file.write("Error using " + tool_name + " " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + " :\n")
    errorlog_file.write(traceback_string + "\n")
    # uses "warning" icon instead of "error" icon because "error" makes a much more stressful sound,
    # and most errors are not that bad, just caused by hickups in the raws
    messagebox.showinfo(message="Error while running " + tool_name + ".\n\n" + str(error) + "\n\n" + traceback_string,
                        title="Error - " + tool_name, icon='warning')


# ====== Widget commands ===============================================================================================

def diagnosipack_help_button_command():
    messagebox.showinfo(message='DF Diagnosipack 1.1.3\nVoliol 2021\nDF Diagnosipack is a collection of modding tools '
                                'for Dwarf Fortress, with a focus on diagnosing problems and getting statistics on what'
                                ' is found within the raws. The tools in DF Diagnosipack were made (and tested) with '
                                'DF 0.47 in mind, but should work on most earlier versions as well.',
                        title="Help - DF Diagnosipack")


# settings commands

def raw_path_browse_button_command():
    dir_name = filedialog.askdirectory()
    # couldn't find another easy way to just clear the entry
    raw_path_entry.delete(0, 10000)
    raw_path_entry.insert(0, dir_name)


def output_path_browse_button_command():
    dir_name = filedialog.askdirectory()
    # couldn't find another easy way to just clear the entry
    output_path_entry.delete(0, 10000)
    output_path_entry.insert(0, dir_name)


def update_settings_button_command():
    global raw_path_setting, use_output_file, output_path_setting, use_name_mode, very_detailed_weights
    global raw_path, output_path
    # updates the entry settings
    raw_path_setting = raw_path_entry.get()
    use_output_file = use_output_file_var.get()
    output_path_setting = output_path_entry.get()
    use_name_mode = use_name_mode_var.get()
    very_detailed_weights = very_detailed_weights_var.get()
    # and their "real" counterparts
    raw_path = raw_path_setting.replace("[HERE]", os.getcwd())
    output_path = output_path_setting.replace("[HERE]", os.getcwd())
    # updates the settings array to write the file
    settings[RAW_PATH_SETTING] = "Raw folder path: " + raw_path_setting.strip()
    settings[USE_OUTPUT_FILE_SETTING] = "Create .txt file output: " + str(use_output_file).capitalize()
    settings[OUTPUT_PATH_SETTING] = "Output folder path: " + output_path_setting.strip()
    settings[USE_NAME_MODE_SETTING] = "Use \"name mode\" on DF Duplisearch: " + str(use_name_mode).capitalize()
    settings[VERY_DETAILED_WEIGHTS_SETTING] = "DF Creaturescale gives very detailed output: " + \
                                              str(very_detailed_weights).capitalize()
    # clears then writes the settings file
    temp_settings_file = open("df_diagnosipack_settings.txt", "w")
    temp_settings_file.write("\n".join(settings))
    temp_settings_file.close()


def update_settings_help_button_command():
    messagebox.showinfo(message='Click the button to update the settings, and have them be used by the tools.'
                                'Make sure to click it each time you make a change to the settings.\n\n'
                                'For the raw path, select a folder directly containing the raw files, such as a '
                                '/raws/objects folder.\n'
                                '"[HERE]" can be used as a shorthand to note the directory DF Duplisearch is running '
                                'from.',
                        title="Help - Settings")


# tool commands:

def duplisearch_button_command():
    print("Running DF Duplisearch...")
    # so errors in the tools don't crash diagnosipack
    try:
        duplisearch_main(raw_path, use_output_file, output_path, use_name_mode)
    except Exception as error:
        traceback_string = traceback.format_exc()
        show_and_print_error("DF Duplisearch", error, traceback_string)


def duplisearch_help_button_command():
    messagebox.showinfo(message='DF Duplisearch 1.3\nVoliol 2020-2021\n'
                                'DF Duplisearch checks the raws for duplicated objects. '
                                'It also counts the instances of each object type (CREATURE, ENTITY, etc. etc.). ' 
                                'Useful for merging mods, or visualizing the size of your mods compared to '
                                'vanilla (and other mods).\n\n'
                                'Duplicated objects, or simply objects sharing the same ID regardless of their origin, '
                                'lead to so-called "duplication errors" jumbling the game around; see the DF wiki for '
                                'more info why you don\'t want them.\n\n'
                                'If "name_mode" is on DF duplisearch will show "duplicated names". ' 
                                'These are the in-game names (e.g "tiger:tigers:tiger" from "CREATURE:TIGER"), and so '
                                'they don\'t cause duplication errors, but can still be confusing to the player.\n'
                                'Note that some vanilla objects are recognized as "duplicated", i.e. skirt, '
                                'short skirt, long skirt.',
                        title="Help - DF Duplisearch")


def creatureclasser_button_command():
    print("Running DF Creatureclasser...")
    try:
        creatureclasser_main(raw_path, use_output_file, output_path)
    except Exception as error:
        traceback_string = traceback.format_exc()
        show_and_print_error("DF Creatureclasser", error, traceback_string)


def creatureclasser_help_button_command():
    messagebox.showinfo(message='DF Creatureclasser 1.1.1\nVoliol 2021\n'
                                'DF Creatureclasser tell you what creature classes there are in your raws, and what '
                                'they are used for. Useful for seeing which creature classes are underused, and '
                                'perhaps when merging mods.\n\n'
                                'Creature classes are arbitrary tags given to creatures. They can be used by other '
                                'objects to not have to specify each single creature of a large group, such as '
                                '"mammals". In DF 0.47, the following 10 tokens use creature classes:\n'
                                'Creature tokens - CREATURE_CLASS, GOBBLE_VERMIN_CLASS, SENSE_CREATURE_CLASS;\n'
                                'Interaction tokens - IT_AFFECTED_CLASS, IT_IMMUNE_CLASS;\n'
                                'Entity tokens - ANIMAL_CLASS, ANIMAL_FORBIDDEN_CLASS, ALLOWED_CLASS;\n'
                                'Syndrome tokens - SYN_AFFECTED_CLASS, SYN_IMMUNE_CLASS, CE_SENSE_CREATURE_CLASS.\n'
                                'See the DF wiki for more info on these.',
                        title="Help - DF Creatureclasser")


def cvunpack_button_command():
    print("Opening DF CVunpack...")
    try:
        cvunpack_main(raw_path, use_output_file, output_path)
    except Exception as error:
        traceback_string = traceback.format_exc()
        show_and_print_error("DF CVunpack", error, traceback_string)


def cvunpack_help_button_command():
    messagebox.showinfo(message='DF CVunpack 1.1\nVoliol 2021\n'
                                'DF CVunpack unpacks creature variations, so you can see how the raws for e.g. '
                                'wolf men *really* look (spoiler: they have 7 fingers). Its functionality came along '
                                'when I made a base for other tools (and the other tools *do* unpack CVs), '
                                'but found it nifty enough that it should be easily accessible for anyone using this '
                                'pack.',
                        title="Help - DF CVunpack")


def creaturescale_button_command():
    print("Running DF Creaturescale...")
    try:
        creaturescale_main(raw_path, use_output_file, output_path, very_detailed_weights)
    except Exception as error:
        traceback_string = traceback.format_exc()
        show_and_print_error("DF Creaturescale", error, traceback_string)


def creaturescale_help_button_command():
    messagebox.showinfo(message='DF Creaturescale 1.0\nVoliol 2021\n'
                                'A scale in the sense that it weighs creatures. '
                                'If you allow "very detailed weights" it also outputs their tissue composition, '
                                'and weights of specific body parts.\n\n'
                                'This is the most complex tool in this pack, but possibly the most inaccurate as well; '
                                'I do not know much about how weight is actually calculated in-game. '
                                'As an example of what could be an oddity, this tool claims male humanoids are lighter '
                                'than their female counterparts - because their beards have lower density than most '
                                'other tissues.',
                        title="Help - DF Creaturescale")


def andmore_button_command():
    messagebox.showinfo(message='Are there more tools? Mostly no. These are all the tools currently in this pack. '
                                ' However, these tools are built on a common base (df_diagnosipack_base.py), '
                                ' which can handle unpacking creature variants, body parts etc.. This base should '
                                'facilitate making a new tool, as those are the most annoying parts of the raws to'
                                ' deal with. '
                                'If you are acquainted with Python, consider giving it a try! '
                                '\n\n'
                                'With that in mind, I am not a professional programmer. If something confuses you about'
                                ' my code, ask me about it and I will explain as best as I can, and look at possible '
                                'adjustments for the next version of DF Diagnosipack. '
                                ' This is also an early version, so all parts needed for your specific tool may not '
                                'be provided. Creatures are pretty well supported, I think.'
                                '\nI am reachable on the Bay 12 forums.'
                                '\n\n//sincerely, Voliol, 2021-07-11 :)',
                        title="And more...?")


# ======================================================================================================================

# gets settings
settings_file = open("df_diagnosipack_settings.txt", "r")
settings = [wline for wline in settings_file]
raw_path_setting = settings[RAW_PATH_SETTING].replace("Raw folder path:", "").strip()
use_output_file = settings[USE_OUTPUT_FILE_SETTING].replace("Create .txt file output:", "").strip().lower() in \
                          ["yes", "y", "true", "1"]
output_path_setting = settings[OUTPUT_PATH_SETTING].replace("Output folder path:", "").strip()
use_name_mode = settings[USE_NAME_MODE_SETTING].replace("Use \"name mode\" on DF Duplisearch:", "").strip().lower() in \
                          ["yes", "y", "true", "1"]
very_detailed_weights = settings[VERY_DETAILED_WEIGHTS_SETTING].replace("DF Creaturescale gives very detailed output:",
                                                                        "").strip().lower() in ["yes", "y", "true", "1"]
settings_file.close()

# because these two can be formatted in the settings file, they have a separate settings variable and "true" variable
# that is actually passed to the sub-tools
# these two do not contain "[HERE]"
raw_path = raw_path_setting.replace("[HERE]", os.getcwd())
output_path = output_path_setting.replace("[HERE]", os.getcwd())

# ======================================================================================================================

# initializes the root window
root = tk.Tk()
root.title("DF Diagnosipack")
print("Welcome to DF Diagnosipack! Keep track of this console, all tools will run within it.")
root.iconbitmap(os.getcwd() + "//icon.ico")

# creates a mainframe+grid within the root
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# creates the option widgets
settings_frame = ttk.Labelframe(mainframe, text='Settings:')
settings_frame.grid(column=0, row=0, columnspan=3)

raw_path_label = ttk.Label(settings_frame, text='Raw folder path:')
raw_path_label.grid(column=0, row=0)
raw_path_entry = tk.Entry(settings_frame)
raw_path_entry.insert(0, raw_path_setting)
raw_path_entry.grid(column=1, row=0)
raw_path_browse_button = tk.Button(settings_frame, text='Browse', command=raw_path_browse_button_command)
raw_path_browse_button.grid(column=2, row=0, sticky=tk.W)

use_output_file_var = tk.BooleanVar(value=use_output_file)
use_output_file_cb = tk.Checkbutton(settings_frame, text='Create .txt file output',
                                    var=use_output_file_var,
                                    onvalue=True, offvalue=False)
use_output_file_cb.grid(column=1, row=1, columnspan=2)

output_path_label = ttk.Label(settings_frame, text='Output folder path:')
output_path_label.grid(column=0, row=2)
output_path_entry = tk.Entry(settings_frame)
output_path_entry.insert(0, output_path_setting)
output_path_entry.grid(column=1, row=2)
output_path_browse_button = tk.Button(settings_frame, text='Browse', command=output_path_browse_button_command)
output_path_browse_button.grid(column=2, row=2, sticky=tk.W)

use_name_mode_var = tk.BooleanVar(value=use_name_mode)
use_name_mode_cb = tk.Checkbutton(settings_frame, text='Use \"name mode\" on DF Duplisearch',
                                  var=use_name_mode_var,
                                  onvalue=True, offvalue=False)
use_name_mode_cb.grid(column=1, row=3, columnspan=2)

very_detailed_weights_var = tk.BooleanVar(value=very_detailed_weights)
very_detailed_weights_cb = tk.Checkbutton(settings_frame, text='DF Creaturescale gives very detailed output',
                                          var=very_detailed_weights_var,
                                          onvalue=True, offvalue=False)
very_detailed_weights_cb.grid(column=1, row=4, columnspan=2)

# update settings
tk.Button(mainframe, text="Update settings", command=update_settings_button_command).grid(column=0, row=1,
                                                                                          sticky=tk.E)
tk.Button(mainframe, text="?", command=update_settings_help_button_command).grid(column=1, row=1, sticky=tk.W)

# ------ Buttons for all the sub-tools -------

tools_frame = ttk.Labelframe(mainframe, text='Tools:')
tools_frame.grid(column=0, row=2)

tk.Button(tools_frame, text="DF Duplisearch", command=duplisearch_button_command).grid(column=0, row=0)
tk.Button(tools_frame, text="?", command=duplisearch_help_button_command).grid(column=1, row=0)
tk.Button(tools_frame, text="DF Creatureclasser", command=creatureclasser_button_command).grid(column=0, row=1)
tk.Button(tools_frame, text="?", command=creatureclasser_help_button_command).grid(column=1, row=1)
tk.Button(tools_frame, text="DF CVunpack", command=cvunpack_button_command).grid(column=0, row=2)
tk.Button(tools_frame, text="?", command=cvunpack_help_button_command).grid(column=1, row=2)
tk.Button(tools_frame, text="DF Creaturescale", command=creaturescale_button_command).grid(column=0, row=3)
tk.Button(tools_frame, text="?", command=creaturescale_help_button_command).grid(column=1, row=3)
tk.Button(tools_frame, text="And more...?", command=andmore_button_command).grid(column=2, row=0, padx=5)

# gets the logo image
image = ImageTk.PhotoImage(Image.open('logo.png'))
logo_label = ttk.Label(mainframe)
logo_label['image'] = image
logo_label.grid(column=1, row=2, sticky=(tk.S, tk.E))

tk.Button(mainframe, text="?", command=diagnosipack_help_button_command).grid(column=2, row=2, sticky=(tk.S, tk.W))

# runs the main loop
root.mainloop()
