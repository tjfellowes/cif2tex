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
    'Cu K\\a': 'Cu K \\alpha ',
    'Mo K\\a': 'Mo K \\alpha '
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
    cell_alpha = f"\( \\alpha = {cif['_cell_angle_alpha']}\)\degree{{}}, "
    cell_beta = f"\( \\beta = {cif['_cell_angle_beta']}\)\degree{{}}, "
    cell_gamma = f"\( \\gamma = {cif['_cell_angle_gamma']}\)\degree{{}}, "
elif cif['_space_group_crystal_system'] == 'monoclinic':
    cell_alpha = f""
    cell_beta = f"\( \\beta = {cif['_cell_angle_beta']}\)\degree{{}}, "
    cell_gamma = f""
elif cif['_space_group_crystal_system'] == 'orthorhombic':
    cell_alpha = f""
    cell_beta = f""
    cell_gamma = f""
else:
    cell_alpha = f"\( \\alpha = {cif['_cell_angle_alpha']}\)\degree{{}}, "
    cell_beta = f"\( \\beta = {cif['_cell_angle_beta']}\)\degree{{}}, "
    cell_gamma = f"\( \\gamma = {cif['_cell_angle_gamma']}\)\degree{{}}, "

cell_volume = f"{cif['_cell_volume']}~\\text{{\AA{{}}}}^3"
cell_z = f"{cif['_cell_formula_units_Z']}"
temperature = f"{cif['_diffrn_ambient_temperature']}~\\text{{K}}"

radiation = "\\mathrm{" + cif['_diffrn_radiation_type'].replace('\\a', '\\alpha').replace(' ', '~') + "}"
mu = f"{cif['_exptl_absorpt_coefficient_mu']}~\\text{{mm}}^{{-1}}"
density = f"{cif['_exptl_crystal_density_diffrn']}~\\text{{g}} \cdot \\text{{cm}} ^{{-3}}"

refln_measured = f"{cif['_diffrn_reflns_number']}"
theta_range = f"\({cif['_diffrn_reflns_theta_min']}\)\\degree{{}} \(\\leq 2\\theta \\leq {cif['_diffrn_reflns_theta_max']}\)\\degree{{}}"

refln_unique = f"{cif['_reflns_number_total']}"
r_int = f"\( R_{{\mathrm{{int}}}} = {cif['_diffrn_reflns_av_R_equivalents']} \)"
r_sigma = f"\(R_{{\mathrm{{sigma}}}} = {cif['_diffrn_reflns_av_unetI/netI']} \)"

r_1 = f"{cif['_refine_ls_R_factor_gt']}"
wr_2 = f"{cif['_refine_ls_wR_factor_ref']}"
refln_expression = "\(" + cif['_reflns_threshold_expression'].replace('\s', '\sigma') + "\)"

# Generate the cif report as a string
report = (f"Crystal Data for {formula} ({molecular_weight}): "
f"{crystal_system}, space group {space_group_symbol} ({space_group_number}), "
f"{cell_a}"
f"{cell_b}"
f"{cell_c}"
f"{cell_alpha}"
f"{cell_beta}"
f"{cell_gamma}"
f"\( V = {cell_volume} \), "
f"\( Z = {cell_z} \), "  
f"\( T = {temperature} \), "
f"\( \mu({radiation}) = {mu} \), "
f"\( D_{{\\text{{calc}}}} = {density} \), "
f"{refln_measured} reflections measured ({theta_range}), "
f"{refln_unique} unique ({r_int}, {r_sigma}) which were used in all calculations. "
f"The final \(R_1\) was {r_1} ({refln_expression}) and \(wR_2\) was {wr_2} (all data).")

print(report)

with open(f"{datablock}.tex", 'w') as outfile:
    outfile.write("\\documentclass{minimal}\n\\usepackage{mhchem,amssymb,gensymb,newtxtext,newtxmath}\n\n\\begin{document}\n")
    outfile.write(report)
    outfile.write("\n\\end{document}\n")



