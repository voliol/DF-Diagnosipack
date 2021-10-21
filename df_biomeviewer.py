import df_diagnosipack_base as base
from importlib import reload
import tabulate
import tkinter as tk
from tkinter import ttk
from doublescrolledframe import DoubleScrolledFrame

# This tool was/is the first one to use an application of its own instead of just running in text mode.
# This is a testament to the great amount of data that needed to be portrayed, and it should not be assumed
# all/any other future tools included in Diagnosipack will follow in its tracks, as coding an UI is considerably
# more time-consuming and troublesome than print() statements are.
# In any case, this code has already been written, so I hope it will be of use! //voliol 2021-10-04


# ====== constants =====================================================================================================

vermin_tokens = ["VERMIN_FISH", "VERMIN_GROUNDER", "VERMIN_ROTTER", "VERMIN_SOIL", "VERMIN_SOIL_COLONY"]

base_biome_ids = ["MOUNTAINS",
                  "GLACIER",
                  "TUNDRA",
                  "SWAMP_TEMPERATE_FRESHWATER",
                  "SWAMP_TEMPERATE_SALTWATER",
                  "MARSH_TEMPERATE_FRESHWATER",
                  "MARSH_TEMPERATE_SALTWATER",
                  "SWAMP_TROPICAL_FRESHWATER",
                  "SWAMP_TROPICAL_SALTWATER",
                  "SWAMP_MANGROVE",
                  "MARSH_TROPICAL_FRESHWATER",
                  "MARSH_TROPICAL_SALTWATER",
                  "TAIGA",
                  "FOREST_TEMPERATE_CONIFER",
                  "FOREST_TEMPERATE_BROADLEAF",
                  "FOREST_TROPICAL_CONIFER",
                  "FOREST_TROPICAL_DRY_BROADLEAF",
                  "FOREST_TROPICAL_MOIST_BROADLEAF",
                  "GRASSLAND_TEMPERATE",
                  "SAVANNA_TEMPERATE",
                  "SHRUBLAND_TEMPERATE",
                  "GRASSLAND_TROPICAL",
                  "SAVANNA_TROPICAL",
                  "SHRUBLAND_TROPICAL",
                  "DESERT_BADLAND",
                  "DESERT_ROCK",
                  "DESERT_SAND",
                  "OCEAN_TROPICAL",
                  "OCEAN_TEMPERATE",
                  "OCEAN_ARCTIC",
                  "POOL_TEMPERATE_FRESHWATER",
                  "POOL_TEMPERATE_BRACKISHWATER",
                  "POOL_TEMPERATE_SALTWATER",
                  "POOL_TROPICAL_FRESHWATER",
                  "POOL_TROPICAL_BRACKISHWATER",
                  "POOL_TROPICAL_SALTWATER",
                  "LAKE_TEMPERATE_FRESHWATER",
                  "LAKE_TEMPERATE_BRACKISHWATER",
                  "LAKE_TEMPERATE_SALTWATER",
                  "LAKE_TROPICAL_FRESHWATER",
                  "LAKE_TROPICAL_BRACKISHWATER",
                  "LAKE_TROPICAL_SALTWATER",
                  "RIVER_TEMPERATE_FRESHWATER",
                  "RIVER_TEMPERATE_BRACKISHWATER",
                  "RIVER_TEMPERATE_SALTWATER",
                  "RIVER_TROPICAL_FRESHWATER",
                  "RIVER_TROPICAL_BRACKISHWATER",
                  "RIVER_TROPICAL_SALTWATER",
                  "SUBTERRANEAN_WATER",
                  "SUBTERRANEAN_CHASM",
                  "SUBTERRANEAN_LAVA"]

cavern_layer_biome_ids = ["SUBTERRANEAN_WATER", "SUBTERRANEAN_CHASM"]

generalized_biome_ids = {"ALL_MAIN": base_biome_ids[0:29 + 1] + base_biome_ids[36:41 + 1],
                         "ANY_LAND": base_biome_ids[0:26 + 1],
                         "ANY_OCEAN": base_biome_ids[27:29 + 1],
                         "ANY_LAKE": base_biome_ids[36:41 + 1],
                         "ANY_TEMPERATE_LAKE": base_biome_ids[36:38 + 1],
                         "ANY_TROPICAL_LAKE": base_biome_ids[39:41 + 1],
                         "ANY_RIVER": base_biome_ids[42:47 + 1],
                         "ANY_TEMPERATE_RIVER": base_biome_ids[42:44 + 1],
                         "ANY_TROPICAL_RIVER": base_biome_ids[45:47 + 1],
                         "ANY_POOL": base_biome_ids[30:35 + 1],
                         "NOT_FREEZING": base_biome_ids[3:26 + 1],
                         "ANY_TEMPERATE": base_biome_ids[3:6 + 1] + base_biome_ids[13:14 + 1] + base_biome_ids[18:20 + 1],
                         "ANY_TROPICAL": base_biome_ids[7:11 + 1] + base_biome_ids[15:17 + 1] + base_biome_ids[21:23 + 1],
                         "ANY_FOREST": base_biome_ids[13:17 + 1],
                         "ANY_SHRUBLAND": ["SHRUBLAND_TROPICAL", "SHRUBLAND_TEMPERATE"],
                         "ANY_GRASSLAND": ["GRASSLAND_TROPICAL", "GRASSLAND_TEMPERATE"],
                         "ANY_SAVANNA": ["SAVANNA_TROPICAL", "SAVANNA_TEMPERATE"],
                         "ANY_TEMPERATE_FOREST": base_biome_ids[13:14 + 1],
                         "ANY_TROPICAL_FOREST": base_biome_ids[15:17 + 1],
                         "ANY_TEMPERATE_BROADLEAF": base_biome_ids[3:6 + 1] + base_biome_ids[14:14 + 1] + base_biome_ids[18:20 + 1],
                         "ANY_TROPICAL_BROADLEAF": base_biome_ids[7:11 + 1] + base_biome_ids[16:17 + 1] + base_biome_ids[21:23 + 1],
                         "ANY_WETLAND": base_biome_ids[3:11 + 1],
                         "ANY_TEMPERATE_WETLAND": base_biome_ids[3:6 + 1],
                         "ANY_TROPICAL_WETLAND": base_biome_ids[7:11 + 1],
                         "ANY_TROPICAL_MARSH": base_biome_ids[10:11 + 1],
                         "ANY_TEMPERATE_MARSH": base_biome_ids[5:6 + 1],
                         "ANY_TROPICAL_SWAMP": base_biome_ids[7:9 + 1],
                         "ANY_TEMPERATE_SWAMP": base_biome_ids[3:4 + 1],
                         "ANY_DESERT": base_biome_ids[24:26 + 1],
                         # a bit of a special case, it's just very practical to deal with synonyms this way
                         "FOREST_TAIGA": ["TAIGA"],
                         "MOUNTAIN": ["MOUNTAINS"]}

visible_biome_categories = [["Wetlands", ["MARSH_TEMPERATE_FRESHWATER", "MARSH_TEMPERATE_SALTWATER",
                                          "SWAMP_TEMPERATE_FRESHWATER", "SWAMP_TEMPERATE_SALTWATER",
                                          "MARSH_TROPICAL_FRESHWATER", "MARSH_TROPICAL_SALTWATER",
                                          "SWAMP_TROPICAL_FRESHWATER", "SWAMP_TROPICAL_SALTWATER",
                                          "SWAMP_MANGROVE"]],
                            ["Forests", ["TAIGA", "FOREST_TEMPERATE_BROADLEAF",
                                         "FOREST_TEMPERATE_CONIFER", "FOREST_TROPICAL_DRY_BROADLEAF",
                                         "FOREST_TROPICAL_MOIST_BROADLEAF", "FOREST_TROPICAL_CONIFER"]],
                            ["Plains", ["GRASSLAND_TEMPERATE", "GRASSLAND_TROPICAL",
                                        "SAVANNA_TEMPERATE", "SAVANNA_TROPICAL",
                                        "SHRUBLAND_TEMPERATE", "SHRUBLAND_TROPICAL"]],
                            ["Deserts", ["DESERT_BADLAND", "DESERT_ROCK",
                                         "DESERT_SAND"]],
                            ["Oceans", ["OCEAN_ARCTIC", "OCEAN_TEMPERATE",
                                        "OCEAN_TROPICAL"]],
                            ["Pools", ["POOL_TEMPERATE_FRESHWATER","POOL_TEMPERATE_BRACKISHWATER",
                                       "POOL_TEMPERATE_SALTWATER", "POOL_TROPICAL_FRESHWATER",
                                       "POOL_TROPICAL_BRACKISHWATER", "POOL_TROPICAL_SALTWATER"]],
                            ["Lakes", ["LAKE_TEMPERATE_FRESHWATER", "LAKE_TEMPERATE_BRACKISHWATER",
                                       "LAKE_TEMPERATE_SALTWATER", "LAKE_TROPICAL_FRESHWATER",
                                       "LAKE_TROPICAL_BRACKISHWATER", "LAKE_TROPICAL_SALTWATER"]],
                            ["Rivers", ["RIVER_TEMPERATE_FRESHWATER", "RIVER_TEMPERATE_BRACKISHWATER",
                                        "RIVER_TEMPERATE_SALTWATER", "RIVER_TROPICAL_FRESHWATER",
                                        "RIVER_TROPICAL_BRACKISHWATER", "RIVER_TROPICAL_SALTWATER"]],
                            ["Underground", ["SUBTERRANEAN_WATER_lvl.1", "SUBTERRANEAN_CHASM_lvl.1",
                                             "SUBTERRANEAN_WATER_lvl.2", "SUBTERRANEAN_CHASM_lvl.2",
                                             "SUBTERRANEAN_WATER_lvl.3", "SUBTERRANEAN_CHASM_lvl.3",
                                             "SUBTERRANEAN_LAVA"]],
                            ["Hidden Fun Stuff", ["HFS"]]]

all_niches = ["CREATURE", "VERMIN", "SHRUB", "TREE", "GRASS"]

all_alignments = [["Unaligned", ["biotope"]],
                  ["Good", ["biotope", "good_biotope"]],
                  ["Evil", ["biotope", "evil_biotope"]],
                  ["Savage", ["biotope", "savage_biotope"]],
                  ["Joyous Wilds (Good+Savage)", ["biotope", "good_biotope", "savage_biotope"]],
                  ["Terrifying (Evil+Savage)", ["biotope", "evil_biotope", "savage_biotope"]]]

listbox_selection = [-1, 0, 0]

TAB_WIDTH = 500
TAB_HEIGHT = 400
DESCRIPTOR_WRAPLENGTH = 400


# ====== Biome class ===================================================================================================

class Biome:

    def __init__(self, biome_id, biome_abbr, use_aligned_biotopes=True):
        self.biome_id = biome_id
        self.biome_abbr = biome_abbr
        self.biotope = {niche_name: [] for niche_name in all_niches}
        # normal above-ground biomes use aligned biotopes, i.e. GOOD/EVIL/SAVAGE species are treated separately
        if use_aligned_biotopes:
            self.good_biotope = {niche_name: [] for niche_name in all_niches}
            self.evil_biotope = {niche_name: [] for niche_name in all_niches}
            self.savage_biotope = {niche_name: [] for niche_name in all_niches}
        else:
            self.good_biotope = None
            self.evil_biotope = None
            self.savage_biotope = None

    def get_data(self, biotopes=("biotope",)):
        # combines the biotopes with the attribute names in "biotopes"
        # subsequent data is taken from these combined biotopes (so you can have e.g. unaligned+savage+good at once)
        combined_biotope = {niche_name: [] for niche_name in all_niches}
        for bt in biotopes:
            for niche_name in all_niches:
                combined_biotope[niche_name] += self.__getattribute__(bt)[niche_name]
        # data is a nested list
        data = [[niche_name.capitalize() for niche_name in all_niches]]
        # adds rows to data
        for i in range(max(len(combined_biotope[niche]) for niche in combined_biotope)):
            datarow = ["---"] * len(all_niches)
            for j in range(len(all_niches)):
                if len(combined_biotope[all_niches[j]]) > i:
                    datarow[j] = combined_biotope[all_niches[j]][i].object_id
            data.append(datarow)
        return data

    def __str__(self):
        biome_string = ""
        biome_string += self.biome_id + "\n"
        # data is a nested list
        data = self.get_data()
        biome_string += str(list(niche + ": " + str(len(niche)) for niche in self.biotope))
        # uses tabulate to make turn that nested list into something pretty
        biome_string += tabulate.tabulate(data)
        return biome_string


# ====== Misc. functions ===============================================================================================

def abbreviate(string, known_abbreviations):
    words = string.split("_")

    # one-word strings
    if len(words) == 1:

        def recursive_one_word_abbreviate(abbr, letters_left, known_abbrs):
            # returns the biome_abbr if it is unique
            if abbr not in known_abbrs:
                return abbr
            # returns False if it runs out of letters
            elif len(letters_left) == 0:
                return False
            # adds a letter and recurses
            else:
                return recursive_one_word_abbreviate(abbr + letters_left[0], letters_left[1:], known_abbrs)

        # uses upper case for the first letter, then lower case
        abbreviation = recursive_one_word_abbreviate(words[0][0], words[0][1:].lower(), known_abbreviations)

    # multi-word strings
    else:
        abbreviation = False

        # iterates through *only* one of the words at a time, does not cover all possibilities
        # i.e. "VERY_LARGE_DOG" could become "VLD", "VLO", "RLD", but never "YEG".
        for i in range(len(words)-1, -1, -1):
            for c in words[i]:
                if c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890":
                    abbr = "".join([word[0] for word in words[:i]] + [c] + [word[0] for word in words[i+1:]])
                    if abbr not in known_abbreviations:
                        return abbr

    if abbreviation is False:
        print("Could not create unique biome_abbr for " + string + ".")
        return False
    else:
        return abbreviation


def get_populated_biomes_from_raws(raw_path, uof):

    biome_abbreviations = []

    biomes = {}
    # goes through the base biome ids, i.e. the valid ids for the BIOME token
    for biome_id in base_biome_ids:
        biome_abbr = abbreviate(biome_id, biome_abbreviations)
        biome_abbreviations.append(biome_abbr)
        # "SUBTERRANEAN_WATER" and "SUBTERRANEAN_CHASM" are special, they one for each cavern layer depth (three)
        if biome_id in cavern_layer_biome_ids:
            for i in range(3):
                biomes[biome_id + "_lvl." + str(i + 1)] = Biome(biome_id + "_lvl." + str(i + 1),
                                                                biome_abbr + str(i + 1),
                                                                use_aligned_biotopes=False)
        # lava's a little special as well
        elif biome_id == "SUBTERRANEAN_LAVA":
            biomes[biome_id] = Biome(biome_id, biome_abbr, use_aligned_biotopes=False)
        # but most base biome ids just get a corresponding biome
        else:
            biomes[biome_id] = Biome(biome_id, biome_abbr)

    # the HFS also counts as its own biome
    biomes["HFS"] = Biome("HFS", "HFS", use_aligned_biotopes=False)

    # reads and loads all raw files
    base.read_and_load_all_raw_files(raw_path)

    # unpacks creature variations so e.g. giant creatures and animal men work
    for c in base.top_level_objects["CREATURE"].values():
        c.unpack_creature_variations()
    print("")
    base.report_missing_top_level_objects("CREATURE_VARIATION", uof)
    base.report_missing_top_level_objects("CREATURE", uof)

    # goes through all creatures and plants
    for object_type in ["CREATURE", "PLANT"]:
        object_ids = list(base.top_level_objects[object_type].keys())
        for i in range(len(object_ids)):
            object_id = object_ids[i]

            print("examining " + object_type.lower() + " " + str(i + 1) + "/" + str(len(object_ids)), object_id)
            o = base.top_level_objects[object_type][object_id]

            niche = "NONE"
            if object_type == "CREATURE":
                if o.has_token_any(vermin_tokens):
                    niche = "VERMIN"
                elif o.has_token("LARGE_ROAMING"):
                    niche = "CREATURE"
            elif object_type == "PLANT":
                if o.has_token("TREE"):
                    niche = "TREE"
                elif o.has_token("GRASS"):
                    niche = "GRASS"
                else:
                    niche = "SHRUB"

            if niche == "NONE":
                print(o.object_id + " has no niche defined.")

            else:
                # adds the species to the right biomes
                # luckily CREATUREs and PLANTs use the same tokens for this, like BIOME, UNDERGROUND_DEPTH, and SAVAGE
                for value in o.get_token_values("BIOME"):
                    pending_ids = [value[0]]

                    # unfolds the "generalized biome ids", like ANY_LAND or NOT_FREEZING
                    if pending_ids[0] in generalized_biome_ids:
                        pending_ids = generalized_biome_ids[pending_ids[0]]

                    for biome_id in pending_ids:

                        # different handling for cavern biomes (which are split into multiple biomes depending on level)
                        if biome_id in cavern_layer_biome_ids:
                            if o.has_token("UNDERGROUND_DEPTH"):
                                (min_depth, max_depth) = o.get_last_token_value("UNDERGROUND_DEPTH")
                                for j in range(max(int(min_depth), 1), min(int(max_depth), 3)+1):
                                    biomes[biome_id+"_lvl."+str(j)].biotope[niche].append(o)
                            else:
                                print(object_id, "has biome", biome_id, "but does not use UNDERGROUND_DEPTH")

                        # and for lava (no splitting or variants)
                        elif biome_id == "SUBTERRANEAN_LAVA":
                            biomes[biome_id].biotope[niche].append(o)

                        # and non-cavern biomes (which have "variants" based on evil/good and
                        # savagery) (not yet implemented)
                        else:
                            # the GOOD/EVIL/SAVAGE tokens exclude each other
                            # I do NOT know if this is the order they are prioritized
                            # !SCIENCE! is needed!
                            if o.has_token("GOOD"):
                                biomes[biome_id].good_biotope[niche].append(o)
                            elif o.has_token("EVIL"):
                                biomes[biome_id].evil_biotope[niche].append(o)
                            elif o.has_token("SAVAGE"):
                                biomes[biome_id].savage_biotope[niche].append(o)
                            else:
                                biomes[biome_id].biotope[niche].append(o)

                # special adds to magma sea and HFS using UNDERGROUND_DEPTH
                # this is my interpretation of the wiki, but I am not 100% certain it is correct,
                # the magma sea could also be a separate "biome" from the lava pipes
                if o.has_token("UNDERGROUND_DEPTH"):
                    (min_depth, max_depth) = o.get_last_token_value("UNDERGROUND_DEPTH")
                    if int(min_depth) < 5 and int(max_depth) >= 4:
                        biomes["SUBTERRANEAN_LAVA"].biotope[niche].append(o)
                    if int(max_depth) >= 5:
                        biomes["HFS"].biotope[niche].append(o)

    return biomes


def get_niche_data(biome_list, niche, biotope="biotope", vertical_biome_abbrs=True):
    # gets a non-repeating list of species belonging to the niche, that appear in any of the visible biomes
    visible_niche_species = []
    for biome in biome_list:
        for species in biome.__getattribute__(biotope)[niche]:
            if species not in visible_niche_species:
                visible_niche_species.append(species)
    # data header
    data = []
    datarow = []
    if vertical_biome_abbrs:
        abbr_max_length = max(len(biome.biome_abbr) for biome in biome_list)
        datarow += ["\n" * (abbr_max_length - 1) + "Object ID", "\n" * (abbr_max_length - 1) + "Species name"]
        datarow += ["\n".join(biome.biome_abbr) for biome in biome_list]
    else:
        datarow += ["Object ID", "Species name"]
        datarow += [biome.biome_abbr for biome in biome_list]
    # frequency column
    datarow.append("F")
    # ubiquitous column
    if vertical_biome_abbrs:
        datarow.append("U\nB\n?")
    else:
        datarow.append("UB?")
    # large predator column
    if niche == "CREATURE":
        if vertical_biome_abbrs:
            datarow.append("L\nP\n?")
        else:
            datarow.append("LP?")
    data.append(datarow)
    # generates the rest of the data
    for species in visible_niche_species:
        # name
        if species.has_token("NAME"):
            species_name = species.get_last_token_value("NAME")[0]
        elif species.has_token("ALL_NAMES"):
            species_name = species.get_last_token_value("ALL_NAMES")[0]
        else:
            species_name = "NO NAME"
        datarow = [species.object_id, species_name]
        # which biomes is it in?
        for biome in biome_list:
            if species in biome.__getattribute__(biotope)[niche]:
                datarow.append("X")
            else:
                datarow.append(" ")
        # frequency
        if species.has_token("FREQUENCY"):
            species_frequency = species.get_last_token_value("FREQUENCY")[0]
        else:
            species_frequency = "50"
        datarow.append(species_frequency)
        # ubiquitous
        if species.has_token("UBIQUITOUS"):
            datarow.append("Y")
        else:
            datarow.append(" ")
        # large predator
        if niche == "CREATURE":
            if species.has_token("LARGE_PREDATOR"):
                datarow.append("Y")
            else:
                datarow.append(" ")
        data.append(datarow)

    return data


def add_data_table(parent, data, grid_x, grid_y, sticky=tk.W):
    data_frame = tk.Frame(parent)
    for j in range(len(data)):
        for k in range(len(data[j])):
            # the table is checkered
            background = ["light gray", "gray"][(j + k) % 2]
            # cuts off strings that are too long
            text = data[j][k]
            if len(text) > 40:
                text = text[:37] + "..."
            tk.Label(data_frame, text=text, anchor="w", background=background).grid(row=j, column=k, sticky="NSEW")
    data_frame.grid(row=grid_x, column=grid_y, sticky=sticky)


def update_niche_tabs():
    # a new name for listbox_selection[2] which is easier to remember
    category = listbox_selection[2]

    # gets all the biomes that belong to that category
    visible_biomes = [biomes[biome_id] for biome_id in
                      category[1]]

    # updates the niche tabs
    for i in range(len(all_niches)):
        niche = all_niches[i]

        # gets the niche tab
        niche_tab = niche_tabs[i]
        # un-hides it
        niche_notebook.add(niche_tab)
        # and clears it (note .inner - because they are VerticalScrolledFrame)
        for child in niche_tab.inner.winfo_children():
            child.destroy()

        # description
        desc_text = "There are " + str(len(visible_biomes)) + " kinds of " + category[0] + ":\n"
        for biome in visible_biomes:
            desc_text += biome.biome_id + " (" + biome.biome_abbr + "); "
        if niche == "CREATURE":
            desc_text += "\nF stands for FREQUENCY, UB for UBIQUITOUS, LP for LARGE_PREDATOR. Species with high " \
                         "FREQUENCY are more likely to appear. UBIQUITOUS species are guaranteed to be included in " \
                         "in-game regions. Only a limited amount of LARGE_PREDATOR species may " \
                         "be included in each in-game region."
        else:
            desc_text += "F stands for FREQUENCY, UB for UBIQUITOUS. Species with high FREQUENCY are more likely to " \
                         "appear. UBIQUITOUS species are guaranteed to be included in in-game regions."
        desc_label = tk.Label(niche_tab, text=desc_text, anchor="w", wraplength=DESCRIPTOR_WRAPLENGTH)
        desc_label.grid(row=0, column=0, sticky=tk.W)

        # gets the data for the table (a nested list)
        data = get_niche_data(visible_biomes, niche)
        # and constructs a table of it which is added to the grid
        add_data_table(niche_tab, data, 1, 0)

        # all biomes in the same category are either aligned or non-aligned,
        # and having a good biotope is equivalent to being aligned,
        # thus this statement suffices to know whether to print tables for good/evil/savage biomes as well
        if visible_biomes[0].good_biotope is not None:
            # GOOD
            tk.Label(niche_tab, text="In good " + category[0].lower() + ":",
                     anchor="w").grid(row=2, column=0, sticky=tk.W)
            data = get_niche_data(visible_biomes, niche, biotope="good_biotope")
            add_data_table(niche_tab, data, 3, 0)
            # EVIL
            tk.Label(niche_tab, text="In evil " + category[0].lower() + ":",
                     anchor="w").grid(row=4, column=0, sticky=tk.W)
            data = get_niche_data(visible_biomes, niche, biotope="evil_biotope")
            add_data_table(niche_tab, data, 5, 0)
            # SAVAGE
            tk.Label(niche_tab, text="In savage " + category[0].lower() + ":",
                     anchor="w").grid(row=6, column=0, sticky=tk.W)
            data = get_niche_data(visible_biomes, niche, biotope="savage_biotope")
            add_data_table(niche_tab, data, 7, 0)


def update_alignment_tabs():
    # a new name for listbox_selection[2] which is easier to remember
    biome = listbox_selection[2]

    # if the biome can be aligned
    if biome.good_biotope is not None:

        for i in range(len(all_alignments)):
            alignment_tab = alignment_tabs[i]
            alignment = all_alignments[i]
            # "unhides" hidden alignment tabs
            alignment_notebook.add(alignment_tab, text=alignment[0])
            # removes old text
            for child in alignment_tab.inner.winfo_children():
                child.destroy()
            # adds table
            data = biome.get_data(alignment[1])
            add_data_table(alignment_tab, data, 0, 0)

    # and if it can't be aligned (i.e. the underground biomes)
    else:
        # only creates the tables for the "unaligned" tab
        alignment_tab = alignment_tabs[0]
        alignment = all_alignments[0]
        # removes old text
        for child in alignment_tab.inner.winfo_children():
            child.destroy()
        # adds table
        data = biome.get_data(alignment[1])
        add_data_table(alignment_tab, data, 0, 0)
        # hides all other tabs
        for i in range(1, len(all_alignments)):
            alignment_notebook.hide(alignment_tabs[i])


def print_biome_category(biome_category):
    uof = base.output_file is not None

    base.either_print("== " + biome_category[0] + " ==", uof)
    # gets the biomes
    biome_list = [biomes[biome_id] for biome_id in biome_category[1]]
    # info about the biome category
    desc_text = "There are " + str(len(biome_list)) + " kinds of " + biome_category[0] + ":\n"
    for biome in biome_list:
        desc_text += biome.biome_id + " (" + biome.biome_abbr + "); "
    desc_text += "\nF stands for FREQUENCY, UB for UBIQUITOUS, LP for LARGE_PREDATOR. Species with high " \
                 "FREQUENCY are more likely to appear. UBIQUITOUS species are guaranteed to be included in " \
                 "in-game regions. Only a limited amount of LARGE_PREDATOR species may " \
                 "be included in each in-game region."
    base.either_print(desc_text, uof)

    for niche in all_niches:
        # prints the niche
        print_biome_category_niche(biome_category, biome_list, niche)


def print_biome_category_niche(biome_category, biome_list, niche):
    uof = base.output_file is not None

    # table format is dictated by use_mediawiki_output
    if use_mediawiki_output is True:
        table_format = "mediawiki"
        headers = []
        vba = False
    else:
        table_format = "grid"
        headers = "firstrow"
        vba = True

    base.either_print("=== " + niche + " ===", uof)
    # table for unaligned species
    data = get_niche_data(biome_list=biome_list, niche=niche, vertical_biome_abbrs=vba)
    base.either_print(tabulate.tabulate(data, tablefmt=table_format, headers=headers), uof)
    # checks if biomes are aligned
    if biome_list[0].good_biotope is not None:
        # GOOD
        if use_mediawiki_output:
            base.either_print("\'\'\'In good " + biome_category[0].lower() + ":\'\'\'", uof)
        else:
            base.either_print("In good " + biome_category[0].lower() + ":", uof)
        data = get_niche_data(biome_list=biome_list, niche=niche, biotope="good_biotope", vertical_biome_abbrs=vba)
        base.either_print(tabulate.tabulate(data, tablefmt=table_format, headers=headers), uof)
        # EVIL
        if use_mediawiki_output:
            base.either_print("\'\'\'In evil " + biome_category[0].lower() + ":\'\'\'", uof)
        else:
            base.either_print("In evil " + biome_category[0].lower() + ":", uof)
        data = get_niche_data(biome_list=biome_list, niche=niche, biotope="evil_biotope", vertical_biome_abbrs=vba)
        base.either_print(tabulate.tabulate(data, tablefmt=table_format, headers=headers), uof)
        # SAVAGE
        if use_mediawiki_output:
            base.either_print("\'\'\'In evil " + biome_category[0].lower() + ":\'\'\'", uof)
        else:
            base.either_print("In evil " + biome_category[0].lower() + ":", uof)
        data = get_niche_data(biome_list=biome_list, niche=niche, biotope="savage_biotope", vertical_biome_abbrs=vba)
        base.either_print(tabulate.tabulate(data, tablefmt=table_format, headers=headers), uof)
    # flushes
    base.flush_output_file(uof)


def print_specific_biome_alignment(biome, alignment):
    uof = base.output_file is not None

    # table format is dictated by use_mediawiki_output
    if use_mediawiki_output is True:
        table_format = "mediawiki"
        headers = []
    else:
        table_format = "grid"
        headers = "firstrow"

    base.either_print("== " + biome.biome_id + ", " + alignment[0] + " ==", uof)
    data = biome.get_data(biotopes=alignment[1])
    base.either_print(tabulate.tabulate(data, tablefmt=table_format, headers=headers), uof)


# ====== Widget commands ===============================================================================================

# listboxes:

def select_visible_biome_category(*args):
    global listbox_selection
    current_selection = visible_biome_categories_listbox.curselection()
    # if the event was due to the listbox being unselected (and thus len(current_selection) not being 1), ignores it
    if len(current_selection) == 1:
        # if the previous item selected was not a biome category
        if listbox_selection != 0:
            # hides the alignment_notebook
            alignment_notebook.grid_remove()
            # shows the niche_notebook
            niche_notebook.grid(row=0, column=2, columnspan=4)
            # selects the first tab
            niche_notebook.select(niche_tabs[0])
        # 0 meaning its the category listbox, then index of it, then the item in visible_biome_categories
        # that represents
        listbox_selection = [0, current_selection[0],
                             visible_biome_categories[current_selection[0]]]
        update_niche_tabs()


def select_specific_biome(*args):
    global listbox_selection
    current_selection = specific_biome_listbox.curselection()
    if len(current_selection) == 1:
        # if the previous item selected was not a specific biome
        if listbox_selection != 1:
            # hides the niche_notebook
            niche_notebook.grid_remove()
            # shows the alignment_notebook
            alignment_notebook.grid(row=0, column=2, columnspan=4)
            # selects the first tab
            alignment_notebook.select(alignment_tabs[0])
        # 1 meaning its the specific biome listbox, then index of it, then the item in biomes that represents
        listbox_selection = [1, current_selection[0],
                             biomes[specific_biome_listbox.get(current_selection[0])]]
        update_alignment_tabs()


# buttons:

def print_all_biomes_command():
    # biome category
    if listbox_selection[0] == 0:
        for biome_category in visible_biome_categories:
            print_biome_category(biome_category)
    # specific biome
    elif listbox_selection[0] == 1:
        for biome in biomes:
            for alignment in all_alignments:
                print_specific_biome_alignment(biome, alignment)


def print_current_biome_command():
    # biome category
    if listbox_selection[0] == 0:
        biome_category = visible_biome_categories[visible_biome_categories_listbox.curselection()[0]]
        print_biome_category(biome_category)
    # specific biome
    elif listbox_selection[0] == 1:
        biome = listbox_selection[2]
        # if the biome is aligned
        if biome.good_biotope is not None:
            for alignment in all_alignments:
                print_specific_biome_alignment(biome, alignment)
        else:
            print_specific_biome_alignment(biome, all_alignments[0])


def print_current_tab_command():
    # biome category
    if listbox_selection[0] == 0:
        # gets the category
        biome_category = listbox_selection[2]
        # gets the biomes
        biome_list = [biomes[biome_id] for biome_id in biome_category[1]]
        # and the current niche/tab
        niche = all_niches[niche_notebook.index("current")]
        print_biome_category_niche(biome_category, biome_list, niche)
    # specific biome
    elif listbox_selection[0] == 1:
        alignment = all_alignments[niche_notebook.index("current")]
        print_specific_biome_alignment(listbox_selection[2], alignment)


# ====== Main function =================================================================================================

def biomeviewer_main(raw_path, uof, output_path, umwo):
    global visible_biome_categories_listbox, specific_biome_listbox
    global niche_notebook, niche_tabs
    global alignment_notebook, alignment_tabs
    global biomes
    global use_mediawiki_output

    # uof for "use output file"
    # umwo for "use mediawiki output"
    use_mediawiki_output = umwo

    # reloads the base module, so e.g. top_level_objects is reset
    reload(base)

    # initializes the output file stuff
    if uof:
        base.initialize_output_file("/df_biomeviewer_output.txt", output_path, raw_path)

    # gets the biomes
    biomes = get_populated_biomes_from_raws(raw_path, uof)

    # ==================================================================================================================

    # initializes the root window
    tool_root = tk.Tk()
    tool_root.title("DF Biomeviewer")
    print("Welcome to DF Biomeviewer!")
    # uses the same icon as the main diagnosipack module
    tool_root.iconbitmap(base.os.getcwd() + "//icon.ico")

    # creates a mainframe+grid within the root
    mainframe = ttk.Frame(tool_root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
    tool_root.columnconfigure(0, weight=1)
    tool_root.rowconfigure(0, weight=1)

    # -- first row ------------------------------------------

    # notebook for listboxes of biome categories/biome ids
    listbox_notebook = ttk.Notebook(mainframe)
    listbox_notebook.grid(column=1, row=0, sticky="NS")

    # listbox for visible biome categories (i.e. "forest", "desert", the kind of categories you find on the wiki)
    visible_biome_categories_listbox = tk.Listbox(listbox_notebook, height=30, width=30)
    listbox_notebook.add(visible_biome_categories_listbox, text="Overview")
    visible_biome_categories_listbox.bind('<<ListboxSelect>>', select_visible_biome_category)
    # populates the listbox
    for vbc in reversed(visible_biome_categories):
        visible_biome_categories_listbox.insert(0, vbc[0])

    # listbox for specific_biome ids
    specific_biome_listbox = tk.Listbox(listbox_notebook, height=30, width=30)
    listbox_notebook.add(specific_biome_listbox, text="Single")
    specific_biome_listbox.bind('<<ListboxSelect>>', select_specific_biome)
    # populates the listbox
    specific_biome_listbox.insert(0, "HFS")
    for biome_id in reversed(base_biome_ids):
        if biome_id in cavern_layer_biome_ids:
            for i in range(3):
                specific_biome_listbox.insert(0, biome_id + "_lvl." + str(i + 1))
        else:
            specific_biome_listbox.insert(0, biome_id)
    # scrollbar for the latter (though it is always visible)
    specific_biome_scrollbar = tk.Scrollbar(mainframe, orient=tk.VERTICAL,
                                            command=specific_biome_listbox.yview)
    specific_biome_listbox.configure(yscrollcommand=specific_biome_scrollbar.set)
    specific_biome_scrollbar.grid(column=0, row=0, sticky="NS")

    # notebook with tabs for each of the niches
    niche_notebook = ttk.Notebook(mainframe)
    niche_notebook.grid(column=2, row=0, columnspan=4)
    niche_tabs = []
    for niche_name in all_niches:
        niche_tab = DoubleScrolledFrame(niche_notebook, width=TAB_WIDTH, height=TAB_HEIGHT)
        niche_tab.grid_propagate(False)
        niche_notebook.add(niche_tab, text=niche_name.capitalize())
        niche_tabs.append(niche_tab)
        tk.Label(niche_tab, text="Select a biome on the left.").grid(column=0, row=0)

    # another notebook for the alignment tabs of specific biomes
    alignment_notebook = ttk.Notebook(mainframe)
    # isn't gridded yet; as it fits in the same spot as niche_book (and is thus "hidden" to begin with)
    alignment_tabs = []
    for alignment in all_alignments:
        alignment_tab = DoubleScrolledFrame(alignment_notebook, width=TAB_WIDTH, height=TAB_HEIGHT)
        alignment_tab.grid_propagate(False)
        alignment_notebook.add(alignment_tab, text=alignment[0])
        alignment_tabs.append(alignment_tab)

    # -- bottom row ------------------------------------------
    # buttons for printing
    tk.Button(mainframe, text="Print all biomes", command=print_all_biomes_command).grid(column=1, row=1)
    tk.Button(mainframe, text="Print current biome", command=print_current_biome_command).grid(column=2, row=1)
    tk.Button(mainframe, text="Print current tab", command=print_current_tab_command).grid(column=3, row=1)

    # runs the main loop
    tool_root.mainloop()

    # ==================================================================================================================

    # flushes
    base.flush_output_file(uof)
    # closes output file
    base.close_output_file(uof)

    input("Done.\nPress enter to kill. >>")


if __name__ == "__main__":
    # settings
    raw_path = base.os.getcwd() + "/raw/objects/"
    use_output_file = True
    output_path = base.os.getcwd()
    use_mediawiki_output = True

    biomeviewer_main(raw_path, use_output_file, output_path, use_mediawiki_output)
