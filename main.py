from results.operator import Operator
# from Smartool.results.operator import Operator
#import matplotlib.pyplot as plt

sumitomo = Operator()
sumitomo.db_info = {'username' : 'root',
                    'password' : '',
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
    print(sumitomo.results)

    print(cont)
    cont += 1
    #plt.xlabel('Samples')
    #plt.ylabel('m/s')
    #plt.show()