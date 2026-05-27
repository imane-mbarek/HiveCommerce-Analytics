# Create your views here.
from django.shortcuts import render
from .queries import (
    get_top_produits, get_chiffre_affaires,
    get_clients_fideles, get_ventes_par_mois,
    get_repartition_statuts, get_notes_moyennes
)

def dashboard(request):
    context = {
        'kpis'           : get_chiffre_affaires(),
        'top_produits'   : get_top_produits(10),
        'clients_fideles': get_clients_fideles(10),
        'ventes_mois'    : get_ventes_par_mois(),
        'statuts'        : get_repartition_statuts(),
        'notes'          : get_notes_moyennes(),
    }
    return render(request, 'dashboard/index.html', context)