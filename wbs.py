# import sys
import argparse  # Parsing input line
#
from datetime import datetime
#
import logging

#
from bottle import Bottle, run, view, static_file, post, request
#
import parser as gpsparse
#
import pandas
FORMAT = 'DEBUG : %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('debug')
#


def runBottle(users, runtype='prod'):
    """
    stats = (km_y, km_w, num_activities_y, num_activities_w,start_y,km_t)
    """
    usr_id = {'Thomas' : 1, 'Elise':2}
    inv_usr_id = {v: k for k, v in usr_id.items()}

    # for usr in users : 
        # __stats = users[usr][0]
        # __image = users[usr][1]
    __runtype = runtype
        # global __user 
        
    # __user = usr_id[usr]
    __user = 'test'
    app = Bottle()

    @app.route('/:mon_id', method=['GET'])
    @view('template.tpl')
    def hello(mon_id, from_post=True,test=__user):
        hstats = users[inv_usr_id[int(mon_id)]][0]
        himage = users[inv_usr_id[int(mon_id)]][1]
        results   = users[inv_usr_id[int(mon_id)]][2]
        head   = results.head(5)

        pandas.set_option('display.max_colwidth', -1)
        head['Map']=head.apply(lambda row: '<form action="" method="post" target="votar"> \
                     <button onclick="on()" class="button-primary" name="maps" value="%s">Show</button> \
                     </form>'%row.File_Name, axis=1)
        cols = ['Date', 'Length', 'Time', 'Ave_Speed','UpHill', 'Map']
        to_print = head[cols].copy()
        km_ym1 = results[results.Year == 2017]['Length'].sum()
        print 'km_ym1',km_ym1
        context = {'date': datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
                   'images': himage,
                   'km_y': hstats[0],
                   # 'km_w': hstats[1],
                   'num_activities_y': hstats[1],
                   # 'num_activities_w': hstats[3],
                   # 'start_y': hstats[4],
                   'km_t': hstats[2],
                   'test': test,
                   'head': to_print.to_html(escape=False),
                   'km_ym1':km_ym1}
        return (context)

    # @post('/')  # or @route('/login', method='POST')
    @app.route('/:mon_id', method=['POST'])
    def do_update(mon_id):
        
        print 'do_update'
        # pst_rtrn = 'rate'
        # print mon_id
        __user = inv_usr_id[int(mon_id)]
        # print __user
        # print request.POST.get('maps','').strip()
        # request.POST.get('maps')
        if request.POST.get('foo','').strip():
            data = gpsparse.globalRun(__runtype, __user)
            return hello(data, True, 'updated')
        #     pst_rtrn = 'Updated'
        # elif request.POST.get('bar','').strip():
        #     # if __user == 'Thomas':
        #     #   __user = 'Elise'
        #     #   stats_up, figs_up = gpsparse.globalRun(__runtype,__user)
        #     #   pst_rtrn = 'Elise'
        #     # else : 
        #     stats_up, figs_up = gpsparse.globalRun(__runtype,__user)
        #     pst_rtrn = __user
        if request.POST.get('maps','').strip():
            gpsparse.leaflet(request.POST.get('maps'))
            return

        # return hello(stats_up, figs_up, True, pst_rtrn)
        return

    @app.route('/static/<filepath:path>')
    def server_static(filepath):
        return static_file(filepath, root='./skeleton')

    @app.route('/images/<filename:re:.*\.png>')
    def send_image(filename):
        return static_file(filename,
                           root='./skeleton/images',
                           mimetype='image/png')

    run(app, host='localhost', port=8080, reloader=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("runtype", help="Test or prod")
    # parser.add_argument("user", default='Thomas', help="Test or prod")
    args = parser.parse_args()
    usr_lst = ['Thomas', 'Elise']
    # usr_lst = ['Thomas']
    usr_dic = {}
    for usr in usr_lst :
      usr_dic[usr] = gpsparse.globalRun(args.runtype, usr)
    runBottle(usr_dic,args.runtype)
