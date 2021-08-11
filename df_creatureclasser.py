import df_diagnosipack_base as base
from importlib import reload


# ====== main function =================================================================================================

def creatureclasser_main(raw_path, uof, output_path):
    # uof for "use output file"

    # reloads the base module, so e.g. top_level_objects is reset
    reload(base)

    # initializes the output file stuff
    if uof:
        base.initialize_output_file("/df_creatureclasser_output.txt", output_path, raw_path)

    # initiates some variables
    creature_class_tokens = ["CREATURE_CLASS", "GOBBLE_VERMIN_CLASS", "SENSE_CREATURE_CLASS",
                             "IT_AFFECTED_CLASS", "IT_IMMUNE_CLASS",
                             "ANIMAL_CLASS", "ANIMAL_FORBIDDEN_CLASS", "ALLOWED_CLASS",
                             "SYN_AFFECTED_CLASS", "SYN_IMMUNE_CLASS", "CE_SENSE_CREATURE_CLASS"]
    creature_classes = {}

    # reads and loads all raw files
    base.read_and_load_all_raw_files(raw_path)

    # unpacks creature variations so e.g. giant creatures and animal men work
    for c in base.top_level_objects["CREATURE"].values():
        c.unpack_creature_variations()
    print("")
    base.report_missing_top_level_objects("CREATURE_VARIATION", uof)
    base.report_missing_top_level_objects("CREATURE", uof)

    # goes through all objects
    for object_type in base.top_level_objects:
        for o in base.top_level_objects[object_type].values():
            for token in o.tokens:

                # creatures, ...
                if object_type == "CREATURE" and \
                        token[0] in ["CREATURE_CLASS", "GOBBLE_VERMIN_CLASS", "SENSE_CREATURE_CLASS"]:
                    # adds the creature class to creature_classes if it weren't already there
                    if token[1] not in creature_classes:
                        creature_classes[token[1]] = {cc_token: [] for cc_token in creature_class_tokens}
                    # adds the instance of the token being used
                    creature_classes[token[1]][token[0]].append(object_type + ":" + o.object_id)

                # ...interactions,
                elif object_type == "INTERACTIONS" and \
                        token[0] in ["IT_AFFECTED_CLASS", "IT_IMMUNE_CLASS"]:
                    if token[1] not in creature_classes:
                        creature_classes[token[1]] = {cc_token: [] for cc_token in creature_class_tokens}
                    creature_classes[token[1]][token[0]].append(object_type + ":" + o.object_id)

                # ...and entities have unique creature class tokens
                elif object_type == "ENTITY" and \
                        token[0] in ["ANIMAL_CLASS", "ANIMAL_FORBIDDEN_CLASS", "ALLOWED_CLASS"]:
                    if token[1] not in creature_classes:
                        creature_classes[token[1]] = {cc_token: [] for cc_token in creature_class_tokens}
                    creature_classes[token[1]][token[0]].append(object_type + ":" + o.object_id)

                # and then just about anything can contain an syndrome and have the syndrome-related tokens in them
                elif token[0] in ["SYN_AFFECTED_CLASS", "SYN_IMMUNE_CLASS", "CE_SENSE_CREATURE_CLASS"]:
                    if token[1] not in creature_classes:
                        creature_classes[token[1]] = {cc_token: [] for cc_token in creature_class_tokens}
                    creature_classes[token[1]][token[0]].append(object_type + ":" + o.object_id)

    base.double_print("\nOverview:", uof)
    # print general info
    for cc in creature_classes:
        base.double_print(cc, uof)
        for cc_token in creature_classes[cc]:
            if len(creature_classes[cc][cc_token]) != 0:
                base.double_print("\t" + cc_token + "\t(occurrences:" + str(len(creature_classes[cc][cc_token])) + ")",
                                  uof)
        base.double_print("", uof)

    # flushes
    base.flush_output_file(uof)
    input("\nPress enter for more detailed output. >>")
    base.double_print("\n--Detailed output:--\n\n", uof)

    # print detailed info
    for cc in creature_classes:
        base.double_print(cc, uof)
        for cc_token in creature_classes[cc]:
            if len(creature_classes[cc][cc_token]) != 0:
                base.double_print("\t" + cc_token + "\t(occurrences:" + str(len(creature_classes[cc][cc_token])) + ")",
                                  uof)
                for obj in creature_classes[cc][cc_token]:
                    base.double_print("\t\t" + obj, uof)
        base.double_print("", uof)

    base.close_output_file(uof)

    input("Done.\nPress enter to kill. >>")


if __name__ == "__main__":
    # settings
    raw_path = base.os.getcwd() + "/raw/objects"
    use_output_file = True
    output_path = base.os.getcwd()

    creatureclasser_main(raw_path, use_output_file, output_path)
