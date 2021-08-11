import df_diagnosipack_base as base
from importlib import reload


# ====== misc functions ================================================================================================

def grams_to_string(a):
    if a < 100:
        return str(round(a, 3)) + " g"
    elif 100 <= a <= 1000000:
        return str(round(a/1000, 3)) + " kg"
    else:
        return str(round(a/1000000, 6)) + " tons"


# ====== main function =================================================================================================

def creaturescale_main(raw_path, uof, output_path, very_detailed_weights):
    # uof for "use output file"

    # reloads the base module, so e.g. top_level_objects is reset
    reload(base)

    # initiates some variables
    heaviest_castes = [[["NO_CREATURE", "NO_CASTE"], 0] for i in range(25)]

    # initializes the output file stuff
    if uof:
        base.initialize_output_file("/df_creaturescale_output.txt", output_path, raw_path)

    # gets "top level objects"
    # top level objects are objects defined at the top level, i.e. not defined within other objects.
    # creatures and tissue templates are top level objects, tissues and syndromes are not.
    # reads and loads all raw files, filling top_level_objects
    base.read_and_load_all_raw_files(raw_path)

    # goes through all creatures
    object_ids = list(base.top_level_objects["CREATURE"].keys())
    for i in range(len(object_ids)):
        object_id = object_ids[i]
        if i % 10 == 0 or i == len(object_ids) - 1:
            print("processing creature " + str(i + 1) + "/" + str(len(object_ids)), object_id)
        c = base.top_level_objects["CREATURE"][object_id]

        # "unpacks" creature variations and body detail plans
        c.unpack_creature_variations()
        base.report_missing_top_level_objects("CREATURE_VARIATION", uof)
        c.unpack_body_detail_plans()
        base.report_missing_top_level_objects("BODY_DETAIL_PLAN", uof)
        # gets creature materials, tissues, castes
        c.get_materials()
        base.report_missing_top_level_objects("MATERIAL_TEMPLATE", uof)
        c.get_tissues()
        base.report_missing_top_level_objects("TISSUE_TEMPLATE", uof)
        c.get_castes()

        for caste in c.castes.values():

            caste.get_body_parts()
            caste.get_tissue_layers()

    # goes through all plants
    object_ids = list(base.top_level_objects["PLANT"].keys())
    for i in range(len(object_ids)):
        object_id = object_ids[i]
        if i % 10 == 0 or i == len(object_ids) - 1:
            print("processing plant " + str(i + 1) + "/" + str(len(object_ids)), object_id)
        p = base.top_level_objects["PLANT"][object_id]
        p.get_materials()

    # warns and allows you to leave in case too many objects are missing
    if sum([len(sublist) for sublist in base.missing_top_level_objects.values()]) >= 10:
        if input("It seems your raw folder is missing many raw object definitions. "
                 "If you proceed, this tool may come to incorrect conclusions. Do you still wish to proceed? "
                 "(Y/N) ").lower() not in ["yes", "y", "sure"]:
            input("Understood.\nPress enter to kill. >>")
            return False

    # and finally, does what this specific script is supposed to do; calculates the weight of each creature (caste)
    # saves most of the output for later, as the top-25 summary should come first.
    output_string = ""
    object_ids = list(base.top_level_objects["CREATURE"].keys())
    for i in range(len(object_ids)):
        object_id = object_ids[i]

        print("weighing creature " + str(i + 1) + "/" + str(len(object_ids)), object_id)
        creature = base.top_level_objects["CREATURE"][object_id]

        # gets the material of each tissue
        creature.get_tissue_materials()

        output_string += "\n\n[CREATURE:" + creature.object_id + "]"

        # caste
        for caste in creature.castes.values():

            # gets the caste body size
            caste.get_body_size()

            output_string += "\n\t" + caste.object_id
            body_part_relsize_total = sum([body_part.relsize for body_part in caste.body_part_list()])

            caste_density = 0

            # body part
            for body_part in caste.body_part_list():
                if very_detailed_weights:
                    output_string += "\n\t\t" + body_part.object_id + ", relsize: " + str(body_part.relsize) + ", " \
                                     + str(round(body_part.relsize / body_part_relsize_total * 100, 3)) + "% of total "\
                                                                                                          "body volume."

                tissue_layer_thickness_total = sum([tissue_layer.thickness for tissue_layer in body_part.tissue_layers])

                body_part_density = 0

                # tissue layer
                for tissue_layer in body_part.tissue_layers:
                    if very_detailed_weights:
                        output_string += "\n\t\t\t" + tissue_layer.base_tissue_id + ", thickness:" + \
                                         str(tissue_layer.thickness) + ", " + \
                                         str(round(tissue_layer.thickness / tissue_layer_thickness_total * 100, 3)) \
                                         + "% of body part volume."

                    tl_density = 0
                    tl_tissue = creature.tissues[tissue_layer.base_tissue_id]
                    if tl_tissue.material is not None:

                        # gets the material density
                        tl_material_density = tl_tissue.material.get_last_token_value("SOLID_DENSITY",
                                                                                      error_message=
                                                                                      creature.object_id + ", " +
                                                                                      tl_tissue.object_id + ", " +
                                                                                      tl_tissue.material.object_id +
                                                                                      "has no SOLID_DENSITY defined.")
                        if tl_material_density is not False:
                            tl_material_density = int(tl_material_density[0])
                        else:
                            # in actuality redundant, because 0 == False in python.
                            tl_material_density = 0

                        tl_density = tl_material_density * \
                                        (tissue_layer.thickness / tissue_layer_thickness_total) * \
                                        (body_part.relsize / body_part_relsize_total)

                        body_part_density += tl_density
                        caste_density += tl_density

                    if very_detailed_weights:
                        tl_weight = tl_density / 1000 * caste.body_size
                        output_string += "\n\t\t\t" + grams_to_string(tl_weight)

                if very_detailed_weights:
                    body_part_weight = body_part_density / 1000 * caste.body_size
                    output_string += "\n\t\t" + grams_to_string(body_part_weight)

            caste_weight = 0
            if caste.body_size != 0:
                # calculates the entire weight, saves it for printing out later
                caste_weight = caste_density / 1000 * caste.body_size
                output_string += "\n\t" + grams_to_string(caste_weight)
                output_string += "\t(Density: " + str(round(caste_density, 3)) + \
                                 ", BODYSIZE: " + str(caste.body_size) + ")"
            else:
                output_string += "\nNO BODYSIZE, NO WEIGHT"

            # inserts the caste into the list of heaviest castes if it belongs there
            for j in range(len(heaviest_castes)):
                # for creatures with castes as heavy as each other, merges their entries on the top-list
                if caste_weight == heaviest_castes[j][1] and creature.object_id == heaviest_castes[j][0][0]:
                    heaviest_castes[j][0][1] += "," + caste.object_id
                    break
                if caste_weight > heaviest_castes[j][1]:
                    heaviest_castes.insert(j, [[creature.object_id, caste.object_id], caste_weight])
                    heaviest_castes = heaviest_castes[:25]
                    break

    base.double_print("\nOverview:", uof)
    # print general info
    base.double_print("Heaviest creature castes:", uof)
    for i in range(len(heaviest_castes)):
        base.double_print(str(i+1) + ". " + grams_to_string(heaviest_castes[i][1]) + "\t" +
                          ":".join(heaviest_castes[i][0]), uof)

    # flushes
    base.flush_output_file(uof)
    base.double_print("\n--Detailed output:--", uof)
    # asks if you want to abort
    if very_detailed_weights:
        if uof:
            if input("You have \"very detailed weights\" on. "
                     "This will lead to a very large text file being generated (several MBs each time used). "
                     "Due to this tool being new, I can't guarantee the output to be perfect. Do you wish to proceed? "
                     "(Y/N) ").lower() not in ["yes", "y", "sure"]:
                base.close_output_file(uof)
                input("Understood.\nPress enter to kill. >>")
                return False
        else:
            if input("It is highly advised to allow file output while using this tool on these settings. "
                     "Due to this tool being new, "
                     "I can't guarantee the output to be perfect. Do you still wish to proceed? "
                     "(Y/N) ").lower() not in ["yes", "y", "sure"]:
                input("Understood.\nPress enter to kill. >>")
                return False

    # print detailed info
    base.double_print(output_string, uof)
    # and finally closes the output file
    base.close_output_file(uof)

    input("Done.\nPress enter to kill. >>")


if __name__ == "__main__":
    # settings
    raw_path = base.os.getcwd() + "/raw/objects"
    use_output_file = True
    output_path = base.os.getcwd()
    very_detailed_weights = True

    creaturescale_main(raw_path, use_output_file, output_path, very_detailed_weights)
