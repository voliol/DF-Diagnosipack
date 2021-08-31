import os
import datetime
from copy import deepcopy

object_types = {"BODY_DETAIL_PLAN": ["BODY_DETAIL_PLAN"],
                "BODY": ["BODY",
                         "BODYGLOSS"],
                "BUILDING": ["BUILDING_WORKSHOP"],
                "CREATURE_VARIATION": ["CREATURE_VARIATION"],
                "CREATURE": ["CREATURE"],
                "DESCRIPTOR_COLOR": ["COLOR"],
                "DESCRIPTOR_PATTERN": ["COLOR_PATTERN"],
                "DESCRIPTOR_SHAPE": ["SHAPE"],
                "ENTITY": ["ENTITY"],
                "INORGANIC": ["INORGANIC"],
                "INTERACTION": ["INTERACTION"],
                "ITEM": ["ITEM_AMMO",
                         "ITEM_ARMOR",
                         "ITEM_FOOD",
                         "ITEM_GLOVES",
                         "ITEM_HELM",
                         "ITEM_INSTRUMENT",
                         "ITEM_PANTS",
                         "ITEM_SHIELD",
                         "ITEM_SIEGEAMMO",
                         "ITEM_TOOL",
                         "ITEM_TOY",
                         "ITEM_TRAPCOMP",
                         "ITEM_WEAPON"],
                "LANGUAGE": ["TRANSLATION",
                             "SYMBOL",
                             "WORD"],
                "MATERIAL_TEMPLATE": ["MATERIAL_TEMPLATE"],
                "PLANT": ["PLANT"],
                "REACTION": ["REACTION"],
                "TISSUE_TEMPLATE": ["TISSUE_TEMPLATE"]}

named_object_types = ["BUILDING", "CREATURE", "COLOR",  # SHAPE could be here but GEMS_USE_ADJ mess it up
                      "ITEM_AMMO", "ITEM_ARMOR", "ITEM_FOOD",
                      "ITEM_GLOVES", "ITEM_HELM", "ITEM_INSTRUMENT",
                      "ITEM_PANTS", "ITEM_SHIELD", "ITEM_SIEGEAMMO",
                      "ITEM_TOOL", "ITEM_TOY", "ITEM_TRAPCOMP",
                      "ITEM_WEAPON", "PLANT", "REACTION"]

# the vanilla ones
attack_creature_variations_ids = ["PUNCH_ATTACK", "KICK_ATTACK", "KICK_HIGHVEL_ATTACK",
                                  "TAIL_ATTACK", "HOOF_ATTACK", "NAIL_SCRATCH_ATTACK",
                                  "CLAW_SCRATCH_ATTACK", "TOOTH_BITE_ATTACK", "TOOTH_BITE_VENOM_ATTACK",
                                  "TAIL_STING_VENOM_ATTACK", "MOUTH_BITE_ATTACK", "MOUTH_SUCK_ATTACK",
                                  "PROBOSCIS_SUCK_ATTACK", "MOUTH_BITE_EDGE_ATTACK", "MOUTH_BITE_VENOM_ATTACK",
                                  "BEAK_BITE_ATTACK", "TALON_SCRATCH_ATTACK", "TUSK_STAB_ATTACK",
                                  "PINCER_ATTACK", "ARM_LOWER_SNATCH_ATTACK"]

# the vanilla ones
gait_creature_variation_ids = ["STANDARD_BIPED_GAITS", "STANDARD_QUADRUPED_GAITS",
                               "STANDARD_WALKING_GAITS", "STANDARD_CLIMBING_GAITS",
                               "STANDARD_SWIMMING_GAITS", "STANDARD_CRAWLING_GAITS",
                               "STANDARD_FLYING_GAITS", "STANDARD_WALK_CRAWL_GAITS"]


# ====== token lists  ==================================================================================================

body_part_definition_tokens = ["APARTURE", "BREATHE", "CATEGORY", "CON", "CON_CAT", "CONTYPE",
                               "CIRCULATION", "CONNECTOR", "DEFAULT_RELSIZE", "DIGIT",
                               "EMBEDDED", "FLIER", "GELDABLE", "GRASP", "GUTS", "HEAD",
                               "HEAR", "INDIVIDUAL_NAME", "INTERNAL", "JOINT", "LIMB",
                               "LOWERBODY", "LEFT", "MOUTH", "NUMBER", "NERVOUS",
                               "PREVENTS_PARENT_COLLAPSE", "RIGHT", "SKELETON", "STANCE",
                               "SIGHT", "SMELL", "SMALL", "SOCKET", "THROAT", "THOUGHT",
                               "TOTEMABLE", "UPPERBODY", "UNDER_PRESSURE", "VERMIN_BUTCHER_ITEM"]

material_definition_tokens = [  # generic material definition tokens
    "PREFIX", "STONE_NAME", "IS_GEM", "TEMP_DIET_INFO", "POWDER_DYE", "TILE",
    "ITEM_SYMBOL", "DISPLAY_COLOR", "BUILD_COLOR", "TILE_COLOR", "BASIC_COLOR",
    "STATE_COLOR", "STATE_NAME", "STATE_ADJ", "STATE_NAME_ADJ",
    "ABSORPTION", "IMPACT_YIELD", "IMPACT_FRACTURE", "IMPACT_STRAIN_AT_YIELD",
    "IMPACT_ELASTICITY", "COMPRESSIVE_YIELD", "COMPRESSIVE_FRACTURE",
    "COMPRESSIVE_STRAIN_AT_YIELD", "COMPRESSIVE_ELASTICITY", "TENSILE_YIELD",
    "TENSILE_FRACTURE", "TENSILE_STRAIN_AT_YIELD", "TENSILE_ELASTICITY", "TORSION_YIELD",
    "TORSION_FRACTURE", "TORSION_STRAIN_AT_YIELD", "TORSION_ELASTICITY", "SHEAR_YIELD",
    "SHEAR_FRACTURE", "SHEAR_STRAIN_AT_YIELD", "SHEAR_ELASTICITY", "BENDING_YIELD",
    "BENDING_FRACTURE", "BENDING_STRAIN_AT_YIELD", "BENDING_ELASTICITY",
    "MAX_EDGE", "MATERIAL_VALUE", "MULTIPLY_VALUE", "SPEC_HEAT", "HEATDAM_POINT",
    "COLDDAM_POINT", "IGNITE_POINT", "MELTING_POINT", "BOILING_POINT", "MAT_FIXED_TEMP",
    "IF_EXISTS_SET_HEATDAM_POINT", "IF_EXISTS_SET_COLDDAM_POINT",
    "IF_EXISTS_SET_IGNITE_POINT", "IF_EXISTS_SET_MELTING_POINT",
    "IF_EXISTS_SET_BOILING_POINT", "IF_EXISTS_SET_MAT_FIXED_TEMP", "SOLID_DENSITY",
    "LIQUID_DENSITY", "MOLAR_MASS", "EXTRACT_STORAGE", "BUTCHER_SPECIAL", "MEAT_NAME",
    "BLOCK_NAME", "WAFERS", "MATERIAL_REACTION_PRODUCT", "ITEM_REACTION_PRODUCT",
    "REACTION_CLASS", "METAL_ORE", "THREAD_METAL", "HARDENS_WITH_WATER", "SOAP_LEVEL",
    # kind of special in that it starts another object def
    "SYNDROME",
    # "material usage tokens"
    "IMPLIES_ANIMAL_KILL", "ALCOHOL_PLANT", "ALCOHOL_CREATURE", "ALCOHOL", "CHEESE_PLANT",
    "CHEESE_CREATURE", "CHEESE", "POWDER_MISC_PLANT", "POWDER_MISC_CREATURE", "POWDER_MISC",
    "STOCKPILE_GLOB", "STOCKPILE_GLOB_SOLID", "STOCKPILE_GLOB_PASTE",
    "STOCKPILE_GLOB_PRESSED", "STOCKPILE_PLANT_GROWTH", "LIQUID_MISC_PLANT",
    "LIQUID_MISC_CREATURE", "LIQUID_MISC_OTHER", "LIQUID_MISC",
    "STRUCTURAL_PLANT_MAT", "SEED_MAT", "BONE", "WOOD", "THREAD_PLANT", "TOOTH",
    "HORN", "PEARL", "SHELL", "LEATHER", "SILK", "SOAP", "GENERATES_MIASMA", "MEAT",
    "ROTS", "BLOOD_MAP_DESCRIPTOR", "SLIME_MAP_DESCRIPTOR", "PUS_MAP_DESCRIPTOR",
    "SWEAT_MAP_DESCRIPTOR", "TEARS_MAP_DESCRIPTOR", "EVAPORATES", "ENTERS_BLOOD",
    "EDIBLE_VERMIN", "EDIBLE_RAW", "EDIBLE_COOKED", "DO_NOT_CLEAN_GLOB",
    "NO_STONE_STOCKPILE", "ITEMS_METAL", "ITEMS_BARRED", "ITEMS_SCALED", "ITEMS_LEATHER",
    "ITEMS_SOFT", "ITEMS_HARD", "IS_STONE", "UNDIGGABLE", "DISPLAY_UNGLAZED",
    "YARN", "STOCKPILE_THREAD_METAL", "IS_METAL", "IS_GLASS", "CRYSTAL_GLASSABLE",
    "ITEMS_WEAPON", "ITEMS_WEAPON_RANGED", "ITEMS_ANVIL", "ITEMS_AMMO", "ITEMS_DIGGER",
    "ITEMS_ARMOR", "ITEMS_DELICATE", "ITEMS_SIEGE_ENGINE", "ITEMS_QUERN"]

syndrome_tokens = ["SYN_NAME",
                   "SYN_CLASS", "SYN_CONTACT", "SYN_INGESTED," "SYN_INHALED", "SYN_INJECTED",
                   "SYN_AFFECTED_CLASS", "SYN_IMMUNE_CLASS", "SYN_AFFECTED_CREATURE", "SYN_IMMUNE_CREATURE",
                   "SYN_NO_HOSPITAL", "SYN_IDENTIFIER", "SYN_CONCENTRATION_ADDED",
                   # self effects (harmful)
                   "CE_BRUISING", "CE_BLISTERS", "CE_OOZING", "CE_BLEEDING", "CE_SWELLING", "CE_NECROSIS",
                   "CE_NUMBNESS", "CE_PAIN", "CE_PARALYSIS", "CE_IMPAIR_FUNCTION", "CE_DIZZINESS",
                   "CE_DROWSINESS", "CE_UNCONCIOUSNESS", "CE_FEVER", "CE_NAUSEA", "CE_COUGH_BLOOD", "CE_VOMIT_BLOOD",
                   # self effects (healing)
                   "CE_REDUCE_PAIN", "CE_REDUCE_SWELLING", "CE_REDUCE_PARALYSIS", "CE_REDUCE_DIZZINESS",
                   "CE_REDUCE_NAUSEA", "CE_REDUCE_FEVER", "CE_STOP_BLEEDING", "CE_CLOSE_OPEN_WOUNDS",
                   "CE_CURE_INFECTION", "CE_HEAL_TISSUES", "CE_HEAL_NERVES", "CE_REGROW_PARTS"
                   # self effects (special)
                                                                             "CE_ADD_TAG", "CE_REMOVE_TAG",
                   "CE_DISPLAY_NAME", "CE_DISPLAY_TILE", "CE_FLASH_TILE",
                   "CE_PHYS_ATT_CHANGE", "CE_MENT_ATT_CHANGE", "CE_SPEED_CHANGE", "CE_SKILL_ROLL_ADJUST",
                   "CE_BODY_APPEARANCE_MODIFIER", "CE_BP_APPEARANCE_MODIFIER",
                   "CE_BODY_TRANSFORMATION", "CE_MATERIAL_FORCE_MULTIPLIER",
                   "CE_SENSE_CREATURE_CLASS", "CE_FEEL_EMOTION", "CE_CHANGE_PERSONALITY", "CE_ERRATIC_BEHAVIOR",
                   # these start an interaction definition
                   "CE_CAN_DO_INTERACTION", "CE_SPECIAL_ATTACK_INTERACTION", "CE_BODY_MAT_INTERACTION",
                   # used by self effects for further arguments (?)
                   "CE"]

tissue_definition_tokens = ["TISSUE_NAME", "TISSUE_MATERIAL", "RELATIVE_THICKNESS",
                            "HEALING_RATE", "VASCULAR", "PAIN_RECEPTORS", "THICKENS_ON_STRENGTH",
                            "THICKENS_ON_ENERGY_STORAGE", "ARTERIES", "SCARS", "STRUCTURAL",
                            "CONNECTIVE_TISSUE_ANCHOR", "SETTABLE", "SPLINTABLE", "FUNCTIONAL",
                            "NERVOUS", "THOUGHT", "MUSCULAR", "SMELL", "HEAR", "FLIGHT",
                            "BREATHE", "SIGHT", "CONNECTS", "MAJOR_ARTERIES", "INSULATION",
                            "COSMETIC", "STYLABLE", "TISSUE_SHAPE", "SUBORDINATE_TO_TISSUE",
                            "TISSUE_MAT_STATE", "TISSUE_LEAKS"]

tissue_layer_definition_tokens = ["TISSUE_LAYER_APPEARANCE_MODIFIER", "TISSUE_STYLE_UNIT",
                                  "TL_CONNECTS", "TL_HEALING_RATE", "TL_MAJOR_ARTERIES",
                                  "TL_PAIN_RECEPTORS", "TL_RELATIVE_THICKNESS", "TL_VASCULAR",
                                  "SET_LAYER_TISSUE",
                                  "TL_COLOR_MODIFIER", "TLCM_GENETIC_MODEL", "TLCM_IMPORTANCE",
                                  "TLCM_NOUN", "TLCM_TIMING",
                                  "SHEARABLE_TISSUE_LAYER"]


# ====== raw object classes  ===========================================================================================
# note that most important functions are methods of one of these classes

class RawObject:

    def __init__(self, object_id, tokens, source_file_name=None):
        self.object_id = object_id
        self.tokens = tokens
        self.source_file_name = source_file_name

    def has_token(self, token_name):
        for token in self.tokens:
            if token[0] == token_name:
                return True
        return False

    def get_token_values(self, token_name, max_amount="inf"):
        token_values = []
        for token in self.tokens:
            if token[0] == token_name:
                token_values.append(token[1:])
            if len(token_values) == max_amount:
                return token_values
        return token_values

    def get_last_token_value(self, token_name, error_message):
        try:
            self.get_token_values(token_name)[-1]
        except IndexError:
            # should perhaps be Raise-d instead?
            print(error_message)
            return False
        else:
            return self.get_token_values(token_name)[-1]


class Creature(RawObject):

    def __init__(self, object_id, tokens, source_file_name=None, materials=None, tissues=None, castes=None):
        super().__init__(object_id, tokens, source_file_name)
        if materials is None:
            self.materials = {}
        if tissues is None:
            self.tissues = {}
        if castes is None:
            self.castes = {}

    def unpack_creature_variations(self):
        new_tokens = []
        insertion_index = 0
        pending_cv_tokens = []

        for token in self.tokens:

            if token[0] == "APPLY_CREATURE_VARIATION":
                # Here is by far the most common error I've encountered, as most tools use
                # Creature.unpack_creature_variations(), but you don't always have your raws in the same folder as
                # the attacks and gaits (and NAIL_MATERIALS).
                if can_get_top_level_object("CREATURE_VARIATION", token[1]):
                    # debug text:
                    # double_print("CREATURE_VARIATION:" + token[1], True)
                    creature_variation = top_level_objects["CREATURE_VARIATION"][token[1]]
                    new_tokens, insertion_index = \
                        apply_creature_variation(new_tokens, insertion_index, creature_variation.tokens,
                                                 token[2:])

            elif token[0] == "APPLY_CURRENT_CREATURE_VARIATION":
                new_tokens, insertion_index = \
                    apply_creature_variation(new_tokens, insertion_index, pending_cv_tokens, [])

            elif token[0] == "COPY_TAGS_FROM":
                if can_get_top_level_object("CREATURE", token[1]):
                    source_creature = top_level_objects["CREATURE"][token[1]]
                    for copy_token in source_creature.tokens:
                        new_tokens.insert(insertion_index, copy_token)
                        insertion_index += 1

            # not applied until the next "APPLY_CURRENT_CREATURE_VARIATION"
            elif token[0] in ["CV_ADD_TAG", "CV_REMOVE_TAG",
                              "CV_CONVERT_TAG",
                              "CVCT_MASTER", "CVCT_TARGET", "CVCT_REPLACEMENT"]:
                pending_cv_tokens.append(token)

            elif token[0] == "GO_TO_END":
                insertion_index = len(new_tokens)

            elif token[0] == "GO_TO_START":
                insertion_index = 0

            elif token[0] == "GO_TO_TAG":
                goto_tag = token[1:]
                goto_finished = False
                i = 0
                while not goto_finished and i < len(new_tokens):
                    if new_tokens[i] == goto_tag:
                        insertion_index = i
                        goto_finished = True
                    i += 1

            else:
                new_tokens.insert(insertion_index, token)
                insertion_index += 1

        self.tokens = new_tokens

    def unpack_body_detail_plans(self):
        new_tokens = []

        for token in self.tokens:

            if token[0] == "BODY_DETAIL_PLAN":
                # sets up a dictionary for later insertions/replacements
                bdp_arg_dict = {"ARG" + str(i - 1): token[i] for i in range(2, len(token))}
                for bdp_token in top_level_objects["BODY_DETAIL_PLAN"][token[1]].tokens:

                    for bdp_arg in bdp_arg_dict:
                        bdp_token = [bdp_token_arg.replace(bdp_arg, bdp_arg_dict[bdp_arg])
                                     for bdp_token_arg in bdp_token]
                    new_tokens.append(bdp_token)

            else:
                new_tokens.append(token)

        self.tokens = new_tokens

    def get_materials(self):
        inside_material_definition = False
        selected_materials = None
        for token in self.tokens:

            if inside_material_definition:

                if token[0] == "PLUS_MATERIAL":
                    selected_materials.append(self.materials[token[1]])

                # if it's neither a material def. token nor a syndrome token we're no longer inside a material def.
                # in theory there could even be an interaction nested within the syndrome,
                # so that should also be checked.
                elif token[0] not in material_definition_tokens + syndrome_tokens:
                    # output_file.write("\n\t"+", ".join([m.object_id for m in selected_materials]))
                    # output_file.write("\n\t["+token[0]+"]")
                    selected_materials = []
                    inside_material_definition = False

                # otherwise, adds the token to all selected materials
                else:
                    for material in selected_materials:
                        material.tokens.append(token)

            if token[0] == "REMOVE_MATERIAL":
                del self.materials[token[1]]

            elif token[0] == "SELECT_MATERIAL":
                if token[1] == "ALL":
                    selected_materials = [self.materials[key] for key in self.materials]
                else:
                    selected_materials = [self.materials[token[1]]]

            elif token[0] == "USE_MATERIAL":
                self.materials[token[1]] = deepcopy(self.materials[token[2]])
                self.materials[token[1]].object_id = token[1]
                selected_materials = [self.materials[token[1]]]
                inside_material_definition = True

            # ADD_MATERIAL is the alias used in body_parts detail plans
            elif token[0] in ["USE_MATERIAL_TEMPLATE", "ADD_MATERIAL"]:
                if can_get_top_level_object("MATERIAL_TEMPLATE", token[2]):
                    self.materials[token[1]] = deepcopy(top_level_objects["MATERIAL_TEMPLATE"][token[2]])
                    self.materials[token[1]].object_id = token[1]
                    selected_materials = [self.materials[token[1]]]
                    inside_material_definition = True

            elif token[0] == "MATERIAL":
                # defines a new material with no tokens
                self.materials[token[1]] = RawObject(token[1], [])
                selected_materials = [self.materials[token[1]]]
                inside_material_definition = True

    def get_tissues(self):
        inside_tissue_definition = False
        selected_tissue = None
        for token in self.tokens:

            if inside_tissue_definition:

                # if it's not a tissue def. token we're no longer inside a tissue def.
                if token[0] not in tissue_definition_tokens:
                    # output_file.write("\n\t"+selected_tissue.object_id)
                    # output_file.write("\n\t["+token[0]+"]")
                    selected_tissue = None
                    inside_tissue_definition = False

                # otherwise, adds the token the selected tissue
                else:
                    selected_tissue.tokens.append(token)

            if token[0] == "REMOVE_TISSUE":
                del self.tissues[token[1]]

            elif token[0] == "SELECT_TISSUE":
                selected_tissue = self.materials[token[1]]

            elif token[0] == "USE_TISSUE":
                self.tissues[token[1]] = deepcopy(self.tissues[token[2]])
                self.tissues[token[1]].object_id = token[1]
                selected_tissue = self.tissues[token[1]]
                inside_tissue_definition = True

            # ADD_TISSUE is the alias used in body_parts detail plans
            elif token[0] in ["USE_TISSUE_TEMPLATE", "ADD_TISSUE"]:
                if can_get_top_level_object("TISSUE_TEMPLATE", token[2]):
                    self.tissues[token[1]] = deepcopy(top_level_objects["TISSUE_TEMPLATE"][token[2]])
                    self.tissues[token[1]].object_id = token[1]
                    selected_tissue = self.tissues[token[1]]
                    inside_tissue_definition = True

            elif token[0] == "TISSUE":
                # defines a new tissue with no tokens
                self.tissues[token[1]] = Tissue(token[1], [])
                selected_tissue = self.tissues[token[1]]
                inside_tissue_definition = True

    def get_castes(self):
        # "Any caste-level tag that occurs before castes are explicitly declared is saved up and placed on any caste
        # that is declared later, unless the caste is explicitly derived from another caste."
        castes_started = False
        shared_caste_tokens = []
        selected_castes = []
        for token in self.tokens:

            if token[0] == "CASTE":
                self.castes[token[1]] = Caste(token[1], deepcopy(shared_caste_tokens), self)
                selected_castes = [self.castes[token[1]]]
                castes_started = True

            elif token[0] == "USE_CASTE":
                self.castes[token[1]] = Caste(token[1], deepcopy(self.castes[token[2]].tokens), self)
                selected_castes = [self.castes[token[1]]]
                castes_started = True

            elif token[0] == "SELECT_CASTE":
                if token[1] == "ALL":
                    selected_castes = [self.castes[caste_key] for caste_key in self.castes]
                else:
                    selected_castes = [self.castes[token[1]]]
                castes_started = True

            elif token[0] == "SELECT_ADDITIONAL_CASTE":
                selected_castes.append(self.castes[token[1]])
                castes_started = True

            else:
                if castes_started:
                    for caste in selected_castes:
                        caste.tokens.append(token)
                else:
                    shared_caste_tokens.append(token)

        # adds a standard caste if there are no others
        if len(self.castes) == 0:
            self.castes["STANDARD"] = Caste("STANDARD", shared_caste_tokens, self)

    def get_tissue_materials(self):

        for tissue in self.tissues.values():

            material_token_value = tissue.get_last_token_value("TISSUE_MATERIAL",
                                                               error_message="The " + tissue.object_id +
                                                                             " tissue of CREATURE:" + self.object_id +
                                                                             " has no material defined.")
            if material_token_value is not False:
                # See https://dwarffortresswiki.org/index.php/Material_token

                if material_token_value[0] in ["INORGANIC", "STONE", "METAL"]:
                    if can_get_top_level_object("INORGANIC", material_token_value[1]):
                        tissue.material = top_level_objects["INORGANIC"][material_token_value[1]]

                elif material_token_value[0] == "CREATURE_MAT":
                    if can_get_top_level_object("CREATURE", material_token_value[1]):
                        tissue.material = top_level_objects["CREATURE"][material_token_value[1]].materials[
                            material_token_value[2]]

                elif material_token_value[0] == "LOCAL_CREATURE_MAT":
                    tissue.material = self.materials[material_token_value[1]]

                elif material_token_value[0] == "PLANT_MAT":
                    if can_get_top_level_object("PLANT", material_token_value[1]):
                        tissue.material = top_level_objects["PLANT"][material_token_value[1]].materials[
                            material_token_value[2]]

                elif material_token_value[0] in hard_coded_materials.keys():
                    tissue.material = hard_coded_materials[material_token_value[0]]

                else:
                    print("Unknown material token used by" + tissue.object_id + " tissue of CREATURE:" +
                          self.object_id + ": " + ":".join(material_token_value))


class Tissue(RawObject):

    def __init__(self, object_id, tokens, source_file_name=None, material=None):
        super().__init__(object_id, tokens, source_file_name)
        if material is None:
            self.material = {}


class Caste(RawObject):

    def __init__(self, object_id, tokens, parent_creature, body_size=None, top_level_body_parts=None):
        super().__init__(object_id, tokens)
        self.parent_creature = parent_creature
        self.body_size = body_size
        if top_level_body_parts is None:
            self.top_level_body_parts = []

    def get_body_size(self):
        # A little more complicated than just checking the BODY_SIZE token,
        # because GRAVITATE_BODY_SIZE and CHANGE_BODY_SIZE_PERC exist.
        # For now, just reads the final adult size.

        body_size_value = self.get_last_token_value("BODY_SIZE", error_message="CREATURE:" +
                                                                               self.parent_creature.object_id +
                                                                               ":" + self.object_id +
                                                                               " has no BODY_SIZE defined.")
        if body_size_value is not False:
            self.body_size = int(body_size_value[2])
            # goes through the tokens, and applies GRAVITATE_BODY_SIZE, CHANGE_BODY_SIZE_PERC if they're there
            for token in self.tokens:
                if token[0] == "GRAVITATE_BODY_SIZE":
                    self.body_size = int((self.body_size + int(token[1])) / 2)
                elif token[0] == "CHANGE_BODY_SIZE_PERC":
                    self.body_size = int(self.body_size * int(token[1]) / 100)
        else:
            self.body_size = 0

    def get_body_parts(self):
        # "BODY" is a token on the caste level
        # goes through and gets each BODY object used by the caste
        for caste_body_token in self.get_token_values("BODY"):
            for i in range(len(caste_body_token)):
                # checks if the BODY object actually exists within the raws
                if can_get_top_level_object("BODY", caste_body_token[i]):
                    body_tokens = top_level_objects["BODY"][caste_body_token[i]].tokens

                    selected_body_part = None
                    con_tokens = []

                    for j in range(len(body_tokens)):
                        token = body_tokens[j]

                        # This logic is very simple because BODY objects are top-level, and are composed solely of
                        # "BP" defining a new body part and tokens between them belonging to those body parts.
                        if token[0] == "BP" or j == len(body_tokens)-1:

                            # if it's not the first body part in the BODY object, adds the current body part
                            if selected_body_part is not None:

                                # a top-level body part
                                if len(con_tokens) == 0:
                                    # a warning message
                                    if len(self.top_level_body_parts) > 0:
                                        print("More than one top level body part used. Might be buggy...",
                                              [bp.name for bp in self.top_level_body_parts])
                                    self.top_level_body_parts.append(selected_body_part)

                                # otherwise goes through the "con tokens" and finds "parents" that satisfy the conditions
                                # of each of those
                                for con_token in con_tokens:
                                    parents = []

                                    if con_token[0] == "CON":
                                        def is_parent_func(func_body_part):
                                            return func_body_part.object_id == con_token[1]

                                    elif con_token[0] == "CON_CAT":
                                        def is_parent_func(func_body_part):
                                            return func_body_part.category == con_token[1]

                                    elif con_token[0] == "CONTYPE":
                                        def is_parent_func(func_body_part):
                                            return func_body_part.has_token(con_token[1])

                                    for top_level_body_part in self.top_level_body_parts:
                                        top_level_body_part.recursive_search(is_parent_func, parents)

                                    # For each parent found (i.e. suitable connectors), creates a new body part based on
                                    # the selected_body_part. So [BP:F1:first finger:STP][CON_CAT:HAND] will give each
                                    # existing hand a "first finger".
                                    for parent in parents:
                                        # note that it makes a copy for each
                                        child_body_part = deepcopy(selected_body_part)
                                        child_body_part.parent = parent
                                        parent.children.append(child_body_part)

                            if token[0] == "BP":
                                # new body part
                                selected_body_part = BodyPart(token[1], [], token[2], token[3])
                                con_tokens = []

                        else:
                            if token[0] == "CATEGORY":
                                selected_body_part.category = token[1]
                            elif token[0] == "DEFAULT_RELSIZE":
                                selected_body_part.relsize = int(token[1])
                            elif token[0] in ["CON", "CON_CAT", "CONTYPE"]:
                                con_tokens.append(token)
                            selected_body_part.tokens.append(token)

        # gets custom relsizes from RELSIZE/BP_RELSIZE
        # (again, the latter is just the creature body detail plan version of the former)
        for token in self.tokens:
            if token[0] in ["RELSIZE", "BP_RELSIZE"]:
                body_parts = self.get_body_parts_by_criteria(token[1:])
                for body_part in body_parts:
                    body_part.relsize = int(token[3])

    def get_tissue_layers(self):
        inside_tissue_layer_definition = False
        selected_tissue_layers = []
        for token in self.tokens:

            # currently just ignores/forcibly removes the sidedness
            token_true = []
            for arg in token:
                if arg in ["FRONT", "BACK", "LEFT", "RIGHT", "TOP", "BOTTOM", "AROUND", "BELOW", "IN_FRONT"]:
                    break
                token_true.append(arg)
            token = token_true

            if inside_tissue_layer_definition:

                if token[0] == "PLUS_TISSUE_LAYER":
                    body_parts = self.get_body_parts_by_criteria(token[2:])
                    for body_part in body_parts:
                        for tissue_layer in body_part.tissue_layers:
                            if token[1] in [tissue_layer.base_tissue_id, "ALL"]:
                                selected_tissue_layers.append(tissue_layer)

                # like SET_TL_GROUP, likely redundant
                elif token[0] == "PLUS_TL_GROUP":
                    body_parts = self.get_body_parts_by_criteria(token[1:])
                    for body_part in body_parts:
                        for tissue_layer in body_part.tissue_layers:
                            if token[3] in [tissue_layer.base_tissue_id, "ALL"]:
                                selected_tissue_layers.append(tissue_layer)

                elif token[0] == "SET_LAYER_TISSUE":
                    for tissue_layer in selected_tissue_layers:
                        tissue_layer.base_tissue_id = token[1]

                # if it's not a tissue layer def. token we're no longer inside a tissue layer def.
                elif token[0] not in tissue_layer_definition_tokens:
                    # output_file.write("\n\t"+selected_tissue.object_id)
                    # output_file.write("\n\t["+token[0]+"]")
                    selected_tissue_layers = []
                    inside_tissue_layer_definition = False

                # otherwise, adds the token to all selected tissue layers
                else:
                    for tissue_layer in selected_tissue_layers:
                        tissue_layer.extra_tokens.append(token)

            if token[0] in ["TISSUE_LAYER", "TISSUE_LAYER_OVER"]:
                selected_tissue_layers = []
                body_parts = self.get_body_parts_by_criteria(token[1:])
                for body_part in body_parts:
                    body_part.tissue_layers.append(TissueLayer(token[3]))
                    selected_tissue_layers.append(body_part.tissue_layers[-1])

                inside_tissue_layer_definition = True

            elif token[0] == "TISSUE_LAYER_UNDER":
                selected_tissue_layers = []
                body_parts = self.get_body_parts_by_criteria(token[1:])
                for body_part in body_parts:
                    # inserts at the beginning instead of appending
                    body_part.tissue_layers.insert(0, TissueLayer(token[3]))
                    selected_tissue_layers.append(body_part.tissue_layers[0])
                inside_tissue_layer_definition = True

            # body detail plan token:
            # I'm not sure if the former token appends or replaces, probably appends in which case it is identical to
            # the latter
            elif token[0] in ["BP_LAYERS", "BP_LAYERS_OVER"]:

                # I don't think tissue layers are "selected" by the body detail plan tokens,
                # thus you aren't inside a tissue layer def. after using them
                inside_tissue_layer_definition = False

                body_parts = self.get_body_parts_by_criteria(token[1:])

                for body_part in body_parts:
                    # goes through the tissues listed in the token
                    for i in range(3, len(token), 2):
                        # NONE can be given as an argument to ignore all those tissue layers,
                        # see the green devourer in vanilla
                        if token[i] != "NONE":
                            body_part.tissue_layers.append(TissueLayer(token[i], int(token[i + 1])))

            # same as above but the tissue layers are inserted (in order) at the start/under under layers,
            # instead of beeing appended/put over the other layers
            elif token[0] == "BP_LAYERS_UNDER":

                print(":".join(token))

                inside_tissue_layer_definition = False

                body_parts = self.get_body_parts_by_criteria(token[1:])

                for body_part in body_parts:
                    insertion_index = 0
                    for i in range(3, len(token), 2):
                        if token[i] != "NONE":
                            body_part.tissue_layers.insert(insertion_index,
                                                           TissueLayer(token[i], int(token[i + 1])))
                            insertion_index += 1

            elif token[0] == "SELECT_TISSUE_LAYER":
                selected_tissue_layers = []
                body_parts = self.get_body_parts_by_criteria(token[2:])
                for body_part in body_parts:
                    for tissue_layer in body_part.tissue_layers:
                        if token[1] in [tissue_layer.base_tissue_id, "ALL"]:
                            selected_tissue_layers.append(tissue_layer)

                inside_tissue_layer_definition = True

            # This token seems to be redundant with the one above existing. As for why, ask Toady.
            # Note that it is still used in the vanilla raws, so this *code*  is not redundant.
            elif token[0] == "SET_TL_GROUP":
                selected_tissue_layers = []
                # still, it's slightly different in use, note "token[1:]" instead of "token[2:]"
                body_parts = self.get_body_parts_by_criteria(token[1:])
                for body_part in body_parts:
                    for tissue_layer in body_part.tissue_layers:
                        # and "token[3]" instead of "token[1]"
                        if token[3] in [tissue_layer.base_tissue_id, "ALL"]:
                            selected_tissue_layers.append(tissue_layer)

                inside_tissue_layer_definition = True

    # many tokens allow you to select a number of body parts, either by category, token, or type
    def get_body_parts_by_criteria(self, criteria):
        # If there are no criteria, then all body parts are selected.
        # (probably only works with SELECT_TISSUE_LAYER, not SET_TL_GROUP)
        # In vanilla, this is used by the hydra like this:
        # [SELECT_TISSUE_LAYER:ALL]
        #   [TL_HEALING_RATE:1]
        if len(criteria) == 0:
            return self.body_part_list()

        # otherwise, it parses the criteria arguments
        selected_body_parts = []

        if criteria[0] == "BY_TOKEN":
            def fits_criteria_func(func_body_part):
                return func_body_part.object_id == criteria[1]

        elif criteria[0] == "BY_CATEGORY":
            def fits_criteria_func(func_body_part):
                return criteria[1] in [func_body_part.category, "ALL"]

        elif criteria[0] == "BY_TYPE":
            def fits_criteria_func(func_body_part):
                return func_body_part.has_token(criteria[1])

        else:
            print("Invalid criteria " + criteria[0] + ".")
            return []

        for top_level_body_part in self.top_level_body_parts:
            top_level_body_part.recursive_search(fits_criteria_func, selected_body_parts)
        return selected_body_parts

    # returns all the body parts as a flat list; easier to go through in cases where the tree structure doesn't matter
    def body_part_list(self):
        body_part_list = []

        def true_func(func_body_part):
            return True

        for top_level_body_part in self.top_level_body_parts:
            body_part_list = top_level_body_part.recursive_search(true_func, body_part_list)
        return body_part_list

    def print_body_parts(self):

        for body_part in self.body_part_list():
            if body_part.parent is not None:
                double_print(body_part.parent.object_id + " - " + body_part.object_id + ", " +
                             body_part.name, output_file is not None)
            else:
                double_print(body_part.object_id + ", " +
                             body_part.name, output_file is not None)


class BodyPart(RawObject):

    def __init__(self, object_id, tokens, name, plural,
                 parent=None, children=None,
                 category=None, relsize=None, tissue_layers=None):
        super().__init__(object_id, tokens)
        self.name = name
        self.plural = plural
        self.category = category
        self.parent = parent
        if children is None:
            self.children = []
        if tissue_layers is None:
            self.tissue_layers = []
        if relsize is None:
            # iirc this is the standard relsize
            self.relsize = 500

    def recursive_search(self, func, return_list):
        if func(self):
            return_list.append(self)
        for child in self.children:
            return_list = child.recursive_search(func, return_list)
        return return_list


class TissueLayer:

    def __init__(self, base_tissue_id, thickness=1, extra_tokens=None):
        self.base_tissue_id = base_tissue_id
        # failsafe in case of clumsy inputting
        if type(thickness) != int:
            thickness = int(thickness)
        self.thickness = thickness
        if extra_tokens is None:
            self.extra_tokens = []


class Plant(RawObject):
    def __init__(self, object_id, tokens, source_file_name=None, materials=None):
        super().__init__(object_id, tokens, source_file_name)
        if materials is None:
            self.materials = {}

    def get_materials(self):
        # for now identical to Creature.get_materials(), because it works fine even if plants don't use
        # PLUS_MATERIAL, REMOVE_MATERIAL, SELECT_MATERIAL
        inside_material_definition = False
        selected_materials = None
        for token in self.tokens:

            if inside_material_definition:

                if token[0] == "PLUS_MATERIAL":
                    selected_materials.append(self.materials[token[1]])

                # if it's neither a material def. token nor a syndrome token we're no longer inside a material def.
                # in theory there could even be an interaction nested within the syndrome,
                # so that should also be checked.
                elif token[0] not in material_definition_tokens + syndrome_tokens:
                    # output_file.write("\n\t"+", ".join([m.object_id for m in selected_materials]))
                    # output_file.write("\n\t["+token[0]+"]")
                    selected_materials = []
                    inside_material_definition = False

                # otherwise, adds the token to all selected materials
                else:
                    for material in selected_materials:
                        material.tokens.append(token)

            if token[0] == "REMOVE_MATERIAL":
                del self.materials[token[1]]

            elif token[0] == "SELECT_MATERIAL":
                if token[1] == "ALL":
                    selected_materials = [self.materials[key] for key in self.materials]
                else:
                    selected_materials = [self.materials[token[1]]]

            elif token[0] == "USE_MATERIAL":
                self.materials[token[1]] = deepcopy(self.materials[token[2]])
                self.materials[token[1]].object_id = token[1]
                selected_materials = [self.materials[token[1]]]
                inside_material_definition = True

            # ADD_MATERIAL is the alias used in body_parts detail plans
            elif token[0] in ["USE_MATERIAL_TEMPLATE", "ADD_MATERIAL"]:
                if can_get_top_level_object("MATERIAL_TEMPLATE", token[2]):
                    self.materials[token[1]] = deepcopy(top_level_objects["MATERIAL_TEMPLATE"][token[2]])
                    self.materials[token[1]].object_id = token[1]
                    selected_materials = [self.materials[token[1]]]
                    inside_material_definition = True

            elif token[0] == "MATERIAL":
                # defines a new material with no tokens
                self.materials[token[1]] = RawObject(token[1], [])
                selected_materials = [self.materials[token[1]]]
                inside_material_definition = True


# ====== other classes  ================================================================================================

class CreatureVariationConvert:

    def __init__(self, master, target, replacement):
        self.master = master
        self.target = target
        if replacement is None:
            replacement = ""
        self.replacement = replacement


# ====== hard-coded materials ==========================================================================================
# Yes, these are annoying to scroll by in IDLE, but they had to be somewhere and this is the least-file solution.
# Also, maybe you should use a better IDE for a non-tiny project such as this?

# Last updated DF 0.47.05
hard_coded_materials = {"AMBER":
                        RawObject("AMBER",
                                  [["STATE_COLOR", "ALL", "AMBER"],
                                   ["STATE_NAME_ADJ", "SOLID", "amber"],
                                   ["STATE_NAME_ADJ", "SOLID_POWDER", "ground amber"],
                                   ["STATE_NAME_ADJ", "SOLID_PASTE", "amber paste"],
                                   ["STATE_NAME_ADJ", "SOLID_PRESSED", "pressed amber"],
                                   ["BASIC_COLOR", "6", "0"],
                                   ["BUILD_COLOR", "6", "0", "0"],
                                   ["TILE_COLOR", "7", "7", "1"],
                                   ["MATERIAL_VALUE", "2"],
                                   ["SPEC_HEAT", "1000"],
                                   ["HEATDAM_POINT", "11000"],
                                   ["SOLID_DENSITY", "1200"],
                                   ["LIQUID_DENSITY", "1200"],
                                   ["ITEMS_DELICATE"]]),
                        "ASH":
                        RawObject("ASH",
                                  [["STATE_COLOR", "ALL", "GRAY"],
                                   ["STATE_NAME_ADJ", "ALL_SOLID", "ash"],
                                   ["STATE_NAME_ADJ", "SOLID_PASTE", "ash paste"],
                                   ["STATE_NAME_ADJ", "SOLID_PRESSED", "pressed ash"],
                                   ["BUILD_COLOR", "7", "0", "0"],
                                   ["TILE_COLOR", "7", "7", "1"],
                                   ["SPEC_HEAT", "800"],
                                   ["SOLID_DENSITY", "1200"],
                                   ["MATERIAL_REACTION_PRODUCT", "GLAZE_MAT", "INORGANIC", "ASH_GLAZE"]]),
                        "COAL":
                        RawObject("COAL",
                                  [["STATE_COLOR", "ALL", "BLACK"],
                                   ["STATE_NAME_ADJ", "SOLID", "coal"],
                                   ["STATE_NAME_ADJ", "SOLID_POWDER", "coal powder"],
                                   ["STATE_NAME_ADJ", "SOLID_PASTE", "coal slush"],
                                   ["STATE_NAME_ADJ", "SOLID_PRESSED", "pressed coal"],
                                   ["BASIC_COLOR", "0", "1"],
                                   ["BUILD_COLOR", "0", "0", "1"],
                                   ["TILE_COLOR", "7", "7", "1"],
                                   ["MATERIAL_VALUE", "2"],
                                   ["SPEC_HEAT", "409"],
                                   ["IGNITE_POINT", "11440"],
                                   ["SOLID_DENSITY", "1346"]]),
                        "CORAL":
                        RawObject("CORAL",
                                  [["STATE_COLOR", "ALL", "WHITE"],
                                   ["STATE_NAME_ADJ", "SOLID", "coral"],
                                   ["STATE_NAME_ADJ", "SOLID_POWDER", "ground coral"],
                                   ["STATE_NAME_ADJ", "SOLID_PASTE", "coral paste"],
                                   ["STATE_NAME_ADJ", "SOLID_PRESSED", "pressed coral"],
                                   ["BASIC_COLOR", "7", "1"],
                                   ["BUILD_COLOR", "7", "0", "1"],
                                   ["TILE_COLOR", "7", "7", "1"],
                                   ["MATERIAL_VALUE", "2"],
                                   ["SPEC_HEAT", "1000"],
                                   ["HEATDAM_POINT", "10600"],
                                   ["SOLID_DENSITY", "1200"],
                                   ["ITEMS_DELICATE"]]),
                        "FILTH_B":
                        RawObject("FILTH_B",
                                  [["STATE_COLOR", "ALL", "BROWN"],
                                   ["STATE_NAME_ADJ", "ALL_SOLID", "filth"],
                                   ["STATE_NAME_ADJ", "SOLID_PRESSED", "pressed filth"],
                                   ["BASIC_COLOR", "6", "0"],
                                   ["BUILD_COLOR", "6", "0", "0"],
                                   ["TILE_COLOR", "7", "7", "1"],
                                   ["SPEC_HEAT", "4181"],
                                   ["HEATDAM_POINT", "10180"],
                                   ["SOLID_DENSITY", "1200"]]),
                        "FILTH_Y":
                        RawObject("FILTH_Y",
                                  [["STATE_COLOR", "ALL", "YELLOW"],
                                   ["STATE_NAME_ADJ", "ALL_SOLID", "frozen filth"],
                                   ["STATE_NAME_ADJ", "LIQUID", "filth"],
                                   ["STATE_NAME_ADJ", "GAS", "boiling filth"],
                                   ["STATE_NAME_ADJ", "SOLID_POWDER", "frozen filth powder"],
                                   ["STATE_NAME_ADJ", "SOLID_PASTE", "filth slush"],
                                   ["BASIC_COLOR", "6", "1"],
                                   ["BUILD_COLOR", "6", "0", "1"],
                                   ["TILE_COLOR", "7", "7", "1"],
                                   ["SPEC_HEAT", "4181"],
                                   ["HEATDAM_POINT", "10180"],
                                   ["MELTING_POINT", "10000"],
                                   ["BOILING_POINT", "10180"],
                                   ["SOLID_DENSITY", "920"],
                                   ["LIQUID_DENSITY", "1000"]]),
                        "GLASS_GREEN":
                        RawObject("GLASS_GREEN",
                                  [["STATE_COLOR", "ALL_SOLID", "DARK_GREEN"],
                                   ["STATE_NAME_ADJ", "SOLID", "green glass"],
                                   ["STATE_COLOR", "LIQUID", "RED"],
                                   ["STATE_NAME_ADJ", "LIQUID", "molten green glass"],
                                   ["STATE_COLOR", "GAS", "RED"],
                                   ["STATE_NAME_ADJ", "GAS", "boiling green glass"],
                                   ["STATE_NAME_ADJ", "SOLID_POWDER", "ground green glass"],
                                   ["STATE_NAME_ADJ", "SOLID_PASTE", "green glass paste"],
                                   ["STATE_NAME_ADJ", "SOLID_PRESSED", "pressed green glass"],
                                   ["BASIC_COLOR", "2", "0"],
                                   ["BUILD_COLOR", "2", "0", "0"],
                                   ["TILE_COLOR", "7", "7", "1"],
                                   ["MATERIAL_VALUE", "2"],
                                   ["SPEC_HEAT", "700"],
                                   ["MELTING_POINT", "13600"],
                                   ["BOILING_POINT", "16000"],
                                   ["SOLID_DENSITY", "2600"],
                                   ["LIQUID_DENSITY", "2240"],
                                   ["BENDING_YIELD", "33000"],
                                   ["BENDING_FRACTURE", "33000"],
                                   ["BENDING_STRAIN_AT_YIELD", "47"],
                                   ["SHEAR_YIELD", "33000"],
                                   ["SHEAR_FRACTURE", "33000"],
                                   ["SHEAR_STRAIN_AT_YIELD", "113"],
                                   ["TORSION_YIELD", "33000"],
                                   ["TORSION_FRACTURE", "33000"],
                                   ["TORSION_STRAIN_AT_YIELD", "113"],
                                   ["IMPACT_YIELD", "1000000"],
                                   ["IMPACT_FRACTURE", "1000000"],
                                   ["IMPACT_STRAIN_AT_YIELD", "2222"],
                                   ["TENSILE_YIELD", "33000"],
                                   ["TENSILE_FRACTURE", "33000"],
                                   ["TENSILE_STRAIN_AT_YIELD", "47"],
                                   ["COMPRESSIVE_YIELD", "1000000"],
                                   ["COMPRESSIVE_FRACTURE", "1000000"],
                                   ["COMPRESSIVE_STRAIN_AT_YIELD", "2222"],
                                   ["MAX_EDGE", "15000"],
                                   ["ITEMS_HARD"],
                                   ["IS_GLASS"]]),
                        "GLASS_CLEAR":
                        RawObject("GLASS_CLEAR",
                                  [["STATE_COLOR", "ALL_SOLID", "CLEAR"],
                                   ["STATE_NAME_ADJ", "SOLID", "clear glass"],
                                   ["STATE_COLOR", "LIQUID", "RED"],
                                   ["STATE_NAME_ADJ", "LIQUID", "molten clear glass"],
                                   ["STATE_COLOR", "GAS", "RED"],
                                   ["STATE_NAME_ADJ", "GAS", "boiling clear glass"],
                                   ["STATE_NAME_ADJ", "SOLID_POWDER", "ground clear glass"],
                                   ["STATE_NAME_ADJ", "SOLID_PASTE", "clear glass paste"],
                                   ["STATE_NAME_ADJ", "SOLID_PRESSED", "pressed clear glass"],
                                   ["BASIC_COLOR", "3", "0"],
                                   ["BUILD_COLOR", "3", "0", "0"],
                                   ["TILE_COLOR", "7", "7", "1"],
                                   ["MATERIAL_VALUE", "5"],
                                   ["SPEC_HEAT", "700"],
                                   ["MELTING_POINT", "13600"],
                                   ["BOILING_POINT", "16000"],
                                   ["SOLID_DENSITY", "2600"],
                                   ["LIQUID_DENSITY", "2240"],
                                   ["BENDING_YIELD", "33000"],
                                   ["BENDING_FRACTURE", "33000"],
                                   ["BENDING_STRAIN_AT_YIELD", "47"],
                                   ["SHEAR_YIELD", "33000"],
                                   ["SHEAR_FRACTURE", "33000"],
                                   ["SHEAR_STRAIN_AT_YIELD", "113"],
                                   ["TORSION_YIELD", "33000"],
                                   ["TORSION_FRACTURE", "33000"],
                                   ["TORSION_STRAIN_AT_YIELD", "113"],
                                   ["IMPACT_YIELD", "1000000"],
                                   ["IMPACT_FRACTURE", "1000000"],
                                   ["IMPACT_STRAIN_AT_YIELD", "2222"],
                                   ["TENSILE_YIELD", "33000"],
                                   ["TENSILE_FRACTURE", "33000"],
                                   ["TENSILE_STRAIN_AT_YIELD", "47"],
                                   ["COMPRESSIVE_YIELD", "1000000"],
                                   ["COMPRESSIVE_FRACTURE", "1000000"],
                                   ["COMPRESSIVE_STRAIN_AT_YIELD", "2222"],
                                   ["MAX_EDGE", "15000"],
                                   ["ITEMS_HARD"],
                                   ["IS_GLASS"]]),
                        "GLASS_CRYSTAL":
                        RawObject("GLASS_CRYSTAL",
                                  [["STATE_COLOR", "ALL_SOLID", "CLEAR"],
                                   ["STATE_NAME_ADJ", "SOLID", "crystal glass"],
                                   ["STATE_COLOR", "LIQUID", "RED"],
                                   ["STATE_NAME_ADJ", "LIQUID", "molten crystal glass"],
                                   ["STATE_COLOR", "GAS", "RED"],
                                   ["STATE_NAME_ADJ", "GAS", "boiling crystal glass"],
                                   ["STATE_NAME_ADJ", "SOLID_POWDER", "ground crystal glass"],
                                   ["STATE_NAME_ADJ", "SOLID_PASTE", "crystal glass paste"],
                                   ["STATE_NAME_ADJ", "SOLID_PRESSED", "pressed crystal glass"],
                                   ["BASIC_COLOR", "7", "1"],
                                   ["BUILD_COLOR", "7", "0", "1"],
                                   ["TILE_COLOR", "7", "7", "1"],
                                   ["MATERIAL_VALUE", "10"],
                                   ["SPEC_HEAT", "700"],
                                   ["MELTING_POINT", "13600"],
                                   ["BOILING_POINT", "16000"],
                                   ["SOLID_DENSITY", "2600"],
                                   ["LIQUID_DENSITY", "2240"],
                                   ["BENDING_YIELD", "33000"],
                                   ["BENDING_FRACTURE", "33000"],
                                   ["BENDING_STRAIN_AT_YIELD", "47"],
                                   ["SHEAR_YIELD", "33000"],
                                   ["SHEAR_FRACTURE", "33000"],
                                   ["SHEAR_STRAIN_AT_YIELD", "113"],
                                   ["TORSION_YIELD", "33000"],
                                   ["TORSION_FRACTURE", "33000"],
                                   ["TORSION_STRAIN_AT_YIELD", "113"],
                                   ["IMPACT_YIELD", "1000000"],
                                   ["IMPACT_FRACTURE", "1000000"],
                                   ["IMPACT_STRAIN_AT_YIELD", "2222"],
                                   ["TENSILE_YIELD", "33000"],
                                   ["TENSILE_FRACTURE", "33000"],
                                   ["TENSILE_STRAIN_AT_YIELD", "47"],
                                   ["COMPRESSIVE_YIELD", "1000000"],
                                   ["COMPRESSIVE_FRACTURE", "1000000"],
                                   ["COMPRESSIVE_STRAIN_AT_YIELD", "2222"],
                                   ["MAX_EDGE", "15000"],
                                   ["ITEMS_HARD"],
                                   ["IS_GLASS"]]),
                        "GRIME":
                        RawObject("GRIME",
                                  [["STATE_COLOR", "ALL", "BROWN"],
                                   ["STATE_NAME_ADJ", "ALL_SOLID", "grime"],
                                   ["STATE_NAME_ADJ", "SOLID_PASTE", "grime paste"],
                                   ["STATE_NAME_ADJ", "SOLID_PRESSED", "pressed grime"],
                                   ["BASIC_COLOR", "2", "0"],
                                   ["BUILD_COLOR", "2", "0", "0"],
                                   ["TILE_COLOR", "7", "7", "1"],
                                   ["SPEC_HEAT", "800"],
                                   ["SOLID_DENSITY", "1200"]]),
                        # magma/lava
                        "INORGANIC":
                        RawObject("INORGANIC",
                                  [["STATE_COLOR", "ALL_SOLID", "GRAY"],
                                   ["STATE_NAME_ADJ", "ALL_SOLID", "rock"],
                                   ["STATE_COLOR", "LIQUID", "RED"],
                                   ["STATE_NAME_ADJ", "LIQUID", "magma"],
                                   ["STATE_COLOR", "GAS", "RED"],
                                   ["STATE_NAME_ADJ", "GAS", "boiling magma"],
                                   ["BUILD_COLOR", "7", "0", "0"],
                                   ["TILE_COLOR", "7", "7", "1"],
                                   ["SPEC_HEAT", "1000"],
                                   ["MELTING_POINT", "11500"],
                                   ["BOILING_POINT", "13000"],
                                   ["MAT_FIXED_TEMP", "12000"],
                                   ["SOLID_DENSITY", "2000"],
                                   ["LIQUID_DENSITY", "2000"]]),
                        "LYE":
                        RawObject("LYE",
                                  [["STATE_COLOR", "ALL", "CLEAR"],
                                   ["STATE_NAME_ADJ", "ALL_SOLID", "frozen lye"],
                                   ["STATE_NAME_ADJ", "LIQUID", "lye"],
                                   ["STATE_NAME_ADJ", "GAS", "boiling lye"],
                                   ["STATE_NAME_ADJ", "SOLID_POWDER", "frozen lye powder"],
                                   ["STATE_NAME_ADJ", "SOLID_PASTE", "lye slush"],
                                   ["BUILD_COLOR", "7", "0", "0"],
                                   ["TILE_COLOR", "7", "7", "1"],
                                   ["MATERIAL_VALUE", "2"],
                                   ["SPEC_HEAT", "4181"],
                                   ["MELTING_POINT", "10000"],
                                   ["BOILING_POINT", "10180"],
                                   ["SOLID_DENSITY", "920"],
                                   ["LIQUID_DENSITY", "1000"]]),
                        "MUD":
                        RawObject("MUD",
                                  [["STATE_COLOR", "ALL", "BROWN"],
                                   ["STATE_NAME_ADJ", "ALL_SOLID", "mud"],
                                   ["STATE_NAME_ADJ", "SOLID_POWDER", "dirt"],
                                   ["STATE_NAME_ADJ", "SOLID_PRESSED", "pressed dirt"],
                                   ["BASIC_COLOR", "6", "0"],
                                   ["BUILD_COLOR", "6", "0", "0"],
                                   ["TILE_COLOR", "7", "7", "1"],
                                   ["SPEC_HEAT", "800"],
                                   ["SOLID_DENSITY", "1200"]]),
                        "PEARLASH":
                        RawObject("PEARLASH",
                                  [["STATE_COLOR", "ALL", "WHITE"],
                                   ["STATE_NAME_ADJ", "ALL_SOLID", "pearlash"],
                                   ["STATE_NAME_ADJ", "SOLID_PASTE", "pearlash paste"],
                                   ["STATE_NAME_ADJ", "SOLID_PRESSED", "pressed pearlash"],
                                   ["BASIC_COLOR", "7", "1"],
                                   ["BUILD_COLOR", "7", "0", "1"],
                                   ["TILE_COLOR", "7", "7", "1"],
                                   ["MATERIAL_VALUE", "4"],
                                   ["SPEC_HEAT", "800"],
                                   ["SOLID_DENSITY", "1200"]]),
                        "POTASH":
                        RawObject("POTASH",
                                  [["STATE_COLOR", "ALL", "WHITE"],
                                   ["STATE_NAME_ADJ", "ALL_SOLID", "potash"],
                                   ["STATE_NAME_ADJ", "SOLID_PASTE", "potash slush"],
                                   ["STATE_NAME_ADJ", "SOLID_PRESSED", "pressed potash"],
                                   ["BASIC_COLOR", "7", "1"],
                                   ["BUILD_COLOR", "7", "0", "1"],
                                   ["TILE_COLOR", "7", "7", "1"],
                                   ["MATERIAL_VALUE", "3"],
                                   ["SPEC_HEAT", "800"],
                                   ["SOLID_DENSITY", "1200"]]),
                        "SALT":
                        RawObject("SALT",
                                  [["STATE_COLOR", "ALL", "WHITE"],
                                   ["STATE_NAME_ADJ", "ALL_SOLID", "salt"],
                                   ["STATE_NAME_ADJ", "LIQUID", "molten salt"],
                                   ["STATE_NAME_ADJ", "GAS", "boiling salt"],
                                   ["BUILD_COLOR", "7", "0", "1"],
                                   ["TILE_COLOR", "7", "7", "1"],
                                   ["MATERIAL_VALUE", "10"],
                                   ["SPEC_HEAT", "854"],
                                   ["MELTING_POINT", "11442"],
                                   ["BOILING_POINT", "12637"],
                                   ["SOLID_DENSITY", "1200"],
                                   ["LIQUID_DENSITY", "1200"]]),
                        "UNKNOWN_SUBSTANCE":
                        RawObject("UNKNOWN_SUBSTANCE",
                                  [["STATE_COLOR", "ALL", "GRAY"],
                                   ["STATE_NAME_ADJ", "ALL_SOLID", "unknown frozen substance"],
                                   ["STATE_NAME_ADJ", "LIQUID", "unknown substance"],
                                   ["STATE_NAME_ADJ", "GAS", "unknown boiling substance"],
                                   ["STATE_NAME_ADJ", "SOLID_POWDER", "unknown frozen powder"],
                                   ["STATE_NAME_ADJ", "SOLID_PASTE", "unknown slush"],
                                   ["BUILD_COLOR", "7", "0", "0"],
                                   ["TILE_COLOR", "7", "7", "1"],
                                   ["SPEC_HEAT", "4181"],
                                   ["HEATDAM_POINT", "10180"],
                                   ["MELTING_POINT", "10000"],
                                   ["BOILING_POINT", "10180"],
                                   ["SOLID_DENSITY", "920"],
                                   ["LIQUID_DENSITY", "1000"]]),
                        "VOMIT":
                        RawObject("VOMIT",
                                  [["STATE_COLOR", "ALL", "DARK_GREEN"],
                                   ["STATE_NAME_ADJ", "ALL_SOLID", "vomit"],
                                   ["STATE_NAME_ADJ", "SOLID_PRESSED", "pressed vomit"],
                                   ["BASIC_COLOR", "2", "0"],
                                   ["BUILD_COLOR", "2", "0", "0"],
                                   ["TILE_COLOR", "7", "7", "1"],
                                   ["SPEC_HEAT", "4181"],
                                   ["HEATDAM_POINT", "10180"],
                                   ["SOLID_DENSITY", "1200"]]),
                        "WATER":
                        RawObject("WATER",
                                  [["STATE_COLOR", "ALL_SOLID", "WHITE"],
                                   ["STATE_NAME_ADJ", "ALL_SOLID", "ice"],
                                   ["STATE_COLOR", "LIQUID", "CLEAR"],
                                   ["STATE_NAME_ADJ", "LIQUID", "water"],
                                   ["STATE_COLOR", "GAS", "CLEAR"],
                                   ["STATE_NAME_ADJ", "GAS", "steam"],
                                   ["STATE_NAME_ADJ", "SOLID_POWDER", "snow"],
                                   ["STATE_NAME_ADJ", "SOLID_PASTE", "slush"],
                                   ["BASIC_COLOR", "1", "0"],
                                   ["BUILD_COLOR", "3", "0", "0"],
                                   ["TILE_COLOR", "7", "7", "1"],
                                   ["SPEC_HEAT", "4181"],
                                   ["MELTING_POINT", "10000"],
                                   ["BOILING_POINT", "10180"],
                                   ["SOLID_DENSITY", "920"],
                                   ["LIQUID_DENSITY", "1000"],
                                   ["EVAPORATES"]])}


# ====== misc. functions ===============================================================================================

def split_file_into_tokens(file):
    # does what it sounds like, splits a text file into tokens, discarding comments along the way
    token_list = []

    file_string = "".join(list(line for line in file))
    reading_mode = "comments"
    token = ""
    args = ""
    # just goes through each of the characters in the file, switching "reading_mode" when necessary.
    for c in file_string:
        if reading_mode == "comments":
            if c == "[":
                reading_mode = "token"
        elif reading_mode == "token":
            if c == ":":
                reading_mode = "args"
            elif c == "]":
                token_list.append([token])
                token = ""
                reading_mode = "comments"
            else:
                token += c
        elif reading_mode == "args":
            if c == "]":
                token_list.append([token] + args.split(":"))
                token = ""
                args = ""
                reading_mode = "comments"
            else:
                args += c

    return token_list


def read_and_load_all_raw_files(raw_path):
    global top_level_objects

    # finds the raw files
    rawfilenames = []
    for filename in os.listdir(raw_path):
        if filename.endswith(".txt"):
            rawfilenames.append(filename)

    # goes through all the raw files and finds the objects, puts them in top_level_objects.
    for i in range(len(rawfilenames)):
        # opens the file and splits it into tokens
        print("reading file " + str(i + 1) + "/" + str(len(rawfilenames)), rawfilenames[i])
        filename = rawfilenames[i]
        rawfile = open(raw_path + "/" + filename, "r", encoding="latin1")
        rawfile_tokens = split_file_into_tokens(rawfile)

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
                pos_object_types = object_types[token[1]]

            # if it's already reading an object, and it's not changing, append the current token to that object's
            # list of tokens
            elif reading_object and token[0] not in pos_object_types:
                object_token_list.append(token)

            # if it finds a new object or it is the last line in the file
            if token[0] in pos_object_types or j == len(rawfile_tokens) - 1:
                # finishes the current object before starting to read the next one
                if reading_object:
                    # makes sure the object type has a dict within top_level_objects
                    if object_type not in top_level_objects:
                        top_level_objects[object_type] = {}

                    if object_type == "CREATURE":
                        top_level_objects[object_type][object_id] = Creature(object_id, object_token_list, filename)
                    elif object_type == "PLANT":
                        top_level_objects[object_type][object_id] = Plant(object_id, object_token_list, filename)
                    elif object_type == "TISSUE_TEMPLATE":
                        # Note: the tissue templates are loaded as Tissue objects for easier handling later
                        top_level_objects[object_type][object_id] = Tissue(object_id, object_token_list, filename)
                    else:
                        top_level_objects[object_type][object_id] = RawObject(object_id, object_token_list, filename)

                if token[0] in pos_object_types:
                    object_type = token[0]
                    object_id = token[1]
                    object_token_list = []
                    reading_object = True


def can_get_top_level_object(object_type, object_id):
    try:
        top_level_objects[object_type][object_id]
    except KeyError:
        # if the object can't be found in top_level_objects, adds it to missing_top_level_objects
        if object_id not in missing_top_level_objects[object_type]:
            missing_top_level_objects[object_type].append(object_id)
    else:
        return True


def apply_creature_variation(new_tokens, insertion_index, cv_tokens, exclamation_args):
    # see: https://dwarffortresswiki.org/index.php/DF2014:Creature_variation_token
    # "Exclamation args" are the ones like !ARG1, !ARG2 etc.
    # does this work? maybe
    for i in range(len(exclamation_args)):
        exclamation_args[i] = exclamation_args[i].replace("|", ":")
    # sets up a dictionary for later insertions/replacements
    exclamation_arg_dict = {"!ARG" + str(i + 1): exclamation_args[i] for i in range(len(exclamation_args))}

    # "pending" list of tokens to remove
    pending_cv_remove_tokens = []
    # stuff for the cv converts
    pending_cv_converts = []
    inside_cv_convert = False
    cv_convert_master = None
    cv_convert_target = None
    cv_convert_replacement = None
    # "pending" list of tokens to add
    pending_cv_add_tokens = []

    for i in range(len(cv_tokens)):
        cv_token = cv_tokens[i]
        # inserts the exclamation args
        for exclamation_arg in exclamation_arg_dict:
            cv_token = [cv_token_arg.replace(exclamation_arg, exclamation_arg_dict[exclamation_arg])
                        for cv_token_arg in cv_token]

        # regarding the cv_converts
        if inside_cv_convert:

            if cv_token[0] == "CVCT_MASTER":
                # CVCT_MASTER does not just take the token name, it may also take the first arguments.
                # e.g. [CVCT_MASTER:BODY:HUMANOID] is just as valid as [CVCT_MASTER:BODY]
                # Note that it only takes full arguments, [CVCT_MASTER:BODY:HUMANOID] prepares a conversion of
                # [BODY:HUMANOID:...], not [BODY:HUMANOID_NECK:...] or [BODY:HUMANOID_LEGLESS:...].
                cv_convert_master = cv_token[1:]

            elif cv_token[0] == "CVCT_TARGET":
                cv_convert_target = ":".join(cv_token[1:])

            elif cv_token[0] == "CVCT_REPLACEMENT":
                cv_convert_replacement = ":".join(cv_token[1:])

            if i == len(cv_tokens) - 1 or cv_token[0] not in ["CVCT_MASTER", "CVCT_TARGET", "CVCT_REPLACEMENT"]:
                # they are appended normally here, but applied in "reverse order" later,
                # as they are in the actual game
                pending_cv_converts.append(CreatureVariationConvert(cv_convert_master,
                                                                    cv_convert_target,
                                                                    cv_convert_replacement))
                cv_convert_master = None
                cv_convert_target = None
                cv_convert_replacement = None
                inside_cv_convert = False

        if cv_token[0] in ["CV_ADD_TAG", "CV_NEW_TAG"]:
            # appends the token to pending_cv_add_tokens (but not "CV_ADD_TAG"/"CV_NEW_TAG")
            pending_cv_add_tokens.append(cv_token[1:])

        elif cv_token[0] == "CV_REMOVE_TAG":
            # appends the token to pending_cv_remove_tokens (but not "CV_REMOVE_TAG")
            pending_cv_remove_tokens.append(cv_token[1:])

        elif cv_token[0] == "CV_CONVERT_TAG":
            inside_cv_convert = True

        # These three "_CTAG" tokens are like the corresponding "_TAG" tokens above, but with the condition that
        # a numbered argument must be equal to a set value.
        # E.g. "[CV_ADD_CTAG:2:HUMANOID:CAN_TALK]" will only add CAN_TALK if the second argument is "HUMANOID".

        elif cv_token[0] in ["CV_ADD_CTAG", "CV_NEW_CTAG"]:
            try:
                int(cv_token[1])
            except ValueError:
                double_print("Incorrect usage of " + cv_token[0] + "; " + cv_token[1] + " is not an integer. "
                             + ":".join(cv_token),
                             output_file is not None)
            else:
                if exclamation_args[int(cv_token[1])-1] == cv_token[2]:
                    pending_cv_add_tokens.append(cv_token[3:])

        elif cv_token[0] == "CV_REMOVE_CTAG":
            try:
                int(cv_token[1])
            except ValueError:
                double_print("Incorrect usage of " + cv_token[0] + "; " + cv_token[1] + " is not an integer. "
                             + ":".join(cv_token),
                             output_file is not None)
            else:
                if exclamation_args[int(cv_token[1]) - 1] == cv_token[2]:
                    pending_cv_remove_tokens.append(cv_token[3:])

        elif cv_token[0] == "CV_CONVERT_CTAG":
            try:
                int(cv_token[1])
            except ValueError:
                double_print("Incorrect usage of " + cv_token[0] + "; " + cv_token[1] + " is not an integer. "
                             + ":".join(cv_token),
                             output_file is not None)
            else:
                if exclamation_args[int(cv_token[1]) - 1] == cv_token[2]:
                    # debug text:
                    # double_print(exclamation_args[int(cv_token[1]) - 1] + "==" + cv_token[2] +
                    #              "\t[" + ", ".join(exclamation_args) + "]",
                    #              output_file is not None)
                    inside_cv_convert = True

    # first, removal of marked tokens (in reverse order, from the "bottom")
    for cv_remove_token in reversed(pending_cv_remove_tokens):
        len_before = len(new_tokens)

        new_tokens = [new_token for new_token in new_tokens
                      if new_token[0:len(cv_remove_token)] != cv_remove_token]

        # adjusts insertion_index, makes sure it doesn't go negative
        insertion_index -= len(new_tokens) - len_before
        if insertion_index < 0:
            insertion_index = 0

    # second, applies cv_converts (in reverse order, from the "bottom")
    for cv_convert in reversed(pending_cv_converts):
        for i in range(len(new_tokens)):
            if new_tokens[i][0:len(cv_convert.master)] == cv_convert.master:
                # joins the args temporarily, so a series of args can be targeted for replacement
                args = ":".join(new_tokens[i][1:])
                if cv_convert.target in args:
                    args = args.replace(cv_convert.target, cv_convert.replacement)
                    new_tokens[i] = [new_tokens[i][0]] + [arg for arg in args.split(":") if arg != ""]
                # debug text:
                # double_print(cv_convert.target + " => " + cv_convert.replacement, True)

    # third, adding marked tokens (in non-reversed order, from the "top")
    for cv_add_token in pending_cv_add_tokens:
        # exclamation args containing a "|"/":" are split into before being added
        true_add_token = []
        for arg in cv_add_token:
            true_add_token += arg.split(":")
        new_tokens.insert(insertion_index, true_add_token)
        insertion_index += 1

    # and finally makes sure these two are updated
    return new_tokens, insertion_index


# ====== output stuff ==================================================================================================

def initialize_output_file(output_file_name, output_path, raw_path):
    global output_file, old_file_string
    # gets a copy of the current (pre-running the program) state of the output file, so it can shift it down later
    if os.path.isfile(os.getcwd() + output_file_name):
        old_file_string = open(output_path + output_file_name, "r").read()
    else:
        old_file_string = ""
    # initiaties the writing of the output file
    output_file = open(os.getcwd() + output_file_name, "w")
    output_file.write("Output from " + raw_path + " " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + " :\n")


def double_print(string, use_output_file):
    # prints both normally and writes to the output file
    global output_file
    print(string)
    if use_output_file:
        output_file.write(string + "\n")


def either_print(string, use_output_file):
    # either writes to the output file, or prints normally
    global output_file
    if use_output_file:
        output_file.write(string + "\n")
    else:
        print(string)


def flush_output_file(use_output_file):
    if use_output_file:
        output_file.flush()


def close_output_file(use_output_file):
    if use_output_file:
        output_file.write(
            "\n--------------------------------------------------------------------------------------------------------"
            "----------------------------------------\n")
        output_file.write(old_file_string)
        output_file.flush()
        output_file.close()


def report_missing_top_level_objects(object_type, use_output_file):
    if len(missing_top_level_objects[object_type]) == 1:
        double_print(object_type + " object " + missing_top_level_objects[object_type][0] +
                     " could not be found. Put its definitions in your raws folder for a more accurate output.",
                     use_output_file)
    elif len(missing_top_level_objects[object_type]) > 1:
        double_print(object_type + " objects " + ", ".join(missing_top_level_objects[object_type]) +
                     " could not be found. Put their definitions in your raws folder for a more accurate output.",
                     use_output_file)


# ====== non-static stuff ==============================================================================================

# a dictionary with empty sub-dicts as values and object_types as keys
# i.e. {"BODY_DETAIL_PLAN": {}, "BODY": {}, "BUILDING": {} ... "TISSUE_TEMPLATE": {}}"
top_level_objects = {object_type: {}
                     for object_type in
                     # this just flattens the list of object_types.values()
                     [val for sublist in object_types.values() for val in sublist]}

# for nicer-looking error messages
missing_top_level_objects = {object_type: []
                             for object_type in
                             [val for sublist in object_types.values() for val in sublist]}

output_file = None
old_file_string = ""
