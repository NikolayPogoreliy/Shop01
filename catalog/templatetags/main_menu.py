from django import template
register = template.Library()

from catalog.models import Category



@register.simple_tag
def main_menu():
    cats = Category.objects.filter(level=0)#Будут отображены в навигационном меню L0
    dictl1 = {}
    dictl0 = {}
    for cat in cats:
        subcats_l1 = cat.get_children() #L1
        for subcat_l1 in subcats_l1:
            subcats_l2 = subcat_l1.get_children()#L2
            dictl1.update({subcat_l1:subcats_l2})
        dictl0[cat]=dictl1
        dictl1 = {}
    #subcats = [[cat,Category.objects.filter(parent=cat)] for cat in cats]
    subcats = {cat: Category.objects.filter(parent=cat) for cat in cats}
    return {'cats':cats, 'subcats':subcats, 'tree_to_L2': dictl0}
