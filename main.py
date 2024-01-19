from Smartool.results.operator import Operator

sumitomo = Operator()
sumitomo.db_info = {'username' : 'root',
                    'password' : 'tassio25789',
                    'hostname' : '127.0.0.1'}

cont = 1
while(1):
    if sumitomo.read_db() == 0:
        break
    sumitomo.treat_data()
    sumitomo.separate_by_zeros()
    sumitomo.define_cycles()
    sumitomo.flag_rest()
    sumitomo.get_results_cycle()
    sumitomo.insert_in_db()

    cont += 1
    print(cont)