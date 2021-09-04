import iotbx.cif,sys,re

# Dictionaries to convert CIF strings into LaTeX. You will need to add to these!

spaceGroups = {
    'P 1': 'P1',
    'P -1': 'P\\bar{1}',
    'P 1 21 1': 'P2_{1}',
    'P 1 21/a 1': 'P2_{1}/a',
    'P 1 21/c 1': 'P2_{1}/c',
    'P 1 21/n 1': 'P2_{1}/n',
    'C 1 c 1': 'Cc'
    }

radiation = {
    'Cu K\\a': '\\ce{Cu K\\alpha}',
    'Mo K\\a': '\\ce{Mo K\\alpha}'
    }

if len(sys.argv) == 1:
    print("Please provide a cif file to read.")

else:
    f = open(sys.argv[1], 'r')
    cifFile = f.read()

    if len(sys.argv) == 2:
        datablock = re.search('data_.*', cifFile)[0].split('data_')[1]
        print(f'Using the first datablock {datablock} in the cif file {f.name}.\n')
        cif = iotbx.cif.reader(input_string=cifFile).model()[datablock]

    elif len(sys.argv) == 3:
        datablock = sys.argv[2]
        try:
            cif = iotbx.cif.reader(input_string=cifFile).model()[datablock]
        except:
            print(f'Could not find the datablock with name {datablock} in the cif file {f.name}.')
            sys.exit(1)

    f.close()

formula = f"\ce{{{cif['_chemical_formula_moiety']}}}"
molecular_weight = f"\(M = {cif['_chemical_formula_weight']}\)~g/mol"
crystal_system = f"{cif['_space_group_crystal_system']}"
space_group_symbol = f"\(\mathrm{{{spaceGroups[cif['_space_group_name_H-M_alt']]}}}\)"
space_group_number = f"no. {cif['_space_group_IT_number']}"

# This may need modification for higher symmetry crystal systems
cell_a = f"\( a = {cif['_cell_length_a']}\)~\AA{{}}, "
cell_b = f"\( b = {cif['_cell_length_b']}\)~\AA{{}}, "
cell_c = f"\( c = {cif['_cell_length_c']}\)~\AA{{}}, "

if cif['_space_group_crystal_system'] == 'triclinic':
    cell_alpha = f"\( \\alpha = {cif['_cell_angle_alpha']}\)~\degree{{}}, "
    cell_beta = f"\( \\beta = {cif['_cell_angle_beta']}\)~\degree{{}}, "
    cell_gamma = f"\( \\gamma = {cif['_cell_angle_gamma']}\)~\degree{{}}, "
elif cif['_space_group_crystal_system'] == 'monoclinic':
    cell_alpha = f""
    cell_beta = f"\( \\beta = {cif['_cell_angle_beta']}\)~\degree{{}}, "
    cell_gamma = f""
elif cif['_space_group_crystal_system'] == 'orthorhombic':
    cell_alpha = f""
    cell_beta = f""
    cell_gamma = f""
else:
    cell_alpha = f"\( \\alpha = {cif['_cell_angle_alpha']}\)~\degree{{}}, "
    cell_beta = f"\( \\beta = {cif['_cell_angle_beta']}\)~\degree{{}}, "
    cell_gamma = f"\( \\gamma = {cif['_cell_angle_gamma']}\)~\degree{{}}, "

refln_expression = cif['_reflns_threshold_expression'].replace('\s', '\sigma')

# Generate the cif report as a string
report = (f"Crystal Data for {formula} ({molecular_weight}): "
f"{crystal_system}, space group {space_group_symbol} ({space_group_number}), "
f"{cell_a}"
f"{cell_b}"
f"{cell_c}"
f"{cell_alpha}"
f"{cell_beta}"
f"{cell_gamma}"
#Tidy this up when I can be bothered
f"\( V = {cif['_cell_volume']} \)~\AA{{}}\(^3\), "
f"\( Z = {cif['_cell_formula_units_Z']} \), "  
f"\( T = {cif['_diffrn_ambient_temperature']}\)~K, "
f"\( \mu ( {radiation[cif['_diffrn_radiation_type']]} ) = {cif['_exptl_absorpt_coefficient_mu']}\)~mm\(^{{-1}}\), "
f"\( D_{{calc}} = {cif['_exptl_crystal_density_diffrn']}\)~g\(\cdot\)cm\(^{{-3}}\), "
f"{cif['_diffrn_reflns_number']} reflections measured ({cif['_diffrn_reflns_theta_min']}\\degree{{}} \(\\leq 2\\theta \\leq\) {cif['_diffrn_reflns_theta_max']}\\degree{{}}), "
f"{cif['_reflns_number_total']} unique (\(R_{{\mathrm{{int}}}} = {cif['_diffrn_reflns_av_R_equivalents']} \), \(R_{{\mathrm{{sigma}}}} = {cif['_diffrn_reflns_av_unetI/netI']} \)) which were used in all calculations. "
f"The final \(R_1\) was {cif['_refine_ls_R_factor_gt']} \( ({refln_expression}) \) and \(wR_2\) was {cif['_refine_ls_wR_factor_ref']} (all data).")

print(report)

with open(f"{datablock}.tex", 'w') as outfile:
    outfile.write("\\documentclass{minimal}\n\\usepackage{mhchem,amssymb,gensymb,newtxtext,newtxmath}\n\n\\begin{document}\n")
    outfile.write(report)
    outfile.write("\n\\end{document}\n")



