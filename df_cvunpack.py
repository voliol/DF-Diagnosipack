import df_diagnosipack_base as base
from importlib import reload


# ====== main function =================================================================================================

def cvunpack_main(raw_path, uof, output_path):
    # uof for "use output file"

    # reloads the base module, so e.g. top_level_objects is reset
    reload(base)

    # asks if you want to abort
    if uof:
        if input("Running this tool will generate a possibly very large text file. Due to this tool being new, "
                 "I can't guarantee the output to be perfect. Do you wish to proceed? "
                 "(Y/N) ").lower() not in ["yes", "y", "sure"]:
            input("Understood.\nPress enter to kill. >>")
            return False
    else:
        if input("It is highly advised to allow file output while using this tool. Due to this tool being new, "
                 "I can't guarantee the output to be perfect. Do you still wish to proceed? "
                 "(Y/N) ").lower() not in ["yes", "y", "sure"]:
            input("Understood.\nPress enter to kill. >>")
            return False
    print("Running DF CVunpack...")

    # initializes the output file stuff
    if uof:
        base.initialize_output_file("/df_cvunpack_output.txt", output_path, raw_path)

    # reads and loads all raw files
    base.read_and_load_all_raw_files(raw_path)

    # unpacks creature variations
    print("unpacking creature variations...")
    for c in base.top_level_objects["CREATURE"].values():
        c.unpack_creature_variations()

    base.report_missing_top_level_objects("CREATURE_VARIATION", uof)
    base.report_missing_top_level_objects("CREATURE", uof)

    # goes through all creatures and prints them
    object_ids = list(base.top_level_objects["CREATURE"].keys())
    for i in range(len(object_ids)):
        object_id = object_ids[i]
        print("printing creature " + str(i + 1) + "/" + str(len(object_ids)), object_id)
        c = base.top_level_objects["CREATURE"][object_id]

        base.either_print("\n[CREATURE:" + object_id + "]", uof)
        for token in c.tokens:
            base.either_print("\t[" + ":".join(token) + "]", uof)

    # and finally closes the output file
    base.close_output_file(uof)

    input("Done.\nPress enter to kill. >>")


if __name__ == "__main__":
    # settings
    raw_path = base.os.getcwd() + "/raw/objects"
    use_output_file = True
    output_path = base.os.getcwd()

    cvunpack_main(raw_path, use_output_file, output_path)
