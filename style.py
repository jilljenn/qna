color = {
    '3': 'red',
    '4': 'orangered',
    '5': 'orange',
    '6': 'yellow',
    '8': 'blue',
    'irt': 'red',
    'mepv-irt': 'darkblue',
    'baseline': 'darkgreen',
    '888': 'green',
    'mirt': 'red',
    'qm': 'blue',
    'qm-qmatrix-cdm': 'green',
    'mirt-qm-matrix-cdm-new': 'gold',
    'random': 'blue',
    'dpp': 'red',
    'cat': 'green',
    'uncertainty': 'black'
}

fmt = {
    'irt': '.',
    'mirt-qm-qmatrix-cdm': '+',
    'mirt-qm-qmatrix-cdm-new': 's',
    'mirt': '^',
    'qm': '^',
    'dpp': '+',
    'random': '^',
    'cat': 'o',
    'uncertainty': '.'
}

main_label = {
    'irt': 'Rasch',
    'qm-qmatrix-cdm': 'DINA',
    'mirt': 'MIRT',
    'qm': 'DINA auto',
    'cat': 'CAT',
    'dpp': 'InitialD',
    'uncertainty': 'Uncertainty',
    'random': 'Random'
}

# linewidth = {'mirt': 5, '888': 3, '8': 3, 'irt': 1, 'qm': 3, 'qm-qmatrix-cdm': 3, 'mirt-qm-qmatrix-cdm': 5, 'mirt-qm-qmatrix-cdm-new': 7, 'mirt-qm-qmatrix-cdm-new': 7}
main_linewidth = {'irt': 2, 'mirt-qm-qmatrix-cdm-new': 3}
for qmatrix_name in ['cdm', 'ecpe', 'ecpe2', 'banach', 'fraction', 'fraction2', 'custom', 'cdm-new', 'fake', 'timss2003', 'timss2003b', 'castor6e', 'castor6e2', 'sat', 'sat2', 'sat3', 'sat4']:
    for prefix in ['qm', 'mirt-qm']:
        tag = '%s-qmatrix-%s' % (prefix, qmatrix_name)
        color[tag] = 'red' if prefix == 'mirt-qm' else 'green'
        # linewidth[tag] = 5 if prefix == 'mirt-qm' else 3
        main_label[tag] = 'GenMA' if prefix == 'mirt-qm' else 'DINA'
        fmt[tag] = 'o' if prefix == 'mirt-qm' else '+'
main_label['mirt-qm-qmatrix-cdm-new'] = 'GenMA + auto'

def get_label(name, dim):
    label = main_label[name]
    if name.startswith('qm') or name.startswith('mirt'):
        label += ' K = %s' % dim
    return label
