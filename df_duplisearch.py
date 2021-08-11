import df_diagnosipack_base as base
from importlib import reload


# ====== main function =================================================================================================

def duplisearch_main(raw_path, uof, output_path, name_mode):
    # uof for "use output file"

    # reloads the base module, so e.g. top_level_objects is reset
    reload(base)

    # initializes the output file stuff
    if uof:
        base.initialize_output_file("/df_duplisearch_output.txt", output_path, raw_path)

    # initiates some variables
    objects_by_type_and_id = {}
    object_count = {object_type: 0
                    for object_type in
                    # this just flattens the list of object_types.values()
                    [val for sublist in base.object_types.values() for val in sublist]}
    objects_by_names = {}
    dup_num = 0
    name_dup_num = 0

    # finds the raw files
    rawfilenames = []
    for filename in base.os.listdir(raw_path):
        if filename.endswith(".txt"):
            rawfilenames.append(filename)

    # goes through all the raw files and finds the objects, puts them in objects_by_type_and_id.
    for i in range(len(rawfilenames)):
        # opens the file and splits it into tokens
        print("reading file " + str(i + 1) + "/" + str(len(rawfilenames)), rawfilenames[i])
        filename = rawfilenames[i]
        rawfile = open(raw_path + "/" + filename, "r", encoding="latin1")
        rawfile_tokens = base.split_file_into_tokens(rawfile)

        # initially it doesn't know what object types to expect
        # and it has to know, because e.g. "COLOR" is both an object type and a common token elsewhere.
        pos_object_types = []

        reading_object = False
        object_token_list = None
        object_id = None
        object_type = None

        # goes through all tokens
        for j in range(len(rawfile_tokens)):
            token = rawfile_tokens[j]
            # the "OBJECT" token tells it what object types to expect
            if token[0] == "OBJECT":
                pos_object_types = base.object_types[token[1]]

            # if it finds a new object
            elif token[0] in pos_object_types or j == len(rawfile_tokens) - 1:
                # finishes the current object before starting to read the next one
                if reading_object:

                    if object_type == "CREATURE":
                        top_level_object = base.Creature(object_id, object_token_list, filename)
                    elif object_type == "PLANT":
                        top_level_object = base.Plant(object_id, object_token_list, filename)
                    elif object_type == "TISSUE_TEMPLATE":
                        # Note: the tissue templates are loaded as Tissue objects for easier handling later
                        top_level_object = base.Tissue(object_id, object_token_list, filename)
                    else:
                        top_level_object = base.RawObject(object_id, object_token_list, filename)

                    if (object_type, object_id) in objects_by_type_and_id:
                        objects_by_type_and_id[(object_type, object_id)].append(top_level_object)
                    else:
                        objects_by_type_and_id[(object_type, object_id)] = [top_level_object]

                    # So that Creature.unpack_creature_variations() may still work
                    if object_type in ["CREATURE", "CREATURE_VARIATION"]:
                        base.top_level_objects[object_type][object_id] = top_level_object

                    # counts the object
                    if object_type in pos_object_types:
                        object_count[object_type] += 1

                if token[0] in pos_object_types:
                    object_type = token[0]
                    object_id = token[1]
                    object_token_list = []
                    reading_object = True

            elif reading_object:
                object_token_list.append(token)

        print(sum(object_count.values()), "objects found.")

    # goes through all objects to look for duplicated names, if name mode is on
    if name_mode:
        for object_key in objects_by_type_and_id:

            # unpacks creature variations
            if object_key[0] == "CREATURE":
                for c in objects_by_type_and_id[object_key]:
                    c.unpack_creature_variations()

            # fills objects_by_name
            for named_object_type in base.named_object_types:
                if object_key[0] == named_object_type:
                    for o in objects_by_type_and_id[object_key]:
                        name = o.get_last_token_value("NAME", ":".join(object_key) + " has no NAME token.")
                        if name is not False:

                            if (object_key[0], ":".join(name)) in objects_by_names:
                                objects_by_names[(object_key[0], ":".join(name))].append(o)
                            else:
                                objects_by_names[(object_key[0], ":".join(name))] = [o]
    # if any were detected during c.unpack_creature_variations()
    base.report_missing_top_level_objects("CREATURE_VARIATION", uof)
    base.report_missing_top_level_objects("CREATURE", uof)

    # print general info
    for object_type in object_count:
        base.double_print(object_type + ": " + str(object_count[object_type]), uof)
    base.double_print(str(sum(object_count.values())) + " objects found in total.", uof)

    # print duplications
    for object_key in objects_by_type_and_id:
        # i.e. if there's a duplication
        if len(objects_by_type_and_id[object_key]) > 1:
            base.double_print("Found " + str(len(objects_by_type_and_id[object_key])) + " instances of " +
                              ":".join(object_key)
                              + ";\n in " + ", ".join([dup_object.source_file_name for dup_object
                                                       in objects_by_type_and_id[object_key]]) + ".", uof)
            dup_num += 1

    if name_mode:
        for name_key in objects_by_names:
            if len(objects_by_names[name_key]) > 1:
                base.double_print(
                    "Found " + str(len(objects_by_names[name_key])) + " " + name_key[0] + " objects named \"" +
                    name_key[1] + "\";\n in " + ", ".join([dup_object.source_file_name for dup_object
                                                           in objects_by_names[name_key]]) + ".", uof)
                name_dup_num += 1
        base.double_print(str(dup_num) + " duplicated raw entries found.\n" +
                          str(name_dup_num) + " duplicated object names found.", uof)
    else:
        base.double_print(str(dup_num) + " duplicated raw entries found.\n", uof)

    # finalizes and closes output file
    base.close_output_file(uof)

    input("Done.\n Press enter to kill. >>")


if __name__ == "__main__":
    # settings
    raw_path = base.os.getcwd() + "/raw/objects/"
    use_output_file = True
    output_path = base.os.getcwd()
    name_mode = True

    duplisearch_main(raw_path, use_output_file, output_path, name_mode)
